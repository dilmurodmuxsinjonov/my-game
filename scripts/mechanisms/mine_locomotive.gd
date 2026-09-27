# scripts/mechanisms/mine_locomotive.gd
class_name MineLocomotive
extends Node3D

# Narrow-Gauge Industrial Steam Mine Locomotive
# Inspired by Create Mod, Railcraft, and Vintage Story
# Transports bulk minerals and materials between subterranean extraction and surface foundries.

signal boiler_pressure_warning(pressure_bar: float)
signal fuel_depleted()
signal speed_changed(speed_m_s: float)

@export var fuel_capacity_kg: float = 60.0
@export var fuel_amount_kg: float = 25.0
@export var water_capacity_liters: float = 400.0
@export var water_amount_liters: float = 250.0

@export var max_boiler_pressure_bar: float = 14.0
@export var safety_valve_popoff_bar: float = 12.0
@export var optimal_working_pressure_bar: float = 8.0

@export var locomotive_tare_weight_kg: float = 3500.0
@export var max_towed_mass_kg: float = 7200.0 # Up to 6 loaded 1200kg hopper carts
@export var max_speed_m_s: float = 4.5 # 16.2 km/h
@export var tractive_effort_max_n: float = 8500.0 # Maximum tractive effort

var firebox_temp_c: float = 20.0
var boiler_pressure_bar: float = 0.0
var throttle: float = 0.0 # -1.0 (full reverse) to +1.0 (full forward)
var brake_engaged: bool = true
var current_speed_m_s: float = 0.0

var coupled_carts: int = 0
var coupled_payload_mass_kg: float = 0.0
var safety_valve_active: bool = false
var total_distance_traveled_m: float = 0.0

func _init(initial_fuel: float = 25.0, initial_water: float = 250.0):
	fuel_amount_kg = clamp(initial_fuel, 0.0, fuel_capacity_kg)
	water_amount_liters = clamp(initial_water, 0.0, water_capacity_liters)

func add_fuel(amount_kg: float) -> bool:
	if amount_kg <= 0.0 or fuel_amount_kg >= fuel_capacity_kg:
		return false
	fuel_amount_kg = min(fuel_amount_kg + amount_kg, fuel_capacity_kg)
	return true

func add_water(amount_liters: float) -> bool:
	if amount_liters <= 0.0 or water_amount_liters >= water_capacity_liters:
		return false
	water_amount_liters = min(water_amount_liters + amount_liters, water_capacity_liters)
	return true

func set_throttle(value: float) -> void:
	throttle = clamp(value, -1.0, 1.0)

func set_brake(engaged: bool) -> void:
	brake_engaged = engaged

func couple_cart(cart_mass_kg: float) -> bool:
	if coupled_carts >= 6:
		return false
	if coupled_payload_mass_kg + cart_mass_kg > max_towed_mass_kg:
		return false
	coupled_carts += 1
	coupled_payload_mass_kg += cart_mass_kg
	return true

func uncouple_cart(cart_mass_kg: float) -> bool:
	if coupled_carts <= 0:
		return false
	coupled_carts -= 1
	coupled_payload_mass_kg = max(0.0, coupled_payload_mass_kg - cart_mass_kg)
	return true

