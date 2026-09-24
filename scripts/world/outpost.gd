class_name Outpost
extends Node3D

## Frontier Outpost & Logistics Hub.
## Inspired by Bellwright and Manor Lords:
## Establishes a forward camp at distant resource nodes (deep mines, logging forests),
## housing local workers and dispatching automated pack caravans when min threshold is met.

signal resource_deposited(item: String, amount: int, current_buffer: int)
signal caravan_dispatched(outpost_name: String, cargo: Dictionary)
signal caravan_arrived_at_capital(cargo: Dictionary)

@export var outpost_name: String = "Frontier Outpost"
@export var min_dispatch_threshold: int = 10 # Items needed to trigger wagon dispatch
@export var max_buffer_capacity: int = 50

var buffer_inventory: Dictionary = {}
var assigned_workers: Array[String] = []
var supply_chain: SupplyChain = null
var model_node: Node3D = null

func _ready() -> void:
	_load_model()

func _load_model() -> void:
	var glb_path = "res://assets/models/outpost_banner.glb"
	if ResourceLoader.exists(glb_path):
		var scene = load(glb_path)
		if scene:
			model_node = scene.instantiate()
			add_child(model_node)

func deposit_resource(item: String, amount: int) -> bool:
	var current_total = get_total_buffer_items()
	if current_total + amount > max_buffer_capacity:
		return false # Buffer full
	
	buffer_inventory[item] = buffer_inventory.get(item, 0) + amount
	emit_signal("resource_deposited", item, amount, buffer_inventory[item])
	
	if should_dispatch_caravan():
		dispatch_caravan()
	return true

func get_total_buffer_items() -> int:
	var total = 0
	for count in buffer_inventory.values():
		total += count
	return total

func should_dispatch_caravan() -> bool:
	return get_total_buffer_items() >= min_dispatch_threshold

func dispatch_caravan() -> Dictionary:
	var cargo = buffer_inventory.duplicate()
	buffer_inventory.clear()
	
	emit_signal("caravan_dispatched", outpost_name, cargo)
	
	if supply_chain:
		for item in cargo.keys():
			supply_chain.add_resource(item, cargo[item])
		emit_signal("caravan_arrived_at_capital", cargo)
		
	return cargo
