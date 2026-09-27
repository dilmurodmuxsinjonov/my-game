# scripts/mechanisms/centrifugal_governor.gd
class_name CentrifugalGovernor
extends Node3D

# James Watt Flyball Centrifugal Speed Governor
# Inspired by Create Mod, Vintage Story, and Thermal Expansion
# Regulates steam throttle valve via centrifugal flyball expansion to stabilize factory grid RPM.

signal throttle_adjusted(throttle_ratio: float)
signal overspeed_alarm(rpm: float)

@export var governor_id: String = "governor_01"
@export var target_operating_rpm: float = 64.0
@export var min_angle_deg: float = 15.0 # Dropped at rest
@export var max_angle_deg: float = 75.0 # Flung outward at max overspeed
@export var max_collar_lift_m: float = 0.25 # Vertical collar throw

var current_rpm: float = 0.0
var flyball_angle_deg: float = 15.0
var collar_lift_m: float = 0.0
var output_throttle: float = 1.0

# PID regulation constants
var kp: float = 0.02
var ki: float = 0.005
var integral_error: float = 0.0

func _init(id: String = "governor_01", target_rpm: float = 64.0):
	governor_id = id
	target_operating_rpm = target_rpm

func update_governor(engine_rpm: float, delta: float) -> Dictionary:
	current_rpm = max(0.0, engine_rpm)

	# 1. Centrifugal ball spread angle physics
	# Flyball outward spread scales with centrifugal force (proportional to omega^2)
	var speed_ratio = clamp(current_rpm / (target_operating_rpm * 1.35), 0.0, 1.2)
	var target_angle = min_angle_deg + (max_angle_deg - min_angle_deg) * (speed_ratio * speed_ratio)
	flyball_angle_deg = move_toward(flyball_angle_deg, target_angle, 60.0 * delta)

	# 2. Sliding collar lift
	var angle_fraction = (flyball_angle_deg - min_angle_deg) / (max_angle_deg - min_angle_deg)
	collar_lift_m = max_collar_lift_m * angle_fraction

	# 3. Throttle modulation (Watt mechanical feedback)
	var error = target_operating_rpm - current_rpm
	integral_error = clamp(integral_error + error * delta, -50.0, 50.0)

	var p_term = kp * error
	var i_term = ki * integral_error
	output_throttle = clamp(1.0 - (collar_lift_m / max_collar_lift_m) + (p_term + i_term), 0.05, 1.0)

	if current_rpm > target_operating_rpm * 1.3:
		overspeed_alarm.emit(current_rpm)

	throttle_adjusted.emit(output_throttle)

	return {
		"current_rpm": current_rpm,
		"flyball_angle_deg": flyball_angle_deg,
		"collar_lift_m": collar_lift_m,
		"output_throttle": output_throttle,
		"is_overspeed": current_rpm > target_operating_rpm * 1.3
	}
