class_name CompostBin
extends StaticBody3D

## Farmer's Delight Organic Compost Bin.
## Converts agricultural waste, grass clippings, spoiled food, and leaves into
## Rich Compost Fertilizer, doubling farmland crop growth speed and preventing cold wilt.

signal compost_produced(amount: int)

@export var decomposition_time: float = 6.0 # Seconds per decomposition batch
@export var organic_waste_required: int = 4 # 4 organic items -> 1 compost

var supply_chain: SupplyChain = null
var current_organic_items: int = 0
var decompose_timer: float = 0.0
var status_label: Label3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	add_to_group("agricultural_stations")
	_setup_visuals()

func _setup_visuals() -> void:
	var col = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.0, 1.0, 1.0)
	col.shape = box
	col.position = Vector3(0, 0.5, 0)
	add_child(col)

	var glb_path = "res://assets/models/compost_bin.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)

	status_label = Label3D.new()
	status_label.text = "🌱 Compost Bin\n[ Waste: 0 / 4 ]"
	status_label.position = Vector3(0, 1.3, 0)
	status_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	status_label.font_size = 20
	status_label.modulate = Color(0.4, 0.8, 0.3)
	add_child(status_label)

func _process(delta: float) -> void:
	if current_organic_items >= organic_waste_required:
		decompose_timer += delta
		var progress = int((decompose_timer / decomposition_time) * 100.0)
		if status_label:
			status_label.text = "🌱 Fermenting Compost...\n[ %d%% ]" % progress
			status_label.modulate = Color(0.9, 0.75, 0.3)
			
		if decompose_timer >= decomposition_time:
			decompose_timer = 0.0
			current_organic_items -= organic_waste_required
			_complete_compost()
	else:
		if status_label:
			status_label.text = "🌱 Compost Bin\n[ Organic Waste: %d / %d ]" % [current_organic_items, organic_waste_required]
			status_label.modulate = Color(0.4, 0.8, 0.3)

func deposit_waste(amount: int = 1) -> bool:
	current_organic_items += amount
	return true

func _complete_compost() -> void:
	if supply_chain:
		supply_chain.add_resource("compost", 1)
	emit_signal("compost_produced", 1)
	if status_label:
		status_label.text = "✨ Rich Compost Ready!"
		status_label.modulate = Color(0.3, 1.0, 0.5)
