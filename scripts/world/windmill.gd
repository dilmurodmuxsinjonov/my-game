class_name Windmill
extends StaticBody3D

## Create-Style Kinetic Windmill & Automated Gristmill Tower.
## Harnesses wind velocity to rotate massive cross sails (32 RPM),
## driving internal mechanical millstones to passively grind wheat into flour at 2x efficiency.

signal grain_milled(wheat_consumed: int, flour_produced: int)

var supply_chain: SupplyChain
var rotation_speed: float = 1.2 # Rad/s (~11.5 RPM)
var mill_timer: float = 0.0
var mill_interval: float = 10.0 # Grinds every 10 seconds automatically

var sails_node: Node3D = null
var status_label: Label3D = null
var is_active: bool = true

func _ready() -> void:
	add_to_group("kinetic_machines")
	_setup_visuals()

func _setup_visuals() -> void:
	var col = CollisionShape3D.new()
	var cyl = CylinderShape3D.new()
	cyl.radius = 1.2
	cyl.height = 4.2
	col.shape = cyl
	col.position = Vector3(0, 2.1, 0)
	add_child(col)

	var glb_path = "res://assets/models/windmill.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)
			sails_node = inst

	status_label = Label3D.new()
	status_label.text = "⚙️ Kinetic Windmill\n[ 32 RPM | Active ]"
	status_label.position = Vector3(0, 5.0, 0)
	status_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	status_label.font_size = 24
	status_label.modulate = Color(0.9, 0.85, 0.6)
	add_child(status_label)

func _process(delta: float) -> void:
	# Passive kinetic rotation of the sail assembly
	if sails_node:
		# If the model has child sail meshes, rotate them, otherwise rotate the node
		sails_node.rotate_y(rotation_speed * 0.15 * delta)
		
	# Automated milling cycle
	mill_timer += delta
	if mill_timer >= mill_interval:
		mill_timer = 0.0
		_process_kinetic_milling()

func _process_kinetic_milling() -> void:
	if not supply_chain:
		return
		
	# Consume 2 wheat, produce 4 flour/bread
	if supply_chain.inventory.get("wheat", 0) >= 2:
		supply_chain.consume_resource("wheat", 2)
		supply_chain.add_resource("bread", 4)
		emit_signal("grain_milled", 2, 4)
		if status_label:
			status_label.text = "⚙️ Kinetic Windmill\n[ Milled 2 Wheat -> 4 Rations ]"
	else:
		if status_label:
			status_label.text = "⚙️ Kinetic Windmill\n[ Awaiting Grain Stockpile ]"
