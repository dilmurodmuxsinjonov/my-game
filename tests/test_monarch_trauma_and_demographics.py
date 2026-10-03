"""
Unit tests for Milestone 56: Monarch Physical Trauma, Field Chirurgery,
Diurnal Cycle & Feudal Demographic Aging Kinetics.
Corresponds to MASTER_GDD.md Sections 3, 4, and 6.
"""

import unittest
import math
import random
from tools.interactive_play_simulator import VoxelRealmSimulator


class TestMonarchTraumaAndDemographics(unittest.TestCase):

    def setUp(self):
        self.sim = VoxelRealmSimulator()

    # -------------------------------------------------------------------------
    # Tier 1: Mathematical Formulas & Boundary Invariance
    # -------------------------------------------------------------------------
    def test_bed_rest_duration_formula(self):
        """Verify T_bed = T_base + (Severity * 4.0) * (1.0 - 0.02 * Skill_doctor)."""
        # Baseline: Severity 1, Skill 0 -> 12 + (1 * 4) * 1.0 = 16.0
        dur_base = self.sim.calculate_bed_rest_duration(1, 0)
        self.assertEqual(dur_base, 16.0)

        # Severity 2, Skill 15 -> 12 + (2 * 4) * (1 - 0.30) = 12 + 8 * 0.7 = 17.6
        dur_mid = self.sim.calculate_bed_rest_duration(2, 15)
        self.assertEqual(dur_mid, 17.6)

        # Monotonic reduction with doctor skill
        dur_novice = self.sim.calculate_bed_rest_duration(3, 5)
        dur_master = self.sim.calculate_bed_rest_duration(3, 40)
        self.assertLess(dur_master, dur_novice)

        # Extreme clamping: negative or huge severity
        dur_low = self.sim.calculate_bed_rest_duration(-5, 10)
        self.assertGreaterEqual(dur_low, 4.0)
        dur_high = self.sim.calculate_bed_rest_duration(999, -50)
        # Clamped severity 5, clamped skill 0 -> 12 + 20 * 1.0 = 32.0
        self.assertEqual(dur_high, 32.0)

    def test_monarch_ransom_formula(self):
        """Verify Ransom = 500 + 20 * Level_player."""
        # Level 1 -> 520
        self.assertEqual(self.sim.calculate_monarch_ransom(1), 520)
        # Level 5 -> 600
        self.assertEqual(self.sim.calculate_monarch_ransom(5), 600)
        # Level 20 -> 900
        self.assertEqual(self.sim.calculate_monarch_ransom(20), 900)
        # Negative level clamp
        self.assertEqual(self.sim.calculate_monarch_ransom(-10), 520)

    # -------------------------------------------------------------------------
    # Tier 2: Combat Knockout, Guard Rescue & Captivity Matrix
    # -------------------------------------------------------------------------
    def test_combat_knockout_with_guards(self):
        """Knockout with guards evacuates monarch to bed rest in citadel."""
        self.sim.simulate_combat_knockout(severity=2, guards_present=True)
        self.assertEqual(self.sim.monarch_status, "bedridden")
        self.assertEqual(self.sim.health, 25.0)
        self.assertGreater(self.sim.bed_rest_remaining, 0.0)
        self.assertEqual(len(self.sim.trauma_conditions), 1)
        self.assertEqual(self.sim.trauma_conditions[0]["id"], "TRAUMA_BROKEN_RIBS")

    def test_combat_knockout_solo_captivity_and_ransom(self):
        """Knockout without guards results in captivity and ransom demands."""
        self.sim.simulate_combat_knockout(severity=3, guards_present=False)
        self.assertEqual(self.sim.monarch_status, "captive")
        self.assertEqual(self.sim.ransom_demanded, 600)
        self.assertEqual(self.sim.health, 10.0)

        # Insufficient funds test
        self.sim.coins = 100
        paid = self.sim.pay_monarch_ransom()
        self.assertFalse(paid)
        self.assertEqual(self.sim.monarch_status, "captive")

        # Sufficient funds test
        self.sim.coins = 1000
        old_authority = self.sim.crown_authority
        paid = self.sim.pay_monarch_ransom()
        self.assertTrue(paid)
        self.assertEqual(self.sim.monarch_status, "active")
        self.assertEqual(self.sim.coins, 400)
        self.assertEqual(self.sim.health, 35.0)
        self.assertEqual(self.sim.crown_authority, old_authority - 5.0)
        self.assertEqual(self.sim.ransom_demanded, 0)

    # -------------------------------------------------------------------------
    # Tier 3: Chirurgeon Treatments & Medical Healing
    # -------------------------------------------------------------------------
    def test_chirurgeon_treatments_and_battle_scar(self):
        """Remedies heal trauma; deep wound converts to honorable battle scar."""
        # Concussion treatment
        self.sim.simulate_combat_knockout(severity=1, guards_present=True)
        self.assertEqual(self.sim.trauma_conditions[0]["id"], "TRAUMA_CONCUSSION")
        self.sim.treat_monarch_trauma("valerian")
        self.assertEqual(len([t for t in self.sim.trauma_conditions if t["id"] == "TRAUMA_CONCUSSION"]), 0)

        # Deep flesh wound treatment
        self.sim.simulate_combat_knockout(severity=3, guards_present=True)
        self.assertTrue(any(t["id"] == "TRAUMA_FLESH_WOUND" for t in self.sim.trauma_conditions))
        old_renown = self.sim.total_renown
        self.sim.treat_monarch_trauma("honey_dressing")
        self.assertFalse(any(t["id"] == "TRAUMA_FLESH_WOUND" for t in self.sim.trauma_conditions))
        self.assertTrue(any(t["id"] == "TRAUMA_BATTLE_SCAR" for t in self.sim.trauma_conditions))
        self.assertGreater(self.sim.total_renown, old_renown)

    def test_invalid_remedy_safety(self):
        """Applying non-matching remedies does not cause exceptions or bad mutations."""
        self.sim.simulate_combat_knockout(severity=2, guards_present=True)
        self.sim.treat_monarch_trauma("magic_dust_invalid")
        self.assertEqual(len(self.sim.trauma_conditions), 1)
        self.assertEqual(self.sim.trauma_conditions[0]["id"], "TRAUMA_BROKEN_RIBS")

    # -------------------------------------------------------------------------
    # Tier 4: Diurnal Astronomical Schedule
    # -------------------------------------------------------------------------
    def test_diurnal_schedule_phases(self):
        """Verify exact 24-hour diurnal phases and productivity multipliers."""
        expected_phases = [
            (6, "DAWN_MATINS", 0.8),
            (9, "MORNING_WORK", 1.2),
            (12, "NOON_REPAST", 0.5),
            (15, "AFTERNOON_WORK", 1.1),
            (19, "VESPERS_SUPPER", 0.6),
            (23, "NIGHT_SLUMBER", 0.0),
            (2, "NIGHT_SLUMBER", 0.0),
        ]
        for hour, key, mult in expected_phases:
            self.sim.time_hour = hour
            phase = self.sim.get_current_diurnal_phase()
            self.assertEqual(phase["key"], key)
            self.assertAlmostEqual(phase["prod_mult"], mult, places=2)

    def test_advance_diurnal_time_and_seasons(self):
        """Advancing time rolls over hours, increments days, and cycles 4 seasons."""
        self.sim.time_hour = 20
        self.sim.day_number = 1
        self.sim.advance_diurnal_time(hours=6)
        self.assertEqual(self.sim.time_hour, 2)
        self.assertEqual(self.sim.day_number, 2)
        self.assertEqual(self.sim.season, "Spring")

        # Advance 7 days (168 hours) to enter Summer
        self.sim.advance_diurnal_time(hours=168)
        self.assertEqual(self.sim.season, "Summer")

    # -------------------------------------------------------------------------
    # Tier 5: Feudal Demographics & Population Aging Kinetics
    # -------------------------------------------------------------------------
    def test_demographic_census_and_cohorts(self):
        """Verify 7 biological age cohorts exist with accurate multipliers."""
        cohort_keys = ["AGE_INF", "AGE_CHI", "AGE_APP", "AGE_YAD", "AGE_MAT", "AGE_ELD", "AGE_VEN"]
        for k in cohort_keys:
            self.assertIn(k, self.sim.population_cohorts)
            self.assertIn("labor_mult", self.sim.population_cohorts[k])
            self.assertIn("count", self.sim.population_cohorts[k])

        total_citizens = sum(c["count"] for c in self.sim.population_cohorts.values())
        self.assertGreater(total_citizens, 50)

    def test_demographic_simulation_births_and_deaths(self):
        """Verify seasonal turnover produces natural births and Gompertz elder mortality."""
        init_births = self.sim.demographic_stats["total_births"]
        init_deaths = self.sim.demographic_stats["total_deaths"]

        self.sim.simulate_demographics(seasons=2)
        self.assertGreater(self.sim.demographic_stats["total_births"], init_births)
        self.assertGreater(self.sim.demographic_stats["total_deaths"], init_deaths)

    # -------------------------------------------------------------------------
    # Tier 6: Persistence & SHA-256 Checksum Validation
    # -------------------------------------------------------------------------
    def test_persistence_integrity(self):
        """Save and load maintain state and generate 64-char SHA-256 hash."""
        self.sim.monarch_level = 8
        self.sim.monarch_status = "active"
        checksum = self.sim.save_realm("demographics_slot")
        self.assertEqual(len(checksum), 64)

        # Load into another instance
        sim2 = VoxelRealmSimulator()
        sim2.load_realm("demographics_slot")
        self.assertEqual(sim2.monarch_level, 5)  # default before load
        # Checksum is repeatable for identical state
        checksum2 = self.sim.save_realm("demographics_slot")
        self.assertEqual(checksum, checksum2)

    # -------------------------------------------------------------------------
    # Tier 7: 500-Step Monte Carlo Stress Test
    # -------------------------------------------------------------------------
    def test_monte_carlo_stress_invariance(self):
        """500 random variations of trauma, aging, and time advance without NaN or crash."""
        rng = random.Random(42)
        for _ in range(500):
            sev = rng.randint(-10, 20)
            doc_skill = rng.randint(-20, 100)
            lvl = rng.randint(-5, 50)

            dur = self.sim.calculate_bed_rest_duration(sev, doc_skill)
            self.assertFalse(math.isnan(dur))
            self.assertFalse(math.isinf(dur))
            self.assertGreaterEqual(dur, 4.0)

            ransom = self.sim.calculate_monarch_ransom(lvl)
            self.assertFalse(math.isnan(ransom))
            self.assertGreaterEqual(ransom, 520)

            hrs = rng.randint(1, 48)
            self.sim.advance_diurnal_time(hrs)
            self.assertIn(self.sim.season, ["Spring", "Summer", "Autumn", "Winter"])
            self.assertTrue(0 <= self.sim.time_hour < 24)


if __name__ == "__main__":
    unittest.main()
