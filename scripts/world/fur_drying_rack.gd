# scripts/world/fur_drying_rack.gd
# Voxel Lord: Feudal Realm - Milestone 26: Fur Curing & Luxury Winter Garments
# Simulates A-frame timber racks curing raw pelts into soft fur for noble winter cloaks.

class_name FurDryingRack
extends RefCounted

signal pelt_cured(rack_id: String, count: int)

var rack_id: String = "drying_rack_1"
var max_slots: int = 4

var mounted_pelts: int = 0
var curing_progress: float = 0.0
var cure_time_per_pelt: float = 20.0 # 20 seconds to cure stretched pelts

var cured_furs_stored: int = 0

func _init(p_id: String = "drying_rack_1") -> void:
	rack_id = p_id

func mount_pelts(count: int) -> int:
	var available_space = max_slots - mounted_pelts
	var added = min(count, available_space)
	mounted_pelts += added
	return added

func process_tick(delta: float) -> bool:
	if mounted_pelts == 0:
		return false

	curing_progress += delta
	if curing_progress >= cure_time_per_pelt:
		# One pelt cured
		mounted_pelts -= 1
		cured_furs_stored += 1
		curing_progress = 0.0

		pelt_cured.emit(rack_id, 1)
		return true
	return false

func collect_cured_furs() -> int:
	var count = cured_furs_stored
	cured_furs_stored = 0
	return count

# Luxury Fur Crafting
static func can_craft_fur_cloak(inv: Dictionary) -> bool:
	return inv.get("cured_fur", 0) >= 3 and inv.get("woolen_tunic", 0) >= 1

static func craft_fur_cloak(inv: Dictionary) -> Dictionary:
	if not can_craft_fur_cloak(inv):
		return {}

	inv["cured_fur"] -= 3
	inv["woolen_tunic"] -= 1
	inv["fur_cloak"] = inv.get("fur_cloak", 0) + 1

	return {
		"item": "fur_cloak",
		"warmth_bonus": 50.0, # Complete blizzard immunity
		"noble_morale_boost": 15,
		"trade_value_coins": 15
	}
