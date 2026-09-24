# scripts/world/training_dummy.gd
# Voxel Lord: Feudal Realm - Milestone 20: Bellwright Combat Training Dummy
# Provides weapon proficiency drills for peasant recruits and militia levies

class_name TrainingDummy
extends Node3D

signal training_completed(soldier_id: String, skill_type: String, new_level: int)
signal dummy_damaged(remaining_durability: int, max_durability: int)
signal dummy_broken()
signal dummy_repaired()

const MAX_DURABILITY: int = 200
var current_durability: int = MAX_DURABILITY
var is_broken: bool = false

# Skill training caps for peasant militia
const MILITIA_SKILL_CAP: int = 50
const XP_PER_STRIKE: int = 2
const XP_PER_LEVEL: int = 20

func _init() -> void:
	current_durability = MAX_DURABILITY

func train(soldier_stats: Dictionary, weapon_type: String, strike_count: int) -> Dictionary:
	if is_broken:
		return {
			"success": false,
			"reason": "DUMMY_BROKEN",
			"strikes_performed": 0,
			"xp_gained": 0
		}
	
	var actual_strikes: int = min(strike_count, current_durability)
	current_durability -= actual_strikes
	dummy_damaged.emit(current_durability, MAX_DURABILITY)
	
	if current_durability <= 0:
		is_broken = true
		dummy_broken.emit()
	
	var skill_key: String = "melee_skill"
	if weapon_type == "hunting_bow":
		skill_key = "archery_skill"
	
	var current_skill: int = soldier_stats.get(skill_key, 10)
	var current_xp: int = soldier_stats.get(skill_key + "_xp", 0)
	
	var total_xp_gained: int = 0
	if current_skill < MILITIA_SKILL_CAP:
		total_xp_gained = actual_strikes * XP_PER_STRIKE
		current_xp += total_xp_gained
		
		while current_xp >= XP_PER_LEVEL and current_skill < MILITIA_SKILL_CAP:
			current_xp -= XP_PER_LEVEL
			current_skill += 1
			training_completed.emit(soldier_stats.get("id", "soldier_unknown"), skill_key, current_skill)
	
	soldier_stats[skill_key] = current_skill
	soldier_stats[skill_key + "_xp"] = current_xp
	
	return {
		"success": true,
		"strikes_performed": actual_strikes,
		"xp_gained": total_xp_gained,
		"skill_type": skill_key,
		"new_skill_level": current_skill,
		"remaining_durability": current_durability
	}

func repair(logs_available: int, leather_available: int) -> bool:
	if not is_broken and current_durability == MAX_DURABILITY:
		return false
	
	# Repair costs 2 timber logs and 1 leather strap
	if logs_available < 2 or leather_available < 1:
		return false
	
	current_durability = MAX_DURABILITY
	is_broken = false
	dummy_repaired.emit()
	return true
