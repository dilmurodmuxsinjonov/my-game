# scripts/combat/projectile.gd
# Voxel Lord: Feudal Realm - Milestone 31 & Realism Architecture R1
# High-Fidelity Ballistic Projectile Engine (Arrow / Bolt / Siege Boulder)
# Simulates aerodynamic drag, altitude air density decay rho(y), crosswind drift,
# and kinetic impact voxel blast fracturing: Damage_voxel(X) = [ImpactDamage / (1.0 + |X - P_impact|^2)] * (1.0 - Hardness/10.0).

class_name Projectile
extends Node3D

signal impacted(hit_target: Node, hit_point: Vector3)
signal voxel_blast_triggered(impact_point: Vector3, destroyed_count: int)

var velocity: Vector3 = Vector3.ZERO
var gravity: float = 9.80665
var damage: float = 35.0
var shooter: Node = null
var lifetime: float = 6.0
var age: float = 0.0
var is_stuck: bool = false

var projectile_type: String = "bodkin_arrow"
var wind_velocity: Vector3 = Vector3.ZERO
var blast_radius: float = 0.0 # Heavy projectiles (boulders) have non-zero blast radius

var model_instance: Node3D

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
	"iron": 3500.0,
	"iron_block": 3500.0
}

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
	"iron": 9.0,
	"iron_block": 9.0
}

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	var glb_path = "res://assets/models/arrow.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_instance = scene_res.instantiate()
			add_child(model_instance)

func launch(
	start_pos: Vector3,
	direction: Vector3,
	speed: float,
	dmg: float,
	p_shooter: Node = null,
	p_type: String = "bodkin_arrow",
	p_wind: Vector3 = Vector3.ZERO,
	p_blast_radius: float = 0.0
) -> void:
	global_position = start_pos
	velocity = direction.normalized() * speed
	damage = dmg
	shooter = p_shooter
	projectile_type = p_type
	wind_velocity = p_wind
	blast_radius = p_blast_radius
	
	if velocity.length_squared() > 0.01:
		look_at(global_position + velocity, Vector3.UP)

func _process(delta: float) -> void:
	if is_stuck:
		return
		
	age += delta
	if age >= lifetime:
		queue_free()
		return
		
	# Aerodynamic drag and altitude barometric air density integration
	var drag_acc = BallisticRealism.compute_aerodynamic_acceleration(
		velocity,
		wind_velocity,
		global_position.y,
		projectile_type
	)
	var total_acc = Vector3(0.0, -gravity, 0.0) + drag_acc
	velocity += total_acc * delta
	var step = velocity * delta
	var next_pos = global_position + step
	
	# Rotate towards flight vector
	if velocity.length_squared() > 0.1:
		var target_look = global_position + velocity
		if abs(velocity.normalized().dot(Vector3.UP)) < 0.99:
			look_at(target_look, Vector3.UP)
			
	# Raycast collision check along trajectory step
	var space_state = get_world_3d().direct_space_state
	var query = PhysicsRayQueryParameters3D.create(global_position, next_pos)
	if shooter is CollisionObject3D:
		query.exclude = [shooter.get_rid()]
		
	var result = space_state.intersect_ray(query)
	if result:
		_handle_impact(result)
	else:
		global_position = next_pos

## Calculates voxel damage with inverse-square distance falloff and material hardness absorption:
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

## Applies kinetic impact voxel blast fracturing to terrain
func apply_voxel_blast(world, impact_pos: Vector3, impact_dmg: float, radius: float = 3.0) -> int:
	if world == null or not world.has_method("get_block_world"):
		return 0
		
	var destroyed_count: int = 0
	var r_ceil = int(ceil(radius))
	var center_i = Vector3i(int(floor(impact_pos.x)), int(floor(impact_pos.y)), int(floor(impact_pos.z)))
	
	for dx in range(-r_ceil, r_ceil + 1):
		for dy in range(-r_ceil, r_ceil + 1):
			for dz in range(-r_ceil, r_ceil + 1):
				var check_pos = center_i + Vector3i(dx, dy, dz)
				var v_center = Vector3(check_pos.x + 0.5, check_pos.y + 0.5, check_pos.z + 0.5)
				if impact_pos.distance_to(v_center) <= radius:
					var b_type = world.get_block_world(check_pos)
					if b_type != VoxelChunk.BlockType.AIR:
						var mat_name = _get_mat_name(b_type)
						var hardness = VOXEL_HARDNESS_TIER.get(mat_name, 4.0)
						var hp = VOXEL_HP.get(mat_name, 600.0)
						var vox_dmg = calculate_blast_damage(impact_dmg, impact_pos, v_center, hardness)
						if vox_dmg >= hp:
							world.set_block_world(check_pos, VoxelChunk.BlockType.AIR, false)
							destroyed_count += 1
							
	if destroyed_count > 0 and world.has_method("set_block_world"):
		# Trigger mesh rebuild
		world.set_block_world(center_i, world.get_block_world(center_i), true)
		voxel_blast_triggered.emit(impact_pos, destroyed_count)
		
	return destroyed_count

func _handle_impact(result: Dictionary) -> void:
	var hit_collider = result.get("collider")
	var hit_pos = result.get("position", global_position)
	
	emit_signal("impacted", hit_collider, hit_pos)
	
	# Check if hit Bandit enemy
	if hit_collider and hit_collider.has_method("take_damage"):
		var knockback = velocity.normalized() * 3.5
		hit_collider.take_damage(damage, knockback)
		queue_free()
		return
		
	# Check if hit Player (if shot by bandit)
	if hit_collider is Player:
		hit_collider.take_damage(damage)
		queue_free()
		return
		
	# Hit terrain or static geometry
	global_position = hit_pos
	
	# If projectile has explosive or kinetic blast capability (e.g. siege boulder)
	var profile = BallisticRealism.PROJECTILE_PROFILES.get(projectile_type, {})
	var mass: float = profile.get("mass", 0.050)
	var ke: float = 0.5 * mass * velocity.length_squared()
	var impact_dmg: float = BallisticRealism.calculate_impact_damage(ke)
	
	# If heavy projectile with kinetic impact or blast radius
	if blast_radius > 0.0 or mass >= 1.0 or impact_dmg >= 200.0:
		var blast_r = blast_radius if blast_radius > 0.0 else 3.0
		var world = _find_voxel_world()
		if world:
			apply_voxel_blast(world, hit_pos, impact_dmg, blast_r)
		queue_free()
		return

	# Light projectile (arrow): stick into surface and fade out
	is_stuck = true
	var tween = create_tween()
	tween.tween_interval(2.5)
	tween.tween_callback(queue_free)

func _find_voxel_world() -> Node:
	var root = get_tree().root if is_inside_tree() else null
	if root:
		return root.find_child("VoxelWorld", true, false)
	return null

func _get_mat_name(block_type: int) -> String:
	match block_type:
		VoxelChunk.BlockType.DIRT, VoxelChunk.BlockType.GRASS: return "dirt"
		VoxelChunk.BlockType.WOOD, VoxelChunk.BlockType.PLANKS, VoxelChunk.BlockType.SUPPORT_BEAM: return "timber"
		VoxelChunk.BlockType.COBBLESTONE: return "cobblestone"
		VoxelChunk.BlockType.STONE_BRICKS: return "brick"
		VoxelChunk.BlockType.STONE: return "stone"
		VoxelChunk.BlockType.STONE_BATTLEMENT: return "reinforced_stone"
		_: return "stone"
