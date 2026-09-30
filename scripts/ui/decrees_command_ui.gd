# scripts/ui/decrees_command_ui.gd
# Voxel Lord: Feudal Realm - Milestone 47: Imperial Decrees & Military Command UI
# Interface for proclaiming royal edicts and issuing tactical garrison squadron orders.

class_name DecreesCommandUI
extends Control

signal menu_closed()
signal rally_requested()

var royal_decrees: RoyalDecrees = null
var squadron_command: SquadronCommand = null
var supply_chain: SupplyChain = null
var quest_manager: QuestManager = null

var panel: PanelContainer
var title_label: Label
var stance_label: Label
var formation_label: Label
var formation_bonus_label: Label
var decrees_list_vbox: VBoxContainer

func _ready() -> void:
	visible = false
	_build_ui()

func setup(
	p_decrees: RoyalDecrees,
	p_squad: SquadronCommand,
	p_supply: SupplyChain = null,
	p_quest: QuestManager = null
) -> void:
	royal_decrees = p_decrees
	squadron_command = p_squad
	supply_chain = p_supply
	quest_manager = p_quest

	if royal_decrees:
		royal_decrees.decree_proclaimed.connect(func(_id, _name): refresh())
		royal_decrees.decree_expired.connect(func(_id, _name): refresh())
	if squadron_command:
		squadron_command.stance_changed.connect(func(_s, _name): refresh())
		squadron_command.formation_changed.connect(func(_f, _name): refresh())
	
	refresh()

func _build_ui() -> void:
	anchors_preset = Control.PRESET_FULL_RECT
	mouse_filter = Control.MOUSE_FILTER_STOP

	var backdrop = ColorRect.new()
	backdrop.anchors_preset = Control.PRESET_FULL_RECT
	backdrop.color = Color(0.03, 0.04, 0.06, 0.80)
	add_child(backdrop)

	panel = PanelContainer.new()
	panel.anchors_preset = Control.PRESET_CENTER
	panel.custom_minimum_size = Vector2(800, 540)
	panel.offset_left = -400
	panel.offset_top = -270
	panel.offset_right = 400
	panel.offset_bottom = 270
	add_child(panel)

	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 10)
	panel.add_child(main_vbox)

	# Header
	title_label = Label.new()
	title_label.text = "👑 IMPERIAL DECREES & GARRISON SQUADRON COMMAND ⚔"
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	main_vbox.add_child(title_label)

	var h_split = HBoxContainer.new()
	h_split.size_flags_vertical = Control.SIZE_EXPAND_FILL
	h_split.add_theme_constant_override("separation", 16)
	main_vbox.add_child(h_split)

	# Left Column: Decrees
	var left_vbox = VBoxContainer.new()
	left_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_vbox.add_theme_constant_override("separation", 8)
	h_split.add_child(left_vbox)

	var decrees_hdr = Label.new()
	decrees_hdr.text = "--- IMPERIAL FEUDAL EDICTS ---"
	left_vbox.add_child(decrees_hdr)

	var scroll = ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	left_vbox.add_child(scroll)

	decrees_list_vbox = VBoxContainer.new()
	decrees_list_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	decrees_list_vbox.add_theme_constant_override("separation", 6)
	scroll.add_child(decrees_list_vbox)

	# Right Column: Squadron Command
	var right_vbox = VBoxContainer.new()
	right_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right_vbox.add_theme_constant_override("separation", 10)
	h_split.add_child(right_vbox)

	var squad_hdr = Label.new()
	squad_hdr.text = "--- GARRISON TACTICAL FORMATIONS ---"
	right_vbox.add_child(squad_hdr)

	# Stance Selector
	var stance_hdr = Label.new()
	stance_hdr.text = "Tactical Stance:"
	right_vbox.add_child(stance_hdr)

	var stance_row = HBoxContainer.new()
	var btn_st_prev = Button.new()
	btn_st_prev.text = " < "
	btn_st_prev.pressed.connect(func(): if squadron_command: squadron_command.cycle_stance(false); refresh())
	stance_row.add_child(btn_st_prev)
	stance_label = Label.new()
	stance_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	stance_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stance_row.add_child(stance_label)
	var btn_st_next = Button.new()
	btn_st_next.text = " > "
	btn_st_next.pressed.connect(func(): if squadron_command: squadron_command.cycle_stance(true); refresh())
	stance_row.add_child(btn_st_next)
	right_vbox.add_child(stance_row)

	# Formation Selector
	var form_hdr = Label.new()
	form_hdr.text = "Military Formation:"
	right_vbox.add_child(form_hdr)

	var form_row = HBoxContainer.new()
	var btn_fm_prev = Button.new()
	btn_fm_prev.text = " < "
	btn_fm_prev.pressed.connect(func(): if squadron_command: squadron_command.cycle_formation(false); refresh())
	form_row.add_child(btn_fm_prev)
	formation_label = Label.new()
	formation_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	formation_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	form_row.add_child(formation_label)
	var btn_fm_next = Button.new()
	btn_fm_next.text = " > "
	btn_fm_next.pressed.connect(func(): if squadron_command: squadron_command.cycle_formation(true); refresh())
	form_row.add_child(btn_fm_next)
	right_vbox.add_child(form_row)

	# Formation Bonuses
	formation_bonus_label = Label.new()
	formation_bonus_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	formation_bonus_label.text = "Formation bonuses active."
	right_vbox.add_child(formation_bonus_label)

	# Rally Garrison Button
	var btn_rally = Button.new()
	btn_rally.text = "📯 Rally Garrison to Monarch Position (H)"
	btn_rally.pressed.connect(func(): rally_requested.emit())
	right_vbox.add_child(btn_rally)

	# Footer / Close
	var btn_close = Button.new()
	btn_close.text = "Return to Realm (ESC / V)"
	btn_close.pressed.connect(close)
	main_vbox.add_child(btn_close)

