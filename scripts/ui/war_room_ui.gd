# scripts/ui/war_room_ui.gd
# Voxel Lord: Feudal Realm - Milestone 49: Royal War Room & Strategic Realm Defense Map UI
# Strategic command interface toggled via 'M' key to manage frontier outposts,
# track invading foreign battalions, muster levies, and trigger boiling pitch defenses.

class_name WarRoomUI
extends Control

signal menu_closed()
signal rally_alarm_requested()

var invasion_manager: ForeignInvasionManager = null
var squadron_command: SquadronCommand = null
var supply_chain: SupplyChain = null

var panel: PanelContainer
var outposts_grid: GridContainer
var battalions_vbox: VBoxContainer
var toast_label: Label

func _ready() -> void:
	visible = false
	_build_ui()

func setup(p_invasion: ForeignInvasionManager, p_squad: SquadronCommand = null, p_supply: SupplyChain = null) -> void:
	invasion_manager = p_invasion
	squadron_command = p_squad
	supply_chain = p_supply

	if invasion_manager:
		invasion_manager.invasion_begun.connect(func(_b, _f, _t): refresh())
		invasion_manager.outpost_attacked.connect(func(_o, _d, _g): refresh())
		invasion_manager.outpost_breached.connect(func(_o): refresh())
		invasion_manager.battalion_routed.connect(func(_b, _c): refresh())
		invasion_manager.pitch_cauldron_ignited.connect(func(_o): refresh())
		invasion_manager.militia_mustered.connect(func(_o, _c): refresh())

	refresh()

func _build_ui() -> void:
	anchors_preset = Control.PRESET_FULL_RECT
	mouse_filter = Control.MOUSE_FILTER_STOP

	var backdrop = ColorRect.new()
	backdrop.anchors_preset = Control.PRESET_FULL_RECT
	backdrop.color = Color(0.05, 0.03, 0.04, 0.88)
	add_child(backdrop)

	panel = PanelContainer.new()
	panel.anchors_preset = Control.PRESET_CENTER
	panel.custom_minimum_size = Vector2(880, 600)
	panel.offset_left = -440
	panel.offset_top = -300
	panel.offset_right = 440
	panel.offset_bottom = 300
	add_child(panel)

	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 10)
	panel.add_child(main_vbox)

	# Header Title
	var title = Label.new()
	title.text = "⚔️ ROYAL WAR ROOM & STRATEGIC REALM DEFENSE MAP 🗺️"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	main_vbox.add_child(title)

	var h_split = HBoxContainer.new()
	h_split.size_flags_vertical = Control.SIZE_EXPAND_FILL
	h_split.add_theme_constant_override("separation", 14)
	main_vbox.add_child(h_split)

	# Left Section: 4 Frontier Outposts Fortifications
	var left_vbox = VBoxContainer.new()
	left_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_vbox.add_theme_constant_override("separation", 8)
	h_split.add_child(left_vbox)

	var outposts_hdr = Label.new()
	outposts_hdr.text = "--- FRONTIER OUTPOSTS & CITADEL REDOUBTS ---"
	left_vbox.add_child(outposts_hdr)

	var op_scroll = ScrollContainer.new()
	op_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	left_vbox.add_child(op_scroll)

	outposts_grid = GridContainer.new()
	outposts_grid.columns = 2
	outposts_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	outposts_grid.add_theme_constant_override("h_separation", 10)
	outposts_grid.add_theme_constant_override("v_separation", 10)
	op_scroll.add_child(outposts_grid)

	# Right Section: Hostile Marching Battalions & Invasions Ticker
	var right_vbox = VBoxContainer.new()
	right_vbox.custom_minimum_size = Vector2(300, 0)
	right_vbox.add_theme_constant_override("separation", 8)
	h_split.add_child(right_vbox)

	var bat_hdr = Label.new()
	bat_hdr.text = "--- INVASION BATTALIONS ---"
	right_vbox.add_child(bat_hdr)

	var bat_scroll = ScrollContainer.new()
	bat_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	right_vbox.add_child(bat_scroll)

	battalions_vbox = VBoxContainer.new()
	battalions_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	battalions_vbox.add_theme_constant_override("separation", 8)
	bat_scroll.add_child(battalions_vbox)

	# Footer
	var footer_hbox = HBoxContainer.new()
	main_vbox.add_child(footer_hbox)

	toast_label = Label.new()
	toast_label.text = "War Room Online. Press 'M' or 'ESC' to return to monarch view."
	toast_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	footer_hbox.add_child(toast_label)

	var alarm_btn = Button.new()
	alarm_btn.text = "📯 General War Alarm"
	alarm_btn.pressed.connect(func():
		emit_signal("rally_alarm_requested")
		_toast("GENERAL WAR ALARM SOUNDED ACROSS ALL DISTRICTS!")
	)
	footer_hbox.add_child(alarm_btn)

	var close_btn = Button.new()
	close_btn.text = "Close War Room (ESC)"
	close_btn.pressed.connect(close_war_room)
	footer_hbox.add_child(close_btn)

