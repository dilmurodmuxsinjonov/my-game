class_name CuttingBoard
extends StaticBody3D

## Farmer's Delight Culinary Cutting Board.
## Allows the Lord or kitchen staff to chop, mince, and dice whole ingredients
## into culinary components for gourmet Cooking Pot stews and pies.

signal item_sliced(source_item: String, sliced_item: String, count: int)

var supply_chain: SupplyChain = null
var status_label: Label3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	add_to_group("kitchen_stations")
	_setup_visuals()

func _setup_visuals() -> void:
	var col = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(0.8, 0.3, 0.6)
	col.shape = box
	col.position = Vector3(0, 0.15, 0)
	add_child(col)

	var glb_path = "res://assets/models/cutting_board.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)

	status_label = Label3D.new()
	status_label.text = "🔪 Butcher's Cutting Board\n[ Ready to Slice ]"
	status_label.position = Vector3(0, 0.6, 0)
	status_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	status_label.font_size = 18
	status_label.modulate = Color(0.9, 0.85, 0.7)
	add_child(status_label)

func slice_ingredient(ingredient_name: String) -> bool:
	if not supply_chain:
		return false
		
	var sliced_name = ""
	match ingredient_name:
		"cabbage":
			sliced_name = "sliced_cabbage"
		"meat":
			sliced_name = "minced_beef"
		"onion":
			sliced_name = "diced_onion"
		_:
			return false

	if supply_chain.consume_resource(ingredient_name, 1):
		supply_chain.add_resource(sliced_name, 2)
		emit_signal("item_sliced", ingredient_name, sliced_name, 2)
		if status_label:
			status_label.text = "🔪 Sliced 1 %s -> 2 %s!" % [ingredient_name.capitalize(), sliced_name.capitalize()]
			status_label.modulate = Color(0.3, 1.0, 0.5)
		return true
	return false
