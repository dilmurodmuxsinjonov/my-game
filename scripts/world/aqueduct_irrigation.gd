# scripts/world/aqueduct_irrigation.gd
# Voxel Lord: Feudal Realm - Milestone 27 / Milestone 2: Elevated Flume Irrigation & Hydraulics
# Simulates Roman-style stone aqueducts delivering moisture saturation to inland farm plots,
# fluid volume conservation across channel networks, conveyance losses, and freeze/thaw transitions.

class_name AqueductIrrigation
extends RefCounted

signal irrigation_active(aqueduct_id: String, moisture_radius: float)
signal flow_interrupted(aqueduct_id: String, reason: String)
signal volume_changed(aqueduct_id: String, new_volume: float)
signal channel_frozen(aqueduct_id: String)
signal channel_thawed(aqueduct_id: String)

enum ChannelType {
	STONE_AQUEDUCT = 0,
	CLAY_CANAL = 1,
	DIRT_DITCH = 2
}

# Conveyance loss per 10 meters:
# Stone Aqueduct: 0%, Clay Canal: 2%, Dirt Ditch: 8%
const CONVEYANCE_LOSS_PER_10M: Dictionary = {
	ChannelType.STONE_AQUEDUCT: 0.0,
	ChannelType.CLAY_CANAL: 0.02,
	ChannelType.DIRT_DITCH: 0.08
}

const FLOW_VELOCITIES: Dictionary = {
	ChannelType.STONE_AQUEDUCT: 3.5, # m/s
	ChannelType.CLAY_CANAL: 1.8,
	ChannelType.DIRT_DITCH: 1.2
}

var aqueduct_id: String = "aqueduct_segment_1"
var is_connected_to_source: bool = true
var moisture_radius: float = 8.0 # 8-meter saturation zone
var growth_speed_bonus: float = 0.30 # +30% growth speed
var max_hp: float = 150.0
var current_hp: float = 150.0

# Upgraded hydraulics & thermal properties
var channel_type: int = ChannelType.STONE_AQUEDUCT
var length_meters: float = 10.0
var max_volume: float = 10.0 # m³
var current_volume: float = 10.0 # m³
var flow_rate: float = 3.5 # m³/s
var is_frozen: bool = false
var ambient_temperature: float = 15.0 # °C

func _init(
	p_id: String = "aqueduct_segment_1",
	connected: bool = true,
	p_type: int = ChannelType.STONE_AQUEDUCT,
	p_length: float = 10.0
) -> void:
	aqueduct_id = p_id
	is_connected_to_source = connected
	channel_type = p_type
	length_meters = p_length
	flow_rate = FLOW_VELOCITIES.get(channel_type, 3.5)
	max_volume = length_meters * 1.0 # 1 m² cross section
	current_volume = max_volume if connected else 0.0

func set_water_source_connection(connected: bool) -> void:
	is_connected_to_source = connected
	if connected and not is_frozen and current_hp > 0.0:
		current_volume = max_volume
		irrigation_active.emit(aqueduct_id, moisture_radius)
	else:
		if not connected:
			current_volume = 0.0
			flow_interrupted.emit(aqueduct_id, "SourceDisconnected")

func is_soil_saturated(crop_pos: Vector2, aqueduct_pos: Vector2) -> bool:
	if not is_connected_to_source or current_hp <= 0.0 or is_frozen or current_volume <= 0.001:
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
		current_volume = 0.0
		flow_interrupted.emit(aqueduct_id, "AqueductDestroyed")

func repair(amount: float) -> void:
	current_hp = min(max_hp, current_hp + amount)
	if current_hp > 0.0 and not is_frozen and is_connected_to_source:
		irrigation_active.emit(aqueduct_id, moisture_radius)

# -------------------------------------------------------------------------
# Hydraulics & Thermal Enhancements
# -------------------------------------------------------------------------
func calculate_conveyance_loss(distance_m: float = -1.0) -> float:
	var dist = length_meters if distance_m < 0.0 else distance_m
	var rate_per_10m = CONVEYANCE_LOSS_PER_10M.get(channel_type, 0.0)
	return (rate_per_10m / 10.0) * dist

func update_ambient_temperature(temp_celsius: float) -> void:
	ambient_temperature = temp_celsius
	
	# Freezing threshold at <= 0.0°C
	if ambient_temperature <= 0.0 and not is_frozen:
		is_frozen = true
		flow_interrupted.emit(aqueduct_id, "WaterFrozen")
		channel_frozen.emit(aqueduct_id)
	elif ambient_temperature > 0.0 and is_frozen:
		is_frozen = false
		channel_thawed.emit(aqueduct_id)
		if current_hp > 0.0 and current_volume > 0.0:
			is_connected_to_source = true
			irrigation_active.emit(aqueduct_id, moisture_radius)

func transfer_water(target: AqueductIrrigation, dt: float) -> float:
	if is_frozen or target.is_frozen or current_volume <= 0.0001:
		return 0.0
	if current_hp <= 0.0 or target.current_hp <= 0.0:
		return 0.0
		
	var available_capacity = max(0.0, target.max_volume - target.current_volume)
	if available_capacity <= 0.0001:
		return 0.0
		
	var flow_budget = min(current_volume, available_capacity, flow_rate * dt)
	var loss_factor = calculate_conveyance_loss(length_meters)
	var delivered_volume = flow_budget * (1.0 - loss_factor)
	
	current_volume -= flow_budget
	target.current_volume += delivered_volume
	
	volume_changed.emit(aqueduct_id, current_volume)
	target.volume_changed.emit(target.aqueduct_id, target.current_volume)
	
	return delivered_volume
