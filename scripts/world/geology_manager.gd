class_name GeologyManager
extends RefCounted

## TerraFirmaCraft-inspired Geological Strata and Underground Structural Stability Engine.
## Governs cave-in collapse mechanics, support beam safety zones, and prospector ore prospecting.

signal cave_in_occurred(origin: Vector3i, affected_blocks: Array[Vector3i], damage: float)

const SUPPORT_BEAM_RADIUS: int = 4 # 4 blocks horizontal safety radius
const SUPPORT_BEAM_VERTICAL: int = 3 # 3 blocks vertical delta safety zone
const UNDERGROUND_THRESHOLD_Y: int = 24 # Heights <= 24 require structural mine props
const BASE_CAVE_IN_CHANCE: float = 0.35 # 35% collapse chance if unpropped
const CRUSH_DAMAGE_MIN: float = 25.0
const CRUSH_DAMAGE_MAX: float = 45.0

# Ores recognized by geological prospector scanning
const PROSPECTABLE_ORES: Array[int] = [
	VoxelChunk.BlockType.COAL_ORE,
	VoxelChunk.BlockType.COPPER_ORE,
	VoxelChunk.BlockType.IRON_ORE,
	VoxelChunk.BlockType.GOLD_ORE,
	VoxelChunk.BlockType.DEEP_GEM_ORE,
	VoxelChunk.BlockType.ROCK_SALT_ORE,
	VoxelChunk.BlockType.SILVER_ORE
]

## Check if a specific voxel position is protected by a nearby Support Beam
func is_position_supported(world, target_pos: Vector3i) -> bool:
	if target_pos.y > UNDERGROUND_THRESHOLD_Y:
		return true # Surface and shallow terrain does not require mine props
		
	# Scan bounding box [pos.x - r, pos.x + r] x [pos.y - v, pos.y + v] x [pos.z - r, pos.z + r]
	for dx in range(-SUPPORT_BEAM_RADIUS, SUPPORT_BEAM_RADIUS + 1):
		for dz in range(-SUPPORT_BEAM_RADIUS, SUPPORT_BEAM_RADIUS + 1):
			for dy in range(-SUPPORT_BEAM_VERTICAL, SUPPORT_BEAM_VERTICAL + 1):
				var check_pos = Vector3i(target_pos.x + dx, target_pos.y + dy, target_pos.z + dz)
				var block = world.get_block_world(check_pos)
				if block == VoxelChunk.BlockType.SUPPORT_BEAM:
					return true
					
	return false

## Check if mining a block causes a structural collapse (cave-in)
func check_mining_stability(world, mined_pos: Vector3i, old_type: int) -> Dictionary:
	# Only underground structural stones/ores can trigger cave-ins
	if mined_pos.y > UNDERGROUND_THRESHOLD_Y:
		return {"collapsed": false, "affected_blocks": [], "damage": 0.0, "reason": "surface"}
		
	if not _is_structural_block(old_type):
		return {"collapsed": false, "affected_blocks": [], "damage": 0.0, "reason": "non_structural"}
		
	# Check if area is protected by a support beam
	if is_position_supported(world, mined_pos):
		return {"collapsed": false, "affected_blocks": [], "damage": 0.0, "reason": "supported"}
		
	# Roll cave-in probability
	var roll = randf()
	if roll > BASE_CAVE_IN_CHANCE:
		return {"collapsed": false, "affected_blocks": [], "damage": 0.0, "reason": "stability_held"}
		
	# Trigger cave-in collapse!
	var affected_blocks: Array[Vector3i] = []
	var collapse_radius: int = randi_range(1, 2)
	
	# Identify unsupported ceiling blocks immediately above the mined spot
	for cx in range(-collapse_radius, collapse_radius + 1):
		for cz in range(-collapse_radius, collapse_radius + 1):
			for cy in range(1, 4):
				var ceiling_pos = Vector3i(mined_pos.x + cx, mined_pos.y + cy, mined_pos.z + cz)
				var ceiling_block = world.get_block_world(ceiling_pos)
				if _is_structural_block(ceiling_block):
					affected_blocks.append(ceiling_pos)
					# Convert ceiling block into fallen cobblestone / rubble at floor level
					world.set_block_world(ceiling_pos, VoxelChunk.BlockType.AIR, false)
					var floor_pos = Vector3i(ceiling_pos.x, mined_pos.y, ceiling_pos.z)
					if world.get_block_world(floor_pos) == VoxelChunk.BlockType.AIR:
						world.set_block_world(floor_pos, VoxelChunk.BlockType.COBBLESTONE, false)
						
	# Rebuild affected chunk meshes
	if not affected_blocks.is_empty():
		world.set_block_world(mined_pos, world.get_block_world(mined_pos), true)
		
	var crush_damage = randf_range(CRUSH_DAMAGE_MIN, CRUSH_DAMAGE_MAX)
	cave_in_occurred.emit(mined_pos, affected_blocks, crush_damage)
	
	return {
		"collapsed": true,
		"affected_blocks": affected_blocks,
		"damage": crush_damage,
		"message": "CAVE-IN! Structural collapse triggered! Support beams were missing!"
	}

