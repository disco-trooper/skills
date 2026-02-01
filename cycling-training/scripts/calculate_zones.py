#!/usr/bin/env python3
"""
Calculate cycling power and heart rate zones.

Usage:
    python calculate_zones.py <FTP_watts>
    python calculate_zones.py 250
    python calculate_zones.py 250 --model seiler
    python calculate_zones.py 250 --json

    # Heart rate zones (requires --lthr)
    python calculate_zones.py 250 --lthr 165
    python calculate_zones.py 250 --lthr 165 --hr-model karvonen --age 40 --rhr 50

Power models: coggan (default), seiler, isf
HR models: percent-lthr (default), karvonen
"""

import argparse
import json
import sys

def coggan_zones(ftp: int) -> dict:
    """Coggan 7-zone model."""
    # Compute boundaries to ensure zone continuity (no gaps)
    z1_upper = int(ftp * 0.55) - 1
    z2_lower = z1_upper + 1
    z2_upper = int(ftp * 0.75)
    z3_lower = z2_upper + 1
    z3_upper = int(ftp * 0.90)
    z4_lower = z3_upper + 1
    z4_upper = int(ftp * 1.05)
    z5_lower = z4_upper + 1
    z5_upper = int(ftp * 1.20)
    z6_lower = z5_upper + 1
    z6_upper = int(ftp * 1.50)

    return {
        "model": "Coggan 7-Zone",
        "ftp": ftp,
        "zones": {
            "Z1 Active Recovery": {"range": f"< {z2_lower}W", "percent": "<55%", "use": "Recovery rides"},
            "Z2 Endurance": {"range": f"{z2_lower}-{z2_upper}W", "percent": "55-75%", "use": "Aerobic base"},
            "Z3 Tempo": {"range": f"{z3_lower}-{z3_upper}W", "percent": "76-90%", "use": "Muscular endurance"},
            "Z4 Threshold": {"range": f"{z4_lower}-{z4_upper}W", "percent": "91-105%", "use": "FTP development"},
            "Z5 VO2max": {"range": f"{z5_lower}-{z5_upper}W", "percent": "106-120%", "use": "Aerobic capacity"},
            "Z6 Anaerobic": {"range": f"{z6_lower}-{z6_upper}W", "percent": "121-150%", "use": "AC intervals"},
            "Z7 Neuromuscular": {"range": f"> {z6_upper}W", "percent": ">150%", "use": "Sprints"},
        }
    }

def seiler_zones(ftp: int) -> dict:
    """Seiler 3-zone polarized model."""
    # Approximation: LT1 ~75% FTP, LT2 ~FTP
    lt1 = int(ftp * 0.75)
    lt2 = ftp
    return {
        "model": "Seiler 3-Zone (Polarized)",
        "ftp": ftp,
        "zones": {
            "Zone 1 (Below LT1)": {"range": f"< {lt1}W", "percent": "<75%", "use": "Easy, conversational - 80% of training"},
            "Zone 2 (LT1-LT2)": {"range": f"{lt1}-{lt2}W", "percent": "75-100%", "use": "Grey zone - minimize (<5%)"},
            "Zone 3 (Above LT2)": {"range": f"> {lt2}W", "percent": ">100%", "use": "Hard intervals - 15-20% of training"},
        }
    }

def isf_zones(ftp: int) -> dict:
    """ISF 5-zone simplified model."""
    # Compute boundaries to ensure zone continuity (no gaps)
    z2_lower = int(ftp * 0.55)
    z2_upper = int(ftp * 0.75)
    z3_lower = z2_upper + 1
    z3_upper = int(ftp * 0.90)
    z4_lower = z3_upper + 1
    z4_upper = int(ftp * 1.05)
    z5_lower = z4_upper + 1

    return {
        "model": "ISF 5-Zone",
        "ftp": ftp,
        "zones": {
            "Z1 Recovery": {"range": f"< {z2_lower}W", "percent": "<55%", "use": "Active recovery"},
            "Z2 Endurance": {"range": f"{z2_lower}-{z2_upper}W", "percent": "55-75%", "use": "Aerobic base"},
            "Z3 Tempo": {"range": f"{z3_lower}-{z3_upper}W", "percent": "76-90%", "use": "Tempo/Sweet spot"},
            "Z4 Threshold": {"range": f"{z4_lower}-{z4_upper}W", "percent": "91-105%", "use": "Threshold"},
            "Z5 VO2max+": {"range": f"> {z4_upper}W", "percent": ">105%", "use": "VO2max and above"},
        }
    }


