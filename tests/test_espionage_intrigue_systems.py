#!/usr/bin/env python3
"""
Unit Test Suite for Milestone 52: Royal Spymaster Court Intrigue & Shadow Espionage Network
Author: Voxel Lord Engineering Team
Tests shadow agent recruitment, covert operations (gather intel, sabotage siege, steal tech, incite revolt),
domestic counter-intelligence, interrogation dungeons, ransom exchanges, and persistence roundtrip integrity.
"""

import unittest
import hashlib
import json
from typing import Dict, Any, List, Optional


class MockSupplyChain:
    """Mock supply chain tracking resources for espionage operations and ransoms."""
    def __init__(self):
        self.resources: Dict[str, int] = {
            "gold_coins": 250,
            "bread": 40,
            "iron_ingots": 30
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


class PythonEspionageManager:
    """Python mirror of scripts/combat/espionage_manager.gd."""

    def __init__(self):
        self.agent_archetypes: Dict[str, Dict[str, Any]] = {}
        self.operations_catalog: Dict[str, Dict[str, Any]] = {}
        self.recruited_agents: Dict[str, Dict[str, Any]] = {}
        self.active_operations: List[Dict[str, Any]] = []
        self.captured_prisoners: List[Dict[str, Any]] = []
        self.citadel_security_rating: float = 65.0
        self.court_suspicion: float = 10.0
        self.total_operations_completed: int = 0
        self.successful_operations_count: int = 0
        self.plots_thwarted_count: int = 0
        self.signal_log: List[tuple] = []
        self.init_archetypes()
        self.init_operations_catalog()

    def init_archetypes(self):
        self.agent_archetypes = {
            "informant": {
                "type": "informant",
                "name": "Whispering Tavern Informant",
                "cost_gold": 30,
                "upkeep_daily": 2,
                "stealth_bonus": 0.15,
                "desc": "Low-profile eyes and ears in town squares and foreign border inns.",
                "icon": "👂"
            },
            "saboteur": {
                "type": "saboteur",
                "name": "Infiltration Sapper & Saboteur",
                "cost_gold": 60,
                "upkeep_daily": 4,
                "sabotage_bonus": 0.35,
                "desc": "Expert in arson, ballistics rigging, and spiking enemy siege catapults.",
                "icon": "🗡️"
            },
            "master_spy": {
                "type": "master_spy",
                "name": "Shadow Courtier & Master Provocateur",
                "cost_gold": 120,
                "upkeep_daily": 8,
                "intel_bonus": 0.45,
                "desc": "Elite court infiltrator capable of falsifying treaties and stealing secrets.",
                "icon": "🎭"
            }
        }

    def init_operations_catalog(self):
        self.operations_catalog = {
            "gather_invasion_intel": {
                "id": "gather_invasion_intel",
                "name": "Uncover Military Invasion War Plans",
                "cost_gold": 25,
                "duration": 45.0,
                "base_success_chance": 0.80,
                "risk_capture": 0.15,
                "desc": "Infiltrate foreign war councils to determine exact attack target and siege engines.",
                "icon": "🗺️"
            },
            "sabotage_siege_weapons": {
                "id": "sabotage_siege_weapons",
                "name": "Spike Battering Rams & Burn Pitch Depots",
                "cost_gold": 45,
                "duration": 60.0,
                "base_success_chance": 0.65,
                "risk_capture": 0.25,
                "desc": "Disables enemy siege engineering, reducing battalion power by 40%.",
                "icon": "💥"
            },
            "steal_scholastic_tech": {
                "id": "steal_scholastic_tech",
                "name": "Pilfer Monastic Scriptoria Parchments",
                "cost_gold": 60,
                "duration": 75.0,
                "base_success_chance": 0.60,
                "risk_capture": 0.30,
                "desc": "Steals ancient engineering parchments, granting +120 scholastic research points.",
                "icon": "📜"
            },
            "incite_border_revolt": {
                "id": "incite_border_revolt",
                "name": "Sow Dissidence & Bribe Border Troops",
                "cost_gold": 80,
                "duration": 90.0,
                "base_success_chance": 0.55,
                "risk_capture": 0.35,
                "desc": "Instigates peasant revolt in rival province, recruiting +3 deserters to royal guard.",
                "icon": "🔥"
            }
        }

    def process(self, delta: float) -> None:
        finished = []
        for op in self.active_operations:
            op["timer"] -= delta
            if op["timer"] <= 0.0:
                finished.append(op)
        for op in finished:
            self.resolve_operation(op)
            self.active_operations.remove(op)

    def recruit_agent(self, archetype_type: str, agent_custom_name: str = "", supply_chain: Optional[MockSupplyChain] = None) -> Dict[str, Any]:
        if archetype_type not in self.agent_archetypes:
            return {"success": False, "reason": "Unknown agent archetype"}
        arch = self.agent_archetypes[archetype_type]
        cost = arch["cost_gold"]
        if supply_chain:
            if supply_chain.get_resource("gold_coins") < cost:
                return {"success": False, "reason": f"Insufficient gold (Requires {cost} Gold)"}
            supply_chain.consume_resource("gold_coins", cost)

        agent_id = f"agent_{len(self.recruited_agents) + 1}"
        final_name = agent_custom_name or f"{arch['name']} of the Shadow"
        agent = {
            "id": agent_id,
            "name": final_name,
            "type": archetype_type,
            "stationed_realm": "domestic_citadel",
            "status": "Ready",
            "experience": 0,
            "stealth_rating": 50.0 + (arch.get("stealth_bonus", 0.0) * 100.0),
            "sabotage_rating": 40.0 + (arch.get("sabotage_bonus", 0.0) * 100.0)
        }
        self.recruited_agents[agent_id] = agent
        self.citadel_security_rating = min(100.0, self.citadel_security_rating + 5.0)
        self.signal_log.append(("agent_recruited", agent_id, final_name, archetype_type))
        return {"success": True, "agent": agent}

    def launch_operation(self, op_id: str, target_realm: str, agent_id: str, supply_chain: Optional[MockSupplyChain] = None) -> Dict[str, Any]:
        if op_id not in self.operations_catalog:
            return {"success": False, "reason": "Unknown covert operation"}
        if agent_id not in self.recruited_agents:
            return {"success": False, "reason": "Agent not found"}

        agent = self.recruited_agents[agent_id]
        if agent["status"] != "Ready":
            return {"success": False, "reason": "Agent is currently busy or unavailable"}

        op_def = self.operations_catalog[op_id]
        cost = op_def["cost_gold"]
        if supply_chain:
            if supply_chain.get_resource("gold_coins") < cost:
                return {"success": False, "reason": f"Insufficient treasury coins (Requires {cost} Gold)"}
            supply_chain.consume_resource("gold_coins", cost)

        agent["status"] = "On Mission"
        agent["stationed_realm"] = target_realm

        op_instance = {
            "instance_id": f"op_inst_{self.total_operations_completed + len(self.active_operations) + 1}",
            "op_id": op_id,
            "target_realm": target_realm,
            "agent_id": agent_id,
            "timer": op_def["duration"],
            "total_duration": op_def["duration"],
            "base_success": op_def["base_success_chance"],
            "risk_capture": op_def["risk_capture"]
        }
        self.active_operations.append(op_instance)
        self.signal_log.append(("operation_launched", op_id, target_realm, agent_id))
        return {"success": True, "operation": op_instance}

    def resolve_operation(self, op: Dict[str, Any], force_success: Optional[bool] = None) -> None:
        self.total_operations_completed += 1
        agent_id = op["agent_id"]
        agent = self.recruited_agents.get(agent_id)

        success_chance = op["base_success"]
        if agent:
            if op["op_id"] == "sabotage_siege_weapons":
                success_chance += (agent.get("sabotage_rating", 40.0) / 200.0)
            else:
                success_chance += (agent.get("stealth_rating", 50.0) / 200.0)

        is_success = force_success if force_success is not None else (0.50 <= success_chance)
        rewards = {}
        desc = ""

        if is_success:
            self.successful_operations_count += 1
            if agent:
                agent["status"] = "Ready"
                agent["experience"] += 25

            if op["op_id"] == "gather_invasion_intel":
                desc = f"Revealed classified war council plans in {op['target_realm'].capitalize()}!"
                rewards = {"intel_accuracy": 1.0, "invasion_revealed": True}
            elif op["op_id"] == "sabotage_siege_weapons":
                desc = f"Saboteurs set fire to siege ram depot in {op['target_realm'].capitalize()}!"
                rewards = {"enemy_siege_penalty": 0.40, "delay_ticks": 60.0}
            elif op["op_id"] == "steal_scholastic_tech":
                desc = f"Stole illuminated parchment treatises from {op['target_realm'].capitalize()} scriptorium!"
                rewards = {"scholar_points": 120.0}
            elif op["op_id"] == "incite_border_revolt":
                desc = f"Peasant revolt ignited in {op['target_realm'].capitalize()}!"
                rewards = {"recruited_guards": 3}
        else:
            if agent:
                agent["status"] = "Captured"
                agent["stationed_realm"] = "foreign_dungeon"
            desc = f"Operation in {op['target_realm'].capitalize()} was compromised!"
            rewards = {"captured": True}

        self.signal_log.append(("operation_resolved", op["op_id"], is_success, desc, rewards))

    def trigger_domestic_counter_intel_check(self, infiltrator_type: str = "assassin") -> Dict[str, Any]:
        thwarted = self.citadel_security_rating >= 40.0
        if thwarted:
            self.plots_thwarted_count += 1
            prisoner = {
                "id": f"prisoner_{len(self.captured_prisoners) + 1}",
                "name": f"Captured {infiltrator_type.capitalize()} from rival realm",
                "interrogated": False,
                "ransom_value": 50
            }
            self.captured_prisoners.append(prisoner)
            self.signal_log.append(("counter_intel_triggered", f"Foiled {infiltrator_type.capitalize()} plot!", True))
            return {"thwarted": True, "prisoner": prisoner}
        else:
            self.court_suspicion = min(100.0, self.court_suspicion + 20.0)
            self.signal_log.append(("counter_intel_triggered", "Enemy infiltrator breached bailey!", False))
            return {"thwarted": False}

    def interrogate_prisoner(self, prisoner_id: str) -> Dict[str, Any]:
        for p in self.captured_prisoners:
            if p["id"] == prisoner_id:
                if p["interrogated"]:
                    return {"success": False, "reason": "Captive has already divulged all their secrets."}
                p["interrogated"] = True
                secrets = "Disclosed concealed spy networks and secret treasury stashes (+75 Gold intelligence)!"
                self.signal_log.append(("prisoner_interrogated", prisoner_id, secrets))
                return {"success": True, "secrets": secrets, "coins_discovered": 75}
        return {"success": False, "reason": "Prisoner not found in citadel dungeons"}

    def ransom_prisoner(self, prisoner_id: str, supply_chain: Optional[MockSupplyChain] = None) -> bool:
        for i, p in enumerate(self.captured_prisoners):
            if p["id"] == prisoner_id:
                val = p["ransom_value"]
                if supply_chain:
                    supply_chain.add_resource("gold_coins", val)
                self.captured_prisoners.pop(i)
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recruited_agents": {k: dict(v) for k, v in self.recruited_agents.items()},
            "active_operations": [dict(op) for op in self.active_operations],
            "captured_prisoners": [dict(p) for p in self.captured_prisoners],
            "citadel_security_rating": self.citadel_security_rating,
            "court_suspicion": self.court_suspicion,
            "total_operations_completed": self.total_operations_completed,
            "successful_operations_count": self.successful_operations_count,
            "plots_thwarted_count": self.plots_thwarted_count
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        if not data:
            return
        self.recruited_agents = data.get("recruited_agents", {})
        self.active_operations = data.get("active_operations", [])
        self.captured_prisoners = data.get("captured_prisoners", [])
        self.citadel_security_rating = data.get("citadel_security_rating", 65.0)
        self.court_suspicion = data.get("court_suspicion", 10.0)
        self.total_operations_completed = data.get("total_operations_completed", 0)
        self.successful_operations_count = data.get("successful_operations_count", 0)
        self.plots_thwarted_count = data.get("plots_thwarted_count", 0)


# ==============================================================================
# Unit Test Cases for Milestone 52
# ==============================================================================
class TestEspionageIntrigueSystems(unittest.TestCase):

    def setUp(self):
        self.em = PythonEspionageManager()
        self.supply = MockSupplyChain()

    def test_initial_espionage_state(self):
        """Verify initial catalog setup, baseline security, and empty rosters."""
        self.assertEqual(len(self.em.agent_archetypes), 3)
        self.assertEqual(len(self.em.operations_catalog), 4)
        self.assertEqual(self.em.citadel_security_rating, 65.0)
        self.assertEqual(len(self.em.recruited_agents), 0)
        self.assertEqual(len(self.em.active_operations), 0)
        self.assertEqual(len(self.em.captured_prisoners), 0)

    def test_archetypes_catalog_attributes(self):
        """Verify all 3 agent archetypes have appropriate costs and bonuses."""
        archs = self.em.agent_archetypes
        self.assertIn("informant", archs)
        self.assertEqual(archs["informant"]["cost_gold"], 30)
        self.assertEqual(archs["informant"]["stealth_bonus"], 0.15)

        self.assertIn("saboteur", archs)
        self.assertEqual(archs["saboteur"]["cost_gold"], 60)
        self.assertEqual(archs["saboteur"]["sabotage_bonus"], 0.35)

        self.assertIn("master_spy", archs)
        self.assertEqual(archs["master_spy"]["cost_gold"], 120)
        self.assertEqual(archs["master_spy"]["intel_bonus"], 0.45)

    def test_operations_catalog_attributes(self):
        """Verify all 4 covert operations have defined durations and risks."""
        ops = self.em.operations_catalog
        self.assertIn("gather_invasion_intel", ops)
        self.assertEqual(ops["gather_invasion_intel"]["cost_gold"], 25)
        self.assertEqual(ops["gather_invasion_intel"]["base_success_chance"], 0.80)

        self.assertIn("sabotage_siege_weapons", ops)
        self.assertEqual(ops["sabotage_siege_weapons"]["cost_gold"], 45)
        self.assertEqual(ops["sabotage_siege_weapons"]["risk_capture"], 0.25)

        self.assertIn("steal_scholastic_tech", ops)
        self.assertEqual(ops["steal_scholastic_tech"]["cost_gold"], 60)

        self.assertIn("incite_border_revolt", ops)
        self.assertEqual(ops["incite_border_revolt"]["cost_gold"], 80)

    def test_recruit_agent_valid(self):
        """Verify recruiting an agent consumes coins, increases security, and emits signal."""
        init_gold = self.supply.get_resource("gold_coins")
        res = self.em.recruit_agent("informant", "Brother Nicholas", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("gold_coins"), init_gold - 30)
        self.assertEqual(self.em.citadel_security_rating, 70.0) # 65 + 5
        self.assertIn("agent_1", self.em.recruited_agents)
        self.assertEqual(self.em.recruited_agents["agent_1"]["name"], "Brother Nicholas")
        self.assertEqual(self.em.signal_log[-1][0], "agent_recruited")

    def test_recruit_agent_insufficient_gold(self):
        """Verify recruitment fails when treasury lacks gold."""
        self.supply.resources["gold_coins"] = 10
        res = self.em.recruit_agent("saboteur", "", self.supply)
        self.assertFalse(res["success"])
        self.assertIn("Insufficient gold", res["reason"])
        self.assertEqual(len(self.em.recruited_agents), 0)

    def test_recruit_unknown_archetype(self):
        """Verify error on nonexistent agent archetype."""
        res = self.em.recruit_agent("ninja", "", self.supply)
        self.assertFalse(res["success"])
        self.assertEqual(res["reason"], "Unknown agent archetype")

    def test_launch_operation_success(self):
        """Verify launching operation transitions agent to On Mission and creates active op."""
        self.em.recruit_agent("informant", "Sylvia", self.supply)
        init_gold = self.supply.get_resource("gold_coins")

        res = self.em.launch_operation("gather_invasion_intel", "ashfell", "agent_1", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("gold_coins"), init_gold - 25)
        self.assertEqual(self.em.recruited_agents["agent_1"]["status"], "On Mission")
        self.assertEqual(self.em.recruited_agents["agent_1"]["stationed_realm"], "ashfell")
        self.assertEqual(len(self.em.active_operations), 1)
        self.assertEqual(self.em.signal_log[-1][0], "operation_launched")

    def test_launch_operation_busy_agent(self):
        """Verify busy agent cannot be dispatched on another mission simultaneously."""
        self.em.recruit_agent("informant", "Sylvia", self.supply)
        self.em.launch_operation("gather_invasion_intel", "ashfell", "agent_1", self.supply)

        # Attempt second launch with same agent
        res = self.em.launch_operation("sabotage_siege_weapons", "valoria", "agent_1", self.supply)
        self.assertFalse(res["success"])
        self.assertIn("busy or unavailable", res["reason"])

    def test_launch_operation_insufficient_gold(self):
        """Verify launching fails when treasury cannot afford operation expenses."""
        self.em.recruit_agent("informant", "Sylvia", self.supply)
        self.supply.resources["gold_coins"] = 10
        res = self.em.launch_operation("sabotage_siege_weapons", "ashfell", "agent_1", self.supply)
        self.assertFalse(res["success"])
        self.assertIn("Insufficient treasury coins", res["reason"])

    def test_process_operation_timer_decay(self):
        """Verify delta processing advances active operation timer and triggers resolution."""
        self.em.recruit_agent("informant", "Sylvia", self.supply)
        self.em.launch_operation("gather_invasion_intel", "ashfell", "agent_1", self.supply)

        # 45s total duration
        self.em.process(20.0)
        self.assertEqual(len(self.em.active_operations), 1)
        self.assertAlmostEqual(self.em.active_operations[0]["timer"], 25.0)

        # Advance remaining 30s -> triggers resolution
        self.em.process(30.0)
        self.assertEqual(len(self.em.active_operations), 0)
        self.assertEqual(self.em.total_operations_completed, 1)

    def test_resolve_gather_invasion_intel_success(self):
        """Verify resolution of invasion intel operation returns accurate battle plan."""
        self.em.recruit_agent("informant", "Sylvia")
        op = {
            "instance_id": "op_1",
            "op_id": "gather_invasion_intel",
            "target_realm": "ashfell",
            "agent_id": "agent_1",
            "base_success": 0.80
        }
        self.em.resolve_operation(op, force_success=True)
        self.assertEqual(self.em.successful_operations_count, 1)
        self.assertEqual(self.em.recruited_agents["agent_1"]["status"], "Ready")
        self.assertEqual(self.em.recruited_agents["agent_1"]["experience"], 25)
        last_sig = self.em.signal_log[-1]
        self.assertEqual(last_sig[0], "operation_resolved")
        self.assertTrue(last_sig[2]) # success
        self.assertTrue(last_sig[4]["invasion_revealed"])

    def test_resolve_sabotage_siege_weapons_success(self):
        """Verify sabotage yields 40% enemy siege weapon penalty and march delay."""
        self.em.recruit_agent("saboteur", "Vance the Sapper")
        op = {
            "instance_id": "op_2",
            "op_id": "sabotage_siege_weapons",
            "target_realm": "valoria",
            "agent_id": "agent_1",
            "base_success": 0.65
        }
        self.em.resolve_operation(op, force_success=True)
        last_sig = self.em.signal_log[-1]
        self.assertEqual(last_sig[4]["enemy_siege_penalty"], 0.40)
        self.assertEqual(last_sig[4]["delay_ticks"], 60.0)

    def test_resolve_steal_scholastic_tech_success(self):
        """Verify stealing tech yields 120 scholar research points."""
        self.em.recruit_agent("master_spy", "Lady Cecily")
        op = {
            "instance_id": "op_3",
            "op_id": "steal_scholastic_tech",
            "target_realm": "silvercoast",
            "agent_id": "agent_1",
            "base_success": 0.60
        }
        self.em.resolve_operation(op, force_success=True)
        last_sig = self.em.signal_log[-1]
        self.assertEqual(last_sig[4]["scholar_points"], 120.0)

    def test_resolve_incite_border_revolt_success(self):
        """Verify inciting revolt recruits 3 deserter guards to the realm."""
        self.em.recruit_agent("master_spy", "Lady Cecily")
        op = {
            "instance_id": "op_4",
            "op_id": "incite_border_revolt",
            "target_realm": "ashfell",
            "agent_id": "agent_1",
            "base_success": 0.55
        }
        self.em.resolve_operation(op, force_success=True)
        last_sig = self.em.signal_log[-1]
        self.assertEqual(last_sig[4]["recruited_guards"], 3)

    def test_resolve_operation_failure_and_capture(self):
        """Verify failure marks agent as Captured in foreign dungeon."""
        self.em.recruit_agent("informant", "Sylvia")
        op = {
            "instance_id": "op_5",
            "op_id": "gather_invasion_intel",
            "target_realm": "ashfell",
            "agent_id": "agent_1",
            "base_success": 0.20
        }
        self.em.resolve_operation(op, force_success=False)
        self.assertEqual(self.em.recruited_agents["agent_1"]["status"], "Captured")
        self.assertEqual(self.em.recruited_agents["agent_1"]["stationed_realm"], "foreign_dungeon")
        last_sig = self.em.signal_log[-1]
        self.assertFalse(last_sig[2]) # success is False
        self.assertTrue(last_sig[4]["captured"])

    def test_domestic_counter_intel_success(self):
        """Verify high security rating thwarts enemy infiltration and captures prisoner."""
        self.em.citadel_security_rating = 65.0
        res = self.em.trigger_domestic_counter_intel_check("assassin")
        self.assertTrue(res["thwarted"])
        self.assertEqual(self.em.plots_thwarted_count, 1)
        self.assertEqual(len(self.em.captured_prisoners), 1)
        self.assertEqual(self.em.captured_prisoners[0]["name"], "Captured Assassin from rival realm")

    def test_domestic_counter_intel_failure(self):
        """Verify low security rating fails to thwart threat and raises court suspicion."""
        self.em.citadel_security_rating = 20.0
        init_suspicion = self.em.court_suspicion
        res = self.em.trigger_domestic_counter_intel_check("arsonist")
        self.assertFalse(res["thwarted"])
        self.assertEqual(self.em.court_suspicion, init_suspicion + 20.0)

    def test_interrogate_prisoner_success(self):
        """Verify interrogation reveals concealed gold and marks prisoner interrogated."""
        self.em.trigger_domestic_counter_intel_check("infiltrator")
        p_id = self.em.captured_prisoners[0]["id"]

        res = self.em.interrogate_prisoner(p_id)
        self.assertTrue(res["success"])
        self.assertEqual(res["coins_discovered"], 75)
        self.assertTrue(self.em.captured_prisoners[0]["interrogated"])
        self.assertEqual(self.em.signal_log[-1][0], "prisoner_interrogated")

    def test_cannot_re_interrogate_prisoner(self):
        """Verify second interrogation attempt fails gracefully."""
        self.em.trigger_domestic_counter_intel_check("infiltrator")
        p_id = self.em.captured_prisoners[0]["id"]
        self.em.interrogate_prisoner(p_id)

        res2 = self.em.interrogate_prisoner(p_id)
        self.assertFalse(res2["success"])
        self.assertIn("already divulged", res2["reason"])

    def test_ransom_prisoner_payout(self):
        """Verify ransoming prisoner removes them from cells and pays ransom into supply chain."""
        self.em.trigger_domestic_counter_intel_check("infiltrator")
        p_id = self.em.captured_prisoners[0]["id"]
        init_gold = self.supply.get_resource("gold_coins")

        ok = self.em.ransom_prisoner(p_id, self.supply)
        self.assertTrue(ok)
        self.assertEqual(len(self.em.captured_prisoners), 0)
        self.assertEqual(self.supply.get_resource("gold_coins"), init_gold + 50)

    def test_save_load_espionage_persistence(self):
        """Verify shadow network agents, operations, and security rating survive roundtrip."""
        self.em.recruit_agent("master_spy", "Countess Vespera", self.supply)
        self.em.launch_operation("gather_invasion_intel", "valoria", "agent_1", self.supply)
        self.em.trigger_domestic_counter_intel_check("saboteur")
        self.em.interrogate_prisoner("prisoner_1")

        saved = self.em.to_dict()
        serialized = json.dumps(saved)
        checksum = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        self.assertEqual(len(checksum), 64)

        restored = PythonEspionageManager()
        restored.from_dict(json.loads(serialized))

        self.assertIn("agent_1", restored.recruited_agents)
        self.assertEqual(restored.recruited_agents["agent_1"]["name"], "Countess Vespera")
        self.assertEqual(restored.recruited_agents["agent_1"]["status"], "On Mission")
        self.assertEqual(len(restored.active_operations), 1)
        self.assertEqual(len(restored.captured_prisoners), 1)
        self.assertTrue(restored.captured_prisoners[0]["interrogated"])
        self.assertEqual(restored.plots_thwarted_count, 1)

    def test_stealth_rating_bonus_calculation(self):
        """Verify stealth and sabotage bonuses correctly populate agent attributes."""
        res = self.em.recruit_agent("master_spy", "Grand Inquisitor", self.supply)
        agent = res["agent"]
        self.assertEqual(agent["stealth_rating"], 50.0)
        self.assertEqual(agent["sabotage_rating"], 40.0)

    def test_ransom_invalid_prisoner_returns_false(self):
        """Verify attempting to ransom non-existent prisoner returns False."""
        self.assertFalse(self.em.ransom_prisoner("invalid_id", self.supply))

    def test_multiple_agents_concurrent_ops(self):
        """Verify multiple agents can execute concurrent operations in different realms."""
        self.em.recruit_agent("informant", "Agent A", self.supply)
        self.em.recruit_agent("saboteur", "Agent B", self.supply)
        res1 = self.em.launch_operation("gather_invasion_intel", "valoria", "agent_1", self.supply)
        res2 = self.em.launch_operation("sabotage_siege_weapons", "ashfell", "agent_2", self.supply)
        self.assertTrue(res1["success"])
        self.assertTrue(res2["success"])
        self.assertEqual(len(self.em.active_operations), 2)

    def test_agent_experience_promotion(self):
        """Verify multiple successful operations accumulate experience on the agent."""
        self.em.recruit_agent("informant", "Sylvia")
        op = {
            "instance_id": "op_test",
            "op_id": "gather_invasion_intel",
            "target_realm": "ashfell",
            "agent_id": "agent_1",
            "base_success": 0.90
        }
        self.em.resolve_operation(op, force_success=True)
        self.em.resolve_operation(op, force_success=True)
        self.assertEqual(self.em.recruited_agents["agent_1"]["experience"], 50)

    def test_all_four_operations_catalog_present(self):
        """Verify completeness of covert operations catalog."""
        cat = self.em.operations_catalog
        expected = ["gather_invasion_intel", "sabotage_siege_weapons", "steal_scholastic_tech", "incite_border_revolt"]
        for exp in expected:
            self.assertIn(exp, cat)
            self.assertGreater(cat[exp]["cost_gold"], 0)
            self.assertGreater(cat[exp]["duration"], 0.0)


if __name__ == "__main__":
    unittest.main()
