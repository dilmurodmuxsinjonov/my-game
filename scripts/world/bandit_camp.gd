# scripts/world/bandit_camp.gd
# Voxel Lord: Feudal Realm - Milestone 25: Procedural Raider War Camp Outpost
# Inspired by Bellwright (Brigand Outposts) and Mount & Blade II (Bandit Hideouts)

class_name BanditCamp
extends Node3D

signal camp_cleared(loot: Dictionary)
signal barricade_damaged(damage_taken: float)

const BARRICADE_DAMAGE_REFLECT: float = 20.0
const CHEST_LOOT: Dictionary = {
	"gold_coins": 35,
	"iron_ingots": 4,
	"bread": 12,
	"raw_wool": 6
}

var camp_center: Vector3 = Vector3.ZERO
var is_cleared: bool = false
var tents_count: int = 2
var barricades_count: int = 3
var raiders_remaining: int = 4

func _init(center_pos: Vector3 = Vector3.ZERO) -> void:
	camp_center = center_pos
	is_cleared = false
	raiders_remaining = 4

func on_raider_killed() -> void:
	raiders_remaining = maxi(0, raiders_remaining - 1)
	if raiders_remaining <= 0 and not is_cleared:
		is_cleared = true
		camp_cleared.emit(CHEST_LOOT)

func trigger_barricade_collision(attacker: Node3D) -> float:
	# Spiked barricades impale reckless charges
	barricade_damaged.emit(BARRICADE_DAMAGE_REFLECT)
	return BARRICADE_DAMAGE_REFLECT

func claim_loot() -> Dictionary:
	if not is_cleared:
		return {"success": false, "reason": "CAMP_DEFENDED", "loot": {}}
	return {"success": true, "loot": CHEST_LOOT}
