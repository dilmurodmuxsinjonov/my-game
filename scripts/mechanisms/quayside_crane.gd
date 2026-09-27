# scripts/mechanisms/quayside_crane.gd
class_name QuaysideCrane
extends Node3D

# Medieval Harbor Quayside Jib Crane on Stone Plinth
# Inspired by Anno 1404, Port Royale, and Create Mod
# Unloads heavy cargo crates, timber balks, and trade barrels from ships into harbor depots.

signal cargo_hoisted(payload_kg: float)
signal cargo_discharged(payload_kg: float)
signal crane_overloaded(payload_kg: float)

@export var crane_id: String = "quayside_crane_01"
@export var max_hoist_capacity_kg: float = 2500.0
@export var kinetic_power_su: float = 48.0
@export var min_kinetic_rpm: float = 16.0

@export var hoist_speed_kinetic_m_s: float = 1.2
@export var hoist_speed_manual_m_s: float = 0.4
@export var slew_speed_kinetic_deg_s: float = 45.0
@export var slew_speed_manual_deg_s: float = 15.0

var is_kinetic_powered: bool = false
var input_rpm: float = 0.0
var operating_crew: int = 0 # 0 to 2 dockworkers

var current_slew_deg: float = 0.0 # -90 (ship hatch) to +90 (quay cart)
var target_slew_deg: float = 0.0
var current_hook_height_m: float = 1.0 # 0.0 (deck) to 4.0 (overhead)
var target_hook_height_m: float = 1.0

var is_holding_cargo: bool = false
var current_payload_kg: float = 0.0
var total_cargo_handled_kg: float = 0.0

func _init(id: String = "quayside_crane_01"):
	crane_id = id

func connect_kinetic_power(rpm: float) -> void:
	input_rpm = rpm
	is_kinetic_powered = (rpm >= min_kinetic_rpm)

func assign_dockworkers(crew: int) -> void:
	operating_crew = clamp(crew, 0, 2)

func can_operate() -> bool:
	return is_kinetic_powered or operating_crew > 0

func attach_cargo(payload_kg: float) -> bool:
	if is_holding_cargo:
		return false
	if payload_kg > max_hoist_capacity_kg:
		crane_overloaded.emit(payload_kg)
		return false

	is_holding_cargo = true
	current_payload_kg = payload_kg
	cargo_hoisted.emit(payload_kg)
	return true

func discharge_cargo() -> Dictionary:
	if not is_holding_cargo:
		return {"success": false, "payload_kg": 0.0}

	var released = current_payload_kg
	total_cargo_handled_kg += released
	is_holding_cargo = false
	current_payload_kg = 0.0
	cargo_discharged.emit(released)
	return {"success": true, "payload_kg": released}

func set_targets(target_slew: float, target_height: float) -> void:
	target_slew_deg = clamp(target_slew, -90.0, 90.0)
	target_hook_height_m = clamp(target_height, 0.0, 4.5)

func get_turnaround_time_reduction() -> float:
	# 65% faster vessel turnaround when powered kinetically, 40% when operated manually
	if is_kinetic_powered:
		return 0.65
	elif operating_crew >= 2:
		return 0.40
	elif operating_crew == 1:
		return 0.25
	return 0.0

func process_crane(delta: float) -> Dictionary:
	if not can_operate():
		return {
			"can_operate": false,
			"current_slew_deg": current_slew_deg,
			"current_hook_height_m": current_hook_height_m,
			"is_holding_cargo": is_holding_cargo,
			"current_payload_kg": current_payload_kg
		}

	var hoist_speed = hoist_speed_kinetic_m_s if is_kinetic_powered else (hoist_speed_manual_m_s * float(operating_crew) * 0.5)
	var slew_speed = slew_speed_kinetic_deg_s if is_kinetic_powered else (slew_speed_manual_deg_s * float(operating_crew) * 0.5)

	# Move hook height
	current_hook_height_m = move_toward(current_hook_height_m, target_hook_height_m, hoist_speed * delta)

	# Rotate boom slewing
	current_slew_deg = move_toward(current_slew_deg, target_slew_deg, slew_speed * delta)

	return {
		"can_operate": true,
		"is_kinetic_powered": is_kinetic_powered,
		"operating_crew": operating_crew,
		"current_slew_deg": current_slew_deg,
		"current_hook_height_m": current_hook_height_m,
		"is_holding_cargo": is_holding_cargo,
		"current_payload_kg": current_payload_kg,
		"turnaround_reduction": get_turnaround_time_reduction(),
		"total_cargo_handled_kg": total_cargo_handled_kg
	}
