# scripts/world/water_cask.gd
# Voxel Lord: Feudal Realm - Milestone 27: Bulk Water Storage & Portable Hydration
# Simulates watertight oak casks storing settlement reserves and filling expedition canteens.

class_name WaterCask
extends RefCounted

signal cask_filled(cask_id: String, current_volume: int)
signal canteen_filled(cask_id: String, squad_id: String)

var cask_id: String = "water_cask_1"
var max_capacity: int = 40
var stored_buckets: int = 20

func _init(p_id: String = "water_cask_1", initial_water: int = 20) -> void:
	cask_id = p_id
	stored_buckets = clamp(initial_water, 0, max_capacity)

func deposit_water(buckets: int) -> int:
	var space = max_capacity - stored_buckets
	var deposited = min(buckets, space)
	stored_buckets += deposited
	cask_filled.emit(cask_id, stored_buckets)
	return deposited

func withdraw_water(buckets: int) -> int:
	var withdrawn = min(buckets, stored_buckets)
	stored_buckets -= withdrawn
	return withdrawn

func fill_expedition_canteens(squad_id: String, squad_size: int) -> Dictionary:
	# Each soldier requires 2 water buckets for full 24h campaign hydration
	var buckets_needed = squad_size * 2
	var allocated = min(buckets_needed, stored_buckets)
	stored_buckets -= allocated

	var fully_hydrated_soldiers = allocated / 2
	var under_hydrated_soldiers = squad_size - fully_hydrated_soldiers

	canteen_filled.emit(cask_id, squad_id)
	return {
		"squad_id": squad_id,
		"hydrated_soldiers": fully_hydrated_soldiers,
		"under_hydrated_soldiers": under_hydrated_soldiers,
		"campaign_hours_safe": 24.0 if under_hydrated_soldiers == 0 else 6.0
	}
