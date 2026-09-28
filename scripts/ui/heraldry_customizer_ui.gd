# scripts/ui/heraldry_customizer_ui.gd
# Voxel Lord: Feudal Realm - Milestone 46: Royal Heraldry & Castle Decor UI
# Interface for tailoring kingdom crest, tinctures, motto, castle decor, and imperial buffs.

class_name HeraldryCustomizerUI
extends Control

signal menu_closed()

var heraldry: RoyalHeraldry = null
var castle_customizer: CastleCustomizer = null
var supply_chain: SupplyChain = null

var panel: PanelContainer
var title_label: Label
var blazon_label: Label
var emblem_label: Label
var primary_label: Label
var secondary_label: Label
var division_label: Label
var buffs_label: Label
var decor_list_vbox: VBoxContainer

func _ready() -> void:
	visible = false
	_build_ui()

func setup(
	p_heraldry: RoyalHeraldry,
	p_castle: CastleCustomizer,
	p_supply: SupplyChain = null
) -> void:
	heraldry = p_heraldry
	castle_customizer = p_castle
	supply_chain = p_supply
	
	if heraldry:
		heraldry.heraldry_changed.connect(_on_heraldry_changed)
	if castle_customizer:
		castle_customizer.realm_buffs_updated.connect(_on_buffs_updated)
	
	refresh()

func _build_ui() -> void:
	anchors_preset = Control.PRESET_FULL_RECT
	mouse_filter = Control.MOUSE_FILTER_STOP
	
	var backdrop = ColorRect.new()
	backdrop.anchors_preset = Control.PRESET_FULL_RECT
	backdrop.color = Color(0.04, 0.04, 0.06, 0.75)
	add_child(backdrop)
	
	panel = PanelContainer.new()
	panel.anchors_preset = Control.PRESET_CENTER
	panel.custom_minimum_size = Vector2(760, 520)
	panel.offset_left = -380
	panel.offset_top = -260
	panel.offset_right = 380
	panel.offset_bottom = 260
	add_child(panel)
	
	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 12)
	panel.add_child(main_vbox)
	
	# Header
	title_label = Label.new()
	title_label.text = "⚔ ROYAL HERALDRY & IMPERIAL THRONE ROOM ⚔"
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	main_vbox.add_child(title_label)
	
	# Blazon display
	blazon_label = Label.new()
	blazon_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	blazon_label.text = "Loading royal blazon..."
	main_vbox.add_child(blazon_label)
	
	var h_split = HBoxContainer.new()
	h_split.size_flags_vertical = Control.SIZE_EXPAND_FILL
	h_split.add_theme_constant_override("separation", 20)
	main_vbox.add_child(h_split)
	
	# Left: Heraldry customization
	var left_vbox = VBoxContainer.new()
	left_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_vbox.add_theme_constant_override("separation", 8)
	h_split.add_child(left_vbox)
	
	var heraldry_hdr = Label.new()
	heraldry_hdr.text = "--- KINGDOM COAT OF ARMS ---"
	left_vbox.add_child(heraldry_hdr)
	
	# Emblem selector
	var emblem_row = HBoxContainer.new()
	var emb_prev = Button.new()
	emb_prev.text = " < "
	emb_prev.pressed.connect(func(): if heraldry: heraldry.cycle_emblem(false); refresh())
	emblem_row.add_child(emb_prev)
	emblem_label = Label.new()
	emblem_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	emblem_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	emblem_row.add_child(emblem_label)
	var emb_next = Button.new()
	emb_next.text = " > "
	emb_next.pressed.connect(func(): if heraldry: heraldry.cycle_emblem(true); refresh())
	emblem_row.add_child(emb_next)
	left_vbox.add_child(emblem_row)
	
	# Primary tincture selector
	var pri_row = HBoxContainer.new()
	var pri_prev = Button.new()
	pri_prev.text = " < "
	pri_prev.pressed.connect(func(): if heraldry: heraldry.cycle_primary_tincture(false); refresh())
	pri_row.add_child(pri_prev)
	primary_label = Label.new()
	primary_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	primary_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	pri_row.add_child(primary_label)
	var pri_next = Button.new()
	pri_next.text = " > "
	pri_next.pressed.connect(func(): if heraldry: heraldry.cycle_primary_tincture(true); refresh())
	pri_row.add_child(pri_next)
	left_vbox.add_child(pri_row)
	
	# Secondary tincture selector
	var sec_row = HBoxContainer.new()
	var sec_prev = Button.new()
	sec_prev.text = " < "
	sec_prev.pressed.connect(func(): if heraldry: heraldry.cycle_secondary_tincture(false); refresh())
	sec_row.add_child(sec_prev)
	secondary_label = Label.new()
	secondary_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	secondary_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sec_row.add_child(secondary_label)
	var sec_next = Button.new()
	sec_next.text = " > "
	sec_next.pressed.connect(func(): if heraldry: heraldry.cycle_secondary_tincture(true); refresh())
	sec_row.add_child(sec_next)
	left_vbox.add_child(sec_row)
	
	# Division selector
	var div_row = HBoxContainer.new()
	var div_prev = Button.new()
	div_prev.text = " < "
	div_prev.pressed.connect(func(): if heraldry: heraldry.cycle_division(false); refresh())
	div_row.add_child(div_prev)
	division_label = Label.new()
	division_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	division_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	div_row.add_child(division_label)
	var div_next = Button.new()
	div_next.text = " > "
	div_next.pressed.connect(func(): if heraldry: heraldry.cycle_division(true); refresh())
	div_row.add_child(div_next)
	left_vbox.add_child(div_row)
	
	# Active realm buffs summary
	var buffs_hdr = Label.new()
	buffs_hdr.text = "--- IMPERIAL REALM BUFFS ---"
	left_vbox.add_child(buffs_hdr)
	buffs_label = Label.new()
	buffs_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	left_vbox.add_child(buffs_label)
	
	# Right: Castle Furnishings Catalog
	var right_vbox = VBoxContainer.new()
	right_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right_vbox.add_theme_constant_override("separation", 8)
	h_split.add_child(right_vbox)
	
	var decor_hdr = Label.new()
	decor_hdr.text = "--- CASTLE FURNISHINGS ---"
	right_vbox.add_child(decor_hdr)
	
	var scroll = ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	right_vbox.add_child(scroll)
	
	decor_list_vbox = VBoxContainer.new()
	decor_list_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(decor_list_vbox)
	
	# Close button
	var btn_close = Button.new()
	btn_close.text = "Return to Realm (ESC / K)"
	btn_close.pressed.connect(close)
	main_vbox.add_child(btn_close)

