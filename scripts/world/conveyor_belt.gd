class_name ConveyorBelt
extends StaticBody3D

## Create-style Mechanical Conveyor Belt.
## Driven by rotational torque from Kinetic Water Wheels or Windmills (consumes 16 Stress Units).
## Stitched heavy leather belt moving across brass idler pulleys at 2.0 m/s.
## Automatically transports mined ores, ingots, crops, and flour between adjacent
## workstations, silos, and kingdom stockpiles without requiring manual hauler trips.

signal item_transported(item_name: String, destination: Vector3)

@export var stress_impact: float = 16.0 # Stress Units (SU)
@export var belt_speed: float = 2.0 # Meters per second

var supply_chain: SupplyChain = null
var kinetic_source: Node = null
var is_powered: bool = false
var carried_items: Array[Dictionary] = []
var belt_phase: float = 0.0

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
	box.size = Vector3(1.0, 0.45, 2.0)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.22, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/conveyor_belt.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	prompt_label = Label3D.new()
	prompt_label.text = "⚙️ Mechanical Conveyor Belt\n[ Searching Kinetic Axle... ]"
	prompt_label.position = Vector3(0, 0.8, 0)
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
		belt_phase += delta * belt_speed
		_transport_items(delta)
	else:
		_update_prompt()

func insert_item(item_name: String, count: int = 1) -> bool:
	if not is_powered:
		return false
	carried_items.append({
		"item": item_name,
		"count": count,
		"progress": 0.0 # 0.0 to 1.0 along belt length
	})
	return true

func _transport_items(delta: float) -> void:
	var items_to_remove: Array[int] = []
	for i in range(carried_items.size()):
		carried_items[i]["progress"] += delta * (belt_speed / 2.0)
		if carried_items[i]["progress"] >= 1.0:
			var completed = carried_items[i]
			items_to_remove.append(i)
			emit_signal("item_transported", completed["item"], global_position + -transform.basis.z * 1.0)
			if supply_chain:
				supply_chain.add_resource(completed["item"], completed["count"])

	for idx in range(items_to_remove.size() - 1, -1, -1):
		carried_items.remove_at(items_to_remove[idx])

	_update_prompt()

func _update_prompt() -> void:
	if not prompt_label:
		return
	if is_powered:
		prompt_label.text = "⚙️ Conveyor Belt (Running: %.1f m/s)\nCarrying: %d item(s)" % [belt_speed, carried_items.size()]
		prompt_label.modulate = Color(0.4, 0.95, 0.5)
	else:
		prompt_label.text = "⚠️ Conveyor Belt (Unpowered)\nRequires 16 SU Kinetic Drive"
		prompt_label.modulate = Color(0.9, 0.45, 0.2)

# --- Static Simulation & Balance Calculations ---

static func calculate_belt_throughput(speed_rpm: float, belt_length: float) -> float:
	## Linear speed = (RPM / 60) * (2 * PI * roller_radius)
	var roller_radius = 0.10 # m
	var linear_speed = (speed_rpm / 60.0) * (2.0 * PI * roller_radius)
	var travel_time = belt_length / maxf(linear_speed, 0.1)
	var items_per_second = linear_speed / 0.5 # 1 item per 0.5 meter spacing
	return items_per_second
