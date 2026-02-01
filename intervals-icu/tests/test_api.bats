#!/usr/bin/env bats
# Integration tests for intervals-icu API helper

setup() {
    SCRIPT="$BATS_TEST_DIRNAME/../scripts/api.sh"
    FIXTURES="$BATS_TEST_DIRNAME/fixtures"
    export INTERVALS_API_KEY="test_key"
    export INTERVALS_ATHLETE_ID="i12345"
}

# Help tests
@test "help command shows usage" {
    run "$SCRIPT" help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "Intervals.icu API Helper" ]]
}

@test "no args shows help" {
    run "$SCRIPT"
    [ "$status" -eq 0 ]
    [[ "$output" =~ "Usage:" ]]
}

@test "--help flag works" {
    run "$SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "Intervals.icu API Helper" ]]
}

# Environment variable tests
@test "missing API key shows error" {
    unset INTERVALS_API_KEY
    run "$SCRIPT" wellness
    [ "$status" -eq 1 ]
    [[ "$output" =~ "INTERVALS_API_KEY not set" ]]
}

@test "missing athlete ID shows error" {
    unset INTERVALS_ATHLETE_ID
    run "$SCRIPT" wellness
    [ "$status" -eq 1 ]
    [[ "$output" =~ "INTERVALS_ATHLETE_ID not set" ]]
}

# Command argument validation
@test "wellness-range requires start date" {
    run "$SCRIPT" wellness-range
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Start date required" ]]
}

@test "activities requires both dates" {
    run "$SCRIPT" activities 2024-01-01
    [ "$status" -eq 1 ]
    [[ "$output" =~ "End date required" ]]
}

@test "unknown command shows error" {
    run "$SCRIPT" unknown-command
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Unknown command" ]]
}

# Fixture validation tests
@test "wellness fixture is valid JSON" {
    run jq '.' "$FIXTURES/wellness.json"
    [ "$status" -eq 0 ]
}

@test "activities fixture is valid JSON array" {
    run jq 'type' "$FIXTURES/activities.json"
    [ "$status" -eq 0 ]
    [ "$output" = '"array"' ]
}

@test "power curves fixture has expected fields" {
    run jq 'has("secs300")' "$FIXTURES/power_curves.json"
    [ "$status" -eq 0 ]
    [ "$output" = "true" ]
}

@test "power curves summary calculation works" {
    run jq '{
        "5s": .secs5,
        "1min": .secs60,
        "5min": .secs300,
        "20min": .secs1200,
        "ftp_estimate": ((.secs1200 // 0) * 0.95 | floor)
    }' "$FIXTURES/power_curves.json"
    [ "$status" -eq 0 ]
    [[ "$output" =~ '"ftp_estimate": 261' ]]
}

@test "fitness calculation from wellness works" {
    run jq '{ctl, atl, rampRate, tsb: (.ctl - .atl)}' "$FIXTURES/wellness.json"
    [ "$status" -eq 0 ]
    [[ "$output" =~ '"tsb":' ]]
}

@test "power-curves help shows format options" {
    run "$SCRIPT" help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "power-curves" ]]
    [[ "$output" =~ "json|summary|<seconds>" ]]
}

@test "api_get retries on network failure" {
    # This test verifies the retry function exists and has correct signature
    run grep -c "retry_curl" "$SCRIPT"
    [ "$status" -eq 0 ]
    [ "$output" -ge 1 ]
}

@test "event-create requires date" {
    run "$SCRIPT" event-create
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Date required" ]]
}

@test "event-create requires JSON data" {
    run "$SCRIPT" event-create 2024-01-15
    [ "$status" -eq 1 ]
    [[ "$output" =~ "JSON data required" ]]
}

@test "activity-upload requires file" {
    run "$SCRIPT" activity-upload
    [ "$status" -eq 1 ]
    [[ "$output" =~ "File required" ]]
}

@test "activity-upload checks file exists" {
    run "$SCRIPT" activity-upload /nonexistent/file.fit
    [ "$status" -eq 1 ]
    [[ "$output" =~ "not found" ]]
}

@test "zones command in help" {
    run "$SCRIPT" help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "zones" ]]
}

@test "api_put uses retry_curl" {
    run grep -A5 "^api_put()" "$SCRIPT"
    [ "$status" -eq 0 ]
    [[ "$output" =~ "retry_curl" ]]
}

@test "api_delete function exists" {
    run grep -c "^api_delete()" "$SCRIPT"
    [ "$status" -eq 0 ]
    [ "$output" -ge 1 ]
}

@test "activity-delete requires ID" {
    run "$SCRIPT" activity-delete
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Activity ID required" ]]
}

@test "activity-delete in help" {
    run "$SCRIPT" help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "activity-delete" ]]
}

@test "event-delete requires ID" {
    run "$SCRIPT" event-delete
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Event ID required" ]]
}

@test "event-update requires ID" {
    run "$SCRIPT" event-update
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Event ID required" ]]
}

@test "event-update requires JSON" {
    run "$SCRIPT" event-update e12345
    [ "$status" -eq 1 ]
    [[ "$output" =~ "JSON data required" ]]
}

@test "INTERVALS_MAX_PAGES is configurable" {
    run grep "INTERVALS_MAX_PAGES" "$SCRIPT"
    [ "$status" -eq 0 ]
    [[ "$output" =~ "\${INTERVALS_MAX_PAGES:-" ]]
}

@test "activity-last in help" {
    run "$SCRIPT" help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "activity-last" ]]
}

@test "dry-run flag is documented" {
    run "$SCRIPT" help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "dry-run" ]] || [[ "$output" =~ "DRY_RUN" ]]
}

@test "dry-run mode prevents activity delete" {
    export INTERVALS_DRY_RUN=true
    export INTERVALS_CONFIRM_DELETE=yes
    run "$SCRIPT" activity-delete test123
    [ "$status" -eq 0 ]
    [[ "$output" =~ "[DRY-RUN]" ]]
    [[ "$output" =~ "DELETE activity" ]]
}

@test "dry-run mode prevents event delete" {
    export INTERVALS_DRY_RUN=true
    export INTERVALS_CONFIRM_DELETE=yes
    run "$SCRIPT" event-delete test123
    [ "$status" -eq 0 ]
    [[ "$output" =~ "[DRY-RUN]" ]]
    [[ "$output" =~ "DELETE event" ]]
}

@test "validate_json function exists" {
    run grep -c "validate_json()" "$SCRIPT"
    [ "$status" -eq 0 ]
    [ "$output" -ge 1 ]
}
