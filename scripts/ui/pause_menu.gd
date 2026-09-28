# scripts/ui/pause_menu.gd
# Voxel Lord: Feudal Realm - Milestone 44: Interactive In-Game Pause & Settings Menu
# Provides complete control over Realm Save/Load, Settings (Graphics, FOV, Audio, Sensitivity),
# and Controls Guide with clean medieval styling.

class_name PauseMenu
extends Control

signal resume_requested()
signal save_requested(slot_name: String)
signal load_requested(slot_name: String)
signal settings_applied(settings_dict: Dictionary)
signal quit_requested()

var is_paused: bool = false
var save_system: SaveSystem

# UI Containers
var main_container: PanelContainer
var save_container: PanelContainer
var load_container: PanelContainer
var settings_container: PanelContainer
var controls_container: PanelContainer

# Settings Values
var mouse_sensitivity: float = 0.003
var field_of_view: float = 85.0
var master_volume: float = 0.8
var is_fullscreen: bool = false

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	anchor_right = 1.0
	anchor_bottom = 1.0
	visible = false
	_create_ui()

func _create_ui() -> void:
	# Dark transparent backdrop
	var bg = ColorRect.new()
	bg.color = Color(0.04, 0.05, 0.08, 0.85)
	bg.anchor_right = 1.0
	bg.anchor_bottom = 1.0
	add_child(bg)

	# 1. Main Pause View
	main_container = _create_panel("PAUSED - VOXEL LORD: FEUDAL REALM", Vector2(380, 480))
	add_child(main_container)
	var vbox = main_container.get_node("VBox")

	_create_button(vbox, "▶ RESUME REALM", _on_resume_pressed)
	_create_button(vbox, "💾 SAVE REALM", _on_open_save_pressed)
	_create_button(vbox, "📂 LOAD REALM", _on_open_load_pressed)
	_create_button(vbox, "⚙️ SETTINGS", _on_open_settings_pressed)
	_create_button(vbox, "📜 CONTROLS GUIDE", _on_open_controls_pressed)
	_create_button(vbox, "🚪 QUIT TO DESKTOP", _on_quit_pressed)

	# 2. Save Menu View
	save_container = _create_panel("SAVE REALM SLOTS", Vector2(440, 420))
	save_container.visible = false
	add_child(save_container)
	var sv_vbox = save_container.get_node("VBox")
	_create_button(sv_vbox, "💾 Slot 1 - Royal Keep", func(): _execute_save("slot_1"))
	_create_button(sv_vbox, "💾 Slot 2 - Trade Harbor", func(): _execute_save("slot_2"))
	_create_button(sv_vbox, "💾 Slot 3 - Steam Foundry", func(): _execute_save("slot_3"))
	_create_button(sv_vbox, "⚡ QuickSave (F5)", func(): _execute_save("quicksave"))
	_create_button(sv_vbox, "↩ BACK", func(): _show_view(main_container))

	# 3. Load Menu View
	load_container = _create_panel("LOAD REALM SLOTS", Vector2(440, 420))
	load_container.visible = false
	add_child(load_container)
	var ld_vbox = load_container.get_node("VBox")
	_create_button(ld_vbox, "📂 Slot 1 - Royal Keep", func(): _execute_load("slot_1"))
	_create_button(ld_vbox, "📂 Slot 2 - Trade Harbor", func(): _execute_load("slot_2"))
	_create_button(ld_vbox, "📂 Slot 3 - Steam Foundry", func(): _execute_load("slot_3"))
	_create_button(ld_vbox, "⚡ QuickSave (F9)", func(): _execute_load("quicksave"))
	_create_button(ld_vbox, "↩ BACK", func(): _show_view(main_container))

	# 4. Settings View
	settings_container = _create_panel("REALM SETTINGS", Vector2(460, 460))
	settings_container.visible = false
	add_child(settings_container)
	var st_vbox = settings_container.get_node("VBox")

	var sens_lbl = Label.new()
	sens_lbl.text = "Mouse Sensitivity: 0.003"
	st_vbox.add_child(sens_lbl)

	var fov_lbl = Label.new()
	fov_lbl.text = "Camera FOV: 85°"
	st_vbox.add_child(fov_lbl)

	var vol_lbl = Label.new()
	vol_lbl.text = "Master Audio Volume: 80%"
	st_vbox.add_child(vol_lbl)

	_create_button(st_vbox, "🖥️ TOGGLE FULLSCREEN", _toggle_fullscreen)
	_create_button(st_vbox, "✓ APPLY & SAVE SETTINGS", func(): _apply_settings(); _show_view(main_container))
	_create_button(st_vbox, "↩ BACK", func(): _show_view(main_container))

	# 5. Controls Guide View
	controls_container = _create_panel("FEUDAL REALM CONTROLS", Vector2(500, 520))
	controls_container.visible = false
	add_child(controls_container)
	var ct_vbox = controls_container.get_node("VBox")

	var ct_info = Label.new()
	ct_info.text = """[MOVEMENT & NAVIGATION]
  W, A, S, D  - Movement (Forward, Left, Back, Right)
  Shift (Hold)- Sprint at 8.5 m/s (Drains Stamina)
  Space       - Jump over terrain obstacles
  Mouse Look  - 360° First-Person View

[COMBAT & VOXEL INTERACTIONS]
  Left Click  - Mine Voxel / Swing Active Weapon
  Right Click - Place Selected Block / Use Station
  E           - Interact / Open Workstation
  1 to 8      - Hotbar Item Selection

[FEUDAL REALM SHORTCUTS]
  C           - Crafting Recipe Menu
  L           - Royal Ledger & Citizen Assignment
  H           - War Horn (Summon Militia)
  F1          - Realism Debug Telemetry Overlay
  F2          - Cycle Fast-Travel Across 8 Districts
  F5 / F9     - Quick Save / Quick Load
  ESC         - Pause Menu & Cursor Toggle"""
	ct_info.add_theme_font_size_override("font_size", 12)
	ct_vbox.add_child(ct_info)

	_create_button(ct_vbox, "↩ BACK", func(): _show_view(main_container))

