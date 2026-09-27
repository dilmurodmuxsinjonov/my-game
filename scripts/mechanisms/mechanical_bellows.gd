# scripts/mechanisms/mechanical_bellows.gd
# Voxel Lord: Feudal Realm - Milestone 35: Mechanical Cam-Driven Bellows
# Double-acting leather accordion bellows driven by kinetic camshaft for forced furnace draft.

class_name MechanicalBellows
extends Node3D

signal airflow_changed(airflow_rate: float)
signal temperature_boost_updated(target_temp: float)

const BASE_TEMP: float = 1100.0         # Baseline charcoal draft without forced blast
const MAX_BOOST_TEMP: float = 1550.0    # Forced blast temperature enabling crucible steel
const KINETIC_LOAD_SU: float = 32.0     # Kinetic stress units consumed while pumping
const MIN_OPERATING_RPM: float = 12.0
const RATED_AIRFLOW: float = 0.45       # m^3/s airflow at 24 RPM

@export var is_operating: bool = false
@export var input_rpm: float = 0.0
@export var current_airflow: float = 0.0
@export var furnace_blast_temp: float = BASE_TEMP

func _init() -> void:
	is_operating = false
	input_rpm = 0.0
	current_airflow = 0.0
	furnace_blast_temp = BASE_TEMP

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	if abs(input_rpm) >= MIN_OPERATING_RPM:
		is_operating = true
		# Airflow scales with RPM ratio (normalized to 24 RPM)
		var rpm_ratio: float = clamp(abs(input_rpm) / 24.0, 0.5, 2.0)
		current_airflow = RATED_AIRFLOW * rpm_ratio
		furnace_blast_temp = lerp(BASE_TEMP, MAX_BOOST_TEMP, clamp((abs(input_rpm) - MIN_OPERATING_RPM) / 12.0, 0.0, 1.0))
	else:
		is_operating = false
		current_airflow = 0.0
		furnace_blast_temp = BASE_TEMP

	airflow_changed.emit(current_airflow)
	temperature_boost_updated(furnace_blast_temp)

func get_kinetic_load() -> float:
	return KINETIC_LOAD_SU if is_operating else 0.0

func can_smelt_high_temp_metals() -> bool:
	return furnace_blast_temp >= 1400.0

func get_smelting_speed_multiplier() -> float:
	return 2.5 if is_operating else 1.0
