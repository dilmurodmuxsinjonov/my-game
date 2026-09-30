# scripts/ui/monastery_ui.gd
# Voxel Lord: Feudal Realm - Milestone 51: High Scholastic Monastic Order & Alchemy UI
# Interactive abbey scriptoria, alchemical laboratory, and relic sanctuary interface toggled via 'B' key.

class_name MonasteryUI
extends Control

signal menu_closed()

var monastery_system: MonasteryResearchSystem = null
var alchemy_lab: AlchemyLaboratory = null
var supply_chain: SupplyChain = null

var panel: PanelContainer
var header_title: Label
var header_stats: Label
var tab_container: TabContainer
var toast_label: Label

# Scriptoria controls
var tech_list_vbox: VBoxContainer
var scribes_count_lbl: Label

# Alchemy controls
var potions_grid: GridContainer
var transmutations_grid: GridContainer
var stone_stage_lbl: Label
var alembic_temp_lbl: Label

# Relic controls
var altar_slots_hbox: HBoxContainer
var relics_list_vbox: VBoxContainer
var blessings_summary_lbl: Label

func _ready() -> void:
	visible = false
	_build_ui()

func setup(p_monastery: MonasteryResearchSystem, p_alchemy: AlchemyLaboratory, p_supply: SupplyChain = null) -> void:
	monastery_system = p_monastery
	alchemy_lab = p_alchemy
	supply_chain = p_supply

	if monastery_system:
		monastery_system.research_started.connect(func(_t, _n, _c): refresh())
		monastery_system.research_progress_updated.connect(func(_t, _c, _m): refresh())
		monastery_system.research_completed.connect(func(_t, n): _on_research_done(n))
		monastery_system.relic_enshrined.connect(func(_r, n, s): _on_relic_enshrined(n, s))
		monastery_system.relic_removed.connect(func(_r, s): _on_relic_removed(s))
		monastery_system.abbey_bell_rung.connect(func(b): _on_bell_rung(b))

	if alchemy_lab:
		alchemy_lab.potion_brewed.connect(func(_p, n, _c): _on_potion_brewed(n))
		alchemy_lab.metal_transmuted.connect(func(_f, _i, o, c): _on_metal_transmuted(o, c))
		alchemy_lab.philosophers_stone_refined.connect(func(s, n): _on_stone_refined(s, n))

	refresh()

func toggle_monastery_ui() -> void:
	visible = not visible
	if visible:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		refresh()
	else:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		menu_closed.emit()

func _build_ui() -> void:
	anchors_preset = Control.PRESET_FULL_RECT
	mouse_filter = Control.MOUSE_FILTER_STOP

	var backdrop = ColorRect.new()
	backdrop.anchors_preset = Control.PRESET_FULL_RECT
	backdrop.color = Color(0.03, 0.04, 0.06, 0.92)
	add_child(backdrop)

	panel = PanelContainer.new()
	panel.anchors_preset = Control.PRESET_CENTER
	panel.custom_minimum_size = Vector2(920, 620)
	panel.offset_left = -460
	panel.offset_top = -310
	panel.offset_right = 460
	panel.offset_bottom = 310
	add_child(panel)

	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 8)
	panel.add_child(main_vbox)

	# Header Bar
	var header_bar = HBoxContainer.new()
	header_title = Label.new()
	header_title.text = "🏛️ HIGH SCHOLASTIC MONASTIC ORDER & ALCHEMY CRUCIBLE"
	header_title.add_theme_font_size_override("font_size", 20)
	header_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header_bar.add_child(header_title)

	var close_btn = Button.new()
	close_btn.text = "✖ Close [B]"
	close_btn.pressed.connect(toggle_monastery_ui)
	header_bar.add_child(close_btn)
	main_vbox.add_child(header_bar)

	# Stats Bar
	header_stats = Label.new()
	header_stats.text = "Scholar Scribes: 3 | Active Research: None | Magnum Opus: Nigredo | Relics Enshrined: 0/3"
	header_stats.add_theme_color_override("font_color", Color(0.85, 0.8, 0.4))
	main_vbox.add_child(header_stats)

	# Tab Container
	tab_container = TabContainer.new()
	tab_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_vbox.add_child(tab_container)

	_build_scriptoria_tab(tab_container)
	_build_alchemy_tab(tab_container)
	_build_relics_tab(tab_container)
	_build_liturgy_tab(tab_container)

	# Toast Notification Label
	toast_label = Label.new()
	toast_label.text = "Monastery gates opened. Press 'B' or Esc to close."
	toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast_label.add_theme_color_override("font_color", Color(0.4, 0.9, 0.6))
	main_vbox.add_child(toast_label)

