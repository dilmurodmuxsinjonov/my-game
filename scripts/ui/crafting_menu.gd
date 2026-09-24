class_name CraftingMenu
extends Control

const Anvil = preload("res://scripts/world/anvil.gd")

## Crafting & Workstation GUI Modal.
## Manages recipes for Handcrafting, Carpentry Workbench, Campfire Cooking, and Stockpile Crates.

signal item_crafted(recipe_name: String, result_item: Dictionary)

var player: Player
var supply_chain: SupplyChain
var active_workstation: Workstation = null
var active_caravan: TradeCaravan = null
var active_enchanter: EnchanterTable = null
var active_cooking_pot: CookingPot = null
var active_anvil: Node = null

var is_open: bool = false

# UI Elements
var panel: PanelContainer
var header_title: Label
var recipe_list_vbox: VBoxContainer
var status_label: Label

# Canonical recipes per tier
const RECIPES: Dictionary = {
	"handcraft": [
		{
			"name": "Wood Planks (x4)",
			"inputs": {"logs": 1},
			"output": {"name": "Wood Planks", "type": "block", "block_type": 10, "icon": "🪵", "count": 4}
		},
		{
			"name": "Campfire",
			"inputs": {"logs": 2, "stone": 4},
			"output": {"name": "Campfire", "type": "placeable", "icon": "🔥", "count": 1}
		},
		{
			"name": "Wooden Crate",
			"inputs": {"planks": 4},
			"output": {"name": "Wooden Crate", "type": "placeable", "icon": "📦", "count": 1}
		},
		{
			"name": "Wall Torch (x4)",
			"inputs": {"logs": 1, "coal": 1},
			"output": {"name": "Torch", "type": "placeable", "icon": "🕯️", "count": 4}
		},
		{
			"name": "Smelting Furnace",
			"inputs": {"stone": 8},
			"output": {"name": "Smelting Furnace", "type": "placeable", "station_type": 3, "icon": "🌋", "count": 1}
		},
		{
			"name": "Mine Support Beam (x2)",
			"inputs": {"logs": 2, "stone": 1},
			"output": {"name": "Support Beam", "type": "block", "block_type": 17, "icon": "🪵", "count": 2}
		},
		{
			"name": "Wooden Palisade (x4)",
			"inputs": {"logs": 4},
			"output": {"name": "Wooden Palisade", "type": "block", "block_type": 19, "icon": "🪵", "count": 4}
		},
		{
			"name": "Stone Battlement (x4)",
			"inputs": {"stone_bricks": 4},
			"output": {"name": "Stone Battlement", "type": "block", "block_type": 20, "icon": "🧱", "count": 4}
		}
	],
	"workbench": [
		{
			"name": "Iron Pickaxe",
			"inputs": {"iron_ore": 3, "logs": 1},
			"output": {"name": "Iron Pickaxe", "type": "tool", "tool_type": "pickaxe", "icon": "⛏️", "count": 1}
		},
		{
			"name": "Woodcutter's Axe",
			"inputs": {"iron_ore": 2, "logs": 1},
			"output": {"name": "Wood Axe", "type": "tool", "tool_type": "axe", "icon": "🪓", "count": 1}
		},
		{
			"name": "Knight's Sword",
			"inputs": {"iron_ore": 3, "logs": 1},
			"output": {"name": "Knight Sword", "type": "tool", "tool_type": "sword", "icon": "⚔️", "count": 1}
		},
		{
			"name": "Hunting Bow",
			"inputs": {"logs": 3, "fine_fabric": 1},
			"output": {"name": "Hunting Bow", "type": "tool", "tool_type": "bow", "icon": "🏹", "count": 1}
		},
		{
			"name": "Arrow Bundle (x10)",
			"inputs": {"logs": 1, "iron_ingots": 1},
			"output": {"name": "Arrows", "type": "arrow", "icon": "🎯", "count": 10}
		},
		{
			"name": "Defensive Watchtower",
			"inputs": {"logs": 8, "stone_bricks": 4},
			"output": {"name": "Watchtower", "type": "placeable", "icon": "🏰", "count": 1}
		},
		{
			"name": "Arcane Enchanter's Table",
			"inputs": {"stone_bricks": 4, "gems": 1, "logs": 2},
			"output": {"name": "Arcane Enchanter's Table", "type": "placeable", "icon": "🔮", "count": 1}
		},
		{
			"name": "Kinetic Windmill Tower",
			"inputs": {"logs": 12, "stone_bricks": 8, "fine_fabric": 2},
			"output": {"name": "Kinetic Windmill Tower", "type": "placeable", "icon": "⚙️", "count": 1}
		},
		{
			"name": "Cooking Pot & Hearth",
			"inputs": {"iron_ingots": 3, "logs": 2, "stone": 4},
			"output": {"name": "Cooking Pot", "type": "placeable", "icon": "🍲", "count": 1}
		},
		{
			"name": "Royal War Horn",
			"inputs": {"wolf_tooth": 2, "gold_ingot": 1, "logs": 1},
			"output": {"name": "Royal War Horn", "type": "tool", "tool_type": "horn", "icon": "📯", "count": 1}
		},
		{
			"name": "Defensive Gate",
			"inputs": {"logs": 4, "iron_ingots": 2},
			"output": {"name": "Defensive Gate", "type": "block", "block_type": 21, "icon": "🚪", "count": 1}
		},
		{
			"name": "Architect's Drafting Desk",
			"inputs": {"logs": 4, "stone": 2, "planks": 4},
			"output": {"name": "Architect Desk", "type": "placeable", "icon": "📐", "count": 1}
		},
		{
			"name": "Hauler's Wheelbarrow",
			"inputs": {"logs": 3, "iron_ingots": 1},
			"output": {"name": "Hauler's Wheelbarrow", "type": "tool", "tool_type": "wheelbarrow", "icon": "🛒", "count": 1}
		},
		{
			"name": "Worker Cottage Blueprint",
			"inputs": {"logs": 2, "stone": 2},
			"output": {"name": "Worker Cottage Blueprint", "type": "blueprint", "blueprint_id": "cottage", "icon": "🏠", "count": 1}
		},
		{
			"name": "Watchtower Blueprint",
			"inputs": {"logs": 3, "stone": 3},
			"output": {"name": "Watchtower Blueprint", "type": "blueprint", "blueprint_id": "watchtower", "icon": "🏰", "count": 1}
		},
		{
			"name": "Granary Silo Blueprint",
			"inputs": {"logs": 4, "stone": 2},
			"output": {"name": "Granary Silo Blueprint", "type": "blueprint", "blueprint_id": "granary", "icon": "🌾", "count": 1}
		},
		{
			"name": "Farmland Hoe",
			"inputs": {"logs": 2, "stone": 2},
			"output": {"name": "Farmland Hoe", "type": "tool", "tool_type": "hoe", "icon": "🌾", "block_type": 13, "count": 1}
		},
		{
			"name": "Cobblestone Blocks (x8)",
			"inputs": {"stone": 8},
			"output": {"name": "Cobblestone", "type": "block", "block_type": 9, "icon": "🪨", "count": 8}
		},
		{
			"name": "Wheat Seeds (x4)",
			"inputs": {"wheat": 1},
			"output": {"name": "Wheat Seeds", "type": "seed", "icon": "🌱", "count": 4}
		},
		{
			"name": "Blacksmith's Anvil",
			"inputs": {"iron_ingots": 4, "logs": 2},
			"output": {"name": "Blacksmith's Anvil", "type": "placeable", "icon": "⚒️", "count": 1}
		},
		{
			"name": "Timber Smoke Rack",
			"inputs": {"logs": 3},
			"output": {"name": "Timber Smoke Rack", "type": "placeable", "icon": "🍖", "count": 1}
		},
		{
			"name": "Kinetic Water Wheel",
			"inputs": {"logs": 8, "planks": 6, "stone": 4},
			"output": {"name": "Kinetic Water Wheel", "type": "placeable", "icon": "🌊", "count": 1}
		},
		{
			"name": "Mechanical Millstone",
			"inputs": {"stone": 6, "logs": 2, "iron_ingots": 1},
			"output": {"name": "Mechanical Millstone", "type": "placeable", "icon": "⚙️", "count": 1}
		},
		{
			"name": "Industrial Trip Hammer",
			"inputs": {"logs": 6, "stone": 4, "iron_ingots": 3},
			"output": {"name": "Industrial Trip Hammer", "type": "placeable", "icon": "🔨", "count": 1}
		},
		{
			"name": "Organic Compost Bin",
			"inputs": {"logs": 4, "planks": 2},
			"output": {"name": "Compost Bin", "type": "placeable", "icon": "🌱", "count": 1}
		},
		{
			"name": "Butcher's Cutting Board",
			"inputs": {"logs": 2, "iron_ingots": 1},
			"output": {"name": "Cutting Board", "type": "placeable", "icon": "🔪", "count": 1}
		},
		{
			"name": "Geologist's Prospector Pick",
			"inputs": {"logs": 2, "copper_ingot": 2},
			"output": {"name": "Prospector Pick", "type": "tool", "tool_type": "prospector_pick", "icon": "⛏️", "count": 1}
		},
		{
			"name": "Underground Ore Minecart",
			"inputs": {"iron_ingots": 5, "planks": 4},
			"output": {"name": "Mine Cart", "type": "placeable", "icon": "🛒", "count": 1}
		},
		{
			"name": "Mining Rail Tracks (x16)",
			"inputs": {"iron_ingots": 6, "planks": 1},
			"output": {"name": "Mining Rail", "type": "block", "block_type": 24, "icon": "🛤️", "count": 16}
		},
		{
			"name": "Lapidary Gem Cutting Table",
			"inputs": {"planks": 4, "iron_ingots": 2, "stone": 1},
			"output": {"name": "Gem Cutting Table", "type": "placeable", "icon": "💎", "count": 1}
		},
		{
			"name": "Cut Ruby (Crit Damage)",
			"inputs": {"gems": 1},
			"output": {"name": "Cut Ruby", "type": "gem", "gem_id": "ruby", "icon": "🔴", "count": 1}
		},
		{
			"name": "Cut Sapphire (Armor Piercing)",
			"inputs": {"gems": 1},
			"output": {"name": "Cut Sapphire", "type": "gem", "gem_id": "sapphire", "icon": "🔵", "count": 1}
		},
		{
			"name": "Cut Topaz (Stamina Efficiency)",
			"inputs": {"gems": 1},
			"output": {"name": "Cut Topaz", "type": "gem", "gem_id": "topaz", "icon": "🟡", "count": 1}
		},
		{
			"name": "Cut Deep Gem (Lifesteal & Regen)",
			"inputs": {"gems": 1},
			"output": {"name": "Cut Deep Gem", "type": "gem", "gem_id": "deep_gem", "icon": "💎", "count": 1}
		}
	],
	"campfire": [
		{
			"name": "Baked Rations (x2)",
			"inputs": {"wheat": 2},
			"output": {"name": "Ration Bread", "type": "food", "nutrition": 25.0, "icon": "🍞", "count": 2}
		},
		{
			"name": "Oak-Smoked Meat",
			"inputs": {"meat": 1, "logs": 1},
			"output": {"name": "Oak-Smoked Meat", "type": "food", "nutrition": 40.0, "warmth_bonus": 15.0, "icon": "🍖", "count": 1}
		},
		{
			"name": "Salt-Cured Meat",
			"inputs": {"meat": 1, "rock_salt": 1},
			"output": {"name": "Salt-Cured Meat", "type": "food", "nutrition": 45.0, "warmth_bonus": 10.0, "icon": "🥓", "count": 1}
		},
		{
			"name": "Rich Cabbage & Beef Stew (x2)",
			"inputs": {"sliced_cabbage": 1, "minced_beef": 1, "diced_onion": 1},
			"output": {"name": "Rich Cabbage Stew", "type": "food", "nutrition": 50.0, "warmth_bonus": 25.0, "icon": "🍲", "count": 2}
		},
		{
			"name": "Monarch's Shepherd Pie (x2)",
			"inputs": {"minced_beef": 1, "diced_onion": 1, "bread": 1},
			"output": {"name": "Shepherd's Pie", "type": "food", "nutrition": 65.0, "warmth_bonus": 30.0, "icon": "🥧", "count": 2}
		}
	],
	"furnace": [
		{
			"name": "Smelt Iron Ingot",
			"inputs": {"iron_ore": 1, "coal": 1},
			"output": {"name": "Iron Ingot", "type": "material", "icon": "🔩", "count": 1}
		},
		{
			"name": "Smelt Crushed Iron (x2 Yield)",
			"inputs": {"crushed_iron": 1, "coal": 1},
			"output": {"name": "Iron Ingot", "type": "material", "icon": "🔩", "count": 2}
		},
		{
			"name": "Smelt Copper Ingot",
			"inputs": {"copper_ore": 1, "coal": 1},
			"output": {"name": "Copper Ingot", "type": "material", "icon": "🪙", "count": 1}
		},
		{
			"name": "Smelt Crushed Copper (x2 Yield)",
			"inputs": {"crushed_copper": 1, "coal": 1},
			"output": {"name": "Copper Ingot", "type": "material", "icon": "🪙", "count": 2}
		},
		{
			"name": "Smelt Gold Ingot",
			"inputs": {"gold_ore": 1, "coal": 2},
			"output": {"name": "Gold Ingot", "type": "material", "icon": "🧈", "count": 1}
		},
		{
			"name": "Bake Stone Bricks (x4)",
			"inputs": {"stone": 4, "coal": 1},
			"output": {"name": "Stone Bricks", "type": "block", "block_type": 16, "icon": "🧱", "count": 4}
		},
		{
			"name": "Forge Steel Ingot",
			"inputs": {"iron_ore": 2, "coal": 3},
			"output": {"name": "Steel Ingot", "type": "material", "icon": "⚔️", "count": 1}
		},
		{
			"name": "Smelt Silver Ingot",
			"inputs": {"silver_ore": 1, "coal": 1},
			"output": {"name": "Silver Ingot", "type": "material", "icon": "🪙", "count": 1}
		}
	],
	"enchanter": [
		{
			"name": "Rune of Sharpness I",
			"inputs": {"blood_vial": 1, "stone": 2, "flax": 1},
			"output": {"name": "Rune of Sharpness I", "type": "rune", "enchantment": "sharpness", "level": 1, "icon": "🗡️", "count": 1}
		},
		{
			"name": "Rune of Protection I",
			"inputs": {"wolf_pelt": 1, "herbs": 2, "stone": 2},
			"output": {"name": "Rune of Protection I", "type": "rune", "enchantment": "protection", "level": 1, "icon": "🛡️", "count": 1}
		},
		{
			"name": "Rune of Unbreaking I",
			"inputs": {"wolf_tooth": 1, "iron_ingots": 1},
			"output": {"name": "Rune of Unbreaking I", "type": "rune", "enchantment": "unbreaking", "level": 1, "icon": "💎", "count": 1}
		},
		{
			"name": "Rune of Power I",
			"inputs": {"spider_thread": 1, "blood_vial": 1, "logs": 1},
			"output": {"name": "Rune of Power I", "type": "rune", "enchantment": "power", "level": 1, "icon": "🏹", "count": 1}
		}
	],
	"cooking_pot": [
		{
			"name": "Hearty Hunter Stew",
			"inputs": {"meat": 1, "wheat": 2, "herbs": 1},
			"output": {"name": "Hearty Hunter Stew", "type": "food", "nutrition": 60.0, "warmth_bonus": 40.0, "icon": "🍲", "count": 1}
		},
		{
			"name": "Feudal Vegetable Broth",
			"inputs": {"wheat": 2, "herbs": 2},
			"output": {"name": "Vegetable Broth", "type": "food", "nutrition": 35.0, "warmth_bonus": 25.0, "icon": "🥣", "count": 1}
		},
		{
			"name": "Roasted Noble Feast",
			"inputs": {"meat": 2, "bread": 2, "herbs": 2},
			"output": {"name": "Noble Feast", "type": "food", "nutrition": 85.0, "warmth_bonus": 50.0, "icon": "🍖", "count": 1}
		}
	]
}

