# scripts/combat/siege_engine.gd
# Voxel Lord: Feudal Realm - Milestone 23 & Realism Architecture R1
# Castle Siege Artillery (Mangonel Catapult & Heavy Trebuchet)
# Simulates long-range artillery ballistics, incendiary shockwaves,
# and kinetic impact voxel blast fracturing into destructible terrain.

class_name SiegeEngine
extends Node3D

signal catapult_fired(target_pos: Vector3, damage: float, aoe_radius: float, is_incendiary: bool)
signal catapult_reloaded(ammo_type: String)
signal voxel_blast_applied(impact_point: Vector3, blocks_destroyed: int)

var supply_chain: Node = null

const MIN_RANGE: float = 15.0
const MAX_RANGE: float = 65.0
const RELOAD_TIME_SECONDS: float = 8.0
const SIEGE_DAMAGE_BASE: float = 120.0
const AOE_RADIUS_METERS: float = 12.0
const INCENDIARY_BONUS_DAMAGE: float = 50.0

var current_reload_timer: float = 0.0
var is_loaded: bool = true
var loaded_ammo_type: String = "fire_boulder"
var boulders_stock: int = 12

# Voxel health thresholds for structural fracture (GDD Section 61.3)
const VOXEL_HP: Dictionary = {
	"dirt": 80.0,
	"timber": 200.0,
	"planks": 200.0,
	"wood": 200.0,
	"cobblestone": 600.0,
	"brick": 1000.0,
	"stone_bricks": 1000.0,
	"stone": 1200.0,
	"chiseled_stone": 1200.0,
	"reinforced_stone": 2500.0,
	"stone_battlement": 2500.0,
	"iron": 3500.0,
	"iron_block": 3500.0
}

# Material hardness tiers (0.0 to 10.0 scale)
const VOXEL_HARDNESS_TIER: Dictionary = {
	"dirt": 1.0,
	"timber": 2.0,
	"planks": 2.0,
	"wood": 2.0,
	"cobblestone": 4.0,
	"brick": 5.0,
	"stone_bricks": 5.0,
	"stone": 6.0,
	"chiseled_stone": 6.0,
	"reinforced_stone": 8.0,
	"stone_battlement": 8.0,
	"iron": 9.0,
	"iron_block": 9.0
}

func _init() -> void:
	pass

## Calculates voxel damage from blast impact with inverse-square distance falloff:
## Damage_voxel(X) = [ImpactDamage / (1.0 + |X - P_impact|^2)] * (1.0 - HardnessTier / 10.0)
static func calculate_blast_damage(
	impact_damage: float,
	impact_pos: Vector3,
	voxel_pos: Vector3,
	hardness_tier: float
) -> float:
	var dist_sq = impact_pos.distance_squared_to(voxel_pos)
	var falloff = 1.0 / (1.0 + dist_sq)
	var hardness_factor = max(0.0, 1.0 - (hardness_tier / 10.0))
	return impact_damage * falloff * hardness_factor

