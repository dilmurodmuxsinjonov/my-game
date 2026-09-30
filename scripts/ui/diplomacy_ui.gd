# scripts/ui/diplomacy_ui.gd
# Voxel Lord: Feudal Realm - Milestone 48: Royal Chancery & Realm Diplomacy UI
# In-game modal interface toggled via 'U' key to manage foreign relations, treaties,
# emissaries, and vassal tribute demands.

class_name DiplomacyUI
extends Control

signal menu_closed()

var diplomacy_system: DiplomacySystem = null
var supply_chain: SupplyChain = null

var selected_faction_id: String = "valoria"

var panel: PanelContainer
var faction_list_vbox: VBoxContainer
var dossier_name_label: Label
var dossier_ruler_label: Label
var dossier_archetype_label: Label
var dossier_status_label: Label
var dossier_opinion_label: Label
var dossier_opinion_bar: ProgressBar
var dossier_demands_label: Label
var dossier_military_label: Label
var active_treaties_label: Label
var toast_label: Label

# Action buttons container
var actions_vbox: VBoxContainer

func _ready() -> void:
	visible = false
	_build_ui()

func setup(p_diplomacy: DiplomacySystem, p_supply: SupplyChain = null) -> void:
	diplomacy_system = p_diplomacy
	supply_chain = p_supply

	if diplomacy_system:
		diplomacy_system.opinion_changed.connect(func(_f, _o, _n, _s): refresh())
		diplomacy_system.treaty_signed.connect(func(_f, _t): refresh())
		diplomacy_system.treaty_broken.connect(func(_f, _t, _p): refresh())
		diplomacy_system.war_declared.connect(func(_f, _a): refresh())
		diplomacy_system.peace_concluded.connect(func(_f): refresh())
		diplomacy_system.tribute_received.connect(_on_tribute_received)
		diplomacy_system.emissary_arrived.connect(_on_emissary_arrived)

	refresh()

