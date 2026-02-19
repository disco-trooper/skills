#!/usr/bin/env python3
"""
Analyze weekly training load with evidence-based metrics.

Usage:
    python analyze_week.py <weekly_tss> <ctl> <atl>
    python analyze_week.py 450 65 72
    python analyze_week.py 450 65 72 --prev-week-tss 400 --daily-tss 60,80,0,70,90,80,70
    python analyze_week.py 450 65 72 --json

Metrics calculated:
- TSB (Training Stress Balance) = CTL - ATL
- ACWR (Acute:Chronic Workload Ratio) = ATL / CTL
- Ramp Rate = weekly CTL change estimate
- Monotony & Strain (Foster 1998) - requires --daily-tss

Heuristic thresholds (interpret cautiously; context matters):
- ACWR: 0.8-1.3 often-cited "optimal" band (widely used; debated)
- Ramp rate: <3 conservative, 3-5 moderate, 5-8 aggressive, >8 excessive
- Monotony >2.0 can indicate elevated risk (Foster 1998)
"""

import argparse
import json
import sys
import math


def calculate_tsb(ctl: float, atl: float) -> float:
    """Calculate Training Stress Balance."""
    return ctl - atl


def calculate_acwr(ctl: float, atl: float) -> float:
    """Calculate Acute:Chronic Workload Ratio."""
    if ctl <= 0:
        return 0.0
    return atl / ctl


def calculate_monotony_strain(daily_tss: list) -> dict:
    """
    Calculate Foster's Monotony and Strain metrics.

    Monotony = mean TSS / std TSS
    Strain = weekly TSS × Monotony

    High monotony (>2.0) with high strain increases injury/illness risk.
    Reference: Foster 1998, MSSE
    """
    if len(daily_tss) < 3:
        return {"monotony": None, "strain": None, "error": "Need at least 3 days"}

    mean_tss = sum(daily_tss) / len(daily_tss)

    # Standard deviation
    variance = sum((x - mean_tss) ** 2 for x in daily_tss) / len(daily_tss)
    std_tss = math.sqrt(variance)

    if std_tss < 0.01:  # Avoid division by zero
        return {"monotony": float('inf'), "strain": float('inf'),
                "warning": "Training too uniform - add variety"}

    monotony = mean_tss / std_tss
    weekly_load = sum(daily_tss)
    strain = weekly_load * monotony

    return {
        "monotony": round(monotony, 2),
        "strain": round(strain, 0),
        "weekly_load": round(weekly_load, 0),
        "mean_daily": round(mean_tss, 1),
        "std_daily": round(std_tss, 1)
    }


def estimate_ramp_rate(weekly_tss: float, ctl: float) -> float:
    """
    Estimate weekly CTL change (ramp rate).

    Using simplified model: new_ctl ≈ ctl + (weekly_tss/7 - ctl) / 6
    This approximates the 42-day exponential weighted average behavior.
    """
    daily_avg = weekly_tss / 7
    # CTL changes by roughly (daily_avg - ctl) / 6 per day
    weekly_change = (daily_avg - ctl) / 6 * 7
    return round(weekly_change, 1)


def get_acwr_status(acwr: float) -> dict:
    """Get ACWR interpretation based on Gabbett 2016, Hulin 2014."""
    if acwr < 0.8:
        return {
            "status": "UNDERTRAINED",
            "color": "yellow",
            "recommendation": "Increase training load gradually to build fitness"
        }
    elif acwr <= 1.3:
        return {
            "status": "OPTIMAL",
            "color": "green",
            "recommendation": "Sweet spot - good balance of load and recovery"
        }
    elif acwr <= 1.5:
        return {
            "status": "CAUTION",
            "color": "orange",
            "recommendation": "Elevated injury risk - consider reducing acute load"
        }
    else:
        return {
            "status": "DANGER",
            "color": "red",
            "recommendation": "High injury risk - reduce load immediately"
        }


