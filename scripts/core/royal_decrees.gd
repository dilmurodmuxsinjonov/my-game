# scripts/core/royal_decrees.gd
# Voxel Lord: Feudal Realm - Milestone 47: Monarch Imperial Decrees & Law Proclamations
# Manages royal edicts, economic tradeoffs, duration timers, and realm-wide active modifiers.

class_name RoyalDecrees
extends Node

signal decree_proclaimed(decree_id: String, decree_name: String)
signal decree_expired(decree_id: String, decree_name: String)
signal modifiers_updated()

const DECREE_CATALOG: Dictionary = {
	"corvee_labor": {
		"id": "corvee_labor",
		"name": "Corvée Mandatory Labor Mandate",
		"description": "Compels all subjects to work double shifts in quarries and logging camps.",
		"cost_renown": 50,
		"cost_coins": 20,
		"duration": 240.0, # 2 game days
		"modifiers": {
			"work_speed_mult": 1.30,
			"hunger_drain_mult": 1.20,
			"morale_decay_offset": 5.0
		}
	},
	"grain_dole_relief": {
		"id": "grain_dole_relief",
		"name": "Imperial Grain Dole & Famine Relief",
		"description": "Distributes reserve bread and wheat to soothe citizens during harsh winters.",
		"cost_renown": 25,
		"cost_coins": 10,
		"cost_items": {"bread": 10, "wheat": 15},
		"duration": 180.0,
		"modifiers": {
			"hunger_drain_mult": 0.65,
			"morale_bonus": 25.0,
			"health_regen_bonus": 1.5
		}
	},
	"guild_subsidies": {
		"id": "guild_subsidies",
		"name": "Artisan Guild Patronage & Subsidies",
		"description": "Funds blacksmiths and engineers to accelerate crucible metallurgy and steam fabrication.",
		"cost_renown": 45,
		"cost_coins": 50,
		"duration": 300.0,
		"modifiers": {
			"craft_output_bonus": 0.25,
			"furnace_heat_speed": 1.35,
			"tax_revenue_mult": 1.15
		}
	},
	"frontier_conscription": {
		"id": "frontier_conscription",
		"name": "Frontier Militia Levy Conscription",
		"description": "Drafts stalwart laborers into shield-bearing castle militia when raiders approach.",
		"cost_renown": 60,
		"cost_coins": 35,
		"duration": 210.0,
		"modifiers": {
			"guard_defense_mult": 1.25,
			"raid_defeat_reward_mult": 1.50,
			"guard_capacity_bonus": 4.0
		}
	},
	"free_trade_charter": {
		"id": "free_trade_charter",
		"name": "Mercantile Free Trade & Toll Exemption",
		"description": "Waives river and road tolls to attract foreign merchant caravans faster.",
		"cost_renown": 30,
		"cost_coins": 30,
		"duration": 360.0,
		"modifiers": {
			"caravan_interval_mult": 0.65,
			"trade_discount": 0.15
		}
	},
	"monastic_scholarship": {
		"id": "monastic_scholarship",
		"name": "Monastic Scholarly Patronage",
		"description": "Endows cloistered scholars to study clockwork astronomy and restorative apothecary arts.",
		"cost_renown": 75,
		"cost_coins": 60,
		"duration": 300.0,
		"modifiers": {
			"tech_speed_mult": 1.40,
			"infirmary_heal_mult": 1.50
		}
	}
}

var active_decrees: Dictionary = {} # decree_id -> {"remaining": float, "total": float}
var aggregated_modifiers: Dictionary = {}

func _init() -> void:
	_recalculate_modifiers()

func get_catalog() -> Dictionary:
	return DECREE_CATALOG

func can_proclaim(decree_id: String, supply_chain: SupplyChain = null, total_renown: int = 9999) -> bool:
	if not DECREE_CATALOG.has(decree_id):
		return false
	if active_decrees.has(decree_id):
		return false # already active
	
	var data = DECREE_CATALOG[decree_id]
	if total_renown < data.get("cost_renown", 0):
		return false
	
	if supply_chain:
		if supply_chain.coins < data.get("cost_coins", 0):
			return false
		var req_items = data.get("cost_items", {})
		for item in req_items:
			if supply_chain.get_item_count(item) < req_items[item]:
				return false
	return true