## Interface Contract: SiegeEngine.apply_voxel_blast(world: VoxelWorld, impact_point: Vector3, kinetic_energy: float, blast_radius: float) -> int
## Applies kinetic energy blast cratering to voxels, converting fractured voxels into AIR
func apply_voxel_blast(
	world,
	impact_point: Vector3,
	kinetic_energy: float,
	blast_radius: float = 6.0
) -> int:
	if world == null or not world.has_method("get_block_world"):
		return 0
		
	# Convert raw kinetic energy (Joules) to impact damage (Damage = Ek * 0.05), or direct damage if <= 5000
	var impact_damage: float = (kinetic_energy * 0.05) if kinetic_energy >= 15000.0 else kinetic_energy
	var destroyed_count: int = 0
	var r_ceil = int(ceil(blast_radius))
	var center_i = Vector3i(int(floor(impact_point.x)), int(floor(impact_point.y)), int(floor(impact_point.z)))

	for dx in range(-r_ceil, r_ceil + 1):
		for dy in range(-r_ceil, r_ceil + 1):
			for dz in range(-r_ceil, r_ceil + 1):
				var check_pos = center_i + Vector3i(dx, dy, dz)
				var v_center = Vector3(check_pos.x + 0.5, check_pos.y + 0.5, check_pos.z + 0.5)
				var dist = impact_point.distance_to(v_center)
				if dist <= blast_radius:
					var b_type = world.get_block_world(check_pos)
					if b_type != VoxelChunk.BlockType.AIR:
						var mat_name = _get_mat_name(b_type)
						var hardness = VOXEL_HARDNESS_TIER.get(mat_name, 4.0)
						var hp = VOXEL_HP.get(mat_name, 600.0)
						var dmg = calculate_blast_damage(impact_damage, impact_point, v_center, hardness)
						if dmg >= hp:
							world.set_block_world(check_pos, VoxelChunk.BlockType.AIR, false)
							destroyed_count += 1

	if destroyed_count > 0:
		# Trigger mesh rebuild for affected chunk
		world.set_block_world(center_i, world.get_block_world(center_i), true)
		voxel_blast_applied.emit(impact_point, destroyed_count)

	return destroyed_count

func fire_at_target(target_pos: Vector3, world = null) -> Dictionary:
	if not is_loaded:
		return {"success": false, "reason": "NOT_LOADED", "damage": 0.0}
	
	var dist: float = global_position.distance_to(target_pos)
	if dist < MIN_RANGE or dist > MAX_RANGE:
		return {"success": false, "reason": "OUT_OF_RANGE", "distance": dist}
	
	is_loaded = false
	current_reload_timer = RELOAD_TIME_SECONDS
	
	var is_incendiary: bool = (loaded_ammo_type == "fire_boulder")
	var total_damage: float = SIEGE_DAMAGE_BASE
	if is_incendiary:
		total_damage += INCENDIARY_BONUS_DAMAGE
	
	catapult_fired.emit(target_pos, total_damage, AOE_RADIUS_METERS, is_incendiary)
	
	var destroyed_blocks: int = 0
	if world:
		# Mangonel boulder: 40 kg at 35 m/s -> Ek = 24,500 J -> 1,225 impact damage
		var boulder_ke = 24500.0
		destroyed_blocks = apply_voxel_blast(world, target_pos, boulder_ke, AOE_RADIUS_METERS * 0.5)
	
	return {
		"success": true,
		"damage": total_damage,
		"aoe_radius": AOE_RADIUS_METERS,
		"is_incendiary": is_incendiary,
		"target_distance": dist,
		"destroyed_blocks": destroyed_blocks
	}

func reload(ammo_type: String = "fire_boulder") -> bool:
	if is_loaded:
		return false
	if boulders_stock <= 0:
		return false
	
	boulders_stock -= 1
	loaded_ammo_type = ammo_type
	is_loaded = true
	current_reload_timer = 0.0
	catapult_reloaded.emit(ammo_type)
	return true

func process_reload(delta: float) -> bool:
	if is_loaded:
		return true
	
	current_reload_timer -= delta
	if current_reload_timer <= 0.0:
		return reload(loaded_ammo_type)
	return false

func _get_mat_name(block_type: int) -> String:
	match block_type:
		VoxelChunk.BlockType.DIRT, VoxelChunk.BlockType.GRASS: return "dirt"
		VoxelChunk.BlockType.WOOD, VoxelChunk.BlockType.PLANKS, VoxelChunk.BlockType.SUPPORT_BEAM: return "timber"
		VoxelChunk.BlockType.COBBLESTONE: return "cobblestone"
		VoxelChunk.BlockType.STONE_BRICKS: return "brick"
		VoxelChunk.BlockType.STONE: return "stone"
		VoxelChunk.BlockType.STONE_BATTLEMENT: return "reinforced_stone"
		_: return "stone"
