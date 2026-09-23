class_name FoodPreservationManager
extends RefCounted

## TerraFirmaCraft-Style Food Preservation & Spoilage Simulation.
## Manages realistic food degradation timers, salting with rock salt,
## smokehouse rack curing, and underground cold cellar thermal decay mitigation.

# Base shelf life in game hours (1 game day = 24 game hours)
const BASE_SHELF_LIFE_HOURS: Dictionary = {
	"fresh_meat": 72.0,      # 3 days
	"ration_bread": 144.0,   # 6 days
	"vegetable_broth": 96.0, # 4 days
	"hearty_stew": 120.0,    # 5 days
	"smoked_meat": 360.0,    # 15 days (5x preservation via smoke rack)
	"cured_meat": 576.0      # 24 days (8x preservation via rock salt)
}

# Thermal Cellar Decay Multiplier (subterranean stone vault)
const CELLAR_DECAY_RATE: float = 0.25 # 75% spoilage reduction (4x shelf life)
const CELLAR_MAX_ELEVATION: int = 22  # Must be 4+ blocks below surface terrain (surface ~ 25m)

static func get_shelf_life(food_type: String, is_cellar: bool = false) -> float:
	var base_hours = BASE_SHELF_LIFE_HOURS.get(food_type, 120.0)
	if is_cellar:
		return base_hours / CELLAR_DECAY_RATE
	return base_hours

static func is_cold_cellar(storage_pos: Vector3i, voxel_world: VoxelWorld = null) -> bool:
	if storage_pos.y > CELLAR_MAX_ELEVATION:
		return false
		
	if voxel_world:
		# Verify overhead rock roof
		var stone_count = 0
		for dy in range(1, 5):
			var b = voxel_world.get_block_world(storage_pos + Vector3i(0, dy, 0))
			if b == VoxelChunk.BlockType.STONE or b == VoxelChunk.BlockType.STONE_BRICKS:
				stone_count += 1
		return stone_count >= 2
	return true

static func simulate_spoilage_cycle(food_inventory: Dictionary, elapsed_hours: float, is_cellar: bool = false) -> Dictionary:
	var report = {
		"spoiled": {},
		"remaining": {},
		"compost_produced": 0
	}
	
	var decay_mult = CELLAR_DECAY_RATE if is_cellar else 1.0

	for item in food_inventory.keys():
		var count = food_inventory[item]
		if count <= 0:
			continue
			
		var max_hours = BASE_SHELF_LIFE_HOURS.get(item, 120.0)
		# Spoilage probability per elapsed hour window
		var hourly_spoil_rate = (1.0 / max_hours) * decay_mult
		var total_loss_fraction = clampf(hourly_spoil_rate * elapsed_hours, 0.0, 1.0)
		var spoiled_amount = int(floor(count * total_loss_fraction))
		
		# If elapsed time exceeds max shelf life completely, everything spoils
		if elapsed_hours * decay_mult >= max_hours:
			spoiled_amount = count
			
		var kept_amount = count - spoiled_amount
		if spoiled_amount > 0:
			report["spoiled"][item] = spoiled_amount
			report["compost_produced"] += spoiled_amount
		report["remaining"][item] = kept_amount

	return report
