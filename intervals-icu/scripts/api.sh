#!/bin/bash
# Intervals.icu API Helper
# Usage: ./api.sh <command> [args...]
#
# Required environment variables:
#   INTERVALS_API_KEY    - Your API key from intervals.icu/settings
#   INTERVALS_ATHLETE_ID - Your athlete ID (e.g., i12345)

set -euo pipefail

BASE_URL="https://intervals.icu/api/v1"

# Error helper for readable messages
die() {
    echo "Error: $1" >&2
    [[ -n "${2:-}" ]] && echo "$2" >&2
    exit 1
}

# Check for help first (doesn't require credentials)
if [[ "${1:-}" == "help" || "${1:-}" == "--help" || "${1:-}" == "-h" || -z "${1:-}" ]]; then
    cat << 'EOF'
Intervals.icu API Helper

Usage: ./api.sh <command> [args...]

Commands:
  wellness [date]              Get wellness for date (default: today)
  wellness-range <start> <end> [format]
                               Get wellness for date range (format: json|csv)
  wellness-update <date> <json>
                               Update wellness fields
  activities <start> <end> [format] [--all]
                               List activities in date range
                               format: json|csv, --all: fetch all pages
  activity <id>                Get single activity details
  activity-streams <id> [types]
                               Get activity data streams
  activity-last [count]        Get most recent activity(s) (default: 1)
  activity-upload <file>       Upload activity (.fit, .gpx, .tcx)
  activity-delete <id>         Delete activity (requires INTERVALS_CONFIRM_DELETE=yes)
  athlete                      Get athlete profile
  zones                        Get power/HR zone settings
  fitness                      Get current CTL/ATL/TSB
  events <start> <end>         Get planned events/workouts
  event-create <date> <json>   Create planned workout/event
  event-update <id> <json>     Update existing event
  event-delete <id>            Delete event (requires INTERVALS_CONFIRM_DELETE=yes)
  power-curves <start> <end> [format]
                               Get power duration curves
                               format: json|summary|<seconds>
  help                         Show this help

Date formats:
  - ISO format: 2024-01-15
  - today, yesterday

Examples:
  ./api.sh wellness
  ./api.sh wellness 2024-01-15
  ./api.sh wellness-update today '{"weight": 72.5, "sleepSecs": 28800}'
  ./api.sh activities 2024-01-01 2024-01-31
  ./api.sh activities 2024-01-01 2024-01-31 csv > activities.csv
  ./api.sh fitness

Environment variables:
  INTERVALS_API_KEY    - Your API key (required)
  INTERVALS_ATHLETE_ID - Your athlete ID (required)
  INTERVALS_DRY_RUN    - Set to 'true' to preview destructive operations

Setup:
  export INTERVALS_API_KEY="your_api_key"
  export INTERVALS_ATHLETE_ID="iXXXXX"
EOF
    exit 0
fi

# Check required environment variables
if [[ -z "${INTERVALS_API_KEY:-}" ]]; then
    echo "Error: INTERVALS_API_KEY not set" >&2
    echo "Get your API key from https://intervals.icu/settings → Developer Settings" >&2
    exit 1
fi

if [[ -z "${INTERVALS_ATHLETE_ID:-}" ]]; then
    echo "Error: INTERVALS_ATHLETE_ID not set" >&2
    echo "Find your athlete ID in the URL: intervals.icu/athlete/iXXXXX/..." >&2
    exit 1
fi

# Build auth header
AUTH="Authorization: Basic $(echo -n "API_KEY:$INTERVALS_API_KEY" | base64)"

# Dry-run mode for testing destructive operations
DRY_RUN="${INTERVALS_DRY_RUN:-false}"

