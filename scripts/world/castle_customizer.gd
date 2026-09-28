# scripts/world/castle_customizer.gd
# Voxel Lord: Feudal Realm - Milestone 46: Monarch Castle Customization & Imperial Buffs
# Manages royal furnishings, throne room decor placement, castle prestige, and realm-wide passive buffs.

class_name CastleCustomizer
extends Node

signal furnishing_placed(decor_id: String, position: Vector3i)
signal furnishing_removed(decor_id: String)
signal realm_buffs_updated(buffs: Dictionary, total_prestige: int)

const CATALOG: Dictionary = {
	"throne_sovereign": {
		"id": "throne_sovereign",
		"name": "Sovereign Gilded Oak Throne",
		"category": "Throne",
		"description": "The imperial seat of rulership. Radiates authority across the realm.",
		"cost": {"wood": 30, "gold_ingot": 10},
		"buffs": {"realm_morale": 15.0, "renown_per_day": 5.0},
		"prestige": 50
	},
	"war_council_map": {
		"id": "war_council_map",
		"name": "Grand Realm War Council Table",
		"category": "Military",
		"description": "Carved topographic battle map. Coordinates guards and fortifies defenses.",
		"cost": {"wood": 25, "iron_ingot": 8},
		"buffs": {"guard_defense_bonus": 0.20, "raid_frequency_reduction": 0.15},
		"prestige": 35
	},
	"chandelier_crystal": {
		"id": "chandelier_crystal",
		"name": "Imperial Chandelier of Starlight",
		"category": "Lighting",
		"description": "Prismatic crystal candelabra illuminating late-night artisan workshops.",
		"cost": {"iron_ingot": 12, "glass": 16},
		"buffs": {"night_crafting_bonus": 0.15, "realm_morale": 5.0},
		"prestige": 25
	},
	"treasury_vault_chest": {
		"id": "treasury_vault_chest",
		"name": "Royal Ironbound Treasury Vault",
		"category": "Economy",
		"description": "Reinforced coffer securing kingdom tax revenues and trade tariffs.",
		"cost": {"wood": 15, "iron_ingot": 20, "gold_ingot": 5},
		"buffs": {"tax_efficiency_bonus": 0.15, "gold_capacity_bonus": 500.0},
		"prestige": 40
	},
	"banquet_great_table": {
		"id": "banquet_great_table",
		"name": "Monarch Feast & Guild Banquet Table",
		"category": "Feast",
		"description": "Massive oak banquet table seating citizens for lavish seasonal harvests.",
		"cost": {"wood": 40, "cloth": 10},
		"buffs": {"hunger_drain_reduction": 0.20, "feast_morale_boost": 25.0},
		"prestige": 30
	},
	"knights_armor_display": {
		"id": "knights_armor_display",
		"name": "Royal Champion Plate Display Stand",
		"category": "Military",
		"description": "Polished steel battle armor inspiring garrison soldiers and archers.",
		"cost": {"iron_ingot": 16, "wood": 8},
		"buffs": {"guard_attack_bonus": 0.15, "garrison_cap_bonus": 4.0},
		"prestige": 20
	},
	"astronomers_armillary": {
		"id": "astronomers_armillary",
		"name": "Brass Armillary Sphere & Astrolabe",
		"category": "Knowledge",
		"description": "Celestial tracking instruments guiding trade routes and scholar discoveries.",
		"cost": {"iron_ingot": 10, "gold_ingot": 4},
		"buffs": {"tech_progress_bonus": 0.25, "caravan_trade_profit": 0.10},
		"prestige": 45
	}
}

var placed_furnishings: Dictionary = {}
var active_buffs: Dictionary = {}
var total_prestige: int = 0

func _init() -> void:
	recalculate_buffs()

func get_catalog() -> Dictionary:
	return CATALOG

func can_afford(decor_id: String, supply_chain: SupplyChain) -> bool:
	if not CATALOG.has(decor_id):
		return false
	if not supply_chain:
		return true
	
	var cost = CATALOG[decor_id]["cost"]
	for item in cost:
		var required_qty = cost[item]
		if supply_chain.get_item_count(item) < required_qty:
			return false
	return true

func place_furnishing(decor_id: String, grid_pos: Vector3i, supply_chain: SupplyChain = null) -> bool:
	if not CATALOG.has(decor_id):
		return false
	
	if supply_chain:
		if not can_afford(decor_id, supply_chain):
			return false
		# Deduct costs
		var cost = CATALOG[decor_id]["cost"]
		for item in cost:
			supply_chain.remove_item(item, cost[item])
	
	placed_furnishings[decor_id] = {
		"id": decor_id,
		"position": grid_pos,
		"active": true
	}
	
	recalculate_buffs()
	furnishing_placed.emit(decor_id, grid_pos)
	return true

func remove_furnishing(decor_id: String) -> bool:
	if not placed_furnishings.has(decor_id):
		return false
	
	placed_furnishings.erase(decor_id)
	recalculate_buffs()
	furnishing_removed.emit(decor_id)
	return true

func recalculate_buffs() -> Dictionary:
	active_buffs.clear()
	total_prestige = 0
	
	for decor_id in placed_furnishings:
		var entry = placed_furnishings[decor_id]
		if not entry.get("active", true):
			continue
		
		if CATALOG.has(decor_id):
			var item_data = CATALOG[decor_id]
			total_prestige += int(item_data.get("prestige", 0))
			var buffs = item_data.get("buffs", {})
			for b_key in buffs:
				var current_val = active_buffs.get(b_key, 0.0)
				active_buffs[b_key] = current_val + float(buffs[b_key])
	
	realm_buffs_updated.emit(active_buffs, total_prestige)
	return active_buffs

func get_buff_value(buff_key: String) -> float:
	return active_buffs.get(buff_key, 0.0)

func get_all_active_buffs() -> Dictionary:
	return active_buffs.duplicate()

func get_total_prestige() -> int:
	return total_prestige

func is_placed(decor_id: String) -> bool:
	return placed_furnishings.has(decor_id)

func to_dict() -> Dictionary:
	var placed_array: Array = []
	for decor_id in placed_furnishings:
		var item = placed_furnishings[decor_id]
		var pos = item.get("position", Vector3i.ZERO)
		placed_array.append({
			"id": decor_id,
			"pos_x": pos.x,
			"pos_y": pos.y,
			"pos_z": pos.z,
			"active": item.get("active", true)
		})
	
	return {
		"placed_furnishings": placed_array,
		"total_prestige": total_prestige
	}

func from_dict(data: Dictionary) -> void:
	placed_furnishings.clear()
	if data.has("placed_furnishings"):
		for item in data["placed_furnishings"]:
			var id = item.get("id", "")
			if CATALOG.has(id):
				placed_furnishings[id] = {
					"id": id,
					"position": Vector3i(int(item.get("pos_x", 0)), int(item.get("pos_y", 0)), int(item.get("pos_z", 0))),
					"active": item.get("active", true)
				}
	recalculate_buffs()
