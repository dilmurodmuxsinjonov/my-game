class_name GameHUD
extends Control

## Real-time HUD displaying monarch vitals (Health, Hunger, Stamina),
## interaction crosshair, notifications, and the 8-slot hotbar.

var health_bar: ProgressBar
var hunger_bar: ProgressBar
var stamina_bar: ProgressBar
var crosshair: Control
var hotbar_container: HBoxContainer
var notification_label: Label
var hotbar_slots: Array[PanelContainer] = []

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
	
	# 3. Notification Label (Top Center)
	notification_label = Label.new()
	notification_label.anchor_left = 0.5
	notification_label.anchor_right = 0.5
	notification_label.position = Vector2(-200, 40)
	notification_label.custom_minimum_size = Vector2(400, 30)
	notification_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	notification_label.modulate = Color(1.0, 1.0, 1.0, 0.0)
	add_child(notification_label)
	
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

func bind_player(player: Player) -> void:
	player.health_changed.connect(_on_health_changed)
	player.stamina_changed.connect(_on_stamina_changed)
	player.hunger_changed.connect(_on_hunger_changed)
	player.hotbar_slot_changed.connect(_on_hotbar_changed)
	player.block_action_performed.connect(_on_block_action)
	
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
