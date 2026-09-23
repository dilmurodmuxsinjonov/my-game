class_name Torch
extends Node3D

## 3D Torch Light Source.
## Emits warm dynamic illumination into caves, houses, and night camps with natural flame flickering.

var light: OmniLight3D
var stick_mesh: MeshInstance3D
var flame_mesh: MeshInstance3D

var base_energy: float = 1.8
var flicker_speed: float = 12.0

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	# 1. Wooden handle
	stick_mesh = MeshInstance3D.new()
	var cyl = CylinderMesh.new()
	cyl.top_radius = 0.04
	cyl.bottom_radius = 0.03
	cyl.height = 0.5
	stick_mesh.mesh = cyl
	stick_mesh.position = Vector3(0, 0.25, 0)
	
	var mat_wood = StandardMaterial3D.new()
	mat_wood.albedo_color = Color(0.35, 0.22, 0.12)
	mat_wood.roughness = 0.9
	stick_mesh.material_override = mat_wood
	add_child(stick_mesh)
	
	# 2. Flame head
	flame_mesh = MeshInstance3D.new()
	var cone = CylinderMesh.new()
	cone.top_radius = 0.01
	cone.bottom_radius = 0.06
	cone.height = 0.15
	flame_mesh.mesh = cone
	flame_mesh.position = Vector3(0, 0.55, 0)
	
	var mat_flame = StandardMaterial3D.new()
	mat_flame.albedo_color = Color(1.0, 0.6, 0.1)
	mat_flame.emission_enabled = true
	mat_flame.emission = Color(1.0, 0.5, 0.1)
	mat_flame.emission_energy_multiplier = 3.0
	flame_mesh.material_override = mat_flame
	add_child(flame_mesh)
	
	# 3. Dynamic OmniLight3D
	light = OmniLight3D.new()
	light.light_color = Color(1.0, 0.72, 0.32)
	light.light_energy = base_energy
	light.omni_range = 10.0
	light.shadow_enabled = true
	light.position = Vector3(0, 0.6, 0)
	add_child(light)

func _process(delta: float) -> void:
	if light:
		var time = Time.get_ticks_msec() * 0.001
		var flicker = sin(time * flicker_speed) * 0.15 + cos(time * flicker_speed * 1.7) * 0.1
		light.light_energy = base_energy + flicker
