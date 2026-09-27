# scripts/mechanisms/steam_engine_drive.gd
class_name SteamEngineDrive
extends Node3D

# Horizontal Stationary Double-Acting Steam Engine Drive
# Inspired by Create Mod, Vintage Story, and Thermal Expansion
# Converts high-pressure steam into 1,024 SU rotational shaft power for factory grids.

signal engine_rpm_changed(rpm: float)
signal engine_stalled()

@export var engine_id: String = "steam_engine_01"
@export var rated_capacity_su: float = 1024.0
@export var rated_rpm: float = 64.0
@export var optimal_inlet_pressure_bar: float = 12.0
@export var flywheel_inertia_mass: float = 450.0 # Flywheel momentum

var throttle_opening: float = 1.0 # 0.0 to 1.0 (controlled by governor or driver)
var inlet_pressure_bar: float = 0.0
var current_rpm: float = 0.0
var current_su_output: float = 0.0
var steam_consumed_m3_s: float = 0.0

func _init(id: String = "steam_engine_01"):
	engine_id = id

func set_throttle(val: float) -> void:
	throttle_opening = clamp(val, 0.0, 1.0)

func supply_steam(pressure_bar: float) -> void:
	inlet_pressure_bar = max(0.0, pressure_bar)

func process_engine(delta: float) -> Dictionary:
	var target_rpm: float = 0.0
	if inlet_pressure_bar > 1.5 and throttle_opening > 0.01:
		var pressure_ratio = clamp(inlet_pressure_bar / optimal_inlet_pressure_bar, 0.0, 1.35)
		target_rpm = rated_rpm * pressure_ratio * throttle_opening
		current_su_output = rated_capacity_su * pressure_ratio * throttle_opening
		steam_consumed_m3_s = 0.45 * pressure_ratio * throttle_opening
	else:
		target_rpm = 0.0
		current_su_output = 0.0
		steam_consumed_m3_s = 0.0
		if current_rpm > 1.0 and target_rpm <= 0.01:
			engine_stalled.emit()

	# Flywheel inertia acceleration/deceleration
	var inertia_accel = (rated_rpm / (flywheel_inertia_mass * 0.02)) * delta
	current_rpm = move_toward(current_rpm, target_rpm, inertia_accel)
	engine_rpm_changed.emit(current_rpm)

	return {
		"current_rpm": current_rpm,
		"current_su_output": current_su_output,
		"throttle_opening": throttle_opening,
		"inlet_pressure_bar": inlet_pressure_bar,
		"steam_consumed_m3_s": steam_consumed_m3_s
	}
