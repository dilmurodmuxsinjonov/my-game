class_name GuardPost
extends StaticBody3D

## Barracks Guard Sentry Post & Weapons Rack.
## Establishes a designated military station and weapons stockpile for garrison soldiers.
## Guards stationed here patrol a 16-meter defense radius, intercept hostiles,
## and equip halberds and heater shields (+15 defense rating) during raids.

signal sentry_alert_triggered(intruder_position: Vector3)

@export var defense_radius: float = 16.0
@export var max_guards_assigned: int = 2

var assigned_guards: Array[Citizen] = []
var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null
var torch_light: OmniLight3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	add_to_group("military_posts")
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.6, 2.2, 1.0)
	collision_box.shape = box
	collision_box.position = Vector3(0, 1.1, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/guard_post.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	torch_light = OmniLight3D.new()
	torch_light.light_color = Color(1.0, 0.55, 0.15)
	torch_light.light_energy = 1.6
	torch_light.omni_range = 5.0
	torch_light.position = Vector3(-0.58, 1.66, -0.12)
	add_child(torch_light)

	prompt_label = Label3D.new()
	prompt_label.text = "🛡️ Garrison Sentry Post\nGuards: 0/%d | Defense: 16m\n[E] Assign Sentry Patrol" % max_guards_assigned
	prompt_label.position = Vector3(0, 2.4, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 20
	prompt_label.modulate = Color(0.9, 0.35, 0.25)
	add_child(prompt_label)

func assign_guard(guard: Citizen) -> bool:
	if assigned_guards.size() >= max_guards_assigned:
		return false
	if not assigned_guards.has(guard):
		assigned_guards.append(guard)
		_update_prompt()
		return true
	return false

func alert_sentries(intruder_pos: Vector3) -> void:
	emit_signal("sentry_alert_triggered", intruder_pos)
	for g in assigned_guards:
		if is_instance_valid(g) and g.has_method("engage_threat"):
			g.engage_threat(intruder_pos)

func _update_prompt() -> void:
	if not prompt_label:
		return
	prompt_label.text = "🛡️ Garrison Sentry Post\nGuards: %d/%d (Armed & Vigilant)\n[E] Sentry Roster" % [
		assigned_guards.size(), max_guards_assigned
	]
	prompt_label.modulate = Color(0.3, 0.95, 0.6) if assigned_guards.size() > 0 else Color(0.9, 0.45, 0.25)

# --- Static Simulation & Balance Calculations ---

static func calculate_defense_score(guard_count: int, has_halberds: bool) -> float:
	var base_defense = float(guard_count) * 20.0
	if has_halberds:
		base_defense *= 1.35 # +35% polearm formation multiplier
	return base_defense
