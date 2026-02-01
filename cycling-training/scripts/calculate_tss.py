#!/usr/bin/env python3
"""
Calculate Training Stress Score (TSS) from workout data.

Usage:
    python calculate_tss.py <FTP> <NP> <duration_minutes>
    python calculate_tss.py 250 230 60
    python calculate_tss.py 250 230 60 --json

    # From AP (Average Power) instead of NP:
    python calculate_tss.py 250 --ap 220 60

    # Estimate NP from AP with VI (Variability Index):
    python calculate_tss.py 250 --ap 200 --vi 1.05 60

TSS Formula: (Duration_sec × NP × IF) / (FTP × 3600) × 100
IF (Intensity Factor) = NP / FTP
"""

import argparse
import json
import sys


def calculate_tss(ftp: int, np: float, duration_min: float) -> dict:
    """Calculate TSS and related metrics."""
    duration_sec = duration_min * 60
    intensity_factor = np / ftp
    tss = (duration_sec * np * intensity_factor) / (ftp * 3600) * 100

    # Training zone estimate based on IF
    if intensity_factor < 0.55:
        zone = "Z1 Recovery"
    elif intensity_factor < 0.75:
        zone = "Z2 Endurance"
    elif intensity_factor < 0.90:
        zone = "Z3 Tempo"
    elif intensity_factor < 1.05:
        zone = "Z4 Threshold"
    elif intensity_factor < 1.20:
        zone = "Z5 VO2max"
    else:
        zone = "Z6+ Anaerobic"

    return {
        "ftp": ftp,
        "normalized_power": round(np, 1),
        "duration_minutes": duration_min,
        "intensity_factor": round(intensity_factor, 3),
        "tss": round(tss, 1),
        "estimated_zone": zone,
        "recovery_hours": round(tss / 50, 1)  # Rough estimate
    }


def print_result(result: dict, as_json: bool = False):
    """Print TSS calculation result."""
    if as_json:
        print(json.dumps(result, indent=2))
        return

    print(f"\n{'='*50}")
    print(f"  TSS Calculation - FTP: {result['ftp']}W")
    print(f"{'='*50}\n")
    print(f"  Normalized Power:  {result['normalized_power']}W")
    print(f"  Duration:          {result['duration_minutes']} min")
    print(f"  Intensity Factor:  {result['intensity_factor']}")
    print(f"  TSS:               {result['tss']}")
    print(f"  Estimated Zone:    {result['estimated_zone']}")
    print(f"  Est. Recovery:     {result['recovery_hours']} hours")
    print()


def main():
    parser = argparse.ArgumentParser(description='Calculate Training Stress Score (TSS)')
    parser.add_argument('ftp', type=int, help='FTP in watts')
    parser.add_argument('np', type=float, nargs='?', help='Normalized Power in watts')
    parser.add_argument('duration', type=float, help='Duration in minutes')
    parser.add_argument('--ap', type=float, help='Average Power (instead of NP)')
    parser.add_argument('--vi', type=float, default=1.0,
                       help='Variability Index to estimate NP from AP (default: 1.0)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Validate FTP
    if args.ftp < 50 or args.ftp > 500:
        print("Error: FTP should be between 50-500W", file=sys.stderr)
        sys.exit(1)

    # Determine NP
    if args.ap:
        np = args.ap * args.vi
    elif args.np:
        np = args.np
    else:
        print("Error: Provide either NP or --ap", file=sys.stderr)
        sys.exit(1)

    result = calculate_tss(args.ftp, np, args.duration)
    print_result(result, args.json)


if __name__ == '__main__':
    main()