# Retry wrapper with exponential backoff
# Usage: retry_curl [curl args...]
retry_curl() {
    local max_attempts="${INTERVALS_MAX_RETRIES:-3}"
    local attempt=1
    local delay=1
    local response

    while [ $attempt -le $max_attempts ]; do
        if response=$(curl "$@" 2>/dev/null); then
            echo "$response"
            return 0
        fi

        if [ $attempt -lt $max_attempts ]; then
            echo "Attempt $attempt failed, retrying in ${delay}s..." >&2
            sleep $delay
            delay=$((delay * 2))
        fi
        attempt=$((attempt + 1))
    done

    echo "Error: Request failed after $max_attempts attempts" >&2
    return 1
}

# Helper function for GET requests with error handling
api_get() {
    local endpoint="$1"
    local response http_code body

    # Capture response and HTTP code
    response=$(retry_curl -s -w "\n%{http_code}" -H "$AUTH" -H "Content-Type: application/json" "${BASE_URL}${endpoint}")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    # Check for HTTP errors with detailed message
    if [[ "$http_code" -ge 400 ]]; then
        local error_msg="API error HTTP $http_code"

        # Try to extract error message from JSON response
        if command -v jq &>/dev/null; then
            local api_error
            api_error=$(echo "$body" | jq -r '.message // .error // empty' 2>/dev/null)
            [[ -n "$api_error" ]] && error_msg="$error_msg: $api_error"
        fi

        echo "Error: $error_msg" >&2

        # Provide helpful hints for common errors
        case "$http_code" in
            401) echo "Hint: Check your INTERVALS_API_KEY is correct" >&2 ;;
            403) echo "Hint: You may not have permission for this resource" >&2 ;;
            404) echo "Hint: Resource not found - check ID or date format" >&2 ;;
            429) echo "Hint: Rate limited - wait before retrying" >&2 ;;
        esac

        return 1
    fi

    echo "$body"
}

# Helper function for PUT requests with error handling
api_put() {
    local endpoint="$1"
    local data="$2"
    local response http_code body

    response=$(retry_curl -s -w "\n%{http_code}" -X PUT -H "$AUTH" -H "Content-Type: application/json" -d "$data" "${BASE_URL}${endpoint}")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    # Check for HTTP errors with detailed message
    if [[ "$http_code" -ge 400 ]]; then
        local error_msg="API error HTTP $http_code"

        # Try to extract error message from JSON response
        if command -v jq &>/dev/null; then
            local api_error
            api_error=$(echo "$body" | jq -r '.message // .error // empty' 2>/dev/null)
            [[ -n "$api_error" ]] && error_msg="$error_msg: $api_error"
        fi

        echo "Error: $error_msg" >&2

        # Provide helpful hints for common errors
        case "$http_code" in
            401) echo "Hint: Check your INTERVALS_API_KEY is correct" >&2 ;;
            403) echo "Hint: You may not have permission for this resource" >&2 ;;
            404) echo "Hint: Resource not found - check ID or date format" >&2 ;;
            429) echo "Hint: Rate limited - wait before retrying" >&2 ;;
        esac

        return 1
    fi

    echo "$body"
}

# Helper function for POST requests with error handling
api_post() {
    local endpoint="$1"
    local data="$2"
    local response http_code body

    response=$(retry_curl -s -w "\n%{http_code}" -X POST -H "$AUTH" -H "Content-Type: application/json" -d "$data" "${BASE_URL}${endpoint}")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    # Check for HTTP errors with detailed message
    if [[ "$http_code" -ge 400 ]]; then
        local error_msg="API error HTTP $http_code"

        # Try to extract error message from JSON response
        if command -v jq &>/dev/null; then
            local api_error
            api_error=$(echo "$body" | jq -r '.message // .error // empty' 2>/dev/null)
            [[ -n "$api_error" ]] && error_msg="$error_msg: $api_error"
        fi

        echo "Error: $error_msg" >&2

        # Provide helpful hints for common errors
        case "$http_code" in
            401) echo "Hint: Check your INTERVALS_API_KEY is correct" >&2 ;;
            403) echo "Hint: You may not have permission for this resource" >&2 ;;
            404) echo "Hint: Resource not found - check ID or date format" >&2 ;;
            429) echo "Hint: Rate limited - wait before retrying" >&2 ;;
        esac

        return 1
    fi

    echo "$body"
}

