# scripts/mechanisms/industrial_trip_hammer.gd
# Voxel Lord: Feudal Realm - Milestone 35: Heavy Water-Powered Industrial Tilt-Hammer (Helve Hammer)
# 800kg counterbalanced oak helve hammer with 3-cam rotating shaft automating heavy forging and bloom consolidation.

class_name IndustrialTripHammer
extends Node3D

signal strike_delivered(strike_force: float)
signal workpiece_completed(output_item: String, count: int)

const KINETIC_LOAD_SU: float = 64.0
const MIN_OPERATING_RPM: float = 16.0
const BASE_STRIKE_FORCE: float = 450.0  # Joules of kinetic blow per strike
const CAM_COUNT: int = 3

@export var is_operating: bool = false
@export var input_rpm: float = 0.0

var current_item: String = ""
var strikes_accumulated: int = 0
var strikes_required: int = 0
var strike_timer: float = 0.0
var output_queue: Array[Dictionary] = []

func _init() -> void:
	is_operating = false
	input_rpm = 0.0
	current_item = ""
	strikes_accumulated = 0
	strikes_required = 0
	strike_timer = 0.0
	output_queue.clear()

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	is_operating = abs(input_rpm) >= MIN_OPERATING_RPM

func get_kinetic_load() -> float:
	return KINETIC_LOAD_SU if is_operating else 0.0

func feed_item(item_id: String) -> bool:
	if current_item != "":
		return false # Anvil occupied
		
	if item_id == "iron_bloom":
		current_item = item_id
		strikes_accumulated = 0
		strikes_required = 4 # 4 strikes consolidates spongy bloom into refined billet
		return true
	elif item_id == "wrought_iron_billet":
		current_item = item_id
		strikes_accumulated = 0
		strikes_required = 3 # 3 strikes draws billet into 2 armor plates
		return true
	elif item_id == "high_carbon_steel":
		current_item = item_id
		strikes_accumulated = 0
		strikes_required = 5 # 5 strikes creates tempered sword blank
		return true
		
	return false

func get_strike_interval() -> float:
	if not is_operating or abs(input_rpm) <= 0.0:
		return 999.0
	var rps: float = abs(input_rpm) / 60.0
	var strikes_per_sec: float = rps * float(CAM_COUNT)
	return 1.0 / max(0.1, strikes_per_sec)

func process_tick(delta: float) -> void:
	if not is_operating or current_item == "":
		return

	var interval: float = get_strike_interval()
	strike_timer += delta

	while strike_timer >= interval and current_item != "":
		strike_timer -= interval
		strikes_accumulated += 1
		strike_delivered.emit(BASE_STRIKE_FORCE)

		if strikes_accumulated >= strikes_required:
			_complete_workpiece()

func _complete_workpiece() -> void:
	var finished_item: String = ""
	var count: int = 1

	if current_item == "iron_bloom":
		finished_item = "wrought_iron_billet"
		count = 1
	elif current_item == "wrought_iron_billet":
		finished_item = "iron_plate"
		count = 2
	elif current_item == "high_carbon_steel":
		finished_item = "steel_sword_blank"
		count = 1

	output_queue.append({"item": finished_item, "count": count})
	workpiece_completed.emit(finished_item, count)

	current_item = ""
	strikes_accumulated = 0
	strikes_required = 0

func collect_output() -> Array[Dictionary]:
	var discharged: Array[Dictionary] = output_queue.duplicate(true)
	output_queue.clear()
	return discharged
