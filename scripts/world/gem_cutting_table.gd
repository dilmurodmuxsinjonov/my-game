class_name GemCuttingTable
extends Node3D

const ApotheosisManager = preload("res://scripts/magic/apotheosis_manager.gd")

## Apotheosis Lapidary Gem Cutting Table (Milestone 14).
## Cuts raw underground gemstone deposits into faceted gems (Ruby, Sapphire, Topaz, Deep Gem)
## and provides multi-socket gem infusion into weapons and royal plate armor.

signal gem_cut(gem_id: String)
signal gem_socketed(item_name: String, gem_id: String)

var supply_chain: SupplyChain
var model_instance: Node3D

func _ready() -> void:
	_load_model()

func _load_model() -> void:
	var glb_path = "res://assets/models/gem_cutting_table.glb"
	if ResourceLoader.exists(glb_path):
		var scene = load(glb_path)
		if scene:
			model_instance = scene.instantiate()
			add_child(model_instance)

## Cut 1 raw gem into a faceted jewel
func cut_raw_gem(preferred_gem: String = "") -> String:
	if not supply_chain:
		return ""
		
	if supply_chain.inventory.get("gems", 0) <= 0:
		return "" # No raw gems in stockpile
		
	supply_chain.consume_resource("gems", 1)
	var result_gem = ApotheosisManager.cut_gem("gems", preferred_gem)
	supply_chain.add_resource(result_gem, 1)
	gem_cut.emit(result_gem)
	return result_gem

## Socket a cut gem into an equipment item
func socket_equipment_item(item: Dictionary, gem_id: String) -> bool:
	if not supply_chain:
		return false
		
	if supply_chain.inventory.get(gem_id, 0) <= 0:
		return false
		
	var success = ApotheosisManager.socket_gem(item, gem_id)
	if success:
		supply_chain.consume_resource(gem_id, 1)
		gem_socketed.emit(item.get("name", "Equipment"), gem_id)
		return true
		
	return false
