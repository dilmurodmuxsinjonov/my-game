class_name RoyalLedger
extends Control

## Royal Ledger UI Controller - The player's main kingdom management interface.

signal role_changed(role_name: String, delta_count: int)
signal tax_rate_changed(new_rate: float)

@export var supply_chain: SupplyChain

# UI Node References
var morale_label: Label
var population_label: Label
var inventory_tree: Tree
var role_buttons: Dictionary = {}

var is_open: bool = false

func _ready() -> void:
	visible = false

func toggle_ledger() -> void:
	is_open = not is_open
	visible = is_open
	if is_open:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		_refresh_display()
	else:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _refresh_display() -> void:
	if not supply_chain:
		return
	# Update morale bar, food counts, tool levels
	print("[Ledger] Morale: %.1f%%, Bread: %d, Tools: %d" % [
		supply_chain.morale,
		supply_chain.inventory.get("bread", 0),
		supply_chain.inventory.get("tools", 0)
	])

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("toggle_ledger") or (event is InputEventKey and event.pressed and event.keycode == KEY_TAB):
		toggle_ledger()
