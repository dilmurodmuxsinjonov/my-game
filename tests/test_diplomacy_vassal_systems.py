#!/usr/bin/env python3
"""
Unit Test Suite for Milestone 48: Kingdom Diplomacy & Vassal Tribute Systems
Author: Voxel Lord Engineering Team
Tests faction relations, treaties, vassal tribute cycles, opinion mechanics, and persistence.
"""

import unittest
import math
import hashlib
import json
from typing import Dict, Any


class MockSupplyChain:
    """Mock supply chain tracking resources for testing tribute delivery."""
    def __init__(self):
        self.resources: Dict[str, int] = {
            "gold_coins": 100,
            "bread": 50,
            "logs": 40,
            "iron_ingots": 20,
            "stone": 30,
            "tools": 10
        }

    def get_resource(self, res: str) -> int:
        return self.resources.get(res, 0)

    def add_resource(self, res: str, amt: int) -> None:
        self.resources[res] = self.resources.get(res, 0) + amt

    def consume_resource(self, res: str, amt: int) -> bool:
        if self.resources.get(res, 0) >= amt:
            self.resources[res] -= amt
            return True
        return False


class PythonDiplomacySystem:
    """Python reference mirror of scripts/core/diplomacy_system.gd."""

    class RelationshipStatus:
        WAR = 0
        HOSTILE = 1
        NEUTRAL = 2
        FRIENDLY = 3
        ALLIED = 4
        VASSAL = 5

    class TreatyType:
        NON_AGGRESSION = 0
        TRADE_CONCORDAT = 1
        DEFENSIVE_LEAGUE = 2
        VASSALAGE_CHARTER = 3

    def __init__(self):
        self.factions: Dict[str, Dict[str, Any]] = {}
        self.emissary_timer = 0.0
        self.emissary_interval = 120.0
        self.signal_log = []
        self.init_default_factions()

    def init_default_factions(self):
        self.factions = {
            "valoria": {
                "id": "valoria",
                "name": "Duchy of Valoria",
                "ruler": "Grand Duke Alden IV",
                "archetype": "Feudal Martial",
                "icon": "🛡️",
                "opinion": 15.0,
                "base_opinion": 15.0,
                "military_strength": 180.0,
                "economic_wealth": 240.0,
                "demands": "food",
                "offers": "iron_ingots",
                "is_vassal": False,
                "vassal_tribute_timer": 0.0,
                "vassal_tribute_interval": 90.0,
                "active_treaties": {},
                "last_gift_time": 0.0,
                "tribute_package": {"iron_ingots": 6, "gold_coins": 20, "tools": 3}
            },
            "silvercoast": {
                "id": "silvercoast",
                "name": "Silvercoast Trade League",
                "ruler": "High Doge Lorenzo",
                "archetype": "Mercantile Guild",
                "icon": "⛵",
                "opinion": 10.0,
                "base_opinion": 10.0,
                "military_strength": 110.0,
                "economic_wealth": 500.0,
                "demands": "timber",
                "offers": "gold_coins",
                "is_vassal": False,
                "vassal_tribute_timer": 0.0,
                "vassal_tribute_interval": 80.0,
                "active_treaties": {},
                "last_gift_time": 0.0,
                "tribute_package": {"gold_coins": 50, "luxury_wine": 2, "salt": 8}
            },
            "ashfell": {
                "id": "ashfell",
                "name": "Ashfell Mountain Clans",
                "ruler": "Chieftain Torvold Ironfang",
                "archetype": "Raider Confederation",
                "icon": "⚔️",
                "opinion": -25.0,
                "base_opinion": -25.0,
                "military_strength": 160.0,
                "economic_wealth": 140.0,
                "demands": "beer",
                "offers": "stone",
                "is_vassal": False,
                "vassal_tribute_timer": 0.0,
                "vassal_tribute_interval": 100.0,
                "active_treaties": {},
                "last_gift_time": 0.0,
                "tribute_package": {"stone": 25, "iron_ore": 12, "gold_coins": 15}
            },
            "sunken_mire": {
                "id": "sunken_mire",
                "name": "Barony of the Sunken Mire",
                "ruler": "Baroness Elspeth the Recluse",
                "archetype": "Agrarian Isolationist",
                "icon": "🌿",
                "opinion": 0.0,
                "base_opinion": 0.0,
                "military_strength": 90.0,
                "economic_wealth": 200.0,
                "demands": "tools",
                "offers": "medicine",
                "is_vassal": False,
                "vassal_tribute_timer": 0.0,
                "vassal_tribute_interval": 90.0,
                "active_treaties": {},
                "last_gift_time": 0.0,
                "tribute_package": {"medicine": 5, "herbs": 15, "food": 20}
            }
        }

    def get_relationship_status(self, faction_id: str) -> int:
        f = self.factions.get(faction_id)
        if not f:
            return self.RelationshipStatus.NEUTRAL
        if f.get("is_vassal", False):
            return self.RelationshipStatus.VASSAL
        op = f.get("opinion", 0.0)
        if op <= -40.0:
            return self.RelationshipStatus.WAR
        elif op <= -10.0:
            return self.RelationshipStatus.HOSTILE
        elif op <= 29.0:
            return self.RelationshipStatus.NEUTRAL
        elif op <= 69.0:
            return self.RelationshipStatus.FRIENDLY
        elif op <= 90.0:
            return self.RelationshipStatus.ALLIED
        else:
            return self.RelationshipStatus.VASSAL

    def get_status_name(self, status: int) -> str:
        names = {
            self.RelationshipStatus.WAR: "War ⚔️",
            self.RelationshipStatus.HOSTILE: "Hostile ⚠️",
            self.RelationshipStatus.NEUTRAL: "Neutral ⚖️",
            self.RelationshipStatus.FRIENDLY: "Friendly 🕊️",
            self.RelationshipStatus.ALLIED: "Allied 🛡️",
            self.RelationshipStatus.VASSAL: "Vassal Fealty 👑"
        }
        return names.get(status, "Unknown")

    def modify_opinion(self, faction_id: str, delta: float, reason: str = "") -> float:
        if faction_id not in self.factions:
            return 0.0
        old_val = self.factions[faction_id]["opinion"]
        new_val = max(-100.0, min(100.0, old_val + delta))
        self.factions[faction_id]["opinion"] = new_val
        st = self.get_relationship_status(faction_id)
        self.signal_log.append(("opinion_changed", faction_id, old_val, new_val, st, reason))
        return new_val

    def can_sign_treaty(self, faction_id: str, treaty_type: int) -> Dict[str, Any]:
        if faction_id not in self.factions:
            return {"allowed": False, "reason": "Unknown faction", "cost_gold": 0}
        f = self.factions[faction_id]
        op = f["opinion"]
        active = f["active_treaties"]

        if treaty_type in active:
            return {"allowed": False, "reason": "Treaty already active", "cost_gold": 0}
        if self.get_relationship_status(faction_id) == self.RelationshipStatus.WAR:
            return {"allowed": False, "reason": "Cannot sign treaty while at war!", "cost_gold": 0}

        if treaty_type == self.TreatyType.NON_AGGRESSION:
            if op < 0.0:
                return {"allowed": False, "reason": "Requires Neutral or higher opinion (>= 0)", "cost_gold": 25}
            return {"allowed": True, "reason": "Eligible for Non-Aggression Pact", "cost_gold": 25}
        elif treaty_type == self.TreatyType.TRADE_CONCORDAT:
            if op < 20.0:
                return {"allowed": False, "reason": "Requires at least +20 opinion for commerce treaty", "cost_gold": 45}
            return {"allowed": True, "reason": "Eligible for Trade Concordat", "cost_gold": 45}
        elif treaty_type == self.TreatyType.DEFENSIVE_LEAGUE:
            if op < 50.0:
                return {"allowed": False, "reason": "Requires Friendly disposition (>= +50 opinion)", "cost_gold": 80}
            return {"allowed": True, "reason": "Eligible for Defensive Military League", "cost_gold": 80}
        elif treaty_type == self.TreatyType.VASSALAGE_CHARTER:
            if f.get("is_vassal", False):
                return {"allowed": False, "reason": "Faction is already your vassal", "cost_gold": 0}
            if op < 80.0:
                return {"allowed": False, "reason": "Requires Allied relationship (>= +80 opinion) to peacefully vassalize", "cost_gold": 150}
            return {"allowed": True, "reason": "Eligible to establish Vassalage Charter", "cost_gold": 150}
        return {"allowed": False, "reason": "Invalid treaty type", "cost_gold": 0}

    def sign_treaty(self, faction_id: str, treaty_type: int, treasury_gold: int) -> bool:
        chk = self.can_sign_treaty(faction_id, treaty_type)
        if not chk["allowed"] or treasury_gold < chk["cost_gold"]:
            return False
        f = self.factions[faction_id]
        if treaty_type == self.TreatyType.VASSALAGE_CHARTER:
            f["active_treaties"][treaty_type] = -1.0
            f["is_vassal"] = True
            f["vassal_tribute_timer"] = 0.0
            self.modify_opinion(faction_id, 20.0, "Vassalage chartered")
        elif treaty_type == self.TreatyType.TRADE_CONCORDAT:
            f["active_treaties"][treaty_type] = 400.0
            self.modify_opinion(faction_id, 10.0, "Trade treaty signed")
        elif treaty_type == self.TreatyType.DEFENSIVE_LEAGUE:
            f["active_treaties"][treaty_type] = 360.0
            self.modify_opinion(faction_id, 15.0, "Defensive alliance enacted")
        elif treaty_type == self.TreatyType.NON_AGGRESSION:
            f["active_treaties"][treaty_type] = 300.0
            self.modify_opinion(faction_id, 8.0, "Non-aggression pact agreed")
        self.signal_log.append(("treaty_signed", faction_id, treaty_type))
        return True

    def break_treaty(self, faction_id: str, treaty_type: int) -> bool:
        if faction_id not in self.factions:
            return False
        f = self.factions[faction_id]
        if treaty_type not in f["active_treaties"]:
            return False
        del f["active_treaties"][treaty_type]
        if treaty_type == self.TreatyType.VASSALAGE_CHARTER:
            f["is_vassal"] = False
        penalty = -35.0
        self.modify_opinion(faction_id, penalty, "Dishonorable treaty breach")
        self.signal_log.append(("treaty_broken", faction_id, treaty_type, penalty))
        return True

    def declare_war(self, faction_id: str) -> bool:
        if faction_id not in self.factions:
            return False
        f = self.factions[faction_id]
        f["is_vassal"] = False
        f["active_treaties"].clear()
        f["opinion"] = -100.0
        self.signal_log.append(("war_declared", faction_id, True))
        return True

    def sue_for_peace(self, faction_id: str, indemnity_gold: int) -> bool:
        if faction_id not in self.factions:
            return False
        f = self.factions[faction_id]
        if self.get_relationship_status(faction_id) != self.RelationshipStatus.WAR:
            return False
        required_gold = int(f.get("military_strength", 100.0) * 0.5)
        if indemnity_gold < required_gold:
            return False
        f["opinion"] = -15.0
        self.signal_log.append(("peace_concluded", faction_id))
        return True

    def send_gift(self, faction_id: str, resource_name: str, amount: int, available_stock: int) -> Dict[str, Any]:
        if faction_id not in self.factions:
            return {"success": False, "opinion_boost": 0.0, "message": "Faction not found"}
        if amount <= 0 or available_stock < amount:
            return {"success": False, "opinion_boost": 0.0, "message": "Insufficient resources to gift"}
        f = self.factions[faction_id]
        multiplier = 1.0
        dem = f.get("demands", "")
        if dem == resource_name or (resource_name == "bread" and dem == "food") or (resource_name == "logs" and dem == "timber"):
            multiplier = 1.75
        elif resource_name == "gold_coins":
            multiplier = 1.4

        boost = min(35.0, max(2.0, (amount * 1.5) * multiplier))
        self.modify_opinion(faction_id, boost, "Envoy tribute gift received")
        return {"success": True, "opinion_boost": boost, "message": f"Gifted {amount} {resource_name}"}

    def demand_tribute(self, faction_id: str, resource_name: str, amount: int, player_military_strength: float) -> Dict[str, Any]:
        if faction_id not in self.factions:
            return {"accepted": False, "amount_received": 0, "opinion_penalty": 0.0, "reason": "Faction not found"}
        f = self.factions[faction_id]
        target_mil = f.get("military_strength", 100.0)
        is_vassal = f.get("is_vassal", False)

        if is_vassal:
            penalty = -10.0
            self.modify_opinion(faction_id, penalty, "Monarch tribute extortion")
            self.signal_log.append(("tribute_demanded", faction_id, {resource_name: amount}, True))
            return {"accepted": True, "amount_received": amount, "opinion_penalty": penalty, "reason": "Vassal complied"}

        if player_military_strength > (target_mil * 1.4):
            penalty = -25.0
            self.modify_opinion(faction_id, penalty, "Extorted by military menace")
            self.signal_log.append(("tribute_demanded", faction_id, {resource_name: amount}, True))
            return {"accepted": True, "amount_received": amount, "opinion_penalty": penalty, "reason": "Intimidated by superior legion"}
        else:
            penalty = -30.0
            self.modify_opinion(faction_id, penalty, "Defiant against insolent tribute demands")
            self.signal_log.append(("tribute_demanded", faction_id, {resource_name: amount}, False))
            if f["opinion"] <= -40.0:
                self.declare_war(faction_id)
            return {"accepted": False, "amount_received": 0, "opinion_penalty": penalty, "reason": "Defiantly rejected"}

    def process_diplomacy(self, delta: float, supply_chain: Any = None) -> None:
        for f_id, f in self.factions.items():
            treaties = f.get("active_treaties", {})
            to_remove = []
            for t_type, remaining in list(treaties.items()):
                if remaining > 0.0:
                    remaining -= delta
                    treaties[t_type] = remaining
                    if remaining <= 0.0:
                        to_remove.append(t_type)
                if t_type == self.TreatyType.TRADE_CONCORDAT:
                    self.modify_opinion(f_id, delta * 0.02, "Trade Concordat prosperity")
                    if supply_chain and (delta >= 1.0):
                        supply_chain.add_resource("gold_coins", 1)

            for exp_t in to_remove:
                del treaties[exp_t]
                self.signal_log.append(("treaty_broken", f_id, exp_t, 0.0))

            if f.get("is_vassal", False):
                v_timer = f.get("vassal_tribute_timer", 0.0) + delta
                v_interval = f.get("vassal_tribute_interval", 90.0)
                if v_timer >= v_interval:
                    v_timer = 0.0
                    pkg = f.get("tribute_package", {"gold_coins": 20})
                    if supply_chain:
                        for k, v in pkg.items():
                            supply_chain.add_resource(k, v)
                    self.signal_log.append(("tribute_received", f_id, pkg))
                f["vassal_tribute_timer"] = v_timer

            # Opinion drift
            cur_op = f.get("opinion", 0.0)
            base_op = f.get("base_opinion", 0.0)
            if abs(cur_op - base_op) > 0.01:
                drift_rate = delta * 0.015
                if cur_op > base_op:
                    f["opinion"] = max(base_op, cur_op - drift_rate)
                else:
                    f["opinion"] = min(base_op, cur_op + drift_rate)

        self.emissary_timer += delta
        if self.emissary_timer >= self.emissary_interval:
            self.emissary_timer = 0.0
            self.signal_log.append(("emissary_arrived", "valoria", {"message": "Envoy arrived"}))

    def to_dict(self) -> Dict[str, Any]:
        out_factions = {}
        for f_id, f in self.factions.items():
            treaties_serialized = {str(k): v for k, v in f.get("active_treaties", {}).items()}
            out_factions[f_id] = {
                "opinion": f.get("opinion", 0.0),
                "base_opinion": f.get("base_opinion", 0.0),
                "military_strength": f.get("military_strength", 100.0),
                "economic_wealth": f.get("economic_wealth", 100.0),
                "is_vassal": f.get("is_vassal", False),
                "vassal_tribute_timer": f.get("vassal_tribute_timer", 0.0),
                "vassal_tribute_interval": f.get("vassal_tribute_interval", 90.0),
                "active_treaties": treaties_serialized
            }
        return {"factions": out_factions, "emissary_timer": self.emissary_timer}

    def from_dict(self, data: Dict[str, Any]) -> None:
        if not data:
            return
        self.emissary_timer = data.get("emissary_timer", 0.0)
        for f_id, src in data.get("factions", {}).items():
            if f_id in self.factions:
                self.factions[f_id]["opinion"] = src.get("opinion", self.factions[f_id]["opinion"])
                self.factions[f_id]["base_opinion"] = src.get("base_opinion", self.factions[f_id]["base_opinion"])
                self.factions[f_id]["military_strength"] = src.get("military_strength", self.factions[f_id]["military_strength"])
                self.factions[f_id]["economic_wealth"] = src.get("economic_wealth", self.factions[f_id]["economic_wealth"])
                self.factions[f_id]["is_vassal"] = src.get("is_vassal", False)
                self.factions[f_id]["vassal_tribute_timer"] = src.get("vassal_tribute_timer", 0.0)
                self.factions[f_id]["vassal_tribute_interval"] = src.get("vassal_tribute_interval", 90.0)
                loaded_treaties = {int(k): v for k, v in src.get("active_treaties", {}).items()}
                self.factions[f_id]["active_treaties"] = loaded_treaties


