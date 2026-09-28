class_name GameHUD
extends Control

## Real-time HUD displaying monarch vitals (Health, Hunger, Stamina),
## interaction crosshair, notifications, and the 8-slot hotbar.

var health_bar: ProgressBar
var hunger_bar: ProgressBar
var stamina_bar: ProgressBar
var warmth_bar: ProgressBar
var season_weather_label: Label
var crosshair: Control
var hotbar_container: HBoxContainer
var notification_label: Label
var hotbar_slots: Array[PanelContainer] = []
var inspect_panel: PanelContainer
var inspect_label: Label
var debug_panel: PanelContainer
var debug_label: Label
var is_debug_visible: bool = false

var active_slot_index: int = 0

func _ready() -> void:
	_create_ui_elements()

func _create_ui_elements() -> void:
	# Set full rect
	anchor_right = 1.0
	anchor_bottom = 1.0
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	
	# 1. Crosshair in center
	crosshair = Control.new()
	crosshair.name = "Crosshair"
	crosshair.anchor_left = 0.5
	crosshair.anchor_top = 0.5
	crosshair.anchor_right = 0.5
	crosshair.anchor_bottom = 0.5
	crosshair.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(crosshair)
	
	var ch_dot = ColorRect.new()
	ch_dot.color = Color(1.0, 1.0, 1.0, 0.8)
	ch_dot.size = Vector2(4, 4)
	ch_dot.position = Vector2(-2, -2)
	crosshair.add_child(ch_dot)
	
	# 2. Vitals container (Top Left)
	var vitals_vbox = VBoxContainer.new()
	vitals_vbox.position = Vector2(24, 24)
	vitals_vbox.custom_minimum_size = Vector2(220, 80)
	add_child(vitals_vbox)
	
	# Health Bar
	var hl = Label.new()
	hl.text = "❤️ HEALTH"
	vitals_vbox.add_child(hl)
	health_bar = ProgressBar.new()
	health_bar.value = 100.0
	health_bar.custom_minimum_size = Vector2(200, 16)
	health_bar.show_percentage = false
	var sb_hp = StyleBoxFlat.new()
	sb_hp.bg_color = Color(0.85, 0.2, 0.2)
	health_bar.add_theme_stylebox_override("fill", sb_hp)
	vitals_vbox.add_child(health_bar)
	
	# Stamina Bar
	var sl = Label.new()
	sl.text = "⚡ STAMINA"
	vitals_vbox.add_child(sl)
	stamina_bar = ProgressBar.new()
	stamina_bar.value = 100.0
	stamina_bar.custom_minimum_size = Vector2(200, 14)
	stamina_bar.show_percentage = false
	var sb_st = StyleBoxFlat.new()
	sb_st.bg_color = Color(0.2, 0.75, 0.3)
	stamina_bar.add_theme_stylebox_override("fill", sb_st)
	vitals_vbox.add_child(stamina_bar)
	
	# Hunger Bar
	var hung_l = Label.new()
	hung_l.text = "🍗 SATIATION"
	vitals_vbox.add_child(hung_l)
	hunger_bar = ProgressBar.new()
	hunger_bar.value = 100.0
	hunger_bar.custom_minimum_size = Vector2(200, 14)
	hunger_bar.show_percentage = false
	var sb_hu = StyleBoxFlat.new()
	sb_hu.bg_color = Color(0.9, 0.6, 0.2)
	hunger_bar.add_theme_stylebox_override("fill", sb_hu)
	vitals_vbox.add_child(hunger_bar)
	
	# Warmth Bar
	var wl = Label.new()
	wl.text = "🔥 WARMTH"
	vitals_vbox.add_child(wl)
	warmth_bar = ProgressBar.new()
	warmth_bar.value = 100.0
	warmth_bar.custom_minimum_size = Vector2(200, 14)
	warmth_bar.show_percentage = false
	var sb_wm = StyleBoxFlat.new()
	sb_wm.bg_color = Color(0.95, 0.45, 0.15)
	warmth_bar.add_theme_stylebox_override("fill", sb_wm)
	vitals_vbox.add_child(warmth_bar)
	
	# 3. Notification Label (Top Center)
	notification_label = Label.new()
	notification_label.anchor_left = 0.5
	notification_label.anchor_right = 0.5
	notification_label.position = Vector2(-200, 40)
	notification_label.custom_minimum_size = Vector2(400, 30)
	notification_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	notification_label.modulate = Color(1.0, 1.0, 1.0, 0.0)
	add_child(notification_label)
	
	# 4. Season & Weather Label (Top Right)
	season_weather_label = Label.new()
	season_weather_label.anchor_left = 1.0
	season_weather_label.anchor_right = 1.0
	season_weather_label.offset_left = -280.0
	season_weather_label.offset_top = 24.0
	season_weather_label.offset_right = -24.0
	season_weather_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	season_weather_label.text = "🌸 Spring | 16°C\nClear Sky"
	season_weather_label.add_theme_font_size_override("font_size", 16)
	add_child(season_weather_label)
	
	# 4. Hotbar Container (Bottom Center)
	hotbar_container = HBoxContainer.new()
	hotbar_container.anchor_left = 0.5
	hotbar_container.anchor_top = 1.0
	hotbar_container.anchor_right = 0.5
	hotbar_container.anchor_bottom = 1.0
	hotbar_container.offset_left = -260.0
	hotbar_container.offset_top = -70.0
	hotbar_container.offset_right = 260.0
	hotbar_container.offset_bottom = -15.0
	hotbar_container.alignment = BoxContainer.ALIGNMENT_CENTER
	add_child(hotbar_container)
	
	# Create 8 slots
	for i in range(8):
		var slot_panel = PanelContainer.new()
		slot_panel.custom_minimum_size = Vector2(58, 52)
		
		var lbl = Label.new()
		lbl.name = "SlotLabel"
		lbl.text = "%d\n---" % (i + 1)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		slot_panel.add_child(lbl)
		
		hotbar_container.add_child(slot_panel)
		hotbar_slots.append(slot_panel)
		
	_highlight_active_slot(0)

	# 5. Target Block Inspect Tooltip (Center-Bottom, above hotbar)
	inspect_panel = PanelContainer.new()
	inspect_panel.name = "InspectPanel"
	inspect_panel.anchor_left = 0.5
	inspect_panel.anchor_top = 1.0
	inspect_panel.anchor_right = 0.5
	inspect_panel.anchor_bottom = 1.0
	inspect_panel.offset_left = -220.0
	inspect_panel.offset_top = -145.0
	inspect_panel.offset_right = 220.0
	inspect_panel.offset_bottom = -80.0
	var sb_inspect = StyleBoxFlat.new()
	sb_inspect.bg_color = Color(0.1, 0.12, 0.16, 0.88)
	sb_inspect.border_width_left = 2
	sb_inspect.border_width_top = 2
	sb_inspect.border_width_right = 2
	sb_inspect.border_width_bottom = 2
	sb_inspect.border_color = Color(0.85, 0.75, 0.45, 0.8)
	sb_inspect.corner_radius_top_left = 4
	sb_inspect.corner_radius_top_right = 4
	sb_inspect.corner_radius_bottom_right = 4
	sb_inspect.corner_radius_bottom_left = 4
	inspect_panel.add_theme_stylebox_override("panel", sb_inspect)
	inspect_panel.visible = false
	add_child(inspect_panel)

	inspect_label = Label.new()
	inspect_label.name = "InspectLabel"
	inspect_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	inspect_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	inspect_label.add_theme_font_size_override("font_size", 13)
	inspect_panel.add_child(inspect_label)

	# 6. Realism Debug Overlay Panel (Top Right below season, F1 toggle)
	debug_panel = PanelContainer.new()
	debug_panel.name = "DebugPanel"
	debug_panel.anchor_left = 1.0
	debug_panel.anchor_right = 1.0
	debug_panel.offset_left = -340.0
	debug_panel.offset_top = 75.0
	debug_panel.offset_right = -20.0
	debug_panel.offset_bottom = 280.0
	var sb_debug = StyleBoxFlat.new()
	sb_debug.bg_color = Color(0.06, 0.08, 0.12, 0.92)
	sb_debug.border_width_left = 1
	sb_debug.border_width_top = 1
	sb_debug.border_width_right = 1
	sb_debug.border_width_bottom = 1
	sb_debug.border_color = Color(0.4, 0.6, 0.9, 0.7)
	debug_panel.add_theme_stylebox_override("panel", sb_debug)
	debug_panel.visible = false
	add_child(debug_panel)

	debug_label = Label.new()
	debug_label.name = "DebugLabel"
	debug_label.add_theme_font_size_override("font_size", 12)
	debug_panel.add_child(debug_label)

