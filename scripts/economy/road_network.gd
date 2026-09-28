# scripts/economy/road_network.gd
# Voxel Lord: Feudal Realm - Milestone 5: Logistics Friction & Road Networks
# Realism transport friction: unpaved mud roads penalize haul velocity by -50% (0.50x speed, 2.0x cost)
# while paved cobblestone highways provide +40% speed boost (1.40x speed, 0.714x cost),
# producing an A* traversal cost ratio of exactly 2.80x.

class_name RoadNetwork
extends RefCounted

signal road_paved(pos: Vector3i, surface: int)
signal road_upgraded(pos: Vector3i, old_surface: int, new_surface: int)
signal road_degraded(pos: Vector3i, current_durability: float)
signal road_churned_to_mud(pos: Vector3i)
signal road_repaired(pos: Vector3i)

## Surface classification according to Total Realism Architecture specifications
enum SurfaceType {
	MUD_UNPAVED = 0,        # Unpaved mud / churned clay: -50% speed (0.50x), 2.0x cost
	WILD_GRASS = 1,         # Baseline natural off-road terrain: 1.00x speed, 1.0x cost
	DIRT_TRAIL = 2,         # Beaten dirt path: +15% speed (1.15x), ~0.8696x cost
	GRAVEL_ROAD = 3,        # Compacted crushed gravel: +25% speed (1.25x), 0.80x cost
	COBBLESTONE_PAVED = 4,  # Paved stone highway: +40% speed (1.40x), ~0.7143x cost
	ROYAL_HIGHWAY = 5       # Engineered royal granite avenue: +60% speed (1.60x), 0.625x cost
}

## Backward compatibility alias for RoadTier
enum RoadTier {
	MUD_UNPAVED = 0,
	NONE = 1,
	DIRT_PATH = 2,
	GRAVEL_ROAD = 3,
	COBBLESTONE_PAVED = 4,
	ROYAL_HIGHWAY = 5
}

## Speed multipliers per surface type
const SPEED_MULTIPLIERS: Dictionary = {
	SurfaceType.MUD_UNPAVED: 0.50,       # -50% haul velocity penalty
	SurfaceType.WILD_GRASS: 1.00,        # Baseline 1.0x
	SurfaceType.DIRT_TRAIL: 1.15,        # +15% boost
	SurfaceType.GRAVEL_ROAD: 1.25,       # +25% boost
	SurfaceType.COBBLESTONE_PAVED: 1.40, # +40% haul velocity boost
	SurfaceType.ROYAL_HIGHWAY: 1.60      # +60% boost
}

## Traversal cost multipliers per surface type (inverse of speed multiplier: Cost = 1.0 / Speed)
const COST_MULTIPLIERS: Dictionary = {
	SurfaceType.MUD_UNPAVED: 2.00,       # 1.0 / 0.50 = 2.0x cost
	SurfaceType.WILD_GRASS: 1.00,        # 1.0 / 1.00 = 1.0x cost
	SurfaceType.DIRT_TRAIL: 0.869565,    # 1.0 / 1.15 =~ 0.8696x cost
	SurfaceType.GRAVEL_ROAD: 0.80,       # 1.0 / 1.25 = 0.80x cost
	SurfaceType.COBBLESTONE_PAVED: 0.7142857, # 1.0 / 1.40 =~ 0.7143x cost
	SurfaceType.ROYAL_HIGHWAY: 0.625     # 1.0 / 1.60 = 0.625x cost
}

## Wear rates per 100 kg freight cart pass
const WEAR_RATES: Dictionary = {
	SurfaceType.MUD_UNPAVED: 0.0,
	SurfaceType.WILD_GRASS: 0.0,
	SurfaceType.DIRT_TRAIL: 0.20,
	SurfaceType.GRAVEL_ROAD: 0.08,
	SurfaceType.COBBLESTONE_PAVED: 0.01,
	SurfaceType.ROYAL_HIGHWAY: 0.0
}

const MAX_DURABILITY: float = 100.0
const BASE_CITIZEN_SPEED: float = 3.2 # meters per second

