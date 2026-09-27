# scripts/mechanisms/mine_dewatering_pump.gd
# Voxel Lord: Feudal Realm - Milestone 36: Chain-and-Bucket Mine Dewatering Pump
# Endless chain with copper scoops lifting groundwater seepage from deep mine shafts to surface flumes.

class_name MineDewateringPump
extends Node3D

signal water_pumped(liters: float)
signal water_level_updated(current_liters: float, is_flooded: bool)

const KINETIC_LOAD_SU: float = 48.0
const MIN_OPERATING_RPM: float = 16.0
const PUMPING_RATE_L_PER_SEC: float = 2.5 # 150 Liters per minute at rated RPM
const MAX_SUMP_CAPACITY_L: float = 2000.0 # Liters before adit is declared flooded

@export var is_operating: bool = false
@export var input_rpm: float = 0.0
@export var current_water_liters: float = 0.0
@export var seepage_rate_l_per_sec: float = 1.667 # 100 L/min natural groundwater influx

func _init(p_start_water: float = 0.0, p_seepage: float = 1.667) -> void:
	current_water_liters = clamp(p_start_water, 0.0, MAX_SUMP_CAPACITY_L)
	seepage_rate_l_per_sec = max(0.0, p_seepage)
	is_operating = false
	input_rpm = 0.0

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	is_operating = abs(input_rpm) >= MIN_OPERATING_RPM

func get_kinetic_load() -> float:
	return KINETIC_LOAD_SU if is_operating else 0.0

func get_effective_pump_rate() -> float:
	if not is_operating or abs(input_rpm) <= 0.0:
		return 0.0
	var speed_ratio: float = clamp(abs(input_rpm) / 20.0, 0.5, 2.0)
	return PUMPING_RATE_L_PER_SEC * speed_ratio

func process_tick(delta: float) -> void:
	# Add natural groundwater seepage
	current_water_liters = min(MAX_SUMP_CAPACITY_L, current_water_liters + seepage_rate_l_per_sec * delta)

	# Drain water via pump if running
	if is_operating and current_water_liters > 0.0:
		var pump_capacity: float = get_effective_pump_rate() * delta
		var actual_pumped: float = min(current_water_liters, pump_capacity)
		current_water_liters = max(0.0, current_water_liters - actual_pumped)
		water_pumped.emit(actual_pumped)

	var is_flooded: bool = current_water_liters >= (MAX_SUMP_CAPACITY_L * 0.8)
	water_level_updated.emit(current_water_liters, is_flooded)

func is_mine_dry() -> bool:
	return current_water_liters < (MAX_SUMP_CAPACITY_L * 0.25)