# Helper function for file uploads
api_upload() {
    local endpoint="$1"
    local file="$2"
    local response http_code body

    response=$(retry_curl -s -w "\n%{http_code}" -X POST -H "$AUTH" -F "file=@$file" "${BASE_URL}${endpoint}")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [[ "$http_code" -ge 400 ]]; then
        echo "Error: API returned HTTP $http_code" >&2
        echo "$body" >&2
        return 1
    fi

    echo "$body"
}

# Helper function for DELETE requests with error handling
api_delete() {
    local endpoint="$1"
    local response http_code body

    response=$(retry_curl -s -w "\n%{http_code}" -X DELETE -H "$AUTH" -H "Content-Type: application/json" "${BASE_URL}${endpoint}")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    # Check for HTTP errors with detailed message
    if [[ "$http_code" -ge 400 ]]; then
        local error_msg="API error HTTP $http_code"

        # Try to extract error message from JSON response
        if command -v jq &>/dev/null; then
            local api_error
            api_error=$(echo "$body" | jq -r '.message // .error // empty' 2>/dev/null)
            [[ -n "$api_error" ]] && error_msg="$error_msg: $api_error"
        fi

        echo "Error: $error_msg" >&2

        # Provide helpful hints for common errors
        case "$http_code" in
            401) echo "Hint: Check your INTERVALS_API_KEY is correct" >&2 ;;
            403) echo "Hint: You may not have permission for this resource" >&2 ;;
            404) echo "Hint: Resource not found - check ID" >&2 ;;
            429) echo "Hint: Rate limited - wait before retrying" >&2 ;;
        esac

        return 1
    fi

    echo "$body"
}

# Check if operation should be executed or just previewed
check_dry_run() {
    local operation="$1"
    local details="$2"

    if [[ "$DRY_RUN" == "true" || "$DRY_RUN" == "1" ]]; then
        echo "[DRY-RUN] Would execute: $operation" >&2
        echo "[DRY-RUN] Details: $details" >&2
        return 1
    fi
    return 0
}

# Parse date helper (supports "today", "yesterday", or ISO date)
# Cross-platform: works on macOS (BSD) and Linux (GNU)
parse_date() {
    local input="${1:-today}"
    case "$input" in
        today)
            date +%Y-%m-%d
            ;;
        yesterday)
            # Try macOS first, fall back to GNU
            date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d
            ;;
        *)
            echo "$input"
            ;;
    esac
}

# Validate JSON data before sending
validate_json() {
    local data="$1"
    local context="${2:-data}"

    if ! command -v jq &>/dev/null; then
        # Skip validation if jq not available
        return 0
    fi

    if ! echo "$data" | jq -e . &>/dev/null; then
        echo "Error: Invalid JSON in $context" >&2
        echo "Received: $data" >&2
        echo "Tip: Validate with: echo '$data' | jq ." >&2
        return 1
    fi

    return 0
}

# Commands
cmd_wellness() {
    local date
    date=$(parse_date "${1:-today}")
    api_get "/athlete/$INTERVALS_ATHLETE_ID/wellness/$date"
}

cmd_wellness_range() {
    [[ -z "${1:-}" ]] && die "Start date required" "Usage: api.sh wellness-range <start> <end>"
    [[ -z "${2:-}" ]] && die "End date required" "Usage: api.sh wellness-range <start> <end>"
    local start="$1"
    local end="$2"
    local format="${3:-json}"

    if [[ "$format" == "csv" ]]; then
        api_get "/athlete/$INTERVALS_ATHLETE_ID/wellness.csv?oldest=$start&newest=$end"
    else
        api_get "/athlete/$INTERVALS_ATHLETE_ID/wellness?oldest=$start&newest=$end"
    fi
}

