class_name GameManager
extends Node3D

## Master Game Coordinator for Voxel Lord: Feudal Realm.
## Links VoxelWorld, Player, Citizens, SupplyChain, Workstations, GameHUD, CraftingMenu, and RoyalLedger.

@onready var voxel_world: VoxelWorld = $VoxelWorld
@onready var player: Player = $Player
@onready var hud: GameHUD = $UI/HUD
@onready var royal_ledger: RoyalLedger = $UI/RoyalLedger
@onready var crafting_menu: CraftingMenu = $UI/CraftingMenu

var supply_chain: SupplyChain
var citizens: Array[Citizen] = []
var workstations: Array[Workstation] = []
var agriculture_manager: AgricultureManager
var threat_manager: ThreatManager

# Game day/night simulation
var day_timer: float = 0.0
var day_duration: float = 120.0 # 2 minutes per full day cycle
var sun_light: DirectionalLight3D

func _ready() -> void:
	supply_chain = SupplyChain.new()
	sun_light = $DirectionalLight3D
	
	# Initialize Agriculture & Threat Systems
	agriculture_manager = AgricultureManager.new(voxel_world, supply_chain)
	agriculture_manager.name = "AgricultureManager"
	add_child(agriculture_manager)
	agriculture_manager.crop_matured.connect(_on_crop_matured)
	agriculture_manager.crop_harvested.connect(_on_crop_harvested)

	threat_manager = ThreatManager.new(voxel_world, supply_chain)
	threat_manager.name = "ThreatManager"
	add_child(threat_manager)
	threat_manager.raid_spawned.connect(_on_raid_spawned)
	threat_manager.raid_defeated.connect(_on_raid_defeated)
	threat_manager.bandit_slain.connect(_on_bandit_slain)
	
	# Wire up player
	if player:
		player.voxel_world = voxel_world
		player.supply_chain = supply_chain
		threat_manager.player_ref = player
		player.open_crafting_requested.connect(_on_open_crafting)
		player.interact_requested.connect(_on_interact_requested)
		player.block_action_performed.connect(_on_player_block_action)
		
		# Position player on top of surface terrain at spawn
		var spawn_x = 32
		var spawn_z = 32
		var surface_y = voxel_world.get_surface_height(spawn_x, spawn_z)
		player.global_position = Vector3(spawn_x + 0.5, surface_y + 2.0, spawn_z + 0.5)
		player.respawn_position = player.global_position
		
		if hud:
			hud.bind_player(player)
			
	# Wire up UI
	if royal_ledger:
		royal_ledger.supply_chain = supply_chain
		royal_ledger.role_reassigned.connect(_on_role_reassigned)

	if crafting_menu:
		crafting_menu.player = player
		crafting_menu.supply_chain = supply_chain
		crafting_menu.item_crafted.connect(_on_item_crafted)
		
	# Spawn initial workstations and citizens
	_spawn_initial_workstations()
	_spawn_initial_citizens()
	
	print("[GAME MANAGER] Voxel Lord realm successfully initialized!")

func _spawn_initial_workstations() -> void:
	# 1. Carpentry Workbench
	var wb = Workstation.new(Workstation.StationType.WORKBENCH)
	var wb_y = voxel_world.get_surface_height(34, 32)
	wb.position = Vector3(34.5, wb_y + 1.0, 32.5)
	add_child(wb)
	workstations.append(wb)

	# 2. Settlement Campfire with warm glow
	var cf = Workstation.new(Workstation.StationType.CAMPFIRE)
	var cf_y = voxel_world.get_surface_height(32, 29)
	cf.position = Vector3(32.5, cf_y + 1.0, 29.5)
	add_child(cf)
	workstations.append(cf)

	# 3. Timber Stockpile Crate
	var cr = Workstation.new(Workstation.StationType.CRATE)
	var cr_y = voxel_world.get_surface_height(36, 32)
	cr.position = Vector3(36.5, cr_y + 1.0, 32.5)
	add_child(cr)
	workstations.append(cr)

