# scripts/ui/tournament_ui.gd
# Voxel Lord: Feudal Realm - Milestone 50: Grand Feudal Jousting Tournament UI
# Interactive arena grandstand modal interface toggled via 'T' key.
# Allows participation in 4 knightly disciplines, placing bets, tracking chivalric honor,
# and hosting royal realm banquets.

class_name TournamentUI
extends Control

signal menu_closed()

var tournament_manager: TournamentManager = null
var supply_chain: SupplyChain = null

var panel: PanelContainer
var header_title: Label
var header_stats: Label
var tab_container: TabContainer
var toast_label: Label

# Joust controls
var joust_opp_opt: OptionButton
var joust_target_opt: OptionButton
var joust_timing_slider: HSlider
var joust_status_lbl: Label
var joust_action_btn: Button

# Melee controls
var melee_opp_opt: OptionButton
var melee_status_lbl: Label
var melee_hp_lbl: Label

# Archery controls
var archery_opp_opt: OptionButton
var archery_status_lbl: Label
var archery_elev_slider: HSlider
var archery_wind_slider: HSlider

# Champion Duel controls
var duel_opp_opt: OptionButton
var duel_status_lbl: Label

# Feast & Wager controls
var wager_champ_opt: OptionButton
var wager_amount_opt: OptionButton
var feast_status_lbl: Label

func _ready() -> void:
	visible = false
	_build_ui()

func setup(p_manager: TournamentManager, p_supply: SupplyChain = null) -> void:
	tournament_manager = p_manager
	supply_chain = p_supply

	if tournament_manager:
		tournament_manager.discipline_started.connect(func(_d, _p, _o): refresh())
		tournament_manager.joust_pass_completed.connect(func(_p, _pp, _op, _pu, _ou): refresh())
		tournament_manager.melee_round_completed.connect(func(_r, _w, _php, _ohp): refresh())
		tournament_manager.archery_shot_recorded.connect(func(_s, _d, _w, _sc): refresh())
		tournament_manager.tournament_victorious.connect(func(d, v, p, h): _on_victory(d, v, p, h))
		tournament_manager.wager_resolved.connect(func(_id, won, pay): _on_wager_resolved(won, pay))
		tournament_manager.chivalric_title_unlocked.connect(func(t, h): _on_title_unlocked(t, h))
		tournament_manager.grand_feast_hosted.connect(func(m, g): _on_feast_hosted(m, g))

	refresh()

func toggle_tournament_ui() -> void:
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
	backdrop.color = Color(0.04, 0.03, 0.05, 0.90)
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
	header_title.text = "🏟️ GRAND FEUDAL TOURNAMENT & CHIVALRIC ARENA"
	header_title.add_theme_font_size_override("font_size", 20)
	header_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header_bar.add_child(header_title)

	var close_btn = Button.new()
	close_btn.text = "✖ Close [T]"
	close_btn.pressed.connect(toggle_tournament_ui)
	header_bar.add_child(close_btn)
	main_vbox.add_child(header_bar)

	# Stats banner
	header_stats = Label.new()
	header_stats.text = "Rank: Page of the Realm | Honor: 0 | Grandstand: 75% | Victorious Bouts: 0"
	header_stats.add_theme_color_override("font_color", Color(0.9, 0.8, 0.4))
	main_vbox.add_child(header_stats)

	# Tab Container
	tab_container = TabContainer.new()
	tab_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_vbox.add_child(tab_container)

	_build_joust_tab(tab_container)
	_build_melee_tab(tab_container)
	_build_archery_tab(tab_container)
	_build_duel_tab(tab_container)
	_build_wagers_and_feast_tab(tab_container)

	# Toast Notification label
	toast_label = Label.new()
	toast_label.text = "Welcome to the Royal Jousting Grandstand. Press 'T' or Esc to close."
	toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast_label.add_theme_color_override("font_color", Color(0.4, 0.9, 0.6))
	main_vbox.add_child(toast_label)