func refresh() -> void:
	if squadron_command:
		stance_label.text = squadron_command.get_stance_name()
		formation_label.text = squadron_command.get_formation_name()
		var bonuses = squadron_command.get_formation_modifiers()
		var bonus_lines: Array[String] = ["Tactical Formation Modifiers:"]
		for k in bonuses:
			bonus_lines.append("• " + k + ": " + str(bonuses[k]))
		formation_bonus_label.text = "\n".join(bonus_lines)

	_refresh_decrees_list()

func _refresh_decrees_list() -> void:
	if not decrees_list_vbox or not royal_decrees:
		return

	for child in decrees_list_vbox.get_children():
		child.queue_free()

	var catalog = royal_decrees.get_catalog()
	var total_renown = quest_manager.total_renown if quest_manager else 9999

	for dec_id in catalog:
		var dec = catalog[dec_id]
		var card = PanelContainer.new()
		var card_vbox = VBoxContainer.new()
		card_vbox.add_theme_constant_override("separation", 2)
		card.add_child(card_vbox)

		var title_row = HBoxContainer.new()
		var lbl_name = Label.new()
		lbl_name.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var is_active = royal_decrees.is_decree_active(dec_id)
		var status_badge = "[ACTIVE]" if is_active else "[PROCLAIMABLE]"
		lbl_name.text = dec["name"] + " " + status_badge
		title_row.add_child(lbl_name)

		var btn_act = Button.new()
		if is_active:
			btn_act.text = "Revoke"
			btn_act.pressed.connect(func():
				royal_decrees.revoke_decree(dec_id)
				refresh()
			)
		else:
			btn_act.text = "Proclaim"
			btn_act.disabled = not royal_decrees.can_proclaim(dec_id, supply_chain, total_renown)
			btn_act.pressed.connect(func():
				royal_decrees.proclaim_decree(dec_id, supply_chain, total_renown)
				refresh()
			)
		title_row.add_child(btn_act)
		card_vbox.add_child(title_row)

		var lbl_desc = Label.new()
		lbl_desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		lbl_desc.text = dec["description"] + " (Renown: " + str(dec["cost_renown"]) + ", Coins: " + str(dec["cost_coins"]) + ")"
		card_vbox.add_child(lbl_desc)

		decrees_list_vbox.add_child(card)

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
		if event.keycode == KEY_ESCAPE or event.keycode == KEY_V:
			close()
			get_viewport().set_input_as_handled()