func _build_ui() -> void:
	anchors_preset = Control.PRESET_FULL_RECT
	mouse_filter = Control.MOUSE_FILTER_STOP

	var backdrop = ColorRect.new()
	backdrop.anchors_preset = Control.PRESET_FULL_RECT
	backdrop.color = Color(0.04, 0.05, 0.08, 0.85)
	add_child(backdrop)

	panel = PanelContainer.new()
	panel.anchors_preset = Control.PRESET_CENTER
	panel.custom_minimum_size = Vector2(860, 580)
	panel.offset_left = -430
	panel.offset_top = -290
	panel.offset_right = 430
	panel.offset_bottom = 290
	add_child(panel)

	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 10)
	panel.add_child(main_vbox)

	# Title Banner
	var title = Label.new()
	title.text = "📜 ROYAL CHANCERY & REALM DIPLOMACY 🕊️"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	main_vbox.add_child(title)

	var h_split = HBoxContainer.new()
	h_split.size_flags_vertical = Control.SIZE_EXPAND_FILL
	h_split.add_theme_constant_override("separation", 16)
	main_vbox.add_child(h_split)

	# Left Column: Foreign Realms List
	var left_vbox = VBoxContainer.new()
	left_vbox.custom_minimum_size = Vector2(300, 0)
	left_vbox.add_theme_constant_override("separation", 8)
	h_split.add_child(left_vbox)

	var left_hdr = Label.new()
	left_hdr.text = "--- NEIGHBORING REALMS ---"
	left_vbox.add_child(left_hdr)

	var scroll = ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	left_vbox.add_child(scroll)

	faction_list_vbox = VBoxContainer.new()
	faction_list_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	faction_list_vbox.add_theme_constant_override("separation", 6)
	scroll.add_child(faction_list_vbox)

	# Right Column: Detailed Faction Dossier & Chancery Actions
	var right_vbox = VBoxContainer.new()
	right_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right_vbox.add_theme_constant_override("separation", 8)
	h_split.add_child(right_vbox)

	var dossier_box = VBoxContainer.new()
	dossier_box.add_theme_constant_override("separation", 4)
	right_vbox.add_child(dossier_box)

	dossier_name_label = Label.new()
	dossier_name_label.text = "Realm Name"
	dossier_box.add_child(dossier_name_label)

	dossier_ruler_label = Label.new()
	dossier_ruler_label.text = "Ruler: Unknown"
	dossier_box.add_child(dossier_ruler_label)

	dossier_archetype_label = Label.new()
	dossier_archetype_label.text = "Archetype: Unknown"
	dossier_box.add_child(dossier_archetype_label)

	dossier_status_label = Label.new()
	dossier_status_label.text = "Disposition: Neutral"
	dossier_box.add_child(dossier_status_label)

	var op_row = HBoxContainer.new()
	dossier_opinion_label = Label.new()
	dossier_opinion_label.text = "Opinion: 0.0"
	op_row.add_child(dossier_opinion_label)

	dossier_opinion_bar = ProgressBar.new()
	dossier_opinion_bar.min_value = -100.0
	dossier_opinion_bar.max_value = 100.0
	dossier_opinion_bar.value = 0.0
	dossier_opinion_bar.custom_minimum_size = Vector2(200, 16)
	op_row.add_child(dossier_opinion_bar)
	dossier_box.add_child(op_row)

	dossier_demands_label = Label.new()
	dossier_demands_label.text = "Desired Imports: Food | Specialty: Iron"
	dossier_box.add_child(dossier_demands_label)

	dossier_military_label = Label.new()
	dossier_military_label.text = "Military Strength: 150 | Wealth: 200"
	dossier_box.add_child(dossier_military_label)

	active_treaties_label = Label.new()
	active_treaties_label.text = "Active Treaties: None"
	dossier_box.add_child(active_treaties_label)

	# Actions
	var actions_hdr = Label.new()
	actions_hdr.text = "--- CHANCERY FEUDAL ACTIONS ---"
	right_vbox.add_child(actions_hdr)

	var act_scroll = ScrollContainer.new()
	act_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	right_vbox.add_child(act_scroll)

	actions_vbox = VBoxContainer.new()
	actions_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	actions_vbox.add_theme_constant_override("separation", 6)
	act_scroll.add_child(actions_vbox)

	# Footer & Toast
	var footer_hbox = HBoxContainer.new()
	main_vbox.add_child(footer_hbox)

	toast_label = Label.new()
	toast_label.text = "Press 'U' or 'ESC' to close Chancery."
	toast_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	footer_hbox.add_child(toast_label)

	var close_btn = Button.new()
	close_btn.text = "Close Chancery (ESC)"
	close_btn.pressed.connect(close_chancery)
	footer_hbox.add_child(close_btn)

func toggle_chancery() -> void:
	if visible:
		close_chancery()
	else:
		open_chancery()

func open_chancery() -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	refresh()

func close_chancery() -> void:
	visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	emit_signal("menu_closed")

func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_ESCAPE or event.keycode == KEY_U:
			close_chancery()
			get_viewport().set_input_as_handled()

