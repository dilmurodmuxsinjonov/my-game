# scripts/mechanisms/cargo_crane.gd
# Voxel Lord: Feudal Realm - Milestone 33: Treadwheel Cargo Crane & Vertical Mining Logistics
# Heavy oak derrick crane with 2.6m treadwheel hoisting up to 1,200kg from depths down to 40m.

class_name CargoCrane
extends Node3D

signal crane_state_changed(new_state: CraneState)
signal depth_reached(target_depth: float)
signal overload_warning(current_weight: float, max_capacity: float)

enum CraneState {
	IDLE,
	HOISTING_UP,
	LOWERING_DOWN,
	OVERLOADED
}

const MAX_DEPTH_METERS: float = 40.0
const MAX_PAYLOAD_KG: float = 1200.0
const MANUAL_HOIST_SPEED: float = 1.2    # meters per second with treadwheel operator
const KINETIC_HOIST_SPEED: float = 2.5   # meters per second when powered by drive shaft
const STAMINA_DRAIN_PER_SEC: float = 0.15 # Worker stamina cost while operating treadwheel
const KINETIC_LOAD_SU: float = 96.0      # Kinetic stress units consumed while hoisting

@export var current_state: CraneState = CraneState.IDLE
@export var current_depth: float = 0.0   # 0.0m (surface) to 40.0m (deep quarry/shaft)
@export var target_depth: float = 0.0
@export var is_kinetic_powered: bool = false
@export var input_rpm: float = 0.0
@export var has_worker: bool = false

var cargo_inventory: Array[Dictionary] = []
var total_payload_weight: float = 0.0

func _init(p_start_depth: float = 0.0) -> void:
	current_depth = clamp(p_start_depth, 0.0, MAX_DEPTH_METERS)
	target_depth = current_depth
	current_state = CraneState.IDLE
	cargo_inventory.clear()
	total_payload_weight = 0.0

func load_cargo(item_id: String, count: int, unit_weight_kg: float) -> bool:
	var added_weight: float = float(count) * unit_weight_kg
	if total_payload_weight + added_weight > MAX_PAYLOAD_KG:
		overload_warning.emit(total_payload_weight + added_weight, MAX_PAYLOAD_KG)
		return false
		
	cargo_inventory.append({
		"item_id": item_id,
		"count": count,
		"unit_weight": unit_weight_kg,
		"total_weight": added_weight
	})
	total_payload_weight += added_weight
	return true

func unload_cargo() -> Array[Dictionary]:
	var discharged: Array[Dictionary] = cargo_inventory.duplicate(true)
	cargo_inventory.clear()
	total_payload_weight = 0.0
	if current_state == CraneState.OVERLOADED:
		current_state = CraneState.IDLE
		crane_state_changed.emit(current_state)
	return discharged

func set_worker_assigned(assigned: bool) -> void:
	has_worker = assigned

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	is_kinetic_powered = abs(input_rpm) >= 12.0

func hoist_to_surface() -> void:
	set_target_depth(0.0)

func lower_to_depth(depth_m: float) -> void:
	set_target_depth(depth_m)

func set_target_depth(depth_m: float) -> void:
	if total_payload_weight > MAX_PAYLOAD_KG:
		current_state = CraneState.OVERLOADED
		crane_state_changed.emit(current_state)
		return
		
	target_depth = clamp(depth_m, 0.0, MAX_DEPTH_METERS)
	if target_depth < current_depth:
		current_state = CraneState.HOISTING_UP
		crane_state_changed.emit(current_state)
	elif target_depth > current_depth:
		current_state = CraneState.LOWERING_DOWN
		crane_state_changed.emit(current_state)
	else:
		current_state = CraneState.IDLE
		crane_state_changed.emit(current_state)

func get_active_hoist_speed() -> float:
	if is_kinetic_powered and abs(input_rpm) > 0.0:
		return KINETIC_HOIST_SPEED
	elif has_worker:
		return MANUAL_HOIST_SPEED
	return 0.0

func calculate_stamina_drain(delta: float) -> float:
	if has_worker and not is_kinetic_powered and (current_state == CraneState.HOISTING_UP or current_state == CraneState.LOWERING_DOWN):
		return STAMINA_DRAIN_PER_SEC * delta
	return 0.0

func calculate_logistics_efficiency_gain() -> float:
	# Compared to manual staircase hauling (1.0), crane takes only 0.30 of the time (70% savings)
	return 0.70

func process_tick(delta: float) -> float:
	# Returns stamina consumed this tick
	if current_state == CraneState.IDLE or current_state == CraneState.OVERLOADED:
		return 0.0
		
	var speed: float = get_active_hoist_speed()
	if speed <= 0.0:
		return 0.0 # No power source available
		
	var stamina_used: float = calculate_stamina_drain(delta)
	
	if current_state == CraneState.HOISTING_UP:
		current_depth = max(target_depth, current_depth - speed * delta)
		if current_depth <= target_depth:
			current_depth = target_depth
			current_state = CraneState.IDLE
			crane_state_changed.emit(current_state)
			depth_reached.emit(current_depth)
	elif current_state == CraneState.LOWERING_DOWN:
		current_depth = min(target_depth, current_depth + speed * delta)
		if current_depth >= target_depth:
			current_depth = target_depth
			current_state = CraneState.IDLE
			crane_state_changed.emit(current_state)
			depth_reached.emit(current_depth)
			
	return stamina_used

func get_kinetic_load() -> float:
	if is_kinetic_powered and (current_state == CraneState.HOISTING_UP or current_state == CraneState.LOWERING_DOWN):
		return KINETIC_LOAD_SU
	return 0.0
