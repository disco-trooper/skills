#!/usr/bin/env python3
"""
Tests for analyze_week.py - Weekly training load analysis.

Verifies TSB, ACWR, Monotony/Strain calculations, status interpretations,
and the full analyze_week() function including warnings.
"""

import sys
import math
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyze_week import (
    calculate_tsb,
    calculate_acwr,
    calculate_monotony_strain,
    estimate_ramp_rate,
    get_acwr_status,
    get_tsb_status,
    get_ramp_status,
    get_monotony_status,
    analyze_week
)


class TestCalculateTSB(unittest.TestCase):
    """Test TSB (Training Stress Balance) calculation."""

    def test_tsb_positive_fresh(self):
        """TSB should be positive when CTL > ATL (fresh)."""
        tsb = calculate_tsb(ctl=80, atl=60)
        self.assertEqual(tsb, 20)

    def test_tsb_negative_fatigued(self):
        """TSB should be negative when CTL < ATL (fatigued)."""
        tsb = calculate_tsb(ctl=65, atl=80)
        self.assertEqual(tsb, -15)

    def test_tsb_zero_balanced(self):
        """TSB should be zero when CTL equals ATL."""
        tsb = calculate_tsb(ctl=70, atl=70)
        self.assertEqual(tsb, 0)

    def test_tsb_very_negative_overreaching(self):
        """TSB very negative indicates overreaching."""
        tsb = calculate_tsb(ctl=60, atl=100)
        self.assertEqual(tsb, -40)

    def test_tsb_very_positive_peaked(self):
        """TSB very positive indicates peaked/rested state."""
        tsb = calculate_tsb(ctl=90, atl=55)
        self.assertEqual(tsb, 35)

    def test_tsb_with_floats(self):
        """TSB calculation should handle float inputs."""
        tsb = calculate_tsb(ctl=72.5, atl=68.3)
        self.assertAlmostEqual(tsb, 4.2, places=1)

    def test_tsb_zero_inputs(self):
        """TSB should handle zero CTL and ATL."""
        tsb = calculate_tsb(ctl=0, atl=0)
        self.assertEqual(tsb, 0)


class TestCalculateACWR(unittest.TestCase):
    """Test ACWR (Acute:Chronic Workload Ratio) calculation."""

    def test_acwr_optimal_ratio(self):
        """ACWR = ATL/CTL, optimal range 0.8-1.3."""
        acwr = calculate_acwr(ctl=70, atl=70)
        self.assertEqual(acwr, 1.0)

    def test_acwr_undertrained(self):
        """ACWR < 0.8 indicates undertraining."""
        acwr = calculate_acwr(ctl=80, atl=50)
        self.assertEqual(acwr, 0.625)

    def test_acwr_danger_zone(self):
        """ACWR > 1.5 indicates danger zone."""
        acwr = calculate_acwr(ctl=60, atl=100)
        self.assertAlmostEqual(acwr, 1.667, places=3)

    def test_acwr_zero_ctl_returns_zero(self):
        """ACWR should return 0 when CTL is 0 (avoid division by zero)."""
        acwr = calculate_acwr(ctl=0, atl=50)
        self.assertEqual(acwr, 0.0)

    def test_acwr_negative_ctl_returns_zero(self):
        """ACWR should return 0 when CTL is negative."""
        acwr = calculate_acwr(ctl=-10, atl=50)
        self.assertEqual(acwr, 0.0)

    def test_acwr_with_floats(self):
        """ACWR calculation should handle float inputs."""
        acwr = calculate_acwr(ctl=72.5, atl=85.3)
        self.assertAlmostEqual(acwr, 85.3 / 72.5, places=3)

    def test_acwr_caution_zone(self):
        """ACWR between 1.3 and 1.5 is caution zone."""
        acwr = calculate_acwr(ctl=70, atl=98)  # 1.4
        self.assertEqual(acwr, 1.4)


