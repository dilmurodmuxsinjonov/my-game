# scripts/mechanisms/mechanical_clutch.gd
# Voxel Lord: Feudal Realm - Milestone 32: Mechanical Friction Clutch & Circuit Breaker
# Dual cast-iron friction plates disengaging downstream kinetic machines via lever.

class_name MechanicalClutch
extends Node3D

signal clutch_state_changed(is_engaged: bool)

@export var transmission_axis: Vector3i = Vector3i(1, 0, 0)
@export var is_engaged: bool = true

var grid_position: Vector3i = Vector3i.ZERO
var input_rpm: float = 0.0

func _init(p_grid_pos: Vector3i = Vector3i.ZERO, p_axis: Vector3i = Vector3i(1, 0, 0), p_start_engaged: bool = true) -> void:
	grid_position = p_grid_pos
	transmission_axis = p_axis.abs()
	is_engaged = p_start_engaged

func toggle_clutch() -> bool:
	is_engaged = not is_engaged
	clutch_state_changed.emit(is_engaged)
	return is_engaged

func set_engaged(engaged: bool) -> void:
	if is_engaged != engaged:
		is_engaged = engaged
		clutch_state_changed.emit(is_engaged)

func get_output_rpm() -> float:
	return input_rpm if is_engaged else 0.0

func get_node_descriptor() -> Dictionary:
	return {
		"type": KineticNetworkManager.NodeType.TRANSMISSION,
		"axis": transmission_axis,
		"is_clutch": true,
		"is_engaged": is_engaged,
		"is_gearbox": false,
		"idle_load_su": 2.0
	}