func _ready() -> void:
	visible = false
	_build_ui()

func _build_ui() -> void:
	anchor_right = 1.0
	anchor_bottom = 1.0
	
	# Dim overlay
	var dim = ColorRect.new()
	dim.color = Color(0, 0, 0, 0.6)
	dim.anchor_right = 1.0
	dim.anchor_bottom = 1.0
	add_child(dim)
	
	# Modal Box
	panel = PanelContainer.new()
	panel.anchor_left = 0.5
	panel.anchor_top = 0.5
	panel.anchor_right = 0.5
	panel.anchor_bottom = 0.5
	panel.offset_left = -280.0
	panel.offset_top = -220.0
	panel.offset_right = 280.0
	panel.offset_bottom = 220.0
	
	var sb = StyleBoxFlat.new()
	sb.bg_color = Color(0.14, 0.16, 0.20, 0.95)
	sb.border_width_left = 2
	sb.border_width_top = 2
	sb.border_width_right = 2
	sb.border_width_bottom = 2
	sb.border_color = Color(0.85, 0.65, 0.25)
	sb.corner_radius_top_left = 8
	sb.corner_radius_top_right = 8
	sb.corner_radius_bottom_left = 8
	sb.corner_radius_bottom_right = 8
	panel.add_theme_stylebox_override("panel", sb)
	add_child(panel)
	
	var margin = MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_bottom", 16)
	panel.add_child(margin)
	
	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 12)
	margin.add_child(main_vbox)
	
	header_title = Label.new()
	header_title.text = "🛠️ FEUDAL WORKBENCH & CRAFTING"
	header_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	header_title.add_theme_font_size_override("font_size", 18)
	main_vbox.add_child(header_title)
	
	var tab_bar = HBoxContainer.new()
	tab_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	tab_bar.add_theme_constant_override("separation", 10)
	main_vbox.add_child(tab_bar)
	
	var btn_recipes = Button.new()
	btn_recipes.text = " 🛠️ Workshop Recipes "
	btn_recipes.pressed.connect(_on_tab_recipes_pressed)
	tab_bar.add_child(btn_recipes)
	
	var btn_quotas = Button.new()
	btn_quotas.text = " 📊 Production Quotas ('Do Until X') "
	btn_quotas.pressed.connect(_populate_quotas)
	tab_bar.add_child(btn_quotas)
	
	var scroll = ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_vbox.add_child(scroll)
	
	recipe_list_vbox = VBoxContainer.new()
	recipe_list_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	recipe_list_vbox.add_theme_constant_override("separation", 8)
	scroll.add_child(recipe_list_vbox)
	
	status_label = Label.new()
	status_label.text = "Select a blueprint to craft."
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status_label.modulate = Color(0.8, 0.8, 0.8)
	main_vbox.add_child(status_label)
	
	var hint = Label.new()
	hint.text = "[Press E, C or ESC to Close]"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.modulate = Color(0.6, 0.6, 0.6)
	main_vbox.add_child(hint)

