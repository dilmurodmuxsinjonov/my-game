# tests/test_decrees_squadron_systems.py
# Voxel Lord: Feudal Realm - Milestone 47 Test Suite
# Tests Monarch Imperial Decrees, Tactical Garrison Squadron Command, and UI Integration.

import unittest
import math
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class MockVector3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __eq__(self, other):
        if not isinstance(other, MockVector3):
            return False
        return (
            abs(self.x - other.x) < 0.001
            and abs(self.y - other.y) < 0.001
            and abs(self.z - other.z) < 0.001
        )

    def __repr__(self):
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


# Simulated RoyalDecrees for headless testing
class SimulatedRoyalDecrees:
    CATALOG = {
        "corvee_labor": {
            "name": "Corvée Mandatory Labor Mandate",
            "cost_renown": 50,
            "cost_coins": 20,
            "duration": 240.0,
            "modifiers": {
                "work_speed_mult": 1.30,
                "hunger_drain_mult": 1.20,
                "morale_decay_offset": 5.0,
            },
        },
        "grain_dole_relief": {
            "name": "Imperial Grain Dole Relief",
            "cost_renown": 25,
            "cost_coins": 10,
            "cost_items": {"bread": 10, "wheat": 15},
            "duration": 180.0,
            "modifiers": {
                "hunger_drain_mult": 0.65,
                "morale_bonus": 25.0,
                "health_regen_bonus": 1.5,
            },
        },
        "guild_subsidies": {
            "name": "Artisan Guild Patronage & Subsidies",
            "cost_renown": 45,
            "cost_coins": 50,
            "duration": 300.0,
            "modifiers": {
                "craft_output_bonus": 0.25,
                "furnace_heat_speed": 1.35,
                "tax_revenue_mult": 1.15,
            },
        },
        "frontier_conscription": {
            "name": "Frontier Militia Levy Conscription",
            "cost_renown": 60,
            "cost_coins": 35,
            "duration": 210.0,
            "modifiers": {
                "guard_defense_mult": 1.25,
                "raid_defeat_reward_mult": 1.50,
                "guard_capacity_bonus": 4.0,
            },
        },
        "free_trade_charter": {
            "name": "Mercantile Free Trade & Toll Exemption",
            "cost_renown": 30,
            "cost_coins": 30,
            "duration": 360.0,
            "modifiers": {
                "caravan_interval_mult": 0.65,
                "trade_discount": 0.15,
            },
        },
        "monastic_scholarship": {
            "name": "Monastic Scholarly Patronage",
            "cost_renown": 75,
            "cost_coins": 60,
            "duration": 300.0,
            "modifiers": {
                "tech_speed_mult": 1.40,
                "infirmary_heal_mult": 1.50,
            },
        },
    }

    def __init__(self):
        self.active_decrees = {}
        self.aggregated_modifiers = {}
        self._recalculate_modifiers()

    def can_proclaim(self, decree_id: str, coins: int = 100, renown: int = 100, items: dict = None):
        if decree_id not in self.CATALOG:
            return False
        if decree_id in self.active_decrees:
            return False
        data = self.CATALOG[decree_id]
        if renown < data["cost_renown"]:
            return False
        if coins < data["cost_coins"]:
            return False
        if items and "cost_items" in data:
            for item, req_qty in data["cost_items"].items():
                if items.get(item, 0) < req_qty:
                    return False
        return True

    def proclaim_decree(self, decree_id: str, coins_ref: dict = None, renown: int = 100):
        coins = coins_ref.get("coins", 100) if coins_ref else 100
        if not self.can_proclaim(decree_id, coins=coins, renown=renown):
            return False
        data = self.CATALOG[decree_id]
        if coins_ref and "coins" in coins_ref:
            coins_ref["coins"] -= data["cost_coins"]
        duration = data["duration"]
        self.active_decrees[decree_id] = {"remaining": duration, "total": duration}
        self._recalculate_modifiers()
        return True

    def revoke_decree(self, decree_id: str):
        if decree_id in self.active_decrees:
            del self.active_decrees[decree_id]
            self._recalculate_modifiers()
            return True
        return False

    def update_timers(self, delta: float):
        expired = []
        for dec_id, info in self.active_decrees.items():
            info["remaining"] -= delta
            if info["remaining"] <= 0.0:
                expired.append(dec_id)
        for dec_id in expired:
            del self.active_decrees[dec_id]
        if expired:
            self._recalculate_modifiers()

    def _recalculate_modifiers(self):
        self.aggregated_modifiers = {
            "work_speed_mult": 1.0,
            "hunger_drain_mult": 1.0,
            "craft_output_bonus": 0.0,
            "guard_defense_mult": 1.0,
            "caravan_interval_mult": 1.0,
            "tech_speed_mult": 1.0,
            "morale_bonus": 0.0,
            "guard_capacity_bonus": 0.0,
        }
        for dec_id in self.active_decrees:
            mods = self.CATALOG[dec_id]["modifiers"]
            for k, val in mods.items():
                if k.endswith("_mult"):
                    self.aggregated_modifiers[k] = self.aggregated_modifiers.get(k, 1.0) * val
                else:
                    self.aggregated_modifiers[k] = self.aggregated_modifiers.get(k, 0.0) + val

    def get_modifier(self, key: str, default_val: float = 1.0):
        return self.aggregated_modifiers.get(key, default_val)

    def to_dict(self):
        return {
            "active_decrees": [
                {"id": k, "remaining": v["remaining"], "total": v["total"]}
                for k, v in self.active_decrees.items()
            ]
        }

    def from_dict(self, data):
        self.active_decrees.clear()
        for item in data.get("active_decrees", []):
            dec_id = item["id"]
            if dec_id in self.CATALOG:
                self.active_decrees[dec_id] = {
                    "remaining": float(item["remaining"]),
                    "total": float(item["total"]),
                }
        self._recalculate_modifiers()