class TestDiplomacyVassalSystems(unittest.TestCase):
    """28 Comprehensive Automated Tests for Milestone 48."""

    def setUp(self):
        self.dip = PythonDiplomacySystem()
        self.supply = MockSupplyChain()

    def test_01_default_factions_initialization(self):
        """Verify all 4 core neighboring realms are registered with expected archetypes and stats."""
        self.assertEqual(len(self.dip.factions), 4)
        self.assertIn("valoria", self.dip.factions)
        self.assertIn("silvercoast", self.dip.factions)
        self.assertIn("ashfell", self.dip.factions)
        self.assertIn("sunken_mire", self.dip.factions)
        self.assertEqual(self.dip.factions["valoria"]["ruler"], "Grand Duke Alden IV")
        self.assertEqual(self.dip.factions["silvercoast"]["archetype"], "Mercantile Guild")
        self.assertEqual(self.dip.factions["ashfell"]["demands"], "beer")
        self.assertEqual(self.dip.factions["sunken_mire"]["offers"], "medicine")

    def test_02_relationship_status_thresholds(self):
        """Verify opinion boundaries for War, Hostile, Neutral, Friendly, Allied, and Vassal."""
        self.dip.factions["valoria"]["opinion"] = -50.0
        self.assertEqual(self.dip.get_relationship_status("valoria"), self.dip.RelationshipStatus.WAR)

        self.dip.factions["valoria"]["opinion"] = -25.0
        self.assertEqual(self.dip.get_relationship_status("valoria"), self.dip.RelationshipStatus.HOSTILE)

        self.dip.factions["valoria"]["opinion"] = 15.0
        self.assertEqual(self.dip.get_relationship_status("valoria"), self.dip.RelationshipStatus.NEUTRAL)

        self.dip.factions["valoria"]["opinion"] = 45.0
        self.assertEqual(self.dip.get_relationship_status("valoria"), self.dip.RelationshipStatus.FRIENDLY)

        self.dip.factions["valoria"]["opinion"] = 80.0
        self.assertEqual(self.dip.get_relationship_status("valoria"), self.dip.RelationshipStatus.ALLIED)

        self.dip.factions["valoria"]["opinion"] = 95.0
        self.assertEqual(self.dip.get_relationship_status("valoria"), self.dip.RelationshipStatus.VASSAL)

    def test_03_opinion_clamping(self):
        """Verify opinion cannot exceed +100.0 or fall below -100.0."""
        self.dip.modify_opinion("valoria", 200.0)
        self.assertEqual(self.dip.factions["valoria"]["opinion"], 100.0)

        self.dip.modify_opinion("valoria", -300.0)
        self.assertEqual(self.dip.factions["valoria"]["opinion"], -100.0)

    def test_04_opinion_changed_signal_logging(self):
        """Verify signal logging on opinion changes."""
        self.dip.modify_opinion("silvercoast", 25.0, "Gold gift")
        self.assertTrue(len(self.dip.signal_log) > 0)
        sig_name, f_id, old_v, new_v, status, reason = self.dip.signal_log[-1]
        self.assertEqual(sig_name, "opinion_changed")
        self.assertEqual(f_id, "silvercoast")
        self.assertEqual(old_v, 10.0)
        self.assertEqual(new_v, 35.0)
        self.assertEqual(status, self.dip.RelationshipStatus.FRIENDLY)

    def test_05_gift_preference_multiplier(self):
        """Preferred imports yield 1.75x bonus over generic goods."""
        res_generic = self.dip.send_gift("valoria", "stone", 10, 50)
        boost_generic = res_generic["opinion_boost"]

        # Reset opinion
        self.dip.factions["valoria"]["opinion"] = 15.0
        res_preferred = self.dip.send_gift("valoria", "bread", 10, 50) # Valoria demands food
        boost_preferred = res_preferred["opinion_boost"]

        self.assertGreater(boost_preferred, boost_generic)
        self.assertAlmostEqual(boost_preferred, boost_generic * 1.75, places=1)

    def test_06_gift_insufficient_stock_rejection(self):
        """Attempting to gift more resources than in stock fails."""
        res = self.dip.send_gift("silvercoast", "gold_coins", 100, 10) # wants 100, only 10 available
        self.assertFalse(res["success"])
        self.assertIn("Insufficient", res["message"])

    def test_07_gift_opinion_cap_per_delivery(self):
        """Individual gift deliveries cap at +35.0 opinion."""
        res = self.dip.send_gift("sunken_mire", "tools", 100, 200)
        self.assertEqual(res["opinion_boost"], 35.0)

    def test_08_can_sign_non_aggression_pact(self):
        """Non-aggression requires opinion >= 0 and costs 25 gold."""
        self.dip.factions["ashfell"]["opinion"] = -25.0
        chk = self.dip.can_sign_treaty("ashfell", self.dip.TreatyType.NON_AGGRESSION)
        self.assertFalse(chk["allowed"])

        self.dip.factions["ashfell"]["opinion"] = 5.0
        chk2 = self.dip.can_sign_treaty("ashfell", self.dip.TreatyType.NON_AGGRESSION)
        self.assertTrue(chk2["allowed"])
        self.assertEqual(chk2["cost_gold"], 25)

    def test_09_can_sign_trade_concordat(self):
        """Trade concordat requires opinion >= 20 and costs 45 gold."""
        self.dip.factions["silvercoast"]["opinion"] = 10.0
        chk = self.dip.can_sign_treaty("silvercoast", self.dip.TreatyType.TRADE_CONCORDAT)
        self.assertFalse(chk["allowed"])

        self.dip.factions["silvercoast"]["opinion"] = 25.0
        chk2 = self.dip.can_sign_treaty("silvercoast", self.dip.TreatyType.TRADE_CONCORDAT)
        self.assertTrue(chk2["allowed"])
        self.assertEqual(chk2["cost_gold"], 45)

    def test_10_can_sign_defensive_league(self):
        """Defensive military league requires opinion >= 50 and costs 80 gold."""
        self.dip.factions["valoria"]["opinion"] = 40.0
        chk = self.dip.can_sign_treaty("valoria", self.dip.TreatyType.DEFENSIVE_LEAGUE)
        self.assertFalse(chk["allowed"])

        self.dip.factions["valoria"]["opinion"] = 60.0
        chk2 = self.dip.can_sign_treaty("valoria", self.dip.TreatyType.DEFENSIVE_LEAGUE)
        self.assertTrue(chk2["allowed"])
        self.assertEqual(chk2["cost_gold"], 80)

    def test_11_can_sign_vassalage_charter(self):
        """Vassalage charter requires opinion >= 80 and costs 150 gold."""
        self.dip.factions["sunken_mire"]["opinion"] = 70.0
        chk = self.dip.can_sign_treaty("sunken_mire", self.dip.TreatyType.VASSALAGE_CHARTER)
        self.assertFalse(chk["allowed"])

        self.dip.factions["sunken_mire"]["opinion"] = 85.0
        chk2 = self.dip.can_sign_treaty("sunken_mire", self.dip.TreatyType.VASSALAGE_CHARTER)
        self.assertTrue(chk2["allowed"])
        self.assertEqual(chk2["cost_gold"], 150)

    def test_12_sign_treaty_insufficient_treasury_rejection(self):
        """Treaty cannot be signed if player treasury gold is insufficient."""
        self.dip.factions["valoria"]["opinion"] = 5.0
        success = self.dip.sign_treaty("valoria", self.dip.TreatyType.NON_AGGRESSION, 10) # costs 25
        self.assertFalse(success)
        self.assertNotIn(self.dip.TreatyType.NON_AGGRESSION, self.dip.factions["valoria"]["active_treaties"])

    def test_13_sign_treaty_active_duration_recorded(self):
        """Signing treaty registers active duration in faction state."""
        self.dip.factions["valoria"]["opinion"] = 25.0
        success = self.dip.sign_treaty("valoria", self.dip.TreatyType.TRADE_CONCORDAT, 100)
        self.assertTrue(success)
        self.assertIn(self.dip.TreatyType.TRADE_CONCORDAT, self.dip.factions["valoria"]["active_treaties"])
        self.assertEqual(self.dip.factions["valoria"]["active_treaties"][self.dip.TreatyType.TRADE_CONCORDAT], 400.0)

    def test_14_sign_vassalage_sets_permanent_fealty(self):
        """Signing vassalage marks is_vassal True and duration -1.0 (permanent)."""
        self.dip.factions["sunken_mire"]["opinion"] = 85.0
        success = self.dip.sign_treaty("sunken_mire", self.dip.TreatyType.VASSALAGE_CHARTER, 200)
        self.assertTrue(success)
        self.assertTrue(self.dip.factions["sunken_mire"]["is_vassal"])
        self.assertEqual(self.dip.factions["sunken_mire"]["active_treaties"][self.dip.TreatyType.VASSALAGE_CHARTER], -1.0)
        self.assertEqual(self.dip.get_relationship_status("sunken_mire"), self.dip.RelationshipStatus.VASSAL)

    def test_15_break_treaty_dishonor_penalty(self):
        """Breaking an active treaty inflicts -35.0 opinion penalty."""
        self.dip.factions["silvercoast"]["opinion"] = 40.0
        self.dip.sign_treaty("silvercoast", self.dip.TreatyType.TRADE_CONCORDAT, 100)
        pre_op = self.dip.factions["silvercoast"]["opinion"]

        self.dip.break_treaty("silvercoast", self.dip.TreatyType.TRADE_CONCORDAT)
        self.assertEqual(self.dip.factions["silvercoast"]["opinion"], pre_op - 35.0)
        self.assertNotIn(self.dip.TreatyType.TRADE_CONCORDAT, self.dip.factions["silvercoast"]["active_treaties"])

    def test_16_break_vassalage_revokes_vassal_fealty(self):
        """Breaking vassalage revokes vassal status and removes fealty status."""
        self.dip.factions["sunken_mire"]["opinion"] = 90.0
        self.dip.sign_treaty("sunken_mire", self.dip.TreatyType.VASSALAGE_CHARTER, 200)
        self.assertTrue(self.dip.factions["sunken_mire"]["is_vassal"])

        self.dip.break_treaty("sunken_mire", self.dip.TreatyType.VASSALAGE_CHARTER)
        self.assertFalse(self.dip.factions["sunken_mire"]["is_vassal"])

    def test_17_declare_war_annuls_all_treaties_and_drops_opinion(self):
        """Declaring war annuls all treaties, resets vassal status, and drops opinion to -100."""
        self.dip.factions["valoria"]["active_treaties"][self.dip.TreatyType.NON_AGGRESSION] = 200.0
        self.dip.factions["valoria"]["active_treaties"][self.dip.TreatyType.TRADE_CONCORDAT] = 300.0

        self.dip.declare_war("valoria")
        self.assertEqual(self.dip.factions["valoria"]["opinion"], -100.0)
        self.assertEqual(len(self.dip.factions["valoria"]["active_treaties"]), 0)
        self.assertEqual(self.dip.get_relationship_status("valoria"), self.dip.RelationshipStatus.WAR)

    def test_18_war_prevents_treaty_negotiations(self):
        """Treaties cannot be signed when at war with a realm."""
        self.dip.declare_war("ashfell")
        chk = self.dip.can_sign_treaty("ashfell", self.dip.TreatyType.NON_AGGRESSION)
        self.assertFalse(chk["allowed"])
        self.assertIn("war", chk["reason"].lower())

    def test_19_sue_for_peace_with_reparations(self):
        """Paying required indemnity gold restores hostile-level peace (-15.0)."""
        self.dip.declare_war("silvercoast") # military strength 110 -> 55 gold required
        success = self.dip.sue_for_peace("silvercoast", 60)
        self.assertTrue(success)
        self.assertEqual(self.dip.factions["silvercoast"]["opinion"], -15.0)
        self.assertEqual(self.dip.get_relationship_status("silvercoast"), self.dip.RelationshipStatus.HOSTILE)

    def test_20_sue_for_peace_insufficient_gold_fails(self):
        """Sue for peace fails if indemnity is lower than required reparation."""
        self.dip.declare_war("valoria") # military strength 180 -> 90 gold required
        success = self.dip.sue_for_peace("valoria", 50)
        self.assertFalse(success)
        self.assertEqual(self.dip.factions["valoria"]["opinion"], -100.0)

    def test_21_vassal_tribute_periodic_delivery_cycle(self):
        """Processing delta past vassal tribute interval triggers tribute delivery."""
        self.dip.factions["valoria"]["is_vassal"] = True
        self.dip.factions["valoria"]["vassal_tribute_timer"] = 85.0
        self.dip.factions["valoria"]["vassal_tribute_interval"] = 90.0

        pre_gold = self.supply.get_resource("gold_coins")
        self.dip.process_diplomacy(10.0, self.supply) # advances 10s -> 95s >= 90s

        self.assertGreater(self.supply.get_resource("gold_coins"), pre_gold)
        self.assertEqual(self.dip.factions["valoria"]["vassal_tribute_timer"], 0.0)
        received_sigs = [s for s in self.dip.signal_log if s[0] == "tribute_received"]
        self.assertEqual(len(received_sigs), 1)

    def test_22_vassal_tribute_adds_package_to_supply_chain(self):
        """Tribute delivery correctly deposits all items from tribute package into supply chain."""
        self.dip.factions["silvercoast"]["is_vassal"] = True
        self.dip.factions["silvercoast"]["vassal_tribute_timer"] = 79.0
        self.dip.factions["silvercoast"]["vassal_tribute_interval"] = 80.0

        pre_wine = self.supply.get_resource("luxury_wine")
        self.dip.process_diplomacy(2.0, self.supply)

        self.assertEqual(self.supply.get_resource("luxury_wine"), pre_wine + 2)

    def test_23_demand_tribute_from_vassal_guaranteed_compliance(self):
        """Demanding tribute from a sworn vassal succeeds with moderate opinion penalty."""
        self.dip.factions["valoria"]["is_vassal"] = True
        pre_op = self.dip.factions["valoria"]["opinion"]

        res = self.dip.demand_tribute("valoria", "gold_coins", 30, 100.0)
        self.assertTrue(res["accepted"])
        self.assertEqual(res["amount_received"], 30)
        self.assertEqual(self.dip.factions["valoria"]["opinion"], pre_op - 10.0)

    def test_24_demand_tribute_intimidation_superior_military(self):
        """Player with > 1.4x military strength successfully extorts tribute from non-vassal."""
        # Sunken Mire military = 90.0; Player military = 150.0 (> 126.0)
        res = self.dip.demand_tribute("sunken_mire", "medicine", 5, 150.0)
        self.assertTrue(res["accepted"])
        self.assertEqual(res["amount_received"], 5)
        self.assertEqual(res["opinion_penalty"], -25.0)

    def test_25_demand_tribute_rejection_triggers_war_escalation(self):
        """Weak player demanding tribute from hostile realm gets rejected and triggers war if opinion drops <= -40."""
        self.dip.factions["ashfell"]["opinion"] = -30.0 # Ashfell military = 160.0
        res = self.dip.demand_tribute("ashfell", "gold_coins", 40, 50.0) # Player military only 50.0
        self.assertFalse(res["accepted"])
        # -30 - 30 = -60 <= -40 -> triggers war
        self.assertEqual(self.dip.get_relationship_status("ashfell"), self.dip.RelationshipStatus.WAR)

    def test_26_treaty_countdown_and_expiration(self):
        """Timed treaties decrement with delta and are erased when remaining duration <= 0."""
        self.dip.factions["valoria"]["active_treaties"][self.dip.TreatyType.NON_AGGRESSION] = 5.0
        self.dip.process_diplomacy(6.0, self.supply)
        self.assertNotIn(self.dip.TreatyType.NON_AGGRESSION, self.dip.factions["valoria"]["active_treaties"])

    def test_27_opinion_natural_drift_towards_base(self):
        """Opinions that deviate from baseline slowly drift back over time."""
        self.dip.factions["valoria"]["opinion"] = 60.0 # base is 15.0
        self.dip.process_diplomacy(100.0, self.supply)
        self.assertLess(self.dip.factions["valoria"]["opinion"], 60.0)
        self.assertGreaterEqual(self.dip.factions["valoria"]["opinion"], 15.0)

    def test_28_serialization_roundtrip_sha256(self):
        """Verify to_dict and from_dict produce consistent payload with valid SHA-256 hash."""
        self.dip.factions["valoria"]["opinion"] = 42.5
        self.dip.factions["valoria"]["active_treaties"][self.dip.TreatyType.TRADE_CONCORDAT] = 250.0
        self.dip.factions["silvercoast"]["is_vassal"] = True

        data = self.dip.to_dict()
        payload_str = json.dumps(data, sort_keys=True)
        h1 = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        self.assertEqual(len(h1), 64)

        # Restore into fresh instance
        fresh_dip = PythonDiplomacySystem()
        fresh_dip.from_dict(data)
        self.assertAlmostEqual(fresh_dip.factions["valoria"]["opinion"], 42.5)
        self.assertTrue(fresh_dip.factions["silvercoast"]["is_vassal"])
        self.assertEqual(fresh_dip.factions["valoria"]["active_treaties"][self.dip.TreatyType.TRADE_CONCORDAT], 250.0)


if __name__ == "__main__":
    unittest.main()