func _build_joust_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "🏇 Joust of Peace"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 10)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	var desc = Label.new()
	desc.text = "Gallop down the tilt barrier with couched lance! Aim for the opponent's helm, shield, or breastplate."
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vbox.add_child(desc)

	var opp_row = HBoxContainer.new()
	var opp_lbl = Label.new()
	opp_lbl.text = "Select Opponent: "
	opp_row.add_child(opp_lbl)
	joust_opp_opt = OptionButton.new()
	joust_opp_opt.add_item("Sir Roland the Ironclad (Bulwark Knight)", 0)
	joust_opp_opt.add_item("Lady Gwendolyn the Swift (Silver Falcon)", 1)
	joust_opp_opt.add_item("Lord Valerie the Falcon (Azure Knight)", 2)
	opp_row.add_child(joust_opp_opt)

	var start_joust_btn = Button.new()
	start_joust_btn.text = "🚩 Mount Steed & Sound Charge"
	start_joust_btn.pressed.connect(_on_start_joust_pressed)
	opp_row.add_child(start_joust_btn)
	vbox.add_child(opp_row)

	var aim_row = HBoxContainer.new()
	var aim_lbl = Label.new()
	aim_lbl.text = "Target Tilt Zone: "
	aim_row.add_child(aim_lbl)
	joust_target_opt = OptionButton.new()
	joust_target_opt.add_item("Shield (Reliable Lance Break, 2 pts)", 0)
	joust_target_opt.add_item("Helm (High Risk / Unhorse Chance, 3 pts)", 1)
	joust_target_opt.add_item("Breastplate (Solid Impact, 1 pt)", 2)
	aim_row.add_child(joust_target_opt)
	vbox.add_child(aim_row)

	var timing_row = HBoxContainer.new()
	var time_lbl = Label.new()
	time_lbl.text = "Lance Couched Timing: "
	timing_row.add_child(time_lbl)
	joust_timing_slider = HSlider.new()
	joust_timing_slider.min_value = 0.3
	joust_timing_slider.max_value = 1.0
	joust_timing_slider.step = 0.05
	joust_timing_slider.value = 0.85
	joust_timing_slider.custom_minimum_size = Vector2(240, 24)
	timing_row.add_child(joust_timing_slider)
	vbox.add_child(timing_row)

	joust_action_btn = Button.new()
	joust_action_btn.text = "💥 TILT LANCE (Pass Strike)"
	joust_action_btn.pressed.connect(_on_joust_pass_pressed)
	vbox.add_child(joust_action_btn)

	joust_status_lbl = Label.new()
	joust_status_lbl.text = "Awaiting match initiation..."
	joust_status_lbl.add_theme_color_override("font_color", Color(0.9, 0.9, 0.5))
	vbox.add_child(joust_status_lbl)

func _build_melee_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "⚔️ Foot Melee"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 10)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	var desc = Label.new()
	desc.text = "Clash on foot in the dirt arena with two-handed broadswords, poleaxes, and heater shields!"
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vbox.add_child(desc)

	var opp_row = HBoxContainer.new()
	var opp_lbl = Label.new()
	opp_lbl.text = "Opponent: "
	opp_row.add_child(opp_lbl)
	melee_opp_opt = OptionButton.new()
	melee_opp_opt.add_item("Brother Bartholomew the Steadfast (Templar)", 0)
	melee_opp_opt.add_item("Sir Roland the Ironclad (Bulwark)", 1)
	opp_row.add_child(melee_opp_opt)

	var start_melee_btn = Button.new()
	start_melee_btn.text = "⚔️ Enter Arena"
	start_melee_btn.pressed.connect(_on_start_melee_pressed)
	opp_row.add_child(start_melee_btn)
	vbox.add_child(opp_row)

	var actions_row = HBoxContainer.new()
	var strike_btn = Button.new()
	strike_btn.text = "🗡️ Standard Strike"
	strike_btn.pressed.connect(func(): _on_melee_action_pressed("strike"))
	actions_row.add_child(strike_btn)

	var cleave_btn = Button.new()
	cleave_btn.text = "🪓 Heavy Cleave"
	cleave_btn.pressed.connect(func(): _on_melee_action_pressed("heavy_cleave"))
	actions_row.add_child(cleave_btn)

	var parry_btn = Button.new()
	parry_btn.text = "🛡️ Parry & Deflect"
	parry_btn.pressed.connect(func(): _on_melee_action_pressed("parry"))
	actions_row.add_child(parry_btn)

	var bash_btn = Button.new()
	bash_btn.text = "🔨 Shield Bash"
	bash_btn.pressed.connect(func(): _on_melee_action_pressed("shield_bash"))
	actions_row.add_child(bash_btn)
	vbox.add_child(actions_row)

	melee_hp_lbl = Label.new()
	melee_hp_lbl.text = "Monarch HP: 100/100 | Opponent HP: 100/100"
	vbox.add_child(melee_hp_lbl)

	melee_status_lbl = Label.new()
	melee_status_lbl.text = "No active melee bout."
	melee_status_lbl.add_theme_color_override("font_color", Color(0.9, 0.9, 0.5))
	vbox.add_child(melee_status_lbl)

