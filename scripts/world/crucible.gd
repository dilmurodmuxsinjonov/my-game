class_name Crucible
extends StaticBody3D

## TerraFirmaCraft-style Refractory Ceramic Crucible & Mold Casting.
## The Crucible is used for melting non-ferrous metals (Copper, Tin, Gold, Silver)
## and combining them into true medieval alloys like Bronze (88% Copper, 12% Tin).
## Once molten, the liquid metal can be poured directly into reusable fired ceramic molds
## (Pickaxe Head Mold, Sword Blade Mold, Axe Head Mold, Ingot Mold) to cast finished metal tool heads!

signal alloy_melted(alloy_name: String, amount: int)
signal tool_cast(tool_type: String, result_item: String)

const MELTING_POINT_COPPER: float = 1085.0 # °C
const MELTING_POINT_TIN: float = 232.0 # °C
const MELTING_POINT_BRONZE: float = 950.0 # °C

var supply_chain: SupplyChain = null
var copper_content: int = 0
var tin_content: int = 0
var molten_bronze: int = 0
var is_heated: bool = true # Placed atop campfire/furnace heat source

var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null
var liquid_light: OmniLight3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.0, 0.9, 1.0)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.45, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/crucible.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	liquid_light = OmniLight3D.new()
	liquid_light.light_color = Color(1.0, 0.6, 0.15)
	liquid_light.light_energy = 1.4
	liquid_light.omni_range = 3.0
	liquid_light.position = Vector3(0, 0.6, 0)
	add_child(liquid_light)

	prompt_label = Label3D.new()
	prompt_label.text = "🏺 TFC Ceramic Crucible\n[E] Add Copper/Tin & Cast Molds"
	prompt_label.position = Vector3(0, 1.25, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 20
	prompt_label.modulate = Color(1.0, 0.7, 0.3)
	add_child(prompt_label)

func add_metals(copper_amt: int, tin_amt: int) -> bool:
	if copper_amt <= 0 and tin_amt <= 0:
		return false
	copper_content += copper_amt
	tin_content += tin_amt
	_check_alloy_reaction()
	_update_prompt()
	return true

func _check_alloy_reaction() -> void:
	var alloy_res = calculate_alloy(copper_content, tin_content)
	if alloy_res["bronze_produced"] > 0:
		molten_bronze += alloy_res["bronze_produced"]
		copper_content = alloy_res["remaining_copper"]
		tin_content = alloy_res["remaining_tin"]
		emit_signal("alloy_melted", "bronze", molten_bronze)

func pour_into_mold(mold_type: String) -> Dictionary:
	var cost_bronze = 1
	if mold_type == "sword_blade":
		cost_bronze = 2
	elif mold_type == "pickaxe_head" or mold_type == "axe_head":
		cost_bronze = 2
	elif mold_type == "ingot":
		cost_bronze = 1

	if molten_bronze < cost_bronze:
		return {
			"success": false,
			"item": "",
			"message": "Insufficient molten bronze (%d/%d needed)." % [molten_bronze, cost_bronze]
		}

	molten_bronze -= cost_bronze
	var cast_res = cast_tool("bronze", mold_type)
	var result_item = cast_res["item_id"]
	
	if supply_chain:
		supply_chain.add_resource(result_item, 1)

	emit_signal("tool_cast", mold_type, result_item)
	_update_prompt()
	return {
		"success": true,
		"item": result_item,
		"name": cast_res["name"],
		"message": "Poured %s into ceramic mold successfully!" % cast_res["name"]
	}

func _update_prompt() -> void:
	if not prompt_label:
		return
	if molten_bronze > 0:
		prompt_label.text = "🏺 TFC Crucible (Molten Bronze: %d)\n[E] Pour into Ceramic Mold\n(Sword / Pickaxe / Axe / Ingot)" % molten_bronze
		prompt_label.modulate = Color(0.4, 0.95, 0.6)
	else:
		prompt_label.text = "🏺 TFC Crucible\nContents: %d Cu | %d Sn\n(Requires 7 Cu + 1 Sn for Bronze)" % [copper_content, tin_content]
		prompt_label.modulate = Color(1.0, 0.7, 0.3)

# --- Static Simulation & Balance Calculations ---

static func calculate_alloy(copper_amt: int, tin_amt: int) -> Dictionary:
	## Authentic TFC Bronze recipe: 7 parts Copper (87.5%) + 1 part Tin (12.5%) = 8 parts Bronze
	var max_batches = mini(copper_amt / 7, tin_amt / 1)
	var bronze_units = max_batches * 8
	var copper_used = max_batches * 7
	var tin_used = max_batches * 1

	return {
		"bronze_produced": bronze_units,
		"copper_consumed": copper_used,
		"tin_consumed": tin_used,
		"remaining_copper": copper_amt - copper_used,
		"remaining_tin": tin_amt - tin_used,
		"ratio_copper_percent": 87.5,
		"ratio_tin_percent": 12.5
	}

static func cast_tool(alloy_type: String, mold_type: String) -> Dictionary:
	var prefix = alloy_type.capitalize()
	match mold_type:
		"sword_blade":
			return {
				"item_id": "cast_bronze_blade",
				"name": "%s Sword Blade" % prefix,
				"durability": 150,
				"damage": 30.0
			}
		"pickaxe_head":
			return {
				"item_id": "cast_bronze_pickaxe",
				"name": "%s Pickaxe" % prefix,
				"durability": 180,
				"mining_speed": 1.4
			}
		"axe_head":
			return {
				"item_id": "cast_bronze_axe",
				"name": "%s Axe" % prefix,
				"durability": 160,
				"chopping_speed": 1.4
			}
		"ingot", _:
			return {
				"item_id": "%s_ingot" % alloy_type.to_lower(),
				"name": "%s Ingot" % prefix,
				"durability": 100,
				"weight": 1.0
			}
