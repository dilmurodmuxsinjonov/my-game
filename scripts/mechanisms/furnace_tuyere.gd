# scripts/mechanisms/furnace_tuyere.gd
# Voxel Lord: Feudal Realm - Milestone 35: Blast Furnace Tuyere Air Injection Assembly
# Refractory copper tuyere regulating blast furnace oxygen draft, pressure, and metal yield purity.

class_name FurnaceTuyere
extends Node3D

signal damper_changed(ratio: float)
signal pressure_changed(pressure_kpa: float)

@export var damper_ratio: float = 0.85   # 0.0 (choked) to 1.0 (wide open)
@export var blast_pressure_kpa: float = 0.0
@export var incoming_airflow: float = 0.0

func _init(p_start_damper: float = 0.85) -> void:
	damper_ratio = clamp(p_start_damper, 0.0, 1.0)
	blast_pressure_kpa = 0.0
	incoming_airflow = 0.0

func set_damper(ratio: float) -> void:
	damper_ratio = clamp(ratio, 0.0, 1.0)
	_recalculate_pressure()
	damper_changed.emit(damper_ratio)

func update_incoming_air(airflow: float) -> void:
	incoming_airflow = max(0.0, airflow)
	_recalculate_pressure()

func _recalculate_pressure() -> void:
	# Effective pressure behind nozzle aperture
	blast_pressure_kpa = incoming_airflow * damper_ratio * 12.5
	pressure_changed.emit(blast_pressure_kpa)

func get_effective_hearth_airflow() -> float:
	return incoming_airflow * damper_ratio

func calculate_metal_yield_factor() -> float:
	# Optimal stoichiometric window: 0.75 to 0.92
	if damper_ratio >= 0.75 and damper_ratio <= 0.92 and incoming_airflow > 0.1:
		return 1.25 # +25% metal yield purity bonus (reduced slag)
	elif damper_ratio > 0.92:
		return 0.90 # Over-oxidation: oxygen burns off metal
	elif damper_ratio < 0.40:
		return 0.60 # Incomplete combustion
	return 1.0
