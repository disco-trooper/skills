#!/usr/bin/env python3
"""
Tests for calculate_zones.py - Power zone calculations.

Verifies zone continuity (no gaps between zones) and correct boundaries.
"""

import re
import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from calculate_zones import coggan_zones, isf_zones, seiler_zones, hr_zones_percent_lthr


def extract_zone_bounds(zone_data: dict) -> list[tuple[int | None, int | None]]:
    """
    Extract (lower, upper) bounds from zone range strings.

    Returns list of tuples: (lower_bound, upper_bound) where None means unbounded.
    Examples:
        "< 137W" -> (None, 136)
        "137-187W" -> (137, 187)
        "> 375W" -> (376, None)
    """
    bounds = []
    for zone_name, zone_info in zone_data['zones'].items():
        range_str = zone_info['range']

        # Match "< X" pattern (upper bound only)
        if match := re.match(r'<\s*(\d+)', range_str):
            upper = int(match.group(1)) - 1  # "< 137" means max is 136
            bounds.append((None, upper))
        # Match "> X" pattern (lower bound only)
        elif match := re.match(r'>\s*(\d+)', range_str):
            lower = int(match.group(1)) + 1  # "> 375" means min is 376
            bounds.append((lower, None))
        # Match "X-Y" pattern (both bounds)
        elif match := re.match(r'(\d+)\s*-\s*(\d+)', range_str):
            bounds.append((int(match.group(1)), int(match.group(2))))
        else:
            raise ValueError(f"Could not parse range: {range_str}")

    return bounds


def check_zone_continuity(zone_data: dict) -> list[str]:
    """
    Check that zones are continuous with no gaps.

    Returns list of error messages (empty if all zones are continuous).
    """
    bounds = extract_zone_bounds(zone_data)
    errors = []

    # Filter to bounded zones only (exclude < and > zones for transition check)
    bounded_zones = []
    zone_names = list(zone_data['zones'].keys())

    for i, (lower, upper) in enumerate(bounds):
        if lower is not None and upper is not None:
            bounded_zones.append((zone_names[i], lower, upper))
        elif lower is None and upper is not None:
            # "< X" zone - remember its upper bound for first bounded zone check
            bounded_zones.append((zone_names[i], None, upper))
        elif lower is not None and upper is None:
            # "> X" zone - check it follows the last bounded zone
            bounded_zones.append((zone_names[i], lower, None))

    # Check transitions between adjacent zones
    for i in range(len(bounded_zones) - 1):
        curr_name, curr_lower, curr_upper = bounded_zones[i]
        next_name, next_lower, next_upper = bounded_zones[i + 1]

        # Skip if current zone has no upper bound (shouldn't happen in middle)
        if curr_upper is None:
            continue
        # Skip if next zone has no lower bound (< X zones)
        if next_lower is None:
            continue

        expected_next_lower = curr_upper + 1

        if next_lower != expected_next_lower:
            gap = next_lower - curr_upper - 1
            if gap > 0:
                errors.append(
                    f"Gap between {curr_name} (ends at {curr_upper}) and "
                    f"{next_name} (starts at {next_lower}): missing {gap}W"
                )
            elif gap < 0:
                errors.append(
                    f"Overlap between {curr_name} (ends at {curr_upper}) and "
                    f"{next_name} (starts at {next_lower}): overlapping by {-gap}W"
                )

    return errors


class TestZoneContinuity(unittest.TestCase):
    """Test that all zone models produce continuous zones without gaps."""

    def test_coggan_zones_continuity_ftp_250(self):
        """Test Coggan zones have no gaps for FTP=250 (the bug case)."""
        zones = coggan_zones(250)
        errors = check_zone_continuity(zones)
        self.assertEqual(errors, [], f"Zone continuity errors found:\n" + "\n".join(errors))

    def test_coggan_zones_continuity_various_ftps(self):
        """Test Coggan zones have no gaps for various FTP values."""
        for ftp in [200, 220, 250, 275, 300, 350]:
            with self.subTest(ftp=ftp):
                zones = coggan_zones(ftp)
                errors = check_zone_continuity(zones)
                self.assertEqual(errors, [],
                    f"Zone continuity errors for FTP={ftp}:\n" + "\n".join(errors))

    def test_isf_zones_continuity_ftp_250(self):
        """Test ISF zones have no gaps for FTP=250."""
        zones = isf_zones(250)
        errors = check_zone_continuity(zones)
        self.assertEqual(errors, [], f"Zone continuity errors found:\n" + "\n".join(errors))

    def test_isf_zones_continuity_various_ftps(self):
        """Test ISF zones have no gaps for various FTP values."""
        for ftp in [200, 220, 250, 275, 300, 350]:
            with self.subTest(ftp=ftp):
                zones = isf_zones(ftp)
                errors = check_zone_continuity(zones)
                self.assertEqual(errors, [],
                    f"Zone continuity errors for FTP={ftp}:\n" + "\n".join(errors))

    def test_seiler_zones_continuity(self):
        """
        Test Seiler zones structure is valid.

        Note: Seiler model uses < and > zones by design (polarized training).
        Zone 1: < LT1, Zone 2: LT1-LT2, Zone 3: > LT2
        This means Zone 1 and Zone 2 share boundary at LT1 (by design).
        We verify the structure is parseable and Zone 2 boundaries are valid.
        """
        for ftp in [200, 250, 300]:
            with self.subTest(ftp=ftp):
                zones = seiler_zones(ftp)
                zone_items = list(zones['zones'].items())

                # Verify 3 zones exist
                self.assertEqual(len(zone_items), 3, "Seiler model should have 3 zones")

                # Verify Zone 2 (middle zone) has valid X-Y format
                z2_name, z2_data = zone_items[1]
                self.assertIn("-", z2_data['range'], f"Zone 2 should have X-Y range: {z2_data['range']}")

                # Verify Zone 2 starts where Zone 1 ends (at LT1)
                lt1 = int(ftp * 0.75)
                self.assertIn(str(lt1), z2_data['range'],
                    f"Zone 2 should start at LT1 ({lt1}W): {z2_data['range']}")


