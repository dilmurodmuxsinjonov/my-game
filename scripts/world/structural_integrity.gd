# scripts/world/structural_integrity.gd
# Voxel Lord: Feudal Realm - Milestone 31 & Realism Architecture R1
# Realistic Structural Integrity & Load-Bearing Physics
# Simulates horizontal cantilever limits, compressive stress (sigma = sum(m) / A),
# material stress thresholds, column mass overload, and cascading cave-in/collapse BFS.

class_name StructuralIntegrityManager
extends RefCounted

signal block_collapsed(position: Vector3i, material: String)
signal collapse_wave_triggered(total_collapsed: int)

# Maximum horizontal overhang (in blocks/meters) without vertical pillar support
const CANTILEVER_LIMITS: Dictionary = {
	"bedrock": 99999,
	"stone": 6,
	"cobblestone": 5,
	"brick": 6,
	"stone_bricks": 6,
	"timber": 4,
	"wood": 4,
	"oak_planks": 4,
	"planks": 4,
	"dirt": 1,
	"sand": 0,
	"gravel": 0,
	"chiseled_stone": 8,
	"iron": 8,
	"iron_block": 8
}

const BUTTRESS_SUPPORT_BONUS: int = 3 # Additional horizontal span provided by masonry buttresses

# Compressive load bearing limits in kg per 1x1m vertical column before crushing failure
const COMPRESSIVE_LIMITS_KG: Dictionary = {
	"timber": 4500.0,
	"wood": 4500.0,
	"oak_planks": 4500.0,
	"planks": 4500.0,
	"dirt": 1500.0,
	"sand": 500.0,
	"cobblestone": 12000.0,
	"brick": 25000.0,
	"stone_bricks": 25000.0,
	"stone": 38000.0,
	"chiseled_stone": 38000.0,
	"iron": 95000.0,
	"iron_block": 95000.0,
	"bedrock": 1e12
}

# Mass per 1x1x1m voxel block in kg
const VOXEL_MASS_KG: Dictionary = {
	"air": 0.0,
	"timber": 500.0,
	"wood": 500.0,
	"oak_planks": 500.0,
	"planks": 500.0,
	"dirt": 1200.0,
	"sand": 1600.0,
	"gravel": 1600.0,
	"cobblestone": 2000.0,
	"brick": 1800.0,
	"stone_bricks": 1800.0,
	"stone": 2600.0,
	"chiseled_stone": 2600.0,
	"iron": 7800.0,
	"iron_block": 7800.0
}

## Returns the horizontal cantilever overhang limit for a material
func get_cantilever_limit(material: String, has_buttress: bool = false) -> int:
	var base_limit: int = CANTILEVER_LIMITS.get(material.to_lower(), 1)
	if has_buttress and base_limit > 0 and base_limit < 90000:
		return base_limit + BUTTRESS_SUPPORT_BONUS
	return base_limit

## Checks if a horizontal span is within the cantilever threshold
func is_block_supported(material: String, horizontal_span: int, has_buttress: bool = false) -> bool:
	var limit = get_cantilever_limit(material, has_buttress)
	return horizontal_span <= limit

## Calculates vertical compressive stress: sigma = sum(m) / A (kg/m^2)
func calculate_compressive_stress(total_mass_kg: float, area_m2: float = 1.0) -> float:
	return total_mass_kg / max(0.001, area_m2)

## Evaluates column cumulative vertical mass and overload condition
func evaluate_column_load(column_material: String, stacked_blocks: Array, area_m2: float = 1.0) -> Dictionary:
	var mat_key = column_material.to_lower()
	var total_mass: float = 0.0
	for b in stacked_blocks:
		var b_key = str(b).to_lower()
		total_mass += VOXEL_MASS_KG.get(b_key, 1000.0)
	
	var capacity: float = COMPRESSIVE_LIMITS_KG.get(mat_key, 5000.0)
	var stress: float = calculate_compressive_stress(total_mass, area_m2)
	var is_overloaded: bool = total_mass > capacity
	var stress_ratio: float = stress / max(0.01, capacity)
	
	return {
		"total_mass_kg": total_mass,
		"capacity_kg": capacity,
		"compressive_stress": stress,
		"is_overloaded": is_overloaded,
		"stress_ratio": stress_ratio
	}

