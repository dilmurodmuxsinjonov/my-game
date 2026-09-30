# scripts/combat/alchemy_laboratory.gd
# Voxel Lord: Feudal Realm - Milestone 51: Alchemical Transmutation Laboratory
# Handles Hermetic alchemical distillations, magnum opus philosopher's stone refinement,
# combat/vitality elixirs, and metal transmutations.

class_name AlchemyLaboratory
extends Node

signal potion_brewed(potion_id: String, potion_name: String, count: int)
signal metal_transmuted(formula_id: String, input_res: String, output_res: String, output_count: int)
signal philosophers_stone_refined(stage: int, stage_name: String)
signal alembic_heat_changed(temp_celsius: float)

# Brewing Recipes Catalog
var potion_recipes: Dictionary = {}

# Transmutation Formulas Catalog
var transmutation_formulas: Dictionary = {}

# Laboratory State
var alembic_temperature: float = 85.0 # Celsius
var philosophers_stone_stage: int = 1 # 1: Nigredo, 2: Albedo, 3: Citrinitas, 4: Rubedo (Magnum Opus)
var brewed_potions_count: int = 0
var transmutations_count: int = 0

# Philosopher's Stone Stages
const STONE_STAGES: Array[Dictionary] = [
	{"stage": 1, "name": "Nigredo (Black Dissolution)", "bonus_purity": 1.0, "icon": "🌑"},
	{"stage": 2, "name": "Albedo (White Purification)", "bonus_purity": 1.25, "icon": "⚪"},
	{"stage": 3, "name": "Citrinitas (Yellow Awakening)", "bonus_purity": 1.60, "icon": "🟡"},
	{"stage": 4, "name": "Rubedo (Magnum Opus / Red Elixir)", "bonus_purity": 2.20, "icon": "🔴"}
]

func _init() -> void:
	init_recipes()
	init_transmutations()

func init_recipes() -> void:
	potion_recipes = {
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

func init_transmutations() -> void:
	transmutation_formulas = {
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

# ----------------- Brewing Mechanics -----------------
func brew_potion(potion_id: String, supply_chain: SupplyChain = null) -> Dictionary:
	if not potion_recipes.has(potion_id):
		return {"success": false, "reason": "Unknown potion formula"}

	var recipe = potion_recipes[potion_id]
	var ingredients: Dictionary = recipe["ingredients"]

	if supply_chain:
		# Verify ingredients
		for item in ingredients.keys():
			var req = ingredients[item]
			if supply_chain.get_resource(item) < req:
				return {"success": false, "reason": "Missing ingredient: %s (Requires %d)" % [item, req]}

		# Consume ingredients
		for item in ingredients.keys():
			supply_chain.consume_resource(item, ingredients[item])

	brewed_potions_count += 1
	alembic_temperature = minf(350.0, alembic_temperature + 15.0)
	alembic_heat_changed.emit(alembic_temperature)

	potion_brewed.emit(potion_id, recipe["name"], 1)
	return {
		"success": true,
		"potion_id": potion_id,
		"name": recipe["name"],
		"effect": recipe
	}

# ----------------- Transmutation Mechanics -----------------
func transmute_metal(formula_id: String, supply_chain: SupplyChain = null) -> Dictionary:
	if not transmutation_formulas.has(formula_id):
		return {"success": false, "reason": "Unknown transmutation formula"}

	var formula = transmutation_formulas[formula_id]
	var inputs: Dictionary = formula["inputs"]
	var outputs: Dictionary = formula["outputs"]

	if supply_chain:
		for item in inputs.keys():
			var req = inputs[item]
			if supply_chain.get_resource(item) < req:
				return {"success": false, "reason": "Insufficient %s (Requires %d)" % [item, req]}

		for item in inputs.keys():
			supply_chain.consume_resource(item, inputs[item])

		for item in outputs.keys():
			var prod = outputs[item]
			# Apply philosopher's stone stage bonus multiplier
			var stage_info = STONE_STAGES[clampi(philosophers_stone_stage - 1, 0, 3)]
			var final_prod = int(round(prod * stage_info["bonus_purity"]))
			supply_chain.add_resource(item, final_prod)

	transmutations_count += 1
	alembic_temperature = minf(400.0, alembic_temperature + 25.0)
	alembic_heat_changed.emit(alembic_temperature)

	var primary_out = outputs.keys()[0]
	metal_transmuted.emit(formula_id, inputs.keys()[0], primary_out, outputs[primary_out])
	return {
		"success": true,
		"formula_id": formula_id,
		"inputs": inputs,
		"outputs": outputs
	}

# ----------------- Magnum Opus Refinement -----------------
func refine_philosophers_stone(supply_chain: SupplyChain = null) -> Dictionary:
	if philosophers_stone_stage >= 4:
		return {"success": false, "reason": "The Magnum Opus (Rubedo) is already perfected!"}

	var gold_cost = 40 * philosophers_stone_stage
	var salt_cost = 5 * philosophers_stone_stage

	if supply_chain:
		if supply_chain.get_resource("gold_coins") < gold_cost:
			return {"success": false, "reason": "Insufficient gold for sublimation (Requires %d Gold)" % gold_cost}
		if supply_chain.get_resource("rock_salt") < salt_cost:
			return {"success": false, "reason": "Insufficient rock salt (Requires %d Salt)" % salt_cost}

		supply_chain.consume_resource("gold_coins", gold_cost)
		supply_chain.consume_resource("rock_salt", salt_cost)

	philosophers_stone_stage += 1
	var stage_info = STONE_STAGES[philosophers_stone_stage - 1]
	philosophers_stone_refined.emit(philosophers_stone_stage, stage_info["name"])

	return {
		"success": true,
		"stage": philosophers_stone_stage,
		"stage_name": stage_info["name"],
		"bonus_purity": stage_info["bonus_purity"]
	}

# ----------------- Persistence -----------------
func to_dict() -> Dictionary:
	return {
		"alembic_temperature": alembic_temperature,
		"philosophers_stone_stage": philosophers_stone_stage,
		"brewed_potions_count": brewed_potions_count,
		"transmutations_count": transmutations_count
	}

func from_dict(data: Dictionary) -> void:
	if data.is_empty():
		return
	alembic_temperature = data.get("alembic_temperature", 85.0)
	philosophers_stone_stage = data.get("philosophers_stone_stage", 1)
	brewed_potions_count = data.get("brewed_potions_count", 0)
	transmutations_count = data.get("transmutations_count", 0)
