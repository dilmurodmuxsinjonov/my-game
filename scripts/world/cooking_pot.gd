class_name CookingPot
extends StaticBody3D

## Farmer's Delight Hearth Cauldron & Cooking Pot.
## Simmers multi-ingredient hearty feudal meals (meat + grains + vegetables/herbs)
## providing massive nutrition, health regeneration, and long-lasting winter warmth buffs.

signal meal_cooked(meal_name: String)

var prompt_label: Label3D
var fire_light: OmniLight3D

func _ready() -> void:
	add_to_group("workstations")
	add_to_group("cooking_pots")
	_setup_visuals()

func _setup_visuals() -> void:
	var col = CollisionShape3D.new()
	var cyl = CylinderShape3D.new()
	cyl.radius = 0.45
	cyl.height = 0.9
	col.shape = cyl
	col.position = Vector3(0, 0.45, 0)
	add_child(col)

	var glb_path = "res://assets/models/cooking_pot.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)

	# Simmering Hearth Fire Light
	fire_light = OmniLight3D.new()
	fire_light.light_color = Color(1.0, 0.45, 0.12)
	fire_light.light_energy = 2.2
	fire_light.omni_range = 4.5
	fire_light.position = Vector3(0, 0.25, 0)
	add_child(fire_light)

	prompt_label = Label3D.new()
	prompt_label.text = "[E] Simmer Hearty Stews"
	prompt_label.position = Vector3(0, 1.1, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 20
	prompt_label.modulate = Color(1.0, 0.85, 0.3)
	prompt_label.visible = false
	add_child(prompt_label)

func set_prompt_visible(is_vis: bool) -> void:
	if prompt_label:
		prompt_label.visible = is_vis
