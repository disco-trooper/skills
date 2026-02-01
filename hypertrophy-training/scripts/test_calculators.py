#!/usr/bin/env python3
"""
Tests for calculators.py
Run: python -m pytest test_calculators.py -v
Or:  python test_calculators.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculators import (
    calculate_tdee,
    calculate_macros,
    calculate_1rm,
    calculate_volume,
    calculate_weekly_volume,
    calculate_protein_needs,
    calculate_rir_to_percentage,
    validate_positive_float,
    validate_positive_int,
    validate_choice,
)


class TestValidators(unittest.TestCase):
    """Test input validation functions."""

    def test_validate_positive_float_valid(self):
        self.assertEqual(validate_positive_float("80.5", "weight"), 80.5)
        self.assertEqual(validate_positive_float("100", "weight"), 100.0)

    def test_validate_positive_float_invalid(self):
        with self.assertRaises(ValueError):
            validate_positive_float("-5", "weight")
        with self.assertRaises(ValueError):
            validate_positive_float("0", "weight")
        with self.assertRaises(ValueError):
            validate_positive_float("abc", "weight")

    def test_validate_positive_int_valid(self):
        self.assertEqual(validate_positive_int("30", "age"), 30)
        self.assertEqual(validate_positive_int("1", "age"), 1)

    def test_validate_positive_int_invalid(self):
        with self.assertRaises(ValueError):
            validate_positive_int("-1", "age")
        with self.assertRaises(ValueError):
            validate_positive_int("0", "age")
        with self.assertRaises(ValueError):
            validate_positive_int("abc", "age")

    def test_validate_choice_valid(self):
        self.assertEqual(validate_choice("m", ["m", "f"], "sex"), "m")
        self.assertEqual(validate_choice("M", ["m", "f"], "sex"), "m")
        self.assertEqual(validate_choice("bulk", ["bulk", "cut", "maintain"], "goal"), "bulk")

    def test_validate_choice_invalid(self):
        with self.assertRaises(ValueError):
            validate_choice("x", ["m", "f"], "sex")


class TestTDEE(unittest.TestCase):
    """Test TDEE calculation."""

    def test_tdee_male_moderate(self):
        result = calculate_tdee(80, 180, 30, "m", "moderate")
        self.assertIn("bmr", result)
        self.assertIn("tdee", result)
        self.assertIn("bulk", result)
        self.assertIn("cut", result)
        # BMR for 80kg, 180cm, 30yo male: 10*80 + 6.25*180 - 5*30 + 5 = 1780
        self.assertEqual(result["bmr"], 1780)
        # TDEE = 1780 * 1.55 = 2759
        self.assertEqual(result["tdee"], 2759)
        # Bulk = TDEE + 300
        self.assertEqual(result["bulk"], 3059)
        # Cut = TDEE - 500
        self.assertEqual(result["cut"], 2259)

    def test_tdee_female_sedentary(self):
        result = calculate_tdee(60, 165, 25, "f", "sedentary")
        # BMR for 60kg, 165cm, 25yo female: 10*60 + 6.25*165 - 5*25 - 161 = 1345.25 ≈ 1345
        self.assertEqual(result["bmr"], 1345)
        # TDEE = 1345 * 1.2 = 1614
        self.assertEqual(result["tdee"], 1614)


class TestMacros(unittest.TestCase):
    """Test macronutrient calculation."""

    def test_macros_bulk(self):
        result = calculate_macros(80, 2500, "bulk")
        self.assertEqual(result["calories"], 2800)  # 2500 + 300
        self.assertEqual(result["protein_g"], 160)  # 80 * 2.0
        self.assertEqual(result["fat_g"], 80)  # 80 * 1.0

    def test_macros_cut(self):
        result = calculate_macros(80, 2500, "cut")
        self.assertEqual(result["calories"], 2000)  # 2500 - 500
        self.assertEqual(result["protein_g"], 176)  # 80 * 2.2

    def test_macros_maintain(self):
        result = calculate_macros(80, 2500, "maintain")
        self.assertEqual(result["calories"], 2500)
        self.assertEqual(result["protein_g"], 144)  # 80 * 1.8


class Test1RM(unittest.TestCase):
    """Test 1RM estimation."""

    def test_1rm_epley(self):
        # Epley: weight * (1 + reps/30)
        result = calculate_1rm(100, 10, "epley")
        self.assertAlmostEqual(result, 133.33, places=2)

    def test_1rm_brzycki(self):
        # Brzycki: weight * (36 / (37 - reps))
        result = calculate_1rm(100, 10, "brzycki")
        self.assertAlmostEqual(result, 133.33, places=2)

    def test_1rm_default(self):
        result = calculate_1rm(100, 5)
        self.assertAlmostEqual(result, 116.67, places=2)


class TestVolume(unittest.TestCase):
    """Test volume calculations."""

    def test_calculate_volume(self):
        result = calculate_volume(4, 10, 80)
        self.assertEqual(result["total_reps"], 40)
        self.assertEqual(result["tonnage_kg"], 3200)
        self.assertEqual(result["avg_per_set"], 800)

    def test_calculate_weekly_volume_below_mev(self):
        result = calculate_weekly_volume(4, 2)
        self.assertEqual(result["weekly_sets"], 8)
        self.assertIn("Below MEV", result["assessment"])

    def test_calculate_weekly_volume_mav(self):
        result = calculate_weekly_volume(8, 2)
        self.assertEqual(result["weekly_sets"], 16)
        self.assertIn("MAV", result["assessment"])

    def test_calculate_weekly_volume_mrv(self):
        result = calculate_weekly_volume(10, 3)
        self.assertEqual(result["weekly_sets"], 30)
        self.assertIn("exceed MRV", result["assessment"])


class TestProtein(unittest.TestCase):
    """Test protein needs calculation."""

    def test_protein_bulk_intermediate(self):
        result = calculate_protein_needs(80, "bulk", "intermediate")
        self.assertEqual(result["daily_low_g"], 144)  # 80 * 1.8
        self.assertEqual(result["daily_high_g"], 176)  # 80 * 2.2

    def test_protein_cut_advanced(self):
        result = calculate_protein_needs(80, "cut", "advanced")
        self.assertEqual(result["daily_low_g"], 176)  # 80 * 2.2
        self.assertEqual(result["daily_high_g"], 224)  # 80 * 2.8


class TestRIR(unittest.TestCase):
    """Test RIR to percentage conversion."""

    def test_rir_0(self):
        result = calculate_rir_to_percentage(0)
        self.assertEqual(result["approximate_percentage"], 100)
        self.assertEqual(result["description"], "Failure")

    def test_rir_2(self):
        result = calculate_rir_to_percentage(2)
        self.assertEqual(result["approximate_percentage"], 90)
        self.assertEqual(result["description"], "2 reps left")

    def test_rir_clamped(self):
        result = calculate_rir_to_percentage(10)
        self.assertEqual(result["approximate_percentage"], 75)


if __name__ == "__main__":
    unittest.main()
