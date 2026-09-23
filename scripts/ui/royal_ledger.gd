class_name RoyalLedger
extends Control

## Royal Ledger Modal: Kingdom Management Interface.
## Oversees demographic labor distribution, stockpile stockpiles, tax rates, and kingdom morale.

signal role_reassigned(role_name: String, delta: int)
signal tax_rate_changed(new_rate: float)

var supply_chain: SupplyChain

var is_open: bool = false

# UI Elements
var panel: PanelContainer
var title_label: Label
var morale_bar: ProgressBar
var morale_label: Label
var stockpile_label: Label
var role_labels: Dictionary = {}
var tax_slider: HSlider
var tax_label: Label

# Current demographics
var assigned_citizens: Dictionary = {
	"farmer": 2,
	"lumberjack": 2,
	"miner": 1,
	"baker": 1,
	"blacksmith": 0
}
var total_citizens: int = 8

func _ready() -> void:
	visible = false
	_build_ui()
	if supply_chain:
		supply_chain.inventory_updated.connect(_on_inventory_updated)
		supply_chain.morale_updated.connect(_on_morale_updated)

func _build_ui() -> void:
	anchor_right = 1.0
	anchor_bottom = 1.0
	
	# Dim background overlay
	var bg_dim = ColorRect.new()
	bg_dim.color = Color(0.0, 0.0, 0.0, 0.65)
	bg_dim.anchor_right = 1.0
	bg_dim.anchor_bottom = 1.0
	add_child(bg_dim)
	
	# Center Window
	panel = PanelContainer.new()
	panel.anchor_left = 0.5
	panel.anchor_top = 0.5
	panel.anchor_right = 0.5
	panel.anchor_bottom = 0.5
	panel.offset_left = -340.0
	panel.offset_top = -260.0
	panel.offset_right = 340.0
	panel.offset_bottom = 260.0
	
	var sb = StyleBoxFlat.new()
	sb.bg_color = Color(0.12, 0.14, 0.18, 0.95)
	sb.border_width_left = 2
	sb.border_width_top = 2
	sb.border_width_right = 2
	sb.border_width_bottom = 2
	sb.border_color = Color(0.75, 0.6, 0.25)
	sb.corner_radius_top_left = 8
	sb.corner_radius_top_right = 8
	sb.corner_radius_bottom_left = 8
	sb.corner_radius_bottom_right = 8
	panel.add_theme_stylebox_override("panel", sb)
	add_child(panel)
	
	var margin = MarginContainer.new()
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_bottom", 16)
	panel.add_child(margin)
	
	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 12)
	margin.add_child(main_vbox)
	
	# Header
	title_label = Label.new()
	title_label.text = "👑 ROYAL LEDGER OF THE FEUDAL REALM"
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_label.add_theme_font_size_override("font_size", 18)
	main_vbox.add_child(title_label)
	
	# Kingdom Morale Bar
	var morale_hbox = HBoxContainer.new()
	var m_lbl = Label.new()
	m_lbl.text = "Realm Morale: "
	morale_hbox.add_child(m_lbl)
	
	morale_bar = ProgressBar.new()
	morale_bar.custom_minimum_size = Vector2(300, 18)
	morale_bar.value = 75.0
	var sb_mor = StyleBoxFlat.new()
	sb_mor.bg_color = Color(0.2, 0.65, 0.85)
	morale_bar.add_theme_stylebox_override("fill", sb_mor)
	morale_hbox.add_child(morale_bar)
	
	morale_label = Label.new()
	morale_label.text = " 75.0%"
	morale_hbox.add_child(morale_label)
	main_vbox.add_child(morale_hbox)
	
	var hsep1 = HSeparator.new()
	main_vbox.add_child(hsep1)
	
	# Middle Section: 2 Columns (Demographics & Stockpile)
	var columns = HBoxContainer.new()
	columns.add_theme_constant_override("separation", 24)
	columns.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_vbox.add_child(columns)
	
	# Column 1: Demographics / Labor
	var col1 = VBoxContainer.new()
	col1.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	columns.add_child(col1)
	
	var demo_title = Label.new()
	demo_title.text = "👥 Labor Distribution"
	demo_title.add_theme_font_size_override("font_size", 15)
	col1.add_child(demo_title)
	
	for role in ["farmer", "lumberjack", "miner", "baker", "blacksmith"]:
		var row = HBoxContainer.new()
		var r_name = Label.new()
		r_name.text = role.capitalize() + ":"
		r_name.custom_minimum_size = Vector2(90, 0)
		row.add_child(r_name)
		
		var btn_minus = Button.new()
		btn_minus.text = " - "
		btn_minus.pressed.connect(_on_role_btn_pressed.bind(role, -1))
		row.add_child(btn_minus)
		
		var count_lbl = Label.new()
		count_lbl.text = str(assigned_citizens[role])
		count_lbl.custom_minimum_size = Vector2(25, 0)
		count_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		role_labels[role] = count_lbl
		row.add_child(count_lbl)
		
		var btn_plus = Button.new()
		btn_plus.text = " + "
		btn_plus.pressed.connect(_on_role_btn_pressed.bind(role, 1))
		row.add_child(btn_plus)
		
		col1.add_child(row)
		
	# Column 2: Stockpile Inventory
	var col2 = VBoxContainer.new()
	col2.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	columns.add_child(col2)
	
	var stock_title = Label.new()
	stock_title.text = "📦 Royal Stockpile"
	stock_title.add_theme_font_size_override("font_size", 15)
	col2.add_child(stock_title)
	
	stockpile_label = Label.new()
	stockpile_label.text = "Loading stockpiles..."
	stockpile_label.autowrap_mode = TextServer.AUTOWRAP_WORD
	col2.add_child(stockpile_label)
	
	var hsep2 = HSeparator.new()
	main_vbox.add_child(hsep2)
	
	# Tax Slider
	var tax_hbox = HBoxContainer.new()
	var tax_t = Label.new()
	tax_t.text = "Tithe / Tax Rate: "
	tax_hbox.add_child(tax_t)
	
	tax_slider = HSlider.new()
	tax_slider.min_value = 0.0
	tax_slider.max_value = 50.0
	tax_slider.value = 10.0
	tax_slider.custom_minimum_size = Vector2(200, 0)
	tax_slider.value_changed.connect(_on_tax_slider_changed)
	tax_hbox.add_child(tax_slider)
	
	tax_label = Label.new()
	tax_label.text = " 10%"
	tax_hbox.add_child(tax_label)
	main_vbox.add_child(tax_hbox)
	
	# Close hint
	var hint = Label.new()
	hint.text = "[Press TAB or ESC to return to 1st-Person Realm]"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.modulate = Color(0.7, 0.7, 0.7)
	main_vbox.add_child(hint)

