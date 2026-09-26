# scripts/entities/bandit_archetype.gd
# Voxel Lord: Feudal Realm - Milestone 25: Specialized Raider Archetypes
# Inspired by Mount & Blade II (Shield Walls & Archers) and Bellwright (Berserker Brigands)

class_name BanditArchetype
extends RefCounted

enum Archetype {
	SHIELDBEARER = 0,
	ARCHER = 1,
	BERSERKER = 2
}

const ARCHETYPE_CONFIG: Dictionary = {
	Archetype.SHIELDBEARER: {
		"title": "Raider Shieldbearer",
		"max_health": 80.0,
		"move_speed": 2.8,
		"attack_damage": 10.0,
		"attack_range": 2.0,
		"block_efficiency": 0.75, # 75% frontal damage mitigation
		"preferred_range": 1.8
	},
	Archetype.ARCHER: {
		"title": "Bandit Marksman",
		"max_health": 45.0,
		"move_speed": 4.2,
		"attack_damage": 18.0, # Ranged arrow volley
		"attack_range": 25.0,
		"block_efficiency": 0.0,
		"preferred_range": 16.0
	},
	Archetype.BERSERKER: {
		"title": "Berserker Marauder",
		"max_health": 65.0,
		"move_speed": 5.2,
		"attack_damage": 24.0, # Dual axe heavy cleave
		"attack_range": 2.2,
		"block_efficiency": 0.0,
		"preferred_range": 2.0
	}
}

var current_archetype: Archetype = Archetype.SHIELDBEARER
var is_shield_raised: bool = true
var is_reloading_bow: bool = false
var leap_cooldown: float = 0.0

func _init(arch: Archetype = Archetype.SHIELDBEARER) -> void:
	current_archetype = arch
	is_shield_raised = (arch == Archetype.SHIELDBEARER)

func get_config() -> Dictionary:
	return ARCHETYPE_CONFIG.get(current_archetype, ARCHETYPE_CONFIG[Archetype.SHIELDBEARER])

func calculate_damage_taken(raw_damage: float, is_frontal: bool, is_piercing: bool = false) -> Dictionary:
	var cfg = get_config()
	var final_damage = raw_damage
	var was_blocked = false

	if current_archetype == Archetype.SHIELDBEARER and is_shield_raised and is_frontal:
		var block_rate = cfg["block_efficiency"]
		# Shields are especially effective against arrows (90% deflection)
		if is_piercing:
			block_rate = 0.90
		final_damage = raw_damage * (1.0 - block_rate)
		was_blocked = true
	
	return {
		"damage": final_damage,
		"was_blocked": was_blocked,
		"mitigated": raw_damage - final_damage
	}

func evaluate_tactical_action(dist_to_target: float) -> Dictionary:
	match current_archetype:
		Archetype.SHIELDBEARER:
			# Advance steadily with shield locked
			return {
				"action": "SHIELD_ADVANCE",
				"desired_speed": ARCHETYPE_CONFIG[Archetype.SHIELDBEARER]["move_speed"],
				"should_attack": dist_to_target <= ARCHETYPE_CONFIG[Archetype.SHIELDBEARER]["attack_range"]
			}
		Archetype.ARCHER:
			# Kite if too close, shoot if in range
			if dist_to_target < 6.0:
				return {"action": "KITE_RETREAT", "desired_speed": 4.5, "should_attack": false}
			elif dist_to_target <= 25.0:
				return {"action": "SHOOT_ARROW", "desired_speed": 0.0, "should_attack": true}
			else:
				return {"action": "APPROACH", "desired_speed": 4.0, "should_attack": false}
		Archetype.BERSERKER:
			# Lunge leap if within 6 meters, otherwise sprint full speed
			if dist_to_target <= 6.0 and dist_to_target > 2.2 and leap_cooldown <= 0.0:
				leap_cooldown = 4.0
				return {"action": "BERSERK_LEAP", "desired_speed": 8.0, "should_attack": true}
			return {
				"action": "BERSERK_CHARGE",
				"desired_speed": ARCHETYPE_CONFIG[Archetype.BERSERKER]["move_speed"],
				"should_attack": dist_to_target <= ARCHETYPE_CONFIG[Archetype.BERSERKER]["attack_range"]
			}
	return {"action": "IDLE", "desired_speed": 0.0, "should_attack": false}