func bind_player(player: Player) -> void:
	player.health_changed.connect(_on_health_changed)
	player.stamina_changed.connect(_on_stamina_changed)
	player.hunger_changed.connect(_on_hunger_changed)
	player.warmth_changed.connect(_on_warmth_changed)
	player.hotbar_slot_changed.connect(_on_hotbar_changed)
	player.block_action_performed.connect(_on_block_action)
	player.target_block_inspected.connect(update_inspect_tooltip)
	player.toggle_debug_requested.connect(toggle_debug_overlay)
	
	# Initialize hotbar displays
	for i in range(player.hotbar.size()):
		_update_slot_display(i, player.hotbar[i])
	_highlight_active_slot(player.active_slot)

func _on_health_changed(hp: float, max_hp: float) -> void:
	if health_bar:
		health_bar.value = (hp / max_hp) * 100.0

func _on_stamina_changed(st: float, max_st: float) -> void:
	if stamina_bar:
		stamina_bar.value = (st / max_st) * 100.0

func _on_hunger_changed(hg: float, max_hg: float) -> void:
	if hunger_bar:
		# Hunger is inverted: 0 hunger = 100% satiated
		hunger_bar.value = ((max_hg - hg) / max_hg) * 100.0

func _on_warmth_changed(wm: float, max_wm: float) -> void:
	if warmth_bar:
		warmth_bar.value = (wm / max_wm) * 100.0