class TestCalculateMonotonyStrain(unittest.TestCase):
    """Test Foster's Monotony and Strain metrics calculation."""

    def test_monotony_varied_training(self):
        """
        Varied training (rest days, different intensities) = low monotony.

        Daily TSS: [60, 80, 0, 70, 90, 80, 0]
        Mean = 54.3, Std = 35.1
        Monotony = 54.3 / 35.1 = 1.55
        """
        daily_tss = [60, 80, 0, 70, 90, 80, 0]
        result = calculate_monotony_strain(daily_tss)

        self.assertIsNotNone(result['monotony'])
        self.assertLess(result['monotony'], 2.0)  # Good variety
        self.assertGreater(result['strain'], 0)

    def test_monotony_uniform_training(self):
        """
        Uniform training (same TSS daily) = high monotony.

        Daily TSS: [70, 70, 70, 70, 70, 70, 70]
        Std = 0, so monotony = inf
        """
        daily_tss = [70, 70, 70, 70, 70, 70, 70]
        result = calculate_monotony_strain(daily_tss)

        self.assertEqual(result['monotony'], float('inf'))
        self.assertEqual(result['strain'], float('inf'))
        self.assertIn('warning', result)

    def test_monotony_nearly_uniform(self):
        """Nearly uniform training should have high monotony."""
        daily_tss = [70, 71, 70, 71, 70, 71, 70]
        result = calculate_monotony_strain(daily_tss)

        self.assertIsNotNone(result['monotony'])
        self.assertGreater(result['monotony'], 100)  # Very high

    def test_strain_calculation(self):
        """
        Strain = weekly_load × monotony.

        Higher strain + high monotony = injury/illness risk.
        """
        daily_tss = [60, 80, 40, 70, 90, 80, 30]
        result = calculate_monotony_strain(daily_tss)

        weekly_load = sum(daily_tss)
        expected_strain = weekly_load * result['monotony']

        self.assertAlmostEqual(result['strain'], expected_strain, delta=1)

    def test_insufficient_data_error(self):
        """Need at least 3 days for monotony calculation."""
        result = calculate_monotony_strain([60, 80])

        self.assertIsNone(result['monotony'])
        self.assertIsNone(result['strain'])
        self.assertIn('error', result)

    def test_single_day_error(self):
        """Single day data should return error."""
        result = calculate_monotony_strain([100])

        self.assertIsNone(result['monotony'])
        self.assertIn('error', result)

    def test_empty_list_error(self):
        """Empty list should return error."""
        result = calculate_monotony_strain([])

        self.assertIsNone(result['monotony'])
        self.assertIn('error', result)

    def test_result_structure(self):
        """Result should contain all expected keys."""
        daily_tss = [60, 80, 0, 70, 90, 80, 70]
        result = calculate_monotony_strain(daily_tss)

        expected_keys = {'monotony', 'strain', 'weekly_load', 'mean_daily', 'std_daily'}
        self.assertTrue(expected_keys.issubset(set(result.keys())))

    def test_weekly_load_sum(self):
        """Weekly load should equal sum of daily TSS."""
        daily_tss = [60, 80, 0, 70, 90, 80, 70]
        result = calculate_monotony_strain(daily_tss)

        self.assertEqual(result['weekly_load'], sum(daily_tss))

    def test_mean_daily_calculation(self):
        """Mean daily should be average of daily TSS."""
        daily_tss = [60, 80, 40, 70, 90, 80, 30]
        result = calculate_monotony_strain(daily_tss)

        expected_mean = sum(daily_tss) / len(daily_tss)
        self.assertAlmostEqual(result['mean_daily'], expected_mean, places=1)


