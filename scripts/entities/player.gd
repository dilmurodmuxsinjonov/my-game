class_name Player
extends CharacterBody3D

## First-Person Monarch Controller.
## Follows the Single Persistent Monarch Paradigm: No dynasty, no permadeath;
## if fallen in battle, monarch recuperates and respawns at the royal castle hearth.

signal health_changed(new_health: float, max_health: float)
signal stamina_changed(new_stamina: float, max_stamina: float)
signal hunger_changed(new_hunger: float, max_hunger: float)
signal hotbar_slot_changed(slot_index: int, item_data: Dictionary)
signal block_action_performed(action: String, block_pos: Vector3i, block_type: int)
signal interact_requested(target: Node3D)
signal open_crafting_requested()

# Movement constants
const WALK_SPEED: float = 5.0
const SPRINT_SPEED: float = 8.5
const JUMP_VELOCITY: float = 6.0
const GRAVITY: float = 18.0
const MOUSE_SENSITIVITY: float = 0.003
const REACH_DISTANCE: float = 5.0

# Monarch Vitals
var max_health: float = 100.0
var health: float = 100.0
var max_stamina: float = 100.0
var stamina: float = 100.0
var max_hunger: float = 100.0
var hunger: float = 0.0 # 0 = satisfied, 100 = starving

# Nodes
@onready var head: Node3D = Node3D.new()
@onready var camera: Camera3D = Camera3D.new()
@onready var raycast: RayCast3D = RayCast3D.new()
@onready var collision_shape: CollisionShape3D = CollisionShape3D.new()
@onready var hand_anchor: Node3D = Node3D.new()

# External references
var voxel_world: VoxelWorld
var supply_chain: SupplyChain
var hovered_workstation: Workstation = null

# Hotbar Inventory (8 slots)
var active_slot: int = 0
var hotbar: Array = [
	{"name": "Iron Pickaxe", "type": "tool", "tool_type": "pickaxe", "icon": "⛏️", "block_type": 0, "count": 1},
	{"name": "Wood Axe", "type": "tool", "tool_type": "axe", "icon": "🪓", "block_type": 0, "count": 1},
	{"name": "Knight Sword", "type": "tool", "tool_type": "sword", "icon": "⚔️", "block_type": 0, "count": 1},
	{"name": "Cobblestone", "type": "block", "block_type": VoxelChunk.BlockType.COBBLESTONE, "icon": "🪨", "count": 64},
	{"name": "Wood Planks", "type": "block", "block_type": VoxelChunk.BlockType.PLANKS, "icon": "🪵", "count": 64},
	{"name": "Stone Blocks", "type": "block", "block_type": VoxelChunk.BlockType.STONE, "icon": "🧱", "count": 64},
	{"name": "Farmland Hoe", "type": "tool", "tool_type": "hoe", "icon": "🌾", "block_type": VoxelChunk.BlockType.FARMLAND, "count": 1},
	{"name": "Ration Bread", "type": "food", "nutrition": 25.0, "icon": "🍞", "count": 16}
]

var respawn_position: Vector3 = Vector3(32.0, 25.0, 32.0)

func _ready() -> void:
	_setup_nodes()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	emit_signal("health_changed", health, max_health)
	emit_signal("stamina_changed", stamina, max_stamina)
	emit_signal("hunger_changed", hunger, max_hunger)
	emit_signal("hotbar_slot_changed", active_slot, hotbar[active_slot])