def get_tsb_status(tsb: float) -> dict:
    """Get TSB interpretation."""
    if tsb < -30:
        return {
            "status": "VERY_FATIGUED",
            "color": "red",
            "recommendation": "Overreaching - plan recovery days"
        }
    elif tsb < -10:
        return {
            "status": "FATIGUED",
            "color": "orange",
            "recommendation": "Building load - monitor recovery"
        }
    elif tsb < 5:
        return {
            "status": "NEUTRAL",
            "color": "yellow",
            "recommendation": "Maintenance phase - ready for training"
        }
    elif tsb < 25:
        return {
            "status": "FRESH",
            "color": "green",
            "recommendation": "Good form - ready for hard efforts or racing"
        }
    else:
        return {
            "status": "VERY_FRESH",
            "color": "green",
            "recommendation": "Peak form - ideal for A races"
        }


def get_ramp_status(ramp: float) -> dict:
    """Get ramp rate interpretation (heuristic)."""
    if ramp < 3:
        return {
            "status": "CONSERVATIVE",
            "color": "green",
            "recommendation": "Safe progression - good for base building"
        }
    elif ramp <= 5:
        return {
            "status": "MODERATE",
            "color": "green",
            "recommendation": "Standard progression - sustainable long-term"
        }
    elif ramp <= 8:
        return {
            "status": "AGGRESSIVE",
            "color": "orange",
            "recommendation": "Fast progression - monitor for overtraining signs"
        }
    else:
        return {
            "status": "EXCESSIVE",
            "color": "red",
            "recommendation": "Too fast - high injury/overtraining risk"
        }


def get_monotony_status(monotony: float) -> dict:
    """Get monotony interpretation based on Foster 1998."""
    if monotony is None:
        return {"status": "UNKNOWN", "color": "gray", "recommendation": "Need daily TSS data"}

    if monotony < 1.5:
        return {
            "status": "VARIED",
            "color": "green",
            "recommendation": "Good training variety"
        }
    elif monotony <= 2.0:
        return {
            "status": "MODERATE",
            "color": "yellow",
            "recommendation": "Consider adding more recovery days"
        }
    else:
        return {
            "status": "HIGH_RISK",
            "color": "red",
            "recommendation": "Training too uniform - increase rest day frequency"
        }


def analyze_week(weekly_tss: float, ctl: float, atl: float,
                 prev_week_tss: float = None, daily_tss: list = None) -> dict:
    """Perform comprehensive weekly analysis."""

    tsb = calculate_tsb(ctl, atl)
    acwr = calculate_acwr(ctl, atl)
    ramp = estimate_ramp_rate(weekly_tss, ctl)

    result = {
        "input": {
            "weekly_tss": weekly_tss,
            "ctl": ctl,
            "atl": atl
        },
        "metrics": {
            "tsb": round(tsb, 1),
            "acwr": round(acwr, 2),
            "ramp_rate": ramp
        },
        "status": {
            "tsb": get_tsb_status(tsb),
            "acwr": get_acwr_status(acwr),
            "ramp": get_ramp_status(ramp)
        },
        "warnings": []
    }

    # Add week-over-week comparison if previous week provided
    if prev_week_tss is not None:
        wow_change = ((weekly_tss - prev_week_tss) / prev_week_tss * 100) if prev_week_tss > 0 else 0
        result["metrics"]["week_over_week_change"] = round(wow_change, 1)

        if wow_change > 30:
            result["warnings"].append({
                "level": "high",
                "message": f"Week-over-week TSS increase of {wow_change:.0f}% exceeds 30% threshold"
            })
        elif wow_change > 20:
            result["warnings"].append({
                "level": "moderate",
                "message": f"Week-over-week TSS increase of {wow_change:.0f}% is aggressive"
            })

    # Add Monotony/Strain if daily data provided
    if daily_tss:
        ms = calculate_monotony_strain(daily_tss)
        result["metrics"]["monotony"] = ms.get("monotony")
        result["metrics"]["strain"] = ms.get("strain")
        result["status"]["monotony"] = get_monotony_status(ms.get("monotony"))

        if ms.get("monotony") and ms["monotony"] > 2.0:
            result["warnings"].append({
                "level": "high",
                "message": f"Monotony {ms['monotony']:.1f} exceeds 2.0 - injury/illness risk elevated"
            })

    # Generate warnings based on metrics
    if acwr > 1.5:
        result["warnings"].append({
            "level": "high",
            "message": f"ACWR {acwr:.2f} in danger zone (>1.5)"
        })
    elif acwr > 1.3:
        result["warnings"].append({
            "level": "moderate",
            "message": f"ACWR {acwr:.2f} elevated - monitor closely"
        })

    if tsb < -30:
        result["warnings"].append({
            "level": "high",
            "message": f"TSB {tsb:.0f} very negative - risk of overreaching"
        })

    if ramp > 8:
        result["warnings"].append({
            "level": "high",
            "message": f"Ramp rate {ramp:.1f} too aggressive"
        })

    return result


