class_name Projectile
extends Node3D

## Ballistic Projectile Engine (Arrow / Bolt).
## Simulates parabolic ballistic trajectory y(t) = y0 + vy*t - 0.5*g*t^2,
## raycast collision detection against entities (Bandits, Player) and voxel terrain.

signal impacted(hit_target: Node, hit_point: Vector3)

var velocity: Vector3 = Vector3.ZERO
var gravity: float = 9.8
var damage: float = 35.0
var shooter: Node = null
var lifetime: float = 6.0
var age: float = 0.0
var is_stuck: bool = false

var model_instance: Node3D

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	var glb_path = "res://assets/models/arrow.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_instance = scene_res.instantiate()
			add_child(model_instance)

func launch(start_pos: Vector3, direction: Vector3, speed: float, dmg: float, p_shooter: Node = null) -> void:
	global_position = start_pos
	velocity = direction.normalized() * speed
	damage = dmg
	shooter = p_shooter
	if velocity.length_squared() > 0.01:
		look_at(global_position + velocity, Vector3.UP)

func _process(delta: float) -> void:
	if is_stuck:
		return
		
	age += delta
	if age >= lifetime:
		queue_free()
		return
		
	# Ballistic arc integration
	velocity.y -= gravity * delta
	var step = velocity * delta
	var next_pos = global_position + step
	
	# Rotate towards flight vector
	if velocity.length_squared() > 0.1:
		var target_look = global_position + velocity
		if abs(velocity.normalized().dot(Vector3.UP)) < 0.99:
			look_at(target_look, Vector3.UP)
			
	# Raycast check along trajectory
	var space_state = get_world_3d().direct_space_state
	var query = PhysicsRayQueryParameters3D.create(global_position, next_pos)
	if shooter is CollisionObject3D:
		query.exclude = [shooter.get_rid()]
		
	var result = space_state.intersect_ray(query)
	if result:
		_handle_impact(result)
	else:
		global_position = next_pos

func _handle_impact(result: Dictionary) -> void:
	var hit_collider = result.get("collider")
	var hit_pos = result.get("position", global_position)
	
	emit_signal("impacted", hit_collider, hit_pos)
	
	# Check if hit Bandit enemy
	if hit_collider and hit_collider.has_method("take_damage"):
		var knockback = velocity.normalized() * 3.5
		hit_collider.take_damage(damage, knockback)
		queue_free()
		return
		
	# Check if hit Player (if shot by bandit)
	if hit_collider is Player:
		hit_collider.take_damage(damage)
		queue_free()
		return
		
	# Hit terrain or static geometry: stick into surface
	global_position = hit_pos
	is_stuck = true
	# Fade out and clean up after 2.5 seconds
	var tween = create_tween()
	tween.tween_interval(2.5)
	tween.tween_callback(queue_free)
