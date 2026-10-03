# tests/test_feudal_justice_and_court.py
# Voxel Lord: Feudal Realm - Automated Test Suite for Feudal Justice, Leet Courts & Crime Dynamics
# Milestone 55: High Magistrate Court, Crown Authority Clamping, Verdict Dynamics, and Monte Carlo Stress.

import unittest
import math
import random
import copy


class FeudalCourtOracle:
    """Accurate Python reference oracle matching Feudal Manor Leet Court specifications."""

    def __init__(self, initial_prestige: float = 110.0, initial_morale: float = 85.0):
        self.prestige = initial_prestige
        self.morale = initial_morale
        self.crime_rate = 15.0 # [0.0, 100.0]
        self.unrest = 10.0 # [0.0, 100.0]
        self.public_order = 80.0 # [0.0, 100.0]
        self.treasury = 500 # Gold Coins
        self.piety = 50.0 # Monastic Piety
        self.crown_authority = 0.0 # Calculated
        self.active_dockets = []
        self.verdict_history = []
        self.ratified_charters = []
        self.calculate_crown_authority()

    def calculate_crown_authority(self) -> float:
        """
        MASTER_GDD Section 5.2 equation:
        A_crown = clamp(50.0 + 0.05 * Prestige + 0.20 * Morale - 0.25 * Crime - 0.30 * Unrest, 0.0, 100.0)
        """
        base = 50.0
        prestige_bonus = 0.05 * self.prestige
        morale_bonus = 0.20 * self.morale
        crime_penalty = 0.25 * self.crime_rate
        unrest_penalty = 0.30 * self.unrest
        raw = base + prestige_bonus + morale_bonus - crime_penalty - unrest_penalty
        self.crown_authority = max(0.0, min(100.0, round(raw, 2)))
        return self.crown_authority

    def add_docket(self, case_id: str, accused: str, charge: str, severity: int = 1, guilt_prob: float = 0.8) -> None:
        self.active_dockets.append({
            "id": case_id,
            "accused": accused,
            "charge": charge,
            "severity": max(1, min(4, severity)),
            "guilt_prob": max(0.0, min(1.0, guilt_prob)),
            "status": "Pending"
        })

    def deliver_verdict(self, case_id: str, verdict: str) -> bool:
        matched = [c for c in self.active_dockets if c["id"] == case_id]
        if not matched:
            return False
        case = matched[0]
        self.active_dockets.remove(case)
        v = verdict.lower()

        if v == "acquit":
            self.unrest = max(0.0, self.unrest - 3.0)
            if case["guilt_prob"] > 0.8:
                self.crime_rate = min(100.0, self.crime_rate + 2.5)
            self.morale = min(100.0, self.morale + 3.0)
        elif v == "pillory":
            self.crime_rate = max(0.0, self.crime_rate - 4.5)
            self.public_order = min(100.0, self.public_order + 5.0)
            self.unrest = max(0.0, self.unrest - 2.0)
        elif v == "fine":
            fine = case["severity"] * 25
            self.treasury += fine
            self.crime_rate = max(0.0, self.crime_rate - 3.0)
            self.public_order = min(100.0, self.public_order + 3.0)
        elif v == "ordeal":
            self.public_order = min(100.0, self.public_order + 6.0)
            self.unrest = max(0.0, self.unrest - 4.0)
            self.piety = min(100.0, self.piety + 15.0)
        elif v == "gallows":
            self.crime_rate = max(0.0, self.crime_rate - 8.0)
            self.public_order = min(100.0, self.public_order + 8.0)
            self.unrest = max(0.0, self.unrest - 5.0)
            self.morale = max(0.0, self.morale - 4.0)
        else:
            return False

        self.verdict_history.append({
            "id": case["id"],
            "verdict": v,
            "severity": case["severity"]
        })
        self.calculate_crown_authority()
        return True

    def ratify_charter(self, charter_key: str) -> bool:
        costs = {"magna": 60, "leet": 40, "assize": 30, "sanctuary": 25}
        if charter_key not in costs or charter_key in self.ratified_charters:
            return False
        cost = costs[charter_key]
        if self.treasury < cost:
            return False
        self.treasury -= cost
        self.ratified_charters.append(charter_key)

        if charter_key == "magna":
            self.public_order = min(100.0, self.public_order + 10.0)
            self.unrest = max(0.0, self.unrest - 5.0)
        elif charter_key == "leet":
            self.crime_rate = max(0.0, self.crime_rate - 8.0)
        elif charter_key == "assize":
            self.public_order = min(100.0, self.public_order + 10.0)
            self.crime_rate = max(0.0, self.crime_rate - 5.0)
        elif charter_key == "sanctuary":
            self.unrest = max(0.0, self.unrest - 10.0)
            self.piety = min(100.0, self.piety + 15.0)

        self.calculate_crown_authority()
        return True

    def process_patrol_tick(self) -> None:
        self.crime_rate = max(1.0, self.crime_rate - 3.5)
        self.public_order = min(100.0, self.public_order + 3.0)
        self.calculate_crown_authority()