cmd_wellness_update() {
    [[ -z "${1:-}" ]] && die "Date required" "Usage: api.sh wellness-update <date> <json>"
    [[ -z "${2:-}" ]] && die "JSON data required" "Usage: api.sh wellness-update <date> '{\"field\": value}'"
    local date
    date=$(parse_date "$1")
    local data="$2"

    validate_json "$data" "wellness update" || return 1

    api_put "/athlete/$INTERVALS_ATHLETE_ID/wellness/$date" "$data"
}

cmd_activities() {
    [[ -z "${1:-}" ]] && die "Start date required" "Usage: api.sh activities <start> <end> [format]"
    [[ -z "${2:-}" ]] && die "End date required" "Usage: api.sh activities <start> <end> [format]"
    local start="$1"
    local end="$2"
    local format="${3:-json}"
    local all_flag="${4:-}"

    # Check if --all flag is passed (either as 3rd or 4th argument)
    if [[ "$format" == "--all" ]]; then
        all_flag="--all"
        format="json"
    fi

    if [[ "$all_flag" == "--all" ]]; then
        cmd_activities_paginated "$start" "$end"
    elif [[ "$format" == "csv" ]]; then
        api_get "/athlete/$INTERVALS_ATHLETE_ID/activities.csv?oldest=$start&newest=$end"
    else
        api_get "/athlete/$INTERVALS_ATHLETE_ID/activities?oldest=$start&newest=$end"
    fi
}

cmd_activities_paginated() {
    local start="$1"
    local end="$2"
    local page_size=100
    local max_pages="${INTERVALS_MAX_PAGES:-50}"
    local page=0
    local all_results="[]"

    # Check jq dependency
    if ! command -v jq &>/dev/null; then
        echo "Error: jq is required for pagination (--all flag)" >&2
        echo "Install: brew install jq (macOS) or apt install jq (Linux)" >&2
        return 1
    fi

    while [[ $page -lt $max_pages ]]; do
        local response
        response=$(api_get "/athlete/$INTERVALS_ATHLETE_ID/activities?oldest=$start&newest=$end&page=$page&pageSize=$page_size") || return 1

        # Check if response is valid JSON array
        if ! echo "$response" | jq -e 'type == "array"' &>/dev/null; then
            echo "Error: Unexpected response format" >&2
            return 1
        fi

        local count
        count=$(echo "$response" | jq 'length')

        # Merge results
        all_results=$(echo "$all_results" "$response" | jq -s '.[0] + .[1]')

        # If we got fewer items than page size, we've reached the end
        if [[ $count -lt $page_size ]]; then
            break
        fi

        ((page++))
    done

    if [[ $page -ge $max_pages ]]; then
        echo "Warning: Reached maximum page limit ($max_pages pages, $((max_pages * page_size)) activities)" >&2
    fi

    echo "$all_results"
}

cmd_activity() {
    [[ -z "${1:-}" ]] && die "Activity ID required" "Usage: api.sh activity <id>"
    local id="$1"
    api_get "/activity/$id"
}

cmd_activity_streams() {
    [[ -z "${1:-}" ]] && die "Activity ID required" "Usage: api.sh activity-streams <id> [types]"
    local id="$1"
    local types="${2:-watts,heartrate,cadence,time}"
    api_get "/activity/$id/streams?types=$types"
}

cmd_activity_last() {
    # Check jq dependency
    if ! command -v jq &>/dev/null; then
        echo "Error: jq is required for activity-last" >&2
        return 1
    fi

    local count="${1:-1}"
    local today
    today=$(date +%Y-%m-%d)
    local month_ago
    month_ago=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d "30 days ago" +%Y-%m-%d)

    local response
    response=$(api_get "/athlete/$INTERVALS_ATHLETE_ID/activities?oldest=$month_ago&newest=$today") || return 1

    if [[ "$count" == "1" ]]; then
        echo "$response" | jq '.[0]'
    else
        echo "$response" | jq ".[:$count]"
    fi
}

