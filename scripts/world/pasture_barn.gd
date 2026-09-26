# scripts/world/pasture_barn.gd
# Voxel Lord: Feudal Realm - Milestone 24: Pasture Barn & Oxen Logistics
# Inspired by Manor Lords (Oxen Log Hauling) and Medieval Dynasty (Dairy Farming & Cattle Stalls)

class_name PastureBarn
extends Node3D

signal milk_collected(amount: int)
signal ox_dispatched(logs_hauled: int)
signal livestock_fed(success: bool)

const MAX_CATTLE_CAPACITY: int = 4
const MAX_OXEN_CAPACITY: int = 2
const DAILY_MILK_PER_COW: int = 2
const OX_HAUL_CAPACITY: int = 4 # Logs hauled simultaneously per trip
const OX_SPEED_MULTIPLIER: float = 1.8

var dairy_cows: int = 2
var draft_oxen: int = 1
var stored_milk: int = 0
var is_ox_hitched: bool = false

func _init() -> void:
	dairy_cows = 2
	draft_oxen = 1
	stored_milk = 0
	is_ox_hitched = false

func process_daily_production(has_fodder: bool = true) -> Dictionary:
	if not has_fodder:
		livestock_fed.emit(false)
		return {
			"success": false,
			"reason": "STARVATION",
			"milk_produced": 0,
			"dairy_cows": dairy_cows,
			"draft_oxen": draft_oxen
		}
	
	livestock_fed.emit(true)
	var milk_produced: int = dairy_cows * DAILY_MILK_PER_COW
	stored_milk += milk_produced
	milk_collected.emit(milk_produced)
	
	return {
		"success": true,
		"milk_produced": milk_produced,
		"total_stored_milk": stored_milk,
		"dairy_cows": dairy_cows,
		"draft_oxen": draft_oxen
	}

func collect_milk() -> int:
	var collected: int = stored_milk
	stored_milk = 0
	return collected

func dispatch_ox_log_hauler(available_logs: int) -> Dictionary:
	if draft_oxen <= 0:
		return {
			"success": false,
			"reason": "NO_OXEN",
			"logs_hauled": 0
		}
	
	var max_capacity: int = draft_oxen * OX_HAUL_CAPACITY
	var logs_to_haul: int = mini(available_logs, max_capacity)
	if logs_to_haul <= 0:
		return {
			"success": false,
			"reason": "NO_LOGS",
			"logs_hauled": 0
		}
	
	is_ox_hitched = true
	ox_dispatched.emit(logs_to_haul)
	return {
		"success": true,
		"logs_hauled": logs_to_haul,
		"speed_multiplier": OX_SPEED_MULTIPLIER
	}

func return_ox_from_haul() -> void:
	is_ox_hitched = false

func add_livestock(animal_type: String, count: int = 1) -> bool:
	match animal_type:
		"cow":
			if dairy_cows + count <= MAX_CATTLE_CAPACITY:
				dairy_cows += count
				return true
		"ox":
			if draft_oxen + count <= MAX_OXEN_CAPACITY:
				draft_oxen += count
				return true
	return false
