# scripts/mechanisms/bevel_gearbox.gd
# Voxel Lord: Feudal Realm - Milestone 32: 90-Degree Bevel Gearbox & Rotation Inverter
# Miter bevel gears redirecting rotational power orthogonal to input axis.

class_name BevelGearbox
extends Node3D

signal direction_inverted(new_inverted_state: bool)

@export var is_inverted: bool = false
@export var gear_ratio: float = 1.0 # 1.0 = direct miter (1:1), 2.0 = speed doubler
@export var idle_friction_su: float = 4.0

var grid_position: Vector3i = Vector3i.ZERO
var current_input_rpm: float = 0.0

func _init(p_grid_pos: Vector3i = Vector3i.ZERO, p_inverted: bool = false) -> void:
	grid_position = p_grid_pos
	is_inverted = p_inverted

func toggle_inversion() -> bool:
	is_inverted = not is_inverted
	direction_inverted.emit(is_inverted)
	return is_inverted

func get_output_rpm(input_rpm: float) -> float:
	var out = input_rpm * gear_ratio
	if is_inverted:
		out = -out
	return out

func get_node_descriptor() -> Dictionary:
	return {
		"type": KineticNetworkManager.NodeType.TRANSMISSION,
		"axis": Vector3i(1, 0, 0), # Gearbox can bridge any axis
		"is_clutch": false,
		"is_gearbox": true,
		"gear_ratio": gear_ratio,
		"inverted": is_inverted,
		"idle_load_su": idle_friction_su
	}
