# scripts/world/mead_fermenter.gd
# Voxel Lord: Feudal Realm - Milestone 22: Mead Fermentation Barrel & Beeswax Candle Press
# Inspired by Valheim (Mead Ketill & Fermenter) and Medieval Dynasty (Tavern Brewing)

class_name MeadFermenter
extends Node3D

signal mead_brewed(batches_produced: int, morale_bonus: int, warmth_bonus: float)
signal candles_molded(candles_produced: int)

var supply_chain: Node = null

const MEAD_MORALE_BONUS: int = 15
const MEAD_WINTER_WARMTH_BONUS: float = 25.0

var fermenter_stock: Dictionary = {
	"honeycomb": 12,
	"beeswax": 8,
	"clean_water": 10,
	"wheat": 10,
	"honey_mead": 0,
	"beeswax_candle": 0
}

func _init() -> void:
	pass

func brew_honey_mead(batches: int = 1) -> Dictionary:
	# 2 honeycomb + 1 clean_water + 1 wheat -> 2 honey_mead
	var hc_needed: int = batches * 2
	if fermenter_stock.get("honeycomb", 0) < hc_needed or fermenter_stock.get("clean_water", 0) < batches or fermenter_stock.get("wheat", 0) < batches:
		return {"success": false, "mead_produced": 0}
	
	fermenter_stock["honeycomb"] -= hc_needed
	fermenter_stock["clean_water"] -= batches
	fermenter_stock["wheat"] -= batches
	
	var produced: int = batches * 2
	fermenter_stock["honey_mead"] = fermenter_stock.get("honey_mead", 0) + produced
	
	if supply_chain and supply_chain.has_method("add_resource"):
		supply_chain.add_resource("honey_mead", produced)
	
	mead_brewed.emit(produced, MEAD_MORALE_BONUS, MEAD_WINTER_WARMTH_BONUS)
	return {
		"success": true,
		"mead_produced": produced,
		"morale_bonus": MEAD_MORALE_BONUS,
		"warmth_bonus": MEAD_WINTER_WARMTH_BONUS
	}

func mold_beeswax_candles(batches: int = 1) -> int:
	# 2 beeswax -> 3 beeswax_candle
	var wax_needed: int = batches * 2
	if fermenter_stock.get("beeswax", 0) < wax_needed:
		return 0
	
	fermenter_stock["beeswax"] -= wax_needed
	var produced: int = batches * 3
	fermenter_stock["beeswax_candle"] = fermenter_stock.get("beeswax_candle", 0) + produced
	
	if supply_chain and supply_chain.has_method("add_resource"):
		supply_chain.add_resource("beeswax_candle", produced)
	
	candles_molded.emit(produced)
	return produced