class TestZoneBoundaries(unittest.TestCase):
    """Test specific zone boundary calculations."""

    def test_coggan_z2_z3_boundary_ftp_250(self):
        """
        Verify Z2 ends at Z3_start - 1 for FTP=250.

        Bug: Previously Z2 ended at 187W but Z3 started at 190W,
        leaving 188-189W in no zone.
        """
        zones = coggan_zones(250)
        zone_items = list(zones['zones'].items())

        # Z2 is index 1, Z3 is index 2
        z2_name, z2_data = zone_items[1]
        z3_name, z3_data = zone_items[2]

        # Extract upper bound of Z2
        z2_match = re.search(r'-(\d+)W', z2_data['range'])
        self.assertIsNotNone(z2_match, f"Could not parse Z2 range: {z2_data['range']}")
        z2_upper = int(z2_match.group(1))

        # Extract lower bound of Z3
        z3_match = re.match(r'(\d+)-', z3_data['range'])
        self.assertIsNotNone(z3_match, f"Could not parse Z3 range: {z3_data['range']}")
        z3_lower = int(z3_match.group(1))

        self.assertEqual(z3_lower, z2_upper + 1,
            f"Gap detected: Z2 ends at {z2_upper}W, Z3 starts at {z3_lower}W. "
            f"Expected Z3 to start at {z2_upper + 1}W.")

    def test_isf_z2_z3_boundary_ftp_250(self):
        """Verify ISF Z2 ends at Z3_start - 1 for FTP=250."""
        zones = isf_zones(250)
        zone_items = list(zones['zones'].items())

        # Z2 is index 1, Z3 is index 2
        z2_name, z2_data = zone_items[1]
        z3_name, z3_data = zone_items[2]

        z2_match = re.search(r'-(\d+)W', z2_data['range'])
        z2_upper = int(z2_match.group(1))

        z3_match = re.match(r'(\d+)-', z3_data['range'])
        z3_lower = int(z3_match.group(1))

        self.assertEqual(z3_lower, z2_upper + 1,
            f"Gap detected: Z2 ends at {z2_upper}W, Z3 starts at {z3_lower}W.")


class TestHRZoneContinuity(unittest.TestCase):
    """Test that HR zones are continuous without gaps."""

    def test_hr_zones_percent_lthr_continuity_165(self):
        """Test HR zones have no gaps for LTHR=165."""
        zones = hr_zones_percent_lthr(165)
        errors = check_hr_zone_continuity(zones)
        self.assertEqual(errors, [], f"HR zone continuity errors:\n" + "\n".join(errors))

    def test_hr_zones_percent_lthr_continuity_various(self):
        """Test HR zones have no gaps for various LTHR values."""
        for lthr in [150, 160, 165, 170, 180]:
            with self.subTest(lthr=lthr):
                zones = hr_zones_percent_lthr(lthr)
                errors = check_hr_zone_continuity(zones)
                self.assertEqual(errors, [],
                    f"HR zone continuity errors for LTHR={lthr}:\n" + "\n".join(errors))


def check_hr_zone_continuity(zone_data: dict) -> list[str]:
    """
    Check that HR zones are continuous with no gaps.
    Parses 'X-Y bpm' and '< X bpm' and '> X bpm' formats.
    """
    bounds = []
    errors = []

    for zone_name, zone_info in zone_data['zones'].items():
        range_str = zone_info['range']

        # Match "< X bpm" pattern
        if match := re.match(r'<\s*(\d+)\s*bpm', range_str):
            upper = int(match.group(1)) - 1
            bounds.append((zone_name, None, upper))
        # Match "> X bpm" pattern
        elif match := re.match(r'>\s*(\d+)\s*bpm', range_str):
            lower = int(match.group(1)) + 1
            bounds.append((zone_name, lower, None))
        # Match "X-Y bpm" pattern
        elif match := re.match(r'(\d+)\s*-\s*(\d+)\s*bpm', range_str):
            bounds.append((zone_name, int(match.group(1)), int(match.group(2))))
        else:
            errors.append(f"Could not parse range: {range_str}")
            continue

    # Check transitions
    for i in range(len(bounds) - 1):
        curr_name, curr_lower, curr_upper = bounds[i]
        next_name, next_lower, next_upper = bounds[i + 1]

        if curr_upper is None or next_lower is None:
            continue

        expected_next_lower = curr_upper + 1
        if next_lower != expected_next_lower:
            gap = next_lower - curr_upper - 1
            if gap > 0:
                errors.append(
                    f"Gap between {curr_name} (ends at {curr_upper}) and "
                    f"{next_name} (starts at {next_lower}): missing {gap} bpm"
                )

    return errors


if __name__ == '__main__':
    unittest.main(verbosity=2)
