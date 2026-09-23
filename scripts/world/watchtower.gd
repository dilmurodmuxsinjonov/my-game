class_name Watchtower
extends StaticBody3D

## Medieval Defensive Watchtower Structure.
## Elevates archers and guards to a high vantage point (+3.5m platform).
## Grants +25% detection & engagement range and +15% kinetic ballistic damage bonus.

var model_instance: Node3D
var collision_shape: CollisionShape3D
var prompt_label: Label3D

# Guard garrisoning
var assigned_guard: Node = null
const PLATFORM_HEIGHT: float = 3.5
const RANGE_BONUS_MULT: float = 1.25
const DAMAGE_BONUS_MULT: float = 1.15

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	# Base collision shape (2.4m x 4.5m x 2.4m)
	collision_shape = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(2.4, 4.6, 2.4)
	collision_shape.shape = box
	collision_shape.position = Vector3(0, 2.3, 0)
	add_child(collision_shape)

	# Load Blender watchtower.glb
	var glb_path = "res://assets/models/watchtower.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_instance = scene_res.instantiate()
			add_child(model_instance)

	# Prompt billboard
	prompt_label = Label3D.new()
	prompt_label.text = "🏹 Defensive Watchtower\n[E] Station Archer / Guard"
	prompt_label.position = Vector3(0, 4.8, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 26
	prompt_label.modulate = Color(0.9, 0.85, 0.4)
	add_child(prompt_label)

func get_platform_position() -> Vector3:
	return global_position + Vector3(0, PLATFORM_HEIGHT, 0)
