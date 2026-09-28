# scripts/world/fluid_hydraulics.gd
# Voxel Lord: Feudal Realm - Milestone 2: Fluid Volume Conservation & Hydraulics Engine
# Simulates conserved volume fluid flow through channels, ditches, and stone aqueducts,
# with channel conveyance losses (dirt -8%, clay -2%, stone 0% per 10m)
# and ambient freeze/thaw transitions at 0°C (water <-> BlockType.ICE).

class_name FluidHydraulics
extends RefCounted

signal fluid_transferred(from_pos: Vector3i, to_pos: Vector3i, amount: float)
signal water_frozen(pos: Vector3i, volume: float)
signal ice_thawed(pos: Vector3i, volume: float)
signal channel_overflow(pos: Vector3i, excess: float)

enum ChannelType {
	OPEN_AIR = 0,
	DIRT_DITCH = 1,
	CLAY_CANAL = 2,
	STONE_AQUEDUCT = 3
}

# Seepage loss per meter of channel travel
# Dirt Ditch: 8% per 10m (0.008/m)
# Clay Canal: 2% per 10m (0.002/m)
# Stone Aqueduct: 0% per 10m (0.0/m)
const SEEPAGE_LOSS_PER_METER: Dictionary = {
	ChannelType.OPEN_AIR: 0.015,
	ChannelType.DIRT_DITCH: 0.008,
	ChannelType.CLAY_CANAL: 0.002,
	ChannelType.STONE_AQUEDUCT: 0.0
}

# Flow velocities [m/s]
const FLOW_VELOCITIES: Dictionary = {
	ChannelType.OPEN_AIR: 1.0,
	ChannelType.DIRT_DITCH: 1.2,
	ChannelType.CLAY_CANAL: 1.8,
	ChannelType.STONE_AQUEDUCT: 3.5
}

# Freezing and melting parameters
const FREEZE_TEMP_THRESHOLD: float = 0.0 # °C
const DENSITY_RATIO_WATER_TO_ICE: float = 0.917 # Ice expansion ~9%

# Maximum volume capacity per voxel cell [m³]
const CELL_CAPACITY: float = 1.0

# 3D Grid State
var fluid_grid: Dictionary = {}    # Vector3i -> float (volume in m³)
var ice_grid: Dictionary = {}      # Vector3i -> float (frozen ice volume)
var temp_grid: Dictionary = {}     # Vector3i -> float (°C)
var channel_grid: Dictionary = {}  # Vector3i -> int (ChannelType)
var solid_grid: Dictionary = {}    # Vector3i -> bool (solid obstacle)
var inflow_sources: Dictionary = {}# Vector3i -> float (m³/s)
var drain_sinks: Dictionary = {}   # Vector3i -> float (m³/s)

var default_ambient_temp: float = 15.0

# Horizontal neighbor offsets (4-connectivity)
const LATERAL_NEIGHBORS: Array[Vector3i] = [
	Vector3i(1, 0, 0), Vector3i(-1, 0, 0),
	Vector3i(0, 0, 1), Vector3i(0, 0, -1)
]

func _init(p_ambient_temp: float = 15.0) -> void:
	default_ambient_temp = p_ambient_temp

func set_fluid_volume(pos: Vector3i, volume: float) -> void:
	if volume <= 0.0001:
		fluid_grid.erase(pos)
	else:
		fluid_grid[pos] = clamp(volume, 0.0, CELL_CAPACITY)

func get_fluid_volume(pos: Vector3i) -> float:
	return fluid_grid.get(pos, 0.0)

func set_ice_volume(pos: Vector3i, volume: float) -> void:
	if volume <= 0.0001:
		ice_grid.erase(pos)
	else:
		ice_grid[pos] = volume

func get_ice_volume(pos: Vector3i) -> float:
	return ice_grid.get(pos, 0.0)

func is_ice(pos: Vector3i) -> bool:
	return ice_grid.has(pos) and ice_grid[pos] > 0.0

func set_cell_temperature(pos: Vector3i, temp: float) -> void:
	temp_grid[pos] = temp

func get_cell_temperature(pos: Vector3i) -> float:
	return temp_grid.get(pos, default_ambient_temp)

