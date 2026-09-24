class_name ApotheosisManager
extends RefCounted

## Apotheosis Combat Modifiers & Gem Socketing System.
## Governs procedural boss champion affixes (Infernal, Armored, Swift, Vampiric, Tempest, Titan)
## and multi-socket gem cutting and socketing onto feudal weapons and armor.

const AFFIX_INFERNAL: String = "infernal"
const AFFIX_ARMORED: String = "armored"
const AFFIX_SWIFT: String = "swift"
const AFFIX_VAMPIRIC: String = "vampiric"
const AFFIX_TEMPEST: String = "tempest"
const AFFIX_TITAN: String = "titan"

const ALL_AFFIXES: Array[String] = [
	AFFIX_INFERNAL,
	AFFIX_ARMORED,
	AFFIX_SWIFT,
	AFFIX_VAMPIRIC,
	AFFIX_TEMPEST,
	AFFIX_TITAN
]

# Gem Types and Socket Modifiers
const GEM_RUBY: String = "ruby"
const GEM_SAPPHIRE: String = "sapphire"
const GEM_TOPAZ: String = "topaz"
const GEM_DEEP_GEM: String = "deep_gem"

const VALID_GEMS: Array[String] = [
	GEM_RUBY,
	GEM_SAPPHIRE,
	GEM_TOPAZ,
	GEM_DEEP_GEM
]

## Roll procedural Apotheosis boss affixes
static func roll_boss_affixes(tier: int = 1) -> Dictionary:
	var pool = ALL_AFFIXES.duplicate()
	pool.shuffle()
	
	var affix_count = mini(tier, 2)
	var chosen_affixes: Array[String] = []
	for i in range(affix_count):
		chosen_affixes.append(pool[i])
		
	var hp_mult: float = 1.0
	var speed_mult: float = 1.0
	var dmg_mult: float = 1.0
	var armor_reduct: float = 0.0
	var lifesteal: float = 0.0
	var burns_target: bool = false
	
	var prefix: String = ""
	var suffix: String = ""
	
	for affix in chosen_affixes:
		match affix:
			AFFIX_INFERNAL:
				prefix = "Infernal"
				dmg_mult += 0.25
				burns_target = true
			AFFIX_ARMORED:
				prefix = "Iron-Clad" if prefix.is_empty() else prefix
				armor_reduct += 0.30
			AFFIX_SWIFT:
				prefix = "Fleet-Footed" if prefix.is_empty() else prefix
				speed_mult += 0.35
			AFFIX_VAMPIRIC:
				suffix = "the Blood Drinker"
				lifesteal += 0.25
			AFFIX_TEMPEST:
				suffix = "of the Tempest"
				dmg_mult += 0.20
			AFFIX_TITAN:
				suffix = "the Colossus"
				hp_mult += 0.50
				
	var title = "Bandit Warlord"
	if not prefix.is_empty() and not suffix.is_empty():
		title = "%s Bandit Warlord %s" % [prefix, suffix]
	elif not prefix.is_empty():
		title = "%s Bandit Warlord" % prefix
	elif not suffix.is_empty():
		title = "Bandit Warlord %s" % suffix
		
	return {
		"title": title,
		"affixes": chosen_affixes,
		"hp_multiplier": hp_mult,
		"speed_multiplier": speed_mult,
		"damage_multiplier": dmg_mult,
		"armor_reduction": armor_reduct,
		"lifesteal_percent": lifesteal,
		"burns_target": burns_target
	}

## Socket a cut gem into an item
static func socket_gem(item: Dictionary, gem_id: String) -> bool:
	if gem_id not in VALID_GEMS:
		return false
		
	if not item.has("sockets"):
		item["sockets"] = []
		
	var max_sockets = item.get("max_sockets", 2)
	if item["sockets"].size() >= max_sockets:
		return false # Sockets are full
		
	item["sockets"].append(gem_id)
	return true

## Remove a gem from an item socket
static func unsocket_gem(item: Dictionary, slot_index: int = 0) -> String:
	if not item.has("sockets") or item["sockets"].is_empty():
		return ""
	if slot_index < 0 or slot_index >= item["sockets"].size():
		return ""
		
	var removed_gem = item["sockets"].pop_at(slot_index)
	return removed_gem

## Calculate cumulative combat bonuses from all socketed gems on an item
static func calculate_socketed_bonuses(item: Dictionary) -> Dictionary:
	var bonuses = {
		"crit_damage_percent": 0.0,
		"armor_penetration_percent": 0.0,
		"stamina_cost_reduction": 0.0,
		"lifesteal_percent": 0.0,
		"bonus_health": 0.0,
		"damage_resistance_percent": 0.0
	}
	
	if not item.has("sockets"):
		return bonuses
		
	var is_weapon = item.get("type") in ["tool", "weapon", "bow"] or item.get("tool_type") in ["sword", "axe", "pickaxe", "bow"]
	
	for gem in item["sockets"]:
		match gem:
			GEM_RUBY:
				if is_weapon:
					bonuses["crit_damage_percent"] += 0.20
				else:
					bonuses["bonus_health"] += 25.0
			GEM_SAPPHIRE:
				if is_weapon:
					bonuses["armor_penetration_percent"] += 0.20
				else:
					bonuses["damage_resistance_percent"] += 0.15
			GEM_TOPAZ:
				if is_weapon:
					bonuses["stamina_cost_reduction"] += 0.25
				else:
					bonuses["damage_resistance_percent"] += 0.10
			GEM_DEEP_GEM:
				if is_weapon:
					bonuses["lifesteal_percent"] += 0.15
				else:
					bonuses["bonus_health"] += 40.0
					bonuses["damage_resistance_percent"] += 0.10
					
	return bonuses

## Cut raw mineral gem into a specific jewel
static func cut_gem(raw_gem_name: String, preferred_gem: String = "") -> String:
	if not preferred_gem.is_empty() and preferred_gem in VALID_GEMS:
		return preferred_gem
		
	var possible = [GEM_RUBY, GEM_SAPPHIRE, GEM_TOPAZ, GEM_DEEP_GEM]
	return possible[randi() % possible.size()]
