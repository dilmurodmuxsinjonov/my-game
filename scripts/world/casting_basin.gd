class_name CastingBasin
extends Node3D

## Tinkers' Construct Casting Basin.
## Placed beneath a smeltery faucet or fed manually.
## Collects 9 units of molten liquid metal and cools it into a solid metal block.

signal metal_poured(metal_type: String, current_units: int, required_units: int)
signal block_solidified(block_id: String)
signal block_extracted(block_id: String)

const UNITS_PER_BLOCK: int = 9
const COOLING_DURATION: float = 5.0 # Seconds to solidify into solid voxel block

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
	var glb_path = "res://assets/models/casting_basin.glb"
	if ResourceLoader.exists(glb_path):
		var scene = load(glb_path)
		if scene:
			model_node = scene.instantiate()
			add_child(model_node)

func pour_metal(metal_type: String, units: int) -> int:
	if is_solid:
		return 0 # Existing block must be collected first

	if current_units > 0 and contained_metal != metal_type:
		return 0 # Cannot mix different molten liquids in same basin

	contained_metal = metal_type
	var needed = UNITS_PER_BLOCK - current_units
	var poured = min(needed, units)
	current_units += poured

	emit_signal("metal_poured", contained_metal, current_units, UNITS_PER_BLOCK)

	if current_units >= UNITS_PER_BLOCK:
		cooling_timer = COOLING_DURATION

	return poured

func tick(delta: float) -> void:
	if current_units >= UNITS_PER_BLOCK and not is_solid:
		if cooling_timer > 0.0:
			cooling_timer -= delta
			if cooling_timer <= 0.0:
				_solidify()

func _solidify() -> void:
	is_solid = true
	cooling_timer = 0.0
	output_item = contained_metal + "_block"
	emit_signal("block_solidified", output_item)

func take_result() -> String:
	if not is_solid:
		return ""
	var result = output_item
	is_solid = false
	contained_metal = ""
	current_units = 0
	output_item = ""
	emit_signal("block_extracted", result)
	return result