class TestCrownAuthorityFormulaAndBounds(unittest.TestCase):
    """Tier 1: Verify Crown Authority mathematical limits and clamping."""

    def test_standard_crown_authority(self):
        court = FeudalCourtOracle(initial_prestige=100.0, initial_morale=80.0)
        court.crime_rate = 10.0
        court.unrest = 10.0
        # base: 50.0 + 5.0 (0.05*100) + 16.0 (0.20*80) - 2.5 (0.25*10) - 3.0 (0.30*10) = 65.5
        auth = court.calculate_crown_authority()
        self.assertAlmostEqual(auth, 65.5, delta=0.1)

    def test_upper_clamp_bound(self):
        """Under extreme prestige and ecstatic morale with 0 crime, authority never exceeds 100.0."""
        court = FeudalCourtOracle(initial_prestige=2000.0, initial_morale=100.0)
        court.crime_rate = 0.0
        court.unrest = 0.0
        auth = court.calculate_crown_authority()
        self.assertEqual(auth, 100.0)

    def test_lower_clamp_bound(self):
        """Under catastrophic crime and rebellion, authority never drops below 0.0."""
        court = FeudalCourtOracle(initial_prestige=0.0, initial_morale=0.0)
        court.crime_rate = 100.0
        court.unrest = 100.0
        auth = court.calculate_crown_authority()
        self.assertEqual(auth, 0.0)


class TestJudicialVerdicts(unittest.TestCase):
    """Tier 2: Testing court docket verdicts and systemic reactions."""

    def setUp(self):
        self.court = FeudalCourtOracle(initial_prestige=120.0, initial_morale=80.0)
        self.court.add_docket("CASE-001", "Robin of Locksley", "Hunting royal deer", severity=2, guilt_prob=0.95)
        self.court.add_docket("CASE-002", "Thomas the Coiner", "Clipping silver coin edges", severity=3, guilt_prob=0.90)
        self.court.add_docket("CASE-003", "Walter the Weaver", "Falsely accused of theft", severity=1, guilt_prob=0.20)
        self.court.add_docket("CASE-004", "Sir Geoffrey", "Feudal treason against the crown", severity=4, guilt_prob=0.99)

    def test_verdict_pillory(self):
        initial_crime = self.court.crime_rate
        initial_order = self.court.public_order
        success = self.court.deliver_verdict("CASE-001", "pillory")
        self.assertTrue(success)
        self.assertLess(self.court.crime_rate, initial_crime)
        self.assertGreater(self.court.public_order, initial_order)

    def test_verdict_fine(self):
        initial_treasury = self.court.treasury
        success = self.court.deliver_verdict("CASE-002", "fine")
        self.assertTrue(success)
        # Severity 3 * 25 = 75 gold
        self.assertEqual(self.court.treasury, initial_treasury + 75)

    def test_verdict_acquittal(self):
        initial_morale = self.court.morale
        success = self.court.deliver_verdict("CASE-003", "acquit")
        self.assertTrue(success)
        self.assertGreater(self.court.morale, initial_morale)

    def test_verdict_gallows_execution(self):
        initial_crime = self.court.crime_rate
        initial_order = self.court.public_order
        success = self.court.deliver_verdict("CASE-004", "gallows")
        self.assertTrue(success)
        self.assertEqual(self.court.crime_rate, max(0.0, initial_crime - 8.0))
        self.assertEqual(self.court.public_order, initial_order + 8.0)

    def test_invalid_docket_handling(self):
        success = self.court.deliver_verdict("CASE-999", "gallows")
        self.assertFalse(success)

    def test_invalid_verdict_handling(self):
        success = self.court.deliver_verdict("CASE-001", "banish_to_moon")
        self.assertFalse(success)


