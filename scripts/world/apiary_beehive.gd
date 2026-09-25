# scripts/world/apiary_beehive.gd
# Voxel Lord: Feudal Realm - Milestone 22: Apiculture Beehive Skep & Crop Pollination
# Inspired by Medieval Dynasty (Apiary) and Valheim (Beehive Comfort & Honey)

class_name ApiaryBeehive
extends Node3D

signal honey_harvested(honeycomb_qty: int, beeswax_qty: int)
signal pollination_pulse(radius: float, growth_bonus: float)

var supply_chain: Node = null

const POLLINATION_RADIUS: float = 18.0
const POLLINATION_GROWTH_MULTIPLIER: float = 1.20 # +20% crop growth speed
const DAILY_HONEYCOMB_YIELD: int = 3
const DAILY_BEESWAX_YIELD: int = 2
const MAX_HIVE_STORAGE: int = 15

var stored_honeycomb: int = 0
var stored_beeswax: int = 0
var bees_happy: bool = true

func _init() -> void:
	pass

func produce_daily_cycle() -> Dictionary:
	if not bees_happy:
		return {"honeycomb": 0, "beeswax": 0}
	
	stored_honeycomb = mini(MAX_HIVE_STORAGE, stored_honeycomb + DAILY_HONEYCOMB_YIELD)
	stored_beeswax = mini(MAX_HIVE_STORAGE, stored_beeswax + DAILY_BEESWAX_YIELD)
	pollination_pulse.emit(POLLINATION_RADIUS, POLLINATION_GROWTH_MULTIPLIER)
	
	return {
		"honeycomb": stored_honeycomb,
		"beeswax": stored_beeswax,
		"pollination_bonus": POLLINATION_GROWTH_MULTIPLIER
	}

func harvest_hive() -> Dictionary:
	var hc: int = stored_honeycomb
	var bw: int = stored_beeswax
	stored_honeycomb = 0
	stored_beeswax = 0
	
	if supply_chain and supply_chain.has_method("add_resource"):
		if hc > 0:
			supply_chain.add_resource("honeycomb", hc)
		if bw > 0:
			supply_chain.add_resource("beeswax", bw)
	
	honey_harvested.emit(hc, bw)
	return {"honeycomb": hc, "beeswax": bw}

func is_crop_within_pollination(crop_pos: Vector3) -> bool:
	return global_position.distance_to(crop_pos) <= POLLINATION_RADIUS
