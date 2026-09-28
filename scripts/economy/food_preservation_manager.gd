class_name FoodPreservationManager
extends RefCounted

## Medieval Food Preservation & Spoilage Simulation.
## Incorporates Arrhenius thermal reaction kinetics (Q10 = 2.0),
## relative humidity spoilage acceleration, halite rock salting,
## hardwood smokehouse curing, subterranean cold cellars, and icehouse vaults.
## Aligns with MASTER_GDD.md §§40, 41, 42 and PROJECT.md M3 interface contracts.

enum ContainerType {
	OPEN_GROUND = 0,    # 1.50x decay multiplier
	WOODEN_CHEST = 1,   # 1.00x decay multiplier
	CLAY_AMPHORA = 2,   # 0.60x decay multiplier
	STILT_GRANARY = 3,  # 0.25x decay multiplier
	COLD_CELLAR = 4,    # 0.25x decay multiplier (subterranean root cellar)
	ICEHOUSE_VAULT = 5  # 0.10x decay multiplier (cold cellar + ice blocks)
}

enum PreservationMode {
	NONE = 0,           # 1.00x
	PICKLED = 1,        # 0.14x (7.1x shelf-life)
	SMOKED = 2,         # 0.10x (10x shelf-life)
	SALTED = 3,         # 0.07x (14.3x shelf-life)
	DEHYDRATED = 4      # 0.08x (12.5x shelf-life)
}

# Base shelf life in game hours at baseline conditions (T = 15°C, RH = 50%, Chest container)
const BASE_SHELF_LIFE_HOURS: Dictionary = {
	"fresh_meat": 72.0,      # 3 days
	"food_meat_raw": 72.0,
	"ration_bread": 144.0,   # 6 days
	"food_bread": 144.0,
	"bread": 144.0,
	"vegetable_broth": 96.0, # 4 days
	"hearty_stew": 120.0,    # 5 days
	"food_fish_stew": 96.0,
	"food_roast_meat": 96.0,
	"cabbage": 168.0,        # 7 days
	"food_cabbage_raw": 168.0,
	"carrot": 240.0,         # 10 days
	"food_carrot_raw": 240.0,
	"berries": 72.0,         # 3 days
	"food_berries_fresh": 72.0,
	"smoked_meat": 360.0,    # 15 days (5x-10x preservation via smoke rack)
	"food_smoked_meat": 360.0,
	"cured_meat": 576.0,     # 24 days (8x-14x preservation via rock salt)
	"salted_meat": 576.0,
	"food_salted_meat": 576.0,
	"pickled_veg": 720.0,    # 30 days
	"food_pickled_veg": 720.0,
	"dried_fruit": 600.0,
	"food_dried_fruit": 600.0
}

# Thermal Cellar Decay Multiplier (subterranean stone vault)
const CELLAR_DECAY_RATE: float = 0.25 # 75% spoilage reduction (4x shelf life)
const ICEHOUSE_DECAY_RATE: float = 0.10 # 90% spoilage reduction (10x shelf life)
const CELLAR_MAX_ELEVATION: int = 22  # Must be 4+ blocks below surface terrain (surface ~ 25m)

const CONTAINER_MULTIPLIERS: Dictionary = {
	ContainerType.OPEN_GROUND: 1.50,
	ContainerType.WOODEN_CHEST: 1.00,
	ContainerType.CLAY_AMPHORA: 0.60,
	ContainerType.STILT_GRANARY: 0.25,
	ContainerType.COLD_CELLAR: 0.25,
	ContainerType.ICEHOUSE_VAULT: 0.10
}

const PRESERVATION_MULTIPLIERS: Dictionary = {
	PreservationMode.NONE: 1.00,
	PreservationMode.PICKLED: 0.14,
	PreservationMode.SMOKED: 0.10,
	PreservationMode.SALTED: 0.07,
	PreservationMode.DEHYDRATED: 0.08
}

## Arrhenius thermal kinetics: M_temp = 2.0^((T - 15) / 10)
static func calculate_arrhenius_multiplier(temp: float) -> float:
	if temp <= -5.0:
		return 0.02 # Deep permafrost freeze (halted microbial activity)
	elif temp <= 0.0:
		return 0.05 # Sub-zero icehouse vault storage
	elif temp > 45.0:
		return 8.00 # High heat microbial denaturation / rapid breakdown
	else:
		# Biological growth zone (0.0°C to 45.0°C) with Q10 = 2.0
		return pow(2.0, (temp - 15.0) / 10.0)

## Ambient relative humidity spoilage acceleration
static func calculate_humidity_multiplier(humidity: float, is_dry_good: bool = false) -> float:
	var rh = clampf(humidity, 0.0, 1.0)
	if is_dry_good:
		# Dry goods (grain, flour, hardtack) rot rapidly if RH > 0.55
		var excess = maxf(0.0, (rh - 0.55) / 0.45)
		return 1.0 + (excess * excess) * 4.0
	else:
		# Wet proteins and prepared meals: linear microbial acceleration
		return 0.80 + 0.60 * rh

static func get_container_multiplier(container_type: int) -> float:
	return CONTAINER_MULTIPLIERS.get(container_type, 1.0)

static func get_preservation_multiplier(mode: int) -> float:
	return PRESERVATION_MULTIPLIERS.get(mode, 1.0)