def print_result(result: dict, as_json: bool = False):
    """Print analysis result."""
    if as_json:
        print(json.dumps(result, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"  Weekly Training Analysis")
    print(f"{'='*60}")
    print(f"\n  Input: TSS={result['input']['weekly_tss']} | CTL={result['input']['ctl']} | ATL={result['input']['atl']}")

    print(f"\n  Metrics:")
    m = result['metrics']
    print(f"    TSB (Form):      {m['tsb']:+.0f}")
    print(f"    ACWR:            {m['acwr']:.2f}")
    print(f"    Ramp Rate:       {m['ramp_rate']:+.1f} CTL/week")

    if 'week_over_week_change' in m:
        print(f"    WoW Change:      {m['week_over_week_change']:+.1f}%")

    if m.get('monotony'):
        print(f"    Monotony:        {m['monotony']:.2f}")
        print(f"    Strain:          {m['strain']:.0f}")

    print(f"\n  Status:")
    for key in ['tsb', 'acwr', 'ramp', 'monotony']:
        if key in result['status']:
            s = result['status'][key]
            print(f"    {key.upper():12} [{s['status']:12}] {s['recommendation']}")

    if result['warnings']:
        print(f"\n  ⚠️  Warnings:")
        for w in result['warnings']:
            level_icon = "🔴" if w['level'] == 'high' else "🟡"
            print(f"    {level_icon} {w['message']}")

    print()


def parse_daily_tss(value: str) -> list:
    """Parse comma-separated daily TSS values."""
    try:
        return [float(x.strip()) for x in value.split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError("Daily TSS must be comma-separated numbers (e.g., 60,80,0,70,90,80,70)")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze weekly training load with evidence-based metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 450 65 72                    Basic analysis
  %(prog)s 450 65 72 --prev-week 400    With week-over-week comparison
  %(prog)s 450 65 72 --daily 60,80,0,70,90,80,70  With Monotony/Strain
  %(prog)s 450 65 72 --json             JSON output for scripting
        """
    )
    parser.add_argument('weekly_tss', type=float, help='Total weekly TSS')
    parser.add_argument('ctl', type=float, help='Current CTL (Chronic Training Load)')
    parser.add_argument('atl', type=float, help='Current ATL (Acute Training Load)')
    parser.add_argument('--prev-week-tss', type=float, help='Previous week TSS for comparison')
    parser.add_argument('--daily-tss', type=parse_daily_tss,
                       help='Daily TSS values (comma-separated) for Monotony/Strain')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Validate inputs
    if args.ctl < 0 or args.ctl > 200:
        print("Warning: CTL outside typical range (0-200)", file=sys.stderr)
    if args.atl < 0 or args.atl > 300:
        print("Warning: ATL outside typical range (0-300)", file=sys.stderr)

    result = analyze_week(
        args.weekly_tss,
        args.ctl,
        args.atl,
        args.prev_week_tss,
        args.daily_tss
    )

    print_result(result, args.json)


if __name__ == '__main__':
    main()
