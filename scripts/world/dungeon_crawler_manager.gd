# scripts/world/dungeon_crawler_manager.gd
# Voxel Lord: Feudal Realm - Milestone 28: Subterranean Dungeon Delving & Sconce Lighting
# Manages party sanity, darkness fear penalties, wall sconce lighting, and relic salvage.

class_name DungeonCrawlerManager
extends RefCounted

signal sconce_lit(sconce_id: String, duration: float)
signal sconce_extinguished(sconce_id: String)
signal sanity_critical(current_sanity: float)
signal fear_debuff_applied()
signal fear_debuff_cleared()
signal relics_salvaged(total_value: int, items_count: int)

var wall_sconces: Dictionary = {}
var party_sanity: float = 100.0
var max_sanity: float = 100.0
var fear_debuff_active: bool = false
var salvaged_vault: Array[Dictionary] = []

func register_sconce(sconce_id: String, pos: Vector3, initial_fuel: float = 0.0, radius: float = 7.5) -> void:
	wall_sconces[sconce_id] = {
		"id": sconce_id,
		"pos": pos,
		"lit": initial_fuel > 0.0,
		"fuel": initial_fuel,
		"radius": radius
	}

func light_sconce(sconce_id: String, torch_fuel_seconds: float = 240.0) -> bool:
	if not wall_sconces.has(sconce_id):
		return false
	var s = wall_sconces[sconce_id]
	s["lit"] = true
	s["fuel"] = torch_fuel_seconds
	sconce_lit.emit(sconce_id, torch_fuel_seconds)
	return true

func update_sconces(delta: float) -> void:
	for id in wall_sconces.keys():
		var s = wall_sconces[id]
		if s["lit"]:
			s["fuel"] -= delta
			if s["fuel"] <= 0.0:
				s["fuel"] = 0.0
				s["lit"] = false
				sconce_extinguished.emit(id)

func get_active_lights() -> Array:
	var lights = []
	for s in wall_sconces.values():
		if s["lit"]:
			lights.append(s)
	return lights

func update_exploration_party(delta: float, party_pos: Vector3) -> Dictionary:
	update_sconces(delta)

	var in_light = false
	for s in wall_sconces.values():
		if s["lit"] and party_pos.distance_to(s["pos"]) <= s["radius"]:
			in_light = true
			break

	if in_light:
		# Recover sanity near warm sconce flame
		party_sanity = min(max_sanity, party_sanity + 1.5 * delta)
		if fear_debuff_active and party_sanity >= 40.0:
			fear_debuff_active = false
			fear_debuff_cleared.emit()
	else:
		# Darkness fear drain
		party_sanity = max(0.0, party_sanity - 2.0 * delta)
		if party_sanity <= 25.0 and not fear_debuff_active:
			fear_debuff_active = true
			fear_debuff_applied.emit()
			sanity_critical.emit(party_sanity)

	return {
		"in_light": in_light,
		"party_sanity": party_sanity,
		"fear_debuff": fear_debuff_active,
		"combat_penalty": -0.30 if fear_debuff_active else 0.0
	}

func deposit_relics(relic_list: Array[Dictionary]) -> int:
	var added = relic_list.size()
	salvaged_vault.append_array(relic_list)
	return added

func transfer_salvage_to_settlement() -> Dictionary:
	var total_val = 0
	var count = salvaged_vault.size()
	for r in salvaged_vault:
		total_val += r.get("value", 0)

	relics_salvaged.emit(total_val, count)
	salvaged_vault.clear()
	return {
		"items_salvaged": count,
		"total_treasury_gold": total_val
	}
