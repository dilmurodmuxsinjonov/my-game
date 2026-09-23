class_name Citizen
extends CharacterBody3D

## Autonomous Medieval Citizen with 10-state HFSM and 3D Voxel Grid Pathfinding.

signal state_changed(citizen: Citizen, old_state: State, new_state: State)
signal work_cycle_completed(citizen: Citizen, role: Role, resource_produced: String, amount: int)

enum Role {
	UNASSIGNED = 0,
	FARMER = 1,
	BAKER = 2,
	LUMBERJACK = 3,
	MINER = 4,
	BLACKSMITH = 5,
	GUARD = 6
}

enum State {
	IDLE = 0,
	WANDER = 1,
	MOVING_TO_WORK = 2,
	WORKING = 3,
	HARVESTING = 4,
	STORING = 5,
	EATING = 6,
	SLEEPING = 7,
	HEALING = 8,
	FLEEING = 9,
	DEFENDING = 10
}

@export var citizen_name: String = "Aldous"
@export var current_role: Role = Role.UNASSIGNED
@export var current_state: State = State.IDLE

# Vitals
var max_health: float = 100.0
var health: float = 100.0
var max_hunger: float = 100.0
var hunger: float = 15.0
var energy: float = 100.0
var morale: float = 80.0

# Movement & Pathfinding
const MOVE_SPEED: float = 3.2
const GRAVITY: float = 16.0
var current_path: Array[Vector3] = []
var path_index: int = 0
var pathfinder: GridPathfinder3D
var voxel_world: VoxelWorld
var supply_chain: SupplyChain

# Guard & Defense
var shoot_cooldown: float = 0.0
var target_bandit: Node3D = null
var watchtower_ref: Node3D = null

# Locations & Timers
var workplace_pos: Vector3 = Vector3.ZERO
var home_pos: Vector3 = Vector3.ZERO
var state_timer: float = 0.0
var work_duration: float = 4.0 # Seconds per productive cycle
var wander_cooldown: float = 3.0

# Node components
var model_instance: Node3D
var nameplate: Label3D
var collision_shape: CollisionShape3D

func _ready() -> void:
	_setup_visuals()
	if voxel_world:
		pathfinder = GridPathfinder3D.new(voxel_world)

func _setup_visuals() -> void:
	collision_shape = CollisionShape3D.new()
	var cap = CapsuleShape3D.new()
	cap.radius = 0.35
	cap.height = 1.7
	collision_shape.shape = cap
	collision_shape.position = Vector3(0, 0.85, 0)
	add_child(collision_shape)
	
	# Load Blender-generated citizen model
	var glb_path = "res://assets/models/citizen.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_instance = scene_res.instantiate()
			add_child(model_instance)
	else:
		# Fallback primitive mesh
		var mi = MeshInstance3D.new()
		var mesh = CapsuleMesh.new()
		mesh.radius = 0.35
		mesh.height = 1.7
		mi.mesh = mesh
		mi.position = Vector3(0, 0.85, 0)
		add_child(mi)
		
	# 3D Nameplate & Status
	nameplate = Label3D.new()
	nameplate.text = "%s\n[%s]" % [citizen_name, _get_role_name(current_role)]
	nameplate.position = Vector3(0, 2.05, 0)
	nameplate.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	nameplate.font_size = 28
	nameplate.modulate = Color(1.0, 0.95, 0.6)
	add_child(nameplate)

func set_role(new_role: Role, work_target: Vector3 = Vector3.ZERO) -> void:
	current_role = new_role
	workplace_pos = work_target
	if nameplate:
		nameplate.text = "%s\n[%s]" % [citizen_name, _get_role_name(current_role)]
		
	if current_role == Role.UNASSIGNED:
		_transition_to(State.IDLE)
	elif current_role == Role.GUARD:
		_navigate_to(workplace_pos, State.DEFENDING)
	else:
		_navigate_to(workplace_pos, State.MOVING_TO_WORK)

func _navigate_to(target: Vector3, next_state: State) -> void:
	if not pathfinder and voxel_world:
		pathfinder = GridPathfinder3D.new(voxel_world)
		
	if pathfinder:
		current_path = pathfinder.find_path(global_position, target)
		path_index = 0
		_transition_to(next_state)
	else:
		current_path = [target]
		path_index = 0
		_transition_to(next_state)

func _physics_process(delta: float) -> void:
	_update_needs(delta)
	
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
		
	match current_state:
		State.IDLE:
			if current_role == Role.GUARD:
				_transition_to(State.DEFENDING)
			else:
				state_timer += delta
				if state_timer >= wander_cooldown:
					state_timer = 0.0
					_start_wandering()
				
		State.WANDER:
			_follow_path(delta, State.DEFENDING if current_role == Role.GUARD else State.IDLE)
			
		State.MOVING_TO_WORK:
			_follow_path(delta, State.DEFENDING if current_role == Role.GUARD else State.WORKING)
			
		State.WORKING:
			velocity.x = 0
			velocity.z = 0
			state_timer += delta
			if state_timer >= work_duration:
				state_timer = 0.0
				_complete_work_cycle()
				
		State.DEFENDING:
			velocity.x = 0
			velocity.z = 0
			_process_guard_defense(delta)
				
		State.EATING:
			velocity.x = 0
			velocity.z = 0
			state_timer += delta
			if state_timer >= 2.0:
				state_timer = 0.0
				hunger = maxf(0.0, hunger - 40.0)
				_transition_to(State.IDLE if current_role == Role.UNASSIGNED else (State.DEFENDING if current_role == Role.GUARD else State.MOVING_TO_WORK))
				
		State.FLEEING:
			_follow_path(delta, State.IDLE)

	move_and_slide()