func _build_archery_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "🏹 Archery Guild"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 10)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	var desc = Label.new()
	desc.text = "Compete against master marksmen over 30m, 50m, and 70m ranges with dynamic crosswind deflection!"
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vbox.add_child(desc)

	var opp_row = HBoxContainer.new()
	var opp_lbl = Label.new()
	opp_lbl.text = "Marksman Opponent: "
	opp_row.add_child(opp_lbl)
	archery_opp_opt = OptionButton.new()
	archery_opp_opt.add_item("Lady Gwendolyn the Swift (Silver Falcon)", 0)
	archery_opp_opt.add_item("Lord Valerie the Falcon", 1)
	opp_row.add_child(archery_opp_opt)

	var start_arch_btn = Button.new()
	start_arch_btn.text = "🎯 Step to Archery Line"
	start_arch_btn.pressed.connect(_on_start_archery_pressed)
	opp_row.add_child(start_arch_btn)
	vbox.add_child(opp_row)

	var elev_row = HBoxContainer.new()
	var elev_lbl = Label.new()
	elev_lbl.text = "Bow Elevation: "
	elev_row.add_child(elev_lbl)
	archery_elev_slider = HSlider.new()
	archery_elev_slider.min_value = 0.0
	archery_elev_slider.max_value = 5.0
	archery_elev_slider.step = 0.2
	archery_elev_slider.value = 1.5
	archery_elev_slider.custom_minimum_size = Vector2(240, 24)
	elev_row.add_child(archery_elev_slider)
	vbox.add_child(elev_row)

	var wind_row = HBoxContainer.new()
	var wind_lbl = Label.new()
	wind_lbl.text = "Wind Offset Adjust: "
	wind_row.add_child(wind_lbl)
	archery_wind_slider = HSlider.new()
	archery_wind_slider.min_value = -5.0
	archery_wind_slider.max_value = 5.0
	archery_wind_slider.step = 0.2
	archery_wind_slider.value = 0.0
	archery_wind_slider.custom_minimum_size = Vector2(240, 24)
	wind_row.add_child(archery_wind_slider)
	vbox.add_child(wind_row)

	var shoot_btn = Button.new()
	shoot_btn.text = "🏹 LOOSE ARROW"
	shoot_btn.pressed.connect(_on_shoot_arrow_pressed)
	vbox.add_child(shoot_btn)

	archery_status_lbl = Label.new()
	archery_status_lbl.text = "Ready to draw longbow."
	archery_status_lbl.add_theme_color_override("font_color", Color(0.9, 0.9, 0.5))
	vbox.add_child(archery_status_lbl)

func _build_duel_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "👑 Champion Duel"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 10)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	var desc = Label.new()
	desc.text = "Challenge the realm's grandmaster boss champions to honor duels for massive renown and knighthood prestige!"
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vbox.add_child(desc)

	var opp_row = HBoxContainer.new()
	var opp_lbl = Label.new()
	opp_lbl.text = "Grand Champion: "
	opp_row.add_child(opp_lbl)
	duel_opp_opt = OptionButton.new()
	duel_opp_opt.add_item("Prince Alden of Valoria (Crown Champion)", 0)
	duel_opp_opt.add_item("Sir Roland the Ironclad (The Bulwark)", 1)
	opp_row.add_child(duel_opp_opt)

	var start_duel_btn = Button.new()
	start_duel_btn.text = "👑 Challenge Champion"
	start_duel_btn.pressed.connect(_on_start_duel_pressed)
	opp_row.add_child(start_duel_btn)
	vbox.add_child(opp_row)

	var gambits_row = HBoxContainer.new()
	var feint_btn = Button.new()
	feint_btn.text = "⚡ Feint & Thrust"
	feint_btn.pressed.connect(func(): _on_duel_gambit_pressed("feint_and_thrust"))
	gambits_row.add_child(feint_btn)

	var counter_btn = Button.new()
	counter_btn.text = "⚔️ Riposte Counter"
	counter_btn.pressed.connect(func(): _on_duel_gambit_pressed("riposte_counter"))
	gambits_row.add_child(counter_btn)

	var guard_btn = Button.new()
	guard_btn.text = "🛡️ Defensive Guard"
	guard_btn.pressed.connect(func(): _on_duel_gambit_pressed("defensive_guard"))
	gambits_row.add_child(guard_btn)
	vbox.add_child(gambits_row)

	duel_status_lbl = Label.new()
	duel_status_lbl.text = "Duel arena open for champion challenges."
	duel_status_lbl.add_theme_color_override("font_color", Color(0.9, 0.9, 0.5))
	vbox.add_child(duel_status_lbl)

