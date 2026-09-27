# scripts/mechanisms/steam_boiler.gd
class_name SteamBoiler
extends Node3D

# High-Pressure Multi-Tube Industrial Steam Boiler
# Inspired by Create Mod, Vintage Story, and Thermal Expansion
# Generates high-enthalpy pressurized steam to drive central factory power grids.

signal overpressure_warning(pressure_bar: float)
signal boiler_exploded()
signal water_low_warning()
signal fuel_exhausted()

@export var boiler_id: String = "boiler_01"
@export var fuel_capacity_kg: float = 120.0
@export var water_capacity_l: float = 1000.0
@export var max_safe_pressure_bar: float = 16.0
@export var popoff_relief_bar: float = 15.0
@export var explosion_limit_bar: float = 20.0

var fuel_amount_kg: float = 40.0
var water_amount_l: float = 600.0
var current_pressure_bar: float = 0.0
var firebox_temp_c: float = 20.0
var steam_output_rate_m3_s: float = 0.0
var popoff_active: bool = false
var is_exploded: bool = false

func _init(id: String = "boiler_01"):
	boiler_id = id

func add_fuel(kg: float) -> float:
	var space = fuel_capacity_kg - fuel_amount_kg
	var added = min(kg, space)
	fuel_amount_kg += added
	return added

func add_water(liters: float) -> float:
	var space = water_capacity_l - water_amount_l
	var added = min(liters, space)
	water_amount_l += added
	return added

func process_boiler(delta: float, steam_demand_m3_s: float = 0.0) -> Dictionary:
	if is_exploded:
		return {"is_exploded": true, "current_pressure_bar": 0.0}

	# 1. Firebox heat dynamics
	if fuel_amount_kg > 0.0:
		var burn_rate_kg_s: float = 0.05
		var fuel_used = min(fuel_amount_kg, burn_rate_kg_s * delta)
		fuel_amount_kg -= fuel_used
		firebox_temp_c = move_toward(firebox_temp_c, 850.0, 35.0 * delta)
		if fuel_amount_kg <= 0.0:
			fuel_exhausted.emit()
	else:
		firebox_temp_c = move_toward(firebox_temp_c, 20.0, 10.0 * delta)

	# 2. Water evaporation and steam generation
	if firebox_temp_c > 100.0 and water_amount_l > 0.0:
		var heat_ratio = (firebox_temp_c - 100.0) / 750.0
		var evap_l_s = 0.15 * heat_ratio
		var water_used = min(water_amount_l, evap_l_s * delta)
		water_amount_l -= water_used
		if water_amount_l < 50.0:
			water_low_warning.emit()

		# Pressure accumulation
		var pressure_gain = 0.85 * heat_ratio * delta
		current_pressure_bar += pressure_gain
	else:
		current_pressure_bar = max(0.0, current_pressure_bar - 0.1 * delta)

	# 3. Steam delivery to engine
	if steam_demand_m3_s > 0.0 and current_pressure_bar > 1.0:
		var delivered = min(current_pressure_bar * 0.25, steam_demand_m3_s)
		steam_output_rate_m3_s = delivered
		current_pressure_bar = max(0.0, current_pressure_bar - (delivered * 0.4 * delta))
	else:
		steam_output_rate_m3_s = 0.0

	# 4. Popoff safety valve & overpressure catastrophe
	if current_pressure_bar >= popoff_relief_bar:
		popoff_active = true
		current_pressure_bar = max(popoff_relief_bar - 0.5, current_pressure_bar - 3.5 * delta)
		overpressure_warning.emit(current_pressure_bar)
	else:
		popoff_active = false

	if current_pressure_bar >= explosion_limit_bar:
		is_exploded = true
		current_pressure_bar = 0.0
		boiler_exploded.emit()

	return {
		"current_pressure_bar": current_pressure_bar,
		"firebox_temp_c": firebox_temp_c,
		"water_amount_l": water_amount_l,
		"fuel_amount_kg": fuel_amount_kg,
		"steam_output_rate_m3_s": steam_output_rate_m3_s,
		"popoff_active": popoff_active,
		"is_exploded": is_exploded
	}
