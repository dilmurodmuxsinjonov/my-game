# scripts/world/street_lamp.gd
# Voxel Lord: Feudal Realm - Milestone 29: Street Lamppost Lighting & Crime Deterrence
# Dusk-to-dawn automated street lighting, tallow fuel consumption, and nocturnal criminal deterrence.

class_name StreetLamp
extends RefCounted

signal lamp_lit(lamp_id: String)
signal lamp_extinguished(lamp_id: String)
signal tallow_depleted(lamp_id: String)
signal crime_deterred(lamp_id: String, criminal_pos: Vector3)

var lamp_id: String = "street_lamp_1"
var position: Vector3 = Vector3.ZERO
var lit: bool = false
var tallow_reserve: int = 4 # 1 tallow = 3 full night cycles (approx 36 hours of burn)
var burn_hours_remaining: float = 36.0
var light_radius: float = 9.0

func _init(p_id: String = "street_lamp_1", p_pos: Vector3 = Vector3.ZERO, initial_tallow: int = 4) -> void:
	lamp_id = p_id
	position = p_pos
	tallow_reserve = initial_tallow
	burn_hours_remaining = float(tallow_reserve) * 9.0

func add_tallow(amount: int) -> int:
	if amount <= 0:
		return tallow_reserve
	tallow_reserve += amount
	burn_hours_remaining += float(amount) * 9.0
	return tallow_reserve

func on_time_tick(game_hour: float, delta_hours: float) -> Dictionary:
	var is_night = (game_hour >= 18.0 or game_hour < 6.0)

	if is_night and burn_hours_remaining > 0.0:
		if not lit:
			lit = true
			lamp_lit.emit(lamp_id)

		burn_hours_remaining = max(0.0, burn_hours_remaining - delta_hours)
		tallow_reserve = int(ceil(burn_hours_remaining / 9.0))

		if burn_hours_remaining == 0.0:
			lit = false
			lamp_extinguished.emit(lamp_id)
			tallow_depleted.emit(lamp_id)
	else:
		if lit and not is_night:
			lit = false
			lamp_extinguished.emit(lamp_id)

	return {
		"lit": lit,
		"hours_left": burn_hours_remaining,
		"tallow_left": tallow_reserve,
		"radius": light_radius if lit else 0.0
	}

func is_position_illuminated(target_pos: Vector3) -> bool:
	if not lit:
		return false
	return position.distance_to(target_pos) <= light_radius

func check_crime_deterrence(thief_pos: Vector3) -> bool:
	if is_position_illuminated(thief_pos):
		crime_deterred.emit(lamp_id, thief_pos)
		return true # Thief deterred by bright lantern illumination
	return false
