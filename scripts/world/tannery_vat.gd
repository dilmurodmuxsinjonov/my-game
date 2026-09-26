# scripts/world/tannery_vat.gd
# Voxel Lord: Feudal Realm - Milestone 26: Oak Bark Leather Tanning
# Simulates soaking vats converting raw animal hides and oak bark tannin into cured leather.

class_name TanneryVat
extends RefCounted

signal batch_cured(vat_id: String, cured_count: int)

var vat_id: String = "tannery_vat_1"
var max_capacity: int = 12 # 6 batches of 2 hides

# Resource inputs in vat
var raw_hides: int = 0
var oak_bark: int = 0
var water_buckets: int = 0

# Tanning process state
var is_soaking: bool = false
var progress_timer: float = 0.0
var soak_duration: float = 30.0 # 30 seconds per cycle

# Finished output
var cured_leather: int = 0

func _init(p_id: String = "tannery_vat_1") -> void:
	vat_id = p_id

func load_materials(hides: int, bark: int, water: int) -> bool:
	if is_soaking:
		return false
	if (raw_hides + hides) > max_capacity:
		return false

	raw_hides += hides
	oak_bark += bark
	water_buckets += water
	return true

func can_start_tanning() -> bool:
	# Requires at least 2 hides, 1 bark, 1 water
	return (not is_soaking) and (raw_hides >= 2) and (oak_bark >= 1) and (water_buckets >= 1)

func start_tanning() -> bool:
	if not can_start_tanning():
		return false

	is_soaking = true
	progress_timer = 0.0
	return true

func process_tick(delta: float) -> bool:
	if not is_soaking:
		return false

	progress_timer += delta
	if progress_timer >= soak_duration:
		# Calculate completed batches
		var batches = min(raw_hides / 2, min(oak_bark, water_buckets))
		var processed_hides = batches * 2

		raw_hides -= processed_hides
		oak_bark -= batches
		water_buckets -= batches

		cured_leather += processed_hides
		is_soaking = false
		progress_timer = 0.0

		batch_cured.emit(vat_id, processed_hides)
		return true
	return false

func collect_leather() -> int:
	var collected = cured_leather
	cured_leather = 0
	return collected

# Feudal Leather Crafting Applications
static func can_craft_gambeson(inv: Dictionary) -> bool:
	return inv.get("cured_leather", 0) >= 4 and inv.get("raw_wool", 0) >= 2

static func craft_gambeson(inv: Dictionary) -> bool:
	if can_craft_gambeson(inv):
		inv["cured_leather"] -= 4
		inv["raw_wool"] -= 2
		inv["gambeson"] = inv.get("gambeson", 0) + 1
		return true
	return false

static func can_craft_ox_harness(inv: Dictionary) -> bool:
	return inv.get("cured_leather", 0) >= 3 and inv.get("iron_ingot", 0) >= 2

static func craft_ox_harness(inv: Dictionary) -> bool:
	if can_craft_ox_harness(inv):
		inv["cured_leather"] -= 3
		inv["iron_ingot"] -= 2
		inv["ox_harness"] = inv.get("ox_harness", 0) + 1
		return true
	return false
