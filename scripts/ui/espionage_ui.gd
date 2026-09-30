# scripts/ui/espionage_ui.gd
# Voxel Lord: Feudal Realm - Milestone 52: Royal Spymaster & Shadow Council UI
# Provides comprehensive covert operations board, agent roster, and interrogation dungeon management.

class_name EspionageUI
extends Control

signal close_requested()
signal recruit_agent_requested(archetype: String)
signal launch_operation_requested(op_id: String, target_realm: String, agent_id: String)
signal interrogate_prisoner_requested(prisoner_id: String)
signal ransom_prisoner_requested(prisoner_id: String)

var espionage_manager: EspionageManager = null
var supply_chain: SupplyChain = null

var tab_container: TabContainer = null
var agent_list_container: VBoxContainer = null
var operations_container: VBoxContainer = null
var dungeons_container: VBoxContainer = null
var security_label: Label = null
var status_label: Label = null

func _ready() -> void:
	visible = false
	setup_ui()

func setup_ui() -> void:
	# Root panel layout
	anchors_preset = PRESET_FULL_RECT
	mouse_filter = MOUSE_FILTER_STOP

	var overlay = ColorRect.new()
	overlay.anchors_preset = PRESET_FULL_RECT
	overlay.color = Color(0.02, 0.02, 0.05, 0.75)
	add_child(overlay)

	var panel = PanelContainer.new()
	panel.anchor_left = 0.15
	panel.anchor_top = 0.10
	panel.anchor_right = 0.85
	panel.anchor_bottom = 0.90
	add_child(panel)

	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 10)
	panel.add_child(main_vbox)

	# Header Bar
	var header_hbox = HBoxContainer.new()
	main_vbox.add_child(header_hbox)

	var title_lbl = Label.new()
	title_lbl.text = "🗡️ ROYAL SPYMASTER & SHADOW COUNCIL (KEY_N)"
	title_lbl.add_theme_font_size_override("font_size", 20)
	title_lbl.size_flags_horizontal = SIZE_EXPAND_FILL
	header_hbox.add_child(title_lbl)

	var close_btn = Button.new()
	close_btn.text = " [X] Close "
	close_btn.pressed.connect(_on_close_pressed)
	header_hbox.add_child(close_btn)

	security_label = Label.new()
	security_label.text = "🛡️ Citadel Security: 65% | Active Agents: 0 | Plots Thwarted: 0"
	main_vbox.add_child(security_label)

	# Tab Container
	tab_container = TabContainer.new()
	tab_container.size_flags_vertical = SIZE_EXPAND_FILL
	main_vbox.add_child(tab_container)

	# 1. Shadow Network Tab
	var network_scroll = ScrollContainer.new()
	network_scroll.name = "Shadow Network"
	tab_container.add_child(network_scroll)

	agent_list_container = VBoxContainer.new()
	agent_list_container.size_flags_horizontal = SIZE_EXPAND_FILL
	network_scroll.add_child(agent_list_container)

	# 2. Intrigue Operations Tab
	var ops_scroll = ScrollContainer.new()
	ops_scroll.name = "Covert Operations"
	tab_container.add_child(ops_scroll)

	operations_container = VBoxContainer.new()
	operations_container.size_flags_horizontal = SIZE_EXPAND_FILL
	ops_scroll.add_child(operations_container)

	# 3. Counter-Intelligence & Dungeons Tab
	var dungeons_scroll = ScrollContainer.new()
	dungeons_scroll.name = "Dungeons & Interrogations"
	tab_container.add_child(dungeons_scroll)

	dungeons_container = VBoxContainer.new()
	dungeons_container.size_flags_horizontal = SIZE_EXPAND_FILL
	dungeons_scroll.add_child(dungeons_container)

	# Status Footer
	status_label = Label.new()
	status_label.text = "Whispers from the shadows await your command, Sire."
	main_vbox.add_child(status_label)

func set_espionage_manager(mgr: EspionageManager, chain: SupplyChain = null) -> void:
	espionage_manager = mgr
	supply_chain = chain
	if is_inside_tree() and visible:
		refresh_ui()

func toggle_visibility() -> void:
	visible = not visible
	if visible:
		refresh_ui()

func refresh_ui() -> void:
	if not espionage_manager:
		return

	# Update header info
	security_label.text = "🛡️ Citadel Security Rating: %.1f%% | Active Agents: %d | Total Operations: %d | Plots Foiled: %d" % [
		espionage_manager.citadel_security_rating,
		espionage_manager.recruited_agents.size(),
		espionage_manager.total_operations_completed,
		espionage_manager.plots_thwarted_count
	]

	refresh_network_tab()
	refresh_operations_tab()
	refresh_dungeons_tab()