## Interface contract: evaluate_block_support(world, pos: Vector3i) -> Dictionary
## Returns {"supported": bool, "stress_ratio": float, "cantilever_distance": int, "overloaded": bool}
func evaluate_block_support(world, pos: Vector3i) -> Dictionary:
	var block_mat = _resolve_material_at(world, pos)
	if block_mat == "air":
		return {
			"supported": true,
			"stress_ratio": 0.0,
			"cantilever_distance": 0,
			"overloaded": false
		}
	
	# 1. Calculate cantilever distance to the nearest grounded column
	var cant_dist = _find_cantilever_distance_to_ground(world, pos)
	var cant_limit = get_cantilever_limit(block_mat)
	var cant_ok = cant_dist <= cant_limit
	
	# 2. Calculate vertical column load resting on this block
	var column_mass: float = 0.0
	var check_y = pos.y + 1
	var max_scan_y = pos.y + 64
	while check_y <= max_scan_y:
		var above_pos = Vector3i(pos.x, check_y, pos.z)
		var above_mat = _resolve_material_at(world, above_pos)
		if above_mat == "air":
			break
		column_mass += VOXEL_MASS_KG.get(above_mat, 1000.0)
		check_y += 1
		
	var capacity: float = COMPRESSIVE_LIMITS_KG.get(block_mat, 5000.0)
	var stress: float = calculate_compressive_stress(column_mass, 1.0)
	var stress_ratio: float = stress / max(0.01, capacity)
	var overloaded: bool = column_mass > capacity
	
	var is_supported: bool = cant_ok and not overloaded
	
	return {
		"supported": is_supported,
		"stress_ratio": stress_ratio,
		"cantilever_distance": cant_dist,
		"overloaded": overloaded
	}

## Evaluate overhangs for a dictionary of blocks using BFS from anchors
func evaluate_overhang(
	blocks: Dictionary, # Vector3i -> String (material) or int (BlockType)
	anchors: Array, # Array of Vector3i representing grounded pillars/bedrock
	buttress_positions: Array = [] # Array of Vector3i with masonry buttress reinforcements
) -> Dictionary:
	var stable_blocks: Array[Vector3i] = []
	var collapsed_blocks: Array[Vector3i] = []

	var buttress_set: Dictionary = {}
	for b in buttress_positions:
		buttress_set[b] = true

	# Breadth-first search from all anchor points
	var min_distance_to_anchor: Dictionary = {}
	var queue: Array[Vector3i] = []

	for anchor in anchors:
		if blocks.has(anchor):
			min_distance_to_anchor[anchor] = 0
			queue.append(anchor)

	var directions = [
		Vector3i(1, 0, 0), Vector3i(-1, 0, 0),
		Vector3i(0, 1, 0), Vector3i(0, -1, 0),
		Vector3i(0, 0, 1), Vector3i(0, 0, -1)
	]

	while not queue.is_empty():
		var current = queue.pop_front()
		var current_dist = min_distance_to_anchor[current]

		for dir in directions:
			var neighbor = current + dir
			if blocks.has(neighbor):
				var mat = _normalize_mat_name(blocks[neighbor])
				var has_buttress = buttress_set.has(neighbor) or buttress_set.has(current)
				var limit = get_cantilever_limit(mat, has_buttress)

				# Vertical support transmits directly down/up with 0 edge cost
				var edge_cost = 0 if dir.y != 0 else 1
				var new_dist = current_dist + edge_cost

				if new_dist <= limit:
					if not min_distance_to_anchor.has(neighbor) or new_dist < min_distance_to_anchor[neighbor]:
						min_distance_to_anchor[neighbor] = new_dist
						queue.append(neighbor)

	for pos in blocks.keys():
		var mat = _normalize_mat_name(blocks[pos])
		if min_distance_to_anchor.has(pos):
			stable_blocks.append(pos)
		else:
			collapsed_blocks.append(pos)
			block_collapsed.emit(pos, mat)

	if collapsed_blocks.size() > 0:
		collapse_wave_triggered.emit(collapsed_blocks.size())

	return {
		"stable": stable_blocks,
		"collapsed": collapsed_blocks
	}