class TestEstimateRampRate(unittest.TestCase):
    """Test ramp rate estimation."""

    def test_ramp_rate_positive_building(self):
        """Positive ramp rate when weekly TSS exceeds CTL×7."""
        # Weekly TSS = 700, CTL = 70
        # Daily avg = 100, CTL = 70
        # Ramp = (100 - 70) / 6 * 7 = 35
        ramp = estimate_ramp_rate(weekly_tss=700, ctl=70)
        self.assertGreater(ramp, 0)

    def test_ramp_rate_negative_detraining(self):
        """Negative ramp rate when weekly TSS below CTL×7."""
        # Weekly TSS = 350, CTL = 70
        # Daily avg = 50, CTL = 70
        # Ramp = (50 - 70) / 6 * 7 = -23.3
        ramp = estimate_ramp_rate(weekly_tss=350, ctl=70)
        self.assertLess(ramp, 0)

    def test_ramp_rate_zero_maintenance(self):
        """Zero ramp rate when at maintenance level."""
        # Weekly TSS = 490, CTL = 70
        # Daily avg = 70, CTL = 70
        # Ramp = 0
        ramp = estimate_ramp_rate(weekly_tss=490, ctl=70)
        self.assertEqual(ramp, 0)

    def test_ramp_rate_aggressive(self):
        """Test aggressive ramp rate detection (>8 CTL/week)."""
        # Need daily avg significantly above CTL
        ramp = estimate_ramp_rate(weekly_tss=700, ctl=50)
        self.assertGreater(ramp, 8)


class TestGetACWRStatus(unittest.TestCase):
    """Test ACWR status interpretation based on Gabbett 2016, Hulin 2014."""

    def test_acwr_undertrained(self):
        """ACWR < 0.8 = UNDERTRAINED."""
        status = get_acwr_status(0.6)

        self.assertEqual(status['status'], 'UNDERTRAINED')
        self.assertEqual(status['color'], 'yellow')
        self.assertIn('Increase', status['recommendation'])

    def test_acwr_optimal_lower_bound(self):
        """ACWR = 0.8 = OPTIMAL (lower bound)."""
        status = get_acwr_status(0.8)

        self.assertEqual(status['status'], 'OPTIMAL')
        self.assertEqual(status['color'], 'green')

    def test_acwr_optimal_upper_bound(self):
        """ACWR = 1.3 = OPTIMAL (upper bound)."""
        status = get_acwr_status(1.3)

        self.assertEqual(status['status'], 'OPTIMAL')
        self.assertEqual(status['color'], 'green')

    def test_acwr_optimal_middle(self):
        """ACWR = 1.0 = OPTIMAL (perfect balance)."""
        status = get_acwr_status(1.0)

        self.assertEqual(status['status'], 'OPTIMAL')
        self.assertEqual(status['color'], 'green')
        self.assertIn('Sweet spot', status['recommendation'])

    def test_acwr_caution(self):
        """ACWR 1.3-1.5 = CAUTION."""
        status = get_acwr_status(1.4)

        self.assertEqual(status['status'], 'CAUTION')
        self.assertEqual(status['color'], 'orange')
        self.assertIn('Elevated', status['recommendation'])

    def test_acwr_danger(self):
        """ACWR > 1.5 = DANGER."""
        status = get_acwr_status(1.6)

        self.assertEqual(status['status'], 'DANGER')
        self.assertEqual(status['color'], 'red')
        self.assertIn('High injury', status['recommendation'])

    def test_acwr_boundary_0_79(self):
        """ACWR = 0.79 is UNDERTRAINED (just below optimal)."""
        status = get_acwr_status(0.79)
        self.assertEqual(status['status'], 'UNDERTRAINED')

    def test_acwr_boundary_1_31(self):
        """ACWR = 1.31 is CAUTION (just above optimal)."""
        status = get_acwr_status(1.31)
        self.assertEqual(status['status'], 'CAUTION')

    def test_acwr_boundary_1_51(self):
        """ACWR = 1.51 is DANGER (just above caution)."""
        status = get_acwr_status(1.51)
        self.assertEqual(status['status'], 'DANGER')


