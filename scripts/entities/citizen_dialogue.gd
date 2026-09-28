# scripts/entities/citizen_dialogue.gd
# Voxel Lord: Feudal Realm - Milestone 45: Dynamic Citizen Dialogue & Interaction System
# Provides authentic medieval peasant dialogue, morale feedback, and monarch command interactions.

class_name CitizenDialogue
extends Control

signal dialogue_closed()
signal ration_offered(citizen_name: String)
signal inspiration_given(citizen_name: String)
signal role_change_requested(citizen: Node, new_role: int)

var current_citizen: Node = null
var supply_chain: SupplyChain = null

# UI Nodes
var panel_container: PanelContainer
var name_label: Label
var role_label: Label
var speech_label: Label
var morale_label: Label
var action_vbox: VBoxContainer

const ROLE_DIALOGUE: Dictionary = {
	0: [ # UNASSIGNED
		"Greetings, Sire! Awaiting your royal decree. Where shall I direct my labor?",
		"The realm calls, and I stand ready to serve the Crown.",
		"Tell me my duty, my Liege, and it shall be done."
	],
	1: [ # FARMER
		"The Norfolk crop rotation is bearing fruit, Sire. The soil is fertile and moist!",
		"We must tend the irrigation ditches before the summer heat parches the grain.",
		"The wheat heads are heavy with golden kernels. A bountiful harvest awaits!"
	],
	2: [ # LUMBERJACK
		"The oak trunks are sturdy, Sire. Our axes are sharp and the timber crates are filling.",
		"Watch your head in the logging groves, my Lord! Falling timber waits for no one.",
		"Good seasoned timber will strengthen our palisades against frontier beasts."
	],
	3: [ # MINER
		"The subterranean shafts run deep into granite strata, Sire. Iron and coal abound!",
		"We keep timber support beams spaced tight. Safety keeps our pickaxes swinging.",
		"Found a sparkling seam of silver and copper in the lower gallery today, my Liege!"
	],
	4: [ # BAKER
		"The millstone flour is ground fine, Sire. The brick ovens are warm and fragrant!",
		"Ration loaves baked fresh every morning keep our militia hearty and content.",
		"Grain from the silos makes the crust crisp and the crumb soft."
	],
	5: [ # BLACKSMITH
		"The tuyeres are blowing a fierce draft! Our blast furnace reaches 1400°C today.",
		"Forging crucibles and iron ingots for your royal armory, Sire.",
		"No blade is truer than steel folded under our heavy water-powered trip hammer!"
	],
	6: [ # GUARD
		"The ramparts are manned and the watchtowers vigilant, Sire! The realm is safe.",
		"Should bandit raiders emerge from the wilds, my spear will strike without mercy.",
		"All clear on the northern perimeter! The royal banner flutters proud in the wind."
	]
}

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	anchor_right = 1.0
	anchor_bottom = 1.0
	visible = false
	_create_ui()

func _create_ui() -> void:
	var bg = ColorRect.new()
	bg.color = Color(0.02, 0.03, 0.05, 0.7)
	bg.anchor_right = 1.0
	bg.anchor_bottom = 1.0
	add_child(bg)

	panel_container = PanelContainer.new()
	panel_container.custom_minimum_size = Vector2(520, 360)
	panel_container.anchor_left = 0.5
	panel_container.anchor_top = 0.5
	panel_container.anchor_right = 0.5
	panel_container.anchor_bottom = 0.5
	panel_container.offset_left = -260.0
	panel_container.offset_top = -180.0
	panel_container.offset_right = 260.0
	panel_container.offset_bottom = 180.0

	var sb = StyleBoxFlat.new()
	sb.bg_color = Color(0.1, 0.12, 0.16, 0.96)
	sb.border_width_left = 2
	sb.border_width_top = 2
	sb.border_width_right = 2
	sb.border_width_bottom = 2
	sb.border_color = Color(0.85, 0.72, 0.42, 0.9)
	sb.corner_radius_top_left = 6
	sb.corner_radius_top_right = 6
	sb.corner_radius_bottom_right = 6
	sb.corner_radius_bottom_left = 6
	panel_container.add_theme_stylebox_override("panel", sb)
	add_child(panel_container)

	var main_vbox = VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 8)
	panel_container.add_child(main_vbox)

	name_label = Label.new()
	name_label.text = "Citizen Name"
	name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_label.add_theme_font_size_override("font_size", 16)
	name_label.add_theme_color_override("font_color", Color(1.0, 0.85, 0.45))
	main_vbox.add_child(name_label)

	role_label = Label.new()
	role_label.text = "Occupation: Freeman"
	role_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	role_label.add_theme_font_size_override("font_size", 12)
	role_label.add_theme_color_override("font_color", Color(0.7, 0.8, 0.9))
	main_vbox.add_child(role_label)

	morale_label = Label.new()
	morale_label.text = "Morale: 85% [Content]"
	morale_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	morale_label.add_theme_font_size_override("font_size", 11)
	morale_label.add_theme_color_override("font_color", Color(0.5, 0.9, 0.5))
	main_vbox.add_child(morale_label)

	var sep = HSeparator.new()
	main_vbox.add_child(sep)

	speech_label = Label.new()
	speech_label.text = '"Greetings, Sire!"'
	speech_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	speech_label.custom_minimum_size = Vector2(0, 60)
	speech_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	speech_label.add_theme_font_size_override("font_size", 13)
	main_vbox.add_child(speech_label)

	var sep2 = HSeparator.new()
	main_vbox.add_child(sep2)

	action_vbox = VBoxContainer.new()
	action_vbox.add_theme_constant_override("separation", 6)
	main_vbox.add_child(action_vbox)

	_create_button(action_vbox, "🍞 Give Fresh Ration (+15 Morale)", _on_give_ration_pressed)
	_create_button(action_vbox, "👑 Monarch's Inspiration (+5 Morale)", _on_inspire_pressed)
	_create_button(action_vbox, "↩ Dismiss (Close)", close_dialogue)