func open_menu(target: Node = null) -> void:
	is_open = true
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	
	if target is TradeCaravan:
		active_caravan = target
		active_workstation = null
		active_enchanter = null
		active_cooking_pot = null
		_populate_caravan_trade()
	elif target is EnchanterTable:
		active_caravan = null
		active_workstation = null
		active_cooking_pot = null
		active_enchanter = target
		_populate_enchanter_recipes()
	elif target is CookingPot:
		active_caravan = null
		active_workstation = null
		active_enchanter = null
		active_anvil = null
		active_cooking_pot = target
		_populate_cooking_recipes()
	elif target is Anvil:
		active_caravan = null
		active_workstation = null
		active_enchanter = null
		active_cooking_pot = null
		active_anvil = target
		_populate_anvil_forging()
	else:
		active_caravan = null
		active_enchanter = null
		active_cooking_pot = null
		active_anvil = null
		active_workstation = target as Workstation
		_populate_recipes()

func close_menu() -> void:
	is_open = false
	visible = false
	active_workstation = null
	active_caravan = null
	active_enchanter = null
	active_cooking_pot = null
	active_anvil = null
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_C or event.keycode == KEY_ESCAPE:
			if is_open:
				close_menu()
			elif event.keycode == KEY_C:
				open_menu(null)
		elif event.keycode == KEY_E and is_open:
			close_menu()