func refresh() -> void:
	if not diplomacy_system:
		return

	# Rebuild Left Column Factions
	for child in faction_list_vbox.get_children():
		child.queue_free()

	var all_f = diplomacy_system.get_all_factions()
	for f_id in all_f.keys():
		var f = all_f[f_id]
		var status = diplomacy_system.get_relationship_status(f_id)
		var status_str = diplomacy_system.get_status_name(status)

		var btn = Button.new()
		btn.text = "%s %s\n[%s] Op: %.0f" % [f["icon"], f["name"], status_str, f["opinion"]]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		if f_id == selected_faction_id:
			btn.modulate = Color(1.3, 1.3, 0.9)
		btn.pressed.connect(func():
			selected_faction_id = f_id
			refresh()
		)
		faction_list_vbox.add_child(btn)

	# Update Right Column Dossier
	var cur_f = diplomacy_system.get_faction(selected_faction_id)
	if cur_f.is_empty():
		return

	dossier_name_label.text = "🏛️ %s" % cur_f["name"]
	dossier_ruler_label.text = "👑 Sovereign: %s" % cur_f["ruler"]
	dossier_archetype_label.text = "⚔️ Archetype: %s" % cur_f["archetype"]

	var cur_status = diplomacy_system.get_relationship_status(selected_faction_id)
	dossier_status_label.text = "Status: %s" % diplomacy_system.get_status_name(cur_status)
	dossier_opinion_label.text = "Opinion: %.1f / 100.0" % cur_f["opinion"]
	dossier_opinion_bar.value = cur_f["opinion"]

	dossier_demands_label.text = "Desired Tribute/Gift: %s | Specialty Export: %s" % [cur_f["demands"].capitalize(), cur_f["offers"].capitalize()]
	dossier_military_label.text = "Military Legion: %.0f soldiers | Wealth: %.0f gold" % [cur_f["military_strength"], cur_f["economic_wealth"]]

	var treaties_str = ""
	var treaties = cur_f.get("active_treaties", {})
	if treaties.is_empty():
		treaties_str = "None"
	else:
		var t_names = []
		for t in treaties.keys():
			var t_name = diplomacy_system.get_treaty_name(t)
			var dur = treaties[t]
			if dur < 0.0:
				t_names.append("%s (Permanent Fealty)" % t_name)
			else:
				t_names.append("%s (%.0fs left)" % [t_name, dur])
		treaties_str = ", ".join(t_names)
	active_treaties_label.text = "📜 Active Treaties: %s" % treaties_str

	# Rebuild Actions Buttons
	for child in actions_vbox.get_children():
		child.queue_free()

	_build_action_buttons(cur_f, cur_status)