func refresh_network_tab() -> void:
	for child in agent_list_container.get_children():
		child.queue_free()

	# Recruitment Section
	var recruit_title = Label.new()
	recruit_title.text = "=== RECRUIT SHADOW AGENTS ==="
	recruit_title.add_theme_font_size_override("font_size", 16)
	agent_list_container.add_child(recruit_title)

	var recruit_hbox = HBoxContainer.new()
	recruit_hbox.add_theme_constant_override("separation", 15)
	agent_list_container.add_child(recruit_hbox)

	for arch_key in espionage_manager.agent_archetypes.keys():
		var arch = espionage_manager.agent_archetypes[arch_key]
		var btn = Button.new()
		btn.text = "%s %s (%d Gold)" % [arch["icon"], arch["name"], arch["cost_gold"]]
		btn.pressed.connect(func(): _on_recruit_clicked(arch_key))
		recruit_hbox.add_child(btn)

	var sep = HSeparator.new()
	agent_list_container.add_child(sep)

	# Active Roster
	var roster_title = Label.new()
	roster_title.text = "=== ACTIVE SHADOW AGENTS ROSTER ==="
	roster_title.add_theme_font_size_override("font_size", 16)
	agent_list_container.add_child(roster_title)

	if espionage_manager.recruited_agents.is_empty():
		var empty_lbl = Label.new()
		empty_lbl.text = "No shadow agents currently on royal retainer. Recruit informants above."
		agent_list_container.add_child(empty_lbl)
	else:
		for agent_id in espionage_manager.recruited_agents.keys():
			var a = espionage_manager.recruited_agents[agent_id]
			var card = PanelContainer.new()
			var card_box = HBoxContainer.new()
			card_box.add_theme_constant_override("separation", 15)
			card.add_child(card_box)

			var arch_info = espionage_manager.agent_archetypes.get(a["type"], {})
			var icon_str = arch_info.get("icon", "👤")

			var lbl = Label.new()
			lbl.text = "%s [%s] %s | Station: %s | Status: %s | Stealth: %.0f | Sabotage: %.0f" % [
				icon_str,
				a["id"].to_upper(),
				a["name"],
				a["stationed_realm"].capitalize(),
				a["status"],
				a["stealth_rating"],
				a["sabotage_rating"]
			]
			lbl.size_flags_horizontal = SIZE_EXPAND_FILL
			card_box.add_child(lbl)
			agent_list_container.add_child(card)

func refresh_operations_tab() -> void:
	for child in operations_container.get_children():
		child.queue_free()

	var ops_title = Label.new()
	ops_title.text = "=== COVERT INTRIGUE OPERATIONS BOARD ==="
	ops_title.add_theme_font_size_override("font_size", 16)
	operations_container.add_child(ops_title)

	for op_id in espionage_manager.operations_catalog.keys():
		var op_def = espionage_manager.operations_catalog[op_id]
		var pnl = PanelContainer.new()
		var hbox = HBoxContainer.new()
		hbox.add_theme_constant_override("separation", 15)
		pnl.add_child(hbox)

		var info_lbl = Label.new()
		info_lbl.text = "%s %s (Cost: %d Gold, Duration: %.0fs)\n%s" % [
			op_def["icon"],
			op_def["name"],
			op_def["cost_gold"],
			op_def["duration"],
			op_def["desc"]
		]
		info_lbl.size_flags_horizontal = SIZE_EXPAND_FILL
		hbox.add_child(info_lbl)

		# Buttons to launch into realms
		var target_realms = ["valoria", "ashfell", "silvercoast"]
		for realm in target_realms:
			var btn = Button.new()
			btn.text = "Dispatch -> %s" % realm.capitalize()
			btn.pressed.connect(func(): _on_launch_op_clicked(op_id, realm))
			hbox.add_child(btn)

		operations_container.add_child(pnl)

	# Active ongoing operations list
	var active_title = Label.new()
	active_title.text = "\n=== ONGOING OPERATIONS IN PROGRESS (%d) ===" % espionage_manager.active_operations.size()
	active_title.add_theme_font_size_override("font_size", 14)
	operations_container.add_child(active_title)

	if espionage_manager.active_operations.is_empty():
		var no_ops = Label.new()
		no_ops.text = "No covert missions currently executing in foreign courts."
		operations_container.add_child(no_ops)
	else:
		for op in espionage_manager.active_operations:
			var active_lbl = Label.new()
			var op_data = espionage_manager.operations_catalog.get(op["op_id"], {})
			active_lbl.text = "⏱️ [%s] %s in %s (Agent: %s) - Timer: %.1f seconds remaining" % [
				op["instance_id"],
				op_data.get("name", op["op_id"]),
				op["target_realm"].capitalize(),
				op["agent_id"],
				op["timer"]
			]
			operations_container.add_child(active_lbl)