static func get_item_preservation_multiplier(food_name: String) -> float:
	var lower = food_name.to_lower()
	if "salted" in lower or "cured" in lower:
		return PRESERVATION_MULTIPLIERS[PreservationMode.SALTED] # 0.07
	elif "smoked" in lower:
		return PRESERVATION_MULTIPLIERS[PreservationMode.SMOKED] # 0.10
	elif "pickled" in lower or "sauerkraut" in lower:
		return PRESERVATION_MULTIPLIERS[PreservationMode.PICKLED] # 0.14
	elif "dried" in lower:
		return PRESERVATION_MULTIPLIERS[PreservationMode.DEHYDRATED] # 0.08
	return 1.0

static func is_dry_good_item(food_name: String) -> bool:
	var lower = food_name.to_lower()
	return "bread" in lower or "flour" in lower or "grain" in lower or "dried" in lower or "porridge" in lower

# --- PROJECT.md M3 Interface Contract ---

## Computes Arrhenius factor 2.0^((T-15)/10) coupled with relative humidity and preservation mode.
static func calculate_decay_multiplier(ambient_temp: float, humidity: float, container_type: int) -> float:
	var m_temp = calculate_arrhenius_multiplier(ambient_temp)
	var m_humidity = calculate_humidity_multiplier(humidity)
	var m_container = get_container_multiplier(container_type)
	return m_temp * m_humidity * m_container

## Extended decay calculation factoring specific food traits and preservation method
static func calculate_food_decay_rate(food_type: String, ambient_temp: float = 15.0, humidity: float = 0.5, container_type: int = ContainerType.WOODEN_CHEST, preservation_mode: int = PreservationMode.NONE) -> float:
	var is_dry = is_dry_good_item(food_type)
	var m_temp = calculate_arrhenius_multiplier(ambient_temp)
	var m_humidity = calculate_humidity_multiplier(humidity, is_dry)
	var m_container = get_container_multiplier(container_type)
	var m_preserv = get_preservation_multiplier(preservation_mode)
	if preservation_mode == PreservationMode.NONE:
		m_preserv = get_item_preservation_multiplier(food_type)
	return m_temp * m_humidity * m_container * m_preserv

static func get_shelf_life(food_type: String, is_cellar: bool = false, ambient_temp: float = 15.0, humidity: float = 0.5) -> float:
	var base_hours = BASE_SHELF_LIFE_HOURS.get(food_type, 120.0)
	var container = ContainerType.COLD_CELLAR if is_cellar else ContainerType.WOODEN_CHEST
	var decay_rate = calculate_food_decay_rate(food_type, ambient_temp, humidity, container)
	if decay_rate <= 0.0001:
		return 999999.0
	return base_hours / decay_rate

static func is_cold_cellar(storage_pos: Vector3i, voxel_world: VoxelWorld = null) -> bool:
	if storage_pos.y > CELLAR_MAX_ELEVATION:
		return false
		
	if voxel_world:
		# Verify overhead rock roof (>= 2 stone/brick blocks)
		var stone_count = 0
		for dy in range(1, 5):
			var b = voxel_world.get_block_world(storage_pos + Vector3i(0, dy, 0))
			if b == VoxelChunk.BlockType.STONE or b == VoxelChunk.BlockType.STONE_BRICKS:
				stone_count += 1
		return stone_count >= 2
	return true

static func is_icehouse_vault(storage_pos: Vector3i, voxel_world: VoxelWorld = null) -> bool:
	if not is_cold_cellar(storage_pos, voxel_world):
		return false
	if voxel_world:
		# Scan nearby voxels (radius 3) for ICE blocks
		for dx in range(-3, 4):
			for dy in range(-1, 3):
				for dz in range(-3, 4):
					var b = voxel_world.get_block_world(storage_pos + Vector3i(dx, dy, dz))
					if b == VoxelChunk.BlockType.ICE:
						return true
	return false

static func simulate_spoilage_cycle(food_inventory: Dictionary, elapsed_hours: float, is_cellar: bool = false, ambient_temp: float = 15.0, humidity: float = 0.5, container_type: int = -1) -> Dictionary:
	var report = {
		"spoiled": {},
		"remaining": {},
		"compost_produced": 0
	}
	
	var active_container = container_type
	if active_container < 0:
		active_container = ContainerType.COLD_CELLAR if is_cellar else ContainerType.WOODEN_CHEST

	for item in food_inventory.keys():
		var count = food_inventory[item]
		if count <= 0:
			continue
			
		var max_hours = BASE_SHELF_LIFE_HOURS.get(item, 120.0)
		var decay_mult = calculate_food_decay_rate(item, ambient_temp, humidity, active_container)
		
		# Spoilage probability per elapsed hour window
		var hourly_spoil_rate = (1.0 / max_hours) * decay_mult
		var total_loss_fraction = clampf(hourly_spoil_rate * elapsed_hours, 0.0, 1.0)
		var spoiled_amount = int(floor(count * total_loss_fraction))
		
		# If elapsed time exceeds effective shelf life completely, everything spoils
		if elapsed_hours * decay_mult >= max_hours:
			spoiled_amount = count
			
		var kept_amount = count - spoiled_amount
		if spoiled_amount > 0:
			report["spoiled"][item] = spoiled_amount
			report["compost_produced"] += spoiled_amount
		report["remaining"][item] = kept_amount

	return report
