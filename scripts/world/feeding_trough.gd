# scripts/world/feeding_trough.gd
# Voxel Lord: Feudal Realm - Milestone 24: Winter Livestock Fodder & Trough Management
# Inspired by RimWorld (Nutrient Dispensers & Animal Feed) and Medieval Dynasty (Winter Animal Starvation)

class_name FeedingTrough
extends Node3D

signal fodder_consumed(amount: int, remaining: int)
signal trough_refilled(amount: int, total: int)
signal trough_empty_warning()

const MAX_FODDER_CAPACITY: int = 40
const FREEZING_TEMP_THRESHOLD: float = 5.0 # Celsius; below this pasture grass is frozen

var stored_fodder: int = 20

func _init() -> void:
	stored_fodder = 20

func add_fodder(amount: int) -> int:
	if amount <= 0:
		return 0
	
	var space: int = MAX_FODDER_CAPACITY - stored_fodder
	var added: int = mini(amount, space)
	stored_fodder += added
	trough_refilled.emit(added, stored_fodder)
	return added

func consume_for_livestock(animal_count: int, ambient_temp: float) -> bool:
	if animal_count <= 0:
		return true
	
	# Warm seasons: Livestock can graze outside in lush pastures freely
	if ambient_temp >= FREEZING_TEMP_THRESHOLD:
		return true
	
	# Winter / Freeze: Livestock require stored hay/silage from the trough
	var needed: int = animal_count
	if stored_fodder >= needed:
		stored_fodder -= needed
		fodder_consumed.emit(needed, stored_fodder)
		return true
	else:
		# Partial or zero fodder: animals starve
		stored_fodder = 0
		trough_empty_warning.emit()
		return false