func _build_scriptoria_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "📜 Scriptoria Tech Tree"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 8)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	# Scribes assignment header
	var scribe_bar = HBoxContainer.new()
	var s_lbl = Label.new()
	s_lbl.text = "Assigned Monk Scribes: "
	scribe_bar.add_child(s_lbl)

	scribes_count_lbl = Label.new()
	scribes_count_lbl.text = "3 Scribes"
	scribes_count_lbl.add_theme_color_override("font_color", Color(0.4, 0.8, 1.0))
	scribe_bar.add_child(scribes_count_lbl)

	var add_scribe_btn = Button.new()
	add_scribe_btn.text = "➕ Assign Monk"
	add_scribe_btn.pressed.connect(func(): _on_adjust_scribes(1))
	scribe_bar.add_child(add_scribe_btn)

	var rem_scribe_btn = Button.new()
	rem_scribe_btn.text = "➖ Reassign Duty"
	rem_scribe_btn.pressed.connect(func(): _on_adjust_scribes(-1))
	scribe_bar.add_child(rem_scribe_btn)
	vbox.add_child(scribe_bar)

	var sep = HSeparator.new()
	vbox.add_child(sep)

	tech_list_vbox = VBoxContainer.new()
	tech_list_vbox.add_theme_constant_override("separation", 6)
	vbox.add_child(tech_list_vbox)

func _build_alchemy_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "⚗️ Alchemical Crucible"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 10)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	# Laboratory Telemetry
	var telem_bar = HBoxContainer.new()
	alembic_temp_lbl = Label.new()
	alembic_temp_lbl.text = "Alembic Temperature: 85°C"
	alembic_temp_lbl.add_theme_color_override("font_color", Color(1.0, 0.6, 0.2))
	telem_bar.add_child(alembic_temp_lbl)

	var spacer = Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	telem_bar.add_child(spacer)

	stone_stage_lbl = Label.new()
	stone_stage_lbl.text = "Magnum Opus: Nigredo (1.0x Purity)"
	stone_stage_lbl.add_theme_color_override("font_color", Color(0.9, 0.8, 0.3))
	telem_bar.add_child(stone_stage_lbl)

	var advance_stone_btn = Button.new()
	advance_stone_btn.text = "🔴 Advance Magnum Opus"
	advance_stone_btn.pressed.connect(_on_advance_stone_pressed)
	telem_bar.add_child(advance_stone_btn)
	vbox.add_child(telem_bar)

	var sep1 = HSeparator.new()
	vbox.add_child(sep1)

	var potion_title = Label.new()
	potion_title.text = "🧪 HERMETIC DRAUGHTS & COMBAT ELIXIRS"
	potion_title.add_theme_font_size_override("font_size", 16)
	vbox.add_child(potion_title)

	potions_grid = GridContainer.new()
	potions_grid.columns = 2
	potions_grid.add_theme_constant_override("h_separation", 12)
	potions_grid.add_theme_constant_override("v_separation", 8)
	vbox.add_child(potions_grid)

	var sep2 = HSeparator.new()
	vbox.add_child(sep2)

	var transmute_title = Label.new()
	transmute_title.text = "🪙 METALLURGICAL TRANSMUTATIONS"
	transmute_title.add_theme_font_size_override("font_size", 16)
	vbox.add_child(transmute_title)

	transmutations_grid = GridContainer.new()
	transmutations_grid.columns = 2
	transmutations_grid.add_theme_constant_override("h_separation", 12)
	transmutations_grid.add_theme_constant_override("v_separation", 8)
	vbox.add_child(transmutations_grid)

