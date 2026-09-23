class_name BanditWarlord
extends CharacterBody3D

## Feudal Raid Boss: Bandit Warlord.
## High hit-point heavily armored raider chief wielding a massive battleaxe.
## Guarantees dropping Legendary Runestone Affixes (Dragon's Breath, Vampiric Leech, Thunderstrike)
## and refined steel ingots upon defeat.

signal defeated(warlord: BanditWarlord, loot: Dictionary)
signal attack_landed(warlord: BanditWarlord, target: Node3D, damage: float)

var max_health: float = 160.0
var health: float = 160.0
var move_speed: float = 3.2
var attack_damage: float = 26.0
var attack_range: float = 2.4
var attack_cooldown: float = 1.8
var attack_timer: float = 0.0

var voxel_world: VoxelWorld
var pathfinder: GridPathfinder3D
var current_path: Array[Vector3] = []
var path_index: int = 0
var target_entity: Node3D = null

var collision_shape: CollisionShape3D
var health_bar_label: Label3D
var flash_timer: float = 0.0

const GRAVITY: float = 16.0

func _ready() -> void:
	add_to_group("bandits")
	_setup_visuals()
	if voxel_world:
		pathfinder = GridPathfinder3D.new(voxel_world)

func _setup_visuals() -> void:
	collision_shape = CollisionShape3D.new()
	var cap = CapsuleShape3D.new()
	cap.radius = 0.45
	cap.height = 2.1
	collision_shape.shape = cap
	collision_shape.position = Vector3(0, 1.05, 0)
	add_child(collision_shape)

	var glb_path = "res://assets/models/bandit_warlord.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			var inst = scene_res.instantiate()
			add_child(inst)

	health_bar_label = Label3D.new()
	health_bar_label.text = "👑 Bandit Warlord (Boss)\n[ 160 / 160 ]"
	health_bar_label.position = Vector3(0, 2.4, 0)
	health_bar_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	health_bar_label.font_size = 28
	health_bar_label.modulate = Color(1.0, 0.25, 0.25)
	add_child(health_bar_label)

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
		
	if attack_timer > 0.0:
		attack_timer = maxf(0.0, attack_timer - delta)
		
	if flash_timer > 0.0:
		flash_timer = maxf(0.0, flash_timer - delta)

	if target_entity and is_instance_valid(target_entity):
		var dist = global_position.distance_to(target_entity.global_position)
		if dist <= attack_range:
			velocity.x = 0
			velocity.z = 0
			_try_melee_strike(target_entity)
		else:
			_advance_along_path(delta)
			
	move_and_slide()

func set_target(target: Node3D) -> void:
	target_entity = target
	_recalculate_path()

func _recalculate_path() -> void:
	if not pathfinder or not target_entity:
		return
	current_path = pathfinder.find_path(global_position, target_entity.global_position)
	path_index = 0

func _advance_along_path(delta: float) -> void:
	if current_path.is_empty() or path_index >= current_path.size():
		return
	var target = current_path[path_index]
	var diff = target - global_position
	diff.y = 0
	if diff.length() < 0.6:
		path_index += 1
		if path_index >= current_path.size():
			return
		target = current_path[path_index]
		diff = target - global_position
		diff.y = 0
		
	var dir = diff.normalized()
	velocity.x = dir.x * move_speed
	velocity.z = dir.z * move_speed
	if dir.length_squared() > 0.01:
		var target_rot = atan2(-dir.x, -dir.z)
		rotation.y = lerp_angle(rotation.y, target_rot, 8.0 * delta)

func _try_melee_strike(target: Node3D) -> void:
	if attack_timer <= 0.0:
		attack_timer = attack_cooldown
		emit_signal("attack_landed", self, target, attack_damage)
		if target.has_method("take_damage"):
			target.take_damage(attack_damage)

func take_damage(amount: float, knockback: Vector3 = Vector3.ZERO) -> void:
	health = maxf(0.0, health - amount)
	velocity += knockback * 0.4 # High mass resistance
	flash_timer = 0.2
	
	if health_bar_label:
		health_bar_label.text = "👑 Bandit Warlord (Boss)\n[ %d / %d ]" % [int(health), int(max_health)]
		
	if health <= 0.0:
		_on_defeated()

func _on_defeated() -> void:
	var legendary_runes = [
		EnchantmentManager.AFFIX_DRAGONS_BREATH,
		EnchantmentManager.AFFIX_VAMPIRIC_LEECH,
		EnchantmentManager.AFFIX_THUNDERSTRIKE,
		EnchantmentManager.AFFIX_WINDSTRIDER,
		EnchantmentManager.AFFIX_FORTRESS_HEART
	]
	var dropped_affix = legendary_runes[randi() % legendary_runes.size()]
	
	var loot = {
		"coins": randi_range(25, 45),
		"steel_ingot": randi_range(2, 4),
		"blood_vial": 3,
		"legendary_rune": dropped_affix
	}
	emit_signal("defeated", self, loot)
	queue_free()