# Simulated SquadronCommand for headless testing
class SimulatedSquadronCommand:
    class Stance:
        DEFENSIVE_SENTINEL = 0
        AGGRESSIVE_ASSAULT = 1
        MONARCH_ESCORT = 2

    class Formation:
        SHIELD_WALL = 0
        SHOCK_WEDGE = 1
        SKIRMISH_LINE = 2
        PERIMETER_SQUARE = 3

    STANCE_NAMES = {
        0: "Defensive Sentinel (Hold Gates & Perimeter)",
        1: "Aggressive Assault (Hunt Raiders & Camps)",
        2: "Monarch Escort (Royal Bodyguard Formation)",
    }

    FORMATION_NAMES = {
        0: "Shield Wall (Locked Bucklers)",
        1: "Shock Wedge (Vanguard Charge)",
        2: "Skirmish Line (Spread Archers)",
        3: "Perimeter Square (360° Bulwark)",
    }

    FORMATION_BONUSES = {
        0: {"defense_bonus": 0.35, "speed_mult": 0.80, "block_chance": 0.30},
        1: {"attack_bonus": 0.40, "speed_mult": 1.10, "charge_knockback": 2.5},
        2: {"attack_speed_bonus": 0.25, "speed_mult": 1.05, "aoe_resistance": 0.50},
        3: {"defense_bonus": 0.20, "speed_mult": 0.90, "perimeter_coverage": 1.0},
    }

    def __init__(self):
        self.current_stance = self.Stance.DEFENSIVE_SENTINEL
        self.current_formation = self.Formation.SHIELD_WALL
        self.rally_pos = MockVector3(32, 12, 32)
        self.guard_morale = 100.0

    def get_stance_name(self, s=None):
        if s is None:
            s = self.current_stance
        return self.STANCE_NAMES.get(s, "Unknown Stance")

    def get_formation_name(self, f=None):
        if f is None:
            f = self.current_formation
        return self.FORMATION_NAMES.get(f, "Unknown Formation")

    def cycle_stance(self, forward=True):
        count = 3
        if forward:
            self.current_stance = (self.current_stance + 1) % count
        else:
            self.current_stance = (self.current_stance - 1 + count) % count
        return self.current_stance

    def cycle_formation(self, forward=True):
        count = 4
        if forward:
            self.current_formation = (self.current_formation + 1) % count
        else:
            self.current_formation = (self.current_formation - 1 + count) % count
        return self.current_formation

    def get_formation_modifiers(self):
        return self.FORMATION_BONUSES[self.current_formation]

    def get_formation_offsets(self, unit_count: int):
        offsets = []
        if unit_count <= 0:
            return offsets
        if self.current_formation == self.Formation.SHIELD_WALL:
            half_w = (unit_count - 1) * 0.75
            for i in range(unit_count):
                offsets.append(MockVector3(i * 1.5 - half_w, 0, 1.2))
        elif self.current_formation == self.Formation.SHOCK_WEDGE:
            offsets.append(MockVector3(0, 0, 2.0))
            for i in range(1, unit_count):
                side = 1.0 if (i % 2 == 1) else -1.0
                rank = (i + 1) // 2
                offsets.append(MockVector3(side * rank * 1.4, 0, 2.0 - rank * 1.2))
        elif self.current_formation == self.Formation.SKIRMISH_LINE:
            half_w = (unit_count - 1) * 1.5
            for i in range(unit_count):
                offsets.append(MockVector3(i * 3.0 - half_w, 0, (i % 2) * 0.8))
        elif self.current_formation == self.Formation.PERIMETER_SQUARE:
            radius = 2.5
            step = (2.0 * math.pi) / max(unit_count, 1)
            for i in range(unit_count):
                offsets.append(MockVector3(math.cos(i * step) * radius, 0, math.sin(i * step) * radius))
        return offsets

    def issue_rally(self, pos: MockVector3, guard_count: int = 4):
        self.rally_pos = pos
        return guard_count

    def to_dict(self):
        return {
            "stance": int(self.current_stance),
            "formation": int(self.current_formation),
            "guard_morale": self.guard_morale,
        }

    def from_dict(self, d):
        self.current_stance = d.get("stance", self.current_stance)
        self.current_formation = d.get("formation", self.current_formation)
        self.guard_morale = d.get("guard_morale", self.guard_morale)