func set_channel_type(pos: Vector3i, type: int) -> void:
	channel_grid[pos] = type

func get_channel_type(pos: Vector3i) -> int:
	return channel_grid.get(pos, ChannelType.OPEN_AIR)

func set_solid(pos: Vector3i, is_solid: bool) -> void:
	if is_solid:
		solid_grid[pos] = true
	else:
		solid_grid.erase(pos)

func is_solid(pos: Vector3i) -> bool:
	return solid_grid.get(pos, false) or is_ice(pos)

func add_inflow_source(pos: Vector3i, rate_m3_per_s: float) -> void:
	inflow_sources[pos] = rate_m3_per_s

func remove_inflow_source(pos: Vector3i) -> void:
	inflow_sources.erase(pos)

func add_drain_sink(pos: Vector3i, rate_m3_per_s: float) -> void:
	drain_sinks[pos] = rate_m3_per_s

func remove_drain_sink(pos: Vector3i) -> void:
	drain_sinks.erase(pos)

func get_total_liquid_volume() -> float:
	var total: float = 0.0
	for vol in fluid_grid.values():
		total += vol
	return total

func get_total_ice_volume() -> float:
	var total: float = 0.0
	for vol in ice_grid.values():
		total += vol
	return total

func get_total_volume() -> float:
	return get_total_liquid_volume() + get_total_ice_volume()

static func calculate_conveyance_loss(channel_type: int, distance_m: float) -> float:
	var rate = SEEPAGE_LOSS_PER_METER.get(channel_type, 0.015)
	return clamp(rate * distance_m, 0.0, 1.0)

# -------------------------------------------------------------------------
# Phase Transitions: Freezing & Seasonal Thawing
# Water freezes to BlockType.ICE (12) when T <= 0°C.
# Ice thaws back to liquid water when T > 0°C with volume conservation.
# -------------------------------------------------------------------------
func freeze_cell(pos: Vector3i) -> bool:
	var water_vol = get_fluid_volume(pos)
	if water_vol <= 0.0001:
		return false
	
	# Transition water to ice with slight volumetric expansion (1 / 0.917)
	var ice_vol = water_vol / DENSITY_RATIO_WATER_TO_ICE
	fluid_grid.erase(pos)
	ice_grid[pos] = ice_vol
	water_frozen.emit(pos, ice_vol)
	return true

func thaw_cell(pos: Vector3i) -> bool:
	var ice_vol = get_ice_volume(pos)
	if ice_vol <= 0.0001:
		return false
		
	# Transition ice back to water with exact conservation of mass
	var water_vol = min(ice_vol * DENSITY_RATIO_WATER_TO_ICE, CELL_CAPACITY)
	ice_grid.erase(pos)
	fluid_grid[pos] = water_vol
	ice_thawed.emit(pos, water_vol)
	return true

func process_freeze_thaw() -> Dictionary:
	var frozen_cells: Array[Vector3i] = []
	var thawed_cells: Array[Vector3i] = []
	
	# Check liquid water cells for freezing (T <= 0°C)
	var liquid_positions = fluid_grid.keys().duplicate()
	for pos in liquid_positions:
		var temp = get_cell_temperature(pos)
		if temp <= FREEZE_TEMP_THRESHOLD:
			if freeze_cell(pos):
				frozen_cells.append(pos)
				
	# Check ice cells for thawing (T > 0°C)
	var ice_positions = ice_grid.keys().duplicate()
	for pos in ice_positions:
		var temp = get_cell_temperature(pos)
		if temp > FREEZE_TEMP_THRESHOLD:
			if thaw_cell(pos):
				thawed_cells.append(pos)
				
	return {
		"frozen": frozen_cells,
		"thawed": thawed_cells
	}

