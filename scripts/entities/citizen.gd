class_name Citizen
extends CharacterBody3D

## Represents a living, working medieval citizen in the kingdom.

enum Role {
	UNASSIGNED,
	FARMER,
	BAKER,
	LUMBERJACK,
	MINER,
	BLACKSMITH,
	GUARD
}

enum State {
	IDLE,
	MOVING_TO_WORK,
	WORKING,
	MOVING_TO_STORAGE,
	EATING,
	SLEEPING,
	FLEEING
}

@export var citizen_name: String = "Peasant"
@export var current_role: Role = Role.UNASSIGNED
@export var current_state: State = State.IDLE

var health: float = 100.0
var hunger: float = 0.0 # 0 = full, 100 = starving
var energy: float = 100.0

var workplace_position: Vector3 = Vector3.ZERO
var home_position: Vector3 = Vector3.ZERO
var work_timer: float = 0.0
var work_duration: float = 5.0 # seconds to complete 1 cycle of work

@onready var nav_agent: NavigationAgent3D = NavigationAgent3D.new()

func _ready() -> void:
	add_child(nav_agent)
	nav_agent.velocity_computed.connect(_on_velocity_computed)

func set_role(new_role: Role, work_pos: Vector3 = Vector3.ZERO) -> void:
	current_role = new_role
	workplace_position = work_pos
	if current_role == Role.UNASSIGNED:
		current_state = State.IDLE
	else:
		move_to(workplace_position)
		current_state = State.MOVING_TO_WORK

func move_to(target: Vector3) -> void:
	nav_agent.target_position = target

func _physics_process(delta: float) -> void:
	# Passive hunger increment
	hunger += delta * 0.5
	if hunger >= 100.0:
		health -= delta * 2.0 # starvation damage
		
	match current_state:
		State.IDLE:
			# Wander or rest
			pass
		State.MOVING_TO_WORK:
			if nav_agent.is_navigation_finished():
				current_state = State.WORKING
				work_timer = 0.0
			else:
				var next_path_pos = nav_agent.get_next_path_position()
				var dir = (next_path_pos - global_position).normalized()
				velocity = dir * 3.0
				move_and_slide()
		State.WORKING:
			work_timer += delta
			if work_timer >= work_duration:
				work_timer = 0.0
				_finish_work_cycle()
		State.FLEEING:
			# Danger response
			pass

func _finish_work_cycle() -> void:
	# Work completed, trigger animation or notify supply chain
	pass

func _on_velocity_computed(safe_velocity: Vector3) -> void:
	velocity = safe_velocity
	move_and_slide()
