# scripts/world/thermodynamic_engine.gd
# Voxel Lord: Feudal Realm - Milestone 2: Grid-Based Thermodynamics & Fire Simulation
# Simulates 3D Fourier heat conduction, chimney stack convection (up to 1400°C),
# and wind-coupled cellular automata fire spread with material ignition thresholds.

class_name ThermodynamicEngine
extends RefCounted

signal temperature_updated(pos: Vector3i, temp_celsius: float)
signal fire_ignited(pos: Vector3i, material: String)
signal fire_extinguished(pos: Vector3i)
signal voxel_consumed(pos: Vector3i, material: String)

enum BurningState {
	UNIGNITED = 0,
	HEATING = 1,
	IGNITED = 2,
	BURNING = 3,
	EXTINGUISHED = 4,
	ASH = 5
}

# Thermal conductivity k [W/(m·K)]
const THERMAL_CONDUCTIVITY: Dictionary = {
	"iron": 50.0,
	"steel": 50.0,
	"stone": 2.5,
	"granite": 2.5,
	"cobblestone": 2.0,
	"stone_bricks": 2.2,
	"brick": 0.8,
	"clay": 0.8,
	"wood": 0.15,
	"timber": 0.15,
	"planks": 0.15,
	"thatch": 0.06,
	"straw": 0.06,
	"peat": 0.12,
	"coal": 0.25,
	"water": 0.60,
	"ice": 2.22,
	"air": 0.026,
	"dirt": 0.45,
	"default": 1.0
}

# Volumetric heat capacity Cv = rho * c_p [J/(m³·K)]
const HEAT_CAPACITY: Dictionary = {
	"iron": 3500000.0,
	"steel": 3500000.0,
	"stone": 2200000.0,
	"granite": 2200000.0,
	"cobblestone": 2000000.0,
	"stone_bricks": 2100000.0,
	"brick": 1400000.0,
	"clay": 1400000.0,
	"wood": 1200000.0,
	"timber": 1200000.0,
	"planks": 1200000.0,
	"thatch": 400000.0,
	"straw": 400000.0,
	"peat": 800000.0,
	"coal": 1500000.0,
	"water": 4184000.0,
	"ice": 1930000.0,
	"air": 1200.0,
	"dirt": 1300000.0,
	"default": 1500000.0
}

# Thermal diffusivity alpha = k / (rho * c_p) [m²/s]
# Scaled for real-time cellular automata stability
const THERMAL_DIFFUSIVITY: Dictionary = {
	"iron": 1.42e-5,
	"steel": 1.42e-5,
	"stone": 1.14e-6,
	"brick": 5.71e-7,
	"wood": 1.25e-7,
	"thatch": 1.50e-7,
	"water": 1.43e-7,
	"ice": 1.15e-6,
	"air": 2.16e-5,
	"default": 1.0e-6
}

# Material auto-ignition temperatures [°C]
const IGNITION_THRESHOLDS: Dictionary = {
	"thatch": 220.0,
	"straw": 220.0,
	"wood": 300.0,
	"timber": 300.0,
	"planks": 300.0,
	"peat": 180.0,
	"coal": 180.0,
	"leaves": 190.0,
	"dirt": 99999.0,
	"stone": 99999.0,
	"cobblestone": 99999.0,
	"iron": 99999.0,
	"water": 99999.0,
	"ice": 99999.0
}

# Base cellular fire spread rates [s⁻¹]
const BASE_SPREAD_RATES: Dictionary = {
	"thatch": 0.15,
	"straw": 0.15,
	"wood": 0.05,
	"timber": 0.05,
	"planks": 0.05,
	"peat": 0.08,
	"coal": 0.08,
	"leaves": 0.12
}

# Thermal power release during combustion [kW]
const COMBUSTION_HEAT_RELEASE: Dictionary = {
	"thatch": 350.0,
	"straw": 350.0,
	"wood": 620.0,
	"timber": 620.0,
	"planks": 620.0,
	"peat": 450.0,
	"coal": 850.0,
	"leaves": 250.0
}

# Burn durations before turning into ash [seconds]
const BURN_DURATIONS: Dictionary = {
	"thatch": 8.0,
	"straw": 8.0,
	"leaves": 5.0,
	"wood": 30.0,
	"timber": 45.0,
	"planks": 25.0,
	"peat": 40.0,
	"coal": 60.0
}

const GRAVITY: float = 9.81
const DEFAULT_DISCHARGE_COEFF: float = 0.65
const MAX_CHIMNEY_TEMP: float = 1400.0

