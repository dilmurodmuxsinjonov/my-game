class_name Chute
extends StaticBody3D

## Create-style Gravity Drop Chute & Hopper Funnel.
## Passive logistics duct powered strictly by gravity (0 Stress Units required).
## Funnels bulk resources (wheat from granary into millstone, crushed iron into bloomery,
## or flour into bakery crates) vertically downward at a constant flow rate of 4.0 items/sec.

signal item_dropped(item_name: String, count: int)

@export var flow_rate: float = 4.0 # Items per second

var supply_chain: SupplyChain = null
var current_buffer: Array[Dictionary] = []
var drop_timer: float = 0.0

var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(0.9, 1.8, 0.9)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.9, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/chute.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	prompt_label = Label3D.new()
	prompt_label.text = "🔻 Gravity Chute (Flow: 4/s)\n[E] Insert Resources"
	prompt_label.position = Vector3(0, 2.0, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 20
	prompt_label.modulate = Color(0.85, 0.7, 0.3)
	add_child(prompt_label)

func feed_item(item_name: String, count: int = 1) -> bool:
	current_buffer.append({"name": item_name, "count": count})
	_update_prompt()
	return true

func _process(delta: float) -> void:
	if current_buffer.is_empty():
		return

	drop_timer += delta
	var interval = 1.0 / flow_rate
	if drop_timer >= interval:
		drop_timer = 0.0
		var entry = current_buffer[0]
		entry["count"] -= 1
		emit_signal("item_dropped", entry["name"], 1)
		
		# Transfer to world below or supply chain
		if supply_chain:
			supply_chain.add_resource(entry["name"], 1)

		if entry["count"] <= 0:
			current_buffer.remove_at(0)
		_update_prompt()

func _update_prompt() -> void:
	if not prompt_label:
		return
	if current_buffer.is_empty():
		prompt_label.text = "🔻 Gravity Chute (Idle)\nReady for Vertical Drop"
		prompt_label.modulate = Color(0.85, 0.7, 0.3)
	else:
		var total = 0
		for item in current_buffer:
			total += item["count"]
		prompt_label.text = "🔻 Gravity Chute (Dropping: %d items)\nSpeed: %.1f items/s" % [total, flow_rate]
		prompt_label.modulate = Color(0.3, 0.95, 0.6)

# --- Static Simulation & Balance Calculations ---

static func calculate_gravity_flow_rate(stack_height: int) -> float:
	## Flow rate scales slightly with vertical gravity head pressure:
	## Base 4.0 items/sec + 0.5 per block of fall height
	return 4.0 + (float(stack_height) * 0.5)
