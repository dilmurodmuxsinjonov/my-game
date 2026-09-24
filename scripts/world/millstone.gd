class_name Millstone
extends StaticBody3D

## Create-Style Mechanical Millstone.
## Powered by kinetic rotational torque (consumes 32 Stress Units).
## Passively grinds grain with twin granite stones at 200% yield (1 wheat -> 2 rations) with zero labor.

signal grain_milled(consumed_wheat: int, produced_bread: int)

@export var stress_impact: float = 32.0 # Stress Units (SU)
@export var grind_interval: float = 4.0 # Seconds per grinding cycle

var supply_chain: SupplyChain = null
var kinetic_source: Node = null
var grind_timer: float = 0.0
var runner_mesh: Node3D = null
var status_label: Label3D = null
var is_powered: bool = false

func _ready() -> void:
	add_to_group("kinetic_consumers")
	add_to_group("interactive_workstations")
	_setup_visuals()
	_find_kinetic_source()

func _setup_visuals() -> void:
	var col = CollisionShape3D.new()
	var cyl = CylinderShape3D.new()
	cyl.radius = 0.75
	cyl.height = 1.8
	col.shape = cyl
	col.position = Vector3(0, 0.9, 0)
	add_child(col)

	var glb_path = "res://assets/models/millstone.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)
			runner_mesh = inst

	status_label = Label3D.new()
	status_label.text = "⚙️ Mechanical Millstone\n[ Searching Kinetic Axle... ]"
	status_label.position = Vector3(0, 2.2, 0)
	status_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	status_label.font_size = 20
	status_label.modulate = Color(0.9, 0.85, 0.6)
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
		# Rotate runner stone
		if runner_mesh:
			runner_mesh.rotate_y(deg_to_rad(45.0) * delta)
		
		grind_timer += delta
		if grind_timer >= grind_interval:
			grind_timer = 0.0
			_perform_grind()
	else:
		if status_label:
			status_label.text = "⚠️ Mechanical Millstone\n[ Unpowered - Requires 32 SU ]"
			status_label.modulate = Color(0.8, 0.4, 0.2)

func _perform_grind() -> void:
	if not supply_chain:
		return
	
	if supply_chain.inventory.get("wheat", 0) >= 1:
		supply_chain.consume_resource("wheat", 1)
		supply_chain.add_resource("bread", 2) # Double yield milling
		emit_signal("grain_milled", 1, 2)
		if status_label:
			status_label.text = "⚙️ Mechanical Millstone\n[ Active: 1 Wheat -> 2 Bread ]"
			status_label.modulate = Color(0.3, 0.9, 0.4)
	else:
		if status_label:
			status_label.text = "⚙️ Mechanical Millstone\n[ Idle: Awaiting Wheat ]"
			status_label.modulate = Color(0.9, 0.85, 0.6)

func disconnect_power() -> void:
	if kinetic_source and kinetic_source.has_method("release_power"):
		kinetic_source.release_power(stress_impact)
	kinetic_source = null
	is_powered = false