func update_season_display(season_name: String, temp: float, weather_name: String) -> void:
	if season_weather_label:
		season_weather_label.text = "%s | %.1f°C\n%s" % [season_name, temp, weather_name]

func _on_hotbar_changed(index: int, item: Dictionary) -> void:
	_highlight_active_slot(index)
	_update_slot_display(index, item)

func _update_slot_display(index: int, item: Dictionary) -> void:
	if index < 0 or index >= hotbar_slots.size():
		return
	var lbl = hotbar_slots[index].get_node_or_null("SlotLabel") as Label
	if lbl:
		var icon = item.get("icon", "📦")
		var count = item.get("count", 1)
		if count > 1:
			lbl.text = "%s %d" % [icon, count]
		else:
			lbl.text = "%s" % icon

func _highlight_active_slot(index: int) -> void:
	active_slot_index = index
	for i in range(hotbar_slots.size()):
		var sb = StyleBoxFlat.new()
		if i == index:
			sb.bg_color = Color(0.25, 0.28, 0.35, 0.95)
			sb.border_width_left = 3
			sb.border_width_top = 3
			sb.border_width_right = 3
			sb.border_width_bottom = 3
			sb.border_color = Color(1.0, 0.85, 0.3)
		else:
			sb.bg_color = Color(0.12, 0.14, 0.18, 0.75)
			sb.border_width_left = 1
			sb.border_width_top = 1
			sb.border_width_right = 1
			sb.border_width_bottom = 1
			sb.border_color = Color(0.3, 0.3, 0.35)
		hotbar_slots[i].add_theme_stylebox_override("panel", sb)

func _on_block_action(action: String, _pos: Vector3i, _btype: int) -> void:
	show_notification("%s block" % action.capitalize())

func show_notification(msg: String) -> void:
	if notification_label:
		notification_label.text = msg
		notification_label.modulate.a = 1.0
		var tween = create_tween()
		tween.tween_property(notification_label, "modulate:a", 0.0, 1.8)

func update_inspect_tooltip(info: Dictionary) -> void:
	if not inspect_panel or not inspect_label:
		return
	if info.is_empty():
		inspect_panel.visible = false
		return
	inspect_panel.visible = true
	var name_str = info.get("name", "Unknown Block")
	var pos = info.get("pos", Vector3i.ZERO)
	var temp = info.get("temperature", 18.0)
	var stress = info.get("stress_mpa", 0.0)
	var max_stress = info.get("max_stress_mpa", 15.0)
	var text_content = "🔍 %s (X:%d, Y:%d, Z:%d)\n🌡️ Temp: %.1f°C | ⚖️ Stress: %.1f / %.1f MPa" % [
		name_str, pos.x, pos.y, pos.z, temp, stress, max_stress
	]
	if info.get("is_soil", false):
		text_content += "\n🌱 NPK: N:%.0f%% P:%.0f%% K:%.0f%% | 💧 Moist: %.0f%%" % [
			info.get("nitrogen", 70.0), info.get("phosphorus", 60.0), info.get("potassium", 65.0), info.get("moisture", 75.0)
		]
	inspect_label.text = text_content

func toggle_debug_overlay() -> void:
	is_debug_visible = not is_debug_visible
	if debug_panel:
		debug_panel.visible = is_debug_visible

func update_debug_info(fps: float, pos: Vector3, district_name: String, biome_name: String) -> void:
	if debug_label and is_debug_visible:
		debug_label.text = "[REALISM DEBUG OVERLAY - F1]\nFPS: %.0f | Monarch: (%.1f, %.1f, %.1f)\nDistrict: %s\nBiome: %s\nControls: [WASD] Move | [Shift] Sprint | [Space] Jump\n[LMB] Mine | [RMB] Place | [E] Interact | [C] Crafting\n[L] Ledger | [H] Horn | [F2] Fast Travel | [ESC] Pause" % [
			fps, pos.x, pos.y, pos.z, district_name, biome_name
		]