func _create_button(parent: Node, text: String, callback: Callable) -> Button:
	var btn = Button.new()
	btn.text = text
	btn.custom_minimum_size = Vector2(0, 32)
	btn.pressed.connect(callback)
	parent.add_child(btn)
	return btn

func open_dialogue(citizen: Node, is_winter: bool = false) -> void:
	if not citizen:
		return
	current_citizen = citizen
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

	var cname = citizen.name if "name" in citizen else "Yeoman Citizen"
	var crole = citizen.current_role if "current_role" in citizen else 0
	var cmorale = citizen.morale if "morale" in citizen else 75.0

	name_label.text = "🗣️ %s" % cname
	role_label.text = "Occupation: %s" % _get_role_name(crole)
	morale_label.text = "Morale: %.0f%% [%s]" % [cmorale, _get_morale_adjective(cmorale)]
	speech_label.text = '"%s"' % get_dialogue_line(crole, cmorale, is_winter)

func get_dialogue_line(role_id: int, morale: float, is_winter: bool) -> String:
	if morale < 40.0:
		return "Sire... rations are scarce and our spirits falter. We yearn for bread and warmth."
	if is_winter:
		return "The winter frost is harsh upon the realm, my Lord. May the hearth stay well-stoked."

	var lines = ROLE_DIALOGUE.get(role_id, ROLE_DIALOGUE[0])
	var rand_idx = randi() % lines.size()
	return lines[rand_idx]

func _on_give_ration_pressed() -> void:
	if not current_citizen:
		return
	if "morale" in current_citizen:
		current_citizen.morale = minf(100.0, current_citizen.morale + 15.0)
		morale_label.text = "Morale: %.0f%% [%s]" % [current_citizen.morale, _get_morale_adjective(current_citizen.morale)]
	speech_label.text = '"A thousand blessings upon you, generous Monarch! This fresh bread warms my heart!"'
	var cname = current_citizen.name if "name" in current_citizen else "Citizen"
	ration_offered.emit(cname)

func _on_inspire_pressed() -> void:
	if not current_citizen:
		return
	if "morale" in current_citizen:
		current_citizen.morale = minf(100.0, current_citizen.morale + 5.0)
		morale_label.text = "Morale: %.0f%% [%s]" % [current_citizen.morale, _get_morale_adjective(current_citizen.morale)]
	speech_label.text = '"For King and Country! We shall toil with renewed vigor under your banner!"'
	var cname = current_citizen.name if "name" in current_citizen else "Citizen"
	inspiration_given.emit(cname)

func close_dialogue() -> void:
	visible = false
	current_citizen = null
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	dialogue_closed.emit()

func _get_role_name(role_id: int) -> String:
	match role_id:
		0: return "Unassigned Freeman"
		1: return "Norfolk Agronomist Farmer"
		2: return "Royal Forester & Lumberjack"
		3: return "Subterranean Miner"
		4: return "Guild Baker"
		5: return "Metallurgist Blacksmith"
		6: return "Feudal Militia Guard"
		_: return "Subject of the Realm"

func _get_morale_adjective(val: float) -> String:
	if val >= 85.0: return "Exultant"
	if val >= 70.0: return "Content"
	if val >= 50.0: return "Enduring"
	if val >= 30.0: return "Discontent"
	return "Rebellious"