func _setup_nodes() -> void:
	# Add collision capsule
	var capsule = CapsuleShape3D.new()
	capsule.radius = 0.4
	capsule.height = 1.8
	collision_shape.shape = capsule
	collision_shape.position = Vector3(0, 0.9, 0)
	add_child(collision_shape)
	
	# Head and Camera
	head.name = "Head"
	head.position = Vector3(0, 1.65, 0)
	add_child(head)
	
	camera.name = "Camera3D"
	camera.current = true
	head.add_child(camera)
	
	# Interaction Raycast
	raycast.name = "InteractionRay"
	raycast.target_position = Vector3(0, 0, -REACH_DISTANCE)
	raycast.collision_mask = 1
	camera.add_child(raycast)
	
	# Hand anchor for held 3D tools/items
	hand_anchor.name = "HandAnchor"
	hand_anchor.position = Vector3(0.35, -0.3, -0.6)
	camera.add_child(hand_anchor)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * MOUSE_SENSITIVITY)
		head.rotate_x(-event.relative.y * MOUSE_SENSITIVITY)
		head.rotation.x = clampf(head.rotation.x, deg_to_rad(-89.0), deg_to_rad(89.0))
		
	elif event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if Input.mouse_mode == Input.MOUSE_MODE_VISIBLE:
				Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
			else:
				_handle_primary_action()
		elif event.button_index == MOUSE_BUTTON_RIGHT and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
			_handle_secondary_action()
		elif event.button_index == MOUSE_BUTTON_WHEEL_UP:
			_select_slot((active_slot - 1 + 8) % 8)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_select_slot((active_slot + 1) % 8)
			
	elif event is InputEventKey and event.pressed:
		if event.keycode >= KEY_1 and event.keycode <= KEY_8:
			_select_slot(event.keycode - KEY_1)
		elif event.keycode == KEY_E and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
			if hovered_workstation:
				emit_signal("interact_requested", hovered_workstation)
			else:
				emit_signal("open_crafting_requested")
		elif event.keycode == KEY_ESCAPE:
			if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
				Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
			else:
				Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _select_slot(index: int) -> void:
	active_slot = clampi(index, 0, 7)
	emit_signal("hotbar_slot_changed", active_slot, hotbar[active_slot])

func _physics_process(delta: float) -> void:
	_update_vitals(delta)
	_handle_movement(delta)
	_check_hovered_interactive()

func _check_hovered_interactive() -> void:
	if raycast and raycast.is_colliding():
		var col = raycast.get_collider()
		if col is Workstation:
			if hovered_workstation != col:
				if hovered_workstation:
					hovered_workstation.set_prompt_visible(false)
				hovered_workstation = col
				hovered_workstation.set_prompt_visible(true)
			return
	if hovered_workstation:
		hovered_workstation.set_prompt_visible(false)
		hovered_workstation = null

func _handle_movement(delta: float) -> void:
	# Gravity
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
	else:
		if Input.is_key_pressed(KEY_SPACE):
			if stamina >= 10.0:
				velocity.y = JUMP_VELOCITY
				stamina -= 8.0
				emit_signal("stamina_changed", stamina, max_stamina)
				
	# Input direction
	var input_dir: Vector2 = Vector2.ZERO
	if Input.is_key_pressed(KEY_W): input_dir.y -= 1
	if Input.is_key_pressed(KEY_S): input_dir.y += 1
	if Input.is_key_pressed(KEY_A): input_dir.x -= 1
	if Input.is_key_pressed(KEY_D): input_dir.x += 1
	input_dir = input_dir.normalized()
	
	# Sprint check
	var is_sprinting = Input.is_key_pressed(KEY_SHIFT) and input_dir != Vector2.ZERO and stamina > 5.0
	var speed = SPRINT_SPEED if is_sprinting else WALK_SPEED
	
	if is_sprinting:
		stamina = maxf(0.0, stamina - delta * 12.0)
		emit_signal("stamina_changed", stamina, max_stamina)
	else:
		stamina = minf(max_stamina, stamina + delta * 15.0)
		emit_signal("stamina_changed", stamina, max_stamina)
		
	# World movement vector
	var forward = -transform.basis.z
	var right = transform.basis.x
	var direction = (right * input_dir.x + forward * -input_dir.y).normalized()
	
	if direction != Vector3.ZERO:
		velocity.x = lerp(velocity.x, direction.x * speed, 12.0 * delta)
		velocity.z = lerp(velocity.z, direction.z * speed, 12.0 * delta)
	else:
		velocity.x = lerp(velocity.x, 0.0, 14.0 * delta)
		velocity.z = lerp(velocity.z, 0.0, 14.0 * delta)
		
	move_and_slide()

