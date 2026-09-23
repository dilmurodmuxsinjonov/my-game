class_name GridPathfinder3D
extends RefCounted

## 3D Voxel Grid A* Pathfinder for autonomous citizens and NPCs.
## Navigates across irregular 3D voxel terrain, supports 1-meter step-ups and safe 2-meter drops.

var voxel_world: VoxelWorld

func _init(p_world: VoxelWorld = null) -> void:
	voxel_world = p_world

func is_standable(pos: Vector3i) -> bool:
	if not voxel_world:
		return false
	var block_floor = voxel_world.get_block_world(pos + Vector3i.DOWN)
	var block_feet = voxel_world.get_block_world(pos)
	var block_head = voxel_world.get_block_world(pos + Vector3i.UP)
	
	# Floor must be solid; feet and head must be air or passable
	var has_solid_floor = block_floor != VoxelChunk.BlockType.AIR and block_floor != VoxelChunk.BlockType.WATER
	var feet_clear = block_feet == VoxelChunk.BlockType.AIR or block_feet == VoxelChunk.BlockType.WHEAT_CROP
	var head_clear = block_head == VoxelChunk.BlockType.AIR
	
	return has_solid_floor and feet_clear and head_clear

func find_path(start_world: Vector3, target_world: Vector3, max_iterations: int = 500) -> Array[Vector3]:
	var start_grid = Vector3i(int(floor(start_world.x)), int(floor(start_world.y)), int(floor(start_world.z)))
	var target_grid = Vector3i(int(floor(target_world.x)), int(floor(target_world.y)), int(floor(target_world.z)))
	
	# Adjust start and target to closest standable ground
	start_grid = _find_closest_standable(start_grid)
	target_grid = _find_closest_standable(target_grid)
	
	if start_grid == target_grid:
		return [target_world]
		
	# Priority queue simulation: sorted array of dictionaries
	# [{pos: Vector3i, g: float, f: float, parent: Vector3i}]
	var open_set: Array = []
	var open_lookup: Dictionary = {}
	var closed_set: Dictionary = {}
	var came_from: Dictionary = {}
	var g_score: Dictionary = {}
	
	g_score[start_grid] = 0.0
	var initial_f = _heuristic(start_grid, target_grid)
	open_set.append({"pos": start_grid, "f": initial_f})
	open_lookup[start_grid] = true
	
	var iterations: int = 0
	var best_node: Vector3i = start_grid
	var best_dist: float = initial_f
	
	while open_set.size() > 0 and iterations < max_iterations:
		iterations += 1
		
		# Find node with lowest f
		var lowest_idx = 0
		var lowest_f = open_set[0]["f"]
		for i in range(1, open_set.size()):
			if open_set[i]["f"] < lowest_f:
				lowest_f = open_set[i]["f"]
				lowest_idx = i
				
		var current: Vector3i = open_set[lowest_idx]["pos"]
		open_set.remove_at(lowest_idx)
		open_lookup.erase(current)
		closed_set[current] = true
		
		# Track closest approached node for fallback
		var dist_to_target = _heuristic(current, target_grid)
		if dist_to_target < best_dist:
			best_dist = dist_to_target
			best_node = current
			
		# Check destination reached
		if current == target_grid or dist_to_target <= 1.0:
			return _reconstruct_path(came_from, current)
			
		# Explore 4 cardinal neighbors
		var neighbors = _get_valid_neighbors(current)
		for next_pos in neighbors:
			if closed_set.has(next_pos):
				continue
				
			var tentative_g = g_score[current] + 1.0 + (abs(next_pos.y - current.y) * 0.5)
			
			if not g_score.has(next_pos) or tentative_g < g_score[next_pos]:
				came_from[next_pos] = current
				g_score[next_pos] = tentative_g
				var f = tentative_g + _heuristic(next_pos, target_grid)
				
				if not open_lookup.has(next_pos):
					open_set.append({"pos": next_pos, "f": f})
					open_lookup[next_pos] = true

	# Fallback: return path to closest explored node
	return _reconstruct_path(came_from, best_node)

func _get_valid_neighbors(current: Vector3i) -> Array[Vector3i]:
	var result: Array[Vector3i] = []
	var offsets = [
		Vector3i(1, 0, 0),
		Vector3i(-1, 0, 0),
		Vector3i(0, 0, 1),
		Vector3i(0, 0, -1)
	]
	
	for off in offsets:
		var flat = current + off
		# 1. Flat move
		if is_standable(flat):
			result.append(flat)
			continue
			
		# 2. Step up 1 block
		var step_up = flat + Vector3i.UP
		if is_standable(step_up):
			# Head clearance above current position before stepping up
			if voxel_world.get_block_world(current + Vector3i(0, 2, 0)) == VoxelChunk.BlockType.AIR:
				result.append(step_up)
				continue
				
		# 3. Drop down 1 block
		var step_down_1 = flat + Vector3i.DOWN
		if is_standable(step_down_1):
			result.append(step_down_1)
			continue
			
		# 4. Safe drop down 2 blocks
		var step_down_2 = flat + Vector3i(0, -2, 0)
		if is_standable(step_down_2):
			result.append(step_down_2)
			continue
			
	return result

func _find_closest_standable(pos: Vector3i) -> Vector3i:
	if is_standable(pos):
		return pos
	for dy in range(-3, 4):
		var check = pos + Vector3i(0, dy, 0)
		if is_standable(check):
			return check
	return pos

func _heuristic(a: Vector3i, b: Vector3i) -> float:
	return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)

func _reconstruct_path(came_from: Dictionary, current: Vector3i) -> Array[Vector3]:
	var path: Array[Vector3] = []
	var cur = current
	while came_from.has(cur):
		# Centered on top of block floor
		path.append(Vector3(cur.x + 0.5, cur.y, cur.z + 0.5))
		cur = came_from[cur]
	path.append(Vector3(cur.x + 0.5, cur.y, cur.z + 0.5))
	path.reverse()
	return path
