# scripts/mechanisms/kinetic_network_manager.gd
# Voxel Lord: Feudal Realm - Milestone 32: Interconnected Kinetic Transmission Grid
# Graph-based BFS kinetic torque & RPM solver inspired by Create Mod & Vintage Story.

class_name KineticNetworkManager
extends RefCounted

signal network_overloaded(network_id: String, total_load: float, total_capacity: float)
signal network_stabilized(network_id: String, total_rpm: float, total_capacity: float)
signal machine_stall_state_changed(pos: Vector3i, is_stalled: bool)

enum NodeType { SOURCE, TRANSMISSION, CONSUMER }
enum NetworkState { ACTIVE, OVERLOADED, IDLE }

# Node descriptor:
# {
#   "type": NodeType,
#   "base_rpm": float,
#   "capacity_su": float,
#   "load_su": float,
#   "axis": Vector3i, # Primary axis of rotation, e.g. (1, 0, 0)
#   "is_clutch": bool,
#   "is_engaged": bool,
#   "is_gearbox": bool,
#   "gear_ratio": float,
#   "inverted": bool
# }

var nodes: Dictionary = {} # Vector3i -> Dictionary
var networks: Dictionary = {} # network_id -> Dictionary of network stats

func register_node(pos: Vector3i, node_data: Dictionary) -> void:
	nodes[pos] = node_data
	recalculate_networks()

func unregister_node(pos: Vector3i) -> void:
	if nodes.has(pos):
		nodes.erase(pos)
		recalculate_networks()

func set_clutch_engaged(pos: Vector3i, engaged: bool) -> void:
	if nodes.has(pos) and nodes[pos].get("is_clutch", false):
		nodes[pos]["is_engaged"] = engaged
		recalculate_networks()

func get_connected_neighbors(pos: Vector3i) -> Array[Vector3i]:
	var neighbors: Array[Vector3i] = []
	if not nodes.has(pos):
		return neighbors

	var current = nodes[pos]
	var current_axis = current.get("axis", Vector3i(1, 0, 0))
	var is_gearbox = current.get("is_gearbox", false)

	var directions = [
		Vector3i(1, 0, 0), Vector3i(-1, 0, 0),
		Vector3i(0, 1, 0), Vector3i(0, -1, 0),
		Vector3i(0, 0, 1), Vector3i(0, 0, -1)
	]

	for dir in directions:
		var n_pos = pos + dir
		if not nodes.has(n_pos):
			continue

		var neighbor = nodes[n_pos]
		var neighbor_axis = neighbor.get("axis", Vector3i(1, 0, 0))

		# Gearboxes can connect in 90-degree orthogonal directions
		if is_gearbox or neighbor.get("is_gearbox", false):
			neighbors.append(n_pos)
		# Linear transmission: must align along the shared connection axis
		elif dir.abs() == current_axis and current_axis == neighbor_axis:
			neighbors.append(n_pos)

	return neighbors

func recalculate_networks() -> void:
	networks.clear()
	var visited: Dictionary = {}
	var network_idx: int = 0

	# Find all SOURCE nodes (Water wheels, windmills) and flood-fill their component
	for pos in nodes.keys():
		if visited.has(pos):
			continue

		var node = nodes[pos]
		if node.get("type") != NodeType.SOURCE:
			continue

		network_idx += 1
		var net_id = "kinetic_net_%d" % network_idx

		var queue: Array[Vector3i] = [pos]
		visited[pos] = true

		var total_capacity: float = 0.0
		var total_load: float = 0.0
		var primary_rpm: float = node.get("base_rpm", 24.0)
		var net_nodes: Array[Vector3i] = []

		while not queue.is_empty():
			var curr_pos = queue.pop_front()
			net_nodes.append(curr_pos)
			var curr_node = nodes[curr_pos]

			var n_type = curr_node.get("type", NodeType.TRANSMISSION)
			if n_type == NodeType.SOURCE:
				total_capacity += curr_node.get("capacity_su", 0.0)
			elif n_type == NodeType.CONSUMER:
				total_load += curr_node.get("load_su", 0.0)
			elif n_type == NodeType.TRANSMISSION:
				# Idle friction / gearbox loss
				total_load += curr_node.get("idle_load_su", 0.0)

			# If this is a disengaged clutch, do not propagate downstream!
			if curr_node.get("is_clutch", false) and not curr_node.get("is_engaged", true):
				continue

			for n_pos in get_connected_neighbors(curr_pos):
				if not visited.has(n_pos):
					visited[n_pos] = true
					queue.append(n_pos)

		var is_overloaded = total_load > total_capacity
		var net_state = NetworkState.OVERLOADED if is_overloaded else NetworkState.ACTIVE
		var effective_rpm = 0.0 if is_overloaded else primary_rpm

		networks[net_id] = {
			"state": net_state,
			"rpm": effective_rpm,
			"capacity_su": total_capacity,
			"load_su": total_load,
			"nodes_count": net_nodes.size(),
			"nodes": net_nodes
		}

		if is_overloaded:
			network_overloaded.emit(net_id, total_load, total_capacity)
		else:
			network_stabilized.emit(net_id, effective_rpm, total_capacity)

		for p in net_nodes:
			machine_stall_state_changed.emit(p, is_overloaded)

func get_network_at(pos: Vector3i) -> Dictionary:
	for net_id in networks.keys():
		var net = networks[net_id]
		if pos in net.get("nodes", []):
			return net
	return {}