func refresh_dungeons_tab() -> void:
	for child in dungeons_container.get_children():
		child.queue_free()

	var dungeon_title = Label.new()
	dungeon_title.text = "=== CITADEL SUBTERRANEAN INTERROGATION DUNGEONS ==="
	dungeon_title.add_theme_font_size_override("font_size", 16)
	dungeons_container.add_child(dungeon_title)

	if espionage_manager.captured_prisoners.is_empty():
		var empty_dungeon = Label.new()
		empty_dungeon.text = "Dungeon cells are vacant. No foreign spies or saboteurs apprehended."
		dungeons_container.add_child(empty_dungeon)
	else:
		for p in espionage_manager.captured_prisoners:
			var p_panel = PanelContainer.new()
			var p_hbox = HBoxContainer.new()
			p_hbox.add_theme_constant_override("separation", 15)
			p_panel.add_child(p_hbox)

			var plbl = Label.new()
			var status_str = "Interrogated" if p["interrogated"] else "Unbroken"
			plbl.text = "⛓️ [%s] %s | Status: %s | Ransom Value: %d Gold" % [
				p["id"],
				p["name"],
				status_str,
				p["ransom_value"]
			]
			plbl.size_flags_horizontal = SIZE_EXPAND_FILL
			p_hbox.add_child(plbl)

			if not p["interrogated"]:
				var int_btn = Button.new()
				var p_id = p["id"]
				int_btn.text = "🔍 Interrogate Secrets"
				int_btn.pressed.connect(func(): _on_interrogate_clicked(p_id))
				p_hbox.add_child(int_btn)

			var ran_btn = Button.new()
			var p_id_ransom = p["id"]
			ran_btn.text = "💰 Ransom (+%d Gold)" % p["ransom_value"]
			ran_btn.pressed.connect(func(): _on_ransom_clicked(p_id_ransom))
			p_hbox.add_child(ran_btn)

			dungeons_container.add_child(p_panel)

func _on_recruit_clicked(archetype: String) -> void:
	if not espionage_manager:
		return
	var res = espionage_manager.recruit_agent(archetype, "", supply_chain)
	if res["success"]:
		status_label.text = "Recruited new %s to the Crown's Shadow Council!" % archetype.capitalize()
		refresh_ui()
	else:
		status_label.text = "Failed to recruit: %s" % res.get("reason", "Unknown error")

func _on_launch_op_clicked(op_id: String, target_realm: String) -> void:
	if not espionage_manager:
		return
	# Find first ready agent
	var ready_agent_id = ""
	for a_id in espionage_manager.recruited_agents.keys():
		if espionage_manager.recruited_agents[a_id]["status"] == "Ready":
			ready_agent_id = a_id
			break

	if ready_agent_id == "":
		status_label.text = "No available shadow agents! Recruit or wait for existing missions to finish."
		return

	var res = espionage_manager.launch_operation(op_id, target_realm, ready_agent_id, supply_chain)
	if res["success"]:
		status_label.text = "Dispatched agent %s on covert mission in %s!" % [ready_agent_id, target_realm.capitalize()]
		refresh_ui()
	else:
		status_label.text = "Operation launch failed: %s" % res.get("reason", "Unknown error")

func _on_interrogate_clicked(prisoner_id: String) -> void:
	if not espionage_manager:
		return
	var res = espionage_manager.interrogate_prisoner(prisoner_id)
	if res["success"]:
		if supply_chain and res.has("coins_discovered"):
			supply_chain.add_resource("gold_coins", res["coins_discovered"])
		status_label.text = "Interrogation success: %s" % res["secrets"]
		refresh_ui()
	else:
		status_label.text = "Interrogation failed: %s" % res.get("reason", "Unknown error")

func _on_ransom_clicked(prisoner_id: String) -> void:
	if not espionage_manager:
		return
	var ok = espionage_manager.ransom_prisoner(prisoner_id, supply_chain)
	if ok:
		status_label.text = "Prisoner %s ransomed cleanly to foreign envoys!" % prisoner_id
		refresh_ui()

func _on_close_pressed() -> void:
	visible = false
	close_requested.emit()

func _unhandled_input(event: InputEvent) -> void:
	if visible and event is InputEventKey and event.pressed:
		if event.keycode == KEY_ESCAPE:
			visible = false
			close_requested.emit()
			get_viewport().set_input_as_handled()