def hr_zones_percent_lthr(lthr: int) -> dict:
    """Heart rate zones based on % of LTHR (Coggan model)."""
    # Compute boundaries to ensure zone continuity (no gaps)
    z1_upper = int(lthr * 0.81) - 1
    z2_lower = z1_upper + 1
    z2_upper = int(lthr * 0.89)
    z3_lower = z2_upper + 1
    z3_upper = int(lthr * 0.93)
    z4_lower = z3_upper + 1
    z4_upper = int(lthr * 0.99)
    z5a_lower = z4_upper + 1
    z5a_upper = int(lthr * 1.02)
    z5b_lower = z5a_upper + 1
    z5b_upper = int(lthr * 1.06)

    return {
        "model": "HR Zones (% LTHR)",
        "lthr": lthr,
        "zones": {
            "Z1 Active Recovery": {"range": f"< {z2_lower} bpm", "percent": "<81%", "use": "Recovery"},
            "Z2 Endurance": {"range": f"{z2_lower}-{z2_upper} bpm", "percent": "81-89%", "use": "Aerobic base"},
            "Z3 Tempo": {"range": f"{z3_lower}-{z3_upper} bpm", "percent": "90-93%", "use": "Tempo"},
            "Z4 Threshold": {"range": f"{z4_lower}-{z4_upper} bpm", "percent": "94-99%", "use": "Threshold"},
            "Z5a VO2max": {"range": f"{z5a_lower}-{z5a_upper} bpm", "percent": "100-102%", "use": "VO2max intervals"},
            "Z5b Anaerobic": {"range": f"{z5b_lower}-{z5b_upper} bpm", "percent": "103-106%", "use": "Anaerobic capacity"},
            "Z5c Neuromuscular": {"range": f"> {z5b_upper} bpm", "percent": ">106%", "use": "Max effort"},
        }
    }


def hr_zones_karvonen(lthr: int, age: int, rhr: int) -> dict:
    """Heart rate zones using Karvonen formula (Heart Rate Reserve)."""
    max_hr = 220 - age
    hrr = max_hr - rhr  # Heart Rate Reserve

    def zone_hr(low_pct: float, high_pct: float) -> str:
        low = int(rhr + hrr * low_pct)
        high = int(rhr + hrr * high_pct)
        return f"{low}-{high} bpm"

    return {
        "model": "HR Zones (Karvonen HRR)",
        "lthr": lthr,
        "max_hr": max_hr,
        "rhr": rhr,
        "hrr": hrr,
        "zones": {
            "Z1 Recovery": {"range": f"< {int(rhr + hrr * 0.60)} bpm", "percent": "<60% HRR", "use": "Recovery"},
            "Z2 Endurance": {"range": zone_hr(0.60, 0.70), "percent": "60-70% HRR", "use": "Aerobic base"},
            "Z3 Tempo": {"range": zone_hr(0.70, 0.80), "percent": "70-80% HRR", "use": "Tempo"},
            "Z4 Threshold": {"range": zone_hr(0.80, 0.90), "percent": "80-90% HRR", "use": "Threshold"},
            "Z5 VO2max+": {"range": f"> {int(rhr + hrr * 0.90)} bpm", "percent": ">90% HRR", "use": "VO2max and above"},
        }
    }

def print_zones(zones_data: dict, as_json: bool = False):
    """Print zones in human-readable or JSON format."""
    if as_json:
        print(json.dumps(zones_data, indent=2))
        return

    print(f"\n{'='*60}")
    if 'ftp' in zones_data:
        print(f"  {zones_data['model']} - FTP: {zones_data['ftp']}W")
    elif 'lthr' in zones_data:
        header = f"  {zones_data['model']} - LTHR: {zones_data['lthr']} bpm"
        if 'max_hr' in zones_data:
            header += f" | MaxHR: {zones_data['max_hr']} | RHR: {zones_data['rhr']}"
        print(header)
    print(f"{'='*60}\n")

    for zone_name, zone_data in zones_data['zones'].items():
        print(f"  {zone_name}")
        print(f"    Range: {zone_data['range']} ({zone_data['percent']})")
        print(f"    Use:   {zone_data['use']}")
        print()

def main():
    parser = argparse.ArgumentParser(description='Calculate cycling power and heart rate zones')
    parser.add_argument('ftp', type=int, help='FTP in watts')
    parser.add_argument('--model', choices=['coggan', 'seiler', 'isf'], default='coggan',
                       help='Power zone model (default: coggan)')
    parser.add_argument('--lthr', type=int, help='Lactate threshold HR for HR zones')
    parser.add_argument('--hr-model', choices=['percent-lthr', 'karvonen'], default='percent-lthr',
                       help='HR zone model (default: percent-lthr)')
    parser.add_argument('--age', type=int, help='Age for Karvonen model')
    parser.add_argument('--rhr', type=int, help='Resting HR for Karvonen model')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.ftp < 50 or args.ftp > 500:
        print("Error: FTP should be between 50-500W", file=sys.stderr)
        sys.exit(1)

    power_models = {
        'coggan': coggan_zones,
        'seiler': seiler_zones,
        'isf': isf_zones
    }

    # Calculate power zones
    power_zones = power_models[args.model](args.ftp)
    print_zones(power_zones, args.json)

    # Calculate HR zones if LTHR provided
    if args.lthr:
        if args.lthr < 100 or args.lthr > 220:
            print("Error: LTHR should be between 100-220 bpm", file=sys.stderr)
            sys.exit(1)

        if args.hr_model == 'karvonen':
            if not args.age or not args.rhr:
                print("Error: Karvonen model requires --age and --rhr", file=sys.stderr)
                sys.exit(1)
            hr_zones = hr_zones_karvonen(args.lthr, args.age, args.rhr)
        else:
            hr_zones = hr_zones_percent_lthr(args.lthr)

        print_zones(hr_zones, args.json)

if __name__ == '__main__':
    main()
