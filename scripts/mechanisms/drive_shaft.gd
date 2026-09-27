# scripts/mechanisms/drive_shaft.gd
# Voxel Lord: Feudal Realm - Milestone 32: Linear Drive Shaft Power Transmission
# 1-meter cylindrical cast-iron axle transmitting rotational RPM along X, Y, or Z.

class_name DriveShaft
extends Node3D

signal shaft_overstressed(pos: Vector3i)

const MAX_UNSUPPORTED_LENGTH: int = 16

@export var transmission_axis: Vector3i = Vector3i(1, 0, 0) # Primary rotation axis
@export var is_encased: bool = false # Encased in stone/timber casing for floor/wall conduits

var grid_position: Vector3i = Vector3i.ZERO
var current_rpm: float = 0.0
var visual_shaft: Node3D = null

func _init(p_grid_pos: Vector3i = Vector3i.ZERO, p_axis: Vector3i = Vector3i(1, 0, 0)) -> void:
	grid_position = p_grid_pos
	transmission_axis = p_axis.abs()

func set_network_state(p_rpm: float) -> void:
	current_rpm = p_rpm

func update_visual_rotation(delta: float) -> void:
	if visual_shaft and abs(current_rpm) > 0.01:
		var rad_per_sec = deg_to_rad(current_rpm * 6.0) * delta
		if transmission_axis == Vector3i(1, 0, 0):
			visual_shaft.rotate_x(rad_per_sec)
		elif transmission_axis == Vector3i(0, 1, 0):
			visual_shaft.rotate_y(rad_per_sec)
		elif transmission_axis == Vector3i(0, 0, 1):
			visual_shaft.rotate_z(rad_per_sec)

func get_node_descriptor() -> Dictionary:
	return {
		"type": KineticNetworkManager.NodeType.TRANSMISSION,
		"axis": transmission_axis,
		"is_clutch": false,
		"is_gearbox": false,
		"idle_load_su": 0.0,
		"is_encased": is_encased
	}