class TestGetTSBStatus(unittest.TestCase):
    """Test TSB status interpretation."""

    def test_tsb_very_fatigued(self):
        """TSB < -30 = VERY_FATIGUED."""
        status = get_tsb_status(-35)

        self.assertEqual(status['status'], 'VERY_FATIGUED')
        self.assertEqual(status['color'], 'red')
        self.assertIn('Overreaching', status['recommendation'])

    def test_tsb_fatigued(self):
        """TSB -30 to -10 = FATIGUED."""
        status = get_tsb_status(-20)

        self.assertEqual(status['status'], 'FATIGUED')
        self.assertEqual(status['color'], 'orange')
        self.assertIn('Building load', status['recommendation'])

    def test_tsb_neutral(self):
        """TSB -10 to 5 = NEUTRAL."""
        status = get_tsb_status(-5)

        self.assertEqual(status['status'], 'NEUTRAL')
        self.assertEqual(status['color'], 'yellow')
        self.assertIn('Maintenance', status['recommendation'])

    def test_tsb_fresh(self):
        """TSB 5 to 25 = FRESH."""
        status = get_tsb_status(15)

        self.assertEqual(status['status'], 'FRESH')
        self.assertEqual(status['color'], 'green')
        self.assertIn('Good form', status['recommendation'])

    def test_tsb_very_fresh(self):
        """TSB >= 25 = VERY_FRESH."""
        status = get_tsb_status(30)

        self.assertEqual(status['status'], 'VERY_FRESH')
        self.assertEqual(status['color'], 'green')
        self.assertIn('Peak form', status['recommendation'])

    def test_tsb_boundary_minus_30(self):
        """TSB = -30 is FATIGUED (boundary)."""
        status = get_tsb_status(-30)
        self.assertEqual(status['status'], 'FATIGUED')

    def test_tsb_boundary_minus_31(self):
        """TSB = -31 is VERY_FATIGUED (just below boundary)."""
        status = get_tsb_status(-31)
        self.assertEqual(status['status'], 'VERY_FATIGUED')

    def test_tsb_boundary_minus_10(self):
        """TSB = -10 is NEUTRAL (boundary)."""
        status = get_tsb_status(-10)
        self.assertEqual(status['status'], 'NEUTRAL')

    def test_tsb_boundary_5(self):
        """TSB = 5 is FRESH (boundary)."""
        status = get_tsb_status(5)
        self.assertEqual(status['status'], 'FRESH')

    def test_tsb_boundary_25(self):
        """TSB = 25 is VERY_FRESH (boundary)."""
        status = get_tsb_status(25)
        self.assertEqual(status['status'], 'VERY_FRESH')

    def test_tsb_zero(self):
        """TSB = 0 is NEUTRAL."""
        status = get_tsb_status(0)
        self.assertEqual(status['status'], 'NEUTRAL')


class TestGetRampStatus(unittest.TestCase):
    """Test ramp rate status interpretation (heuristic)."""

    def test_ramp_conservative(self):
        """Ramp < 3 = CONSERVATIVE."""
        status = get_ramp_status(2)

        self.assertEqual(status['status'], 'CONSERVATIVE')
        self.assertEqual(status['color'], 'green')

    def test_ramp_moderate(self):
        """Ramp 3-5 = MODERATE."""
        status = get_ramp_status(4)

        self.assertEqual(status['status'], 'MODERATE')
        self.assertEqual(status['color'], 'green')

    def test_ramp_aggressive(self):
        """Ramp 5-8 = AGGRESSIVE."""
        status = get_ramp_status(7)

        self.assertEqual(status['status'], 'AGGRESSIVE')
        self.assertEqual(status['color'], 'orange')
        self.assertIn('monitor', status['recommendation'].lower())

    def test_ramp_excessive(self):
        """Ramp > 8 = EXCESSIVE."""
        status = get_ramp_status(10)

        self.assertEqual(status['status'], 'EXCESSIVE')
        self.assertEqual(status['color'], 'red')
        self.assertIn('Too fast', status['recommendation'])

    def test_ramp_negative(self):
        """Negative ramp rate should be CONSERVATIVE."""
        status = get_ramp_status(-5)
        self.assertEqual(status['status'], 'CONSERVATIVE')