## Prospect rock face with TerraFirmaCraft-style Prospector's Pick
func prospect_area(world, origin_pos: Vector3i, radius: int = 12) -> Dictionary:
	var ore_counts: Dictionary = {}
	var total_ores: int = 0
	
	var r_sq = radius * radius
	for dx in range(-radius, radius + 1):
		for dy in range(-radius, radius + 1):
			for dz in range(-radius, radius + 1):
				if (dx * dx + dy * dy + dz * dz) <= r_sq:
					var check_pos = Vector3i(origin_pos.x + dx, origin_pos.y + dy, origin_pos.z + dz)
					var block = world.get_block_world(check_pos)
					if block in PROSPECTABLE_ORES:
						var ore_name = _get_ore_name(block)
						ore_counts[ore_name] = ore_counts.get(ore_name, 0) + 1
						total_ores += 1
						
	if total_ores == 0:
		return {
			"status": "NONE",
			"dominant_ore": "",
			"ore_count": 0,
			"all_counts": {},
			"strata": get_strata_layer_name(origin_pos.y),
			"message": "No ores detected in this stratum."
		}
		
	# Find dominant ore
	var dominant_ore: String = ""
	var max_count: int = 0
	for ore_name in ore_counts:
		if ore_counts[ore_name] > max_count:
			max_count = ore_counts[ore_name]
			dominant_ore = ore_name
			
	var status: String = ""
	var message: String = ""
	if max_count <= 3:
		status = "TRACES"
		message = "Found traces of %s nearby." % dominant_ore.capitalize()
	elif max_count <= 8:
		status = "SAMPLE"
		message = "Found a promising sample of %s nearby." % dominant_ore.capitalize()
	elif max_count <= 15:
		status = "RICH"
		message = "Found a rich vein of %s nearby!" % dominant_ore.capitalize()
	else:
		status = "MOTHERLODE"
		message = "Found an abundant motherlode of %s!" % dominant_ore.capitalize()
		
	return {
		"status": status,
		"dominant_ore": dominant_ore,
		"ore_count": total_ores,
		"dominant_count": max_count,
		"all_counts": ore_counts,
		"strata": get_strata_layer_name(origin_pos.y),
		"message": message
	}

## Get the geological stratum layer name based on subterranean depth Y
func get_strata_layer_name(depth_y: int) -> String:
	if depth_y >= 20:
		return "Upper Sedimentary Strata (Chalk & Sandstone)"
	elif depth_y >= 10:
		return "Middle Metamorphic Strata (Slate & Marble)"
	else:
		return "Deep Igneous Strata (Basalt & Granite)"

func _is_structural_block(block_type: int) -> bool:
	return (
		block_type == VoxelChunk.BlockType.STONE or
		block_type == VoxelChunk.BlockType.COBBLESTONE or
		block_type == VoxelChunk.BlockType.STONE_BRICKS or
		block_type == VoxelChunk.BlockType.IRON_ORE or
		block_type == VoxelChunk.BlockType.COPPER_ORE or
		block_type == VoxelChunk.BlockType.GOLD_ORE or
		block_type == VoxelChunk.BlockType.COAL_ORE or
		block_type == VoxelChunk.BlockType.ROCK_SALT_ORE or
		block_type == VoxelChunk.BlockType.SILVER_ORE or
		block_type == VoxelChunk.BlockType.DEEP_GEM_ORE
	)

func _get_ore_name(block_type: int) -> String:
	match block_type:
		VoxelChunk.BlockType.COAL_ORE: return "coal"
		VoxelChunk.BlockType.COPPER_ORE: return "copper"
		VoxelChunk.BlockType.IRON_ORE: return "iron"
		VoxelChunk.BlockType.GOLD_ORE: return "gold"
		VoxelChunk.BlockType.DEEP_GEM_ORE: return "gem"
		VoxelChunk.BlockType.ROCK_SALT_ORE: return "rock_salt"
		VoxelChunk.BlockType.SILVER_ORE: return "silver"
		_: return "ore"