# 3D Grid State
var ambient_temperature: float = 20.0 # Celsius
var temperature_grid: Dictionary = {} # Vector3i -> float (°C)
var material_grid: Dictionary = {}    # Vector3i -> String
var heat_sources: Dictionary = {}     # Vector3i -> Dictionary {"temp": float, "power": float, "maintained": bool}
var burning_voxels: Dictionary = {}   # Vector3i -> Dictionary {"timer": float, "duration": float, "material": String, "heat_output": float, "state": int}

# Neighbor offsets in 3D grid (6-connectivity)
const NEIGHBORS_6: Array[Vector3i] = [
	Vector3i(1, 0, 0), Vector3i(-1, 0, 0),
	Vector3i(0, 1, 0), Vector3i(0, -1, 0),
	Vector3i(0, 0, 1), Vector3i(0, 0, -1)
]

func _init(p_ambient: float = 20.0) -> void:
	ambient_temperature = p_ambient

func set_ambient_temperature(temp: float) -> void:
	ambient_temperature = temp

func get_ambient_temperature() -> float:
	return ambient_temperature

func set_temperature(pos: Vector3i, temp: float) -> void:
	temperature_grid[pos] = temp
	temperature_updated.emit(pos, temp)

func get_temperature(pos: Vector3i) -> float:
	return temperature_grid.get(pos, ambient_temperature)

func set_material(pos: Vector3i, material: String) -> void:
	material_grid[pos] = material.to_lower()

func get_material(pos: Vector3i) -> String:
	return material_grid.get(pos, "air")

func add_heat_source(pos: Vector3i, target_temp: float, power: float = 1000.0, maintained: bool = true) -> void:
	heat_sources[pos] = {
		"temp": target_temp,
		"power": power,
		"maintained": maintained
	}
	set_temperature(pos, target_temp)

func remove_heat_source(pos: Vector3i) -> void:
	heat_sources.erase(pos)

func get_conductivity(material: String) -> float:
	return THERMAL_CONDUCTIVITY.get(material.to_lower(), THERMAL_CONDUCTIVITY["default"])

func get_heat_capacity(material: String) -> float:
	return HEAT_CAPACITY.get(material.to_lower(), HEAT_CAPACITY["default"])

func get_diffusivity(material: String) -> float:
	var mat = material.to_lower()
	if THERMAL_DIFFUSIVITY.has(mat):
		return THERMAL_DIFFUSIVITY[mat]
	var k = get_conductivity(mat)
	var cv = get_heat_capacity(mat)
	return k / cv if cv > 0.0 else 1.0e-6

# -------------------------------------------------------------------------
# 1. 3D Fourier Solid Heat Conduction Cellular Automata
# Equation: dT/dt = alpha * laplacian(T)
# Discrete CA: Delta_T_i = sum_j [ k_ij / (Cv_i * d) * (T_j - T_i) ] * dt
# -------------------------------------------------------------------------
func step_thermal_conduction(dt: float) -> void:
	if temperature_grid.is_empty() and heat_sources.is_empty():
		return
		
	# Gather all cells that need thermal processing (active grid + 1-ring neighbors)
	var active_cells: Dictionary = {}
	for pos in temperature_grid.keys():
		active_cells[pos] = true
		for offset in NEIGHBORS_6:
			active_cells[pos + offset] = true
			
	for pos in heat_sources.keys():
		active_cells[pos] = true
		for offset in NEIGHBORS_6:
			active_cells[pos + offset] = true

	var delta_temps: Dictionary = {}
	var grid_spacing: float = 1.0 # 1 meter voxels

	for pos in active_cells.keys():
		# Maintained heat sources stay fixed
		if heat_sources.has(pos) and heat_sources[pos].get("maintained", true):
			continue
			
		var t_self: float = get_temperature(pos)
		var mat_self: String = get_material(pos)
		var k_self: float = get_conductivity(mat_self)
		var cv_self: float = get_heat_capacity(mat_self)
		
		var net_heat_flux: float = 0.0 # W/m²
		
		for offset in NEIGHBORS_6:
			var n_pos = pos + offset
			var t_neighbor: float = get_temperature(n_pos)
			var mat_neighbor: String = get_material(n_pos)
			var k_neighbor: float = get_conductivity(mat_neighbor)
			
			# Harmonic mean for interface thermal conductivity
			var k_effective: float = (2.0 * k_self * k_neighbor) / (k_self + k_neighbor) if (k_self + k_neighbor) > 0.0 else 0.0
			
			# Fourier conduction flux: q = k * (T_neighbor - T_self) / d
			var flux = k_effective * (t_neighbor - t_self) / grid_spacing
			net_heat_flux += flux

		# dT = (net_flux / Cv) * dt
		# Scale time step for CA stability (CFL condition: alpha * dt / dx^2 <= 1/6)
		var delta_t = (net_heat_flux / cv_self) * dt * 50.0 # acceleration factor for simulation responsiveness
		
		# Clamp delta_t to prevent oscillations
		delta_t = clamp(delta_t, -150.0, 150.0)
		delta_temps[pos] = delta_t

	# Apply temperature updates
	for pos in delta_temps.keys():
		var new_temp = get_temperature(pos) + delta_temps[pos]
		temperature_grid[pos] = new_temp
		temperature_updated.emit(pos, new_temp)

	# Ensure maintained heat sources enforce exact temperature
	for pos in heat_sources.keys():
		if heat_sources[pos].get("maintained", true):
			temperature_grid[pos] = heat_sources[pos]["temp"]

