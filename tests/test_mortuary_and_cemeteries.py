"""
Unit tests for Milestone 58: Gravedigger Mortuary Logistics, Corpse Decomposition Dynamics,
Consecrated Memorial Cemeteries & Procedural Epitaph Engine.
Corresponds to MASTER_GDD.md Sections 93, 94, 95, and 96.
"""

import unittest
import math
import random
from tools.interactive_play_simulator import VoxelRealmSimulator


class TestMortuaryAndCemeteries(unittest.TestCase):

    def setUp(self):
        self.sim = VoxelRealmSimulator()

    # -------------------------------------------------------------------------
    # Tier 1: 4-Stage Corpse Decomposition Kinetics & Boundary Checks
    # -------------------------------------------------------------------------
    def test_decomposition_stages_and_morale_penalties(self):
        """Verify 48-hour 4-stage timeline: fresh, putrefaction, liquefaction, skeleton."""
        # 0 - 6h: Fresh Corpse (-15 Morale)
        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(0.0)
        self.assertEqual(stage_k, "fresh")
        self.assertEqual(pen, -15.0)

        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(5.9)
        self.assertEqual(stage_k, "fresh")

        # 6 - 24h: Putrefaction & Bloating (-30 Morale)
        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(6.0)
        self.assertEqual(stage_k, "putrefaction")
        self.assertEqual(pen, -30.0)

        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(23.9)
        self.assertEqual(stage_k, "putrefaction")

        # 24 - 48h: Active Liquefaction (-45 Morale)
        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(24.0)
        self.assertEqual(stage_k, "liquefaction")
        self.assertEqual(pen, -45.0)

        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(47.9)
        self.assertEqual(stage_k, "liquefaction")

        # 48h+: Contaminated Skeleton (-60 Morale)
        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(48.0)
        self.assertEqual(stage_k, "skeleton")
        self.assertEqual(pen, -60.0)

        stage_k, pen, desc = self.sim.get_corpse_decomposition_stage(150.0)
        self.assertEqual(stage_k, "skeleton")

    # -------------------------------------------------------------------------
    # Tier 2: Scavenger Dynamics & Environmental Hazards
    # -------------------------------------------------------------------------
    def test_scavengers_circling_crows_and_wolf_threat(self):
        """Circling crows appear at 6h; wild wolf pack prowls at 24h unburied."""
        self.sim.register_deceased_citizen("Osric the Tanner", 42, "Tanner", "Cold", "Supplied leather armor", 20, False)
        self.assertEqual(len(self.sim.unburied_corpses), 1)

        # Step 2 hours -> Fresh stage, no scavengers
        self.sim.simulate_decomposition_step(hours=2)
        self.assertEqual(self.sim.scavengers_active["circling_crows"], 0)
        self.assertFalse(self.sim.scavengers_active["wolf_pack_threat"])

        # Step 5 more hours (total 7h) -> Putrefaction, crows should gather
        self.sim.simulate_decomposition_step(hours=5)
        self.assertGreater(self.sim.scavengers_active["circling_crows"], 0)
        self.assertFalse(self.sim.scavengers_active["wolf_pack_threat"])

        # Step 18 more hours (total 25h) -> Liquefaction, wolf pack threat triggered
        self.sim.simulate_decomposition_step(hours=18)
        self.assertTrue(self.sim.scavengers_active["wolf_pack_threat"])

        # Once corpse is collected and buried, scavengers disperse
        cid = self.sim.unburied_corpses[0]["id"]
        self.sim.collect_and_bury_corpse(cid, "wooden_coffin")
        self.assertEqual(len(self.sim.unburied_corpses), 0)
        self.assertEqual(self.sim.scavengers_active["circling_crows"], 0)
        self.assertFalse(self.sim.scavengers_active["wolf_pack_threat"])

    # -------------------------------------------------------------------------
    # Tier 3: Gravedigger Appointment & Undertaker Role
    # -------------------------------------------------------------------------
    def test_appoint_gravedigger(self):
        """Appointing Brother Barnaby activates undertaker logistics."""
        self.assertFalse(self.sim.gravedigger_appointed)
        old_renown = self.sim.total_renown

        self.sim.appoint_gravedigger()
        self.assertTrue(self.sim.gravedigger_appointed)
        self.assertEqual(self.sim.total_renown, old_renown + 50)

    # -------------------------------------------------------------------------
    # Tier 4: Casket Crafting & Workshop Recipes
    # -------------------------------------------------------------------------
    def test_coffin_crafting_recipes(self):
        """Crafting caskets consumes gold and populates inventory."""
        self.sim.coins = 200
        old_shrouds = self.sim.coffin_inventory["linen_shroud"]
        old_coffins = self.sim.coffin_inventory["wooden_coffin"]
        old_sarcophagi = self.sim.coffin_inventory["stone_sarcophagus"]

        # Craft Shroud (cost 10)
        success = self.sim.craft_coffin("linen_shroud")
        self.assertTrue(success)
        self.assertEqual(self.sim.coins, 190)
        self.assertEqual(self.sim.coffin_inventory["linen_shroud"], old_shrouds + 1)

        # Craft Wooden Coffin (cost 20)
        success = self.sim.craft_coffin("wooden_coffin")
        self.assertTrue(success)
        self.assertEqual(self.sim.coins, 170)
        self.assertEqual(self.sim.coffin_inventory["wooden_coffin"], old_coffins + 1)

        # Craft Stone Sarcophagus (cost 45)
        success = self.sim.craft_coffin("stone_sarcophagus")
        self.assertTrue(success)
        self.assertEqual(self.sim.coins, 125)
        self.assertEqual(self.sim.coffin_inventory["stone_sarcophagus"], old_sarcophagi + 1)

        # Invalid type
        self.assertFalse(self.sim.craft_coffin("golden_pyramid"))

        # Insufficient coins
        self.sim.coins = 5
        self.assertFalse(self.sim.craft_coffin("wooden_coffin"))
        self.assertEqual(self.sim.coins, 5)

    # -------------------------------------------------------------------------
    # Tier 5: Burial Logistics & Crown Escheat Law
    # -------------------------------------------------------------------------
    def test_burial_and_escheat_law(self):
        """Unclaimed estates revert to Crown Treasury under Escheat Law."""
        self.sim.coins = 100
        # Register deceased without heirs
        self.sim.register_deceased_citizen("Cedric the Hermit", 55, "Herbalist", "Old Age", "Discovered rare mountain herbs", 40, has_heirs=False)
        corpse = self.sim.unburied_corpses[-1]
        cid = corpse["id"]

        old_occupied = self.sim.cemetery["occupied_plots"]
        buried = self.sim.collect_and_bury_corpse(cid, "wooden_coffin")
        self.assertTrue(buried)
        self.assertEqual(len(self.sim.unburied_corpses), 0)
        self.assertEqual(self.sim.cemetery["occupied_plots"], old_occupied + 1)
        # Escheat Law check: 40 gold added to Crown Treasury
        self.assertEqual(self.sim.coins, 140)
        self.assertEqual(self.sim.escheat_treasury_collected, 40)

    def test_burial_with_heirs(self):
        """Estates with heirs are passed to family, not added to Crown Treasury."""
        self.sim.coins = 100
        self.sim.register_deceased_citizen("Rowan the Mason", 38, "Stonemason", "Raid", "Built South Wall", 50, has_heirs=True)
        cid = self.sim.unburied_corpses[-1]["id"]

        buried = self.sim.collect_and_bury_corpse(cid, "stone_sarcophagus")
        self.assertTrue(buried)
        # Coins remain 100
        self.assertEqual(self.sim.coins, 100)
        self.assertEqual(self.sim.escheat_treasury_collected, 0)

    def test_burial_when_cemetery_full(self):
        """Full cemetery rejects new burials until expanded."""
        self.sim.cemetery["total_plots"] = 10
        self.sim.cemetery["occupied_plots"] = 10
        self.sim.register_deceased_citizen("Gareth", 25, "Peasant", "Accident", "Farmed barley", 10, True)
        cid = self.sim.unburied_corpses[-1]["id"]

        buried = self.sim.collect_and_bury_corpse(cid, "linen_shroud")
        self.assertFalse(buried)
        self.assertEqual(len(self.sim.unburied_corpses), 1)

    # -------------------------------------------------------------------------
    # Tier 6: Consecration & Anti-Necromancy Protection
    # -------------------------------------------------------------------------
    def test_priest_sanctification(self):
        """Priest consecrates graveyard ground with Holy Water and litanies."""
        self.sim.cemetery["consecrated_by_priest"] = False
        self.sim.cemetery["serenity_aura_active"] = False

        success = self.sim.sanctify_cemetery_ground()
        self.assertTrue(success)
        self.assertTrue(self.sim.cemetery["consecrated_by_priest"])
        self.assertTrue(self.sim.cemetery["serenity_aura_active"])
        for g in self.sim.cemetery["graves"]:
            self.assertTrue(g["sanctified"])

    # -------------------------------------------------------------------------
    # Tier 7: Procedural 4-Line Epitaph Engine
    # -------------------------------------------------------------------------
    def test_procedural_epitaph_generation(self):
        """Verify 4-line procedural epitaph contains historical record and eulogy."""
        epitaph = self.sim.generate_procedural_epitaph(
            name="Sir Gerald the Bold",
            age=52,
            profession="Knight Hospitaller",
            achievement="Slew 14 marauding bandits during the Siege of Ashfell",
            cause="Fell honorably in battle defending the Citadel drawbridge",
            headstone="stone_sarcophagus"
        )
        self.assertIn("Regal Marble Sarcophagus", epitaph)
        self.assertIn("Sir Gerald the Bold (Age 52)", epitaph)
        self.assertIn("Knight Hospitaller", epitaph)
        self.assertIn("Slew 14 marauding bandits", epitaph)
        self.assertIn("Fell honorably in battle", epitaph)
        self.assertIn("saltanatimiz bunyodkori", epitaph)

    # -------------------------------------------------------------------------
    # Tier 8: SHA-256 Persistence & 500-Iteration Monte Carlo Stress Test
    # -------------------------------------------------------------------------
    def test_mortuary_save_load_persistence(self):
        """State persistence preserves unburied corpses, caskets, and cemetery graves."""
        self.sim.appoint_gravedigger()
        self.sim.coffin_inventory["wooden_coffin"] = 5
        self.sim.register_deceased_citizen("Pippin", 19, "Apprentice Baker", "Fever", "Baked harvest loaves", 12, False)
        self.sim.simulate_decomposition_step(10)
        self.sim.escheat_treasury_collected = 75

        h = self.sim.save_realm("unit_test_mortuary_slot")
        self.assertEqual(len(h), 64)

        # Mutate in memory
        self.sim.gravedigger_appointed = False
        self.sim.unburied_corpses = []
        self.sim.coffin_inventory["wooden_coffin"] = 0
        self.sim.escheat_treasury_collected = 0

        # Load and verify
        success = self.sim.load_realm("unit_test_mortuary_slot")
        self.assertTrue(success)
        self.assertTrue(self.sim.gravedigger_appointed)
        self.assertEqual(self.sim.coffin_inventory["wooden_coffin"], 5)
        self.assertEqual(len(self.sim.unburied_corpses), 1)
        self.assertEqual(self.sim.unburied_corpses[0]["citizen_name"], "Pippin")
        self.assertEqual(self.sim.unburied_corpses[0]["stage"], "putrefaction")
        self.assertEqual(self.sim.escheat_treasury_collected, 75)

    def test_monte_carlo_mortuary_stress(self):
        """500-iteration stochastic stress test verifying non-negative bounds and numerical stability."""
        random.seed(42)

        for i in range(500):
            # Stochastic deaths
            if random.random() < 0.25:
                name = f"Citizen #{i}"
                age = random.randint(15, 80)
                prof = random.choice(["Farmer", "Smith", "Guard", "Baker", "Weaver"])
                cause = random.choice(["Plague", "Old Age", "Hypothermia", "Workplace Fall"])
                heirs = random.choice([True, False])
                gold = random.randint(0, 50)
                self.sim.register_deceased_citizen(name, age, prof, cause, "Served faithfully", gold, heirs)

            # Craft coffins
            if random.random() < 0.20 and self.sim.coins >= 30:
                c_type = random.choice(["linen_shroud", "wooden_coffin", "stone_sarcophagus"])
                self.sim.craft_coffin(c_type)

            # Burials
            if self.sim.unburied_corpses and random.random() < 0.35:
                corpse = self.sim.unburied_corpses[0]
                c_type = random.choice(["linen_shroud", "wooden_coffin", "stone_sarcophagus"])
                self.sim.collect_and_bury_corpse(corpse["id"], c_type)

            # Sanctification
            if random.random() < 0.05:
                self.sim.sanctify_cemetery_ground()

            # Time step
            hrs = random.randint(1, 12)
            self.sim.simulate_decomposition_step(hours=hrs)

            # Verify invariants
            self.assertTrue(0 <= self.sim.cemetery["occupied_plots"] <= self.sim.cemetery["total_plots"])
            self.assertTrue(0.0 <= self.sim.filth_level <= 100.0)
            self.assertTrue(self.sim.coins >= 0)
            self.assertTrue(self.sim.escheat_treasury_collected >= 0)
            for c in self.sim.unburied_corpses:
                self.assertTrue(c["hours_unburied"] >= 0.0)
                self.assertIn(c["stage"], ["fresh", "putrefaction", "liquefaction", "skeleton"])


if __name__ == "__main__":
    unittest.main()
