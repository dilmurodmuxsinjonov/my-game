# scripts/world/sheep_pasture.gd
# Voxel Lord: Feudal Realm - Milestone 24: Sheepfold Pasture & Wool Weaving Loom
# Inspired by Medieval Dynasty (Sheep Shearing) and Going Medieval (Warm Woolen Garments & Hypothermia Defense)

class_name SheepPasture
extends Node3D

signal sheep_shorn(wool_yield: int)
signal tunic_woven(total_tunics: int)

const MAX_SHEEP: int = 6
const WOOL_PER_SHEEP: int = 2
const SHEARING_CYCLE_DAYS: float = 2.0
const WOOLEN_TUNIC_WOOL_COST: int = 2
const TUNIC_WARMTH_BONUS: float = 35.0
const TUNIC_MORALE_BONUS: int = 10

var sheep_count: int = 4
var shearing_cooldown: float = 0.0
var stored_wool: int = 0
var woven_tunics: int = 0

func _init() -> void:
	sheep_count = 4
	shearing_cooldown = 0.0
	stored_wool = 0
	woven_tunics = 0

func update_growth(delta_days: float) -> void:
	if shearing_cooldown > 0.0:
		shearing_cooldown = maxf(0.0, shearing_cooldown - delta_days)

func shear_sheep(force: bool = false) -> Dictionary:
	if not force and shearing_cooldown > 0.0:
		return {
			"success": false,
			"reason": "NOT_READY",
			"remaining_cooldown": shearing_cooldown
		}
	
	var wool_produced: int = sheep_count * WOOL_PER_SHEEP
	stored_wool += wool_produced
	shearing_cooldown = SHEARING_CYCLE_DAYS
	sheep_shorn.emit(wool_produced)
	
	return {
		"success": true,
		"wool_produced": wool_produced,
		"total_stored_wool": stored_wool,
		"sheep_count": sheep_count
	}

func weave_woolen_tunic(count: int = 1) -> Dictionary:
	var wool_needed: int = count * WOOLEN_TUNIC_WOOL_COST
	if stored_wool < wool_needed:
		return {
			"success": false,
			"reason": "INSUFFICIENT_WOOL",
			"stored_wool": stored_wool,
			"wool_needed": wool_needed
		}
	
	stored_wool -= wool_needed
	woven_tunics += count
	tunic_woven.emit(woven_tunics)
	
	return {
		"success": true,
		"tunics_woven": count,
		"total_tunics": woven_tunics,
		"warmth_bonus": TUNIC_WARMTH_BONUS,
		"morale_bonus": TUNIC_MORALE_BONUS
	}

func add_sheep(count: int = 1) -> bool:
	if sheep_count + count <= MAX_SHEEP:
		sheep_count += count
		return true
	return false
