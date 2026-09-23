class_name Workstation
extends StaticBody3D

## Interactive 3D Workstation in the feudal realm.
## Renders Blender-generated .glb models and handles player interaction (Workbench, Campfire, Crate, Furnace).

signal player_interacted(station: Workstation, player: Node3D)

enum StationType {
	WORKBENCH = 0,
	CAMPFIRE = 1,
	CRATE = 2,
	FURNACE = 3
}

@export var station_type: StationType = StationType.WORKBENCH
@export var station_name: String = "Carpentry Workbench"

var model_node: Node3D
var collision_box: CollisionShape3D
var prompt_label: Label3D
var omni_light: OmniLight3D

func _init(p_type: StationType = StationType.WORKBENCH) -> void:
	station_type = p_type

func _ready() -> void:
	_setup_station()

func _setup_station() -> void:
	# 1. Collision shape
	collision_box = CollisionShape3D.new()
	var box_shape = BoxShape3D.new()
	
	var glb_path = ""
	match station_type:
		StationType.WORKBENCH:
			glb_path = "res://assets/models/workbench.glb"
			station_name = "Carpentry Workbench"
			box_shape.size = Vector3(1.4, 1.0, 1.0)
			collision_box.position = Vector3(0, 0.5, 0)
			
		StationType.CAMPFIRE:
			glb_path = "res://assets/models/campfire.glb"
			station_name = "Settlement Campfire"
			box_shape.size = Vector3(1.2, 0.6, 1.2)
			collision_box.position = Vector3(0, 0.3, 0)
			
			# Add warm glowing firelight
			omni_light = OmniLight3D.new()
			omni_light.light_color = Color(1.0, 0.6, 0.2)
			omni_light.light_energy = 2.5
			omni_light.omni_range = 8.0
			omni_light.shadow_enabled = true
			omni_light.position = Vector3(0, 0.5, 0)
			add_child(omni_light)
			
		StationType.CRATE:
			glb_path = "res://assets/models/crate.glb"
			station_name = "Timber Stockpile Crate"
			box_shape.size = Vector3(1.0, 1.0, 1.0)
			collision_box.position = Vector3(0, 0.5, 0)
			
		StationType.FURNACE:
			glb_path = "res://assets/models/furnace.glb"
			station_name = "Stone Bloomery Furnace"
			box_shape.size = Vector3(1.2, 1.4, 1.2)
			collision_box.position = Vector3(0, 0.7, 0)
			
			omni_light = OmniLight3D.new()
			omni_light.light_color = Color(1.0, 0.45, 0.1)
			omni_light.light_energy = 3.2
			omni_light.omni_range = 7.0
			omni_light.shadow_enabled = true
			omni_light.position = Vector3(0, 0.6, 0)
			add_child(omni_light)

	collision_box.shape = box_shape
	add_child(collision_box)

	# 2. Instantiate GLB Model
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_node = scene_res.instantiate()
			add_child(model_node)
	else:
		# Fallback primitive mesh
		var mi = MeshInstance3D.new()
		var box = BoxMesh.new()
		box.size = box_shape.size
		mi.mesh = box
		mi.position = collision_box.position
		add_child(mi)

	# 3. 3D Interaction Prompt
	prompt_label = Label3D.new()
	prompt_label.text = "[E] Use %s" % station_name
	prompt_label.position = Vector3(0, box_shape.size.y + 0.4, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 22
	prompt_label.modulate = Color(1.0, 0.9, 0.4)
	prompt_label.visible = false
	add_child(prompt_label)

func set_prompt_visible(is_visible: bool) -> void:
	if prompt_label:
		prompt_label.visible = is_visible

func interact(player: Node3D) -> void:
	emit_signal("player_interacted", self, player)
