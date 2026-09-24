class_name AlloyManager
extends RefCounted

## Tinkers' Construct Metallurgical Alloying Engine.
## Manages liquid metal properties, melting points, stoichiometries,
## and alloy reactions (Bronze, Steel, Electrum).

const METAL_PROPERTIES: Dictionary = {
	"copper": {
		"name": "Molten Copper",
		"melting_point": 1085.0, # Celsius
		"color": Color(0.9, 0.45, 0.2, 1.0)
	},
	"tin": {
		"name": "Molten Tin",
		"melting_point": 232.0,
		"color": Color(0.75, 0.78, 0.82, 1.0)
	},
	"bronze": {
		"name": "Molten Bronze",
		"melting_point": 950.0,
		"color": Color(0.85, 0.55, 0.15, 1.0)
	},
	"iron": {
		"name": "Molten Iron",
		"melting_point": 1538.0,
		"color": Color(0.85, 0.85, 0.90, 1.0)
	},
	"steel": {
		"name": "Molten Steel",
		"melting_point": 1450.0,
		"color": Color(0.65, 0.70, 0.75, 1.0)
	},
	"gold": {
		"name": "Molten Gold",
		"melting_point": 1064.0,
		"color": Color(1.0, 0.84, 0.0, 1.0)
	},
	"silver": {
		"name": "Molten Silver",
		"melting_point": 961.0,
		"color": Color(0.92, 0.94, 0.96, 1.0)
	},
	"electrum": {
		"name": "Molten Electrum",
		"melting_point": 1000.0,
		"color": Color(0.95, 0.88, 0.45, 1.0)
	}
}

## Check and perform metallurgical alloy reactions inside a molten tank.
## Modifies tank_contents dictionary in-place: { "copper": 3, "tin": 1, ... }
## Returns an array of reaction logs.
static func process_alloys(tank_contents: Dictionary, current_temp: float) -> Array[String]:
	var logs: Array[String] = []

	# 1. Bronze: 3 Copper + 1 Tin -> 4 Bronze (Requires temp >= 950°C)
	if current_temp >= 950.0:
		var cu = tank_contents.get("copper", 0)
		var sn = tank_contents.get("tin", 0)
		if cu >= 3 and sn >= 1:
			var max_batches = min(int(cu / 3), sn)
			if max_batches > 0:
				tank_contents["copper"] -= max_batches * 3
				tank_contents["tin"] -= max_batches * 1
				tank_contents["bronze"] = tank_contents.get("bronze", 0) + (max_batches * 4)
				logs.append("Alloyed %d batches of Bronze (+%d molten bronze)" % [max_batches, max_batches * 4])

	# 2. Steel: 1 Iron + 1 Carbon/Coal -> 1 Steel (Requires temp >= 1450°C)
	if current_temp >= 1450.0:
		var fe = tank_contents.get("iron", 0)
		var carbon = tank_contents.get("carbon", 0)
		if fe >= 1 and carbon >= 1:
			var batches = min(fe, carbon)
			if batches > 0:
				tank_contents["iron"] -= batches
				tank_contents["carbon"] -= batches
				tank_contents["steel"] = tank_contents.get("steel", 0) + batches
				logs.append("Alloyed %d batches of Refined Steel (+%d molten steel)" % [batches, batches])

	# 3. Electrum: 1 Gold + 1 Silver -> 2 Electrum (Requires temp >= 1000°C)
	if current_temp >= 1000.0:
		var au = tank_contents.get("gold", 0)
		var ag = tank_contents.get("silver", 0)
		if au >= 1 and ag >= 1:
			var batches = min(au, ag)
			if batches > 0:
				tank_contents["gold"] -= batches
				tank_contents["silver"] -= batches
				tank_contents["electrum"] = tank_contents.get("electrum", 0) + (batches * 2)
				logs.append("Alloyed %d batches of Royal Electrum (+%d molten electrum)" % [batches, batches * 2])

	# Clean up zero counts
	var keys_to_remove: Array = []
	for k in tank_contents.keys():
		if tank_contents[k] <= 0:
			keys_to_remove.append(k)
	for k in keys_to_remove:
		tank_contents.erase(k)

	return logs

static func get_melting_point(metal_type: String) -> float:
	return METAL_PROPERTIES.get(metal_type, {}).get("melting_point", 1000.0)

static func is_molten(metal_type: String, temp: float) -> bool:
	return temp >= get_melting_point(metal_type)
