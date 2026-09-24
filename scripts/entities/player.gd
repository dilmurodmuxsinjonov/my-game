class_name Player
extends CharacterBody3D

const BlueprintConstruction = preload("res://scripts/world/blueprint_construction.gd")
const Anvil = preload("res://scripts/world/anvil.gd")
const WaterWheel = preload("res://scripts/world/water_wheel.gd")
const Millstone = preload("res://scripts/world/millstone.gd")
const TripHammer = preload("res://scripts/world/trip_hammer.gd")

## First-Person Monarch Controller.
## Follows the Single Persistent Monarch Paradigm: No dynasty, no permadeath;
## if fallen in battle, monarch recuperates and respawns at the royal castle hearth.

signal health_changed(new_health: float, max_health: float)
signal stamina_changed(new_stamina: float, max_stamina: float)
signal hunger_changed(new_hunger: float, max_hunger: float)
signal warmth_changed(new_warmth: float, max_warmth: float)
signal hotbar_slot_changed(slot_index: int, item_data: Dictionary)
signal block_action_performed(action: String, block_pos: Vector3i, block_type: int)
signal interact_requested(target: Node3D)
signal open_crafting_requested()
signal war_horn_sounded()

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
var max_warmth: float = 100.0
var warmth: float = 100.0
var ambient_temperature: float = 16.0

# Nodes
@onready var head: Node3D = Node3D.new()
@onready var camera: Camera3D = Camera3D.new()
@onready var raycast: RayCast3D = RayCast3D.new()
@onready var collision_shape: CollisionShape3D = CollisionShape3D.new()
@onready var hand_anchor: Node3D = Node3D.new()

# External references
var voxel_world: VoxelWorld
var supply_chain: SupplyChain
var hovered_interactive: Node3D = null

