class_name EnchantmentManager
extends Node

## Arcane Enchantment & Rune Engine (Apotheosis & Enigmatic Legacy paradigm).
## Distinguishes between craftable common runes (crafted by Enchanter from mob drops/herbs)
## and legendary uncraftable affixes (dropped exclusively by Bandit Warlords & Ancient Ruins).

signal item_enchanted(item_name: String, enchantment_name: String, level: int)
signal legendary_affix_triggered(affix_name: String, source_entity: Node, target_entity: Node)

# Common Enchantment Identifiers
const ENCH_SHARPNESS: String = "sharpness"      # Tiers I-V (+15% melee damage/tier)
const ENCH_PROTECTION: String = "protection"    # Tiers I-IV (+10% damage mitigation/tier)
const ENCH_UNBREAKING: String = "unbreaking"    # Tiers I-III (-25% wear/tier)
const ENCH_POWER: String = "power"              # Tiers I-V (+15% arrow velocity & damage/tier)

# Legendary Affixes (Drop Only)
const AFFIX_DRAGONS_BREATH: String = "dragons_breath" # Burns targets for 4s (8 dmg/sec)
const AFFIX_VAMPIRIC_LEECH: String = "vampiric_leech" # 15% life steal into Monarch health
const AFFIX_THUNDERSTRIKE: String = "thunderstrike"   # Lightning AOE explosion at arrow impact (30 dmg, 5m radius)
const AFFIX_WINDSTRIDER: String = "windstrider"       # +30% movement speed & water walking
const AFFIX_FORTRESS_HEART: String = "fortress_heart" # 90% mitigation shield for 5s when HP < 25%

# Common Rune Crafting Recipes (Enchanter's Table)
const RUNE_RECIPES: Dictionary = {
	"rune_sharpness_1": {
		"name": "Rune of Sharpness I",
		"enchantment": ENCH_SHARPNESS,
		"level": 1,
		"inputs": {"blood_vial": 1, "stone": 2, "flax": 1},
		"icon": "🗡️"
	},
	"rune_protection_1": {
		"name": "Rune of Protection I",
		"enchantment": ENCH_PROTECTION,
		"level": 1,
		"inputs": {"wolf_pelt": 1, "herbs": 2, "stone": 2},
		"icon": "🛡️"
	},
	"rune_unbreaking_1": {
		"name": "Rune of Unbreaking I",
		"enchantment": ENCH_UNBREAKING,
		"level": 1,
		"inputs": {"wolf_tooth": 1, "iron_ingots": 1},
		"icon": "💎"
	},
	"rune_power_1": {
		"name": "Rune of Power I",
		"enchantment": ENCH_POWER,
		"level": 1,
		"inputs": {"spider_thread": 1, "blood_vial": 1, "logs": 1},
		"icon": "🏹"
	}
}

static func calculate_melee_damage(base_damage: float, enchantments: Dictionary) -> float:
	var final_damage = base_damage
	if enchantments.has(ENCH_SHARPNESS):
		var level = enchantments[ENCH_SHARPNESS]
		final_damage *= (1.0 + (level * 0.15))
	return final_damage

static func calculate_arrow_damage(base_damage: float, enchantments: Dictionary) -> float:
	var final_damage = base_damage
	if enchantments.has(ENCH_POWER):
		var level = enchantments[ENCH_POWER]
		final_damage *= (1.0 + (level * 0.15))
	return final_damage

static func calculate_armor_mitigation(damage_in: float, enchantments: Dictionary) -> float:
	var mitigation_mult = 1.0
	if enchantments.has(ENCH_PROTECTION):
		var level = enchantments[ENCH_PROTECTION]
		mitigation_mult = maxf(0.2, 1.0 - (level * 0.10))
	return damage_in * mitigation_mult

static func apply_life_steal(damage_dealt: float, enchantments: Dictionary) -> float:
	if enchantments.has(AFFIX_VAMPIRIC_LEECH):
		return damage_dealt * 0.15 # 15% life steal
	return 0.0

static func has_dragons_breath(enchantments: Dictionary) -> bool:
	return enchantments.has(AFFIX_DRAGONS_BREATH)

static func has_thunderstrike(enchantments: Dictionary) -> bool:
	return enchantments.has(AFFIX_THUNDERSTRIKE)

static func has_windstrider(enchantments: Dictionary) -> bool:
	return enchantments.has(AFFIX_WINDSTRIDER)

static func has_fortress_heart(enchantments: Dictionary) -> bool:
	return enchantments.has(AFFIX_FORTRESS_HEART)

func apply_enchantment(item: Dictionary, en_name: String, level: int = 1) -> bool:
	if not item.has("enchantments"):
		item["enchantments"] = {}
	item["enchantments"][en_name] = level
	emit_signal("item_enchanted", item.get("name", "Item"), en_name, level)
	return true