func refresh() -> void:
	if heraldry:
		blazon_label.text = heraldry.get_blazon()
		emblem_label.text = "Emblem: " + heraldry.get_emblem_name()
		primary_label.text = "Primary: " + heraldry.get_tincture_name(heraldry.primary_tincture)
		secondary_label.text = "Secondary: " + heraldry.get_tincture_name(heraldry.secondary_tincture)
		division_label.text = "Field: " + heraldry.get_division_name(heraldry.division)
	
	if castle_customizer:
		var buffs = castle_customizer.get_all_active_buffs()
		var buff_lines: Array[String] = []
		buff_lines.append("Castle Prestige: " + str(castle_customizer.get_total_prestige()))
		if buffs.is_empty():
			buff_lines.append("No active furnishings installed.")
		else:
			for k in buffs:
				buff_lines.append("• " + k + ": +" + str(buffs[k]))
		buffs_label.text = "\n".join(buff_lines)
		
		_refresh_decor_list()

func _refresh_decor_list() -> void:
	if not decor_list_vbox or not castle_customizer:
		return
	
	for child in decor_list_vbox.get_children():
		child.queue_free()
	
	var catalog = castle_customizer.get_catalog()
	for decor_id in catalog:
		var item = catalog[decor_id]
		var row = HBoxContainer.new()
		
		var desc_lbl = Label.new()
		desc_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var status_str = "[INSTALLED]" if castle_customizer.is_placed(decor_id) else "[AVAILABLE]"
		desc_lbl.text = item["name"] + " " + status_str + " (Prestige +" + str(item["prestige"]) + ")"
		row.add_child(desc_lbl)
		
		var action_btn = Button.new()
		if castle_customizer.is_placed(decor_id):
			action_btn.text = "Remove"
			action_btn.pressed.connect(func():
				castle_customizer.remove_furnishing(decor_id)
				refresh()
			)
		else:
			action_btn.text = "Install"
			action_btn.pressed.connect(func():
				castle_customizer.place_furnishing(decor_id, Vector3i(32, 10, 32), supply_chain)
				refresh()
			)
		row.add_child(action_btn)
		decor_list_vbox.add_child(row)

func _on_heraldry_changed(_blazon: String, _pri: Color, _sec: Color) -> void:
	refresh()

func _on_buffs_updated(_buffs: Dictionary, _prestige: int) -> void:
	refresh()

func toggle_menu() -> void:
	if visible:
		close()
	else:
		open()

func open() -> void:
	visible = true
	refresh()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func close() -> void:
	visible = false
	menu_closed.emit()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if visible and event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE or event.keycode == KEY_K:
			close()
			get_viewport().set_input_as_handled()