func _build_wagers_and_feast_tab(parent: TabContainer) -> void:
	var scroll = ScrollContainer.new()
	scroll.name = "💰 Wagers & 🍖 Feast"
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 12)
	scroll.add_child(vbox)
	parent.add_child(scroll)

	# Grandstand Wagers
	var wager_header = Label.new()
	wager_header.text = "💰 GRANDSTAND WAGERING BOOTH"
	wager_header.add_theme_font_size_override("font_size", 16)
	wbox_add(vbox, wager_header)

	var wager_row = HBoxContainer.new()
	var w_lbl = Label.new()
	w_lbl.text = "Back Champion: "
	wager_row.add_child(w_lbl)
	wager_champ_opt = OptionButton.new()
	wager_champ_opt.add_item("Monarch (Odds 1.8x)", 0)
	wager_champ_opt.add_item("Sir Roland the Ironclad (Odds 1.75x)", 1)
	wager_champ_opt.add_item("Lady Gwendolyn the Swift (Odds 2.10x)", 2)
	wager_champ_opt.add_item("Prince Alden of Valoria (Odds 1.50x)", 3)
	wager_row.add_child(wager_champ_opt)

	var a_lbl = Label.new()
	a_lbl.text = " Amount: "
	wager_row.add_child(a_lbl)
	wager_amount_opt = OptionButton.new()
	wager_amount_opt.add_item("10 Gold Coins", 0)
	wager_amount_opt.add_item("25 Gold Coins", 1)
	wager_amount_opt.add_item("50 Gold Coins", 2)
	wager_row.add_child(wager_amount_opt)

	var bet_btn = Button.new()
	bet_btn.text = "🪙 Place Wager"
	bet_btn.pressed.connect(_on_place_wager_pressed)
	wager_row.add_child(bet_btn)
	vbox.add_child(wager_row)

	var separator = HSeparator.new()
	vbox.add_child(separator)

	# Grand Realm Banquet
	var feast_header = Label.new()
	feast_header.text = "🍖 GRAND REGAL BANQUET OF THE REALM"
	feast_header.add_theme_font_size_override("font_size", 16)
	vbox.add_child(feast_header)

	var feast_desc = Label.new()
	feast_desc.text = "Host a lavish tournament feast in the Great Hall. Serves roasted meats, hearth bread, and barrels of ale to all subjects and visiting nobility."
	feast_desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vbox.add_child(feast_desc)

	var feast_cost_lbl = Label.new()
	feast_cost_lbl.text = "Feast Costs: 15 Hearth Bread | 25 Gold Coins   (Awards +25% Realm Morale & +100 Chivalric Honor)"
	feast_cost_lbl.add_theme_color_override("font_color", Color(0.9, 0.8, 0.3))
	vbox.add_child(feast_cost_lbl)

	var host_feast_btn = Button.new()
	host_feast_btn.text = "🍷 PROCLAIM GRAND FEAST OF THE REALM"
	host_feast_btn.pressed.connect(_on_host_feast_pressed)
	vbox.add_child(host_feast_btn)

	feast_status_lbl = Label.new()
	feast_status_lbl.text = "Feast hall awaiting monarch decree."
	feast_status_lbl.add_theme_color_override("font_color", Color(0.9, 0.9, 0.5))
	vbox.add_child(feast_status_lbl)

