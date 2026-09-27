# scripts/mechanisms/fluyt_cargo_ship.gd
class_name FluytCargoShip
extends Node3D

# Ocean-Going Fluyt Merchant Cargo Vessel
# Inspired by Anno 1404, Port Royale, and Vintage Story
# High-capacity trading vessel navigating coastal and overseas merchant routes.

signal cargo_loaded(item_type: String, count: int)
signal cargo_unloaded(item_type: String, count: int)
signal port_arrived(port_name: String)
signal voyage_completed(trade_profit_gold: int)

@export var vessel_id: String = "fluyt_01"
@export var vessel_name: String = "The Sea Sovereign"
@export var max_cargo_slots: int = 80
@export var max_speed_knots: float = 6.5 # ~3.34 m/s
@export var crew_capacity: int = 8
@export var min_crew_required: int = 4

var cargo_hold: Dictionary = {} # item_type -> count
var crew_count: int = 6
var hull_integrity_pct: float = 100.0

var heading_degrees: float = 90.0 # Eastbound
var wind_direction_degrees: float = 45.0 # Northeast
var wind_speed_knots: float = 14.0
var current_speed_knots: float = 0.0

var active_route_name: String = ""
var home_port: String = "Royal Citadel Harbor"
var target_port: String = "Hanseatic Merchant Post"
var voyage_total_distance_nm: float = 50.0 # Nautical miles
var voyage_distance_covered_nm: float = 0.0
var is_docked: bool = true

func _init(id: String = "fluyt_01", name: String = "The Sea Sovereign"):
	vessel_id = id
	vessel_name = name
	cargo_hold = {}

func get_total_cargo_count() -> int:
	var total: int = 0
	for count in cargo_hold.values():
		total += count
	return total

func get_free_cargo_capacity() -> int:
	return max_cargo_slots - get_total_cargo_count()

func load_cargo(item_type: String, count: int) -> int:
	if count <= 0:
		return 0
	var space = get_free_cargo_capacity()
	var to_load = min(count, space)
	if to_load > 0:
		cargo_hold[item_type] = cargo_hold.get(item_type, 0) + to_load
		cargo_loaded.emit(item_type, to_load)
	return to_load

func unload_cargo(item_type: String, count: int) -> int:
	if not cargo_hold.has(item_type) or count <= 0:
		return 0
	var available = cargo_hold[item_type]
	var to_unload = min(count, available)
	cargo_hold[item_type] -= to_unload
	if cargo_hold[item_type] <= 0:
		cargo_hold.erase(item_type)
	cargo_unloaded.emit(item_type, to_unload)
	return to_unload

func calculate_points_of_sail(rel_angle_deg: float) -> float:
	# rel_angle_deg: 0 to 180 degrees
	if rel_angle_deg < 35.0:
		return 0.0 # In irons (cannot sail directly into wind)
	elif rel_angle_deg < 70.0:
		return 0.55 # Close hauled
	elif rel_angle_deg < 110.0:
		return 0.90 # Beam reach
	elif rel_angle_deg < 155.0:
		return 1.00 # Broad reach (optimal for square/lateen rig)
	else:
		return 0.78 # Running dead downwind

func calculate_current_speed() -> float:
	if is_docked or crew_count < min_crew_required or hull_integrity_pct <= 10.0:
		return 0.0

	var angle_diff = abs(fmod(heading_degrees - wind_direction_degrees + 180.0, 360.0) - 180.0)
	var sail_efficiency = calculate_points_of_sail(angle_diff)
	var wind_factor = clamp(wind_speed_knots / 15.0, 0.2, 1.2)
	var crew_efficiency = clamp(float(crew_count) / float(crew_capacity), 0.5, 1.0)
	var hull_factor = hull_integrity_pct / 100.0

	return max_speed_knots * sail_efficiency * wind_factor * crew_efficiency * hull_factor

func depart_on_voyage(route_name: String, dest_port: String, distance_nm: float) -> bool:
	if not is_docked or crew_count < min_crew_required:
		return false
	active_route_name = route_name
	target_port = dest_port
	voyage_total_distance_nm = max(1.0, distance_nm)
	voyage_distance_covered_nm = 0.0
	is_docked = false
	return true

func process_voyage(delta: float) -> Dictionary:
	if is_docked:
		current_speed_knots = 0.0
		return {
			"is_docked": true,
			"current_speed_knots": 0.0,
			"progress": 0.0,
			"port": home_port
		}

	current_speed_knots = calculate_current_speed()
	# 1 knot = 1 nautical mile per hour = 1/3600 nm per second
	var nm_covered = (current_speed_knots / 3600.0) * delta
	voyage_distance_covered_nm = min(voyage_total_distance_nm, voyage_distance_covered_nm + nm_covered)
	var progress = voyage_distance_covered_nm / voyage_total_distance_nm

	if progress >= 1.0:
		is_docked = true
		port_arrived.emit(target_port)
		voyage_completed.emit(int(get_total_cargo_count() * 1.5))

	return {
		"is_docked": is_docked,
		"current_speed_knots": current_speed_knots,
		"distance_covered_nm": voyage_distance_covered_nm,
		"total_distance_nm": voyage_total_distance_nm,
		"progress": progress,
		"current_port": target_port if is_docked else "At Sea"
	}
