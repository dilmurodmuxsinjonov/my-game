class_name Anvil
extends StaticBody3D

## Tinkers' Construct Modular Blacksmith Anvil Workstation.
## Enables players to forge modular tools and weapons from component parts:
## Blades, Crossguards, and Grips, combining material properties into masterwork arms.

signal modular_weapon_forged(weapon_data: Dictionary)

const BLADE_COMPONENTS: Dictionary = {
	"iron": {
		"name": "Forged Iron Blade",
		"damage": 35.0,
		"durability": 120,
		"crit_chance": 0.05,
		"icon": "🗡️",
		"cost": {"iron_ingots": 3}
	},
	"steel": {
		"name": "Tempered Steel Blade",
		"damage": 48.0,
		"durability": 260,
		"crit_chance": 0.18,
		"icon": "⚔️",
		"cost": {"steel_ingot": 2, "coal": 2}
	},
	"gold": {
		"name": "Gilded Ritual Blade",
		"damage": 28.0,
		"durability": 65,
		"crit_chance": 0.25,
		"rune_potency": 1.5,
		"icon": "✨",
		"cost": {"gold_ingot": 2}
	}
}

const GUARD_COMPONENTS: Dictionary = {
	"leather": {
		"name": "Rawhide Crossguard",
		"durability_bonus": 15,
		"defense_parry": 0.05,
		"icon": "🛡️",
		"cost": {"leather": 1}
	},
	"iron": {
		"name": "Reinforced Iron Guard",
		"durability_bonus": 45,
		"defense_parry": 0.15,
		"icon": "🛡️",
		"cost": {"iron_ingots": 1}
	},
	"gold": {
		"name": "Gilded Filigree Guard",
		"durability_bonus": 25,
		"defense_parry": 0.08,
		"rune_slots": 2,
		"icon": "⚜️",
		"cost": {"gold_ingot": 1}
	}
}

const HANDLE_COMPONENTS: Dictionary = {
	"oak": {
		"name": "Turned Oak Grip",
		"stamina_cost_mult": 1.0,
		"swing_speed": 1.0,
		"icon": "🪵",
		"cost": {"logs": 1}
	},
	"hardwood": {
		"name": "Hardwood Heartwood Grip",
		"stamina_cost_mult": 0.85,
		"swing_speed": 1.08,
		"icon": "🪵",
		"cost": {"logs": 2}
	},
	"leather_bound": {
		"name": "Leather-Bound Grip",
		"stamina_cost_mult": 0.90,
		"swing_speed": 1.15,
		"icon": "🪢",
		"cost": {"logs": 1, "leather": 1}
	}
}

var model_instance: Node3D
var collision_box: CollisionShape3D
var prompt_label: Label3D
var spark_light: OmniLight3D

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.2, 1.0, 0.8)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.5, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/anvil.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	spark_light = OmniLight3D.new()
	spark_light.light_color = Color(1.0, 0.6, 0.2)
	spark_light.light_energy = 1.2
	spark_light.omni_range = 3.5
	spark_light.position = Vector3(0, 0.85, 0)
	add_child(spark_light)

	prompt_label = Label3D.new()
	prompt_label.text = "⚒️ Blacksmith's Anvil\n[E] Forge Modular Tinkers' Weapon"
	prompt_label.position = Vector3(0, 1.6, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 26
	prompt_label.modulate = Color(1.0, 0.75, 0.3)
	add_child(prompt_label)

func set_prompt_visible(is_vis: bool) -> void:
	if prompt_label:
		prompt_label.visible = is_vis

static func assemble_modular_weapon(blade_key: String, guard_key: String, handle_key: String) -> Dictionary:
	var blade = BLADE_COMPONENTS.get(blade_key, BLADE_COMPONENTS["iron"])
	var guard = GUARD_COMPONENTS.get(guard_key, GUARD_COMPONENTS["iron"])
	var handle = HANDLE_COMPONENTS.get(handle_key, HANDLE_COMPONENTS["oak"])

	var total_dmg = blade["damage"]
	var total_durability = blade["durability"] + guard["durability_bonus"]
	var crit_rate = blade.get("crit_chance", 0.05)
	var stamina_mult = handle.get("stamina_cost_mult", 1.0)
	var swing_spd = handle.get("swing_speed", 1.0)
	var parry = guard.get("defense_parry", 0.0)

	var weapon_title = "%s %s" % [blade_key.capitalize(), "Broadsword"]
	if handle_key == "leather_bound" or guard_key == "gold":
		weapon_title = "Noble " + weapon_title

	return {
		"name": weapon_title,
		"type": "tool",
		"tool_type": "sword",
		"blade": blade_key,
		"guard": guard_key,
		"handle": handle_key,
		"damage": total_dmg,
		"max_durability": total_durability,
		"durability": total_durability,
		"crit_chance": crit_rate,
		"stamina_cost_mult": stamina_mult,
		"swing_speed": swing_spd,
		"parry_defense": parry,
		"icon": "⚔️",
		"count": 1
	}
