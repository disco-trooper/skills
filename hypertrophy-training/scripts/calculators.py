#!/usr/bin/env python3
"""
Hypertrophy Training Calculators
Usage: python calculators.py [command] [args]
"""

import sys
import math


def validate_positive_float(value: str, name: str) -> float:
    """Validate and convert string to positive float."""
    try:
        result = float(value)
        if result <= 0:
            raise ValueError(f"{name} must be positive, got {result}")
        return result
    except ValueError as e:
        if "could not convert" in str(e).lower() or "invalid literal" in str(e).lower():
            raise ValueError(f"{name} must be a number, got '{value}'")
        raise


def validate_positive_int(value: str, name: str) -> int:
    """Validate and convert string to positive integer."""
    try:
        result = int(value)
        if result <= 0:
            raise ValueError(f"{name} must be positive, got {result}")
        return result
    except ValueError as e:
        if "invalid literal" in str(e).lower():
            raise ValueError(f"{name} must be an integer, got '{value}'")
        raise


def validate_choice(value: str, choices: list, name: str) -> str:
    """Validate value is one of allowed choices."""
    if value.lower() not in [c.lower() for c in choices]:
        raise ValueError(f"{name} must be one of {choices}, got '{value}'")
    return value.lower()


def calculate_tdee(weight_kg: float, height_cm: float, age: int, sex: str, activity: str) -> dict:
    """Calculate TDEE using Mifflin-St Jeor equation."""
    if sex.lower() == 'm':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }

    tdee = bmr * multipliers.get(activity, 1.55)

    return {
        'bmr': round(bmr),
        'tdee': round(tdee),
        'bulk': round(tdee + 300),
        'cut': round(tdee - 500)
    }

def calculate_macros(weight_kg: float, tdee: float, goal: str) -> dict:
    """Calculate macronutrient targets."""
    if goal == 'bulk':
        calories = tdee + 300
        protein = weight_kg * 2.0
    elif goal == 'cut':
        calories = tdee - 500
        protein = weight_kg * 2.2
    else:  # maintain
        calories = tdee
        protein = weight_kg * 1.8

    fat = weight_kg * 1.0  # 1g/kg
    fat_cals = fat * 9
    protein_cals = protein * 4
    carb_cals = calories - fat_cals - protein_cals
    carbs = carb_cals / 4

    return {
        'calories': round(calories),
        'protein_g': round(protein),
        'fat_g': round(fat),
        'carbs_g': round(carbs)
    }

def calculate_1rm(weight: float, reps: int, formula: str = 'epley') -> float:
    """Estimate 1RM from submaximal lift."""
    if formula == 'epley':
        return weight * (1 + reps / 30)
    elif formula == 'brzycki':
        return weight * (36 / (37 - reps))
    else:
        return weight * (1 + reps / 30)

def calculate_volume(sets: int, reps: int, weight: float) -> dict:
    """Calculate training volume metrics."""
    total_reps = sets * reps
    tonnage = sets * reps * weight
    return {
        'total_reps': total_reps,
        'tonnage_kg': round(tonnage),
        'avg_per_set': round(reps * weight)
    }


def calculate_weekly_volume(sets_per_session: int, frequency: int) -> dict:
    """Calculate weekly volume for a muscle group."""
    weekly_sets = sets_per_session * frequency

    # Volume landmark assessment
    if weekly_sets < 10:
        assessment = "Below MEV for most muscle groups"
    elif weekly_sets <= 14:
        assessment = "Around MEV-MAV low end"
    elif weekly_sets <= 20:
        assessment = "Within MAV for most muscle groups"
    elif weekly_sets <= 25:
        assessment = "High volume, approaching MRV"
    else:
        assessment = "Very high volume, may exceed MRV"

    return {
        'weekly_sets': weekly_sets,
        'assessment': assessment
    }


def calculate_protein_needs(weight_kg: float, goal: str, training_status: str) -> dict:
    """Calculate protein requirements based on goal and training status."""
    # Base recommendations (g/kg)
    protein_ranges = {
        'bulk': {'beginner': (1.6, 2.0), 'intermediate': (1.8, 2.2), 'advanced': (1.8, 2.2)},
        'cut': {'beginner': (2.0, 2.4), 'intermediate': (2.2, 2.6), 'advanced': (2.2, 2.8)},
        'maintain': {'beginner': (1.4, 1.8), 'intermediate': (1.6, 2.0), 'advanced': (1.6, 2.0)}
    }

    low, high = protein_ranges.get(goal, {}).get(training_status, (1.6, 2.2))

    protein_low = weight_kg * low
    protein_high = weight_kg * high

    # Per-meal targets (4-5 meals)
    per_meal_low = protein_low / 5
    per_meal_high = protein_high / 4

    return {
        'daily_low_g': round(protein_low),
        'daily_high_g': round(protein_high),
        'per_meal_g': f"{round(per_meal_low)}-{round(per_meal_high)}"
    }


def calculate_rir_to_percentage(rir: int) -> dict:
    """Convert RIR to approximate percentage of 1RM."""
    # Approximate mapping (varies by exercise and individual)
    rir_map = {
        0: (100, "Failure"),
        1: (95, "1 rep left"),
        2: (90, "2 reps left"),
        3: (85, "3 reps left"),
        4: (80, "4 reps left"),
        5: (75, "5+ reps left")
    }

    if rir > 5:
        rir = 5
    if rir < 0:
        rir = 0

    percentage, description = rir_map[rir]

    return {
        'approximate_percentage': percentage,
        'description': description,
        'note': "Percentages are approximate and vary by exercise/individual"
    }