func _on_tab_recipes_pressed() -> void:
	if active_enchanter:
		_populate_enchanter_recipes()
	elif active_cooking_pot:
		_populate_cooking_recipes()
	elif active_anvil:
		_populate_anvil_forging()
	elif active_caravan:
		_populate_caravan_trade()
	else:
		_populate_recipes()

func _populate_quotas() -> void:
	for child in recipe_list_vbox.get_children():
		child.queue_free()
		
	header_title.text = "📊 ROYAL PRODUCTION QUOTAS ('DO UNTIL X')"
	status_label.text = "RimWorld-style quotas: Workers pause production when stock limits are met."
	
	if not supply_chain:
		var err = Label.new()
		err.text = "Error: Supply chain not linked!"
		recipe_list_vbox.add_child(err)
		return
		
	var tracked_items = ["bread", "tools", "weapons", "iron_ingots"]
	for item in tracked_items:
		var row = HBoxContainer.new()
		row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		
		# Name & Current Stock
		var name_lbl = Label.new()
		var cur_stock = supply_chain.get_resource(item)
		name_lbl.text = "• %s (Current: %d)" % [item.capitalize(), cur_stock]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		
		# Quota Mode Button
		var cur_mode = supply_chain.get_quota_mode(item)
		var mode_btn = Button.new()
		mode_btn.text = " Mode: %s " % _get_quota_mode_label(cur_mode)
		mode_btn.pressed.connect(_cycle_quota_mode.bind(item))
		row.add_child(mode_btn)
		
		# Decrement Button
		var dec_btn = Button.new()
		dec_btn.text = " -5 "
		dec_btn.pressed.connect(_adjust_quota.bind(item, -5))
		row.add_child(dec_btn)
		
		# Target Limit Label
		var target_lbl = Label.new()
		var cur_quota = supply_chain.get_quota(item)
		target_lbl.text = " Target: %d " % cur_quota
		target_lbl.modulate = Color(1.0, 0.85, 0.4)
		row.add_child(target_lbl)
		
		# Increment Button
		var inc_btn = Button.new()
		inc_btn.text = " +5 "
		inc_btn.pressed.connect(_adjust_quota.bind(item, 5))
		row.add_child(inc_btn)
		
		recipe_list_vbox.add_child(row)