func proclaim_decree(decree_id: String, supply_chain: SupplyChain = null, total_renown: int = 9999) -> bool:
	if not can_proclaim(decree_id, supply_chain, total_renown):
		return false
	
	var data = DECREE_CATALOG[decree_id]
	if supply_chain:
		supply_chain.coins -= data.get("cost_coins", 0)
		var req_items = data.get("cost_items", {})
		for item in req_items:
			supply_chain.remove_item(item, req_items[item])
	
	var duration = float(data.get("duration", 180.0))
	active_decrees[decree_id] = {
		"remaining": duration,
		"total": duration
	}
	
	_recalculate_modifiers()
	decree_proclaimed.emit(decree_id, data["name"])
	return true

func revoke_decree(decree_id: String) -> bool:
	if not active_decrees.has(decree_id):
		return false
	var dname = DECREE_CATALOG[decree_id]["name"] if DECREE_CATALOG.has(decree_id) else decree_id
	active_decrees.erase(decree_id)
	_recalculate_modifiers()
	decree_expired.emit(decree_id, dname)
	return true

func update_timers(delta: float) -> void:
	if active_decrees.is_empty():
		return
	
	var expired: Array[String] = []
	for dec_id in active_decrees:
		active_decrees[dec_id]["remaining"] -= delta
		if active_decrees[dec_id]["remaining"] <= 0.0:
			expired.append(dec_id)
	
	for dec_id in expired:
		var dname = DECREE_CATALOG[dec_id]["name"] if DECREE_CATALOG.has(dec_id) else dec_id
		active_decrees.erase(dec_id)
		decree_expired.emit(dec_id, dname)
	
	if not expired.is_empty():
		_recalculate_modifiers()

func _recalculate_modifiers() -> void:
	aggregated_modifiers.clear()
	# Set baseline multipliers
	aggregated_modifiers["work_speed_mult"] = 1.0
	aggregated_modifiers["hunger_drain_mult"] = 1.0
	aggregated_modifiers["craft_output_bonus"] = 0.0
	aggregated_modifiers["guard_defense_mult"] = 1.0
	aggregated_modifiers["caravan_interval_mult"] = 1.0
	aggregated_modifiers["tech_speed_mult"] = 1.0
	aggregated_modifiers["morale_bonus"] = 0.0
	aggregated_modifiers["guard_capacity_bonus"] = 0.0

	for dec_id in active_decrees:
		if DECREE_CATALOG.has(dec_id):
			var mods = DECREE_CATALOG[dec_id].get("modifiers", {})
			for m_key in mods:
				var val = float(mods[m_key])
				if m_key.ends_with("_mult"):
					aggregated_modifiers[m_key] = aggregated_modifiers.get(m_key, 1.0) * val
				else:
					aggregated_modifiers[m_key] = aggregated_modifiers.get(m_key, 0.0) + val
	
	modifiers_updated.emit()

func get_modifier(mod_key: String, default_val: float = 1.0) -> float:
	return aggregated_modifiers.get(mod_key, default_val)

func is_decree_active(decree_id: String) -> bool:
	return active_decrees.has(decree_id)

func get_active_decree_list() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for dec_id in active_decrees:
		if DECREE_CATALOG.has(dec_id):
			var data = DECREE_CATALOG[dec_id]
			result.append({
				"id": dec_id,
				"name": data["name"],
				"remaining": active_decrees[dec_id]["remaining"],
				"total": active_decrees[dec_id]["total"]
			})
	return result

func to_dict() -> Dictionary:
	var list_arr: Array = []
	for dec_id in active_decrees:
		list_arr.append({
			"id": dec_id,
			"remaining": active_decrees[dec_id]["remaining"],
			"total": active_decrees[dec_id]["total"]
		})
	return {"active_decrees": list_arr}

func from_dict(data: Dictionary) -> void:
	active_decrees.clear()
	if data.has("active_decrees"):
		for item in data["active_decrees"]:
			var id = item.get("id", "")
			if DECREE_CATALOG.has(id):
				active_decrees[id] = {
					"remaining": float(item.get("remaining", 100.0)),
					"total": float(item.get("total", 180.0))
				}
	_recalculate_modifiers()