## Graph-based load bearing and localized cave-in / collapse BFS solver
## Evaluates vertical compressive stress overload and horizontal cantilever limits,
## propagating failure cascades when pillars collapse.
func simulate_structural_collapse(
	blocks: Dictionary, # Vector3i -> String/int
	anchors: Array = [], # Array[Vector3i]
	buttress_positions: Array = []
) -> Dictionary:
	# 1. Establish ground anchors if none specified (Y <= 0 or bedrock)
	var effective_anchors: Array = []
	for pos in anchors:
		effective_anchors.append(pos)
		
	if effective_anchors.is_empty():
		for pos in blocks.keys():
			var mat = _normalize_mat_name(blocks[pos])
			if pos.y <= 0 or mat == "bedrock":
				effective_anchors.append(pos)

	# 2. Run overhang evaluation
	var overhang_result = evaluate_overhang(blocks, effective_anchors, buttress_positions)
	var active_blocks: Dictionary = {}
	for pos in overhang_result["stable"]:
		active_blocks[pos] = blocks[pos]
		
	var collapsed: Array[Vector3i] = []
	for pos in overhang_result["collapsed"]:
		collapsed.append(pos)
		
	# 3. Graph-based vertical compressive load evaluation
	# Group remaining stable blocks by vertical columns (X, Z)
	var columns: Dictionary = {} # Vector2i -> Array[Vector3i] sorted descending by Y
	for pos in active_blocks.keys():
		var col_key = Vector2i(pos.x, pos.z)
		if not columns.has(col_key):
			columns[col_key] = []
		columns[col_key].append(pos)
		
	for col_key in columns.keys():
		var col_blocks: Array = columns[col_key]
		col_blocks.sort_custom(func(a, b): return a.y > b.y) # Top to bottom
		
		# Accumulate mass from top to bottom
		var accumulated_mass: float = 0.0
		for i in range(col_blocks.size()):
			var b_pos = col_blocks[i]
			var mat = _normalize_mat_name(active_blocks[b_pos])
			accumulated_mass += VOXEL_MASS_KG.get(mat, 1000.0)
			
			var capacity = COMPRESSIVE_LIMITS_KG.get(mat, 5000.0)
			if accumulated_mass > capacity:
				# Column crushing failure! Block at b_pos fails under compressive load
				active_blocks.erase(b_pos)
				collapsed.append(b_pos)
				block_collapsed.emit(b_pos, mat)

	# 4. Localized Cave-In / Collapse BFS Cascade
	# If any column crushed, re-evaluate connectivity from anchors until fixed point
	var changed: bool = true
	var iterations: int = 0
	while changed and iterations < 10:
		changed = false
		iterations += 1
		var re_eval = evaluate_overhang(active_blocks, effective_anchors, buttress_positions)
		if not re_eval["collapsed"].is_empty():
			changed = true
			for pos in re_eval["collapsed"]:
				active_blocks.erase(pos)
				collapsed.append(pos)

	var stable: Array[Vector3i] = []
	for pos in active_blocks.keys():
		stable.append(pos)

	# Calculate debris impact for collapsed blocks
	var debris_impacts: Array = []
	for pos in collapsed:
		var mat = _normalize_mat_name(blocks.get(pos, "stone"))
		var fall_height = float(max(1, pos.y))
		debris_impacts.append(calculate_debris_impact(mat, fall_height))

	if not collapsed.is_empty():
		collapse_wave_triggered.emit(collapsed.size())

	return {
		"stable": stable,
		"collapsed": collapsed,
		"debris_impacts": debris_impacts,
		"total_collapsed": collapsed.size()
	}