func _get_quota_mode_label(m: int) -> String:
	match m:
		SupplyChain.QuotaMode.DO_FOREVER: return "DO FOREVER"
		SupplyChain.QuotaMode.DO_UNTIL_X: return "DO UNTIL X"
		SupplyChain.QuotaMode.PAUSED: return "PAUSED"
		_: return "UNKNOWN"

func _cycle_quota_mode(item: String) -> void:
	if not supply_chain:
		return
	var cur = supply_chain.get_quota_mode(item)
	var next_mode = (cur + 1) % 3
	var cur_limit = supply_chain.get_quota(item)
	supply_chain.set_quota(item, cur_limit, next_mode)
	_populate_quotas()

func _adjust_quota(item: String, delta: int) -> void:
	if not supply_chain:
		return
	var cur_mode = supply_chain.get_quota_mode(item)
	var cur_limit = supply_chain.get_quota(item)
	var new_limit = maxi(0, cur_limit + delta)
	supply_chain.set_quota(item, new_limit, cur_mode)
	_populate_quotas()

var selected_blade: String = "iron"
var selected_guard: String = "iron"
var selected_handle: String = "oak"

func _populate_anvil_forging() -> void:
	for child in recipe_list_vbox.get_children():
		child.queue_free()

	header_title.text = "⚒️ TINKERS' MODULAR BLACKSMITH ANVIL"
	status_label.text = "Select components to assemble a custom modular blade."

	var preview_data = Anvil.assemble_modular_weapon(selected_blade, selected_guard, selected_handle)

	# 1. Blade Selection Row
	var blade_row = HBoxContainer.new()
	blade_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var b_lbl = Label.new()
	b_lbl.text = "Blade Component:"
	b_lbl.custom_minimum_size = Vector2(160, 0)
	blade_row.add_child(b_lbl)

	for b_key in Anvil.BLADE_COMPONENTS.keys():
		var btn = Button.new()
		var b_info = Anvil.BLADE_COMPONENTS[b_key]
		btn.text = "%s %s" % [b_info.get("icon", "🗡️"), b_info["name"]]
		btn.pressed.connect(_on_select_blade.bind(b_key))
		if b_key == selected_blade:
			btn.modulate = Color(1.0, 0.9, 0.4)
		blade_row.add_child(btn)
	recipe_list_vbox.add_child(blade_row)

	# 2. Guard Selection Row
	var guard_row = HBoxContainer.new()
	guard_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var g_lbl = Label.new()
	g_lbl.text = "Crossguard Component:"
	g_lbl.custom_minimum_size = Vector2(160, 0)
	guard_row.add_child(g_lbl)

	for g_key in Anvil.GUARD_COMPONENTS.keys():
		var btn = Button.new()
		var g_info = Anvil.GUARD_COMPONENTS[g_key]
		btn.text = "%s %s" % [g_info.get("icon", "🛡️"), g_info["name"]]
		btn.pressed.connect(_on_select_guard.bind(g_key))
		if g_key == selected_guard:
			btn.modulate = Color(1.0, 0.9, 0.4)
		guard_row.add_child(btn)
	recipe_list_vbox.add_child(guard_row)

	# 3. Handle Selection Row
	var handle_row = HBoxContainer.new()
	handle_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var h_lbl = Label.new()
	h_lbl.text = "Grip & Handle:"
	h_lbl.custom_minimum_size = Vector2(160, 0)
	handle_row.add_child(h_lbl)

	for h_key in Anvil.HANDLE_COMPONENTS.keys():
		var btn = Button.new()
		var h_info = Anvil.HANDLE_COMPONENTS[h_key]
		btn.text = "%s %s" % [h_info.get("icon", "🪵"), h_info["name"]]
		btn.pressed.connect(_on_select_handle.bind(h_key))
		if h_key == selected_handle:
			btn.modulate = Color(1.0, 0.9, 0.4)
		handle_row.add_child(btn)
	recipe_list_vbox.add_child(handle_row)

	# 4. Assembled Weapon Stats Summary Box
	var stat_panel = PanelContainer.new()
	var stat_margin = MarginContainer.new()
	stat_margin.add_theme_constant_override("margin_left", 12)
	stat_margin.add_theme_constant_override("margin_right", 12)
	stat_margin.add_theme_constant_override("margin_top", 8)
	stat_margin.add_theme_constant_override("margin_bottom", 8)
	stat_panel.add_child(stat_margin)

	var stat_vbox = VBoxContainer.new()
	stat_margin.add_child(stat_vbox)

	var title_lbl = Label.new()
	title_lbl.text = "⚔️ %s" % preview_data["name"]
	title_lbl.add_theme_font_size_override("font_size", 16)
	title_lbl.modulate = Color(1.0, 0.85, 0.3)
	stat_vbox.add_child(title_lbl)

	var stat_lbl = Label.new()
	stat_lbl.text = "Damage: %.1f | Max Durability: %d | Crit: %d%% | Stamina Mult: %.2fx | Parry: %d%%" % [
		preview_data["damage"],
		preview_data["max_durability"],
		int(preview_data["crit_chance"] * 100),
		preview_data["stamina_cost_mult"],
		int(preview_data["parry_defense"] * 100)
	]
	stat_lbl.modulate = Color(0.9, 0.95, 1.0)
	stat_vbox.add_child(stat_lbl)

	# Calculate total component costs
	var total_cost: Dictionary = {}
	var b_cost = Anvil.BLADE_COMPONENTS[selected_blade]["cost"]
	var g_cost = Anvil.GUARD_COMPONENTS[selected_guard]["cost"]
	var h_cost = Anvil.HANDLE_COMPONENTS[selected_handle]["cost"]
	for d in [b_cost, g_cost, h_cost]:
		for mat in d.keys():
			total_cost[mat] = total_cost.get(mat, 0) + d[mat]

	var cost_text = "Required Material Costs: "
	for mat in total_cost.keys():
		var avail = supply_chain.get_resource(mat) if supply_chain else 0
		cost_text += "%s: %d/%d  " % [mat.capitalize(), avail, total_cost[mat]]
	var cost_lbl = Label.new()
	cost_lbl.text = cost_text
	cost_lbl.modulate = Color(0.8, 0.8, 0.8)
	stat_vbox.add_child(cost_lbl)

	recipe_list_vbox.add_child(stat_panel)

	# 5. Strike Anvil / Forge Button
	var forge_btn = Button.new()
	forge_btn.text = " ⚒️ Strike Anvil & Quench Modular Weapon ⚒️ "
	forge_btn.add_theme_font_size_override("font_size", 16)
	forge_btn.pressed.connect(_on_forge_modular_weapon_pressed.bind(preview_data, total_cost))
	recipe_list_vbox.add_child(forge_btn)