# -------------------------------------------------------------------------
# Fluid Volume Conservation Simulation Step
# Flow rules:
# 1. Downward gravity flow into cell below
# 2. Horizontal pressure equalization between adjacent channel cells
# 3. Conveyance loss subtraction based on channel lining material
# -------------------------------------------------------------------------
func step_fluid_simulation(dt: float) -> void:
	# 1. Process ambient thermal freeze/thaw state changes
	process_freeze_thaw()
	
	# 2. Add inflows from sources
	for pos in inflow_sources.keys():
		if not is_ice(pos) and not is_solid(pos):
			var current = get_fluid_volume(pos)
			var added = inflow_sources[pos] * dt
			set_fluid_volume(pos, min(current + added, CELL_CAPACITY))

	if fluid_grid.is_empty():
		return

	# 3. Compute volume exchanges with strict mass conservation
	var active_positions = fluid_grid.keys().duplicate()
	var net_changes: Dictionary = {} # Vector3i -> float
	
	# Helper to accumulate transfer
	var transfer = func(from_p: Vector3i, to_p: Vector3i, amount: float):
		if amount <= 0.0001:
			return
		net_changes[from_p] = net_changes.get(from_p, 0.0) - amount
		net_changes[to_p] = net_changes.get(to_p, 0.0) + amount
		fluid_transferred.emit(from_p, to_p, amount)

	for pos in active_positions:
		var v_self = get_fluid_volume(pos) + net_changes.get(pos, 0.0)
		if v_self <= 0.0001:
			continue

		var channel_t = get_channel_type(pos)
		var flow_speed = FLOW_VELOCITIES.get(channel_t, 1.0)
		var max_flow_rate = flow_speed * dt

		# A. Downward Gravity Flow (-Y)
		var below_pos = pos + Vector3i(0, -1, 0)
		if not is_solid(below_pos) and not is_ice(below_pos):
			var v_below = get_fluid_volume(below_pos) + net_changes.get(below_pos, 0.0)
			var space_below = max(0.0, CELL_CAPACITY - v_below)
			if space_below > 0.0001:
				var flow_down = min(v_self, space_below, max_flow_rate * 2.0)
				transfer.call(pos, below_pos, flow_down)
				v_self -= flow_down

		if v_self <= 0.0001:
			continue

		# B. Lateral Horizontal Flow (+X, -X, +Z, -Z)
		# Distribute based on hydrostatic head differences
		var eligible_neighbors: Array[Vector3i] = []
		var total_head_diff: float = 0.0
		
		for offset in LATERAL_NEIGHBORS:
			var n_pos = pos + offset
			if not is_solid(n_pos) and not is_ice(n_pos):
				var v_neighbor = get_fluid_volume(n_pos) + net_changes.get(n_pos, 0.0)
				if v_self > v_neighbor + 0.001:
					eligible_neighbors.append(n_pos)
					total_head_diff += (v_self - v_neighbor)

		if not eligible_neighbors.is_empty() and total_head_diff > 0.0:
			var total_transfer_budget = min(v_self * 0.5, max_flow_rate)
			for n_pos in eligible_neighbors:
				var v_neighbor = get_fluid_volume(n_pos) + net_changes.get(n_pos, 0.0)
				var head_diff = v_self - v_neighbor
				var proportion = head_diff / total_head_diff
				var raw_flow = total_transfer_budget * proportion
				
				# Conveyance seepage loss applied during transit
				var loss_factor = calculate_conveyance_loss(channel_t, 1.0) # 1 meter segment
				var delivered_flow = raw_flow * (1.0 - loss_factor)
				
				net_changes[pos] = net_changes.get(pos, 0.0) - raw_flow
				net_changes[n_pos] = net_changes.get(n_pos, 0.0) + delivered_flow
				fluid_transferred.emit(pos, n_pos, delivered_flow)

	# 4. Apply net changes to the fluid grid
	for pos in net_changes.keys():
		var final_vol = get_fluid_volume(pos) + net_changes[pos]
		if final_vol > CELL_CAPACITY:
			channel_overflow.emit(pos, final_vol - CELL_CAPACITY)
			final_vol = CELL_CAPACITY
		set_fluid_volume(pos, max(0.0, final_vol))

	# 5. Process drain sinks
	for pos in drain_sinks.keys():
		var vol = get_fluid_volume(pos)
		if vol > 0.0:
			var drain_amt = min(vol, drain_sinks[pos] * dt)
			set_fluid_volume(pos, vol - drain_amt)
