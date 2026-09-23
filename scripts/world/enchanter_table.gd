class_name EnchanterTable
extends StaticBody3D

## Arcane Enchanter's Table Workstation.
## Allows crafting common runes from mob drops & botanical herbs,
## and infusing equipment with ancient enchantments and legendary affixes.

var model_instance: Node3D
var collision_box: CollisionShape3D
var prompt_label: Label3D
var arcane_light: OmniLight3D

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	# Base collision
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.5, 1.2, 1.1)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.6, 0)
	add_child(collision_box)

	# Load Blender enchanter_table.glb
	var glb_path = "res://assets/models/enchanter_table.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_instance = scene_res.instantiate()
			add_child(model_instance)

	# Arcane violet light
	arcane_light = OmniLight3D.new()
	arcane_light.light_color = Color(0.75, 0.25, 1.0)
	arcane_light.light_energy = 1.6
	arcane_light.omni_range = 4.5
	arcane_light.position = Vector3(0.35, 1.1, 0)
	add_child(arcane_light)

	# Prompt billboard
	prompt_label = Label3D.new()
	prompt_label.text = "🔮 Enchanter's Arcane Table\n[E] Inscribe Runes & Enchant Gear"
	prompt_label.position = Vector3(0, 1.8, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 26
	prompt_label.modulate = Color(0.85, 0.5, 1.0)
	add_child(prompt_label)