func _build_relics_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "🏛️ Holy Relic Sanctuaries"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 10)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	var desc = Label.new()
	desc.text = "Enshrine sacred kingdom relics upon the High Abbey Altars to bestow perpetual divine blessings upon all citizens and lands."
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vbox.add_child(desc)

	altar_slots_hbox = HBoxContainer.new()
	altar_slots_hbox.add_theme_constant_override("separation", 10)
	vbox.add_child(altar_slots_hbox)

	blessings_summary_lbl = Label.new()
	blessings_summary_lbl.text = "Active Blessings: None"
	blessings_summary_lbl.add_theme_color_override("font_color", Color(0.4, 0.9, 0.7))
	vbox.add_child(blessings_summary_lbl)

	var sep = HSeparator.new()
	vbox.add_child(sep)

	var relics_title = Label.new()
	relics_title.text = "⚜️ DISCOVERED SACRED RELICS"
	relics_title.add_theme_font_size_override("font_size", 16)
	vbox.add_child(relics_title)

	relics_list_vbox = VBoxContainer.new()
	relics_list_vbox.add_theme_constant_override("separation", 6)
	vbox.add_child(relics_list_vbox)

func _build_liturgy_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "🔔 Liturgy & Abbey Bells"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 12)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	var desc = Label.new()
	desc.text = "Ring the consecrated bronze bells of the high monastery belfry. The sacred chimes echo across all 8 feudal districts, lifting citizen morale and warding off ill omens."
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vbox.add_child(desc)

	var bell_btn = Button.new()
	bell_btn.text = "🔔 RING GREAT ABBEY BELLS (+30% Citizen Serenity)"
	bell_btn.pressed.connect(_on_ring_bells_pressed)
	vbox.add_child(bell_btn)

func refresh() -> void:
	if not monastery_system or not alchemy_lab:
		return

	# Update Header Stats
	var res_name = "None"
	if monastery_system.current_research_id != "":
		var t = monastery_system.technologies.get(monastery_system.current_research_id)
		if t: res_name = t["name"]

	var stage_info = alchemy_lab.STONE_STAGES[clampi(alchemy_lab.philosophers_stone_stage - 1, 0, 3)]
	var enshrined_count = 0
	for s in monastery_system.active_altar_relics.keys():
		if monastery_system.active_altar_relics[s] != "":
			enshrined_count += 1

	header_stats.text = "Scholar Scribes: %d | Active: %s | Magnum Opus: %s | Relics Enshrined: %d/3" % [
		monastery_system.assigned_monk_scribes,
		res_name,
		stage_info["name"].split(" ")[0],
		enshrined_count
	]

	scribes_count_lbl.text = "%d Monk Scribes" % monastery_system.assigned_monk_scribes
	alembic_temp_lbl.text = "Alembic Temperature: %.0f°C" % alchemy_lab.alembic_temperature
	stone_stage_lbl.text = "Magnum Opus: %s (%.2fx Purity)" % [stage_info["name"], stage_info["bonus_purity"]]

	_refresh_tech_tree()
	_refresh_alchemy_potions()
	_refresh_transmutations()
	_refresh_relic_altars()

func _refresh_tech_tree() -> void:
	for child in tech_list_vbox.get_children():
		child.queue_free()

	for tid in monastery_system.technologies.keys():
		var t = monastery_system.technologies[tid]
		var is_unlocked = monastery_system.is_tech_unlocked(tid)
		var is_current = (monastery_system.current_research_id == tid)
		var cur_pts = monastery_system.research_progress.get(tid, 0.0)
		var cost = float(t["cost"])

		var row = HBoxContainer.new()
		var icon_lbl = Label.new()
		icon_lbl.text = t["icon"]
		row.add_child(icon_lbl)

		var name_lbl = Label.new()
		name_lbl.text = "%s (%d Pts)" % [t["name"], t["cost"]]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)

		var status_lbl = Label.new()
		if is_unlocked:
			status_lbl.text = "✅ Researched"
			status_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 0.4))
		elif is_current:
			status_lbl.text = "⏳ Researching (%.0f/%.0f)" % [cur_pts, cost]
			status_lbl.add_theme_color_override("font_color", Color(1.0, 0.8, 0.3))
		else:
			status_lbl.text = "🔒 Available"
			status_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
		row.add_child(status_lbl)

		if not is_unlocked and not is_current:
			var btn = Button.new()
			btn.text = "📜 Transcribe"
			btn.pressed.connect(func(): _on_start_research_pressed(tid))
			row.add_child(btn)

		tech_list_vbox.add_child(row)