def print_help():
    """Print usage information."""
    print("""
Hypertrophy Calculators

Commands:
  tdee <weight_kg> <height_cm> <age> <m/f> <activity>
       Activity: sedentary, light, moderate, active, very_active

  macros <weight_kg> <tdee> <goal>
       Goal: bulk, cut, maintain

  1rm <weight> <reps> [formula]
       Formula: epley (default), brzycki

  volume <sets> <reps> <weight>

  weekly-volume <sets_per_session> <frequency>
       Calculate weekly volume and assess against volume landmarks

  protein <weight_kg> <goal> <training_status>
       Goal: bulk, cut, maintain
       Training status: beginner, intermediate, advanced

  rir <reps_in_reserve>
       Convert RIR to approximate percentage of 1RM

Examples:
  python calculators.py tdee 80 180 30 m moderate
  python calculators.py macros 80 2500 bulk
  python calculators.py 1rm 100 8
  python calculators.py volume 4 10 80
  python calculators.py weekly-volume 6 2
  python calculators.py protein 80 bulk intermediate
  python calculators.py rir 2
    """)


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1]

    try:
        if cmd == 'tdee':
            if len(sys.argv) != 7:
                print("Error: tdee requires 5 arguments: weight_kg height_cm age sex activity")
                print("Example: python calculators.py tdee 80 180 30 m moderate")
                return
            weight = validate_positive_float(sys.argv[2], "weight_kg")
            height = validate_positive_float(sys.argv[3], "height_cm")
            age = validate_positive_int(sys.argv[4], "age")
            sex = validate_choice(sys.argv[5], ['m', 'f'], "sex")
            activity = validate_choice(sys.argv[6],
                ['sedentary', 'light', 'moderate', 'active', 'very_active'], "activity")
            result = calculate_tdee(weight, height, age, sex, activity)
            print(f"BMR: {result['bmr']} kcal")
            print(f"TDEE: {result['tdee']} kcal")
            print(f"Bulk (+300): {result['bulk']} kcal")
            print(f"Cut (-500): {result['cut']} kcal")

        elif cmd == 'macros':
            if len(sys.argv) != 5:
                print("Error: macros requires 3 arguments: weight_kg tdee goal")
                print("Example: python calculators.py macros 80 2500 bulk")
                return
            weight = validate_positive_float(sys.argv[2], "weight_kg")
            tdee = validate_positive_float(sys.argv[3], "tdee")
            goal = validate_choice(sys.argv[4], ['bulk', 'cut', 'maintain'], "goal")
            result = calculate_macros(weight, tdee, goal)
            print(f"Calories: {result['calories']} kcal")
            print(f"Protein: {result['protein_g']}g")
            print(f"Fat: {result['fat_g']}g")
            print(f"Carbs: {result['carbs_g']}g")

        elif cmd == '1rm':
            if len(sys.argv) < 4:
                print("Error: 1rm requires 2 arguments: weight reps [formula]")
                print("Example: python calculators.py 1rm 100 8")
                return
            weight = validate_positive_float(sys.argv[2], "weight")
            reps = validate_positive_int(sys.argv[3], "reps")
            formula = 'epley'
            if len(sys.argv) > 4:
                formula = validate_choice(sys.argv[4], ['epley', 'brzycki'], "formula")
            result = calculate_1rm(weight, reps, formula)
            print(f"Estimated 1RM: {round(result)} kg")

        elif cmd == 'volume':
            if len(sys.argv) != 5:
                print("Error: volume requires 3 arguments: sets reps weight")
                print("Example: python calculators.py volume 4 10 80")
                return
            sets = validate_positive_int(sys.argv[2], "sets")
            reps = validate_positive_int(sys.argv[3], "reps")
            weight = validate_positive_float(sys.argv[4], "weight")
            result = calculate_volume(sets, reps, weight)
            print(f"Total reps: {result['total_reps']}")
            print(f"Tonnage: {result['tonnage_kg']} kg")

        elif cmd == 'weekly-volume':
            if len(sys.argv) != 4:
                print("Error: weekly-volume requires 2 arguments: sets_per_session frequency")
                print("Example: python calculators.py weekly-volume 6 2")
                return
            sets_per_session = validate_positive_int(sys.argv[2], "sets_per_session")
            frequency = validate_positive_int(sys.argv[3], "frequency")
            result = calculate_weekly_volume(sets_per_session, frequency)
            print(f"Weekly sets: {result['weekly_sets']}")
            print(f"Assessment: {result['assessment']}")

        elif cmd == 'protein':
            if len(sys.argv) != 5:
                print("Error: protein requires 3 arguments: weight_kg goal training_status")
                print("Example: python calculators.py protein 80 bulk intermediate")
                return
            weight = validate_positive_float(sys.argv[2], "weight_kg")
            goal = validate_choice(sys.argv[3], ['bulk', 'cut', 'maintain'], "goal")
            status = validate_choice(sys.argv[4], ['beginner', 'intermediate', 'advanced'], "training_status")
            result = calculate_protein_needs(weight, goal, status)
            print(f"Daily protein: {result['daily_low_g']}-{result['daily_high_g']}g")
            print(f"Per meal (4-5 meals): {result['per_meal_g']}g")

        elif cmd == 'rir':
            if len(sys.argv) != 3:
                print("Error: rir requires 1 argument: reps_in_reserve")
                print("Example: python calculators.py rir 2")
                return
            rir = int(sys.argv[2])
            if rir < 0:
                rir = 0
            result = calculate_rir_to_percentage(rir)
            print(f"Approximate %1RM: {result['approximate_percentage']}%")
            print(f"Description: {result['description']}")
            print(f"Note: {result['note']}")

        else:
            print(f"Error: Unknown command '{cmd}'")
            print_help()

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
