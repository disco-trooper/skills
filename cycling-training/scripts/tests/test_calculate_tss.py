#!/usr/bin/env python3
"""
Tests for calculate_tss.py - Training Stress Score calculations.

Verifies TSS formula, intensity factor, zone estimation, and recovery time.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from calculate_tss import calculate_tss


class TestTSSFormula(unittest.TestCase):
    """Test the core TSS formula calculations."""

    def test_baseline_100_tss(self):
        """
        Test basic TSS formula: FTP=250, NP=250, 60min = 100 TSS.

        When riding at exactly FTP (IF=1.0) for one hour, TSS should be 100.
        Formula: (3600 × 250 × 1.0) / (250 × 3600) × 100 = 100
        """
        result = calculate_tss(ftp=250, np=250, duration_min=60)

        self.assertEqual(result['ftp'], 250)
        self.assertEqual(result['normalized_power'], 250)
        self.assertEqual(result['duration_minutes'], 60)
        self.assertEqual(result['intensity_factor'], 1.0)
        self.assertEqual(result['tss'], 100.0)

    def test_lower_intensity_if_0_8(self):
        """
        Test lower intensity (IF=0.8) TSS calculation.

        FTP=250, NP=200 (IF=0.8), 60min
        TSS = (3600 × 200 × 0.8) / (250 × 3600) × 100 = 64
        """
        result = calculate_tss(ftp=250, np=200, duration_min=60)

        self.assertEqual(result['intensity_factor'], 0.8)
        self.assertEqual(result['tss'], 64.0)

    def test_shorter_duration_30_min(self):
        """
        Test shorter duration (30min) TSS calculation.

        FTP=250, NP=250 (IF=1.0), 30min
        TSS = (1800 × 250 × 1.0) / (250 × 3600) × 100 = 50
        """
        result = calculate_tss(ftp=250, np=250, duration_min=30)

        self.assertEqual(result['duration_minutes'], 30)
        self.assertEqual(result['tss'], 50.0)

    def test_high_intensity_if_1_05(self):
        """
        Test above-threshold intensity (IF=1.05) TSS calculation.

        FTP=200, NP=210 (IF=1.05), 60min
        TSS = (3600 × 210 × 1.05) / (200 × 3600) × 100 = 110.25
        """
        result = calculate_tss(ftp=200, np=210, duration_min=60)

        self.assertEqual(result['intensity_factor'], 1.05)
        self.assertEqual(result['tss'], 110.2)  # Rounded to 1 decimal

    def test_very_short_interval(self):
        """
        Test very short high-intensity interval (20min at IF=1.2).

        FTP=300, NP=360 (IF=1.2), 20min
        TSS = (1200 × 360 × 1.2) / (300 × 3600) × 100 = 48
        """
        result = calculate_tss(ftp=300, np=360, duration_min=20)

        self.assertEqual(result['intensity_factor'], 1.2)
        self.assertEqual(result['tss'], 48.0)

    def test_long_endurance_ride(self):
        """
        Test long endurance ride (3 hours at IF=0.7).

        FTP=250, NP=175 (IF=0.7), 180min
        TSS = (10800 × 175 × 0.7) / (250 × 3600) × 100 = 147
        """
        result = calculate_tss(ftp=250, np=175, duration_min=180)

        self.assertEqual(result['intensity_factor'], 0.7)
        self.assertEqual(result['tss'], 147.0)


class TestIntensityFactorCalculation(unittest.TestCase):
    """Test IF (Intensity Factor) calculations."""

    def test_if_exact_ftp(self):
        """IF should be 1.0 when NP equals FTP."""
        result = calculate_tss(ftp=250, np=250, duration_min=60)
        self.assertEqual(result['intensity_factor'], 1.0)

    def test_if_below_ftp(self):
        """IF should be < 1.0 when NP is below FTP."""
        result = calculate_tss(ftp=250, np=187.5, duration_min=60)
        self.assertEqual(result['intensity_factor'], 0.75)

    def test_if_above_ftp(self):
        """IF should be > 1.0 when NP exceeds FTP."""
        result = calculate_tss(ftp=250, np=275, duration_min=60)
        self.assertEqual(result['intensity_factor'], 1.1)

    def test_if_rounding(self):
        """IF should be rounded to 3 decimal places."""
        # NP=233 / FTP=250 = 0.932
        result = calculate_tss(ftp=250, np=233, duration_min=60)
        self.assertEqual(result['intensity_factor'], 0.932)

    def test_if_very_low_recovery(self):
        """Test very low IF for recovery ride (IF < 0.55)."""
        result = calculate_tss(ftp=250, np=125, duration_min=60)
        self.assertEqual(result['intensity_factor'], 0.5)


class TestZoneEstimation(unittest.TestCase):
    """Test training zone estimation based on IF."""

    def test_zone_1_recovery(self):
        """Z1 Recovery: IF < 0.55"""
        result = calculate_tss(ftp=250, np=125, duration_min=60)  # IF=0.5
        self.assertEqual(result['estimated_zone'], "Z1 Recovery")

    def test_zone_2_endurance(self):
        """Z2 Endurance: 0.55 <= IF < 0.75"""
        result = calculate_tss(ftp=250, np=162.5, duration_min=60)  # IF=0.65
        self.assertEqual(result['estimated_zone'], "Z2 Endurance")

    def test_zone_2_lower_boundary(self):
        """Z2 at exact lower boundary (IF=0.55)."""
        result = calculate_tss(ftp=200, np=110, duration_min=60)  # IF=0.55
        self.assertEqual(result['estimated_zone'], "Z2 Endurance")

    def test_zone_3_tempo(self):
        """Z3 Tempo: 0.75 <= IF < 0.90"""
        result = calculate_tss(ftp=250, np=200, duration_min=60)  # IF=0.8
        self.assertEqual(result['estimated_zone'], "Z3 Tempo")

    def test_zone_4_threshold(self):
        """Z4 Threshold: 0.90 <= IF < 1.05"""
        result = calculate_tss(ftp=250, np=237.5, duration_min=60)  # IF=0.95
        self.assertEqual(result['estimated_zone'], "Z4 Threshold")

    def test_zone_4_exact_ftp(self):
        """Z4 at exactly FTP (IF=1.0)."""
        result = calculate_tss(ftp=250, np=250, duration_min=60)  # IF=1.0
        self.assertEqual(result['estimated_zone'], "Z4 Threshold")

    def test_zone_5_vo2max(self):
        """Z5 VO2max: 1.05 <= IF < 1.20"""
        result = calculate_tss(ftp=250, np=275, duration_min=60)  # IF=1.1
        self.assertEqual(result['estimated_zone'], "Z5 VO2max")

    def test_zone_6_anaerobic(self):
        """Z6+ Anaerobic: IF >= 1.20"""
        result = calculate_tss(ftp=250, np=312.5, duration_min=60)  # IF=1.25
        self.assertEqual(result['estimated_zone'], "Z6+ Anaerobic")


class TestRecoveryHoursEstimation(unittest.TestCase):
    """Test recovery time estimation based on TSS."""

    def test_recovery_hours_baseline(self):
        """100 TSS should require ~2 hours recovery (TSS/50)."""
        result = calculate_tss(ftp=250, np=250, duration_min=60)
        self.assertEqual(result['recovery_hours'], 2.0)

    def test_recovery_hours_easy_ride(self):
        """50 TSS should require ~1 hour recovery."""
        result = calculate_tss(ftp=250, np=250, duration_min=30)
        self.assertEqual(result['recovery_hours'], 1.0)

    def test_recovery_hours_hard_ride(self):
        """147 TSS should require ~2.9 hours recovery."""
        result = calculate_tss(ftp=250, np=175, duration_min=180)
        self.assertEqual(result['recovery_hours'], 2.9)


class TestOutputStructure(unittest.TestCase):
    """Test that the output dictionary has all required keys."""

    def test_all_keys_present(self):
        """Result dictionary should contain all expected keys."""
        result = calculate_tss(ftp=250, np=250, duration_min=60)

        expected_keys = {
            'ftp',
            'normalized_power',
            'duration_minutes',
            'intensity_factor',
            'tss',
            'estimated_zone',
            'recovery_hours'
        }

        self.assertEqual(set(result.keys()), expected_keys)

    def test_normalized_power_rounding(self):
        """Normalized power should be rounded to 1 decimal place."""
        result = calculate_tss(ftp=250, np=233.333, duration_min=60)
        self.assertEqual(result['normalized_power'], 233.3)

    def test_tss_rounding(self):
        """TSS should be rounded to 1 decimal place."""
        # FTP=250, NP=233.333, 60min
        # IF = 233.333/250 = 0.9333...
        # TSS = (3600 * 233.333 * 0.9333) / (250 * 3600) * 100 = 87.11...
        result = calculate_tss(ftp=250, np=233.333, duration_min=60)
        # TSS = (233.333 * 0.9333) / 250 * 100 = 87.11 (roughly)
        self.assertIsInstance(result['tss'], float)
        # Check it's properly rounded (1 decimal)
        self.assertEqual(result['tss'], round(result['tss'], 1))


class TestParametrizedFTPNPCombinations(unittest.TestCase):
    """Parametrized tests for various FTP/NP combinations."""

    def test_various_ftp_np_combinations(self):
        """
        Test TSS calculations for various FTP and NP combinations.

        Verifies the formula: TSS = (duration_sec × NP × IF) / (FTP × 3600) × 100
        """
        test_cases = [
            # (ftp, np, duration_min, expected_if, expected_tss)
            (200, 200, 60, 1.0, 100.0),      # Baseline at FTP=200
            (300, 300, 60, 1.0, 100.0),      # Baseline at FTP=300
            (250, 225, 60, 0.9, 81.0),       # Tempo ride
            (250, 262.5, 60, 1.05, 110.2),   # Above threshold (rounded)
            (200, 160, 45, 0.8, 48.0),       # Short Z3 ride
            (300, 210, 90, 0.7, 73.5),       # Long Z2 ride
            (250, 250, 120, 1.0, 200.0),     # 2-hour FTP test equivalent
            (280, 252, 60, 0.9, 81.0),       # Different FTP, same IF
        ]

        for ftp, np, duration, expected_if, expected_tss in test_cases:
            with self.subTest(ftp=ftp, np=np, duration=duration):
                result = calculate_tss(ftp=ftp, np=np, duration_min=duration)
                self.assertEqual(result['intensity_factor'], expected_if,
                    f"IF mismatch for FTP={ftp}, NP={np}")
                self.assertAlmostEqual(result['tss'], expected_tss, places=1,
                    msg=f"TSS mismatch for FTP={ftp}, NP={np}, duration={duration}")

    def test_ftp_range_low_to_high(self):
        """Test TSS calculation across typical FTP range (150-400W)."""
        ftps = [150, 200, 250, 300, 350, 400]

        for ftp in ftps:
            with self.subTest(ftp=ftp):
                # Ride at 80% of FTP for 1 hour = 64 TSS regardless of FTP
                np = ftp * 0.8
                result = calculate_tss(ftp=ftp, np=np, duration_min=60)

                self.assertEqual(result['intensity_factor'], 0.8)
                self.assertEqual(result['tss'], 64.0)

    def test_duration_range(self):
        """Test TSS scales linearly with duration."""
        durations = [15, 30, 45, 60, 90, 120, 180]

        for duration in durations:
            with self.subTest(duration=duration):
                result = calculate_tss(ftp=250, np=250, duration_min=duration)

                # At IF=1.0, TSS = duration * 100 / 60
                expected_tss = duration * 100 / 60
                self.assertAlmostEqual(result['tss'], expected_tss, places=1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_very_short_duration(self):
        """Test very short duration (5 minutes)."""
        result = calculate_tss(ftp=250, np=300, duration_min=5)
        self.assertGreater(result['tss'], 0)
        self.assertEqual(result['duration_minutes'], 5)

    def test_very_long_duration(self):
        """Test very long duration (6 hours)."""
        result = calculate_tss(ftp=250, np=150, duration_min=360)
        # 6 hours at IF=0.6
        # TSS = (360*60 * 150 * 0.6) / (250 * 3600) * 100 = 216
        self.assertEqual(result['intensity_factor'], 0.6)
        self.assertAlmostEqual(result['tss'], 216.0, places=1)

    def test_fractional_duration(self):
        """Test fractional duration (45.5 minutes)."""
        result = calculate_tss(ftp=250, np=250, duration_min=45.5)
        self.assertEqual(result['duration_minutes'], 45.5)
        # TSS = 45.5/60 * 100 = 75.83...
        self.assertAlmostEqual(result['tss'], 75.8, places=1)

    def test_fractional_np(self):
        """Test fractional NP value."""
        result = calculate_tss(ftp=250, np=187.5, duration_min=60)
        self.assertEqual(result['normalized_power'], 187.5)
        self.assertEqual(result['intensity_factor'], 0.75)

    def test_zone_boundary_if_0_55(self):
        """Test zone boundary at IF=0.55 (Z1/Z2 boundary)."""
        result = calculate_tss(ftp=200, np=110, duration_min=60)  # IF=0.55 exactly
        self.assertEqual(result['estimated_zone'], "Z2 Endurance")

    def test_zone_boundary_if_0_75(self):
        """Test zone boundary at IF=0.75 (Z2/Z3 boundary)."""
        result = calculate_tss(ftp=200, np=150, duration_min=60)  # IF=0.75 exactly
        self.assertEqual(result['estimated_zone'], "Z3 Tempo")

    def test_zone_boundary_if_0_90(self):
        """Test zone boundary at IF=0.90 (Z3/Z4 boundary)."""
        result = calculate_tss(ftp=200, np=180, duration_min=60)  # IF=0.90 exactly
        self.assertEqual(result['estimated_zone'], "Z4 Threshold")

    def test_zone_boundary_if_1_05(self):
        """Test zone boundary at IF=1.05 (Z4/Z5 boundary)."""
        result = calculate_tss(ftp=200, np=210, duration_min=60)  # IF=1.05 exactly
        self.assertEqual(result['estimated_zone'], "Z5 VO2max")

    def test_zone_boundary_if_1_20(self):
        """Test zone boundary at IF=1.20 (Z5/Z6 boundary)."""
        result = calculate_tss(ftp=200, np=240, duration_min=60)  # IF=1.20 exactly
        self.assertEqual(result['estimated_zone'], "Z6+ Anaerobic")


if __name__ == '__main__':
    unittest.main(verbosity=2)
