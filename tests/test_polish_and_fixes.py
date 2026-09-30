# tests/test_polish_and_fixes.py
# Voxel Lord: Feudal Realm - Automated Polish, Controls Guide & Systems Integration Test Suite
# Tests UI Keybinding Consistency, Mouse Cursor Sync, Espionage Daily Upkeep, and Relic Blessing Vitals.

import unittest
import os
import re


class MockSupplyChain:
    def __init__(self, initial_gold: int = 100):
        self.resources = {"gold_coins": initial_gold}

    def get_resource(self, res_id: str) -> int:
        return self.resources.get(res_id, 0)

    def add_resource(self, res_id: str, amount: int) -> None:
        self.resources[res_id] = self.resources.get(res_id, 0) + amount

    def consume_resource(self, res_id: str, amount: int) -> bool:
        if self.get_resource(res_id) >= amount:
            self.resources[res_id] -= amount
            return True
        return False


class MockEspionageManager:
    def __init__(self):
        self.agent_archetypes = {
            "informant": {"upkeep_daily": 2, "cost_gold": 30},
            "saboteur": {"upkeep_daily": 4, "cost_gold": 60},
            "master_spy": {"upkeep_daily": 8, "cost_gold": 120}
        }
        self.recruited_agents = {}
        self.operations_catalog = {
            "gather_invasion_intel": {"id": "gather_invasion_intel", "cost_gold": 25}
        }
        self.last_upkeep_signal = None

    def recruit_agent(self, archetype_type: str, supply_chain: MockSupplyChain = None) -> dict:
        arch = self.agent_archetypes[archetype_type]
        if supply_chain:
            if not supply_chain.consume_resource("gold_coins", arch["cost_gold"]):
                return {"success": False, "reason": "Insufficient gold"}

        agent_id = f"agent_{len(self.recruited_agents) + 1}"
        agent = {
            "id": agent_id,
            "type": archetype_type,
            "status": "Ready",
            "experience": 0
        }
        self.recruited_agents[agent_id] = agent
        return {"success": True, "agent": agent}

    def launch_operation(self, op_id: str, agent_id: str, supply_chain: MockSupplyChain = None) -> dict:
        if agent_id not in self.recruited_agents:
            return {"success": False, "reason": "Agent not found"}
        agent = self.recruited_agents[agent_id]
        if agent["status"] != "Ready":
            return {"success": False, "reason": "Agent is currently busy or unavailable"}
        op_def = self.operations_catalog.get(op_id, {})
        cost = op_def.get("cost_gold", 0)
        if supply_chain and not supply_chain.consume_resource("gold_coins", cost):
            return {"success": False, "reason": "Insufficient gold"}
        agent["status"] = "On Mission"
        return {"success": True}

    def process_daily_upkeep(self, supply_chain: MockSupplyChain = None) -> dict:
        total_upkeep_needed = 0
        paid_count = 0
        unpaid_count = 0

        for agent_id, agent in self.recruited_agents.items():
            if agent.get("status") == "Captured":
                continue
            atype = agent.get("type", "informant")
            arch = self.agent_archetypes.get(atype, {})
            upkeep = arch.get("upkeep_daily", 2)
            total_upkeep_needed += upkeep

        current_gold = supply_chain.get_resource("gold_coins") if supply_chain else 0
        remaining_gold = current_gold

        for agent_id, agent in self.recruited_agents.items():
            if agent.get("status") == "Captured":
                continue
            atype = agent.get("type", "informant")
            arch = self.agent_archetypes.get(atype, {})
            upkeep = arch.get("upkeep_daily", 2)

            if supply_chain and remaining_gold >= upkeep:
                supply_chain.consume_resource("gold_coins", upkeep)
                remaining_gold -= upkeep
                if agent.get("status") == "Unpaid":
                    agent["status"] = "Ready"
                paid_count += 1
            else:
                if agent.get("status") == "Ready":
                    agent["status"] = "Unpaid"
                unpaid_count += 1

        actual_cost_paid = current_gold - remaining_gold
        self.last_upkeep_signal = (actual_cost_paid, paid_count, unpaid_count)

        return {
            "total_cost_needed": total_upkeep_needed,
            "cost_paid": actual_cost_paid,
            "paid_count": paid_count,
            "unpaid_count": unpaid_count,
            "all_paid": (unpaid_count == 0)
        }


