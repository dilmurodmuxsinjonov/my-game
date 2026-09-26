# scripts/world/baker_oven.gd
# Voxel Lord: Feudal Realm - Milestone 30: Vaulted Brick Dome Bread Bakery Oven
# Thermal mass heating, firewood fuel, and batch baking for rye and royal brioche loaves.

class_name BakerOven
extends RefCounted

signal oven_heated(temp_celsius: float)
signal baking_started(recipe_name: String, batch_size: int)
signal batch_finished(recipe_name: String, loaves_produced: int)
signal fuel_exhausted(oven_id: String)

const OPTIMAL_TEMP = 220.0
const AMBIENT_TEMP = 20.0

var oven_id: String = "baker_oven_1"
var temperature_celsius: float = AMBIENT_TEMP
var firewood_units: int = 4
var current_batch: Dictionary = {}
var baked_loaves: Dictionary = {
	"rye_bread": 0,
	"royal_brioche": 0
}

func _init(p_id: String = "baker_oven_1", initial_firewood: int = 4) -> void:
	oven_id = p_id
	firewood_units = initial_firewood

func add_firewood(amount: int) -> int:
	firewood_units += amount
	return firewood_units

func heat_up(delta: float) -> float:
	if firewood_units > 0 and temperature_celsius < OPTIMAL_TEMP:
		temperature_celsius = min(OPTIMAL_TEMP, temperature_celsius + 25.0 * delta)
		oven_heated.emit(temperature_celsius)
	elif firewood_units <= 0:
		temperature_celsius = max(AMBIENT_TEMP, temperature_celsius - 8.0 * delta)
	return temperature_celsius

func start_baking_batch(recipe_name: String, ingredients: Dictionary) -> bool:
	if temperature_celsius < 180.0 or not current_batch.is_empty():
		return false

	if recipe_name == "rye_bread":
		if ingredients.get("flour", 0) < 2 or ingredients.get("water", 0) < 1:
			return false
		current_batch = {
			"recipe": "rye_bread",
			"progress": 0.0,
			"duration": 15.0, # 15s per batch
			"yield": 3
		}
	elif recipe_name == "royal_brioche":
		if ingredients.get("flour", 0) < 2 or ingredients.get("milk", 0) < 1 or ingredients.get("honey", 0) < 1:
			return false
		current_batch = {
			"recipe": "royal_brioche",
			"progress": 0.0,
			"duration": 20.0, # 20s per batch
			"yield": 3
		}
	else:
		return false

	baking_started.emit(recipe_name, current_batch["yield"])
	return true

func process_baking(delta: float) -> Dictionary:
	if current_batch.is_empty():
		return {"baking": false, "ready_bread": baked_loaves}

	# Baking requires maintaining oven temperature
	heat_up(delta)
	current_batch["progress"] += delta

	var done = false
	if current_batch["progress"] >= current_batch["duration"]:
		var r = current_batch["recipe"]
		var loaves = current_batch["yield"]
		baked_loaves[r] = baked_loaves.get(r, 0) + loaves
		batch_finished.emit(r, loaves)
		current_batch.clear()
		done = true

	return {
		"baking": not done,
		"batch_completed": done,
		"temperature": temperature_celsius,
		"ready_bread": baked_loaves
	}

func take_bread(recipe_name: String, amount: int) -> int:
	var available = baked_loaves.get(recipe_name, 0)
	var taken = min(amount, available)
	baked_loaves[recipe_name] = available - taken
	return taken
