# scripts/world/aqueduct_irrigation.gd
# Voxel Lord: Feudal Realm - Milestone 27: Elevated Flume Irrigation
# Simulates Roman-style stone aqueducts delivering moisture saturation to inland farm plots.

class_name AqueductIrrigation
extends RefCounted

signal irrigation_active(aqueduct_id: String, moisture_radius: float)
signal flow_interrupted(aqueduct_id: String, reason: String)

var aqueduct_id: String = "aqueduct_segment_1"
var is_connected_to_source: bool = true
var moisture_radius: float = 8.0 # 8-meter saturation zone
var growth_speed_bonus: float = 0.30 # +30% growth speed
var max_hp: float = 150.0
var current_hp: float = 150.0

func _init(p_id: String = "aqueduct_segment_1", connected: bool = true) -> void:
	aqueduct_id = p_id
	is_connected_to_source = connected

func set_water_source_connection(connected: bool) -> void:
	is_connected_to_source = connected
	if connected:
		irrigation_active.emit(aqueduct_id, moisture_radius)
	else:
		flow_interrupted.emit(aqueduct_id, "SourceDisconnected")

func is_soil_saturated(crop_pos: Vector2, aqueduct_pos: Vector2) -> bool:
	if not is_connected_to_source or current_hp <= 0.0:
		return false
	var distance = crop_pos.distance_to(aqueduct_pos)
	return distance <= moisture_radius

func calculate_effective_growth_speed(base_speed: float, crop_pos: Vector2, aqueduct_pos: Vector2, is_drought: bool = false) -> float:
	if is_soil_saturated(crop_pos, aqueduct_pos):
		# Saturated soil accelerates growth by 30% and protects against drought withering
		return base_speed * (1.0 + growth_speed_bonus)
	elif is_drought:
		# Unirrigated crops wither and grow 60% slower during drought
		return base_speed * 0.40
	return base_speed

func take_damage(amount: float) -> void:
	current_hp = max(0.0, current_hp - amount)
	if current_hp <= 0.0:
		is_connected_to_source = false
		flow_interrupted.emit(aqueduct_id, "AqueductDestroyed")

func repair(amount: float) -> void:
	current_hp = min(max_hp, current_hp + amount)