func toggle_war_room() -> void:
	if visible:
		close_war_room()
	else:
		open_war_room()

func open_war_room() -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	refresh()

func close_war_room() -> void:
	visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	emit_signal("menu_closed")

func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_ESCAPE or event.keycode == KEY_M:
			close_war_room()
			get_viewport().set_input_as_handled()

func refresh() -> void:
	if not invasion_manager:
		return

	# Rebuild Outposts
	for c in outposts_grid.get_children():
		c.queue_free()

	var all_ops = invasion_manager.get_all_outposts()
	for op_id in all_ops.keys():
		var op = all_ops[op_id]
		var card = _build_outpost_card(op_id, op)
		outposts_grid.add_child(card)

	# Rebuild Battalions
	for c in battalions_vbox.get_children():
		c.queue_free()

	var bats = invasion_manager.get_active_battalions()
	if bats.is_empty():
		var empty_lbl = Label.new()
		empty_lbl.text = "No active hostile marching battalions.\nFrontier borders are currently peaceful."
		battalions_vbox.add_child(empty_lbl)
	else:
		for b_id in bats.keys():
			var b = bats[b_id]
			var card = _build_battalion_card(b)
			battalions_vbox.add_child(card)

func _build_outpost_card(op_id: String, op: Dictionary) -> PanelContainer:
	var pc = PanelContainer.new()
	pc.custom_minimum_size = Vector2(260, 200)

	var vb = VBoxContainer.new()
	vb.add_theme_constant_override("separation", 4)
	pc.add_child(vb)

	var name_lbl = Label.new()
	name_lbl.text = "🏰 %s" % op["name"]
	vb.add_child(name_lbl)

	var stat_lbl = Label.new()
	stat_lbl.text = "Status: %s" % op["status"]
	vb.add_child(stat_lbl)

	var hp_bar = ProgressBar.new()
	hp_bar.min_value = 0.0
	hp_bar.max_value = op["max_health"]
	hp_bar.value = op["health"]
	hp_bar.custom_minimum_size = Vector2(200, 14)
	vb.add_child(hp_bar)

	var garr_lbl = Label.new()
	garr_lbl.text = "🛡️ Garrison: %d Guards / Militia" % op["garrison_count"]
	vb.add_child(garr_lbl)

	# Buttons
	var reinforce_btn = Button.new()
	reinforce_btn.text = "🛡️ Dispatch +2 Guards"
	reinforce_btn.pressed.connect(func():
		invasion_manager.assign_guards_to_outpost(op_id, 2)
		_toast("Dispatched 2 Royal Guards to %s!" % op["name"])
	)
	vb.add_child(reinforce_btn)

	var levy_btn = Button.new()
	levy_btn.text = "🌾 Muster Peasant Levy (15 Food)"
	levy_btn.pressed.connect(func():
		var res = invasion_manager.muster_peasant_militia(op_id, supply_chain)
		_toast(res["message"])
	)
	vb.add_child(levy_btn)

	if op.get("has_pitch_cauldron", false):
		if op.get("pitch_ready", false):
			var unleash_btn = Button.new()
			unleash_btn.text = "💥 UNLEASH BOILING PITCH!"
			unleash_btn.pressed.connect(func():
				var res = invasion_manager.unleash_boiling_pitch(op_id)
				_toast("Pitch unleashed! Dealt %.0f burning damage to invaders!" % res["damage"])
			)
			vb.add_child(unleash_btn)
		else:
			var arm_btn = Button.new()
			arm_btn.text = "🔥 Arm Pitch Cauldron (5 Coal)"
			arm_btn.pressed.connect(func():
				var res = invasion_manager.arm_boiling_pitch(op_id, supply_chain)
				_toast(res["message"])
			)
			vb.add_child(arm_btn)

	return pc

func _build_battalion_card(b: Dictionary) -> PanelContainer:
	var pc = PanelContainer.new()
	var vb = VBoxContainer.new()
	vb.add_theme_constant_override("separation", 3)
	pc.add_child(vb)

	var title = Label.new()
	title.text = "⚔️ %s (%s)" % [b["leader"], b["faction_id"].capitalize()]
	vb.add_child(title)

	var info = Label.new()
	info.text = "Troops: %d | Siege: %s" % [b["troop_count"], b["siege_engine"].capitalize()]
	vb.add_child(info)

	var prog_bar = ProgressBar.new()
	prog_bar.min_value = 0.0
	prog_bar.max_value = 1.0
	prog_bar.value = b["progress"]
	prog_bar.custom_minimum_size = Vector2(180, 12)
	vb.add_child(prog_bar)

	var target_lbl = Label.new()
	target_lbl.text = "Target: %s" % b["target_outpost"]
	vb.add_child(target_lbl)

	return pc

func _toast(msg: String) -> void:
	if toast_label:
		toast_label.text = msg
	refresh()