func _spawn_initial_citizens() -> void:
	var roles_to_spawn = [
		{"role": Citizen.Role.FARMER, "name": "Geoffrey"},
		{"role": Citizen.Role.FARMER, "name": "Matilda"},
		{"role": Citizen.Role.LUMBERJACK, "name": "Robin"},
		{"role": Citizen.Role.LUMBERJACK, "name": "Barnaby"},
		{"role": Citizen.Role.MINER, "name": "Giles"},
		{"role": Citizen.Role.BAKER, "name": "Elsbeth"}
	]
	
	var spawn_center = Vector3(32, 0, 32)
	
	for info in roles_to_spawn:
		var citizen = Citizen.new()
		citizen.citizen_name = info["name"]
		citizen.voxel_world = voxel_world
		citizen.supply_chain = supply_chain
		
		var rx = randf_range(-6.0, 6.0)
		var rz = randf_range(-6.0, 6.0)
		var cx = int(spawn_center.x + rx)
		var cz = int(spawn_center.z + rz)
		var cy = voxel_world.get_surface_height(cx, cz)
		
		citizen.position = Vector3(cx + 0.5, cy + 1.2, cz + 0.5)
		add_child(citizen)
		citizens.append(citizen)
		
		# Set initial work target near workstations
		var work_target = citizen.position + Vector3(randf_range(-4, 4), 0, randf_range(-4, 4))
		citizen.set_role(info["role"], work_target)

func _process(delta: float) -> void:
	# Day/Night lighting rotation
	day_timer += delta
	var progress = fmod(day_timer, day_duration) / day_duration
	var angle_rad = progress * TAU
	if sun_light:
		sun_light.rotation.x = angle_rad - (PI * 0.5)
		# Dim sun at night
		var sun_height = sin(angle_rad)
		sun_light.light_energy = maxf(0.1, sun_height * 1.2)

func _on_role_reassigned(role_name: String, _delta: int) -> void:
	var role_enum = Citizen.Role.UNASSIGNED
	match role_name:
		"farmer": role_enum = Citizen.Role.FARMER
		"lumberjack": role_enum = Citizen.Role.LUMBERJACK
		"miner": role_enum = Citizen.Role.MINER
		"baker": role_enum = Citizen.Role.BAKER
		"blacksmith": role_enum = Citizen.Role.BLACKSMITH
		
	for c in citizens:
		if c.current_role != role_enum and c.current_role == Citizen.Role.UNASSIGNED:
			c.set_role(role_enum, c.position + Vector3(randf_range(-5, 5), 0, randf_range(-5, 5)))
			break

func _on_open_crafting() -> void:
	if crafting_menu:
		crafting_menu.open_menu(null)

func _on_interact_requested(target: Node3D) -> void:
	if target is Workstation and crafting_menu:
		crafting_menu.open_menu(target)

func _on_item_crafted(recipe_name: String, _item: Dictionary) -> void:
	if hud:
		hud.show_notification("Crafted %s" % recipe_name)

func _on_player_block_action(action: String, pos: Vector3i, btype: int) -> void:
	match action:
		"till":
			if agriculture_manager:
				agriculture_manager.register_farmland(pos)
		"plant":
			if agriculture_manager:
				agriculture_manager.plant_crop(pos, "wheat")
		"mine":
			if btype == VoxelChunk.BlockType.WHEAT_CROP and agriculture_manager:
				agriculture_manager.harvest_crop(pos)

func _on_crop_matured(pos: Vector3i) -> void:
	# Dispatch available farmer to harvest
	for c in citizens:
		if c.current_role == Citizen.Role.FARMER:
			if c.current_state == Citizen.State.IDLE or c.current_state == Citizen.State.WANDER:
				c._navigate_to(Vector3(pos.x + 0.5, pos.y, pos.z + 0.5), Citizen.State.HARVESTING)
				break

func _on_crop_harvested(_pos: Vector3i, yield_data: Dictionary) -> void:
	if hud:
		hud.show_notification("🌾 Harvest: +%d Wheat, +%d Seeds" % [yield_data.get("wheat", 2), yield_data.get("seeds", 1)])

func _on_raid_spawned(count: int) -> void:
	if hud:
		hud.show_notification("⚠️ Bandit Raid approaching! %d Raiders spotted!" % count)

func _on_raid_defeated() -> void:
	if hud:
		hud.show_notification("⚔️ Raid Repelled! The Realm is Secure.")

func _on_bandit_slain(_loot: Dictionary) -> void:
	if hud:
		hud.show_notification("☠️ Bandit Slain! Spoils gathered.")
