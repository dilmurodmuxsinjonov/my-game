# scripts/world/geology_manager.gd
# Voxel Lord: Feudal Realm - Geological Strata, Lithostatic Overburden & Subterranean Stability Engine.
# Simulates depth overburden pressure P = rho * g * |y|, rock tensile constants K_rock,
# mine ceiling stability index Sc, support beam safety radii, and cascading cave-in collapses.

class_name GeologyManager
extends RefCounted

signal cave_in_occurred(origin: Vector3i, affected_blocks: Array[Vector3i], damage: float)

const SUPPORT_BEAM_RADIUS: int = 4 # 4 blocks horizontal safety radius
const SUPPORT_BEAM_VERTICAL: int = 3 # 3 blocks vertical delta safety zone
const UNDERGROUND_THRESHOLD_Y: int = 24 # Heights <= 24 require structural mine props
const BASE_CAVE_IN_CHANCE: float = 0.35 # Fallback collapse chance if unpropped
const CRUSH_DAMAGE_MIN: float = 25.0
const CRUSH_DAMAGE_MAX: float = 45.0

# Rock tensile strength factors K_rock (GDD Section 32.2)
const ROCK_TENSILE_K: Dictionary = {
	"soil": 0.20,
	"sand": 0.20,
	"clay": 0.20,
	"sandstone": 0.55,
	"limestone": 0.55,
	"granite": 0.90,
	"stone": 0.90,
	"cobblestone": 0.65,
	"stone_bricks": 0.85,
	"monolithic_granite": 1.40,
	"basalt": 1.00,
	"bedrock": 999.0,
	"iron_ore": 0.85,
	"copper_ore": 0.70,
	"coal_ore": 0.50,
	"gold_ore": 0.60,
	"deep_gem_ore": 1.00,
	"rock_salt_ore": 0.45,
	"silver_ore": 0.75
}

# Rock density (kg/m^3) for lithostatic overburden pressure
const ROCK_DENSITY: Dictionary = {
	"soil": 1600.0,
	"sand": 1600.0,
	"sandstone": 2300.0,
	"limestone": 2300.0,
	"granite": 2600.0,
	"stone": 2600.0,
	"monolithic_granite": 2750.0,
	"basalt": 2900.0,
	"bedrock": 3000.0
}

# Mine support beam specifications
const SUPPORT_TYPES: Dictionary = {
	"softwood_timber": {"radius": 3.0, "capacity_kpa": 150.0},
	"support_beam": {"radius": 4.0, "capacity_kpa": 300.0},
	"hardwood_frame": {"radius": 5.0, "capacity_kpa": 450.0},
	"reinforced_oak": {"radius": 6.0, "capacity_kpa": 600.0},
	"stone_pillar": {"radius": 7.5, "capacity_kpa": 1200.0},
	"iron_arch": {"radius": 11.0, "capacity_kpa": 3500.0}
}

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

## Calculates lithostatic overburden pressure in kPa: P = (rho * g * |y|) / 1000.0
func calculate_overburden_pressure_kpa(rock_type: String, depth_m: float) -> float:
	var rho: float = ROCK_DENSITY.get(rock_type.to_lower(), 2600.0)
	var g: float = 9.81
	var y_abs: float = abs(depth_m)
	return (rho * g * y_abs) / 1000.0

## Mathematical mine ceiling stability index Sc formula (GDD Section 32.1):
## Sc = [K_rock * max(1.0, sum(R_sup^2 / (d^2 + 0.1)))] /
##      [1.0 + alpha_span * (L_span / 2)^2 * (1.0 + beta_depth * (|y| / 100))]
func calculate_mine_stability_index(
	rock_type: String,
	span_m: float,
	depth_m: float,
	supports: Array = []
) -> float:
	var k_rock: float = ROCK_TENSILE_K.get(rock_type.to_lower(), 0.90)
	var alpha_span: float = 0.08
	var beta_depth: float = 0.35

	var sup_factor: float = 1.0
	if not supports.is_empty():
		var support_term: float = 0.0
		for s in supports:
			var r_sup: float = 4.0
			var d: float = 1.0
			if s is Array and s.size() >= 2:
				r_sup = float(s[0])
				d = float(s[1])
			elif s is Dictionary:
				r_sup = float(s.get("radius", 4.0))
				d = float(s.get("distance", 1.0))
			support_term += (r_sup * r_sup) / (d * d + 0.1)
		sup_factor = max(1.0, support_term)

	var y_abs: float = abs(depth_m)
	var depth_factor: float = 1.0 + beta_depth * (y_abs / 100.0)
	var span_factor: float = alpha_span * pow(span_m / 2.0, 2) * depth_factor
	var denominator: float = 1.0 + span_factor

	return (k_rock * sup_factor) / max(0.01, denominator)

