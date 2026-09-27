# scripts/mechanisms/mine_ventilator.gd
# Voxel Lord: Feudal Realm - Milestone 36: Centrifugal Mine Air Ventilation Impeller
# Snail-shell centrifugal blower fan forcing fresh air through wooden ducts to purge toxic mine gases.

class_name MineVentilator
extends Node3D

signal airflow_rate_changed(airflow_rate: float)
signal ventilation_status_changed(is_active: bool, clearance_radius: float)

const KINETIC_LOAD_SU: float = 32.0
const MIN_OPERATING_RPM: float = 18.0
const RATED_AIRFLOW: float = 0.75       # m^3/s at 24 RPM
const MAX_CLEARANCE_RADIUS_M: float = 24.0

@export var is_operating: bool = false
@export var input_rpm: float = 0.0
@export var active_clearance_radius: float = 0.0
@export var current_airflow: float = 0.0

func _init() -> void:
	is_operating = false
	input_rpm = 0.0
	active_clearance_radius = 0.0
	current_airflow = 0.0

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	if abs(input_rpm) >= MIN_OPERATING_RPM:
		is_operating = true
		var speed_ratio: float = clamp(abs(input_rpm) / 24.0, 0.5, 2.0)
		current_airflow = RATED_AIRFLOW * speed_ratio
		active_clearance_radius = MAX_CLEARANCE_RADIUS_M * min(1.0, speed_ratio)
	else:
		is_operating = false
		current_airflow = 0.0
		active_clearance_radius = 0.0

	airflow_rate_changed.emit(current_airflow)
	ventilation_status_changed.emit(is_operating, active_clearance_radius)

func get_kinetic_load() -> float:
	return KINETIC_LOAD_SU if is_operating else 0.0

func is_area_ventilated(distance_from_vent: float) -> bool:
	return is_operating and distance_from_vent <= active_clearance_radius

func calculate_gas_toxicity_mitigation(raw_gas_ppm: float, distance: float) -> float:
	if not is_area_ventilated(distance):
		return raw_gas_ppm # No mitigation: lethal gas remains
	# Purges 95% of toxic gas in ventilated envelope
	return raw_gas_ppm * 0.05
