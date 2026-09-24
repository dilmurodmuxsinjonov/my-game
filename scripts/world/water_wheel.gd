class_name WaterWheel
extends StaticBody3D

## Create-Style Kinetic Water Wheel.
## Placed along riverbeds or water flumes to generate rotational kinetic force (24 RPM, 256 Stress Units).
## Directly powers adjacent and nearby mechanical machines (Millstone, Trip Hammer).

signal kinetic_power_changed(capacity: float, rpm: float)

@export var base_stress_capacity: float = 256.0 # Stress Units (SU)
@export var base_rpm: float = 24.0 # Rotations Per Minute
@export var power_radius: float = 8.0 # Reach of rotational drive shaft network

var is_water_flowing: bool = true
var current_stress_load: float = 0.0
var wheel_node: Node3D = null
var status_label: Label3D = null

func _ready() -> void:
	add_to_group("kinetic_sources")
	add_to_group("interactive_workstations")
	_setup_visuals()

func _setup_visuals() -> void:
	var col = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(2.2, 4.2, 3.8)
	col.shape = box
	col.position = Vector3(0, 2.1, 0)
	add_child(col)

	var glb_path = "res://assets/models/water_wheel.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)
			wheel_node = inst

	status_label = Label3D.new()
	status_label.text = "🌊 Kinetic Water Wheel\n[ 24 RPM | 256 SU Available ]"
	status_label.position = Vector3(0, 4.4, 0)
	status_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	status_label.font_size = 22
	status_label.modulate = Color(0.4, 0.8, 1.0)
	add_child(status_label)

func _process(delta: float) -> void:
	if is_water_flowing:
		# Rotate wheel continuously along local X axis (paddle rotation)
		if wheel_node:
			wheel_node.rotate_x(deg_to_rad(base_rpm * 6.0) * delta)
		
		var avail = get_available_capacity()
		if status_label:
			status_label.text = "🌊 Kinetic Water Wheel\n[ %.0f RPM | Load: %.0f / %.0f SU ]" % [base_rpm, current_stress_load, base_stress_capacity]
			status_label.modulate = Color(0.4, 0.8, 1.0) if current_stress_load <= base_stress_capacity else Color(1.0, 0.3, 0.3)

func get_available_capacity() -> float:
	if not is_water_flowing:
		return 0.0
	return maxf(0.0, base_stress_capacity - current_stress_load)

func request_power(stress_cost: float) -> bool:
	if not is_water_flowing:
		return false
	if current_stress_load + stress_cost <= base_stress_capacity:
		current_stress_load += stress_cost
		emit_signal("kinetic_power_changed", get_available_capacity(), base_rpm)
		return true
	return false

func release_power(stress_cost: float) -> void:
	current_stress_load = maxf(0.0, current_stress_load - stress_cost)
	emit_signal("kinetic_power_changed", get_available_capacity(), base_rpm)

func set_water_flow(flowing: bool) -> void:
	is_water_flowing = flowing
	if not is_water_flowing and status_label:
		status_label.text = "⚠️ Water Wheel [ Stalled: No Flow ]"
		status_label.modulate = Color(0.8, 0.4, 0.2)