# -------------------------------------------------------------------------
# 2. Vertical Chimney Stack Convection Draft Velocity (Stack Effect)
# Equation: v_draft = C_d * sqrt(2 * g * H * delta_T / T_base)
# Valid up to 1400°C in bloomeries, fireboxes, and furnaces.
# -------------------------------------------------------------------------
static func calculate_chimney_draft(
	height: float,
	t_chimney: float,
	t_ambient: float,
	cd: float = DEFAULT_DISCHARGE_COEFF,
	use_hot_base: bool = false
) -> float:
	if height <= 0.0:
		return 0.0
		
	# Convert temperatures to Kelvin if given in Celsius (< 150°C heuristic)
	var t_amb_k: float = t_ambient if t_ambient >= 150.0 else (t_ambient + 273.15)
	var t_ch_k: float = t_chimney if t_chimney >= 150.0 else (t_chimney + 273.15)
	
	var delta_t: float = t_ch_k - t_amb_k
	if delta_t <= 0.0:
		return 0.0

	var t_base: float = t_ch_k if use_hot_base else t_amb_k
	if t_base <= 0.0:
		return 0.0

	# Stack effect velocity equation
	var velocity = cd * sqrt(2.0 * GRAVITY * height * (delta_t / t_base))
	return max(0.0, velocity)

static func calculate_stack_pressure_diff(
	height: float,
	t_chimney: float,
	t_ambient: float,
	rho_amb: float = 1.204
) -> float:
	if height <= 0.0:
		return 0.0
	var t_amb_k: float = t_ambient if t_ambient >= 150.0 else (t_ambient + 273.15)
	var t_ch_k: float = t_chimney if t_chimney >= 150.0 else (t_chimney + 273.15)
	if t_ch_k <= 0.0:
		return 0.0
	return rho_amb * GRAVITY * height * (1.0 - (t_amb_k / t_ch_k))

static func calculate_convective_heat_flux(
	height: float,
	t_chimney: float,
	t_ambient: float,
	area: float = 1.0,
	cd: float = DEFAULT_DISCHARGE_COEFF
) -> float:
	var v_draft = calculate_chimney_draft(height, t_chimney, t_ambient, cd)
	var t_amb_k = t_ambient if t_ambient >= 150.0 else (t_ambient + 273.15)
	var t_ch_k = t_chimney if t_chimney >= 150.0 else (t_chimney + 273.15)
	var rho_air = 1.204 * (293.15 / t_ch_k) # density at chimney temp
	var cp_air = 1005.0 # J/(kg·K)
	var delta_t = t_ch_k - t_amb_k
	return (rho_air * area * v_draft) * cp_air * delta_t

# -------------------------------------------------------------------------
# 3. Fire Spread Cellular Automata with Wind & Moisture Coupling
# Equation: P_spread = BaseSpreadRate * (1.0 + k_w * (v_wind · d_voxel)) * (1.0 - Humidity)
# Material ignition thresholds: Thatch 220°C, Wood 300°C, Peat 180°C.
# -------------------------------------------------------------------------
func is_combustible(material: String) -> bool:
	var mat = material.to_lower()
	return IGNITION_THRESHOLDS.get(mat, 99999.0) < 5000.0

func get_ignition_threshold(material: String) -> float:
	return IGNITION_THRESHOLDS.get(material.to_lower(), 99999.0)

func get_base_spread_rate(material: String) -> float:
	return BASE_SPREAD_RATES.get(material.to_lower(), 0.05)