## Active road tiles grid: Vector3i -> Dictionary
## { "surface": int, "durability": float }
var road_tiles: Dictionary = {}

## Returns speed multiplier for surface type
static func get_surface_speed_multiplier(surface_type: int) -> float:
	return SPEED_MULTIPLIERS.get(surface_type, 1.0)

## Returns cost multiplier for surface type
static func get_surface_cost_multiplier(surface_type: int) -> float:
	return COST_MULTIPLIERS.get(surface_type, 1.0)

## Instance helper for speed multiplier
func get_speed_multiplier(pos_or_surface) -> float:
	if pos_or_surface is Vector3i:
		if not road_tiles.has(pos_or_surface):
			return SPEED_MULTIPLIERS[SurfaceType.WILD_GRASS]
		var surface = road_tiles[pos_or_surface]["surface"]
		return SPEED_MULTIPLIERS.get(surface, 1.0)
	elif pos_or_surface is int:
		return SPEED_MULTIPLIERS.get(pos_or_surface, 1.0)
	return 1.0

## Instance helper for cost multiplier
func get_cost_multiplier(pos_or_surface) -> float:
	if pos_or_surface is Vector3i:
		if not road_tiles.has(pos_or_surface):
			return COST_MULTIPLIERS[SurfaceType.WILD_GRASS]
		var surface = road_tiles[pos_or_surface]["surface"]
		return COST_MULTIPLIERS.get(surface, 1.0)
	elif pos_or_surface is int:
		return COST_MULTIPLIERS.get(pos_or_surface, 1.0)
	return 1.0

## Relative traversal cost ratio between two surface types
## Cobblestone vs Mud yields exactly 2.0 / (1.0 / 1.40) = 2.80x
static func get_relative_cost_ratio(surface_a: int, surface_b: int) -> float:
	var cost_a = get_surface_cost_multiplier(surface_a)
	var cost_b = get_surface_cost_multiplier(surface_b)
	if cost_b <= 0.0001:
		return 1.0
	return cost_a / cost_b

## Calculate realistic haul velocity factoring surface, freight load, and slope incline
static func calculate_haul_velocity(
	base_speed: float,
	surface: int,
	current_weight_kg: float = 0.0,
	max_capacity_kg: float = 100.0,
	incline_degrees: float = 0.0
) -> float:
	var m_surface: float = SPEED_MULTIPLIERS.get(surface, 1.0)
	var load_ratio: float = clampf(current_weight_kg / maxf(1.0, max_capacity_kg), 0.0, 1.0)
	var m_load: float = 1.0 - 0.25 * load_ratio

	# Critical heavy cart stall on mud: carts with >= 80% capacity drop to 0.20x speed
	if surface == SurfaceType.MUD_UNPAVED and load_ratio >= 0.80:
		return base_speed * 0.20

	var m_gradient: float = 1.0
	if incline_degrees > 0.0:
		# Uphill slope resistance
		m_gradient = maxf(0.20, 1.0 - 0.05 * incline_degrees)
	elif incline_degrees < 0.0:
		var abs_inc: float = absf(incline_degrees)
		if abs_inc <= 10.0:
			# Gentle downhill assistance
			m_gradient = minf(1.15, 1.0 + 0.02 * abs_inc)
		else:
			# Steep downhill braking caution
			m_gradient = maxf(0.60, 1.0 - 0.04 * (abs_inc - 10.0))

	var vel = base_speed * m_surface * m_load * m_gradient
	return maxf(0.1, vel)

## A* Pathfinding edge traversal cost between adjacent grid positions
## EdgeCost(u, v) = Distance(u, v) / V_haul(surface)
## When comparing 100m over mud (cost = 100 / (3.2 * 0.5) = 62.5s)
## vs 100m over cobblestone (cost = 100 / (3.2 * 1.4) = 22.32s), ratio is exactly 2.80x!
static func get_traversal_cost(
	from_pos: Vector3i,
	to_pos: Vector3i,
	surface_type: int,
	base_speed: float = BASE_CITIZEN_SPEED,
	current_weight_kg: float = 0.0,
	max_capacity_kg: float = 100.0
) -> float:
	var dist: float
	if from_pos == to_pos:
		dist = 1.0
	else:
		dist = Vector3(from_pos).distance_to(Vector3(to_pos))

	var vel = calculate_haul_velocity(base_speed, surface_type, current_weight_kg, max_capacity_kg, 0.0)
	return dist / vel

