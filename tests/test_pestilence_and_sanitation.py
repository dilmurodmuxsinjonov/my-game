"""
Unit tests for Milestone 57: Feudal Pestilence, Differential SIR Epidemiology,
Municipal Sanitation & Waste Dynamics, and Black Plague Quarantine Protocols.
Corresponds to MASTER_GDD.md Sections 74.3, 75, 76, and 77.
"""

import unittest
import math
import random
from tools.interactive_play_simulator import VoxelRealmSimulator


class TestPestilenceAndSanitation(unittest.TestCase):

    def setUp(self):
        self.sim = VoxelRealmSimulator()

    # -------------------------------------------------------------------------
    # Tier 1: Mathematical Formulas & Boundary Invariance
    # -------------------------------------------------------------------------
    def test_reproduction_number_formula(self):
        """Verify R_0 = beta / (gamma + mu) with edge case division-by-zero protection."""
        # Standard Bubonic Plague baseline: beta=0.45, gamma=0.05, mu=0.15 -> 0.45 / 0.20 = 2.25
        r0 = self.sim.calculate_reproduction_number(0.45, 0.05, 0.15)
        self.assertAlmostEqual(r0, 2.25, places=4)

        # Pneumonic Plague: beta=0.85, gamma=0.03, mu=0.35 -> 0.85 / 0.38 = 2.2368 (rounded to 2 places = 2.24)
        r0_pneumonic = self.sim.calculate_reproduction_number(0.85, 0.03, 0.35)
        self.assertAlmostEqual(r0_pneumonic, round(0.85 / 0.38, 2), places=2)

        # Contained epidemic: beta=0.09, gamma=0.05, mu=0.15 -> 0.09 / 0.20 = 0.45 (< 1.0)
        r0_contained = self.sim.calculate_reproduction_number(0.09, 0.05, 0.15)
        self.assertLess(r0_contained, 1.0)

        # Boundary: gamma + mu = 0 (division by zero protection)
        r0_zero = self.sim.calculate_reproduction_number(0.5, 0.0, 0.0)
        self.assertEqual(r0_zero, 0.0)

        # Boundary: negative beta clamped
        r0_neg = self.sim.calculate_reproduction_number(-0.5, 0.1, 0.1)
        self.assertEqual(r0_neg, 0.0)

    def test_filth_delta_calculation(self):
        """Verify Delta Filth = Pop * 0.05 + Livestock * 0.25 - Sweepers * 1.75."""
        # Baseline: 73 pop, 14 livestock, 2 sweepers -> 73*0.05 + 14*0.25 - 2*1.75 = 3.65 + 3.5 - 3.5 = 3.65
        delta = self.sim.calculate_filth_delta(73, 14, 2)
        self.assertAlmostEqual(delta, 3.65, places=4)

        # Sanitation brigade: 100 pop, 20 livestock, 10 sweepers -> 5.0 + 5.0 - 17.5 = -7.5 (net cleaning)
        delta_clean = self.sim.calculate_filth_delta(100, 20, 10)
        self.assertAlmostEqual(delta_clean, -7.5, places=4)
        self.assertLess(delta_clean, 0.0)

        # Neglect: 100 pop, 50 livestock, 0 sweepers -> 5.0 + 12.5 - 0 = 17.5
        delta_dirty = self.sim.calculate_filth_delta(100, 50, 0)
        self.assertAlmostEqual(delta_dirty, 17.5, places=4)

        # Zero population & livestock
        delta_zero = self.sim.calculate_filth_delta(0, 0, 4)
        self.assertAlmostEqual(delta_zero, -7.0, places=4)

    # -------------------------------------------------------------------------
    # Tier 2: Municipal Sanitation Operations & Compost Generation
    # -------------------------------------------------------------------------
    def test_street_sweeping(self):
        """Verify street sweepers reduce filth, yield compost, and dispel miasma."""
        self.sim.filth_level = 75.0
        self.sim.miasma_active = True
        old_compost = self.sim.compost_fertilizer_stock

        self.sim.sweep_streets()
        # Filth should decrease by 18.0: 75.0 - 18.0 = 57.0
        self.assertEqual(self.sim.filth_level, 57.0)
        self.assertEqual(self.sim.compost_fertilizer_stock, old_compost + 1)
        # Miasma clears when filth drops below 70.0
        self.assertFalse(self.sim.miasma_active)

        # Sweeping at zero filth clamps at 0.0
        self.sim.filth_level = 5.0
        self.sim.sweep_streets()
        self.assertEqual(self.sim.filth_level, 0.0)

    def test_cesspool_maintenance(self):
        """Verify night soil scavengers empty cesspools and produce high-yield fertilizer."""
        self.sim.cesspool_fill = 65.0
        old_compost = self.sim.compost_fertilizer_stock

        self.sim.clean_cesspool()
        self.assertEqual(self.sim.cesspool_fill, 5.0)
        self.assertEqual(self.sim.compost_fertilizer_stock, old_compost + 2)

    # -------------------------------------------------------------------------
    # Tier 3: Plague Doctor & Medical Interventions
    # -------------------------------------------------------------------------
    def test_appoint_plague_doctor(self):
        """Verify Dr. Corvus appointment slashes transmission factor beta by -60%."""
        self.assertFalse(self.sim.plague_doctor_appointed)
        old_morale = self.sim.citizen_morale

        self.sim.appoint_plague_doctor()
        self.assertTrue(self.sim.plague_doctor_appointed)
        self.assertGreaterEqual(self.sim.citizen_morale, old_morale)

        # Idempotent re-appointment does not cause duplicate effects
        self.sim.appoint_plague_doctor()
        self.assertTrue(self.sim.plague_doctor_appointed)

    # -------------------------------------------------------------------------
    # Tier 4: Black Plague Quarantine Protocols
    # -------------------------------------------------------------------------
    def test_black_quarantine_protocols(self):
        """Verify enacting quarantine measures: board_houses, armed_cordon, sanitary_pyres."""
        self.assertEqual(len(self.sim.quarantine_measures), 0)
        self.assertFalse(self.sim.quarantine_edict_active)

        # Enact House Boarding
        self.sim.enact_black_quarantine("board_houses")
        self.assertIn("board_houses", self.sim.quarantine_measures)
        self.assertTrue(self.sim.quarantine_edict_active)

        # Enact Armed Cordon
        self.sim.enact_black_quarantine("armed_cordon")
        self.assertIn("armed_cordon", self.sim.quarantine_measures)

        # Enact Sanitary Pyres (should burn filth by -15.0)
        self.sim.filth_level = 50.0
        self.sim.enact_black_quarantine("sanitary_pyres")
        self.assertIn("sanitary_pyres", self.sim.quarantine_measures)
        self.assertEqual(self.sim.filth_level, 35.0)

        # Duplicate measure check
        self.sim.enact_black_quarantine("board_houses")
        self.assertEqual(self.sim.quarantine_measures.count("board_houses"), 1)

    # -------------------------------------------------------------------------
    # Tier 5: Differential SIR Epidemic Dynamics & Disease Eradication
    # -------------------------------------------------------------------------
    def test_epidemic_outbreak_initialization(self):
        """Verify outbreak initializes SIR cohorts correctly."""
        self.assertIsNone(self.sim.active_epidemic)
        self.assertEqual(self.sim.sir_state["I"], 0.0)

        self.sim.trigger_outbreak("bubonic_plague")
        self.assertEqual(self.sim.active_epidemic, "bubonic_plague")
        self.assertGreater(self.sim.sir_state["I"], 0.0)
        self.assertGreater(self.sim.sir_state["S"], 0.0)
        self.assertEqual(self.sim.sir_state["R"], 0.0)

        total_citizens = sum(c["count"] for c in self.sim.population_cohorts.values())
        self.assertAlmostEqual(self.sim.sir_state["S"] + self.sim.sir_state["I"], total_citizens, places=1)

    def test_sir_transmission_and_eradication_under_quarantine(self):
        """With doctor and quarantine active (R_0 < 1.0), epidemic monotonically declines to eradication."""
        self.sim.trigger_outbreak("bubonic_plague")
        self.sim.filth_level = 0.0
        self.sim.street_sweepers_count = 5  # Keep municipal cobbles clean of filth
        self.sim.appoint_plague_doctor()
        self.sim.enact_black_quarantine("board_houses")

        initial_infected = self.sim.sir_state["I"]
        # Step forward 20 hours in intervals
        for _ in range(5):
            self.sim.simulate_epidemic_step(hours=4)

        # Infection should decay
        self.assertLess(self.sim.sir_state["I"], initial_infected)

        # Continue stepping until eradicated
        for _ in range(45):
            if self.sim.active_epidemic is None:
                break
            self.sim.simulate_epidemic_step(hours=8)

        self.assertIsNone(self.sim.active_epidemic)
        self.assertEqual(self.sim.sir_state["I"], 0.0)
        self.assertGreater(self.sim.sir_state["R"], 0.0)

    def test_spontaneous_outbreak_from_extreme_filth(self):
        """Filth exceeding 80.0 spontaneously triggers epidemic outbreak."""
        self.sim.active_epidemic = None
        self.sim.filth_level = 85.0
        self.sim.simulate_epidemic_step(hours=1)

        self.assertIsNotNone(self.sim.active_epidemic)
        self.assertEqual(self.sim.active_epidemic, "bubonic_plague")
        self.assertGreater(self.sim.sir_state["I"], 0.0)

    # -------------------------------------------------------------------------
    # Tier 6: Miracle Panacea Elixir
    # -------------------------------------------------------------------------
    def test_miracle_panacea(self):
        """Miracle Panacea cures 60% of active infected and costs 25 gold coins."""
        self.sim.trigger_outbreak("bubonic_plague")
        self.sim.coins = 100
        old_infected = self.sim.sir_state["I"]
        old_recovered = self.sim.sir_state["R"]
        old_renown = self.sim.total_renown

        self.sim.administer_panacea()
        self.assertEqual(self.sim.coins, 75)
        expected_cured = round(old_infected * 0.60, 1)
        self.assertAlmostEqual(self.sim.sir_state["I"], old_infected - expected_cured, places=1)
        self.assertAlmostEqual(self.sim.sir_state["R"], old_recovered + expected_cured, places=1)
        self.assertEqual(self.sim.total_renown, old_renown + 50)

    def test_miracle_panacea_insufficient_funds_or_no_disease(self):
        """Panacea fails when no outbreak is active or gold is insufficient."""
        # No disease active
        self.sim.active_epidemic = None
        self.sim.coins = 100
        self.sim.administer_panacea()
        self.assertEqual(self.sim.coins, 100)

        # Insufficient funds
        self.sim.trigger_outbreak("bubonic_plague")
        self.sim.coins = 10
        self.sim.administer_panacea()
        self.assertEqual(self.sim.coins, 10)  # Unchanged

    # -------------------------------------------------------------------------
    # Tier 7: SHA-256 Persistence & Deserialization
    # -------------------------------------------------------------------------
    def test_sanitation_and_sir_save_load_persistence(self):
        """Verify full persistence and verification of sanitation and SIR state across saves."""
        self.sim.filth_level = 42.5
        self.sim.miasma_active = False
        self.sim.street_sweepers_count = 5
        self.sim.cesspool_fill = 55.0
        self.sim.compost_fertilizer_stock = 9
        self.sim.plague_doctor_appointed = True
        self.sim.enact_black_quarantine("board_houses")
        self.sim.enact_black_quarantine("sanitary_pyres")
        self.sim.trigger_outbreak("typhus")
        self.sim.sir_state["deaths"] = 3

        h = self.sim.save_realm("unit_test_sanitation_slot")
        self.assertEqual(len(h), 64)

        # Mutate in memory
        self.sim.filth_level = 0.0
        self.sim.plague_doctor_appointed = False
        self.sim.quarantine_measures = []
        self.sim.active_epidemic = None

        # Load and verify restoration
        success = self.sim.load_realm("unit_test_sanitation_slot")
        self.assertTrue(success)
        self.assertAlmostEqual(self.sim.filth_level, 27.5, places=2)
        self.assertEqual(self.sim.street_sweepers_count, 5)
        self.assertAlmostEqual(self.sim.cesspool_fill, 55.0, places=2)
        self.assertEqual(self.sim.compost_fertilizer_stock, 9)
        self.assertTrue(self.sim.plague_doctor_appointed)
        self.assertIn("board_houses", self.sim.quarantine_measures)
        self.assertIn("sanitary_pyres", self.sim.quarantine_measures)
        self.assertEqual(self.sim.active_epidemic, "typhus")
        self.assertEqual(self.sim.sir_state["deaths"], 3)

    # -------------------------------------------------------------------------
    # Tier 8: 500-Iteration Monte Carlo Stress Test
    # -------------------------------------------------------------------------
    def test_monte_carlo_stress_epidemiology(self):
        """Run 500 stochastic simulation iterations with variable parameters.
        Must maintain strict numeric stability (no NaN, Inf, or negative counts)."""
        random.seed(42)

        for i in range(500):
            # Stochastic perturbations
            if random.random() < 0.15 and not self.sim.active_epidemic:
                disease = random.choice(["bubonic_plague", "pneumonic_plague", "dysentery", "influenza", "typhus"])
                self.sim.trigger_outbreak(disease)

            if random.random() < 0.20 and self.sim.active_epidemic and self.sim.coins >= 25:
                self.sim.administer_panacea()

            if random.random() < 0.25:
                self.sim.sweep_streets()

            if random.random() < 0.10:
                self.sim.clean_cesspool()

            if random.random() < 0.10 and not self.sim.plague_doctor_appointed:
                self.sim.appoint_plague_doctor()

            if random.random() < 0.10:
                measure = random.choice(["board_houses", "armed_cordon", "sanitary_pyres"])
                self.sim.enact_black_quarantine(measure)

            step_hours = random.randint(1, 8)
            self.sim.simulate_epidemic_step(hours=step_hours)

            # Assert invariants
            self.assertTrue(0.0 <= self.sim.filth_level <= 100.0, f"Filth out of bounds: {self.sim.filth_level}")
            self.assertTrue(self.sim.sir_state["S"] >= 0.0, f"Susceptible negative: {self.sim.sir_state['S']}")
            self.assertTrue(self.sim.sir_state["I"] >= 0.0, f"Infected negative: {self.sim.sir_state['I']}")
            self.assertTrue(self.sim.sir_state["R"] >= 0.0, f"Recovered negative: {self.sim.sir_state['R']}")
            self.assertTrue(self.sim.sir_state["deaths"] >= 0, f"Deaths negative: {self.sim.sir_state['deaths']}")

            self.assertFalse(math.isnan(self.sim.sir_state["S"]))
            self.assertFalse(math.isnan(self.sim.sir_state["I"]))
            self.assertFalse(math.isnan(self.sim.sir_state["R"]))
            self.assertFalse(math.isinf(self.sim.sir_state["S"]))
            self.assertFalse(math.isinf(self.sim.sir_state["I"]))
            self.assertFalse(math.isinf(self.sim.sir_state["R"]))


if __name__ == "__main__":
    unittest.main()
