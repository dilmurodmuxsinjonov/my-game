# scripts/mechanisms/mining_capstan.gd
# Voxel Lord: Feudal Realm - Milestone 36: Underground Incline Capstan Hoist Winch
# Geared timber capstan hauling loaded ore carts up steep 30-degree mine incline winzes.

class_name MiningCapstan
extends Node3D

signal haul_progress_updated(current_dist: float, target_dist: float)
signal haul_arrived()
signal overload_halt(payload_kg: float, max_capacity: float)

enum CapstanState {
	IDLE,
	HAULING_UP,
	LOWERING_DOWN,
	OVERLOADED
}

const KINETIC_LOAD_SU: float = 40.0
const MAX_CAPACITY_KG: float = 1500.0
const KINETIC_HAUL_SPEED: float = 1.0    # m/s
const MANUAL_HAUL_SPEED: float = 0.35   # m/s with 2 miners
const MAX_INCLINE_TRACK_M: float = 50.0

@export var current_state: CapstanState = CapstanState.IDLE
@export var is_kinetic_powered: bool = false
@export var input_rpm: float = 0.0
@export var has_manual_miners: bool = false
@export var current_distance_m: float = 0.0
@export var target_distance_m: float = 0.0
@export var payload_weight_kg: float = 0.0

func _init(p_track_length: float = 40.0) -> void:
	current_distance_m = 0.0
	target_distance_m = clamp(p_track_length, 0.0, MAX_INCLINE_TRACK_M)
	current_state = CapstanState.IDLE
	is_kinetic_powered = false
	input_rpm = 0.0
	has_manual_miners = false
	payload_weight_kg = 0.0

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	is_kinetic_powered = abs(input_rpm) >= 12.0

func set_miners_assigned(assigned: bool) -> void:
	has_manual_miners = assigned

func load_minecart(weight_kg: float) -> bool:
	if weight_kg > MAX_CAPACITY_KG:
		current_state = CapstanState.OVERLOADED
		overload_halt.emit(weight_kg, MAX_CAPACITY_KG)
		return false
	payload_weight_kg = weight_kg
	return true

func start_haul_up() -> bool:
	if payload_weight_kg > MAX_CAPACITY_KG:
		current_state = CapstanState.OVERLOADED
		return false
	current_state = CapstanState.HAULING_UP
	return true

func get_active_haul_speed() -> float:
	if is_kinetic_powered and abs(input_rpm) > 0.0:
		return KINETIC_HAUL_SPEED
	elif has_manual_miners:
		return MANUAL_HAUL_SPEED
	return 0.0

func process_tick(delta: float) -> void:
	if current_state != CapstanState.HAULING_UP:
		return

	var speed: float = get_active_haul_speed()
	if speed <= 0.0:
		return # Pawl holds cart in place; no movement

	current_distance_m = min(target_distance_m, current_distance_m + speed * delta)
	haul_progress_updated.emit(current_distance_m, target_distance_m)

	if current_distance_m >= target_distance_m:
		current_state = CapstanState.IDLE
		haul_arrived.emit()

func get_kinetic_load() -> float:
	return KINETIC_LOAD_SU if (current_state == CapstanState.HAULING_UP and is_kinetic_powered) else 0.0
