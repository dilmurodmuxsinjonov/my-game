# scripts/combat/siege_engine.gd
# Voxel Lord: Feudal Realm - Milestone 23: Castle Siege Mangonel Catapult
# Inspired by Stronghold (Mangonels & Catapults) and Mount & Blade II: Bannerlord (Siege Artillery)

class_name SiegeEngine
extends Node3D

signal catapult_fired(target_pos: Vector3, damage: float, aoe_radius: float, is_incendiary: bool)
signal catapult_reloaded(ammo_type: String)

var supply_chain: Node = null

const MIN_RANGE: float = 15.0
const MAX_RANGE: float = 65.0
const RELOAD_TIME_SECONDS: float = 8.0
const SIEGE_DAMAGE_BASE: float = 120.0
const AOE_RADIUS_METERS: float = 12.0
const INCENDIARY_BONUS_DAMAGE: float = 50.0

var current_reload_timer: float = 0.0
var is_loaded: bool = true
var loaded_ammo_type: String = "fire_boulder"
var boulders_stock: int = 12

func _init() -> void:
	pass

func fire_at_target(target_pos: Vector3) -> Dictionary:
	if not is_loaded:
		return {"success": false, "reason": "NOT_LOADED", "damage": 0.0}
	
	var dist: float = global_position.distance_to(target_pos)
	if dist < MIN_RANGE or dist > MAX_RANGE:
		return {"success": false, "reason": "OUT_OF_RANGE", "distance": dist}
	
	is_loaded = false
	current_reload_timer = RELOAD_TIME_SECONDS
	
	var is_incendiary: bool = (loaded_ammo_type == "fire_boulder")
	var total_damage: float = SIEGE_DAMAGE_BASE
	if is_incendiary:
		total_damage += INCENDIARY_BONUS_DAMAGE
	
	catapult_fired.emit(target_pos, total_damage, AOE_RADIUS_METERS, is_incendiary)
	
	return {
		"success": true,
		"damage": total_damage,
		"aoe_radius": AOE_RADIUS_METERS,
		"is_incendiary": is_incendiary,
		"target_distance": dist
	}

func reload(ammo_type: String = "fire_boulder") -> bool:
	if is_loaded:
		return false
	if boulders_stock <= 0:
		return false
	
	boulders_stock -= 1
	loaded_ammo_type = ammo_type
	is_loaded = true
	current_reload_timer = 0.0
	catapult_reloaded.emit(ammo_type)
	return true

func process_reload(delta: float) -> bool:
	if is_loaded:
		return true
	
	current_reload_timer -= delta
	if current_reload_timer <= 0.0:
		return reload(loaded_ammo_type)
	return false
