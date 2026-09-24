# scripts/world/burgage_plot.gd
# Voxel Lord: Feudal Realm - Milestone 20: Manor Lords Burgage Backyard Extension Plots
# Simulates peasant household auxiliary production (chicken coops, goat pens, vegetable gardens)

class_name BurgagePlot
extends Node3D

signal plot_harvested(plot_type: String, items: Dictionary)
signal plot_extension_upgraded(new_extension: String)

enum ExtensionType {
	NONE,
	CHICKEN_COOP,
	GOAT_PEN,
	VEGETABLE_GARDEN,
	BACKYARD_WORKSHOP
}

@export var current_extension: ExtensionType = ExtensionType.CHICKEN_COOP
@export var assigned_household_id: String = "peasant_family_1"

# Production accumulator and storage
var production_timer: float = 0.0
const DAILY_CYCLE_SECONDS: float = 120.0 # 2 minutes real time per game day
var stored_produce: Dictionary = {}
const MAX_PLOT_STORAGE: int = 24

# Household welfare metrics
var household_happiness_bonus: int = 15
var daily_land_tax_contribution: int = 1 # Paid directly to Royal Treasury

func _init(extension: ExtensionType = ExtensionType.CHICKEN_COOP) -> void:
	current_extension = extension

func set_extension(new_ext: ExtensionType) -> void:
	current_extension = new_ext
	stored_produce.clear()
	production_timer = 0.0
	plot_extension_upgraded.emit(get_extension_name())

func get_extension_name() -> String:
	match current_extension:
		ExtensionType.CHICKEN_COOP: return "CHICKEN_COOP"
		ExtensionType.GOAT_PEN: return "GOAT_PEN"
		ExtensionType.VEGETABLE_GARDEN: return "VEGETABLE_GARDEN"
		ExtensionType.BACKYARD_WORKSHOP: return "BACKYARD_WORKSHOP"
		_: return "NONE"

func process_production(delta: float) -> Dictionary:
	production_timer += delta
	var produced_this_tick: Dictionary = {}
	
	if production_timer >= DAILY_CYCLE_SECONDS:
		production_timer -= DAILY_CYCLE_SECONDS
		produced_this_tick = generate_daily_yield()
	
	return produced_this_tick

func generate_daily_yield() -> Dictionary:
	var yield_items: Dictionary = {}
	match current_extension:
		ExtensionType.CHICKEN_COOP:
			# Yields 3 fresh eggs and 1 feather daily
			yield_items = {"egg": 3, "feather": 1}
		ExtensionType.GOAT_PEN:
			# Yields 2 leather hides and 1 milk jug
			yield_items = {"leather_hide": 2, "milk_jug": 1}
		ExtensionType.VEGETABLE_GARDEN:
			# Yields seasonal vegetables: carrots, cabbage, onions
			yield_items = {"carrot": 2, "cabbage": 2, "onion": 1}
		ExtensionType.BACKYARD_WORKSHOP:
			# Crafts basic domestic wooden bowls and tools
			yield_items = {"wooden_bowl": 2, "iron_nails": 4}
	
	for item in yield_items.keys():
		var qty: int = yield_items[item]
		var current_qty: int = stored_produce.get(item, 0)
		var total_stored: int = get_total_stored_count()
		var space_left: int = max(0, MAX_PLOT_STORAGE - total_stored)
		var to_add: int = min(qty, space_left)
		stored_produce[item] = current_qty + to_add
	
	return yield_items

func get_total_stored_count() -> int:
	var count: int = 0
	for amt in stored_produce.values():
		count += amt
	return count

func harvest_all() -> Dictionary:
	var collected: Dictionary = stored_produce.duplicate()
	stored_produce.clear()
	plot_harvested.emit(get_extension_name(), collected)
	return collected

func get_dietary_diversity_score() -> int:
	# Manor Lords food variety satisfaction mechanic
	match current_extension:
		ExtensionType.CHICKEN_COOP: return 2 # Eggs provide protein diversity
		ExtensionType.GOAT_PEN: return 2     # Dairy/milk
		ExtensionType.VEGETABLE_GARDEN: return 3 # 3 vegetable varieties
		_: return 0
