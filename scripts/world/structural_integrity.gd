# scripts/world/structural_integrity.gd
# Voxel Lord: Feudal Realm - Milestone 31: Realistic Structural Integrity & Load-Bearing Physics
# Simulates horizontal cantilever limits, arch/buttress reinforcement, and dynamic voxel collapse.

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
	"timber": 4,
	"oak_planks": 4,
	"dirt": 1,
	"sand": 0,
	"iron_block": 8
}

const BUTTRESS_SUPPORT_BONUS: int = 3 # Additional horizontal span provided by masonry buttresses

func get_cantilever_limit(material: String, has_buttress: bool = false) -> int:
	var base_limit: int = CANTILEVER_LIMITS.get(material.to_lower(), 2)
	if has_buttress and base_limit > 0 and base_limit < 90000:
		return base_limit + BUTTRESS_SUPPORT_BONUS
	return base_limit

func is_block_supported(material: String, horizontal_span: int, has_buttress: bool = false) -> bool:
	var limit = get_cantilever_limit(material, has_buttress)
	return horizontal_span <= limit

func evaluate_overhang(
	blocks: Dictionary, # Vector3i -> String (material)
	anchors: Array, # Array of Vector3i representing grounded pillars/bedrock (Y <= 0 or grounded)
	buttress_positions: Array = [] # Array of Vector3i with masonry buttress reinforcements
) -> Dictionary:
	# Returns {"stable": Array[Vector3i], "collapsed": Array[Vector3i]}
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
				var mat = blocks[neighbor]
				var has_buttress = buttress_set.has(neighbor) or buttress_set.has(current)
				var limit = get_cantilever_limit(mat, has_buttress)

				# Vertical support transmits directly down/up with lower structural stress
				var edge_cost = 0 if dir.y != 0 else 1
				var new_dist = current_dist + edge_cost

				if new_dist <= limit:
					if not min_distance_to_anchor.has(neighbor) or new_dist < min_distance_to_anchor[neighbor]:
						min_distance_to_anchor[neighbor] = new_dist
						queue.append(neighbor)

	for pos in blocks.keys():
		var mat = blocks[pos]
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

func calculate_debris_impact(material: String, fall_height: float) -> Dictionary:
	var density_map = {
		"stone": 2600.0,      # kg/m^3
		"cobblestone": 2400.0,
		"brick": 2200.0,
		"timber": 650.0,
		"oak_planks": 600.0,
		"dirt": 1500.0,
		"sand": 1600.0
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