cmd_activity_upload() {
    [[ -z "${1:-}" ]] && die "File required" "Usage: api.sh activity-upload <file.fit|file.gpx|file.tcx>"
    local file="$1"

    [[ ! -f "$file" ]] && die "File not found: $file"

    # Validate file extension
    local ext="${file##*.}"
    case "$ext" in
        fit|FIT|gpx|GPX|tcx|TCX)
            ;;
        *)
            die "Unsupported file type: .$ext" "Supported: .fit, .gpx, .tcx"
            ;;
    esac

    api_upload "/athlete/$INTERVALS_ATHLETE_ID/activities" "$file"
}

cmd_activity_delete() {
    [[ -z "${1:-}" ]] && die "Activity ID required" "Usage: api.sh activity-delete <id>"
    local id="$1"

    # Check dry-run first
    if ! check_dry_run "DELETE activity" "$id"; then
        return 0
    fi

    # Safety check - require confirmation via environment variable
    if [[ "${INTERVALS_CONFIRM_DELETE:-}" != "yes" ]]; then
        echo "Warning: This will permanently delete activity $id" >&2
        echo "Set INTERVALS_CONFIRM_DELETE=yes to confirm" >&2
        return 1
    fi

    api_delete "/activity/$id"
}

cmd_athlete() {
    api_get "/athlete/$INTERVALS_ATHLETE_ID"
}

cmd_zones() {
    api_get "/athlete/$INTERVALS_ATHLETE_ID/zones"
}

cmd_fitness() {
    # Check jq dependency
    if ! command -v jq &>/dev/null; then
        echo "Error: jq is required for the fitness command" >&2
        echo "Install: brew install jq (macOS) or apt install jq (Linux)" >&2
        return 1
    fi

    # Get current fitness metrics (CTL, ATL, TSB) from today's wellness
    local today
    today=$(date +%Y-%m-%d)
    local response
    response=$(api_get "/athlete/$INTERVALS_ATHLETE_ID/wellness/$today") || return 1
    echo "$response" | jq '{ctl, atl, rampRate, tsb: (.ctl - .atl)}' 2>/dev/null || {
        echo "Error: Failed to parse fitness data" >&2
        echo "$response" >&2
        return 1
    }
}

cmd_events() {
    [[ -z "${1:-}" ]] && die "Start date required" "Usage: api.sh events <start> <end>"
    [[ -z "${2:-}" ]] && die "End date required" "Usage: api.sh events <start> <end>"
    local start="$1"
    local end="$2"
    api_get "/athlete/$INTERVALS_ATHLETE_ID/events?oldest=$start&newest=$end"
}

cmd_event_create() {
    [[ -z "${1:-}" ]] && die "Date required" "Usage: api.sh event-create <date> <json>"
    [[ -z "${2:-}" ]] && die "JSON data required" "Usage: api.sh event-create <date> '{\"name\": \"...\", \"description\": \"...\"}'"
    local date
    date=$(parse_date "$1")
    local data="$2"

    validate_json "$data" "event create" || return 1

    # Ensure start_date_local is set in JSON
    if command -v jq &>/dev/null && ! echo "$data" | jq -e '.start_date_local' &>/dev/null 2>&1; then
        data=$(echo "$data" | jq --arg d "$date" '. + {start_date_local: $d}')
    fi

    api_post "/athlete/$INTERVALS_ATHLETE_ID/events" "$data"
}

cmd_event_update() {
    [[ -z "${1:-}" ]] && die "Event ID required" "Usage: api.sh event-update <id> <json>"
    [[ -z "${2:-}" ]] && die "JSON data required" "Usage: api.sh event-update <id> '{\"name\": \"...\"}'"
    local id="$1"
    local data="$2"

    validate_json "$data" "event update" || return 1

    api_put "/athlete/$INTERVALS_ATHLETE_ID/events/$id" "$data"
}