func _follow_path(delta: float, on_reach_state: State) -> void:
	if current_path.is_empty() or path_index >= current_path.size():
		velocity.x = 0
		velocity.z = 0
		_transition_to(on_reach_state)
		return
		
	var target = current_path[path_index]
	var diff = target - global_position
	diff.y = 0 # horizontal navigation
	
	if diff.length() < 0.6:
		path_index += 1
		if path_index >= current_path.size():
			velocity.x = 0
			velocity.z = 0
			_transition_to(on_reach_state)
			return
		target = current_path[path_index]
		diff = target - global_position
		diff.y = 0
		
	var dir = diff.normalized()
	velocity.x = dir.x * MOVE_SPEED
	velocity.z = dir.z * MOVE_SPEED
	
	# Face movement direction
	if dir.length_squared() > 0.01:
		var target_rot = atan2(-dir.x, -dir.z)
		rotation.y = lerp_angle(rotation.y, target_rot, 10.0 * delta)

func _complete_work_cycle() -> void:
	var item_name: String = ""
	var item_qty: int = 1
	
	match current_role:
		Role.FARMER:
			item_name = "wheat"
			item_qty = 2
		Role.LUMBERJACK:
			item_name = "logs"
			item_qty = 2
		Role.MINER:
			item_name = "stone"
			item_qty = 2
		Role.BAKER:
			if supply_chain and supply_chain.consume_resource("wheat", 1):
				item_name = "bread"
				item_qty = 2
		Role.BLACKSMITH:
			if supply_chain and supply_chain.consume_resource("iron_ore", 1):
				item_name = "tools"
				item_qty = 1
				
	if supply_chain and item_name != "":
		supply_chain.add_resource(item_name, item_qty)
		emit_signal("work_cycle_completed", self, current_role, item_name, item_qty)

func _start_wandering() -> void:
	var rx = randf_range(-6.0, 6.0)
	var rz = randf_range(-6.0, 6.0)
	var target = global_position + Vector3(rx, 0, rz)
	_navigate_to(target, State.WANDER)

func _update_needs(delta: float) -> void:
	hunger += delta * 0.2
	if hunger >= 80.0 and current_state != State.EATING:
		# Check if kingdom has food
		if supply_chain and supply_chain.consume_resource("bread", 1):
			_transition_to(State.EATING)
		elif hunger >= 100.0:
			health -= delta * 1.5 # Starvation damage

func _transition_to(new_state: State) -> void:
	if current_state != new_state:
		var old = current_state
		current_state = new_state
		state_timer = 0.0
		emit_signal("state_changed", self, old, new_state)

func on_royal_alarm(active: bool, bunker_pos: Vector3 = Vector3(32, 0, 32)) -> void:
	if current_role == Role.GUARD:
		if active:
			_transition_to(State.DEFENDING)
	else:
		if active:
			_navigate_to(bunker_pos, State.FLEEING)
			if nameplate:
				nameplate.text = "%s\n[RETREATING TO KEEP]" % citizen_name
		else:
			_transition_to(State.IDLE)
			if nameplate:
				nameplate.text = "%s\n[%s]" % [citizen_name, _get_role_name(current_role)]

func take_damage(amount: float) -> void:
	health = maxf(0.0, health - amount)
	if nameplate:
		nameplate.text = "%s\n[%s] (HP: %d)" % [citizen_name, _get_role_name(current_role), int(health)]
	if health < 30.0 and current_role != Role.GUARD:
		_transition_to(State.FLEEING)
	if health <= 0.0:
		_transition_to(State.HEALING)
		health = 25.0

func _process_guard_defense(delta: float) -> void:
	shoot_cooldown = maxf(0.0, shoot_cooldown - delta)
	
	# Scan for bandits
	var scan_range = 24.0
	var damage_mult = 1.0
	if watchtower_ref:
		scan_range *= Watchtower.RANGE_BONUS_MULT
		damage_mult *= Watchtower.DAMAGE_BONUS_MULT
		
	if not target_bandit or not is_instance_valid(target_bandit) or target_bandit.health <= 0.0 or global_position.distance_to(target_bandit.global_position) > scan_range:
		target_bandit = null
		var bandits = get_tree().get_nodes_in_group("bandits")
		var closest_dist = scan_range
		for b in bandits:
			if b is Node3D and is_instance_valid(b) and b.get("health") > 0.0:
				var d = global_position.distance_to(b.global_position)
				if d < closest_dist:
					closest_dist = d
					target_bandit = b
					
	if target_bandit and is_instance_valid(target_bandit):
		var diff = target_bandit.global_position - global_position
		diff.y = 0
		if diff.length_squared() > 0.01:
			var target_rot = atan2(-diff.x, -diff.z)
			rotation.y = lerp_angle(rotation.y, target_rot, 8.0 * delta)
			
		if shoot_cooldown <= 0.0:
			shoot_cooldown = 1.8
			_fire_arrow_at(target_bandit, damage_mult)
	else:
		state_timer += delta
		if state_timer >= 3.0:
			state_timer = 0.0
			_start_wandering()

func _fire_arrow_at(target: Node3D, dmg_mult: float) -> void:
	var proj = Projectile.new()
	var spawn_pos = global_position + Vector3(0, 1.3, 0)
	var dir = (target.global_position + Vector3(0, 0.8, 0) - spawn_pos).normalized()
	get_parent().add_child(proj)
	proj.launch(spawn_pos, dir, 32.0, 30.0 * dmg_mult, self)

func _get_role_name(r: Role) -> String:
	match r:
		Role.FARMER: return "Farmer"
		Role.BAKER: return "Baker"
		Role.LUMBERJACK: return "Lumberjack"
		Role.MINER: return "Miner"
		Role.BLACKSMITH: return "Blacksmith"
		Role.GUARD: return "Guard"
		_: return "Peasant"