func wbox_add(parent: Node, child: Node) -> void:
	parent.add_child(child)

func refresh() -> void:
	if not tournament_manager:
		return

	header_stats.text = "Rank: %s | Honor: %d | Grandstand: %d%% | Wins: %d (Joust: %d, Melee: %d, Archery: %d, Duels: %d)" % [
		tournament_manager.current_title,
		tournament_manager.chivalric_honor,
		int(tournament_manager.grandstand_excitement),
		tournament_manager.total_tournaments_won,
		tournament_manager.total_jousts_won,
		tournament_manager.total_melees_won,
		tournament_manager.total_archery_won,
		tournament_manager.total_duels_won
	]

	if tournament_manager.active_discipline == "joust" and not tournament_manager.current_match.is_empty():
		var m = tournament_manager.current_match
		joust_status_lbl.text = "Pass: %d/%d | Monarch Pts: %d vs %s Pts: %d | Status: %s" % [
			m.get("current_pass", 1),
			m.get("max_passes", 3),
			m.get("player_score", 0),
			m.get("opponent_name", "Opponent"),
			m.get("opponent_score", 0),
			"Concluded" if m.get("is_finished", false) else "In Progress"
		]

	if tournament_manager.active_discipline == "melee" and not tournament_manager.current_match.is_empty():
		var m = tournament_manager.current_match
		melee_hp_lbl.text = "Monarch HP: %.0f/100 | %s HP: %.0f/100 (Round %d)" % [
			m.get("player_hp", 100.0),
			m.get("opponent_name", "Opponent"),
			m.get("opponent_hp", 100.0),
			m.get("round", 1)
		]

	if tournament_manager.active_discipline == "archery" and not tournament_manager.current_match.is_empty():
		var m = tournament_manager.current_match
		archery_status_lbl.text = "Shot: %d/%d | Range: %.0fm | Wind: %.1f m/s | Monarch Score: %d vs %s: %d" % [
			m.get("current_shot", 1),
			m.get("max_shots", 3),
			m.get("current_distance", 30.0),
			m.get("current_wind", 0.0),
			m.get("player_total_score", 0),
			m.get("opponent_name", "Opponent"),
			m.get("opp_total_score", 0)
		]

	if tournament_manager.active_discipline == "champion_duel" and not tournament_manager.current_match.is_empty():
		var m = tournament_manager.current_match
		duel_status_lbl.text = "Turn: %d | Monarch HP: %.0f vs %s HP: %.0f" % [
			m.get("turn", 1),
			m.get("player_hp", 120.0),
			m.get("opponent_name", "Prince Alden"),
			m.get("opponent_hp", 150.0)
		]

# ----------------- UI Button Callbacks -----------------
func _on_start_joust_pressed() -> void:
	if not tournament_manager: return
	var opp_id = "sir_roland"
	if joust_opp_opt.selected == 1: opp_id = "lady_gwendolyn"
	elif joust_opp_opt.selected == 2: opp_id = "lord_valerie"
	tournament_manager.start_joust_match(opp_id)
	toast_label.text = "🏇 Match Commenced: Monarch vs %s!" % opp_id.capitalize()
	refresh()

func _on_joust_pass_pressed() -> void:
	if not tournament_manager: return
	var target = "shield"
	if joust_target_opt.selected == 1: target = "helm"
	elif joust_target_opt.selected == 2: target = "breastplate"
	var timing = joust_timing_slider.value
	var res = tournament_manager.execute_joust_pass(target, timing)
	if res.has("clean_break") and res["clean_break"]:
		toast_label.text = "💥 CLEAN LANCE BREAK! Scored %d points!" % res.get("player_pts", 0)
	elif res.has("opp_unhorsed") and res["opp_unhorsed"]:
		toast_label.text = "👑 SPECTACULAR UNHORSING! The grandstand roars in ovation!"
	refresh()

func _on_start_melee_pressed() -> void:
	if not tournament_manager: return
	var opp_id = "brother_bartholomew"
	if melee_opp_opt.selected == 1: opp_id = "sir_roland"
	tournament_manager.start_melee_match(opp_id)
	toast_label.text = "⚔️ Arena Melee Commenced against %s!" % opp_id.capitalize()
	refresh()