cmd_event_delete() {
    [[ -z "${1:-}" ]] && die "Event ID required" "Usage: api.sh event-delete <id>"
    local id="$1"

    # Check dry-run first
    if ! check_dry_run "DELETE event" "$id"; then
        return 0
    fi

    # Safety check - require confirmation via environment variable
    if [[ "${INTERVALS_CONFIRM_DELETE:-}" != "yes" ]]; then
        echo "Warning: This will permanently delete event $id" >&2
        echo "Set INTERVALS_CONFIRM_DELETE=yes to confirm" >&2
        return 1
    fi

    api_delete "/athlete/$INTERVALS_ATHLETE_ID/events/$id"
}

cmd_power_curves() {
    [[ -z "${1:-}" ]] && die "Start date required" "Usage: api.sh power-curves <start> <end> [format]"
    [[ -z "${2:-}" ]] && die "End date required" "Usage: api.sh power-curves <start> <end> [format]"
    local start="$1"
    local end="$2"
    local format="${3:-json}"

    # Check jq for non-json formats
    if [[ "$format" != "json" ]] && ! command -v jq &>/dev/null; then
        echo "Error: jq is required for formatted output" >&2
        echo "Install: brew install jq (macOS) or apt install jq (Linux)" >&2
        return 1
    fi

    local response
    response=$(api_get "/athlete/$INTERVALS_ATHLETE_ID/power-curves?oldest=$start&newest=$end") || return 1

    case "$format" in
        json)
            echo "$response"
            ;;
        summary)
            echo "$response" | jq '{
                "5s": .secs5,
                "1min": .secs60,
                "5min": .secs300,
                "20min": .secs1200,
                "60min": .secs3600,
                "ftp_estimate": ((.secs1200 // 0) * 0.95 | floor)
            }' 2>/dev/null || {
                echo "Error: Failed to parse power curve data" >&2
                return 1
            }
            ;;
        *)
            # Specific duration in seconds
            if [[ "$format" =~ ^[0-9]+$ ]]; then
                echo "$response" | jq ".secs${format} // \"Duration not found\"" 2>/dev/null || {
                    echo "Error: Failed to parse power curve data" >&2
                    return 1
                }
            else
                echo "Error: Unknown format '$format'. Use: json, summary, or duration in seconds" >&2
                return 1
            fi
            ;;
    esac
}

# cmd_help is handled at the top of the script before credential check

# Main dispatcher
command="${1:-help}"
shift || true

case "$command" in
    wellness)
        cmd_wellness "$@"
        ;;
    wellness-range)
        cmd_wellness_range "$@"
        ;;
    wellness-update)
        cmd_wellness_update "$@"
        ;;
    activities)
        cmd_activities "$@"
        ;;
    activity)
        cmd_activity "$@"
        ;;
    activity-streams)
        cmd_activity_streams "$@"
        ;;
    activity-last)
        cmd_activity_last "$@"
        ;;
    activity-upload)
        cmd_activity_upload "$@"
        ;;
    activity-delete)
        cmd_activity_delete "$@"
        ;;
    athlete)
        cmd_athlete "$@"
        ;;
    zones)
        cmd_zones "$@"
        ;;
    fitness)
        cmd_fitness "$@"
        ;;
    events)
        cmd_events "$@"
        ;;
    event-create)
        cmd_event_create "$@"
        ;;
    event-update)
        cmd_event_update "$@"
        ;;
    event-delete)
        cmd_event_delete "$@"
        ;;
    power-curves)
        cmd_power_curves "$@"
        ;;
    *)
        echo "Unknown command: $command" >&2
        echo "Run './api.sh help' for usage" >&2
        exit 1
        ;;
esac