## Pave a new road tile at the given coordinate
func pave_tile(pos: Vector3i, surface: int = SurfaceType.DIRT_TRAIL) -> bool:
	if road_tiles.has(pos) and road_tiles[pos]["surface"] >= surface:
		return false
	road_tiles[pos] = {
		"surface": surface,
		"durability": MAX_DURABILITY
	}
	road_paved.emit(pos, surface)
	return true

## Upgrade an existing road tile with material requirements
func upgrade_tile(pos: Vector3i, target_surface: int, materials: Dictionary) -> bool:
	if not road_tiles.has(pos):
		# Auto-initialize baseline dirt if not already placed
		road_tiles[pos] = {"surface": SurfaceType.DIRT_TRAIL, "durability": MAX_DURABILITY}

	var current = road_tiles[pos]["surface"]
	if target_surface <= current:
		return false

	var required_stone: int = 0
	var required_gravel: int = 0
	match target_surface:
		SurfaceType.GRAVEL_ROAD:
			required_gravel = 2
		SurfaceType.COBBLESTONE_PAVED:
			required_stone = 2
			required_gravel = 1
		SurfaceType.ROYAL_HIGHWAY:
			required_stone = 4
			required_gravel = 2

	if materials.get("stone", 0) < required_stone or materials.get("gravel", 0) < required_gravel:
		return false

	var old = current
	road_tiles[pos]["surface"] = target_surface
	road_tiles[pos]["durability"] = MAX_DURABILITY
	road_upgraded.emit(pos, old, target_surface)
	return true

## Apply heavy traffic wear with rain multiplier; churns to mud if broken in rain
func apply_traffic_wear(pos: Vector3i, cart_weight: float, rain_intensity: float = 0.0) -> Dictionary:
	if not road_tiles.has(pos):
		return {
			"has_road": false,
			"surface": SurfaceType.WILD_GRASS,
			"durability": 0.0,
			"needs_repair": false
		}

	var data = road_tiles[pos]
	var surface = data["surface"]
	var wear_rate = WEAR_RATES.get(surface, 0.05)
	var rain_factor = 1.0 + 3.0 * clampf(rain_intensity, 0.0, 1.0)
	var wear = (cart_weight / 100.0) * wear_rate * rain_factor

	data["durability"] = maxf(0.0, data["durability"] - wear)

	# Dynamic mud degradation: If unpaved/dirt road durability breaks during rain (> 0.40),
	# the road churns into deep mud, dropping speed by 50%
	if data["durability"] <= 0.0 and rain_intensity > 0.40 and surface != SurfaceType.MUD_UNPAVED:
		data["surface"] = SurfaceType.MUD_UNPAVED
		road_churned_to_mud.emit(pos)

	if data["durability"] < 30.0:
		road_degraded.emit(pos, data["durability"])

	return {
		"has_road": true,
		"surface": data["surface"],
		"durability": data["durability"],
		"needs_repair": data["durability"] < 40.0
	}

## Repair a degraded road tile back towards maximum durability
func repair_road(pos: Vector3i, materials: Dictionary) -> bool:
	if not road_tiles.has(pos):
		return false

	var data = road_tiles[pos]
	var stone_count: int = materials.get("stone", 0)
	var gravel_count: int = materials.get("gravel", 0)
	if stone_count <= 0 and gravel_count <= 0:
		return false

	# If tile was churned into mud, restoring requires gravel/stone to rebuild surface
	if data["surface"] == SurfaceType.MUD_UNPAVED:
		if stone_count >= 1:
			data["surface"] = SurfaceType.COBBLESTONE_PAVED
		else:
			data["surface"] = SurfaceType.GRAVEL_ROAD

	var repair_boost = (stone_count * 30.0) + (gravel_count * 20.0)
	data["durability"] = minf(MAX_DURABILITY, data["durability"] + repair_boost)
	road_repaired.emit(pos)
	return true