func _on_select_blade(k: String) -> void:
	selected_blade = k
	_populate_anvil_forging()

func _on_select_guard(k: String) -> void:
	selected_guard = k
	_populate_anvil_forging()

func _on_select_handle(k: String) -> void:
	selected_handle = k
	_populate_anvil_forging()

func _on_forge_modular_weapon_pressed(weapon_data: Dictionary, total_cost: Dictionary) -> void:
	if not supply_chain:
		status_label.text = "Error: Supply chain not connected!"
		return

	for mat in total_cost.keys():
		if supply_chain.get_resource(mat) < total_cost[mat]:
			status_label.text = "Missing materials! Need more %s!" % mat.capitalize()
			return

	for mat in total_cost.keys():
		supply_chain.consume_resource(mat, total_cost[mat])

	if player:
		_add_to_player_hotbar(weapon_data)

	status_label.text = "Masterwork Forged: %s!" % weapon_data["name"]
	emit_signal("item_crafted", weapon_data["name"], weapon_data)
	_populate_anvil_forging()

func _populate_cooking_recipes() -> void:
	for child in recipe_list_vbox.get_children():
		child.queue_free()
		
	header_title.text = "🍲 FEUDAL HEARTH & COOKING POT"
	var recipes = RECIPES.get("cooking_pot", [])
	for recipe in recipes:
		var row = HBoxContainer.new()
		row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		
		var name_lbl = Label.new()
		name_lbl.text = "%s %s" % [recipe["output"].get("icon", "🍲"), recipe["name"]]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		
		var req_text = "Cost: "
		for mat in recipe["inputs"].keys():
			var count = recipe["inputs"][mat]
			var avail = supply_chain.inventory.get(mat, 0) if supply_chain else 0
			req_text += "%s: %d/%d  " % [mat, avail, count]
		var cost_lbl = Label.new()
		cost_lbl.text = req_text
		cost_lbl.modulate = Color(1.0, 0.8, 0.5)
		row.add_child(cost_lbl)
		
		var btn = Button.new()
		btn.text = " Simmer Meal "
		btn.pressed.connect(_on_craft_pressed.bind(recipe))
		row.add_child(btn)
		
		recipe_list_vbox.add_child(row)