func evaluate_fire_spread(pos: Vector3i, wind_vec: Vector3, humidity: float) -> bool:
	var mat = get_material(pos)
	if not is_combustible(mat):
		return false
		
	# High humidity suppresses ignition
	if humidity >= 0.85:
		return false

	var temp = get_temperature(pos)
	var threshold = get_ignition_threshold(mat)
	
	# Direct thermal ignition if local temperature exceeds threshold
	if temp >= threshold:
		return true

	# Check for neighboring burning voxels
	var has_burning_neighbor = false
	var max_spread_prob: float = 0.0
	var kw: float = 0.35 # wind coupling coefficient

	for offset in NEIGHBORS_6:
		var n_pos = pos + offset
		if is_burning(n_pos):
			has_burning_neighbor = true
			var d_voxel = Vector3(-offset.x, -offset.y, -offset.z).normalized()
			var wind_alignment = wind_vec.dot(d_voxel)
			var wind_mult = max(0.1, 1.0 + kw * wind_alignment)
			var base_rate = get_base_spread_rate(mat)
			var prob = base_rate * wind_mult * (1.0 - humidity)
			max_spread_prob = max(max_spread_prob, prob)

	if not has_burning_neighbor:
		return false

	# If temperature is near ignition (> 85% of threshold), boost probability
	var heat_ratio = temp / threshold
	if heat_ratio > 0.85:
		max_spread_prob *= (1.0 + (heat_ratio - 0.85) * 4.0)

	# Probability test
	return randf() < clamp(max_spread_prob, 0.0, 1.0)

func ignite_voxel(pos: Vector3i, forced: bool = false) -> bool:
	var mat = get_material(pos)
	if not forced and not is_combustible(mat):
		return false
		
	var duration = BURN_DURATIONS.get(mat, 20.0)
	var heat_kw = COMBUSTION_HEAT_RELEASE.get(mat, 500.0)
	
	burning_voxels[pos] = {
		"timer": 0.0,
		"duration": duration,
		"material": mat,
		"heat_output": heat_kw,
		"state": BurningState.BURNING
	}
	
	# Raise local temperature to at least combustion level
	var current_t = get_temperature(pos)
	var target_fire_t = max(current_t, get_ignition_threshold(mat) + 150.0)
	set_temperature(pos, target_fire_t)
	
	fire_ignited.emit(pos, mat)
	return true

func extinguish_voxel(pos: Vector3i, cooling_amount: float = 250.0) -> void:
	if burning_voxels.has(pos):
		burning_voxels.erase(pos)
		fire_extinguished.emit(pos)
		
	var current_t = get_temperature(pos)
	set_temperature(pos, max(ambient_temperature, current_t - cooling_amount))

func is_burning(pos: Vector3i) -> bool:
	return burning_voxels.has(pos)

func get_burning_voxels() -> Array:
	return burning_voxels.keys()

func step_fire_simulation(dt: float, wind_vec: Vector3 = Vector3.ZERO, humidity: float = 0.0) -> Array[Vector3i]:
	var newly_ignited: Array[Vector3i] = []
	var finished_voxels: Array[Vector3i] = []
	
	# 1. Advance existing fires and release combustion heat
	for pos in burning_voxels.keys():
		var fire_data = burning_voxels[pos]
		fire_data["timer"] += dt
		
		# Heat injection from combustion
		var heat_release_temp = fire_data["heat_output"] * 0.1 * dt
		var current_t = get_temperature(pos)
		set_temperature(pos, min(current_t + heat_release_temp, 900.0))
		
		# Check burn out
		if fire_data["timer"] >= fire_data["duration"]:
			finished_voxels.append(pos)

	# 2. Check spread to adjacent unignited combustible voxels
	var candidates: Dictionary = {}
	for pos in burning_voxels.keys():
		for offset in NEIGHBORS_6:
			var n_pos = pos + offset
			if not is_burning(n_pos) and is_combustible(get_material(n_pos)):
				candidates[n_pos] = true

	for target_pos in candidates.keys():
		if evaluate_fire_spread(target_pos, wind_vec, humidity):
			if ignite_voxel(target_pos):
				newly_ignited.append(target_pos)

	# 3. Clean up consumed voxels -> convert to ash
	for pos in finished_voxels:
		var mat = burning_voxels[pos]["material"]
		burning_voxels.erase(pos)
		material_grid[pos] = "ash"
		voxel_consumed.emit(pos, mat)

	return newly_ignited
