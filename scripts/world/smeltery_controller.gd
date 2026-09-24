class_name SmelteryController
extends Node3D

## Tinkers' Construct Smeltery Multiblock Controller.
## Melts raw ores and ingots into molten metals using lava or charcoal,
## auto-alloys liquids (e.g. Copper + Tin -> Bronze), and pours into casting stations.

signal temperature_changed(current_temp: float, max_temp: float)
signal liquid_alloyed(alloy_log: String)
signal metal_melted(metal_type: String, units: int)
signal liquid_drained(metal_type: String, units: int)

const MAX_CAPACITY: int = 36 # Max molten metal units in internal tank
const MAX_TEMPERATURE: float = 1600.0 # Celsius
const AMBIENT_TEMP: float = 20.0

@export var current_temperature: float = 20.0
@export var target_temperature: float = 20.0
@export var fuel_timer: float = 0.0 # Seconds of fuel remaining
@export var is_multiblock_formed: bool = true

# Internal tank contents: { "copper": 6, "tin": 2, "bronze": 4, ... }
var molten_tank: Dictionary = {}

# Solid queue waiting to melt: [ { "item": "copper_ore", "metal": "copper", "progress": 0.0, "max_progress": 10.0 } ]
var melting_queue: Array[Dictionary] = []

var supply_chain: SupplyChain = null
var model_node: Node3D = null

func _ready() -> void:
	_load_model()

func _load_model() -> void:
	var glb_path = "res://assets/models/smeltery_controller.glb"
	if ResourceLoader.exists(glb_path):
		var scene = load(glb_path)
		if scene:
			model_node = scene.instantiate()
			add_child(model_node)

func add_fuel(fuel_type: String, count: int = 1) -> bool:
	if fuel_type == "lava" or fuel_type == "lava_bucket":
		fuel_timer += 120.0 * count
		target_temperature = 1550.0
		return true
	elif fuel_type == "charcoal":
		fuel_timer += 45.0 * count
		target_temperature = 1350.0
		return true
	elif fuel_type == "coal":
		fuel_timer += 35.0 * count
		target_temperature = 1200.0
		return true
	return false

func add_solid_item(item_id: String, count: int = 1) -> bool:
	var total_queued_and_tank = get_total_molten_units() + melting_queue.size()
	if total_queued_and_tank + count > MAX_CAPACITY:
		return false # Tank full

	var metal_type = ""
	var units_yield = 1
	var melt_time = 8.0

	if "copper" in item_id:
		metal_type = "copper"
		units_yield = 2 if "ore" in item_id else 1 # Ore doubles yield in smeltery!
	elif "tin" in item_id:
		metal_type = "tin"
		units_yield = 2 if "ore" in item_id else 1
	elif "iron" in item_id:
		metal_type = "iron"
		units_yield = 2 if "ore" in item_id else 1
	elif "gold" in item_id:
		metal_type = "gold"
		units_yield = 2 if "ore" in item_id else 1
	elif "silver" in item_id:
		metal_type = "silver"
		units_yield = 2 if "ore" in item_id else 1
	elif "coal" in item_id or "carbon" in item_id:
		metal_type = "carbon"
		units_yield = 1
		melt_time = 4.0
	else:
		return false # Not a smeltable metal

	for i in range(count):
		melting_queue.append({
			"item_id": item_id,
			"metal_type": metal_type,
			"yield": units_yield,
			"progress": 0.0,
			"melt_time": melt_time
		})
	return true

func tick(delta: float) -> void:
	# 1. Fuel and temperature dynamics
	if fuel_timer > 0.0:
		fuel_timer -= delta
		if current_temperature < target_temperature:
			current_temperature = min(target_temperature, current_temperature + (45.0 * delta))
	else:
		target_temperature = AMBIENT_TEMP
		if current_temperature > AMBIENT_TEMP:
			current_temperature = max(AMBIENT_TEMP, current_temperature - (15.0 * delta))

	emit_signal("temperature_changed", current_temperature, MAX_TEMPERATURE)

	# 2. Melting progress
	var i = 0
	while i < melting_queue.size():
		var entry = melting_queue[i]
		var req_temp = AlloyManager.get_melting_point(entry["metal_type"])
		if current_temperature >= req_temp:
			entry["progress"] += delta
			if entry["progress"] >= entry["melt_time"]:
				# Melted successfully into tank
				var m_type = entry["metal_type"]
				var m_yield = entry["yield"]
				molten_tank[m_type] = molten_tank.get(m_type, 0) + m_yield
				emit_signal("metal_melted", m_type, m_yield)
				melting_queue.remove_at(i)
				continue
		i += 1

	# 3. Metallurgical Alloying reaction
	var alloy_logs = AlloyManager.process_alloys(molten_tank, current_temperature)
	for log_msg in alloy_logs:
		emit_signal("liquid_alloyed", log_msg)

func drain_liquid(metal_type: String, requested_units: int) -> int:
	var available = molten_tank.get(metal_type, 0)
	if available <= 0:
		return 0
	var drained = min(available, requested_units)
	molten_tank[metal_type] -= drained
	if molten_tank[metal_type] <= 0:
		molten_tank.erase(metal_type)
	emit_signal("liquid_drained", metal_type, drained)
	return drained

func get_bottom_metal() -> String:
	var keys = molten_tank.keys()
	if keys.is_empty():
		return ""
	return keys[0]

func get_total_molten_units() -> int:
	var total = 0
	for count in molten_tank.values():
		total += count
	return total
