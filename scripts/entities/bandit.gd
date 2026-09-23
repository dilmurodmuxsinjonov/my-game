class_name Bandit
extends CharacterBody3D

## Feudal Bandit Raider.
## Navigates via 3D Grid Pathfinder, raids kingdom stockpiles, and engages in melee combat with player and guards.

signal defeated(bandit: Bandit, loot: Dictionary)
signal attack_landed(bandit: Bandit, target: Node3D, damage: float)

var max_health: float = 60.0
var health: float = 60.0
var move_speed: float = 3.6
var attack_damage: float = 12.0
var attack_range: float = 2.0
var attack_cooldown: float = 1.4
var attack_timer: float = 0.0

var voxel_world: VoxelWorld
var pathfinder: GridPathfinder3D
var current_path: Array[Vector3] = []
var path_index: int = 0
var target_entity: Node3D = null

# Visual components
var model_mesh: MeshInstance3D
var collision_shape: CollisionShape3D
var health_bar_label: Label3D
var flash_timer: float = 0.0
var default_material: StandardMaterial3D
var flash_material: StandardMaterial3D

const GRAVITY: float = 16.0

func _ready() -> void:
	add_to_group("bandits")
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
	
	# Load Blender-generated bandit model
	var glb_path = "res://assets/models/bandit.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)
	else:
		# Fallback capsule mesh
		model_mesh = MeshInstance3D.new()
		var body_mesh = CapsuleMesh.new()
		body_mesh.radius = 0.35
		body_mesh.height = 1.7
		model_mesh.mesh = body_mesh
		model_mesh.position = Vector3(0, 0.85, 0)
		
		default_material = StandardMaterial3D.new()
		default_material.albedo_color = Color(0.35, 0.15, 0.15) # Crimson raider tunic
		default_material.roughness = 0.8
		model_mesh.material_override = default_material
		add_child(model_mesh)
	
	flash_material = StandardMaterial3D.new()
	flash_material.albedo_color = Color(1.0, 0.2, 0.2)
	flash_material.emission_enabled = true
	flash_material.emission = Color(1.0, 0.1, 0.1)
	flash_material.emission_energy_multiplier = 2.0
	
	# 3D Health Bar
	health_bar_label = Label3D.new()
	health_bar_label.text = "☠️ Bandit Raider [60/60]"
	health_bar_label.position = Vector3(0, 2.05, 0)
	health_bar_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	health_bar_label.font_size = 24
	health_bar_label.modulate = Color(1.0, 0.3, 0.3)
	add_child(health_bar_label)

func set_target(target: Node3D) -> void:
	target_entity = target
	_recalculate_path()

func _recalculate_path() -> void:
	if not target_entity or not pathfinder:
		return
	current_path = pathfinder.find_path(global_position, target_entity.global_position)
	path_index = 0

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
		
	# Damage flash timer
	if flash_timer > 0.0:
		flash_timer -= delta
		if flash_timer <= 0.0 and model_mesh:
			model_mesh.material_override = default_material
			
	attack_timer += delta
	
	# Check target distance
	if target_entity and is_instance_valid(target_entity):
		var dist = global_position.distance_to(target_entity.global_position)
		if dist <= attack_range:
			velocity.x = 0
			velocity.z = 0
			if attack_timer >= attack_cooldown:
				attack_timer = 0.0
				_perform_attack()
		else:
			_follow_path(delta)
	else:
		velocity.x = 0
		velocity.z = 0
		
	move_and_slide()

func _follow_path(delta: float) -> void:
	if current_path.is_empty() or path_index >= current_path.size():
		if target_entity:
			_recalculate_path()
		return
		
	var target_pos = current_path[path_index]
	var diff = target_pos - global_position
	diff.y = 0
	
	if diff.length() < 0.6:
		path_index += 1
		if path_index >= current_path.size():
			return
		target_pos = current_path[path_index]
		diff = target_pos - global_position
		diff.y = 0
		
	var dir = diff.normalized()
	velocity.x = dir.x * move_speed
	velocity.z = dir.z * move_speed
	
	if dir.length_squared() > 0.01:
		var target_rot = atan2(-dir.x, -dir.z)
		rotation.y = lerp_angle(rotation.y, target_rot, 10.0 * delta)

func _perform_attack() -> void:
	if not target_entity:
		return
	if target_entity.has_method("take_damage"):
		target_entity.take_damage(attack_damage)
		emit_signal("attack_landed", self, target_entity, attack_damage)

func take_damage(amount: float, knockback: Vector3 = Vector3.ZERO) -> void:
	health = maxf(0.0, health - amount)
	if health_bar_label:
		health_bar_label.text = "☠️ Bandit Raider [%d/%d]" % [int(health), int(max_health)]
		
	# Damage flash
	flash_timer = 0.15
	if model_mesh:
		model_mesh.material_override = flash_material
		
	# Apply knockback
	if knockback != Vector3.ZERO:
		velocity += knockback * 5.0
		
	if health <= 0.0:
		_die()

func _die() -> void:
	var loot = {
		"iron_ore": 1,
		"coins": randi_range(3, 8),
		"bread": 1,
		"blood_vial": 1
	}
	emit_signal("defeated", self, loot)
	queue_free()