func _populate_enchanter_recipes() -> void:
	for child in recipe_list_vbox.get_children():
		child.queue_free()
		
	header_title.text = "🔮 ARCANE ENCHANTER'S TABLE"
	var recipes = RECIPES.get("enchanter", [])
	for recipe in recipes:
		var row = HBoxContainer.new()
		row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		
		var name_lbl = Label.new()
		name_lbl.text = "%s %s" % [recipe["output"].get("icon", "🔮"), recipe["name"]]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		
		var req_text = "Cost: "
		for mat in recipe["inputs"].keys():
			var count = recipe["inputs"][mat]
			var avail = supply_chain.inventory.get(mat, 0) if supply_chain else 0
			req_text += "%s: %d/%d  " % [mat, avail, count]
		var cost_lbl = Label.new()
		cost_lbl.text = req_text
		cost_lbl.modulate = Color(0.75, 0.85, 1.0)
		row.add_child(cost_lbl)
		
		var btn = Button.new()
		btn.text = " Inscribe Rune "
		btn.pressed.connect(_on_craft_pressed.bind(recipe))
		row.add_child(btn)
		
		recipe_list_vbox.add_child(row)

func _populate_recipes() -> void:
	# Clear previous recipes
	for child in recipe_list_vbox.get_children():
		child.queue_free()
		
	var category = "handcraft"
	if active_workstation:
		match active_workstation.station_type:
			Workstation.StationType.WORKBENCH:
				category = "workbench"
				header_title.text = "🪚 CARPENTRY WORKBENCH"
			Workstation.StationType.CAMPFIRE:
				category = "campfire"
				header_title.text = "🔥 SETTLEMENT CAMPFIRE"
			Workstation.StationType.FURNACE:
				category = "furnace"
				header_title.text = "🌋 STONE BLOOMERY FURNACE"
			Workstation.StationType.CRATE:
				header_title.text = "📦 ROYAL STOCKPILE CRATE"
				_populate_crate_storage()
				return
	else:
		header_title.text = "🖐️ HANDCRAFTING BLUEPRINTS"
		
	var recipes = RECIPES.get(category, [])
	for recipe in recipes:
		var row = HBoxContainer.new()
		row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		
		# Recipe Name
		var name_lbl = Label.new()
		name_lbl.text = "%s %s" % [recipe["output"].get("icon", "📦"), recipe["name"]]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		
		# Required materials
		var req_text = "Cost: "
		for mat in recipe["inputs"].keys():
			req_text += "%d %s " % [recipe["inputs"][mat], mat]
		var req_lbl = Label.new()
		req_lbl.text = req_text
		req_lbl.modulate = Color(0.8, 0.75, 0.6)
		row.add_child(req_lbl)
		
		# Craft Button
		var craft_btn = Button.new()
		craft_btn.text = " Craft "
		craft_btn.pressed.connect(_on_craft_pressed.bind(recipe))
		row.add_child(craft_btn)
		
		recipe_list_vbox.add_child(row)

func _populate_crate_storage() -> void:
	if not supply_chain:
		return
	var info = Label.new()
	info.text = "Kingdom Stockpile quick storage. Mined resources automatically synchronize with this stockpile."
	info.autowrap_mode = TextServer.AUTOWRAP_WORD
	recipe_list_vbox.add_child(info)
	
	for item in supply_chain.inventory.keys():
		var row = HBoxContainer.new()
		var lbl = Label.new()
		lbl.text = "• %s: %d" % [item.capitalize(), supply_chain.inventory[item]]
		lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(lbl)
		
		var take_btn = Button.new()
		take_btn.text = " Withdraw 5 "
		take_btn.pressed.connect(_withdraw_from_stockpile.bind(item, 5))
		row.add_child(take_btn)
		recipe_list_vbox.add_child(row)

func _withdraw_from_stockpile(item: String, amount: int) -> void:
	if supply_chain and supply_chain.consume_resource(item, amount):
		status_label.text = "Withdrew %d %s from royal stockpile." % [amount, item]
		_populate_crate_storage()