func toggle_ledger() -> void:
	is_open = not is_open
	visible = is_open
	if is_open:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		_refresh_display()
	else:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_TAB:
			toggle_ledger()
		elif event.keycode == KEY_ESCAPE and is_open:
			toggle_ledger()

func _on_role_btn_pressed(role: String, delta: int) -> void:
	var cur = assigned_citizens.get(role, 0)
	var new_val = cur + delta
	if new_val >= 0:
		assigned_citizens[role] = new_val
		if role_labels.has(role):
			role_labels[role].text = str(new_val)
		emit_signal("role_reassigned", role, delta)

func _on_tax_slider_changed(val: float) -> void:
	tax_label.text = " %d%%" % int(val)
	if supply_chain:
		supply_chain.tax_rate = val / 100.0
	emit_signal("tax_rate_changed", val / 100.0)

func _refresh_display() -> void:
	if not supply_chain:
		return
		
	# Update morale
	morale_bar.value = supply_chain.morale
	morale_label.text = " %.1f%%" % supply_chain.morale
	
	# Update stockpile text
	var inv_text = ""
	for item in supply_chain.inventory.keys():
		inv_text += "• %s: %d\n" % [item.capitalize(), supply_chain.inventory[item]]
	stockpile_label.text = inv_text

func _on_inventory_updated(_item: String, _amount: int) -> void:
	if is_open:
		_refresh_display()

func _on_morale_updated(new_morale: float) -> void:
	if morale_bar:
		morale_bar.value = new_morale
		morale_label.text = " %.1f%%" % new_morale
