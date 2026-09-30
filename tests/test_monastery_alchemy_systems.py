#!/usr/bin/env python3
"""
Unit Test Suite for Milestone 51: Monastic Scriptoria, Alchemical Laboratory, Holy Relics, and Abbey UI
Author: Voxel Lord Engineering Team
Tests high scholastic research tech tree, illuminated manuscript progression, sacred relic enshrinement,
abbey bell liturgy, alchemical elixir brewing, crucible metal transmutations, Magnum Opus philosopher's stone,
and persistence roundtrip integrity.
"""

import unittest
import hashlib
import json
from typing import Dict, Any, List, Optional


class MockSupplyChain:
    """Mock supply chain tracking resources for alchemy distillations and transmutations."""
    def __init__(self):
        self.resources: Dict[str, int] = {
            "rock_salt": 50,
            "bread": 30,
            "iron_ore": 40,
            "iron_ingots": 30,
            "coal": 80,
            "wheat": 50,
            "stone": 100,
            "wood": 100,
            "gold_coins": 200,
            "silver_ore": 0,
            "gems": 0
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


class PythonMonasteryResearchSystem:
    """Python mirror of scripts/core/monastery_research_system.gd."""

    BELL_BLESSING_DURATION: float = 180.0

    def __init__(self):
        self.technologies: Dict[str, Dict[str, Any]] = {}
        self.relics: Dict[str, Dict[str, Any]] = {}
        self.scholar_points: float = 0.0
        self.assigned_monk_scribes: int = 3
        self.current_research_id: str = ""
        self.research_progress: Dict[str, float] = {}
        self.unlocked_techs: List[str] = []
        self.active_altar_relics: Dict[int, str] = {0: "", 1: "", 2: ""}
        self.discovered_relics: List[str] = ["true_hearth_shard", "st_columba_tome", "perpetual_chalice"]
        self.bell_blessing_active: bool = False
        self.bell_blessing_timer: float = 0.0
        self.signal_log: List[tuple] = []
        self.init_technologies()
        self.init_relics()

    def init_technologies(self):
        self.technologies = {
            "norfolk_genetics": {
                "id": "norfolk_genetics",
                "name": "Norfolk Four-Course Agronomy Genetics",
                "cost": 100,
                "desc": "+25% crop growth velocity, +15% soil nitrogen & phosphorus retention.",
                "icon": "🌾",
                "effects": {"crop_growth_mult": 1.25, "soil_retention_mult": 1.15}
            },
            "blast_catalysts": {
                "id": "blast_catalysts",
                "name": "Thermodynamic Blast Furnace Flux Catalysts",
                "cost": 150,
                "desc": "+30% smelting speed, unlocks crucible steel folded blade crafting.",
                "icon": "🔥",
                "effects": {"smelt_speed_mult": 1.30, "crucible_unlocked": True}
            },
            "counterweight_ballistics": {
                "id": "counterweight_ballistics",
                "name": "Gravitational Counterweight Ballistics",
                "cost": 200,
                "desc": "+35% siege weapon damage, increases trebuchet trajectory range to 250m.",
                "icon": "🎯",
                "effects": {"siege_damage_mult": 1.35, "trebuchet_range": 250.0}
            },
            "deep_shaft_geology": {
                "id": "deep_shaft_geology",
                "name": "Deep Subterranean Geological Surveying",
                "cost": 180,
                "desc": "+25% rare gem & silver ore extraction yield from mining shafts.",
                "icon": "💎",
                "effects": {"mining_gem_bonus": 1.25}
            },
            "guild_charters": {
                "id": "guild_charters",
                "name": "Imperial Artisan Guild Charters",
                "cost": 220,
                "desc": "+20% craft batch yield, -15% trading prices with merchant caravans.",
                "icon": "📜",
                "effects": {"craft_yield_mult": 1.20, "trade_discount": 0.15}
            },
            "sacred_architecture": {
                "id": "sacred_architecture",
                "name": "Gothic Monastic Vaulting & Flying Buttresses",
                "cost": 250,
                "desc": "+30% structural integrity load threshold before ceiling collapse.",
                "icon": "🏛️",
                "effects": {"structural_load_mult": 1.30}
            }
        }

    def init_relics(self):
        self.relics = {
            "true_hearth_shard": {
                "id": "true_hearth_shard",
                "name": "Shard of the True Hearth",
                "desc": "Spiritual ember of the ancient founding hearth.",
                "icon": "🔥",
                "blessing": {"warmth_bonus": 15.0, "frost_immunity": True}
            },
            "first_monarch_crown": {
                "id": "first_monarch_crown",
                "name": "Crown of the First Sovereign",
                "desc": "Golden circlet worn by the kingdom's founder.",
                "icon": "👑",
                "blessing": {"renown_mult": 1.25, "diplomatic_opinion": 10.0}
            },
            "st_columba_tome": {
                "id": "st_columba_tome",
                "name": "Tome of St. Columba",
                "desc": "Sacred illuminated parchment.",
                "icon": "📖",
                "blessing": {"research_speed_mult": 1.40}
            },
            "perpetual_chalice": {
                "id": "perpetual_chalice",
                "name": "Chalice of Perpetual Abundance",
                "desc": "Holy vessel sanctifying water and wheat.",
                "icon": "🏆",
                "blessing": {"harvest_bonus": 1.20, "hunger_drain_mult": 0.75}
            },
            "holy_light_banner": {
                "id": "holy_light_banner",
                "name": "Banner of the Holy Light",
                "desc": "Consecrated silver silk standard.",
                "icon": "🚩",
                "blessing": {"garrison_morale_bonus": 20.0, "raid_suppression": 0.30}
            }
        }

    def process(self, delta: float) -> None:
        if self.assigned_monk_scribes > 0 and self.current_research_id != "":
            speed_mult = 1.0
            for slot in self.active_altar_relics.values():
                if slot == "st_columba_tome":
                    speed_mult *= 1.40
            points = (self.assigned_monk_scribes * 0.75 * speed_mult) * delta
            self.add_research_progress(points)

        if self.bell_blessing_active:
            self.bell_blessing_timer -= delta
            if self.bell_blessing_timer <= 0.0:
                self.bell_blessing_active = False

    def start_research(self, tech_id: str) -> bool:
        if tech_id not in self.technologies or tech_id in self.unlocked_techs:
            return False
        self.current_research_id = tech_id
        if tech_id not in self.research_progress:
            self.research_progress[tech_id] = 0.0
        tech = self.technologies[tech_id]
        self.signal_log.append(("research_started", tech_id, tech["name"], tech["cost"]))
        return True

    def add_research_progress(self, points: float) -> None:
        if not self.current_research_id:
            self.scholar_points += points
            return
        tech = self.technologies.get(self.current_research_id)
        if not tech:
            return
        cur = self.research_progress.get(self.current_research_id, 0.0) + points
        cost = float(tech["cost"])
        if cur >= cost:
            self.research_progress[self.current_research_id] = cost
            self.unlocked_techs.append(self.current_research_id)
            completed_id = self.current_research_id
            self.current_research_id = ""
            self.signal_log.append(("research_completed", completed_id, tech["name"]))
        else:
            self.research_progress[self.current_research_id] = cur
            self.signal_log.append(("research_progress_updated", self.current_research_id, cur, cost))

    def is_tech_unlocked(self, tech_id: str) -> bool:
        return tech_id in self.unlocked_techs

    def assign_monks(self, delta_count: int) -> int:
        self.assigned_monk_scribes = max(0, min(10, self.assigned_monk_scribes + delta_count))
        return self.assigned_monk_scribes

    def enshrine_relic(self, slot_index: int, relic_id: str) -> bool:
        if slot_index < 0 or slot_index > 2:
            return False
        if relic_id not in self.relics or relic_id not in self.discovered_relics:
            return False
        for s, r in list(self.active_altar_relics.items()):
            if r == relic_id:
                self.active_altar_relics[s] = ""
        self.active_altar_relics[slot_index] = relic_id
        r = self.relics[relic_id]
        self.signal_log.append(("relic_enshrined", relic_id, r["name"], slot_index))
        return True

    def remove_relic(self, slot_index: int) -> bool:
        if slot_index < 0 or slot_index > 2:
            return False
        old = self.active_altar_relics.get(slot_index, "")
        if old != "":
            self.active_altar_relics[slot_index] = ""
            self.signal_log.append(("relic_removed", old, slot_index))
            return True
        return False

    def ring_abbey_bells(self) -> Dict[str, Any]:
        self.bell_blessing_active = True
        self.bell_blessing_timer = self.BELL_BLESSING_DURATION
        self.signal_log.append(("abbey_bell_rung", "Grace of the High Abbey (+30% Citizen Serenity)"))
        return {
            "success": True,
            "duration": self.BELL_BLESSING_DURATION,
            "morale_boost": 30.0
        }

    def get_active_blessings(self) -> Dict[str, Any]:
        combined = {}
        for rid in self.active_altar_relics.values():
            if rid and rid in self.relics:
                b = self.relics[rid]["blessing"]
                for k, v in b.items():
                    combined[k] = v
        if self.bell_blessing_active:
            combined["abbey_bell_serenity"] = 30.0
        return combined

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scholar_points": self.scholar_points,
            "assigned_monk_scribes": self.assigned_monk_scribes,
            "current_research_id": self.current_research_id,
            "research_progress": dict(self.research_progress),
            "unlocked_techs": list(self.unlocked_techs),
            "active_altar_relics": {str(k): v for k, v in self.active_altar_relics.items()},
            "discovered_relics": list(self.discovered_relics),
            "bell_blessing_active": self.bell_blessing_active,
            "bell_blessing_timer": self.bell_blessing_timer
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        if not data:
            return
        self.scholar_points = data.get("scholar_points", 0.0)
        self.assigned_monk_scribes = data.get("assigned_monk_scribes", 3)
        self.current_research_id = data.get("current_research_id", "")
        self.research_progress = data.get("research_progress", {})
        self.unlocked_techs = data.get("unlocked_techs", [])
        raw_altar = data.get("active_altar_relics", {})
        self.active_altar_relics = {int(k): v for k, v in raw_altar.items()}
        self.discovered_relics = data.get("discovered_relics", ["true_hearth_shard"])
        self.bell_blessing_active = data.get("bell_blessing_active", False)
        self.bell_blessing_timer = data.get("bell_blessing_timer", 0.0)


class PythonAlchemyLaboratory:
    """Python mirror of scripts/combat/alchemy_laboratory.gd."""

    STONE_STAGES = [
        {"stage": 1, "name": "Nigredo (Black Dissolution)", "bonus_purity": 1.0, "icon": "🌑"},
        {"stage": 2, "name": "Albedo (White Purification)", "bonus_purity": 1.25, "icon": "⚪"},
        {"stage": 3, "name": "Citrinitas (Yellow Awakening)", "bonus_purity": 1.60, "icon": "🟡"},
        {"stage": 4, "name": "Rubedo (Magnum Opus / Red Elixir)", "bonus_purity": 2.20, "icon": "🔴"}
    ]

    def __init__(self):
        self.potion_recipes: Dict[str, Dict[str, Any]] = {}
        self.transmutation_formulas: Dict[str, Dict[str, Any]] = {}
        self.alembic_temperature: float = 85.0
        self.philosophers_stone_stage: int = 1
        self.brewed_potions_count: int = 0
        self.transmutations_count: int = 0
        self.signal_log: List[tuple] = []
        self.init_recipes()
        self.init_transmutations()

    def init_recipes(self):
        self.potion_recipes = {
            "elixir_of_vitality": {
                "id": "elixir_of_vitality",
                "name": "Elixir of Vitality",
                "desc": "Instantly heals 50 HP and accelerates monarch biological recuperation.",
                "ingredients": {"rock_salt": 1, "bread": 1},
                "icon": "🧪",
                "effect_heal": 50.0
            },
            "elixir_of_iron_skin": {
                "id": "elixir_of_iron_skin",
                "name": "Elixir of Iron Skin",
                "desc": "+40% physical armor damage mitigation against bandit & invader blades for 60s.",
                "ingredients": {"iron_ore": 1, "coal": 1},
                "icon": "🛡️",
                "defense_buff": 0.40
            },
            "elixir_of_windstrider": {
                "id": "elixir_of_windstrider",
                "name": "Elixir of the Windstrider",
                "desc": "+35% sprint velocity and zero stamina loss during royal travels for 60s.",
                "ingredients": {"wheat": 2, "rock_salt": 1},
                "icon": "💨",
                "speed_buff": 0.35
            },
            "dragons_breath_flask": {
                "id": "dragons_breath_flask",
                "name": "Dragon's Breath Volatile Flask",
                "desc": "Incendiary alchemical flask inflicting 60 fire AOE damage on enemy formations.",
                "ingredients": {"coal": 2, "rock_salt": 2},
                "icon": "🔥",
                "aoe_damage": 60.0
            }
        }

    def init_transmutations(self):
        self.transmutation_formulas = {
            "lead_to_silver": {
                "id": "lead_to_silver",
                "name": "Baser Ore into Noble Silver",
                "desc": "Calcinates common stone and coal into precious silver ore.",
                "inputs": {"stone": 8, "coal": 4},
                "outputs": {"silver_ore": 2},
                "icon": "🪙"
            },
            "iron_to_gold": {
                "id": "iron_to_gold",
                "name": "Great Magnum Transmutation: Iron into Gold",
                "desc": "Hermetic crucible transmutation of forged iron into glittering gold coins.",
                "inputs": {"iron_ingots": 3, "coal": 4},
                "outputs": {"gold_coins": 25},
                "icon": "👑"
            },
            "salt_into_reagent": {
                "id": "salt_into_reagent",
                "name": "Sublimation of Salt into Philospher's Catalyst",
                "desc": "Refines rock salt into alchemical flux reagent for advanced metallurgy.",
                "inputs": {"rock_salt": 4, "wood": 4},
                "outputs": {"gems": 1},
                "icon": "💎"
            }
        }

    def brew_potion(self, potion_id: str, supply_chain: Optional[MockSupplyChain] = None) -> Dict[str, Any]:
        if potion_id not in self.potion_recipes:
            return {"success": False, "reason": "Unknown potion formula"}
        recipe = self.potion_recipes[potion_id]
        ingredients = recipe["ingredients"]

        if supply_chain:
            for item, req in ingredients.items():
                if supply_chain.get_resource(item) < req:
                    return {"success": False, "reason": f"Missing ingredient: {item} (Requires {req})"}
            for item, req in ingredients.items():
                supply_chain.consume_resource(item, req)

        self.brewed_potions_count += 1
        self.alembic_temperature = min(350.0, self.alembic_temperature + 15.0)
        self.signal_log.append(("alembic_heat_changed", self.alembic_temperature))
        self.signal_log.append(("potion_brewed", potion_id, recipe["name"], 1))

        return {
            "success": True,
            "potion_id": potion_id,
            "name": recipe["name"],
            "effect": recipe
        }

    def transmute_metal(self, formula_id: str, supply_chain: Optional[MockSupplyChain] = None) -> Dict[str, Any]:
        if formula_id not in self.transmutation_formulas:
            return {"success": False, "reason": "Unknown transmutation formula"}
        formula = self.transmutation_formulas[formula_id]
        inputs = formula["inputs"]
        outputs = formula["outputs"]

        if supply_chain:
            for item, req in inputs.items():
                if supply_chain.get_resource(item) < req:
                    return {"success": False, "reason": f"Insufficient {item} (Requires {req})"}
            for item, req in inputs.items():
                supply_chain.consume_resource(item, req)
            for item, prod in outputs.items():
                stage_idx = max(0, min(3, self.philosophers_stone_stage - 1))
                bonus = self.STONE_STAGES[stage_idx]["bonus_purity"]
                final_prod = int(round(prod * bonus))
                supply_chain.add_resource(item, final_prod)

        self.transmutations_count += 1
        self.alembic_temperature = min(400.0, self.alembic_temperature + 25.0)
        self.signal_log.append(("alembic_heat_changed", self.alembic_temperature))
        primary_out = list(outputs.keys())[0]
        self.signal_log.append(("metal_transmuted", formula_id, list(inputs.keys())[0], primary_out, outputs[primary_out]))

        return {
            "success": True,
            "formula_id": formula_id,
            "inputs": inputs,
            "outputs": outputs
        }

    def refine_philosophers_stone(self, supply_chain: Optional[MockSupplyChain] = None) -> Dict[str, Any]:
        if self.philosophers_stone_stage >= 4:
            return {"success": False, "reason": "The Magnum Opus (Rubedo) is already perfected!"}

        gold_cost = 40 * self.philosophers_stone_stage
        salt_cost = 5 * self.philosophers_stone_stage

        if supply_chain:
            if supply_chain.get_resource("gold_coins") < gold_cost:
                return {"success": False, "reason": f"Insufficient gold for sublimation (Requires {gold_cost} Gold)"}
            if supply_chain.get_resource("rock_salt") < salt_cost:
                return {"success": False, "reason": f"Insufficient rock salt (Requires {salt_cost} Salt)"}
            supply_chain.consume_resource("gold_coins", gold_cost)
            supply_chain.consume_resource("rock_salt", salt_cost)

        self.philosophers_stone_stage += 1
        stage_info = self.STONE_STAGES[self.philosophers_stone_stage - 1]
        self.signal_log.append(("philosophers_stone_refined", self.philosophers_stone_stage, stage_info["name"]))

        return {
            "success": True,
            "stage": self.philosophers_stone_stage,
            "stage_name": stage_info["name"],
            "bonus_purity": stage_info["bonus_purity"]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alembic_temperature": self.alembic_temperature,
            "philosophers_stone_stage": self.philosophers_stone_stage,
            "brewed_potions_count": self.brewed_potions_count,
            "transmutations_count": self.transmutations_count
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        if not data:
            return
        self.alembic_temperature = data.get("alembic_temperature", 85.0)
        self.philosophers_stone_stage = data.get("philosophers_stone_stage", 1)
        self.brewed_potions_count = data.get("brewed_potions_count", 0)
        self.transmutations_count = data.get("transmutations_count", 0)


# ==============================================================================
# Unit Test Cases for Milestone 51
# ==============================================================================
class TestMonasteryAndAlchemySystems(unittest.TestCase):

    def setUp(self):
        self.monastery = PythonMonasteryResearchSystem()
        self.alchemy = PythonAlchemyLaboratory()
        self.supply = MockSupplyChain()

    # ----------------- Scholastic Research Tests -----------------
    def test_monastery_initial_state(self):
        """Verify initial catalog setup and baseline scribe count."""
        self.assertEqual(len(self.monastery.technologies), 6)
        self.assertEqual(len(self.monastery.relics), 5)
        self.assertEqual(self.monastery.assigned_monk_scribes, 3)
        self.assertEqual(len(self.monastery.discovered_relics), 3)
        self.assertEqual(self.monastery.current_research_id, "")
        self.assertEqual(len(self.monastery.unlocked_techs), 0)

    def test_all_six_technologies_catalog(self):
        """Verify presence, costs, and effects of all 6 scholastic technologies."""
        techs = self.monastery.technologies
        self.assertIn("norfolk_genetics", techs)
        self.assertEqual(techs["norfolk_genetics"]["cost"], 100)
        self.assertEqual(techs["norfolk_genetics"]["effects"]["crop_growth_mult"], 1.25)

        self.assertIn("blast_catalysts", techs)
        self.assertEqual(techs["blast_catalysts"]["cost"], 150)
        self.assertTrue(techs["blast_catalysts"]["effects"]["crucible_unlocked"])

        self.assertIn("counterweight_ballistics", techs)
        self.assertEqual(techs["counterweight_ballistics"]["cost"], 200)
        self.assertEqual(techs["counterweight_ballistics"]["effects"]["trebuchet_range"], 250.0)

        self.assertIn("deep_shaft_geology", techs)
        self.assertEqual(techs["deep_shaft_geology"]["cost"], 180)
        self.assertEqual(techs["deep_shaft_geology"]["effects"]["mining_gem_bonus"], 1.25)

        self.assertIn("guild_charters", techs)
        self.assertEqual(techs["guild_charters"]["cost"], 220)
        self.assertEqual(techs["guild_charters"]["effects"]["trade_discount"], 0.15)

        self.assertIn("sacred_architecture", techs)
        self.assertEqual(techs["sacred_architecture"]["cost"], 250)
        self.assertEqual(techs["sacred_architecture"]["effects"]["structural_load_mult"], 1.30)

    def test_start_research_valid_and_invalid(self):
        """Verify starting valid research emits signal and invalid returns False."""
        res_ok = self.monastery.start_research("norfolk_genetics")
        self.assertTrue(res_ok)
        self.assertEqual(self.monastery.current_research_id, "norfolk_genetics")
        self.assertEqual(self.monastery.signal_log[-1][0], "research_started")

        res_invalid = self.monastery.start_research("non_existent_tech")
        self.assertFalse(res_invalid)

    def test_add_research_progress_and_completion(self):
        """Verify incremental scholar points unlock tech upon reaching cost threshold."""
        self.monastery.start_research("norfolk_genetics")
        self.monastery.add_research_progress(50.0)
        self.assertEqual(self.monastery.research_progress["norfolk_genetics"], 50.0)
        self.assertFalse(self.monastery.is_tech_unlocked("norfolk_genetics"))

        # Complete remainder
        self.monastery.add_research_progress(60.0) # 50 + 60 = 110 >= 100
        self.assertTrue(self.monastery.is_tech_unlocked("norfolk_genetics"))
        self.assertEqual(self.monastery.current_research_id, "")
        self.assertEqual(self.monastery.signal_log[-1][0], "research_completed")

    def test_cannot_research_already_unlocked_tech(self):
        """Verify cannot re-research already acquired technology."""
        self.monastery.start_research("norfolk_genetics")
        self.monastery.add_research_progress(100.0)
        self.assertTrue(self.monastery.is_tech_unlocked("norfolk_genetics"))

        # Attempt to re-start
        res = self.monastery.start_research("norfolk_genetics")
        self.assertFalse(res)

    def test_passive_scribe_research_generation(self):
        """Verify monk scribes generate passive research progress during delta ticks."""
        self.monastery.start_research("blast_catalysts")
        # 3 monks * 0.75 pts/sec * 10 sec = 22.5 pts
        self.monastery.process(10.0)
        self.assertAlmostEqual(self.monastery.research_progress["blast_catalysts"], 22.5, places=1)

    def test_monk_scribe_assignment_clamping(self):
        """Verify monk scribe assignment clamps between 0 and 10."""
        self.monastery.assign_monks(5)
        self.assertEqual(self.monastery.assigned_monk_scribes, 8)
        self.monastery.assign_monks(10) # Clamps at 10
        self.assertEqual(self.monastery.assigned_monk_scribes, 10)
        self.monastery.assign_monks(-20) # Clamps at 0
        self.assertEqual(self.monastery.assigned_monk_scribes, 0)

    # ----------------- Holy Relic Sanctuary Tests -----------------
    def test_enshrine_relic_valid_and_slots(self):
        """Verify holy relics can be placed in 3 altar slots."""
        ok = self.monastery.enshrine_relic(0, "true_hearth_shard")
        self.assertTrue(ok)
        self.assertEqual(self.monastery.active_altar_relics[0], "true_hearth_shard")

        # Invalid slot
        self.assertFalse(self.monastery.enshrine_relic(5, "st_columba_tome"))
        # Undiscovered relic
        self.assertFalse(self.monastery.enshrine_relic(1, "first_monarch_crown"))

    def test_enshrine_relic_moves_from_previous_slot(self):
        """Verify moving a relic to another slot removes it from previous slot."""
        self.monastery.enshrine_relic(0, "true_hearth_shard")
        self.assertEqual(self.monastery.active_altar_relics[0], "true_hearth_shard")

        self.monastery.enshrine_relic(2, "true_hearth_shard")
        self.assertEqual(self.monastery.active_altar_relics[0], "")
        self.assertEqual(self.monastery.active_altar_relics[2], "true_hearth_shard")

    def test_remove_relic(self):
        """Verify removing relic clears altar slot and emits signal."""
        self.monastery.enshrine_relic(1, "st_columba_tome")
        self.assertTrue(self.monastery.remove_relic(1))
        self.assertEqual(self.monastery.active_altar_relics[1], "")
        self.assertEqual(self.monastery.signal_log[-1][0], "relic_removed")

    def test_st_columba_tome_research_speed_blessing(self):
        """Verify Tome of St. Columba accelerates research generation by +40%."""
        self.monastery.start_research("counterweight_ballistics")
        self.monastery.enshrine_relic(0, "st_columba_tome")

        # Base rate: 3 * 0.75 = 2.25. With St Columba: 2.25 * 1.40 = 3.15 per sec.
        self.monastery.process(10.0)
        self.assertAlmostEqual(self.monastery.research_progress["counterweight_ballistics"], 31.5, places=1)

    def test_get_active_blessings_aggregation(self):
        """Verify active blessings aggregate correctly from all altar slots."""
        self.monastery.enshrine_relic(0, "true_hearth_shard")
        self.monastery.enshrine_relic(1, "perpetual_chalice")

        blessings = self.monastery.get_active_blessings()
        self.assertIn("warmth_bonus", blessings)
        self.assertEqual(blessings["warmth_bonus"], 15.0)
        self.assertTrue(blessings["frost_immunity"])
        self.assertEqual(blessings["harvest_bonus"], 1.20)
        self.assertEqual(blessings["hunger_drain_mult"], 0.75)

    def test_abbey_bells_ringing_and_decay(self):
        """Verify abbey bells grant +30% serenity and decay over 180s."""
        res = self.monastery.ring_abbey_bells()
        self.assertTrue(res["success"])
        self.assertTrue(self.monastery.bell_blessing_active)
        self.assertEqual(self.monastery.bell_blessing_timer, 180.0)

        blessings = self.monastery.get_active_blessings()
        self.assertEqual(blessings["abbey_bell_serenity"], 30.0)

        # Decay partially
        self.monastery.process(100.0)
        self.assertTrue(self.monastery.bell_blessing_active)
        self.assertEqual(self.monastery.bell_blessing_timer, 80.0)

        # Decay completely
        self.monastery.process(90.0)
        self.assertFalse(self.monastery.bell_blessing_active)
        self.assertNotIn("abbey_bell_serenity", self.monastery.get_active_blessings())

    # ----------------- Alchemy Laboratory Tests -----------------
    def test_alchemy_initial_state(self):
        """Verify alchemy recipes catalog, initial temperature, and stage."""
        self.assertEqual(len(self.alchemy.potion_recipes), 4)
        self.assertEqual(len(self.alchemy.transmutation_formulas), 3)
        self.assertEqual(self.alchemy.alembic_temperature, 85.0)
        self.assertEqual(self.alchemy.philosophers_stone_stage, 1)

    def test_brew_elixir_of_vitality(self):
        """Verify brewing vitality elixir consumes salt and bread, increasing alembic heat."""
        init_salt = self.supply.get_resource("rock_salt")
        init_bread = self.supply.get_resource("bread")

        res = self.alchemy.brew_potion("elixir_of_vitality", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("rock_salt"), init_salt - 1)
        self.assertEqual(self.supply.get_resource("bread"), init_bread - 1)
        self.assertEqual(self.alchemy.brewed_potions_count, 1)
        self.assertEqual(self.alchemy.alembic_temperature, 100.0) # 85 + 15

    def test_brew_elixir_of_iron_skin(self):
        """Verify brewing iron skin consumes iron ore and coal."""
        init_ore = self.supply.get_resource("iron_ore")
        init_coal = self.supply.get_resource("coal")

        res = self.alchemy.brew_potion("elixir_of_iron_skin", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("iron_ore"), init_ore - 1)
        self.assertEqual(self.supply.get_resource("coal"), init_coal - 1)

    def test_brew_elixir_of_windstrider(self):
        """Verify brewing windstrider consumes wheat and salt."""
        init_wheat = self.supply.get_resource("wheat")
        init_salt = self.supply.get_resource("rock_salt")

        res = self.alchemy.brew_potion("elixir_of_windstrider", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("wheat"), init_wheat - 2)
        self.assertEqual(self.supply.get_resource("rock_salt"), init_salt - 1)

    def test_brew_dragons_breath_volatile_flask(self):
        """Verify brewing dragon's breath consumes coal and salt."""
        init_coal = self.supply.get_resource("coal")
        init_salt = self.supply.get_resource("rock_salt")

        res = self.alchemy.brew_potion("dragons_breath_flask", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("coal"), init_coal - 2)
        self.assertEqual(self.supply.get_resource("rock_salt"), init_salt - 2)

    def test_brew_fails_when_missing_ingredients(self):
        """Verify brewing fails gracefully without depleting resources when ingredients insufficient."""
        self.supply.resources["bread"] = 0
        res = self.alchemy.brew_potion("elixir_of_vitality", self.supply)
        self.assertFalse(res["success"])
        self.assertIn("Missing ingredient: bread", res["reason"])

    def test_transmute_lead_to_silver(self):
        """Verify transmutation of stone and coal into precious silver ore."""
        init_stone = self.supply.get_resource("stone")
        init_coal = self.supply.get_resource("coal")
        init_silver = self.supply.get_resource("silver_ore")

        res = self.alchemy.transmute_metal("lead_to_silver", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("stone"), init_stone - 8)
        self.assertEqual(self.supply.get_resource("coal"), init_coal - 4)
        self.assertEqual(self.supply.get_resource("silver_ore"), init_silver + 2)
        self.assertEqual(self.alchemy.alembic_temperature, 110.0) # 85 + 25

    def test_transmute_iron_to_gold(self):
        """Verify crucible transmutation of forged iron ingots into gold coins."""
        init_iron = self.supply.get_resource("iron_ingots")
        init_coal = self.supply.get_resource("coal")
        init_gold = self.supply.get_resource("gold_coins")

        res = self.alchemy.transmute_metal("iron_to_gold", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("iron_ingots"), init_iron - 3)
        self.assertEqual(self.supply.get_resource("coal"), init_coal - 4)
        self.assertEqual(self.supply.get_resource("gold_coins"), init_gold + 25)

    def test_transmute_salt_into_reagent(self):
        """Verify sublimating rock salt and timber into gems."""
        init_salt = self.supply.get_resource("rock_salt")
        init_wood = self.supply.get_resource("wood")
        init_gems = self.supply.get_resource("gems")

        res = self.alchemy.transmute_metal("salt_into_reagent", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("rock_salt"), init_salt - 4)
        self.assertEqual(self.supply.get_resource("wood"), init_wood - 4)
        self.assertEqual(self.supply.get_resource("gems"), init_gems + 1)

    def test_philosophers_stone_magnum_opus_progression(self):
        """Verify all 4 stages of the Philosopher's stone from Nigredo to Rubedo."""
        self.assertEqual(self.alchemy.philosophers_stone_stage, 1)

        # Refine to Stage 2: Albedo (Requires 40 gold, 5 salt)
        res1 = self.alchemy.refine_philosophers_stone(self.supply)
        self.assertTrue(res1["success"])
        self.assertEqual(self.alchemy.philosophers_stone_stage, 2)
        self.assertEqual(res1["bonus_purity"], 1.25)

        # Refine to Stage 3: Citrinitas (Requires 80 gold, 10 salt)
        res2 = self.alchemy.refine_philosophers_stone(self.supply)
        self.assertTrue(res2["success"])
        self.assertEqual(self.alchemy.philosophers_stone_stage, 3)
        self.assertEqual(res2["bonus_purity"], 1.60)

        # Refine to Stage 4: Rubedo (Requires 120 gold, 15 salt) - MockSupply has 200-40-80 = 80 -> need more gold
        self.supply.add_resource("gold_coins", 100)
        res3 = self.alchemy.refine_philosophers_stone(self.supply)
        self.assertTrue(res3["success"])
        self.assertEqual(self.alchemy.philosophers_stone_stage, 4)
        self.assertEqual(res3["bonus_purity"], 2.20)

        # Already at max stage
        res4 = self.alchemy.refine_philosophers_stone(self.supply)
        self.assertFalse(res4["success"])
        self.assertIn("Rubedo", res4["reason"])

    def test_magnum_opus_purity_boosts_transmutation_yield(self):
        """Verify higher philosopher's stone stage amplifies transmutation yields."""
        # Elevate to Rubedo (2.20x yield)
        self.alchemy.philosophers_stone_stage = 4
        init_gold = self.supply.get_resource("gold_coins")

        # Base output is 25 gold coins -> 25 * 2.20 = 55 gold coins!
        res = self.alchemy.transmute_metal("iron_to_gold", self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(self.supply.get_resource("gold_coins"), init_gold + 55)

    # ----------------- Persistence Roundtrip Tests -----------------
    def test_monastery_save_load_roundtrip(self):
        """Verify monastery research, scribes, relics, and bell state survive serialization."""
        self.monastery.start_research("sacred_architecture")
        self.monastery.add_research_progress(120.0)
        self.monastery.unlocked_techs.append("norfolk_genetics")
        self.monastery.assign_monks(3)
        self.monastery.enshrine_relic(0, "true_hearth_shard")
        self.monastery.enshrine_relic(1, "st_columba_tome")
        self.monastery.ring_abbey_bells()

        saved = self.monastery.to_dict()
        serialized = json.dumps(saved)
        checksum = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        self.assertEqual(len(checksum), 64)

        restored = PythonMonasteryResearchSystem()
        restored.from_dict(json.loads(serialized))

        self.assertEqual(restored.current_research_id, "sacred_architecture")
        self.assertEqual(restored.research_progress["sacred_architecture"], 120.0)
        self.assertIn("norfolk_genetics", restored.unlocked_techs)
        self.assertEqual(restored.assigned_monk_scribes, 6)
        self.assertEqual(restored.active_altar_relics[0], "true_hearth_shard")
        self.assertEqual(restored.active_altar_relics[1], "st_columba_tome")
        self.assertTrue(restored.bell_blessing_active)

    def test_alchemy_save_load_roundtrip(self):
        """Verify alchemy laboratory stage, heat, and production stats survive serialization."""
        self.alchemy.philosophers_stone_stage = 3
        self.alchemy.alembic_temperature = 220.0
        self.alchemy.brewed_potions_count = 12
        self.alchemy.transmutations_count = 8

        saved = self.alchemy.to_dict()
        serialized = json.dumps(saved)
        checksum = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        self.assertEqual(len(checksum), 64)

        restored = PythonAlchemyLaboratory()
        restored.from_dict(json.loads(serialized))

        self.assertEqual(restored.philosophers_stone_stage, 3)
        self.assertEqual(restored.alembic_temperature, 220.0)
        self.assertEqual(restored.brewed_potions_count, 12)
        self.assertEqual(restored.transmutations_count, 8)


if __name__ == "__main__":
    unittest.main()
