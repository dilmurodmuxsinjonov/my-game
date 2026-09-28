# scripts/ui/quest_journal.gd
# Voxel Lord: Feudal Realm - Milestone 45: Royal Quest & Renown Journal
# Displays sovereign deeds, active questline progression, feudal prestige, and realm statistics.

class_name QuestJournal
extends Control

signal journal_closed()

var quest_manager: QuestManager = null
var supply_chain: SupplyChain = null

# UI Containers
var panel_container: PanelContainer
var title_label: Label
var renown_label: Label
var quest_title_label: Label
var quest_desc_label: Label
var objectives_vbox: VBoxContainer
var stats_label: Label

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	anchor_right = 1.0
	anchor_bottom = 1.0
	visible = false
	_create_ui()

func _create_ui() -> void:
	var bg = ColorRect.new()
	bg.color = Color(0.03, 0.04, 0.06, 0.8)
	bg.anchor_right = 1.0
	bg.anchor_bottom = 1.0
	add_child(bg)

	panel_container = PanelContainer.new()
	panel_container.custom_minimum_size = Vector2(580, 520)
	panel_container.anchor_left = 0.5
	panel_container.anchor_top = 0.5
	panel_container.anchor_right = 0.5
	panel_container.anchor_bottom = 0.5
	panel_container.offset_left = -290.0
	panel_container.offset_top = -260.0
	panel_container.offset_right = 290.0
	panel_container.offset_bottom = 260.0

	var sb = StyleBoxFlat.new()
	sb.bg_color = Color(0.08, 0.1, 0.14, 0.96)
	sb.border_width_left = 2
	sb.border_width_top = 2
	sb.border_width_right = 2
	sb.border_width_bottom = 2
	sb.border_color = Color(0.9, 0.8, 0.45, 0.9)
	sb.corner_radius_top_left = 8
	sb.corner_radius_top_right = 8
	sb.corner_radius_bottom_right = 8
	sb.corner_radius_bottom_left = 8
	panel_container.add_theme_stylebox_override("panel", sb)
	add_child(panel_container)

	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 10)
	panel_container.add_child(main_vbox)

	title_label = Label.new()
	title_label.text = "📜 ROYAL DEEDS & FEUDAL QUEST CHRONICLE"
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_label.add_theme_font_size_override("font_size", 16)
	title_label.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	main_vbox.add_child(title_label)

	renown_label = Label.new()
	renown_label.text = "👑 Sovereign Title: Lord of the Frontier | ⚜️ Total Renown: 100"
	renown_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	renown_label.add_theme_font_size_override("font_size", 13)
	renown_label.add_theme_color_override("font_color", Color(0.85, 0.75, 0.5))
	main_vbox.add_child(renown_label)

	var sep = HSeparator.new()
	main_vbox.add_child(sep)

	# Active Quest Header
	quest_title_label = Label.new()
	quest_title_label.text = "I. Foundations of the Realm"
	quest_title_label.add_theme_font_size_override("font_size", 14)
	quest_title_label.add_theme_color_override("font_color", Color(0.95, 0.95, 0.95))
	main_vbox.add_child(quest_title_label)

	quest_desc_label = Label.new()
	quest_desc_label.text = "Establish a foothold in the wilderness. Gather timber and stone, and kindle a communal hearth."
	quest_desc_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	quest_desc_label.add_theme_font_size_override("font_size", 11)
	quest_desc_label.add_theme_color_override("font_color", Color(0.75, 0.8, 0.85))
	main_vbox.add_child(quest_desc_label)

	var sep2 = HSeparator.new()
	main_vbox.add_child(sep2)

	# Objectives List
	var obj_header = Label.new()
	obj_header.text = "FEUDAL OBJECTIVES:"
	obj_header.add_theme_font_size_override("font_size", 12)
	obj_header.add_theme_color_override("font_color", Color(1.0, 0.8, 0.3))
	main_vbox.add_child(obj_header)

	objectives_vbox = VBoxContainer.new()
	objectives_vbox.add_theme_constant_override("separation", 6)
	main_vbox.add_child(objectives_vbox)

	var sep3 = HSeparator.new()
	main_vbox.add_child(sep3)

	# Realm Statistics
	stats_label = Label.new()
	stats_label.text = "🏛️ Realm Status: 8 Districts Assembled | 👥 Population: 4 Citizens"
	stats_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stats_label.add_theme_font_size_override("font_size", 11)
	stats_label.add_theme_color_override("font_color", Color(0.65, 0.85, 0.95))
	main_vbox.add_child(stats_label)

	var close_btn = Button.new()
	close_btn.text = "↩ CLOSE JOURNAL (J or ESC)"
	close_btn.custom_minimum_size = Vector2(0, 36)
	close_btn.pressed.connect(close_journal)
	main_vbox.add_child(close_btn)

func open_journal() -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	refresh_display()

func close_journal() -> void:
	visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	journal_closed.emit()

func toggle_journal() -> void:
	if visible:
		close_journal()
	else:
		open_journal()

func refresh_display() -> void:
	if not quest_manager:
		return

	renown_label.text = "👑 Sovereign Title: %s | ⚜️ Total Renown: %d" % [
		quest_manager.get_monarch_title(),
		quest_manager.total_renown
	]

	var q = quest_manager.get_active_quest()
	if q.is_empty():
		quest_title_label.text = "🎉 All Sovereign Deeds Accomplished!"
		quest_desc_label.text = "The realm is completely unified and triumphant. You reign supreme as Sovereign King!"
		_clear_objectives()
		return

	quest_title_label.text = "%s (Reward: +%d Renown)" % [q["title"], q.get("reward_renown", 100)]
	quest_desc_label.text = q.get("description", "")

	_clear_objectives()
	for obj in q["objectives"]:
		var is_done = (obj["current"] >= obj["required"])
		var check_icon = "✓" if is_done else "○"
		var color = Color(0.4, 0.9, 0.4) if is_done else Color(0.85, 0.85, 0.85)

		var lbl = Label.new()
		lbl.text = "  [%s] %s: %d / %d" % [check_icon, obj["desc"], obj["current"], obj["required"]]
		lbl.add_theme_font_size_override("font_size", 12)
		lbl.add_theme_color_override("font_color", color)
		objectives_vbox.add_child(lbl)

func _clear_objectives() -> void:
	if not objectives_vbox:
		return
	for c in objectives_vbox.get_children():
		c.queue_free()