class TestGetMonotonyStatus(unittest.TestCase):
    """Test monotony status interpretation based on Foster 1998."""

    def test_monotony_varied(self):
        """Monotony < 1.5 = VARIED (good)."""
        status = get_monotony_status(1.2)

        self.assertEqual(status['status'], 'VARIED')
        self.assertEqual(status['color'], 'green')

    def test_monotony_moderate(self):
        """Monotony 1.5-2.0 = MODERATE."""
        status = get_monotony_status(1.8)

        self.assertEqual(status['status'], 'MODERATE')
        self.assertEqual(status['color'], 'yellow')

    def test_monotony_high_risk(self):
        """Monotony > 2.0 = HIGH_RISK."""
        status = get_monotony_status(2.5)

        self.assertEqual(status['status'], 'HIGH_RISK')
        self.assertEqual(status['color'], 'red')
        self.assertIn('uniform', status['recommendation'].lower())

    def test_monotony_none(self):
        """Monotony = None = UNKNOWN."""
        status = get_monotony_status(None)

        self.assertEqual(status['status'], 'UNKNOWN')
        self.assertEqual(status['color'], 'gray')


class TestAnalyzeWeekBasic(unittest.TestCase):
    """Test the full analyze_week() function with basic inputs."""

    def test_basic_analysis_structure(self):
        """Result should have all required top-level keys."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72)

        expected_keys = {'input', 'metrics', 'status', 'warnings'}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_input_preserved(self):
        """Input values should be preserved in result."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72)

        self.assertEqual(result['input']['weekly_tss'], 450)
        self.assertEqual(result['input']['ctl'], 65)
        self.assertEqual(result['input']['atl'], 72)

    def test_metrics_calculated(self):
        """All metrics should be calculated correctly."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72)

        # TSB = 65 - 72 = -7
        self.assertEqual(result['metrics']['tsb'], -7.0)

        # ACWR = 72 / 65 = 1.11
        self.assertAlmostEqual(result['metrics']['acwr'], 1.11, places=2)

        # Ramp rate should be calculated
        self.assertIn('ramp_rate', result['metrics'])

    def test_status_included(self):
        """Status interpretations should be included for all metrics."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72)

        self.assertIn('tsb', result['status'])
        self.assertIn('acwr', result['status'])
        self.assertIn('ramp', result['status'])

    def test_warnings_list(self):
        """Warnings should be a list."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72)

        self.assertIsInstance(result['warnings'], list)


class TestAnalyzeWeekWithPrevWeek(unittest.TestCase):
    """Test analyze_week() with previous week TSS comparison."""

    def test_wow_change_calculated(self):
        """Week-over-week change should be calculated."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72, prev_week_tss=400)

        # WoW = (450 - 400) / 400 * 100 = 12.5%
        self.assertIn('week_over_week_change', result['metrics'])
        self.assertAlmostEqual(result['metrics']['week_over_week_change'], 12.5, places=1)

    def test_wow_change_negative(self):
        """Negative WoW change when load decreased."""
        result = analyze_week(weekly_tss=350, ctl=65, atl=72, prev_week_tss=400)

        # WoW = (350 - 400) / 400 * 100 = -12.5%
        self.assertAlmostEqual(result['metrics']['week_over_week_change'], -12.5, places=1)

    def test_wow_warning_over_30_percent(self):
        """Warning when WoW increase > 30%."""
        result = analyze_week(weekly_tss=550, ctl=65, atl=72, prev_week_tss=400)

        # WoW = (550 - 400) / 400 * 100 = 37.5%
        high_warnings = [w for w in result['warnings'] if w['level'] == 'high']
        wow_warnings = [w for w in high_warnings if 'Week-over-week' in w['message']]

        self.assertEqual(len(wow_warnings), 1)

    def test_wow_warning_over_20_percent(self):
        """Moderate warning when WoW increase 20-30%."""
        result = analyze_week(weekly_tss=500, ctl=65, atl=72, prev_week_tss=400)

        # WoW = (500 - 400) / 400 * 100 = 25%
        moderate_warnings = [w for w in result['warnings'] if w['level'] == 'moderate']
        wow_warnings = [w for w in moderate_warnings if 'Week-over-week' in w['message']]

        self.assertEqual(len(wow_warnings), 1)

    def test_wow_zero_prev_week(self):
        """Handle zero previous week TSS."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72, prev_week_tss=0)

        # Should return 0% change (not divide by zero)
        self.assertEqual(result['metrics']['week_over_week_change'], 0)


class TestAnalyzeWeekWithDailyTSS(unittest.TestCase):
    """Test analyze_week() with daily TSS for Monotony/Strain."""

    def test_monotony_included(self):
        """Monotony should be calculated when daily TSS provided."""
        daily_tss = [60, 80, 0, 70, 90, 80, 70]
        result = analyze_week(weekly_tss=450, ctl=65, atl=72, daily_tss=daily_tss)

        self.assertIn('monotony', result['metrics'])
        self.assertIsNotNone(result['metrics']['monotony'])

    def test_strain_included(self):
        """Strain should be calculated when daily TSS provided."""
        daily_tss = [60, 80, 0, 70, 90, 80, 70]
        result = analyze_week(weekly_tss=450, ctl=65, atl=72, daily_tss=daily_tss)

        self.assertIn('strain', result['metrics'])
        self.assertIsNotNone(result['metrics']['strain'])

    def test_monotony_status_included(self):
        """Monotony status should be included."""
        daily_tss = [60, 80, 0, 70, 90, 80, 70]
        result = analyze_week(weekly_tss=450, ctl=65, atl=72, daily_tss=daily_tss)

        self.assertIn('monotony', result['status'])

    def test_high_monotony_warning(self):
        """Warning when monotony > 2.0."""
        # Create daily TSS with high monotony (little variation)
        daily_tss = [70, 72, 68, 70, 71, 69, 70]  # Very uniform
        result = analyze_week(weekly_tss=490, ctl=65, atl=72, daily_tss=daily_tss)

        high_warnings = [w for w in result['warnings'] if w['level'] == 'high']
        monotony_warnings = [w for w in high_warnings if 'Monotony' in w['message']]

        self.assertGreater(len(monotony_warnings), 0)


class TestAnalyzeWeekWarnings(unittest.TestCase):
    """Test warning generation in analyze_week()."""

    def test_acwr_danger_warning(self):
        """Warning when ACWR > 1.5."""
        # CTL=60, ATL=100 -> ACWR = 1.67
        result = analyze_week(weekly_tss=700, ctl=60, atl=100)

        high_warnings = [w for w in result['warnings'] if w['level'] == 'high']
        acwr_warnings = [w for w in high_warnings if 'ACWR' in w['message'] and 'danger' in w['message'].lower()]

        self.assertEqual(len(acwr_warnings), 1)

    def test_acwr_caution_warning(self):
        """Moderate warning when ACWR 1.3-1.5."""
        # CTL=70, ATL=98 -> ACWR = 1.4
        result = analyze_week(weekly_tss=700, ctl=70, atl=98)

        moderate_warnings = [w for w in result['warnings'] if w['level'] == 'moderate']
        acwr_warnings = [w for w in moderate_warnings if 'ACWR' in w['message']]

        self.assertEqual(len(acwr_warnings), 1)

    def test_tsb_very_negative_warning(self):
        """Warning when TSB < -30."""
        # CTL=60, ATL=95 -> TSB = -35
        result = analyze_week(weekly_tss=700, ctl=60, atl=95)

        high_warnings = [w for w in result['warnings'] if w['level'] == 'high']
        tsb_warnings = [w for w in high_warnings if 'TSB' in w['message']]

        self.assertEqual(len(tsb_warnings), 1)

    def test_ramp_excessive_warning(self):
        """Warning when ramp rate > 8."""
        # High weekly TSS relative to low CTL = aggressive ramp
        result = analyze_week(weekly_tss=700, ctl=40, atl=60)

        high_warnings = [w for w in result['warnings'] if w['level'] == 'high']
        ramp_warnings = [w for w in high_warnings if 'Ramp' in w['message'] or 'ramp' in w['message']]

        self.assertGreater(len(ramp_warnings), 0)

    def test_no_warnings_optimal(self):
        """No warnings in optimal training scenario."""
        # Balanced training: ACWR ~1.0, TSB ~-5, moderate ramp
        result = analyze_week(weekly_tss=490, ctl=70, atl=72)

        # Filter out daily TSS related warnings (not provided)
        acwr_tsb_ramp_warnings = [
            w for w in result['warnings']
            if 'ACWR' in w['message'] or 'TSB' in w['message'] or 'Ramp' in w['message']
        ]

        self.assertEqual(len(acwr_tsb_ramp_warnings), 0)


class TestAnalyzeWeekEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_zero_ctl(self):
        """Handle zero CTL (new cyclist)."""
        result = analyze_week(weekly_tss=200, ctl=0, atl=30)

        self.assertEqual(result['metrics']['acwr'], 0.0)  # Avoid division by zero

    def test_zero_atl(self):
        """Handle zero ATL (after rest period)."""
        result = analyze_week(weekly_tss=200, ctl=50, atl=0)

        self.assertEqual(result['metrics']['tsb'], 50.0)
        self.assertEqual(result['metrics']['acwr'], 0.0)

    def test_very_high_values(self):
        """Handle very high training load values."""
        result = analyze_week(weekly_tss=1500, ctl=150, atl=180)

        self.assertIsNotNone(result['metrics']['tsb'])
        self.assertIsNotNone(result['metrics']['acwr'])

    def test_float_values(self):
        """Handle float input values."""
        result = analyze_week(weekly_tss=450.5, ctl=65.3, atl=72.7)

        self.assertIsNotNone(result['metrics']['tsb'])
        self.assertIsNotNone(result['metrics']['acwr'])

    def test_combined_options(self):
        """Test with both prev_week_tss and daily_tss provided."""
        daily_tss = [60, 80, 0, 70, 90, 80, 70]
        result = analyze_week(
            weekly_tss=450,
            ctl=65,
            atl=72,
            prev_week_tss=400,
            daily_tss=daily_tss
        )

        # Should have all metrics
        self.assertIn('week_over_week_change', result['metrics'])
        self.assertIn('monotony', result['metrics'])
        self.assertIn('strain', result['metrics'])


class TestWarningStructure(unittest.TestCase):
    """Test the structure of warning objects."""

    def test_warning_has_level(self):
        """Warnings should have a level (high/moderate)."""
        result = analyze_week(weekly_tss=700, ctl=60, atl=100)

        for warning in result['warnings']:
            self.assertIn('level', warning)
            self.assertIn(warning['level'], ['high', 'moderate'])

    def test_warning_has_message(self):
        """Warnings should have a message."""
        result = analyze_week(weekly_tss=700, ctl=60, atl=100)

        for warning in result['warnings']:
            self.assertIn('message', warning)
            self.assertIsInstance(warning['message'], str)
            self.assertGreater(len(warning['message']), 0)


class TestStatusStructure(unittest.TestCase):
    """Test the structure of status objects."""

    def test_status_has_required_keys(self):
        """Status objects should have status, color, and recommendation."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72)

        for key in ['tsb', 'acwr', 'ramp']:
            status = result['status'][key]
            self.assertIn('status', status)
            self.assertIn('color', status)
            self.assertIn('recommendation', status)

    def test_color_valid(self):
        """Colors should be valid values."""
        result = analyze_week(weekly_tss=450, ctl=65, atl=72)

        valid_colors = {'green', 'yellow', 'orange', 'red', 'gray'}
        for key in ['tsb', 'acwr', 'ramp']:
            self.assertIn(result['status'][key]['color'], valid_colors)


if __name__ == '__main__':
    unittest.main(verbosity=2)
