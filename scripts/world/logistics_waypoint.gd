# scripts/world/logistics_waypoint.gd
# Voxel Lord: Feudal Realm - Milestone 29: Logistics Waypoints & Supply Corridor Prioritization
# Crossroad signposts that set directional route priorities, boosting hauler cart transport throughput.

class_name LogisticsWaypoint
extends RefCounted

signal priority_route_changed(waypoint_id: String, new_route: String)
signal hauler_boosted(hauler_id: String, bonus_capacity: float)
signal muster_point_set(waypoint_id: String)

var waypoint_id: String = "waypoint_crossroads_1"
var position: Vector3 = Vector3.ZERO
var destination_labels: Array[String] = ["Market Square", "Castle Keep", "Iron Mine"]
var priority_route: String = "Market Square"
var throughput_bonus: float = 0.15 # +15% carrying payload efficiency
var is_muster_point: bool = false
var total_haulers_routed: int = 0

func _init(p_id: String = "waypoint_crossroads_1", p_pos: Vector3 = Vector3.ZERO) -> void:
	waypoint_id = p_id
	position = p_pos

func set_priority_route(route_name: String) -> bool:
	if not destination_labels.has(route_name):
		return false
	priority_route = route_name
	priority_route_changed.emit(waypoint_id, route_name)
	return true

func route_hauler(hauler_id: String, base_capacity: float, target_destination: String) -> Dictionary:
	total_haulers_routed += 1
	var is_priority = (target_destination == priority_route)
	var final_capacity = base_capacity * ((1.0 + throughput_bonus) if is_priority else 1.0)

	if is_priority:
		hauler_boosted.emit(hauler_id, final_capacity - base_capacity)

	return {
		"hauler_id": hauler_id,
		"priority_boosted": is_priority,
		"assigned_capacity": final_capacity,
		"destination": target_destination
	}

func toggle_muster_point(enabled: bool) -> bool:
	is_muster_point = enabled
	if enabled:
		muster_point_set.emit(waypoint_id)
	return is_muster_point
