# scripts/world/road_network.gd
# Voxel Lord: Feudal Realm - Milestone 29: Road Paving & Pathfinding Optimization
# Multi-tier road grid, speed multipliers, pathfinding traversal costs, and heavy cart wear.

class_name RoadNetwork
extends RefCounted

signal road_paved(pos: Vector3i, tier: int)
signal road_upgraded(pos: Vector3i, old_tier: int, new_tier: int)
signal road_degraded(pos: Vector3i, current_durability: float)
signal road_repaired(pos: Vector3i)

enum RoadTier {
	NONE = 0,
	DIRT_PATH = 1,
	GRAVEL_ROAD = 2,
	COBBLESTONE_PAVED = 3
}

const TIER_SPEED_MULTIPLIERS = {
	RoadTier.NONE: 1.0,
	RoadTier.DIRT_PATH: 1.10,
	RoadTier.GRAVEL_ROAD: 1.25,
	RoadTier.COBBLESTONE_PAVED: 1.50
}

const TIER_PATHFINDING_COSTS = {
	RoadTier.NONE: 1.0,
	RoadTier.DIRT_PATH: 0.90,
	RoadTier.GRAVEL_ROAD: 0.75,
	RoadTier.COBBLESTONE_PAVED: 0.50
}

const MAX_DURABILITY = 100.0

var road_tiles: Dictionary = {} # Vector3i -> Dictionary { "tier": int, "durability": float }

func pave_tile(pos: Vector3i, tier: int = RoadTier.DIRT_PATH) -> bool:
	if road_tiles.has(pos) and road_tiles[pos]["tier"] >= tier:
		return false
	road_tiles[pos] = {
		"tier": tier,
		"durability": MAX_DURABILITY
	}
	road_paved.emit(pos, tier)
	return true

func upgrade_tile(pos: Vector3i, target_tier: int, materials: Dictionary) -> bool:
	if not road_tiles.has(pos):
		return false
	var current = road_tiles[pos]["tier"]
	if target_tier <= current:
		return false

	var required_stone = 2 if target_tier == RoadTier.COBBLESTONE_PAVED else 1
	if materials.get("stone", 0) < required_stone:
		return false

	var old = current
	road_tiles[pos]["tier"] = target_tier
	road_tiles[pos]["durability"] = MAX_DURABILITY
	road_upgraded.emit(pos, old, target_tier)
	return true

func get_speed_multiplier(pos: Vector3i) -> float:
	if not road_tiles.has(pos):
		return 1.0
	var tier = road_tiles[pos]["tier"]
	return TIER_SPEED_MULTIPLIERS.get(tier, 1.0)

func get_pathfinding_cost(pos: Vector3i) -> float:
	if not road_tiles.has(pos):
		return 1.0
	var tier = road_tiles[pos]["tier"]
	return TIER_PATHFINDING_COSTS.get(tier, 1.0)

func apply_traffic_wear(pos: Vector3i, cart_weight: float) -> Dictionary:
	if not road_tiles.has(pos):
		return {"has_road": false, "durability": 0.0}

	var data = road_tiles[pos]
	var wear_factor = 0.5 if data["tier"] == RoadTier.COBBLESTONE_PAVED else 1.2
	var wear = cart_weight * wear_factor * 0.05
	data["durability"] = max(0.0, data["durability"] - wear)

	if data["durability"] < 30.0:
		road_degraded.emit(pos, data["durability"])

	return {
		"has_road": true,
		"tier": data["tier"],
		"durability": data["durability"],
		"needs_repair": data["durability"] < 40.0
	}

func repair_road(pos: Vector3i, stone_count: int) -> bool:
	if not road_tiles.has(pos) or stone_count <= 0:
		return false
	var data = road_tiles[pos]
	data["durability"] = min(MAX_DURABILITY, data["durability"] + stone_count * 25.0)
	road_repaired.emit(pos)
	return true
