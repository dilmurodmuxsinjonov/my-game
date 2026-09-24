class_name FuneralPyre
extends Node3D

## Sanctified Funeral Pyre & Crematorium.
## Inspired by RimWorld and Going Medieval:
## Cleanses casualties after sieges or plagues, eliminating filth and disease miasma.
## Also grants +10 kingdom morale for dignified rites and prevents undead raising.

signal corpse_cremated(total_burned: int, morale_gained: float)
signal pyre_ignited()
signal pyre_extinguished()

@export var is_burning: bool = true
@export var ashes_count: int = 0
@export var miasma_protection_radius: float = 30.0 # Meters of pathogen protection

var supply_chain: SupplyChain = null
var model_node: Node3D = null

func _ready() -> void:
	_load_model()

func _load_model() -> void:
	var glb_path = "res://assets/models/funeral_pyre.glb"
	if ResourceLoader.exists(glb_path):
		var scene = load(glb_path)
		if scene:
			model_node = scene.instantiate()
			add_child(model_node)

func cremate_corpses(corpse_count: int = 1, wood_logs_supplied: int = 2) -> Dictionary:
	if wood_logs_supplied < corpse_count * 2:
		return {"success": false, "reason": "Insufficient firewood for holy pyre"}
	
	ashes_count += corpse_count
	var morale_boost = 10.0 * float(corpse_count)
	
	if supply_chain:
		supply_chain.morale = clamp(supply_chain.morale + (2.0 * corpse_count), 0.0, 100.0)
	
	emit_signal("corpse_cremated", corpse_count, morale_boost)
	return {
		"success": true,
		"cremated_count": corpse_count,
		"ashes_yield": corpse_count,
		"morale_gain": morale_boost
	}

func is_position_protected(pos: Vector3) -> bool:
	return global_position.distance_to(pos) <= miasma_protection_radius
