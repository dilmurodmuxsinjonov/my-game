# scripts/combat/pitch_cauldron.gd
# Voxel Lord: Feudal Realm - Milestone 23: Gate Boiling Pitch Defense
# Inspired by Stronghold (Boiling Pitch Cauldrons) and Mount & Blade II (Murder Holes)

class_name PitchCauldron
extends Node3D

signal pitch_dumped(puddle_radius: float, dps: float, duration: float)
signal cauldron_reheated()

const PITCH_DPS: float = 40.0
const PUDDLE_RADIUS: float = 6.0
const BURN_DURATION_SECONDS: float = 15.0
const MOVEMENT_SLOW_MULTIPLIER: float = 0.40 # 60% movement speed reduction
const REHEAT_TIME_SECONDS: float = 45.0

var is_boiling: bool = true
var reheat_timer: float = 0.0
var pitch_charges: int = 5

func _init() -> void:
	pass

func dump_pitch() -> Dictionary:
	if not is_boiling or pitch_charges <= 0:
		return {"success": false, "reason": "NOT_READY"}
	
	pitch_charges -= 1
	is_boiling = false
	reheat_timer = REHEAT_TIME_SECONDS
	
	pitch_dumped.emit(PUDDLE_RADIUS, PITCH_DPS, BURN_DURATION_SECONDS)
	return {
		"success": true,
		"puddle_radius": PUDDLE_RADIUS,
		"burn_dps": PITCH_DPS,
		"duration": BURN_DURATION_SECONDS,
		"slow_multiplier": MOVEMENT_SLOW_MULTIPLIER,
		"remaining_charges": pitch_charges
	}

func process_reheat(delta: float) -> bool:
	if is_boiling:
		return true
	
	reheat_timer -= delta
	if reheat_timer <= 0.0 and pitch_charges > 0:
		is_boiling = true
		cauldron_reheated.emit()
		return true
	return false