## Calculates kinetic energy and damage of falling debris from collapse
func calculate_debris_impact(material: String, fall_height: float) -> Dictionary:
	var density_map = {
		"stone": 2600.0,      # kg/m^3
		"cobblestone": 2400.0,
		"brick": 2200.0,
		"stone_bricks": 2200.0,
		"timber": 650.0,
		"oak_planks": 600.0,
		"wood": 650.0,
		"dirt": 1500.0,
		"sand": 1600.0,
		"iron": 7800.0,
		"iron_block": 7800.0
	}
	var mass_kg = density_map.get(material.to_lower(), 1000.0)
	var gravity = 9.81
	var impact_velocity = sqrt(2.0 * gravity * max(0.1, fall_height))
	var kinetic_energy_joules = 0.5 * mass_kg * (impact_velocity * impact_velocity)
	var structural_damage = int(round(kinetic_energy_joules / 500.0))

	return {
		"mass_kg": mass_kg,
		"impact_velocity": impact_velocity,
		"kinetic_energy_joules": kinetic_energy_joules,
		"structural_damage": structural_damage
	}

# --- Helper Methods ---

func _normalize_mat_name(raw_val) -> String:
	if raw_val is String:
		return raw_val.to_lower()
	if raw_val is int:
		match raw_val:
			0: return "air"
			1, 2: return "dirt"
			3: return "stone"
			4: return "timber"
			9: return "cobblestone"
			10: return "planks"
			16: return "brick"
			17: return "timber"
			_: return "stone"
	return "stone"

func _resolve_material_at(world, pos: Vector3i) -> String:
	if world == null:
		return "stone"
	if world is Dictionary:
		if world.has(pos):
			return _normalize_mat_name(world[pos])
		return "air"
	if world.has_method("get_block_world"):
		var b_type = world.get_block_world(pos)
		return _normalize_mat_name(b_type)
	return "stone"

func _find_cantilever_distance_to_ground(world, pos: Vector3i) -> int:
	# Direct grounded column check: is this column solid straight down to y <= 0?
	var is_direct_grounded: bool = true
	var check_y = pos.y - 1
	while check_y >= 0:
		var check_pos = Vector3i(pos.x, check_y, pos.z)
		if _resolve_material_at(world, check_pos) == "air":
			is_direct_grounded = false
			break
		check_y -= 1
		
	if is_direct_grounded:
		return 0

	# BFS search in 2D horizontal plane (radius up to 16) for nearest grounded column
	var visited: Dictionary = {pos: true}
	var queue: Array = [{"pos": pos, "dist": 0}]
	var horizontal_dirs = [
		Vector3i(1, 0, 0), Vector3i(-1, 0, 0),
		Vector3i(0, 0, 1), Vector3i(0, 0, -1)
	]
	
	while not queue.is_empty():
		var item = queue.pop_front()
		var cur_pos: Vector3i = item["pos"]
		var cur_dist: int = item["dist"]
		
		if cur_dist > 16:
			break
			
		# Check if cur_pos column is grounded
		var grounded: bool = true
		var y_down = cur_pos.y - 1
		while y_down >= 0:
			if _resolve_material_at(world, Vector3i(cur_pos.x, y_down, cur_pos.z)) == "air":
				grounded = false
				break
			y_down -= 1
			
		if grounded and cur_dist > 0:
			return cur_dist
			
		for d in horizontal_dirs:
			var n_pos = cur_pos + d
			if not visited.has(n_pos) and _resolve_material_at(world, n_pos) != "air":
				visited[n_pos] = true
				queue.append({"pos": n_pos, "dist": cur_dist + 1})
				
	return 999 # Unconnected / ungrounded
