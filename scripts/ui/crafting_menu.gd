class_name CraftingMenu
extends Control

## Crafting & Workstation GUI Modal.
## Manages recipes for Handcrafting, Carpentry Workbench, Campfire Cooking, and Stockpile Crates.

signal item_crafted(recipe_name: String, result_item: Dictionary)

var player: Player
var supply_chain: SupplyChain
var active_workstation: Workstation = null
var active_caravan: TradeCaravan = null
var active_enchanter: EnchanterTable = null

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
			"name": "Defensive Gate",
			"inputs": {"logs": 4, "iron_ingots": 2},
			"output": {"name": "Defensive Gate", "type": "block", "block_type": 21, "icon": "🚪", "count": 1}
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
		}
	],
	"campfire": [
		{
			"name": "Baked Rations (x2)",
			"inputs": {"wheat": 2},
			"output": {"name": "Ration Bread", "type": "food", "nutrition": 25.0, "icon": "🍞", "count": 2}
		}
	],
	"furnace": [
		{
			"name": "Smelt Iron Ingot",
			"inputs": {"iron_ore": 1, "coal": 1},
			"output": {"name": "Iron Ingot", "type": "material", "icon": "🔩", "count": 1}
		},
		{
			"name": "Smelt Copper Ingot",
			"inputs": {"copper_ore": 1, "coal": 1},
			"output": {"name": "Copper Ingot", "type": "material", "icon": "🪙", "count": 1}
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
		_populate_caravan_trade()
	elif target is EnchanterTable:
		active_caravan = null
		active_workstation = null
		active_enchanter = target
		_populate_enchanter_recipes()
	else:
		active_caravan = null
		active_enchanter = null
		active_workstation = target as Workstation
		_populate_recipes()

func close_menu() -> void:
	is_open = false
	visible = false
	active_workstation = null
	active_caravan = null
	active_enchanter = null
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
