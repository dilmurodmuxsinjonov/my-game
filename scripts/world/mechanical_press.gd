class_name MechanicalPress
extends StaticBody3D

## Create-style Industrial Mechanical Stamping Press.
## Driven by kinetic torque (consumes 48 Stress Units).
## Heavy cam-lifted ram strikes metal ingots resting on a hardened steel die block:
## - Iron Ingots / Wrought Iron -> Heavy Iron Sheets (for Knight Plate Armor & Reinforced Shields)
## - Copper Ingots -> Weatherproof Copper Sheets (for Palace Roofing & Fluid Pipes)
## - Gold Ingots -> Royal Minted Gold Coins (1 Gold Ingot = 10 Gold Coins for Trade & Feudal Taxes)

signal item_pressed(input_item: String, output_item: String, count: int)

@export var stress_impact: float = 48.0 # Stress Units (SU)
@export var press_cycle_duration: float = 3.0 # Seconds per stroke

var supply_chain: SupplyChain = null
var kinetic_source: Node = null
var is_powered: bool = false
var stroke_timer: float = 0.0
var ram_node: Node3D = null

var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null

func _ready() -> void:
	add_to_group("kinetic_consumers")
	add_to_group("interactive_workstations")
	_setup_visuals()
	_find_kinetic_source()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.6, 2.7, 1.4)
	collision_box.shape = box
	collision_box.position = Vector3(0, 1.35, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/mechanical_press.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)
			ram_node = model_instance

	prompt_label = Label3D.new()
	prompt_label.text = "🪙 Mechanical Stamping Press\n[ Searching Kinetic Axle... ]"
	prompt_label.position = Vector3(0, 3.0, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 20
	prompt_label.modulate = Color(0.85, 0.7, 0.3)
	add_child(prompt_label)

func _find_kinetic_source() -> void:
	var sources = get_tree().get_nodes_in_group("kinetic_sources")
	for src in sources:
		var rad: float = float(src.get("power_radius")) if src.get("power_radius") != null else 8.0
		if global_position.distance_to(src.global_position) <= rad:
			if src.has_method("request_power") and src.request_power(stress_impact):
				kinetic_source = src
				is_powered = true
				_update_prompt()
				break

func _process(delta: float) -> void:
	if not is_powered and not kinetic_source:
		_find_kinetic_source()

	if is_powered:
		stroke_timer += delta
		# Animate ram drop and raise
		if ram_node:
			var phase = fmod(stroke_timer, press_cycle_duration) / press_cycle_duration
			# Fast downward slam, slow retract
			var y_disp = 0.0
			if phase < 0.2:
				y_disp = -0.35 * (phase / 0.2)
			elif phase < 0.4:
				y_disp = -0.35
			else:
				y_disp = -0.35 * (1.0 - (phase - 0.4) / 0.6)
			ram_node.position.y = y_disp

		if stroke_timer >= press_cycle_duration:
			stroke_timer = 0.0
			_perform_press()
	else:
		_update_prompt()

func _perform_press() -> void:
	if not supply_chain:
		return

	# Priority 1: Gold Ingot -> Royal Gold Coins (Feudal Minting)
	if supply_chain.inventory.get("gold_ingot", 0) >= 1:
		supply_chain.consume_resource("gold_ingot", 1)
		supply_chain.add_resource("gold_coins", 10)
		emit_signal("item_pressed", "gold_ingot", "gold_coins", 10)
		if prompt_label:
			prompt_label.text = "🪙 Minted 10 Royal Gold Coins!"
			prompt_label.modulate = Color(1.0, 0.85, 0.2)
	# Priority 2: Iron Ingot / Wrought Iron -> Heavy Iron Sheet
	elif supply_chain.inventory.get("wrought_iron_ingot", 0) >= 1:
		supply_chain.consume_resource("wrought_iron_ingot", 1)
		supply_chain.add_resource("iron_sheet", 1)
		emit_signal("item_pressed", "wrought_iron_ingot", "iron_sheet", 1)
		if prompt_label:
			prompt_label.text = "🛡️ Pressed Wrought Iron Sheet!"
			prompt_label.modulate = Color(0.4, 0.95, 0.6)
	elif supply_chain.inventory.get("iron_ingots", 0) >= 1:
		supply_chain.consume_resource("iron_ingots", 1)
		supply_chain.add_resource("iron_sheet", 1)
		emit_signal("item_pressed", "iron_ingots", "iron_sheet", 1)
		if prompt_label:
			prompt_label.text = "🛡️ Pressed Iron Sheet!"
			prompt_label.modulate = Color(0.4, 0.95, 0.6)
	# Priority 3: Copper Ingot -> Copper Sheet
	elif supply_chain.inventory.get("copper_ingot", 0) >= 1:
		supply_chain.consume_resource("copper_ingot", 1)
		supply_chain.add_resource("copper_sheet", 1)
		emit_signal("item_pressed", "copper_ingot", "copper_sheet", 1)
		if prompt_label:
			prompt_label.text = "⚡ Pressed Copper Sheet!"
			prompt_label.modulate = Color(0.9, 0.6, 0.3)
	else:
		_update_prompt()

func _update_prompt() -> void:
	if not prompt_label:
		return
	if is_powered:
		prompt_label.text = "🪙 Mechanical Stamping Press (Ready: 48 SU)\n[ Gold -> Coins | Iron -> Sheets ]"
		prompt_label.modulate = Color(0.3, 0.95, 0.6)
	else:
		prompt_label.text = "⚠️ Mechanical Press (Unpowered)\nRequires 48 SU Kinetic Drive"
		prompt_label.modulate = Color(0.9, 0.45, 0.2)

# --- Static Simulation & Balance Calculations ---

static func calculate_press_recipe(input_item: String, count: int) -> Dictionary:
	match input_item:
		"gold_ingot":
			return {
				"output_item": "gold_coins",
				"output_count": count * 10,
				"name": "Royal Gold Coinage"
			}
		"wrought_iron_ingot", "iron_ingots":
			return {
				"output_item": "iron_sheet",
				"output_count": count,
				"name": "Heavy Iron Armor Plate"
			}
		"copper_ingot":
			return {
				"output_item": "copper_sheet",
				"output_count": count,
				"name": "Copper Sheet Metal"
			}
		_:
			return {
				"output_item": "",
				"output_count": 0,
				"name": "Unknown"
			}