func _build_action_buttons(f: Dictionary, status: DiplomacySystem.RelationshipStatus) -> void:
	var f_id = f["id"]
	var gold_count = supply_chain.get_resource("gold_coins") if supply_chain else 100
	var bread_count = supply_chain.get_resource("bread") if supply_chain else 50
	var timber_count = supply_chain.get_resource("logs") if supply_chain else 40

	if status == DiplomacySystem.RelationshipStatus.WAR:
		# At war: Sue for Peace button
		var peace_btn = Button.new()
		var peace_cost = int(f.get("military_strength", 100.0) * 0.5)
		peace_btn.text = "🕊️ Sue for Peace (Cost: %d Gold)" % peace_cost
		peace_btn.pressed.connect(func():
			if diplomacy_system.sue_for_peace(f_id, gold_count):
				if supply_chain:
					supply_chain.consume_resource("gold_coins", peace_cost)
				_toast("Peace concluded with %s!" % f["name"])
			else:
				_toast("Failed to conclude peace! Insufficient gold reparations.")
		)
		actions_vbox.add_child(peace_btn)
		return

	# 1. Gift Buttons
	var gift_gold_btn = Button.new()
	gift_gold_btn.text = "🎁 Dispatch Envoy with Royal Gold (10 Gold Coins)"
	gift_gold_btn.pressed.connect(func():
		var res = diplomacy_system.send_gift(f_id, "gold_coins", 10, gold_count)
		if res["success"]:
			if supply_chain:
				supply_chain.consume_resource("gold_coins", 10)
			_toast(res["message"])
		else:
			_toast("Could not send gift: %s" % res["message"])
	)
	actions_vbox.add_child(gift_gold_btn)

	var gift_demand_btn = Button.new()
	var pref_res = f.get("demands", "food")
	var send_res_name = "bread" if pref_res == "food" else ("logs" if pref_res == "timber" else pref_res)
	var stock = bread_count if send_res_name == "bread" else (timber_count if send_res_name == "logs" else 20)
	gift_demand_btn.text = "🌾 Envoy Preferred Tribute (15 %s)" % send_res_name.capitalize()
	gift_demand_btn.pressed.connect(func():
		var res = diplomacy_system.send_gift(f_id, send_res_name, 15, stock)
		if res["success"]:
			if supply_chain:
				supply_chain.consume_resource(send_res_name, 15)
			_toast(res["message"])
		else:
			_toast("Could not send preferred gift: %s" % res["message"])
	)
	actions_vbox.add_child(gift_demand_btn)

	# 2. Treaties Buttons
	var treaties_to_check = [
		DiplomacySystem.TreatyType.NON_AGGRESSION,
		DiplomacySystem.TreatyType.TRADE_CONCORDAT,
		DiplomacySystem.TreatyType.DEFENSIVE_LEAGUE,
		DiplomacySystem.TreatyType.VASSALAGE_CHARTER
	]

	for t_type in treaties_to_check:
		var check = diplomacy_system.can_sign_treaty(f_id, t_type)
		var t_name = diplomacy_system.get_treaty_name(t_type)
		if f.get("active_treaties", {}).has(t_type):
			var break_btn = Button.new()
			break_btn.text = "❌ Renounce & Sever %s" % t_name
			break_btn.pressed.connect(func():
				diplomacy_system.break_treaty(f_id, t_type)
				_toast("Severed %s with %s! Opinion plummeted." % [t_name, f["name"]])
			)
			actions_vbox.add_child(break_btn)
		else:
			var sign_btn = Button.new()
			sign_btn.text = "🤝 Sign %s (Cost: %d Gold)" % [t_name, check["cost_gold"]]
			sign_btn.disabled = not check["allowed"] or (gold_count < check["cost_gold"])
			sign_btn.tooltip_text = check["reason"]
			sign_btn.pressed.connect(func():
				if diplomacy_system.sign_treaty(f_id, t_type, gold_count):
					if supply_chain:
						supply_chain.consume_resource("gold_coins", check["cost_gold"])
					_toast("Ratified %s with %s!" % [t_name, f["name"]])
				else:
					_toast("Failed to sign treaty: %s" % check["reason"])
			)
			actions_vbox.add_child(sign_btn)

	# 3. Demand Tribute Button
	var demand_btn = Button.new()
	demand_btn.text = "⚔️ Demand Emergency Feudal Tribute"
	demand_btn.pressed.connect(func():
		var player_mil = 200.0 # Standard royal guard garrison strength
		var res = diplomacy_system.demand_tribute(f_id, "gold_coins", 30, player_mil)
		if res["accepted"]:
			if supply_chain:
				supply_chain.add_resource("gold_coins", res["amount_received"])
			_toast("Tribute extracted: +%d Gold! (%s)" % [res["amount_received"], res["reason"]])
		else:
			_toast("Demands rejected! %s" % res["reason"])
	)
	actions_vbox.add_child(demand_btn)

	# 4. Declare War Button
	var war_btn = Button.new()
	war_btn.text = "⚔️ Declare Imperial War & Expel Envoys"
	war_btn.pressed.connect(func():
		diplomacy_system.declare_war(f_id)
		_toast("WAR DECLARED against %s! Border hostilities commence." % f["name"])
	)
	actions_vbox.add_child(war_btn)

func _toast(msg: String) -> void:
	if toast_label:
		toast_label.text = msg
	refresh()

func _on_tribute_received(faction_id: String, resources: Dictionary) -> void:
	var f = diplomacy_system.get_faction(faction_id)
	var parts = []
	for k in resources.keys():
		parts.append("%d %s" % [resources[k], k])
	_toast("👑 Vassal Tribute arrived from %s: %s" % [f.get("name", faction_id), ", ".join(parts)])

func _on_emissary_arrived(faction_id: String, evt: Dictionary) -> void:
	_toast("🕊️ Envoy arrived from %s: '%s'" % [evt.get("faction", faction_id), evt.get("message", "")])
