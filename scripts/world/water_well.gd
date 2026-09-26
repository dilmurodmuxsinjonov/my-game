# scripts/world/water_well.gd
# Voxel Lord: Feudal Realm - Milestone 27: Village Water Logistics
# Simulates deep stone groundwater wells, thirst mechanics, and firefighting reserves.

class_name WaterWell
extends RefCounted

signal water_drawn(well_id: String, amount: int)
signal well_depleted(well_id: String)
signal fire_extinguished(well_id: String, water_used: int)

var well_id: String = "water_well_1"
var max_capacity: int = 24
var stored_water: int = 12
var daily_replenishment: int = 8

func _init(p_id: String = "water_well_1", initial_water: int = 12) -> void:
	well_id = p_id
	stored_water = clamp(initial_water, 0, max_capacity)

func replenish_daily() -> int:
	var added = min(daily_replenishment, max_capacity - stored_water)
	stored_water += added
	return added

func draw_water(amount: int) -> int:
	var drawn = min(amount, stored_water)
	stored_water -= drawn
	if drawn > 0:
		water_drawn.emit(well_id, drawn)
	if stored_water == 0:
		well_depleted.emit(well_id)
	return drawn

func satisfy_citizen_thirst(citizen_count: int) -> Dictionary:
	var needed = citizen_count
	var satisfied = min(needed, stored_water)
	stored_water -= satisfied

	var dehydrated_count = needed - satisfied
	return {
		"satisfied_citizens": satisfied,
		"dehydrated_citizens": dehydrated_count,
		"work_speed_penalty": -0.25 if dehydrated_count > 0 else 0.0,
		"morale_penalty": -15 if dehydrated_count > 0 else 0
	}

func extinguish_fire(required_water: int = 4) -> bool:
	if stored_water >= required_water:
		stored_water -= required_water
		fire_extinguished.emit(well_id, required_water)
		return true
	return false

func get_water_level() -> int:
	return stored_water