func process_locomotive(delta: float) -> Dictionary:
	# 1. Firebox and Combustion Simulation
	var fuel_burn_rate_kg_s: float = 0.0
	if fuel_amount_kg > 0.0:
		# Combustion rate scales with draft (air draft scales with speed/throttle)
		var draft_multiplier: float = 1.0 + abs(throttle) * 1.5
		fuel_burn_rate_kg_s = 0.04 * draft_multiplier
		var fuel_consumed: float = min(fuel_amount_kg, fuel_burn_rate_kg_s * delta)
		fuel_amount_kg -= fuel_consumed
		if fuel_amount_kg <= 0.0:
			fuel_depleted.emit()
		
		# Target firebox temperature: up to 850°C
		var target_firebox_c: float = 20.0 + 830.0 * (1.0 if fuel_amount_kg > 0.0 else 0.0)
		firebox_temp_c = move_toward(firebox_temp_c, target_firebox_c, 45.0 * delta)
	else:
		firebox_temp_c = move_toward(firebox_temp_c, 20.0, 15.0 * delta)

	# 2. Boiler Steam Generation and Pressure Dynamics
	var water_evaporated_l_s: float = 0.0
	if firebox_temp_c > 100.0 and water_amount_liters > 0.0:
		var heat_ratio: float = (firebox_temp_c - 100.0) / 750.0
		water_evaporated_l_s = 0.08 * heat_ratio
		var water_used: float = min(water_amount_liters, water_evaporated_l_s * delta)
		water_amount_liters -= water_used

		# Steam generation raises pressure
		var steam_pressure_gain: float = 0.65 * heat_ratio * delta
		boiler_pressure_bar = min(max_boiler_pressure_bar, boiler_pressure_bar + steam_pressure_gain)
	else:
		boiler_pressure_bar = max(0.0, boiler_pressure_bar - 0.05 * delta)

	# 3. Steam Consumption by Cylinders
	var steam_consumed_bar: float = abs(throttle) * 0.35 * (boiler_pressure_bar / optimal_working_pressure_bar) * delta
	boiler_pressure_bar = max(0.0, boiler_pressure_bar - steam_consumed_bar)

	# 4. Safety Popoff Valve (Overpressure Protection)
	if boiler_pressure_bar >= safety_valve_popoff_bar:
		safety_valve_active = true
		boiler_pressure_bar = max(safety_valve_popoff_bar - 0.5, boiler_pressure_bar - 2.5 * delta)
		boiler_pressure_warning.emit(boiler_pressure_bar)
	else:
		safety_valve_active = false

	# 5. Tractive Effort & Train Dynamics
	var total_train_mass_kg: float = locomotive_tare_weight_kg + coupled_payload_mass_kg
	var tractive_force_n: float = 0.0

	if not brake_engaged and boiler_pressure_bar > 1.5:
		var pressure_factor: float = clamp(boiler_pressure_bar / optimal_working_pressure_bar, 0.0, 1.25)
		tractive_force_n = throttle * tractive_effort_max_n * pressure_factor

	# Resistance and Acceleration
	# Rolling resistance (~0.003 * mass * g)
	var rolling_resistance_n: float = total_train_mass_kg * 9.81 * 0.003
	var net_force_n: float = 0.0

	if brake_engaged:
		# Braking applies strong retarding force
		var brake_force_n: float = 12000.0
		if abs(current_speed_m_s) > 0.01:
			var brake_dir: float = -sign(current_speed_m_s)
			current_speed_m_s = move_toward(current_speed_m_s, 0.0, (brake_force_n / total_train_mass_kg) * delta)
		else:
			current_speed_m_s = 0.0
	else:
		if abs(tractive_force_n) > rolling_resistance_n:
			net_force_n = tractive_force_n - (sign(tractive_force_n) * rolling_resistance_n)
		else:
			# Coasting down under resistance
			net_force_n = -sign(current_speed_m_s) * rolling_resistance_n if abs(current_speed_m_s) > 0.05 else 0.0

		var acceleration_m_s2: float = net_force_n / total_train_mass_kg
		current_speed_m_s = clamp(current_speed_m_s + acceleration_m_s2 * delta, -max_speed_m_s, max_speed_m_s)

	total_distance_traveled_m += abs(current_speed_m_s) * delta
	speed_changed.emit(current_speed_m_s)

	return {
		"fuel_amount_kg": fuel_amount_kg,
		"water_amount_liters": water_amount_liters,
		"firebox_temp_c": firebox_temp_c,
		"boiler_pressure_bar": boiler_pressure_bar,
		"throttle": throttle,
		"brake_engaged": brake_engaged,
		"current_speed_m_s": current_speed_m_s,
		"coupled_carts": coupled_carts,
		"total_train_mass_kg": total_train_mass_kg,
		"tractive_force_n": tractive_force_n,
		"safety_valve_active": safety_valve_active,
		"total_distance_traveled_m": total_distance_traveled_m
	}