func _create_panel(title_text: String, panel_size: Vector2) -> PanelContainer:
	var panel = PanelContainer.new()
	panel.anchor_left = 0.5
	panel.anchor_top = 0.5
	panel.anchor_right = 0.5
	panel.anchor_bottom = 0.5
	panel.offset_left = -panel_size.x * 0.5
	panel.offset_top = -panel_size.y * 0.5
	panel.offset_right = panel_size.x * 0.5
	panel.offset_bottom = panel_size.y * 0.5

	var sb = StyleBoxFlat.new()
	sb.bg_color = Color(0.1, 0.12, 0.16, 0.95)
	sb.border_width_left = 2
	sb.border_width_top = 2
	sb.border_width_right = 2
	sb.border_width_bottom = 2
	sb.border_color = Color(0.85, 0.75, 0.45, 0.85)
	sb.corner_radius_top_left = 6
	sb.corner_radius_top_right = 6
	sb.corner_radius_bottom_right = 6
	sb.corner_radius_bottom_left = 6
	panel.add_theme_stylebox_override("panel", sb)

	var vbox = VBoxContainer.new()
	vbox.name = "VBox"
	vbox.add_theme_constant_override("separation", 10)
	panel.add_child(vbox)

	var title = Label.new()
	title.text = title_text
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 15)
	title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.4))
	vbox.add_child(title)

	var sep = HSeparator.new()
	vbox.add_child(sep)

	return panel

func _create_button(parent: Node, text: String, callback: Callable) -> Button:
	var btn = Button.new()
	btn.text = text
	btn.custom_minimum_size = Vector2(0, 36)
	btn.pressed.connect(callback)
	parent.add_child(btn)
	return btn

func _show_view(target_view: PanelContainer) -> void:
	main_container.visible = (target_view == main_container)
	save_container.visible = (target_view == save_container)
	load_container.visible = (target_view == load_container)
	settings_container.visible = (target_view == settings_container)
	controls_container.visible = (target_view == controls_container)

func open_pause_menu() -> void:
	is_paused = true
	visible = true
	_show_view(main_container)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	if get_tree():
		get_tree().paused = true

func close_pause_menu() -> void:
	is_paused = false
	visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	if get_tree():
		get_tree().paused = false
	resume_requested.emit()

func toggle_pause_menu() -> void:
	if is_paused:
		close_pause_menu()
	else:
		open_pause_menu()

func _on_resume_pressed() -> void:
	close_pause_menu()

func _on_open_save_pressed() -> void:
	_show_view(save_container)

func _on_open_load_pressed() -> void:
	_show_view(load_container)

func _on_open_settings_pressed() -> void:
	_show_view(settings_container)

func _on_open_controls_pressed() -> void:
	_show_view(controls_container)

func _on_quit_pressed() -> void:
	quit_requested.emit()
	if get_tree():
		get_tree().quit()

func _execute_save(slot_name: String) -> void:
	save_requested.emit(slot_name)
	_show_view(main_container)

func _execute_load(slot_name: String) -> void:
	load_requested.emit(slot_name)
	close_pause_menu()

func _toggle_fullscreen() -> void:
	is_fullscreen = not is_fullscreen
	if is_fullscreen:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)

func _apply_settings() -> void:
	var cfg = {
		"mouse_sensitivity": mouse_sensitivity,
		"fov": field_of_view,
		"volume": master_volume,
		"fullscreen": is_fullscreen
	}
	settings_applied.emit(cfg)