func _on_craft_pressed(recipe: Dictionary) -> void:
	if not supply_chain:
		status_label.text = "Error: Supply chain not linked!"
		return
		
	# Check materials in stockpile
	var can_afford: bool = true
	for mat in recipe["inputs"].keys():
		var needed = recipe["inputs"][mat]
		var available = supply_chain.inventory.get(mat, 0)
		if available < needed:
			can_afford = false
			status_label.text = "Need %d more %s!" % [needed - available, mat]
			break
			
	if not can_afford:
		return
		
	# Deduct materials
	for mat in recipe["inputs"].keys():
		supply_chain.consume_resource(mat, recipe["inputs"][mat])
		
	# Add crafted item to player hotbar or inscribe if rune
	var out_item = recipe["output"].duplicate()
	if player:
		if out_item.get("type") == "rune":
			var cur_item = player.hotbar[player.active_slot]
			if cur_item.get("type") in ["tool", "weapon", "bow"] or cur_item.get("tool_type") in ["sword", "axe", "pickaxe", "bow"]:
				if not cur_item.has("enchantments"):
					cur_item["enchantments"] = {}
				cur_item["enchantments"][out_item["enchantment"]] = out_item["level"]
				player.emit_signal("hotbar_slot_changed", player.active_slot, cur_item)
				status_label.text = "Inscribed %s onto %s!" % [out_item["name"], cur_item.get("name", "Tool")]
				emit_signal("item_crafted", recipe["name"], out_item)
				if active_enchanter:
					_populate_enchanter_recipes()
				return
		_add_to_player_hotbar(out_item)
		
	status_label.text = "Crafted: %s!" % recipe["name"]
	emit_signal("item_crafted", recipe["name"], out_item)
	if active_enchanter:
		_populate_enchanter_recipes()
	elif active_cooking_pot:
		_populate_cooking_recipes()
	elif active_workstation:
		_populate_recipes()

func _add_to_player_hotbar(item: Dictionary) -> void:
	# Try stack with existing slot
	for slot in player.hotbar:
		if slot.get("name") == item.get("name") and slot.get("type") == item.get("type"):
			slot["count"] = slot.get("count", 0) + item.get("count", 1)
			player.emit_signal("hotbar_slot_changed", player.active_slot, player.hotbar[player.active_slot])
			return
			
	# Place in active slot or first empty
	player.hotbar[player.active_slot] = item
	player.emit_signal("hotbar_slot_changed", player.active_slot, item)

func _populate_caravan_trade() -> void:
	for child in recipe_list_vbox.get_children():
		child.queue_free()
		
	if not active_caravan or not supply_chain:
		return
		
	header_title.text = "🐪 FEUDAL TRADE CARAVAN"
	var coins = supply_chain.inventory.get("coins", 0)
	status_label.text = "Royal Treasury: %d Gold Coins" % coins
	
	# Section 1: Buy Exotic Goods
	var sec1 = Label.new()
	sec1.text = "--- EXOTIC WARES TO BUY ---"
	sec1.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sec1.modulate = Color(1.0, 0.85, 0.4)
	recipe_list_vbox.add_child(sec1)
	
	for item_key in active_caravan.wares.keys():
		var ware = active_caravan.wares[item_key]
		var row = HBoxContainer.new()
		row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		
		var name_lbl = Label.new()
		name_lbl.text = "%s %s (Stock: %d)" % [ware.get("icon", "📦"), item_key.capitalize(), ware["stock"]]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		
		var price_lbl = Label.new()
		price_lbl.text = "%d Coins" % ware["price"]
		price_lbl.modulate = Color(1.0, 0.85, 0.3)
		row.add_child(price_lbl)
		
		var buy_btn = Button.new()
		buy_btn.text = " Buy 1 "
		buy_btn.disabled = ware["stock"] <= 0 or coins < ware["price"]
		buy_btn.pressed.connect(_on_caravan_buy.bind(item_key))
		row.add_child(buy_btn)
		
		recipe_list_vbox.add_child(row)
		
	# Section 2: Sell Realm Surplus
	var sec2 = Label.new()
	sec2.text = "--- SELL REALM COMMODITIES (Earn Coins) ---"
	sec2.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sec2.modulate = Color(0.6, 0.85, 1.0)
	recipe_list_vbox.add_child(sec2)
	
	for item_key in active_caravan.purchase_rates.keys():
		var rate = active_caravan.purchase_rates[item_key]
		var available = supply_chain.inventory.get(item_key, 0)
		var row = HBoxContainer.new()
		row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		
		var name_lbl = Label.new()
		name_lbl.text = "• %s (Stored: %d)" % [item_key.capitalize(), available]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		
		var rate_lbl = Label.new()
		rate_lbl.text = "+%d Coins each" % rate
		rate_lbl.modulate = Color(0.4, 0.9, 0.4)
		row.add_child(rate_lbl)
		
		var sell_btn = Button.new()
		sell_btn.text = " Sell 5 "
		sell_btn.disabled = available < 5
		sell_btn.pressed.connect(_on_caravan_sell.bind(item_key, 5))
		row.add_child(sell_btn)
		
		recipe_list_vbox.add_child(row)

func _on_caravan_buy(item_key: String) -> void:
	if active_caravan and active_caravan.buy_item(item_key, supply_chain):
		status_label.text = "Purchased 1 %s from Trade Caravan!" % item_key.capitalize()
		_populate_caravan_trade()

func _on_caravan_sell(item_key: String, amount: int) -> void:
	if active_caravan and active_caravan.sell_resource(item_key, amount, supply_chain):
		status_label.text = "Sold %d %s for coins!" % [amount, item_key.capitalize()]
		_populate_caravan_trade()