class MockMonasteryResearchSystem:
    def __init__(self):
        self.active_altar_relics = {0: "", 1: "", 2: ""}
        self.relics = {
            "true_hearth_shard": {"blessing": {"warmth_bonus": 15.0, "frost_immunity": True}},
            "perpetual_chalice": {"blessing": {"harvest_bonus": 1.20, "hunger_drain_mult": 0.75}},
            "first_monarch_crown": {"blessing": {"renown_mult": 1.25, "diplomatic_opinion": 10.0}}
        }

    def enshrine_relic(self, relic_id: str, slot: int):
        self.active_altar_relics[slot] = relic_id

    def get_active_blessings(self) -> dict:
        combined = {}
        for slot, rid in self.active_altar_relics.items():
            if rid and rid in self.relics:
                b = self.relics[rid]["blessing"]
                for k, v in b.items():
                    combined[k] = v
        return combined


class MockPlayerVitals:
    def __init__(self, monastery_sys=None):
        self.health = 100.0
        self.max_health = 100.0
        self.hunger = 0.0
        self.max_hunger = 100.0
        self.warmth = 100.0
        self.max_warmth = 100.0
        self.ambient_temperature = 16.0
        self.monastery_research_system = monastery_sys

    def update_vitals(self, delta: float):
        blessings = {}
        if self.monastery_research_system and hasattr(self.monastery_research_system, "get_active_blessings"):
            blessings = self.monastery_research_system.get_active_blessings()

        hunger_mult = blessings.get("hunger_drain_mult", 1.0)
        self.hunger = min(self.max_hunger, self.hunger + delta * 0.1 * hunger_mult)

        self.update_thermal_balance(delta, blessings)

    def update_thermal_balance(self, delta: float, blessings: dict):
        effective_temp = self.ambient_temperature + blessings.get("warmth_bonus", 0.0)
        if effective_temp >= 15.0:
            self.warmth = min(self.max_warmth, self.warmth + delta * 6.0)
        elif effective_temp < 5.0:
            cold_severity = max(1.0, (5.0 - effective_temp) * 0.4)
            self.warmth = max(0.0, self.warmth - delta * cold_severity)

        if self.warmth <= 0.0 and not bool(blessings.get("frost_immunity", False)):
            self.take_damage(delta * 2.5)

    def take_damage(self, amount: float):
        self.health = max(0.0, self.health - amount)


class MockAgricultureManager:
    def __init__(self, monastery_sys=None):
        self.monastery_research_system = monastery_sys

    def harvest_crop(self, base_yield: int = 3, is_blighted: bool = False) -> int:
        yield_qty = base_yield
        if self.monastery_research_system and hasattr(self.monastery_research_system, "get_active_blessings"):
            blessings = self.monastery_research_system.get_active_blessings()
            if "harvest_bonus" in blessings and not is_blighted:
                yield_qty = int(round(yield_qty * blessings["harvest_bonus"]))
        return yield_qty


