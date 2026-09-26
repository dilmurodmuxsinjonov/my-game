# scripts/world/stone_windmill.gd
# Voxel Lord: Feudal Realm - Milestone 30: Stone Windmill Kinetic Power & Grain Milling
# Atmospheric wind velocity scaling, 384 SU mechanical output, and automated grindstone milling.

class_name StoneWindmill
extends RefCounted

signal wind_changed(velocity: float, power_output: float)
signal grain_milled(wheat_consumed: int, flour_produced: int)
signal hopper_empty(windmill_id: String)

var windmill_id: String = "stone_windmill_1"
var base_power_output: float = 384.0 # Stress Units (SU)
var current_wind_velocity: float = 1.0 # 0.5x to 1.8x
var wheat_hopper: int = 0
var flour_milled: int = 0
var milling_progress: float = 0.0
var base_milling_rate: float = 1.5 # grains/sec at 1.0x wind

func _init(p_id: String = "stone_windmill_1", initial_wheat: int = 20) -> void:
	windmill_id = p_id
	wheat_hopper = initial_wheat

func update_wind_velocity(altitude_y: float = 30.0, is_stormy: bool = false) -> float:
	var altitude_bonus = clamp((altitude_y - 10.0) * 0.015, 0.0, 0.5)
	var storm_mult = 1.35 if is_stormy else 1.0
	current_wind_velocity = clamp((1.0 + altitude_bonus) * storm_mult, 0.5, 1.8)
	wind_changed.emit(current_wind_velocity, get_kinetic_power_output())
	return current_wind_velocity

func get_kinetic_power_output() -> float:
	return base_power_output * current_wind_velocity

func add_wheat(amount: int) -> int:
	if amount > 0:
		wheat_hopper += amount
	return wheat_hopper

func process_milling(delta: float) -> Dictionary:
	if wheat_hopper <= 0:
		hopper_empty.emit(windmill_id)
		return {"milled": 0, "remaining_wheat": 0, "total_flour": flour_milled}

	var rate = base_milling_rate * current_wind_velocity
	milling_progress += rate * delta

	var grains_to_process = int(floor(milling_progress))
	var processed = min(grains_to_process, wheat_hopper)

	if processed > 0:
		milling_progress -= float(processed)
		wheat_hopper -= processed
		var new_flour = processed * 2 # 1 wheat -> 2 sacks of flour (200% yield)
		flour_milled += new_flour
		grain_milled.emit(processed, new_flour)

	return {
		"processed_wheat": processed,
		"remaining_wheat": wheat_hopper,
		"total_flour": flour_milled,
		"power_su": get_kinetic_power_output()
	}
