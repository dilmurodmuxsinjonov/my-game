# scripts/mechanisms/drydock_slipway.gd
class_name DrydockSlipway
extends Node3D

# Medieval Shipbuilding Slipway Cradle with Scaffolding & Greased Skids
# Inspired by Anno 1404, Port Royale, and Vintage Story
# Enables construction and launching of large ocean-going merchant and military vessels.

signal construction_phase_completed(phase_name: String)
signal vessel_ready_for_launch(ship_type: String)
signal vessel_launched(ship_type: String)
signal materials_depleted(missing_item: String)

enum Stage {
	IDLE,
	KEEL_LAYING,
	RIB_FRAMING,
	HULL_PLANKING_AND_CAULKING,
	RIGGING_AND_OUTFITTING,
	READY_FOR_LAUNCH,
	LAUNCHED
}

@export var slipway_id: String = "slipway_01"
@export var active_ship_type: String = "fluyt_cargo_ship"
@export var current_stage: Stage = Stage.IDLE
@export var stage_progress: float = 0.0 # 0.0 to 1.0
@export var assigned_shipwrights: int = 0 # 0 to 6 artisans
@export var max_shipwrights: int = 6

var material_inventory: Dictionary = {}
var total_build_time_s: float = 0.0

# Material requirements per construction phase
const STAGE_REQUIREMENTS = {
	Stage.KEEL_LAYING: {
		"materials": {"oak_log": 8, "iron_plate": 4},
		"base_work_s": 60.0,
		"name": "Keel Laying"
	},
	Stage.RIB_FRAMING: {
		"materials": {"oak_log": 16, "iron_plate": 8},
		"base_work_s": 90.0,
		"name": "Rib Framing"
	},
	Stage.HULL_PLANKING_AND_CAULKING: {
		"materials": {"oak_log": 24, "pitch_bucket": 6, "iron_sheet": 12},
		"base_work_s": 120.0,
		"name": "Hull Planking & Pitch Caulking"
	},
	Stage.RIGGING_AND_OUTFITTING: {
		"materials": {"spruce_log": 8, "fine_fabric": 12, "hemp_rope": 6},
		"base_work_s": 90.0,
		"name": "Rigging, Spars & Sail Outfitting"
	}
}

func _init(id: String = "slipway_01"):
	slipway_id = id
	material_inventory = {}

func deposit_material(item_id: String, count: int) -> int:
	if count <= 0:
		return 0
	material_inventory[item_id] = material_inventory.get(item_id, 0) + count
	return count

func assign_shipwrights(count: int) -> void:
	assigned_shipwrights = clamp(count, 0, max_shipwrights)

func start_shipbuilding(ship_type: String = "fluyt_cargo_ship") -> bool:
	if current_stage != Stage.IDLE and current_stage != Stage.LAUNCHED:
		return false
	active_ship_type = ship_type
	current_stage = Stage.KEEL_LAYING
	stage_progress = 0.0
	total_build_time_s = 0.0
	return true

func has_phase_materials(stage: Stage) -> bool:
	if not STAGE_REQUIREMENTS.has(stage):
		return true
	var reqs = STAGE_REQUIREMENTS[stage]["materials"]
	for mat in reqs.keys():
		if material_inventory.get(mat, 0) < reqs[mat]:
			return false
	return true

func consume_phase_materials(stage: Stage) -> bool:
	if not has_phase_materials(stage):
		return false
	var reqs = STAGE_REQUIREMENTS[stage]["materials"]
	for mat in reqs.keys():
		material_inventory[mat] -= reqs[mat]
	return true

func process_shipbuilding(delta: float) -> Dictionary:
	if current_stage == Stage.IDLE or current_stage == Stage.READY_FOR_LAUNCH or current_stage == Stage.LAUNCHED:
		return {
			"stage": current_stage,
			"progress": stage_progress,
			"assigned_shipwrights": assigned_shipwrights,
			"is_working": false
		}

	if assigned_shipwrights <= 0:
		return {
			"stage": current_stage,
			"progress": stage_progress,
			"assigned_shipwrights": 0,
			"is_working": false,
			"stall_reason": "No shipwrights assigned"
		}

	# Check material readiness for current stage
	if not has_phase_materials(current_stage) and stage_progress <= 0.001:
		var reqs = STAGE_REQUIREMENTS[current_stage]["materials"]
		var missing: String = ""
		for mat in reqs.keys():
			if material_inventory.get(mat, 0) < reqs[mat]:
				missing = mat
				break
		materials_depleted.emit(missing)
		return {
			"stage": current_stage,
			"progress": stage_progress,
			"assigned_shipwrights": assigned_shipwrights,
			"is_working": false,
			"stall_reason": "Missing materials: " + missing
		}

	# Work speed scales with artisan crew: 1 shipwright = 1.0x, each extra = +0.5x
	var crew_speed_multiplier: float = 1.0 + (float(assigned_shipwrights - 1) * 0.5)
	var stage_duration_s: float = STAGE_REQUIREMENTS[current_stage]["base_work_s"]
	var advance_step: float = (delta * crew_speed_multiplier) / stage_duration_s

	# Consume materials on stage commencement
	if stage_progress <= 0.001:
		consume_phase_materials(current_stage)

	stage_progress = min(1.0, stage_progress + advance_step)
	total_build_time_s += delta

	if stage_progress >= 1.0:
		var completed_name = STAGE_REQUIREMENTS[current_stage]["name"]
		construction_phase_completed.emit(completed_name)

		# Advance to next stage
		if current_stage == Stage.KEEL_LAYING:
			current_stage = Stage.RIB_FRAMING
			stage_progress = 0.0
		elif current_stage == Stage.RIB_FRAMING:
			current_stage = Stage.HULL_PLANKING_AND_CAULKING
			stage_progress = 0.0
		elif current_stage == Stage.HULL_PLANKING_AND_CAULKING:
			current_stage = Stage.RIGGING_AND_OUTFITTING
			stage_progress = 0.0
		elif current_stage == Stage.RIGGING_AND_OUTFITTING:
			current_stage = Stage.READY_FOR_LAUNCH
			stage_progress = 1.0
			vessel_ready_for_launch.emit(active_ship_type)

	return {
		"stage": current_stage,
		"progress": stage_progress,
		"assigned_shipwrights": assigned_shipwrights,
		"is_working": true,
		"total_build_time_s": total_build_time_s
	}

func launch_vessel() -> Dictionary:
	if current_stage != Stage.READY_FOR_LAUNCH:
		return {"success": false, "reason": "Vessel not ready for launch"}

	current_stage = Stage.LAUNCHED
	stage_progress = 1.0
	vessel_launched.emit(active_ship_type)
	return {
		"success": true,
		"ship_type": active_ship_type,
		"total_build_time_s": total_build_time_s
	}
