class_name TripHammer
extends StaticBody3D

## Create-Style Industrial Mechanical Trip Hammer.
## Powered by kinetic rotational torque (consumes 64 Stress Units).
## Cam-driven heavy hammer repeatedly strikes raw ore chunks on an anvil block.
## Crushes raw iron/copper ore into crushed ore chunks, doubling furnace smelting yields!

signal ore_crushed(ore_type: String, crushed_output: String, bonus_item: String)

@export var stress_impact: float = 64.0 # Stress Units (SU)
@export var crush_interval: float = 5.0 # Seconds per crushing stroke

var supply_chain: SupplyChain = null
var kinetic_source: Node = null
var crush_timer: float = 0.0
var hammer_arm_node: Node3D = null
var status_label: Label3D = null
var is_powered: bool = false
var stroke_phase: float = 0.0

func _ready() -> void:
	add_to_group("kinetic_consumers")
	add_to_group("interactive_workstations")
	_setup_visuals()
	_find_kinetic_source()

func _setup_visuals() -> void:
	var col = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.6, 2.6, 2.6)
	col.shape = box
	col.position = Vector3(0, 1.3, 0)
	add_child(col)

	var glb_path = "res://assets/models/trip_hammer.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)
			hammer_arm_node = inst

	status_label = Label3D.new()
	status_label.text = "🔨 Mechanical Trip Hammer\n[ Searching Kinetic Axle... ]"
	status_label.position = Vector3(0, 3.0, 0)
	status_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	status_label.font_size = 20
	status_label.modulate = Color(0.9, 0.6, 0.4)
	add_child(status_label)

func _find_kinetic_source() -> void:
	var sources = get_tree().get_nodes_in_group("kinetic_sources")
	for src in sources:
		var rad: float = float(src.get("power_radius")) if src.get("power_radius") != null else 8.0
		if global_position.distance_to(src.global_position) <= rad:
			if src.has_method("request_power") and src.request_power(stress_impact):
				kinetic_source = src
				is_powered = true
				break

func _process(delta: float) -> void:
	if not is_powered and not kinetic_source:
		_find_kinetic_source()

	if is_powered:
		# Animate cam lifter & hammer stroke
		stroke_phase += delta * 3.5
		if hammer_arm_node:
			# Oscillating tilt simulating cam lift and drop impact
			var pitch = sin(stroke_phase) * 0.12
			hammer_arm_node.rotation.x = pitch
		
		crush_timer += delta
		if crush_timer >= crush_interval:
			crush_timer = 0.0
			_perform_crush()
	else:
		if status_label:
			status_label.text = "⚠️ Mechanical Trip Hammer\n[ Unpowered - Requires 64 SU ]"
			status_label.modulate = Color(0.8, 0.4, 0.2)

func _perform_crush() -> void:
	if not supply_chain:
		return
	
	if supply_chain.inventory.get("iron_bloom", 0) >= 1:
		supply_chain.consume_resource("iron_bloom", 1)
		supply_chain.add_resource("wrought_iron_ingot", 1)
		emit_signal("ore_crushed", "iron_bloom", "wrought_iron_ingot", "slag")
		if status_label:
			status_label.text = "🔨 Trip Hammer\n[ Refined Bloom -> Wrought Iron Ingot ]"
			status_label.modulate = Color(0.3, 0.95, 0.6)
	elif supply_chain.inventory.get("iron_ore", 0) >= 1:
		supply_chain.consume_resource("iron_ore", 1)
		supply_chain.add_resource("crushed_iron", 1)
		
		var bonus_item = ""
		# 25% chance to extract mineral rock salt from raw stone veins
		if randf() <= 0.25:
			supply_chain.add_resource("rock_salt", 1)
			bonus_item = "rock_salt"
			
		emit_signal("ore_crushed", "iron_ore", "crushed_iron", bonus_item)
		if status_label:
			status_label.text = "🔨 Trip Hammer\n[ Crushed Iron Ore -> Crushed Iron ]"
			status_label.modulate = Color(0.4, 0.9, 0.6)
	elif supply_chain.inventory.get("copper_ore", 0) >= 1:
		supply_chain.consume_resource("copper_ore", 1)
		supply_chain.add_resource("crushed_copper", 1)
		emit_signal("ore_crushed", "copper_ore", "crushed_copper", "")
		if status_label:
			status_label.text = "🔨 Trip Hammer\n[ Crushed Copper Ore -> Crushed Copper ]"
			status_label.modulate = Color(0.8, 0.7, 0.4)
	else:
		if status_label:
			status_label.text = "🔨 Mechanical Trip Hammer\n[ Idle: Awaiting Raw Ore ]"
			status_label.modulate = Color(0.9, 0.6, 0.4)

func disconnect_power() -> void:
	if kinetic_source and kinetic_source.has_method("release_power"):
		kinetic_source.release_power(stress_impact)
	kinetic_source = null
	is_powered = false