func _update_vitals(delta: float) -> void:
	# Passive hunger (1 point per 10 real seconds)
	hunger = minf(max_hunger, hunger + delta * 0.1)
	emit_signal("hunger_changed", hunger, max_hunger)
	
	# Starvation damage
	if hunger >= 100.0:
		take_damage(delta * 2.0)
	elif hunger < 30.0 and health < max_health:
		# Passive health regeneration when well fed
		health = minf(max_health, health + delta * 1.5)
		emit_signal("health_changed", health, max_health)

func take_damage(amount: float) -> void:
	health = maxf(0.0, health - amount)
	emit_signal("health_changed", health, max_health)
	if health <= 0.0:
		_respawn_monarch()

func _respawn_monarch() -> void:
	# Single Persistent Monarch Paradigm: Respawn in castle infirmary, realm remains intact!
	global_position = respawn_position
	velocity = Vector3.ZERO
	health = 50.0
	hunger = 40.0
	stamina = 100.0
	emit_signal("health_changed", health, max_health)
	emit_signal("hunger_changed", hunger, max_hunger)
	emit_signal("stamina_changed", stamina, max_stamina)

func _handle_primary_action() -> void:
	if not raycast or not raycast.is_colliding():
		return
		
	var collider = raycast.get_collider()
	var hit_point = raycast.get_collision_point()
	var hit_normal = raycast.get_collision_normal()
	
	var item = hotbar[active_slot]
	
	if voxel_world and (collider is VoxelChunk or collider == voxel_world):
		var result = voxel_world.mine_block(hit_point, hit_normal)
		if result["success"]:
			emit_signal("block_action_performed", "mine", result["pos"], result["type"])
			_add_resource_from_mined_block(result["type"])

func _handle_secondary_action() -> void:
	var item = hotbar[active_slot]
	
	# 1. Food consumption
	if item.get("type") == "food" and item.get("count", 0) > 0:
		var nutrition = item.get("nutrition", 20.0)
		hunger = maxf(0.0, hunger - nutrition)
		health = minf(max_health, health + 10.0)
		item["count"] -= 1
		emit_signal("hunger_changed", hunger, max_hunger)
		emit_signal("health_changed", health, max_health)
		emit_signal("hotbar_slot_changed", active_slot, item)
		return
		
	if not raycast or not raycast.is_colliding():
		return
		
	var collider = raycast.get_collider()
	var hit_point = raycast.get_collision_point()
	var hit_normal = raycast.get_collision_normal()
	
	# 2. Farmland hoe tilling
	if item.get("tool_type") == "hoe" and voxel_world:
		var center = hit_point - hit_normal * 0.4
		var target_pos = Vector3i(int(floor(center.x)), int(floor(center.y)), int(floor(center.z)))
		var cur_type = voxel_world.get_block_world(target_pos)
		if cur_type == VoxelChunk.BlockType.GRASS or cur_type == VoxelChunk.BlockType.DIRT:
			voxel_world.set_block_world(target_pos, VoxelChunk.BlockType.FARMLAND, true)
			emit_signal("block_action_performed", "till", target_pos, VoxelChunk.BlockType.FARMLAND)
			return

	# 3. Block placement
		var btype = item.get("block_type", VoxelChunk.BlockType.STONE)
		var result = voxel_world.place_block(hit_point, hit_normal, btype)
		if result["success"]:
			item["count"] -= 1
			emit_signal("block_action_performed", "place", result["pos"], result["type"])
			emit_signal("hotbar_slot_changed", active_slot, item)

func _add_resource_from_mined_block(block_type: int) -> void:
	if not supply_chain:
		return
	match block_type:
		VoxelChunk.BlockType.STONE, VoxelChunk.BlockType.COBBLESTONE:
			supply_chain.add_resource("stone", 1)
		VoxelChunk.BlockType.WOOD:
			supply_chain.add_resource("logs", 1)
		VoxelChunk.BlockType.IRON_ORE:
			supply_chain.add_resource("iron_ore", 1)
		VoxelChunk.BlockType.COAL_ORE:
			supply_chain.add_resource("coal", 1)
		VoxelChunk.BlockType.WHEAT_CROP:
			supply_chain.add_resource("wheat", 2)