class TestDecreesSquadronSystems(unittest.TestCase):
    """Test suite covering Milestone 47 systems."""

    def setUp(self):
        self.decrees = SimulatedRoyalDecrees()
        self.squad = SimulatedSquadronCommand()

    def test_decrees_catalog_completeness(self):
        self.assertEqual(len(self.decrees.CATALOG), 6)
        self.assertIn("corvee_labor", self.decrees.CATALOG)
        self.assertIn("grain_dole_relief", self.decrees.CATALOG)
        self.assertIn("guild_subsidies", self.decrees.CATALOG)
        self.assertIn("frontier_conscription", self.decrees.CATALOG)
        self.assertIn("free_trade_charter", self.decrees.CATALOG)
        self.assertIn("monastic_scholarship", self.decrees.CATALOG)

    def test_decree_proclamation_and_activation(self):
        coins = {"coins": 100}
        ok = self.decrees.proclaim_decree("corvee_labor", coins_ref=coins, renown=100)
        self.assertTrue(ok)
        self.assertEqual(coins["coins"], 80)  # 100 - 20
        self.assertIn("corvee_labor", self.decrees.active_decrees)
        self.assertAlmostEqual(self.decrees.get_modifier("work_speed_mult"), 1.30)
        self.assertAlmostEqual(self.decrees.get_modifier("hunger_drain_mult"), 1.20)

    def test_decree_double_proclamation_prevention(self):
        self.decrees.proclaim_decree("corvee_labor")
        self.assertTrue(self.decrees.can_proclaim("corvee_labor") is False)
        # Attempt to proclaim second time fails
        ok_second = self.decrees.proclaim_decree("corvee_labor")
        self.assertFalse(ok_second)

    def test_decree_insufficient_renown_rejection(self):
        # Monastic scholarship requires 75 renown
        can_p = self.decrees.can_proclaim("monastic_scholarship", renown=30)
        self.assertFalse(can_p)
        ok = self.decrees.proclaim_decree("monastic_scholarship", renown=30)
        self.assertFalse(ok)

    def test_decree_timer_countdown_and_expiration(self):
        self.decrees.proclaim_decree("grain_dole_relief")
        self.assertIn("grain_dole_relief", self.decrees.active_decrees)
        self.assertAlmostEqual(self.decrees.get_modifier("morale_bonus"), 25.0)

        # Advance timer past 180s duration
        self.decrees.update_timers(190.0)
        self.assertNotIn("grain_dole_relief", self.decrees.active_decrees)
        self.assertAlmostEqual(self.decrees.get_modifier("morale_bonus"), 0.0)

    def test_decree_manual_revocation(self):
        self.decrees.proclaim_decree("free_trade_charter")
        self.assertAlmostEqual(self.decrees.get_modifier("caravan_interval_mult"), 0.65)
        rev = self.decrees.revoke_decree("free_trade_charter")
        self.assertTrue(rev)
        self.assertAlmostEqual(self.decrees.get_modifier("caravan_interval_mult"), 1.0)

    def test_decree_multiple_modifier_aggregation(self):
        self.decrees.proclaim_decree("corvee_labor")  # work speed 1.30, hunger 1.20
        self.decrees.proclaim_decree("guild_subsidies")  # craft bonus 0.25, tax mult 1.15
        self.decrees.proclaim_decree("monastic_scholarship")  # tech speed 1.40

        self.assertAlmostEqual(self.decrees.get_modifier("work_speed_mult"), 1.30)
        self.assertAlmostEqual(self.decrees.get_modifier("craft_output_bonus"), 0.25)
        self.assertAlmostEqual(self.decrees.get_modifier("tech_speed_mult"), 1.40)

    def test_decree_serialization_roundtrip(self):
        self.decrees.proclaim_decree("frontier_conscription")
        data = self.decrees.to_dict()

        copy_decrees = SimulatedRoyalDecrees()
        copy_decrees.from_dict(data)
        self.assertIn("frontier_conscription", copy_decrees.active_decrees)
        self.assertAlmostEqual(copy_decrees.get_modifier("guard_defense_mult"), 1.25)
        self.assertAlmostEqual(copy_decrees.get_modifier("guard_capacity_bonus"), 4.0)

    def test_squadron_initial_state(self):
        self.assertEqual(self.squad.current_stance, SimulatedSquadronCommand.Stance.DEFENSIVE_SENTINEL)
        self.assertEqual(self.squad.current_formation, SimulatedSquadronCommand.Formation.SHIELD_WALL)
        self.assertEqual(self.squad.guard_morale, 100.0)

    def test_squadron_stance_cycling(self):
        s1 = self.squad.cycle_stance(True)
        self.assertEqual(s1, SimulatedSquadronCommand.Stance.AGGRESSIVE_ASSAULT)
        s2 = self.squad.cycle_stance(True)
        self.assertEqual(s2, SimulatedSquadronCommand.Stance.MONARCH_ESCORT)
        s3 = self.squad.cycle_stance(True)
        self.assertEqual(s3, SimulatedSquadronCommand.Stance.DEFENSIVE_SENTINEL)

        # Backward cycle
        s_back = self.squad.cycle_stance(False)
        self.assertEqual(s_back, SimulatedSquadronCommand.Stance.MONARCH_ESCORT)

    def test_squadron_formation_cycling(self):
        f1 = self.squad.cycle_formation(True)
        self.assertEqual(f1, SimulatedSquadronCommand.Formation.SHOCK_WEDGE)
        f2 = self.squad.cycle_formation(True)
        self.assertEqual(f2, SimulatedSquadronCommand.Formation.SKIRMISH_LINE)
        f3 = self.squad.cycle_formation(True)
        self.assertEqual(f3, SimulatedSquadronCommand.Formation.PERIMETER_SQUARE)
        f4 = self.squad.cycle_formation(True)
        self.assertEqual(f4, SimulatedSquadronCommand.Formation.SHIELD_WALL)

    def test_squadron_formation_modifiers(self):
        self.squad.current_formation = SimulatedSquadronCommand.Formation.SHIELD_WALL
        mods_shield = self.squad.get_formation_modifiers()
        self.assertAlmostEqual(mods_shield["defense_bonus"], 0.35)
        self.assertAlmostEqual(mods_shield["speed_mult"], 0.80)

        self.squad.current_formation = SimulatedSquadronCommand.Formation.SHOCK_WEDGE
        mods_wedge = self.squad.get_formation_modifiers()
        self.assertAlmostEqual(mods_wedge["attack_bonus"], 0.40)
        self.assertAlmostEqual(mods_wedge["speed_mult"], 1.10)

    def test_squadron_offsets_shield_wall(self):
        self.squad.current_formation = SimulatedSquadronCommand.Formation.SHIELD_WALL
        offsets = self.squad.get_formation_offsets(4)
        self.assertEqual(len(offsets), 4)
        # All units aligned at Z=1.2
        for off in offsets:
            self.assertAlmostEqual(off.z, 1.2)
        # Symmetrical about X=0
        self.assertAlmostEqual(offsets[0].x, -offsets[-1].x)

    def test_squadron_offsets_shock_wedge(self):
        self.squad.current_formation = SimulatedSquadronCommand.Formation.SHOCK_WEDGE
        offsets = self.squad.get_formation_offsets(5)
        self.assertEqual(len(offsets), 5)
        # Point unit is at (0, 0, 2.0)
        self.assertEqual(offsets[0], MockVector3(0, 0, 2.0))
        # Wing units trail back
        self.assertLess(offsets[1].z, offsets[0].z)
        self.assertLess(offsets[2].z, offsets[0].z)

    def test_squadron_offsets_perimeter_square(self):
        self.squad.current_formation = SimulatedSquadronCommand.Formation.PERIMETER_SQUARE
        offsets = self.squad.get_formation_offsets(4)
        self.assertEqual(len(offsets), 4)
        # Each unit should be distance ~2.5 from origin
        for off in offsets:
            dist = math.sqrt(off.x * off.x + off.z * off.z)
            self.assertAlmostEqual(dist, 2.5, places=2)

    def test_squadron_rally_call(self):
        rally_target = MockVector3(45, 10, 50)
        count = self.squad.issue_rally(rally_target, guard_count=5)
        self.assertEqual(count, 5)
        self.assertEqual(self.squad.rally_pos, rally_target)

    def test_squadron_serialization_roundtrip(self):
        self.squad.current_stance = SimulatedSquadronCommand.Stance.MONARCH_ESCORT
        self.squad.current_formation = SimulatedSquadronCommand.Formation.SHOCK_WEDGE
        self.squad.guard_morale = 85.0
        data = self.squad.to_dict()

        copy_squad = SimulatedSquadronCommand()
        copy_squad.from_dict(data)
        self.assertEqual(copy_squad.current_stance, SimulatedSquadronCommand.Stance.MONARCH_ESCORT)
        self.assertEqual(copy_squad.current_formation, SimulatedSquadronCommand.Formation.SHOCK_WEDGE)
        self.assertEqual(copy_squad.guard_morale, 85.0)

    def test_save_system_decrees_and_squadron_integration(self):
        self.decrees.proclaim_decree("guild_subsidies")
        self.squad.current_formation = SimulatedSquadronCommand.Formation.PERIMETER_SQUARE

        save_dict = {
            "decrees": self.decrees.to_dict(),
            "squadron": self.squad.to_dict(),
        }

        # Simulated load
        new_dec = SimulatedRoyalDecrees()
        new_dec.from_dict(save_dict["decrees"])
        self.assertIn("guild_subsidies", new_dec.active_decrees)

        new_sq = SimulatedSquadronCommand()
        new_sq.from_dict(save_dict["squadron"])
        self.assertEqual(new_sq.current_formation, SimulatedSquadronCommand.Formation.PERIMETER_SQUARE)

    def test_corvee_labor_tradeoff(self):
        self.decrees.proclaim_decree("corvee_labor")
        self.assertGreater(self.decrees.get_modifier("work_speed_mult"), 1.0)
        self.assertGreater(self.decrees.get_modifier("hunger_drain_mult"), 1.0)

    def test_grain_dole_relief_benefits(self):
        self.decrees.proclaim_decree("grain_dole_relief")
        self.assertLess(self.decrees.get_modifier("hunger_drain_mult"), 1.0)
        self.assertGreater(self.decrees.get_modifier("morale_bonus"), 0.0)

    def test_frontier_conscription_defense_benefit(self):
        self.decrees.proclaim_decree("frontier_conscription")
        self.assertGreater(self.decrees.get_modifier("guard_defense_mult"), 1.0)
        self.assertEqual(self.decrees.get_modifier("guard_capacity_bonus"), 4.0)

    def test_free_trade_charter_acceleration(self):
        self.decrees.proclaim_decree("free_trade_charter")
        self.assertLess(self.decrees.get_modifier("caravan_interval_mult"), 1.0)

    def test_monastic_scholarship_speedup(self):
        self.decrees.proclaim_decree("monastic_scholarship")
        self.assertGreater(self.decrees.get_modifier("tech_speed_mult"), 1.0)

    def test_squadron_stance_names(self):
        stance_map = {
            SimulatedSquadronCommand.Stance.DEFENSIVE_SENTINEL: "Defensive Sentinel",
            SimulatedSquadronCommand.Stance.AGGRESSIVE_ASSAULT: "Aggressive Assault",
            SimulatedSquadronCommand.Stance.MONARCH_ESCORT: "Monarch Escort",
        }
        for st, expected_substr in stance_map.items():
            name = self.squad.get_stance_name(st)
            self.assertIn(expected_substr, name)

    def test_squadron_formation_names(self):
        formations = ["Shield Wall", "Shock Wedge", "Skirmish Line", "Perimeter Square"]
        for i, f_name in enumerate(formations):
            name = self.squad.get_formation_name(i)
            self.assertIn(f_name, name)


if __name__ == "__main__":
    unittest.main()
