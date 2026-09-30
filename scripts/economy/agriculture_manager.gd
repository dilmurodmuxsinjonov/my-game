class_name AgricultureManager
extends Node

## Manages feudal agriculture, soil hydration, crop growth ticks, and harvest logistics.
## Integrated with AgronomySoilManager for voxel NPK chemistry, Liebig's law of the minimum,
## 9-crop depletion/fixation, monoculture blight, and 4-year crop rotations.

signal crop_planted(pos: Vector3i, crop_type: String)
signal crop_matured(pos: Vector3i)
signal crop_harvested(pos: Vector3i, yield_data: Dictionary)

var voxel_world: VoxelWorld
var supply_chain: SupplyChain
var soil_manager: AgronomySoilManager
var monastery_research_system = null

# Position (Vector3i) -> Crop State Dictionary
# {"crop_type": "wheat", "stage": int, "progress": float, "hydrated": bool}
var active_crops: Dictionary = {}
var registered_farmlands: Dictionary = {}

const MAX_GROWTH_STAGE: int = 3
const BASE_GROWTH_DURATION: float = 18.0 # seconds to reach full maturity
const HYDRATION_RADIUS: int = 4 # blocks from water

func _init(p_world: VoxelWorld = null, p_supply: SupplyChain = null, p_soil: AgronomySoilManager = null) -> void:
	voxel_world = p_world
	supply_chain = p_supply
	if p_soil:
		soil_manager = p_soil
	else:
		soil_manager = AgronomySoilManager.new()

func _ready() -> void:
	if not soil_manager:
		soil_manager = get_node_or_null("AgronomySoilManager")
	if not soil_manager:
		soil_manager = AgronomySoilManager.new()
		soil_manager.name = "AgronomySoilManager"
		add_child(soil_manager)

func _process(delta: float) -> void:
	_tick_crop_growth(delta)

func register_farmland(pos: Vector3i) -> void:
	var is_hydrated = _check_soil_hydration(pos)
	registered_farmlands[pos] = {"hydrated": is_hydrated}
	if soil_manager:
		soil_manager.register_farmland(pos)

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
		"hydrated": is_hydrated,
		"floor_pos": floor_pos
	}
	
	if soil_manager:
		soil_manager.register_farmland(floor_pos)
	
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
			
		# Modulate growth speed with Liebig's Law of the Minimum from soil
		if soil_manager:
			var floor_pos = crop.get("floor_pos", pos + Vector3i.DOWN)
			var liebig_mult = soil_manager.calculate_yield_multiplier(floor_pos, crop["crop_type"])
			growth_speed *= clampf(liebig_mult, 0.20, 1.25)
			
		crop["progress"] += (delta / BASE_GROWTH_DURATION) * growth_speed
		
		# Advance growth stage
		var new_stage = clampi(int(crop["progress"] * MAX_GROWTH_STAGE), 0, MAX_GROWTH_STAGE)
		if new_stage > crop["stage"]:
			crop["stage"] = new_stage
			if crop["stage"] == MAX_GROWTH_STAGE:
				emit_signal("crop_matured", pos)

func harvest_crop(pos: Vector3i, farmer_skill: int = 1) -> Dictionary:
	if not active_crops.has(pos):
		return {"success": false}
		
	var crop = active_crops[pos]
	if crop["stage"] < MAX_GROWTH_STAGE:
		return {"success": false, "reason": "Not yet mature"}
		
	var crop_type = crop.get("crop_type", "wheat")
	var floor_pos = crop.get("floor_pos", pos + Vector3i.DOWN)
	
	var yield_qty = 3
	var is_blighted = false
	var post_fertility = 100.0
	
	if soil_manager:
		var harvest_res = soil_manager.process_harvest(floor_pos, crop_type, farmer_skill)
		yield_qty = harvest_res.get("yield", 1)
		is_blighted = harvest_res.get("blight", false)
	if monastery_research_system and monastery_research_system.has_method("get_active_blessings"):
		var blessings = monastery_research_system.get_active_blessings()
		if blessings.has("harvest_bonus") and not is_blighted:
			yield_qty = int(round(yield_qty * blessings["harvest_bonus"]))

	var yield_data = {
		crop_type: yield_qty,
		"seeds": 2 if not is_blighted else 0
	}
	
	# Reset crop or clear block
	active_crops.erase(pos)
	if voxel_world:
		voxel_world.set_block_world(pos, VoxelChunk.BlockType.AIR, true)
		
	if supply_chain and not is_blighted:
		supply_chain.add_resource(crop_type, yield_qty)
		
	emit_signal("crop_harvested", pos, yield_data)
	return {
		"success": true,
		"yield": yield_data,
		"blight": is_blighted,
		"fertility_post": post_fertility
	}

func get_mature_crops() -> Array[Vector3i]:
	var result: Array[Vector3i] = []
	for pos in active_crops.keys():
		if active_crops[pos]["stage"] >= MAX_GROWTH_STAGE:
			result.append(pos)
	return result

func advance_crop_rotation(cycle_year: int) -> void:
	if soil_manager:
		soil_manager.advance_rotation_year(cycle_year)

func apply_fertilizer(farmland_pos: Vector3i, amendment: String = "compost_barrel") -> void:
	if soil_manager:
		soil_manager.apply_amendment(farmland_pos, amendment)

func apply_fallow(farmland_pos: Vector3i, with_grazing: bool = false) -> void:
	if soil_manager:
		soil_manager.apply_fallow_regeneration(farmland_pos, with_grazing)