func _refresh_alchemy_potions() -> void:
	for child in potions_grid.get_children():
		child.queue_free()

	for pid in alchemy_lab.potion_recipes.keys():
		var p = alchemy_lab.potion_recipes[pid]
		var p_box = VBoxContainer.new()
		var title = Label.new()
		title.text = "%s %s" % [p["icon"], p["name"]]
		title.add_theme_color_override("font_color", Color(0.9, 0.8, 0.4))
		p_box.add_child(title)

		var desc = Label.new()
		desc.text = p["desc"]
		desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		p_box.add_child(desc)

		var btn = Button.new()
		btn.text = "🧪 Brew Draught"
		btn.pressed.connect(func(): _on_brew_potion_pressed(pid))
		p_box.add_child(btn)

		potions_grid.add_child(p_box)

func _refresh_transmutations() -> void:
	for child in transmutations_grid.get_children():
		child.queue_free()

	for fid in alchemy_lab.transmutation_formulas.keys():
		var f = alchemy_lab.transmutation_formulas[fid]
		var f_box = VBoxContainer.new()
		var title = Label.new()
		title.text = "%s %s" % [f["icon"], f["name"]]
		title.add_theme_color_override("font_color", Color(0.8, 0.9, 0.4))
		f_box.add_child(title)

		var desc = Label.new()
		desc.text = f["desc"]
		desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		f_box.add_child(desc)

		var btn = Button.new()
		btn.text = "🪙 Transmute Metal"
		btn.pressed.connect(func(): _on_transmute_pressed(fid))
		f_box.add_child(btn)

		transmutations_grid.add_child(f_box)

func _refresh_relic_altars() -> void:
	for child in altar_slots_hbox.get_children():
		child.queue_free()

	var altar_names = ["High Chancel Altar", "North Nave Altar", "Lady Chapel Altar"]
	for i in range(3):
		var abox = VBoxContainer.new()
		abox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var title = Label.new()
		title.text = "🏛️ %s" % altar_names[i]
		abox.add_child(title)

		var rid = monastery_system.active_altar_relics.get(i, "")
		var r_lbl = Label.new()
		if rid != "":
			var r = monastery_system.relics.get(rid)
			r_lbl.text = "Active: %s %s" % [r["icon"], r["name"]]
			r_lbl.add_theme_color_override("font_color", Color(1.0, 0.85, 0.3))
			abox.add_child(r_lbl)

			var rem_btn = Button.new()
			rem_btn.text = "✖ Remove Relic"
			rem_btn.pressed.connect(func(): _on_remove_relic_pressed(i))
			abox.add_child(rem_btn)
		else:
			r_lbl.text = "Empty Sacred Altar"
			r_lbl.add_theme_color_override("font_color", Color(0.6, 0.6, 0.6))
			abox.add_child(r_lbl)

		altar_slots_hbox.add_child(abox)

	for child in relics_list_vbox.get_children():
		child.queue_free()

	for rid in monastery_system.discovered_relics:
		var r = monastery_system.relics.get(rid)
		var r_row = HBoxContainer.new()
		var n_lbl = Label.new()
		n_lbl.text = "%s %s - %s" % [r["icon"], r["name"], r["desc"]]
		n_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		r_row.add_child(n_lbl)

		var e0_btn = Button.new()
		e0_btn.text = "Enshrine [Slot 1]"
		e0_btn.pressed.connect(func(): _on_enshrine_relic_pressed(0, rid))
		r_row.add_child(e0_btn)

		var e1_btn = Button.new()
		e1_btn.text = "Slot 2"
		e1_btn.pressed.connect(func(): _on_enshrine_relic_pressed(1, rid))
		r_row.add_child(e1_btn)

		var e2_btn = Button.new()
		e2_btn.text = "Slot 3"
		e2_btn.pressed.connect(func(): _on_enshrine_relic_pressed(2, rid))
		r_row.add_child(e2_btn)

		relics_list_vbox.add_child(r_row)

	var b = monastery_system.get_active_blessings()
	blessings_summary_lbl.text = "Active Divine Blessings: %s" % str(b)

