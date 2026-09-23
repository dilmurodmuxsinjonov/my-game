class_name AgricultureManager
extends Node

## Manages feudal agriculture, soil hydration, crop growth ticks, and harvest logistics.

signal crop_planted(pos: Vector3i, crop_type: String)
signal crop_matured(pos: Vector3i)
signal crop_harvested(pos: Vector3i, yield_data: Dictionary)

var voxel_world: VoxelWorld
var supply_chain: SupplyChain

# Position (Vector3i) -> Crop State Dictionary
# {"crop_type": "wheat", "stage": int, "progress": float, "hydrated": bool}
var active_crops: Dictionary = {}
var registered_farmlands: Dictionary = {}

const MAX_GROWTH_STAGE: int = 3
const BASE_GROWTH_DURATION: float = 18.0 # seconds to reach full maturity
const HYDRATION_RADIUS: int = 4 # blocks from water

func _init(p_world: VoxelWorld = null, p_supply: SupplyChain = null) -> void:
	voxel_world = p_world
	supply_chain = p_supply

func _process(delta: float) -> void:
	_tick_crop_growth(delta)

func register_farmland(pos: Vector3i) -> void:
	var is_hydrated = _check_soil_hydration(pos)
	registered_farmlands[pos] = {"hydrated": is_hydrated}

func plant_crop(pos: Vector3i, crop_type: String = "wheat") -> bool:
	if not voxel_world:
		return false
		
	# Check if block below is farmland
	var floor_pos = pos + Vector3i.DOWN
	var floor_type = voxel_world.get_block_world(floor_pos)
	if floor_type != VoxelChunk.BlockType.FARMLAND:
		return false
		
	# Place wheat crop block in voxel world
	voxel_world.set_block_world(pos, VoxelChunk.BlockType.WHEAT_CROP, true)
	
	var is_hydrated = _check_soil_hydration(floor_pos)
	active_crops[pos] = {
		"crop_type": crop_type,
		"stage": 0,
		"progress": 0.0,
		"hydrated": is_hydrated
	}
	
	emit_signal("crop_planted", pos, crop_type)
	return true

func _check_soil_hydration(farmland_pos: Vector3i) -> bool:
	if not voxel_world:
		return false
	# Check adjacent voxels within HYDRATION_RADIUS for water
	for dx in range(-HYDRATION_RADIUS, HYDRATION_RADIUS + 1):
		for dz in range(-HYDRATION_RADIUS, HYDRATION_RADIUS + 1):
			for dy in range(-1, 2):
				var check_pos = farmland_pos + Vector3i(dx, dy, dz)
				if voxel_world.get_block_world(check_pos) == VoxelChunk.BlockType.WATER:
					return true
	return false

func _tick_crop_growth(delta: float) -> void:
	for pos in active_crops.keys():
		var crop = active_crops[pos]
		if crop["stage"] >= MAX_GROWTH_STAGE:
			continue
			
		var growth_speed = 1.0
		if crop["hydrated"]:
			growth_speed = 2.2 # Hydrated crops grow 2.2x faster
			
		crop["progress"] += (delta / BASE_GROWTH_DURATION) * growth_speed
		
		# Advance growth stage
		var new_stage = clampi(int(crop["progress"] * MAX_GROWTH_STAGE), 0, MAX_GROWTH_STAGE)
		if new_stage > crop["stage"]:
			crop["stage"] = new_stage
			if crop["stage"] == MAX_GROWTH_STAGE:
				emit_signal("crop_matured", pos)

func harvest_crop(pos: Vector3i) -> Dictionary:
	if not active_crops.has(pos):
		return {"success": false}
		
	var crop = active_crops[pos]
	if crop["stage"] < MAX_GROWTH_STAGE:
		return {"success": false, "reason": "Not yet mature"}
		
	# Harvest yield
	var yield_data = {
		"wheat": 3,
		"seeds": 2
	}
	
	# Reset crop or clear block
	active_crops.erase(pos)
	if voxel_world:
		voxel_world.set_block_world(pos, VoxelChunk.BlockType.AIR, true)
		
	if supply_chain:
		supply_chain.add_resource("wheat", yield_data["wheat"])
		
	emit_signal("crop_harvested", pos, yield_data)
	return {"success": true, "yield": yield_data}

func get_mature_crops() -> Array[Vector3i]:
	var result: Array[Vector3i] = []
	for pos in active_crops.keys():
		if active_crops[pos]["stage"] >= MAX_GROWTH_STAGE:
			result.append(pos)
	return result