class TestFeudalChartersAndAssizes(unittest.TestCase):
    """Tier 3: Testing royal charters, assizes, and institutional law."""

    def setUp(self):
        self.court = FeudalCourtOracle(initial_prestige=150.0, initial_morale=85.0)

    def test_ratify_manor_leet_charter(self):
        initial_crime = self.court.crime_rate
        initial_treasury = self.court.treasury
        success = self.court.ratify_charter("leet")
        self.assertTrue(success)
        self.assertEqual(self.court.treasury, initial_treasury - 40)
        self.assertEqual(self.court.crime_rate, initial_crime - 8.0)
        self.assertIn("leet", self.court.ratified_charters)

    def test_duplicate_charter_prevention(self):
        self.court.ratify_charter("assize")
        success = self.court.ratify_charter("assize")
        self.assertFalse(success)

    def test_insufficient_funds_for_charter(self):
        self.court.treasury = 10 # Cannot afford 60 Gold Magna Carta
        success = self.court.ratify_charter("magna")
        self.assertFalse(success)
        self.assertNotIn("magna", self.court.ratified_charters)


class TestBailiffPatrolsAndCrimeKinetics(unittest.TestCase):
    """Tier 4: Testing law enforcement patrols and crime suppression."""

    def test_patrol_tick_suppresses_crime(self):
        court = FeudalCourtOracle()
        court.crime_rate = 25.0
        court.public_order = 70.0
        court.process_patrol_tick()
        self.assertEqual(court.crime_rate, 21.5)
        self.assertEqual(court.public_order, 73.0)


class TestJudicialMonteCarloStress(unittest.TestCase):
    """Tier 5: 500-case randomized Monte Carlo stress simulation."""

    def test_monte_carlo_court_simulation(self):
        court = FeudalCourtOracle()
        verdicts = ["acquit", "pillory", "fine", "ordeal", "gallows"]

        for i in range(500):
            # Spawn random case
            sev = random.randint(1, 4)
            guilt = random.uniform(0.1, 0.99)
            court.add_docket(f"CASE-{i}", f"Defendant_{i}", "Random felony", severity=sev, guilt_prob=guilt)

            # Deliver random verdict
            chosen_v = random.choice(verdicts)
            success = court.deliver_verdict(f"CASE-{i}", chosen_v)
            self.assertTrue(success)

            # Occasional patrol or charter attempt
            if i % 25 == 0:
                court.process_patrol_tick()
            if i % 100 == 0:
                court.treasury += 200

            # Assert absolute invariants
            auth = court.calculate_crown_authority()
            self.assertTrue(0.0 <= auth <= 100.0, f"Crown Authority {auth} out of bounds at step {i}")
            self.assertTrue(0.0 <= court.crime_rate <= 100.0)
            self.assertTrue(0.0 <= court.unrest <= 100.0)
            self.assertTrue(0.0 <= court.public_order <= 100.0)
            self.assertFalse(math.isnan(auth))
            self.assertFalse(math.isinf(auth))

        self.assertEqual(len(court.verdict_history), 500)


if __name__ == "__main__":
    unittest.main()