# ----------------- Button Callbacks -----------------
func _on_adjust_scribes(delta: int) -> void:
	if monastery_system:
		var count = monastery_system.assign_monks(delta)
		toast_label.text = "Assigned Monk Scribes updated: %d Scribes." % count
		refresh()

func _on_start_research_pressed(tech_id: String) -> void:
	if monastery_system:
		var ok = monastery_system.start_research(tech_id)
		if ok:
			var t = monastery_system.technologies[tech_id]
			toast_label.text = "📜 Scribes commenced manuscript transcription: %s!" % t["name"]
		refresh()

func _on_brew_potion_pressed(potion_id: String) -> void:
	if alchemy_lab:
		var res = alchemy_lab.brew_potion(potion_id, supply_chain)
		if res.get("success", false):
			toast_label.text = "🧪 Alchemical Draught Brewed: %s!" % res["name"]
		else:
			toast_label.text = "⚠️ Brewing failed: %s" % res.get("reason", "Missing supplies")
		refresh()

func _on_transmute_pressed(formula_id: String) -> void:
	if alchemy_lab:
		var res = alchemy_lab.transmute_metal(formula_id, supply_chain)
		if res.get("success", false):
			toast_label.text = "🪙 Transmutation successful! Baser metal transmuted into noble wealth!"
		else:
			toast_label.text = "⚠️ Transmutation failed: %s" % res.get("reason", "Missing ore")
		refresh()

func _on_advance_stone_pressed() -> void:
	if alchemy_lab:
		var res = alchemy_lab.refine_philosophers_stone(supply_chain)
		if res.get("success", false):
			toast_label.text = "🔴 MAGNUM OPUS ADVANCED! Reached: %s!" % res["stage_name"]
		else:
			toast_label.text = "⚠️ Sublimation failed: %s" % res.get("reason", "Requirements unmet")
		refresh()

func _on_enshrine_relic_pressed(slot: int, relic_id: String) -> void:
	if monastery_system:
		var ok = monastery_system.enshrine_relic(slot, relic_id)
		if ok:
			var r = monastery_system.relics[relic_id]
			toast_label.text = "🏛️ Enshrined %s upon Altar Slot %d!" % [r["name"], slot + 1]
		refresh()

func _on_remove_relic_pressed(slot: int) -> void:
	if monastery_system:
		monastery_system.remove_relic(slot)
		toast_label.text = "Relic removed from Altar Slot %d." % (slot + 1)
		refresh()

func _on_ring_bells_pressed() -> void:
	if monastery_system:
		monastery_system.ring_abbey_bells()
		toast_label.text = "🔔 THE GREAT ABBEY BELLS TOLL! Grace and serenity fill the realm!"
		refresh()

func _on_research_done(tech_name: String) -> void:
	toast_label.text = "📜 SCHOLASTIC TRIUMPH! Technology researched: %s!" % tech_name
	refresh()

func _on_relic_enshrined(rname: String, slot: int) -> void:
	toast_label.text = "🏛️ Holy Relic %s consecrated on Altar %d!" % [rname, slot + 1]
	refresh()

func _on_relic_removed(slot: int) -> void:
	toast_label.text = "Relic removed from Altar %d." % (slot + 1)
	refresh()

func _on_bell_rung(blessing: String) -> void:
	toast_label.text = "🔔 Abbey bells echoing: %s!" % blessing
	refresh()

func _on_potion_brewed(pname: String) -> void:
	toast_label.text = "🧪 Alchemical Draught brewed: %s!" % pname
	refresh()

func _on_metal_transmuted(out_res: String, count: int) -> void:
	toast_label.text = "🪙 Transmuted into %d %s!" % [count, out_res]
	refresh()

func _on_stone_refined(stage: int, sname: String) -> void:
	toast_label.text = "🔴 Philosopher's Stone refined to Stage %d: %s!" % [stage, sname]
	refresh()