## Interface Contract: GeologyManager.calculate_stability_index(world: VoxelWorld, pos: Vector3i) -> float
## Evaluates subterranean stability index Sc for a specific voxel position in the world
func calculate_stability_index(world, pos: Vector3i) -> float:
	if world == null:
		return calculate_mine_stability_index("granite", 4.0, float(pos.y))

	var rock_name = _get_rock_name_for_pos(world, pos)
	
	# Determine subterranean depth
	var depth_m: float = 0.0
	if pos.y <= 0:
		depth_m = float(abs(pos.y))
	elif pos.y <= UNDERGROUND_THRESHOLD_Y:
		depth_m = float(UNDERGROUND_THRESHOLD_Y - pos.y) * 4.0 # Scale to meters
	else:
		return 1.5 # Surface is inherently stable

	# Measure unsupported horizontal span (distance between solid structural walls along X/Z)
	var span_x = _measure_span_axis(world, pos, Vector3i(1, 0, 0))
	var span_z = _measure_span_axis(world, pos, Vector3i(0, 0, 1))
	var span_m = float(max(2.0, max(span_x, span_z)))

	# Scan for active mine props (SUPPORT_BEAM) within radius 12m
	var supports: Array = []
	var scan_r: int = 12
	var min_x = pos.x - scan_r
	var max_x = pos.x + scan_r
	var min_z = pos.z - scan_r
	var max_z = pos.z + scan_r
	var min_y = max(0, pos.y - 4)
	var max_y = min(VoxelChunk.CHUNK_SIZE_Y - 1, pos.y + 4)

	for sx in range(min_x, max_x + 1):
		for sz in range(min_z, max_z + 1):
			for sy in range(min_y, max_y + 1):
				var check_pos = Vector3i(sx, sy, sz)
				var b = world.get_block_world(check_pos)
				if b == VoxelChunk.BlockType.SUPPORT_BEAM:
					var dist = Vector3(pos.x - sx, pos.y - sy, pos.z - sz).length()
					supports.append([SUPPORT_BEAM_RADIUS, max(0.5, dist)])

	return calculate_mine_stability_index(rock_name, span_m, depth_m, supports)

## Check if a specific voxel position is protected by a nearby Support Beam
func is_position_supported(world, target_pos: Vector3i) -> bool:
	if target_pos.y > UNDERGROUND_THRESHOLD_Y:
		return true # Surface does not require mine props
		
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
## Evaluates lithostatic stability Sc and propagates localized collapse
func check_mining_stability(world, mined_pos: Vector3i, old_type: int) -> Dictionary:
	# Only underground structural stones/ores can trigger cave-ins
	if mined_pos.y > UNDERGROUND_THRESHOLD_Y:
		return {"collapsed": false, "affected_blocks": [], "damage": 0.0, "reason": "surface", "sc": 1.5}
		
	if not _is_structural_block(old_type):
		return {"collapsed": false, "affected_blocks": [], "damage": 0.0, "reason": "non_structural", "sc": 1.0}
		
	# Calculate subterranean stability index Sc
	var sc: float = calculate_stability_index(world, mined_pos)
	
	# If fully stable (Sc >= 1.0)
	if sc >= 1.0:
		return {
			"collapsed": false,
			"affected_blocks": [],
			"damage": 0.0,
			"reason": "supported",
			"sc": sc
		}
		
	# If experiencing structural strain (0.75 <= Sc < 1.0)
	if sc >= 0.75:
		return {
			"collapsed": false,
			"affected_blocks": [],
			"damage": 0.0,
			"reason": "structural_strain",
			"sc": sc,
			"message": "Timber creaks under overburden pressure. Ceiling remains intact."
		}

	# Critical failure (Sc < 0.75): Cave-in collapse!
	var collapse_prob: float = clampf(1.0 - sc, 0.25, 0.95)
	if randf() > collapse_prob:
		return {
			"collapsed": false,
			"affected_blocks": [],
			"damage": 0.0,
			"reason": "stability_held",
			"sc": sc
		}
		
	# Execute localized cave-in cascade!
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
		
	var depth_factor: float = 1.0 + (float(UNDERGROUND_THRESHOLD_Y - mined_pos.y) / 20.0)
	var crush_damage: float = randf_range(CRUSH_DAMAGE_MIN, CRUSH_DAMAGE_MAX) * depth_factor
	cave_in_occurred.emit(mined_pos, affected_blocks, crush_damage)
	
	return {
		"collapsed": true,
		"affected_blocks": affected_blocks,
		"damage": crush_damage,
		"sc": sc,
		"message": "CAVE-IN! Lithostatic pressure triggered collapse! Sc = %.2f < 0.75!" % sc
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

func _get_rock_name_for_pos(world, pos: Vector3i) -> String:
	var b = world.get_block_world(pos)
	match b:
		VoxelChunk.BlockType.COAL_ORE: return "coal_ore"
		VoxelChunk.BlockType.COPPER_ORE: return "copper_ore"
		VoxelChunk.BlockType.IRON_ORE: return "iron_ore"
		VoxelChunk.BlockType.GOLD_ORE: return "gold_ore"
		VoxelChunk.BlockType.DEEP_GEM_ORE: return "deep_gem_ore"
		VoxelChunk.BlockType.ROCK_SALT_ORE: return "rock_salt_ore"
		VoxelChunk.BlockType.SILVER_ORE: return "silver_ore"
		VoxelChunk.BlockType.COBBLESTONE: return "cobblestone"
		VoxelChunk.BlockType.STONE_BRICKS: return "stone_bricks"
		_:
			if pos.y >= 20:
				return "sandstone"
			elif pos.y >= 10:
				return "granite"
			else:
				return "basalt"

func _measure_span_axis(world, origin: Vector3i, step_dir: Vector3i) -> float:
	var count = 0
	# Positive direction
	for i in range(1, 16):
		var p = origin + step_dir * i
		if _is_structural_block(world.get_block_world(p)):
			break
		count += 1
	# Negative direction
	for i in range(1, 16):
		var p = origin - step_dir * i
		if _is_structural_block(world.get_block_world(p)):
			break
		count += 1
	return float(count)
