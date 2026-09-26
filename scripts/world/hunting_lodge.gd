# scripts/world/hunting_lodge.gd
# Voxel Lord: Feudal Realm - Milestone 26: Hunting, Trapping & Wildlife Tracking
# Simulates forest/highland hunting outposts, wildlife yields, and archery blind upgrades.

class_name HuntingLodge
extends RefCounted

signal harvest_completed(lodge_id: String, yield_dict: Dictionary)
signal hunter_injured(hunter_id: String, damage: float, cause: String)

var lodge_id: String = "hunting_lodge_1"
var max_hunters: int = 3
var assigned_hunters: Array[String] = []

# Biome ecology modifiers
var current_biome: String = "DeepForest"
var biome_multipliers: Dictionary = {
	"DeepForest": 1.50,
	"Highlands": 1.20,
	"RiverValley": 1.00,
	"Plains": 0.80
}

# Upgrades
var has_archery_blind: bool = false
var has_hunting_bows: bool = true

# Storage stockpile
var inventory: Dictionary = {
	"raw_venison": 0,
	"raw_hide": 0,
	"tallow": 0,
	"raw_pelt": 0,
	"stag_antlers": 0
}

func _init(p_id: String = "hunting_lodge_1", p_biome: String = "DeepForest") -> void:
	lodge_id = p_id
	current_biome = p_biome

func assign_hunter(hunter_id: String) -> bool:
	if assigned_hunters.size() >= max_hunters:
		return false
	if not assigned_hunters.has(hunter_id):
		assigned_hunters.append(hunter_id)
		return true
	return false

func unassign_hunter(hunter_id: String) -> bool:
	if assigned_hunters.has(hunter_id):
		assigned_hunters.erase(hunter_id)
		return true
	return false

func set_archery_blind(installed: bool) -> void:
	has_archery_blind = installed

func execute_daily_hunt(rng_seed: float = 0.5) -> Dictionary:
	var hunter_count = assigned_hunters.size()
	if hunter_count == 0:
		return {}

	var biome_mult = biome_multipliers.get(current_biome, 1.0)
	var blind_bonus = 1.35 if has_archery_blind else 1.0
	var effective_mult = biome_mult * blind_bonus

	var venison_yield = int(round(3.0 * hunter_count * effective_mult))
	var hide_yield = int(round(2.0 * hunter_count * effective_mult))
	var tallow_yield = int(round(1.0 * hunter_count * effective_mult))
	var pelt_yield = int(round(1.0 * hunter_count * effective_mult))

	inventory["raw_venison"] += venison_yield
	inventory["raw_hide"] += hide_yield
	inventory["tallow"] += tallow_yield
	inventory["raw_pelt"] += pelt_yield

	# Rare stag trophy roll
	if rng_seed > 0.85:
		inventory["stag_antlers"] += 1

	# Wildlife attack risk (boar charge / wolf pack)
	# Archery blind lowers injury risk from 15% to 3%
	var injury_risk = 0.03 if has_archery_blind else 0.15
	if rng_seed < injury_risk and hunter_count > 0:
		var injured_hunter = assigned_hunters[0]
		hunter_injured.emit(injured_hunter, 25.0, "WildBoarTuskGore")

	var batch_yield = {
		"raw_venison": venison_yield,
		"raw_hide": hide_yield,
		"tallow": tallow_yield,
		"raw_pelt": pelt_yield
	}

	harvest_completed.emit(lodge_id, batch_yield)
	return batch_yield

func get_stockpile() -> Dictionary:
	return inventory.duplicate()
