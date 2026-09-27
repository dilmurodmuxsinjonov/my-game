# scripts/mechanisms/hopper_unloader.gd
class_name HopperUnloader
extends Node3D

# Trackside Bottom-Dump Hopper Unloader Station
# Inspired by Create Mod, Railcraft, and Vintage Story
# Rapidly evacuates bulk ores and coal from hopper cars into subterranean chutes and conveyor lines.

signal cart_unloaded(cart_id: String, item_count: int)
signal hopper_full()
signal items_discharged_downstream(item_type: String, count: int)

@export var unloader_id: String = "unloader_01"
@export var hopper_capacity_items: int = 120
@export var discharge_rate_items_s: float = 12.0 # Empties 30-slot cart in 2.5s
@export var chute_transfer_rate_items_s: float = 8.0 # Feed to conveyor/furnace

var buffer_inventory: Dictionary = {} # item_type -> count
var is_cart_docked: bool = false
var current_cart_id: String = ""
var trip_lever_engaged: bool = false
var unloading_timer: float = 0.0
var total_unloaded_lifetime: int = 0
var downstream_receiver_connected: bool = true

func _init(id: String = "unloader_01"):
	unloader_id = id
	buffer_inventory = {}

func get_total_stored_items() -> int:
	var total: int = 0
	for count in buffer_inventory.values():
		total += count
	return total

func get_free_capacity() -> int:
	return hopper_capacity_items - get_total_stored_items()

func dock_hopper_cart(cart_id: String, cart_inventory: Dictionary) -> bool:
	if is_cart_docked:
		return false
	if get_free_capacity() <= 0:
		hopper_full.emit()
		return false

	is_cart_docked = true
	current_cart_id = cart_id
	trip_lever_engaged = true
	unloading_timer = 0.0
	return true

func undock_cart() -> void:
	is_cart_docked = false
	current_cart_id = ""
	trip_lever_engaged = false
	unloading_timer = 0.0

func process_unloader(delta: float, cart_inventory: Dictionary = {}) -> Dictionary:
	var items_unloaded_this_tick: int = 0
	var items_fed_downstream_this_tick: int = 0

	# 1. Unload from docked cart
	if is_cart_docked and trip_lever_engaged and not cart_inventory.is_empty():
		unloading_timer += delta
		var max_items_to_drain: int = int(discharge_rate_items_s * delta)
		if max_items_to_drain < 1 and randf() < (discharge_rate_items_s * delta):
			max_items_to_drain = 1

		var keys_to_remove: Array = []
		for item_type in cart_inventory.keys():
			if items_unloaded_this_tick >= max_items_to_drain or get_free_capacity() <= 0:
				break

			var available_in_cart: int = cart_inventory[item_type]
			var space_available: int = get_free_capacity()
			var transfer_amount: int = min(min(available_in_cart, max_items_to_drain - items_unloaded_this_tick), space_available)

			if transfer_amount > 0:
				cart_inventory[item_type] -= transfer_amount
				if cart_inventory[item_type] <= 0:
					keys_to_remove.append(item_type)

				buffer_inventory[item_type] = buffer_inventory.get(item_type, 0) + transfer_amount
				items_unloaded_this_tick += transfer_amount
				total_unloaded_lifetime += transfer_amount

		for k in keys_to_remove:
			cart_inventory.erase(k)

		if cart_inventory.is_empty() and items_unloaded_this_tick > 0:
			cart_unloaded.emit(current_cart_id, items_unloaded_this_tick)

	# 2. Downstream chute feed to conveyor / smelting bunker
	if downstream_receiver_connected and get_total_stored_items() > 0:
		var max_feed: int = int(chute_transfer_rate_items_s * delta)
		if max_feed < 1 and randf() < (chute_transfer_rate_items_s * delta):
			max_feed = 1

		var empty_buffer_keys: Array = []
		for item_type in buffer_inventory.keys():
			if items_fed_downstream_this_tick >= max_feed:
				break

			var in_buffer: int = buffer_inventory[item_type]
			var send_amount: int = min(in_buffer, max_feed - items_fed_downstream_this_tick)
			if send_amount > 0:
				buffer_inventory[item_type] -= send_amount
				if buffer_inventory[item_type] <= 0:
					empty_buffer_keys.append(item_type)

				items_fed_downstream_this_tick += send_amount
				items_discharged_downstream.emit(item_type, send_amount)

		for k in empty_buffer_keys:
			buffer_inventory.erase(k)

	return {
		"is_cart_docked": is_cart_docked,
		"trip_lever_engaged": trip_lever_engaged,
		"total_stored_items": get_total_stored_items(),
		"free_capacity": get_free_capacity(),
		"items_unloaded_tick": items_unloaded_this_tick,
		"items_discharged_tick": items_fed_downstream_this_tick,
		"total_unloaded_lifetime": total_unloaded_lifetime
	}