func _on_melee_action_pressed(act: String) -> void:
	if not tournament_manager: return
	var res = tournament_manager.execute_melee_action(act)
	if res.has("player_damage"):
		toast_label.text = "⚔️ Executed %s: Dealt %.0f DMG, Took %.0f DMG." % [act.capitalize(), res["player_damage"], res["opp_damage"]]
	refresh()

func _on_start_archery_pressed() -> void:
	if not tournament_manager: return
	var opp_id = "lady_gwendolyn"
	if archery_opp_opt.selected == 1: opp_id = "lord_valerie"
	tournament_manager.start_archery_contest(opp_id)
	toast_label.text = "🎯 Marksman contest initiated against %s!" % opp_id.capitalize()
	refresh()

func _on_shoot_arrow_pressed() -> void:
	if not tournament_manager: return
	var elev = archery_elev_slider.value
	var wind_comp = archery_wind_slider.value
	var res = tournament_manager.shoot_archery_arrow(elev, wind_comp)
	if res.has("player_score"):
		toast_label.text = "🏹 Arrow Impact: Scored %d pts (Opponent: %d pts)!" % [res["player_score"], res["opp_score"]]
	refresh()

func _on_start_duel_pressed() -> void:
	if not tournament_manager: return
	var opp_id = "prince_alden"
	if duel_opp_opt.selected == 1: opp_id = "sir_roland"
	tournament_manager.start_champion_duel(opp_id)
	toast_label.text = "👑 Grandmaster Duel Commenced against %s!" % opp_id.capitalize()
	refresh()

func _on_duel_gambit_pressed(gambit: String) -> void:
	if not tournament_manager: return
	var res = tournament_manager.execute_duel_gambit(gambit)
	if res.has("player_damage"):
		toast_label.text = "👑 Gambit %s: Dealt %.0f DMG, Took %.0f DMG." % [gambit.capitalize(), res["player_damage"], res["opponent_damage"]]
	refresh()

func _on_place_wager_pressed() -> void:
	if not tournament_manager: return
	var champ_id = "monarch"
	if wager_champ_opt.selected == 1: champ_id = "sir_roland"
	elif wager_champ_opt.selected == 2: champ_id = "lady_gwendolyn"
	elif wager_champ_opt.selected == 3: champ_id = "prince_alden"

	var amt = 10
	if wager_amount_opt.selected == 1: amt = 25
	elif wager_amount_opt.selected == 2: amt = 50

	var res = tournament_manager.place_wager(champ_id, amt)
	if res.get("success", false):
		toast_label.text = "🪙 Wager accepted! %d gold placed on %s." % [amt, champ_id.capitalize()]
	else:
		toast_label.text = "⚠️ Wager failed: %s" % res.get("reason", "Unknown")
	refresh()

func _on_host_feast_pressed() -> void:
	if not tournament_manager: return
	var res = tournament_manager.host_grand_feast(supply_chain)
	if res.get("success", false):
		feast_status_lbl.text = "🍗 Regal Feast in progress! %d guests dining, +%.0f%% morale!" % [res.get("guests_count", 50), res.get("morale_boost", 25.0)]
		toast_label.text = "🍷 THE GRAND FEUDAL BANQUET HAS BEGUN! Realm citizens celebrate!"
	else:
		toast_label.text = "⚠️ Feast failed: %s" % res.get("reason", "Insufficient supplies")
	refresh()

func _on_victory(discipline: String, victor: String, prize: int, honor: int) -> void:
	toast_label.text = "🏆 VICTORY in %s! Victor: %s (+%d Gold, +%d Honor)!" % [discipline.capitalize(), victor, prize, honor]
	refresh()

func _on_wager_resolved(won: bool, payout: int) -> void:
	if won:
		toast_label.text = "💰 Wager Won! Collected payout of %d Gold!" % payout
	else:
		toast_label.text = "💸 Wager Lost! Better fortune in the next tilt!"
	refresh()

func _on_title_unlocked(title: String, honor: int) -> void:
	toast_label.text = "🛡️ CHIVALRIC PROMOTION! You have attained the title: '%s' (%d Honor)!" % [title, honor]
	refresh()

func _on_feast_hosted(boost: float, guests: int) -> void:
	toast_label.text = "🍷 Regal Banquet Hosted: %d guests entertained (+%.0f%% Realm Morale)!" % [guests, boost]
	refresh()