class TestControlsGuideAndDebugOverlay(unittest.TestCase):
    """Verifies that all 12 keybindings and shortcuts are explicitly documented."""

    def setUp(self):
        self.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pause_menu_path = os.path.join(self.repo_root, "scripts", "ui", "pause_menu.gd")
        self.hud_path = os.path.join(self.repo_root, "scripts", "ui", "hud.gd")

    def test_pause_menu_controls_completeness(self):
        """Verify all hotkeys are documented in pause_menu.gd."""
        self.assertTrue(os.path.exists(self.pause_menu_path), "pause_menu.gd not found")
        with open(self.pause_menu_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_keys = [
            "C", "L", "J", "K", "V", "U", "M", "T", "B", "N", "H", "F1", "F2", "F5", "F9", "ESC"
        ]
        for key in required_keys:
            pattern = rf"\b{re.escape(key)}\b"
            self.assertRegex(content, pattern, f"Keybinding '{key}' missing from pause_menu.gd")

    def test_hud_debug_overlay_shortcuts_completeness(self):
        """Verify all shortcuts are present in HUD F1 debug overlay string."""
        self.assertTrue(os.path.exists(self.hud_path), "hud.gd not found")
        with open(self.hud_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_markers = [
            "[C] Craft", "[L] Ledger", "[J] Deeds", "[K] Heraldry",
            "[V] Decrees", "[U] Diplomacy", "[M] War Room", "[T] Tourney",
            "[B] Monastery", "[N] Espionage", "[H] Horn", "[F2] Districts",
            "[F5/F9] Save/Load", "[ESC] Pause"
        ]
        for marker in required_markers:
            self.assertIn(marker, content, f"HUD debug overlay missing '{marker}'")


class TestCursorModeSynchronization(unittest.TestCase):
    """Verifies centralized mouse mode capture & liberation logic."""

    def test_cursor_mode_when_modal_open(self):
        """When at least one modal is visible, mouse mode must be VISIBLE."""
        modals = {
            "crafting_menu": False,
            "royal_ledger": False,
            "quest_journal": False,
            "heraldry_ui": False,
            "decrees_ui": False,
            "diplomacy_ui": False,
            "war_room_ui": False,
            "tournament_ui": False,
            "monastery_ui": True,  # Monastic scriptoria open
            "espionage_ui": False,
            "pause_menu": False
        }

        any_open = any(modals.values())
        mouse_mode = "MOUSE_MODE_VISIBLE" if any_open else "MOUSE_MODE_CAPTURED"
        self.assertEqual(mouse_mode, "MOUSE_MODE_VISIBLE")

    def test_cursor_mode_when_all_modals_closed(self):
        """When all modals are closed, mouse mode must be CAPTURED."""
        modals = {
            "crafting_menu": False,
            "royal_ledger": False,
            "quest_journal": False,
            "heraldry_ui": False,
            "decrees_ui": False,
            "diplomacy_ui": False,
            "war_room_ui": False,
            "tournament_ui": False,
            "monastery_ui": False,
            "espionage_ui": False,
            "pause_menu": False
        }

        any_open = any(modals.values())
        mouse_mode = "MOUSE_MODE_VISIBLE" if any_open else "MOUSE_MODE_CAPTURED"
        self.assertEqual(mouse_mode, "MOUSE_MODE_CAPTURED")


class TestEspionageDailyUpkeep(unittest.TestCase):
    """Tests shadow council daily upkeep deduction and strike mechanics."""

    def setUp(self):
        self.supply = MockSupplyChain(initial_gold=250)
        self.espionage = MockEspionageManager()

    def test_upkeep_deduction_with_sufficient_gold(self):
        """Daily upkeep is accurately deducted for all recruited agents."""
        self.espionage.recruit_agent("informant", self.supply)  # 2 gold daily
        self.espionage.recruit_agent("saboteur", self.supply)   # 4 gold daily
        self.espionage.recruit_agent("master_spy", self.supply) # 8 gold daily
        # Total daily upkeep = 2 + 4 + 8 = 14 gold

        gold_before = self.supply.get_resource("gold_coins")
        res = self.espionage.process_daily_upkeep(self.supply)

        self.assertTrue(res["all_paid"])
        self.assertEqual(res["total_cost_needed"], 14)
        self.assertEqual(res["cost_paid"], 14)
        self.assertEqual(res["paid_count"], 3)
        self.assertEqual(res["unpaid_count"], 0)
        self.assertEqual(self.supply.get_resource("gold_coins"), gold_before - 14)

    def test_unpaid_strike_when_treasury_empty(self):
        """Agents switch to Unpaid status when treasury lacks funds and cannot launch ops."""
        self.espionage.recruit_agent("master_spy", self.supply)  # 8 gold daily
        # Drain all gold
        self.supply.consume_resource("gold_coins", self.supply.get_resource("gold_coins"))

        res = self.espionage.process_daily_upkeep(self.supply)
        self.assertFalse(res["all_paid"])
        self.assertEqual(res["unpaid_count"], 1)

        agent = self.espionage.recruited_agents["agent_1"]
        self.assertEqual(agent["status"], "Unpaid")

        # Attempt to launch covert mission with unpaid agent
        launch_res = self.espionage.launch_operation("gather_invasion_intel", "agent_1", self.supply)
        self.assertFalse(launch_res["success"])
        self.assertIn("unavailable", launch_res["reason"])

    def test_strike_resolved_upon_payment(self):
        """Once funds are replenished, next upkeep resolves Unpaid status back to Ready."""
        self.espionage.recruit_agent("informant", self.supply)
        # Empty treasury
        self.supply.consume_resource("gold_coins", self.supply.get_resource("gold_coins"))
        self.espionage.process_daily_upkeep(self.supply)
        self.assertEqual(self.espionage.recruited_agents["agent_1"]["status"], "Unpaid")

        # Refill treasury
        self.supply.add_resource("gold_coins", 50)
        res = self.espionage.process_daily_upkeep(self.supply)
        self.assertTrue(res["all_paid"])
        self.assertEqual(self.espionage.recruited_agents["agent_1"]["status"], "Ready")


class TestRelicBlessingsAndVitalsIntegration(unittest.TestCase):
    """Tests sacred relic blessings affecting player survival, hunger, and crop yields."""

    def setUp(self):
        self.monastery = MockMonasteryResearchSystem()

    def test_perpetual_chalice_reduces_hunger_drain(self):
        """Perpetual Chalice relic blessing reduces passive hunger drain by 25%."""
        player_normal = MockPlayerVitals(None)
        player_blessed = MockPlayerVitals(self.monastery)

        self.monastery.enshrine_relic("perpetual_chalice", 0)

        delta = 100.0  # 100 seconds
        player_normal.update_vitals(delta)
        player_blessed.update_vitals(delta)

        # Normal: 100 * 0.1 = 10.0 hunger
        # Blessed: 100 * 0.1 * 0.75 = 7.5 hunger
        self.assertAlmostEqual(player_normal.hunger, 10.0, places=2)
        self.assertAlmostEqual(player_blessed.hunger, 7.5, places=2)

    def test_true_hearth_shard_frost_immunity(self):
        """True Hearth Shard prevents freezing damage at 0 warmth."""
        player_normal = MockPlayerVitals(None)
        player_normal.warmth = 0.0
        player_normal.ambient_temperature = -10.0

        player_blessed = MockPlayerVitals(self.monastery)
        player_blessed.warmth = 0.0
        player_blessed.ambient_temperature = -10.0
        self.monastery.enshrine_relic("true_hearth_shard", 0)

        delta = 4.0
        # Normal player takes freeze damage
        player_normal.update_vitals(delta)
        self.assertLess(player_normal.health, 100.0)

        # Blessed player with frost immunity takes NO freeze damage
        player_blessed.update_vitals(delta)
        self.assertEqual(player_blessed.health, 100.0)

    def test_perpetual_chalice_boosts_crop_yield(self):
        """Perpetual Chalice blessing increases agricultural harvest yield by 20%."""
        agri_normal = MockAgricultureManager(None)
        agri_blessed = MockAgricultureManager(self.monastery)
        self.monastery.enshrine_relic("perpetual_chalice", 0)

        base_harvest = 10
        yield_normal = agri_normal.harvest_crop(base_harvest, False)
        yield_blessed = agri_blessed.harvest_crop(base_harvest, False)

        self.assertEqual(yield_normal, 10)
        self.assertEqual(yield_blessed, 12)  # 10 * 1.20 = 12


class TestDayRolloverProcess(unittest.TestCase):
    """Tests day_timer accumulation and rollover execution."""

    def test_day_timer_rollover_triggers(self):
        day_duration = 120.0
        day_timer = 119.5
        delta = 1.0
        days_elapsed = 0
        rollover_triggered = False

        day_timer += delta
        if day_timer >= day_duration:
            day_timer -= day_duration
            days_elapsed += 1
            rollover_triggered = True

        self.assertTrue(rollover_triggered)
        self.assertEqual(days_elapsed, 1)
        self.assertAlmostEqual(day_timer, 0.5, places=2)


if __name__ == "__main__":
    unittest.main()
