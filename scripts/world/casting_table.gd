class_name CastingTable
extends Node3D

## Tinkers' Construct Casting Table.
## Holds swappable ceramic or brass tool molds.
## Pours molten alloys directly into precision tool parts (blades, pickaxe heads, ingots)
## with zero material waste.

signal mold_changed(new_mold: String)
signal metal_poured(metal_type: String, current_units: int, required_units: int)
signal item_solidified(item_id: String)
signal item_extracted(item_id: String)

const COOLING_DURATION: float = 3.0 # Seconds to cool tool mold

const MOLD_RECIPES: Dictionary = {
	"ingot_mold": {
		"required_units": 1,
		"output_pattern": "{metal}_ingot"
	},
	"sword_blade_mold": {
		"required_units": 2,
		"output_pattern": "cast_{metal}_blade"
	},
	"pickaxe_head_mold": {
		"required_units": 3,
		"output_pattern": "cast_{metal}_pickaxe"
	},
	"axe_head_mold": {
		"required_units": 3,
		"output_pattern": "cast_{metal}_axe"
	}
}

@export var current_mold: String = "ingot_mold"
@export var contained_metal: String = ""
@export var current_units: int = 0
@export var cooling_timer: float = 0.0
@export var is_solid: bool = false
@export var output_item: String = ""

var supply_chain: SupplyChain = null
var model_node: Node3D = null

func _ready() -> void:
	_load_model()

func _load_model() -> void:
	var glb_path = "res://assets/models/casting_table.glb"
	if ResourceLoader.exists(glb_path):
		var scene = load(glb_path)
		if scene:
			model_node = scene.instantiate()
			add_child(model_node)

func set_mold(mold_id: String) -> bool:
	if current_units > 0 or is_solid:
		return false # Cannot change mold while metal is inside
	if mold_id in MOLD_RECIPES:
		current_mold = mold_id
		emit_signal("mold_changed", current_mold)
		return true
	return false

func get_required_units() -> int:
	return MOLD_RECIPES.get(current_mold, {}).get("required_units", 1)

func pour_metal(metal_type: String, units: int) -> int:
	if is_solid:
		return 0 # Must collect previous cast item

	if current_units > 0 and contained_metal != metal_type:
		return 0 # Cannot mix metals

	var req = get_required_units()
	contained_metal = metal_type
	var needed = req - current_units
	var poured = min(needed, units)
	current_units += poured

	emit_signal("metal_poured", contained_metal, current_units, req)

	if current_units >= req:
		cooling_timer = COOLING_DURATION

	return poured

func tick(delta: float) -> void:
	var req = get_required_units()
	if current_units >= req and not is_solid:
		if cooling_timer > 0.0:
			cooling_timer -= delta
			if cooling_timer <= 0.0:
				_solidify()

func _solidify() -> void:
	is_solid = true
	cooling_timer = 0.0
	var pattern = MOLD_RECIPES.get(current_mold, {}).get("output_pattern", "{metal}_ingot")
	output_item = pattern.replace("{metal}", contained_metal)
	emit_signal("item_solidified", output_item)

func take_result() -> String:
	if not is_solid:
		return ""
	var result = output_item
	is_solid = false
	contained_metal = ""
	current_units = 0
	output_item = ""
	emit_signal("item_extracted", result)
	return result