# Hotbar Inventory (8 slots)
var active_slot: int = 0
var hotbar: Array = [
	{"name": "Iron Pickaxe", "type": "tool", "tool_type": "pickaxe", "icon": "⛏️", "block_type": 0, "count": 1},
	{"name": "Wood Axe", "type": "tool", "tool_type": "axe", "icon": "🪓", "block_type": 0, "count": 1},
	{"name": "Knight Sword", "type": "tool", "tool_type": "sword", "icon": "⚔️", "block_type": 0, "count": 1},
	{"name": "Farmland Hoe", "type": "tool", "tool_type": "hoe", "icon": "🌾", "block_type": VoxelChunk.BlockType.FARMLAND, "count": 1},
	{"name": "Wheat Seeds", "type": "seed", "icon": "🌱", "count": 16},
	{"name": "Torch", "type": "placeable", "icon": "🕯️", "count": 8},
	{"name": "Ration Bread", "type": "food", "nutrition": 25.0, "icon": "🍞", "count": 16},
	{"name": "Cobblestone", "type": "block", "block_type": VoxelChunk.BlockType.COBBLESTONE, "icon": "🪨", "count": 64}
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
			if hovered_interactive:
				emit_signal("interact_requested", hovered_interactive)
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
		if col is Workstation or col is TradeCaravan or col is EnchanterTable or col is CookingPot or col is Anvil:
			if hovered_interactive != col:
				if hovered_interactive and hovered_interactive.has_method("set_prompt_visible"):
					hovered_interactive.set_prompt_visible(false)
				hovered_interactive = col
				if hovered_interactive and hovered_interactive.has_method("set_prompt_visible"):
					hovered_interactive.set_prompt_visible(true)
			return
	if hovered_interactive:
		if hovered_interactive.has_method("set_prompt_visible"):
			hovered_interactive.set_prompt_visible(false)
		hovered_interactive = null

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
	
	# Windstrider Legendary Affix speed bonus (+30%)
	var active_item = hotbar[active_slot]
	var enchs = active_item.get("enchantments", {})
	if EnchantmentManager.has_windstrider(enchs):
		speed *= 1.3
	
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
		
	# Thermal warmth loop
	_update_thermal_balance(delta)

func _update_thermal_balance(delta: float) -> void:
	var is_sheltered = false
	if voxel_world:
		var head_pos = Vector3i(int(floor(global_position.x)), int(floor(global_position.y + 1.8)), int(floor(global_position.z)))
		for dy in range(1, 9):
			var check_block = voxel_world.get_block_world(head_pos + Vector3i(0, dy, 0))
			if check_block != VoxelChunk.BlockType.AIR and check_block != VoxelChunk.BlockType.WATER:
				is_sheltered = true
				break
				
	var is_near_heat = false
	var scene = get_tree().current_scene
	if scene:
		for child in scene.get_children():
			if child is Torch:
				if global_position.distance_to(child.global_position) < 4.0:
					is_near_heat = true
					break
			elif child is Workstation:
				if child.station_type == Workstation.StationType.CAMPFIRE or child.station_type == Workstation.StationType.FURNACE:
					if global_position.distance_to(child.global_position) < 7.0:
						is_near_heat = true
						break

	if is_near_heat or ambient_temperature >= 15.0:
		warmth = minf(max_warmth, warmth + delta * 6.0)
	elif ambient_temperature < 5.0 and not is_sheltered:
		var cold_severity = maxf(1.0, (5.0 - ambient_temperature) * 0.4)
		warmth = maxf(0.0, warmth - delta * cold_severity)
	elif ambient_temperature < 0.0 and is_sheltered:
		warmth = maxf(0.0, warmth - delta * 0.5)

	emit_signal("warmth_changed", warmth, max_warmth)
	
	if warmth <= 0.0:
		take_damage(delta * 2.5)

func take_damage(amount: float) -> void:
	var item = hotbar[active_slot]
	var enchs = item.get("enchantments", {})
	var final_dmg = EnchantmentManager.calculate_armor_mitigation(amount, enchs)
	if EnchantmentManager.has_fortress_heart(enchs) and health < (max_health * 0.25):
		final_dmg *= 0.1 # 90% emergency barrier when critical HP
	health = maxf(0.0, health - final_dmg)
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
	warmth = 100.0
	emit_signal("health_changed", health, max_health)
	emit_signal("hunger_changed", hunger, max_hunger)
	emit_signal("stamina_changed", stamina, max_stamina)
	emit_signal("warmth_changed", warmth, max_warmth)

func _handle_primary_action() -> void:
	if not raycast or not raycast.is_colliding():
		return
		
	var collider = raycast.get_collider()
	var hit_point = raycast.get_collision_point()
	var hit_normal = raycast.get_collision_normal()
	
	var item = hotbar[active_slot]
	
	# 0. Ranged archery attack
	if item.get("tool_type") == "bow":
		_fire_player_arrow()
		return
		
	# 1. Melee combat against enemies (Bandit, BanditWarlord)
	if collider is Bandit or collider is BanditWarlord:
		var dmg = 20.0
		if item.get("tool_type") == "sword":
			dmg = 35.0
		elif item.get("tool_type") == "axe":
			dmg = 24.0
		elif item.get("tool_type") == "pickaxe":
			dmg = 16.0
			
		var enchs = item.get("enchantments", {})
		dmg = EnchantmentManager.calculate_melee_damage(dmg, enchs)
		
		# Vampiric leech life steal
		var lsteal = EnchantmentManager.apply_life_steal(dmg, enchs)
		if lsteal > 0.0:
			health = minf(max_health, health + lsteal)
			emit_signal("health_changed", health, max_health)
			
		# Dragon's breath fiery combustion
		if EnchantmentManager.has_dragons_breath(enchs):
			dmg += 8.0
			
		var knockback = -camera.global_transform.basis.z.normalized()
		collider.take_damage(dmg, knockback)
		emit_signal("block_action_performed", "attack", Vector3i.ZERO, 0)
		return
	
	# 2. Voxel mining
	if voxel_world and (collider is VoxelChunk or collider == voxel_world):
		var result = voxel_world.mine_block(hit_point, hit_normal)
		if result["success"]:
			emit_signal("block_action_performed", "mine", result["pos"], result["type"])
			_add_resource_from_mined_block(result["type"])

func _handle_secondary_action() -> void:
	var item = hotbar[active_slot]
	
	# 1. Food consumption (Hearty stews, rations, broth)
	if item.get("type") == "food" and item.get("count", 0) > 0:
		var nutrition = item.get("nutrition", 20.0)
		var warmth_bonus = item.get("warmth_bonus", 0.0)
		hunger = maxf(0.0, hunger - nutrition)
		health = minf(max_health, health + 10.0)
		if warmth_bonus > 0.0:
			warmth = minf(max_warmth, warmth + warmth_bonus)
			emit_signal("warmth_changed", warmth, max_warmth)
		item["count"] -= 1
		emit_signal("hunger_changed", hunger, max_hunger)
		emit_signal("health_changed", health, max_health)
		emit_signal("hotbar_slot_changed", active_slot, item)
		return
		
	# 2. Sound Royal War Horn (Civilian Bunker Retreat / All-Clear)
	if item.get("name") == "Royal War Horn" or item.get("tool_type") == "horn":
		emit_signal("war_horn_sounded")
		return
		
	# 3. Inscribe Rune directly onto primary weapon (slot 0)
	if item.get("type") == "rune" and item.get("count", 0) > 0:
		var target_item = hotbar[0]
		if target_item.get("type") in ["tool", "weapon", "bow"] or target_item.get("tool_type") in ["sword", "axe", "pickaxe", "bow"]:
			if not target_item.has("enchantments"):
				target_item["enchantments"] = {}
			target_item["enchantments"][item.get("enchantment", "sharpness")] = item.get("level", 1)
			item["count"] -= 1
			emit_signal("hotbar_slot_changed", active_slot, item)
			emit_signal("hotbar_slot_changed", 0, target_item)
			return
		
	if not raycast or not raycast.is_colliding():
		return
		
	var collider = raycast.get_collider()
	var hit_point = raycast.get_collision_point()
	var hit_normal = raycast.get_collision_normal()
	
	# 4. Farmland hoe tilling
	if item.get("tool_type") == "hoe" and voxel_world:
		var center = hit_point - hit_normal * 0.4
		var target_pos = Vector3i(int(floor(center.x)), int(floor(center.y)), int(floor(center.z)))
		var cur_type = voxel_world.get_block_world(target_pos)
		if cur_type == VoxelChunk.BlockType.GRASS or cur_type == VoxelChunk.BlockType.DIRT:
			voxel_world.set_block_world(target_pos, VoxelChunk.BlockType.FARMLAND, true)
			emit_signal("block_action_performed", "till", target_pos, VoxelChunk.BlockType.FARMLAND)
			return

	# 5. Seed planting on Farmland
	if (item.get("type") == "seed" or item.get("name") == "Wheat Seeds") and item.get("count", 0) > 0 and voxel_world:
		var center = hit_point - hit_normal * 0.4
		var target_pos = Vector3i(int(floor(center.x)), int(floor(center.y)), int(floor(center.z)))
		var above_pos = target_pos + Vector3i.UP
		var cur_type = voxel_world.get_block_world(target_pos)
		if cur_type == VoxelChunk.BlockType.FARMLAND and voxel_world.get_block_world(above_pos) == VoxelChunk.BlockType.AIR:
			item["count"] -= 1
			emit_signal("block_action_performed", "plant", above_pos, VoxelChunk.BlockType.WHEAT_CROP)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return

	# 6. Torch placement
	if item.get("name") == "Torch" and item.get("count", 0) > 0:
		var torch = Torch.new()
		var torch_pos = hit_point + hit_normal * 0.1
		torch.position = torch_pos
		get_tree().current_scene.add_child(torch)
		item["count"] -= 1
		emit_signal("block_action_performed", "torch", Vector3i(int(torch_pos.x), int(torch_pos.y), int(torch_pos.z)), 0)
		emit_signal("hotbar_slot_changed", active_slot, item)
		return

	# 7. Block placement
	if voxel_world and item.get("type") == "block" and item.get("count", 0) > 0:
		var btype = item.get("block_type", VoxelChunk.BlockType.STONE)
		var result = voxel_world.place_block(hit_point, hit_normal, btype)
		if result["success"]:
			item["count"] -= 1
			emit_signal("block_action_performed", "place", result["pos"], result["type"])
			emit_signal("hotbar_slot_changed", active_slot, item)
			return

	# 7.5. Holographic Blueprint Placement (MineColonies style)
	if item.get("type") == "blueprint" and item.get("count", 0) > 0:
		_place_blueprint(item, hit_point, hit_normal)
		return

	# 8. Placeable workstation placement (Furnace, Campfire, Crate, Workbench, Watchtower, Enchanter Table, Windmill, Cooking Pot, Architect Desk)
	if item.get("type") == "placeable" and item.get("count", 0) > 0 and item.get("name") != "Torch":
		var item_name = item.get("name", "")
		if "Architect" in item_name:
			var ws = Workstation.new()
			ws.station_type = Workstation.StationType.WORKBENCH
			ws.custom_name = "Architect's Drafting Desk"
			ws.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(ws)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(ws.position.x), int(ws.position.y), int(ws.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Watchtower" in item_name:
			var wt = Watchtower.new()
			wt.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(wt)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(wt.position.x), int(wt.position.y), int(wt.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Enchanter" in item_name:
			var et = EnchanterTable.new()
			et.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(et)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(et.position.x), int(et.position.y), int(et.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Windmill" in item_name:
			var wm = Windmill.new()
			wm.supply_chain = supply_chain
			wm.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(wm)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(wm.position.x), int(wm.position.y), int(wm.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Cooking Pot" in item_name:
			var cp = CookingPot.new()
			cp.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(cp)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(cp.position.x), int(cp.position.y), int(cp.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Anvil" in item_name:
			var an = Anvil.new()
			an.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(an)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(an.position.x), int(an.position.y), int(an.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Water Wheel" in item_name:
			var ww = WaterWheel.new()
			ww.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(ww)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(ww.position.x), int(ww.position.y), int(ww.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Millstone" in item_name:
			var ms = Millstone.new()
			ms.supply_chain = supply_chain
			ms.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(ms)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(ms.position.x), int(ms.position.y), int(ms.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Trip Hammer" in item_name:
			var th = TripHammer.new()
			th.supply_chain = supply_chain
			th.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(th)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(th.position.x), int(th.position.y), int(th.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return
		elif "Smoke Rack" in item_name:
			var ws = Workstation.new()
			ws.station_type = Workstation.StationType.CAMPFIRE
			ws.custom_name = "Timber Smoke Rack"
			ws.position = hit_point + hit_normal * 0.1
			get_tree().current_scene.add_child(ws)
			item["count"] -= 1
			emit_signal("block_action_performed", "place_station", Vector3i(int(ws.position.x), int(ws.position.y), int(ws.position.z)), 0)
			emit_signal("hotbar_slot_changed", active_slot, item)
			return

		var st_type = item.get("station_type", Workstation.StationType.CAMPFIRE)
		if "Furnace" in item_name:
			st_type = Workstation.StationType.FURNACE
		elif "Crate" in item_name:
			st_type = Workstation.StationType.CRATE
		elif "Campfire" in item_name:
			st_type = Workstation.StationType.CAMPFIRE
		elif "Workbench" in item_name:
			st_type = Workstation.StationType.WORKBENCH
			
		var ws = Workstation.new(st_type)
		ws.position = hit_point + hit_normal * 0.5
		get_tree().current_scene.add_child(ws)
		item["count"] -= 1
		emit_signal("block_action_performed", "place_station", Vector3i(int(ws.position.x), int(ws.position.y), int(ws.position.z)), 0)
		emit_signal("hotbar_slot_changed", active_slot, item)
		return

func _fire_player_arrow() -> void:
	if not camera:
		return
	var item = hotbar[active_slot]
	var enchs = item.get("enchantments", {})
	var base_dmg = 45.0
	var final_dmg = EnchantmentManager.calculate_arrow_damage(base_dmg, enchs)
	var speed = 36.0
	if enchs.has(EnchantmentManager.ENCH_POWER):
		speed *= (1.0 + enchs[EnchantmentManager.ENCH_POWER] * 0.15)
	var proj = Projectile.new()
	var spawn_pos = camera.global_position - camera.global_transform.basis.z * 0.4 + Vector3(0, -0.1, 0)
	var dir = -camera.global_transform.basis.z.normalized()
	get_tree().current_scene.add_child(proj)
	proj.launch(spawn_pos, dir, speed, final_dmg, self)
	emit_signal("block_action_performed", "shoot_arrow", Vector3i.ZERO, 0)

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
		VoxelChunk.BlockType.COPPER_ORE:
			supply_chain.add_resource("copper_ore", 1)
		VoxelChunk.BlockType.GOLD_ORE:
			supply_chain.add_resource("gold_ore", 1)
		VoxelChunk.BlockType.DEEP_GEM_ORE:
			supply_chain.add_resource("gems", 1)
		VoxelChunk.BlockType.STONE_BRICKS:
			supply_chain.add_resource("stone_bricks", 1)
		VoxelChunk.BlockType.SUPPORT_BEAM:
			supply_chain.add_resource("support_beam", 1)
		VoxelChunk.BlockType.WOODEN_PALISADE:
			supply_chain.add_resource("palisade", 1)
		VoxelChunk.BlockType.STONE_BATTLEMENT:
			supply_chain.add_resource("battlement", 1)
		VoxelChunk.BlockType.WOODEN_GATE:
			supply_chain.add_resource("gate", 1)
		VoxelChunk.BlockType.WHEAT_CROP:
			supply_chain.add_resource("wheat", 2)

func _place_blueprint(item: Dictionary, hit_point: Vector3, hit_normal: Vector3) -> void:
	var place_pos = hit_point + hit_normal * 0.05
	var bp = BlueprintConstruction.new()
	bp.structure_id = item.get("blueprint_id", "cottage")
	bp.display_name = item.get("name", "Worker Cottage Blueprint")
	bp.position = place_pos
	
	if bp.structure_id == "cottage":
		bp.required_resources = {"logs": 8, "stone": 12}
		bp.bounds_size = Vector3(4.0, 3.0, 4.0)
	elif bp.structure_id == "watchtower":
		bp.required_resources = {"logs": 8, "stone_bricks": 4}
		bp.bounds_size = Vector3(3.0, 8.0, 3.0)
	elif bp.structure_id == "granary":
		bp.required_resources = {"logs": 12, "stone": 8, "iron_ingots": 2}
		bp.bounds_size = Vector3(5.0, 4.0, 5.0)
		
	get_tree().current_scene.add_child(bp)
	item["count"] -= 1
	if item["count"] <= 0:
		hotbar[active_slot] = {}
	emit_signal("block_action_performed", "place_blueprint", Vector3i(int(place_pos.x), int(place_pos.y), int(place_pos.z)), 0)
	emit_signal("hotbar_slot_changed", active_slot, hotbar[active_slot])

