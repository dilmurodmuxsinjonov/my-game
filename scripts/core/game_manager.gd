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
var season_manager: SeasonManager
var active_caravans: Array[TradeCaravan] = []
var caravan_timer: float = 0.0
var caravan_interval: float = 160.0

# Game day/night simulation
var day_timer: float = 0.0
var day_duration: float = 120.0 # 2 minutes per full day cycle
var sun_light: DirectionalLight3D

func _ready() -> void:
	supply_chain = SupplyChain.new()
	sun_light = $DirectionalLight3D
	
	# Initialize Agriculture, Threat & Season Systems
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
	
	season_manager = SeasonManager.new(agriculture_manager)
	season_manager.name = "SeasonManager"
	add_child(season_manager)
	season_manager.season_changed.connect(_on_season_changed)
	season_manager.weather_changed.connect(_on_weather_changed)
	
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
		
	# Spawn initial workstations, citizens, and trade caravan
	_spawn_initial_workstations()
	_spawn_initial_citizens()
	spawn_trade_caravan()
	
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

	# 4. Stone Bloomery Furnace
	var fn = Workstation.new(Workstation.StationType.FURNACE)
	var fn_y = voxel_world.get_surface_height(30, 32)
	fn.position = Vector3(30.5, fn_y + 1.0, 32.5)
	add_child(fn)
	workstations.append(fn)

	# 5. Defensive Watchtower
	var wt = Watchtower.new()
	var wt_y = voxel_world.get_surface_height(28, 28)
	wt.position = Vector3(28.5, wt_y + 0.1, 28.5)
	add_child(wt)

	# 6. Arcane Enchanter's Table
	var et = EnchanterTable.new()
	var et_y = voxel_world.get_surface_height(34, 30)
	et.position = Vector3(34.5, et_y + 0.1, 30.5)
	add_child(et)

func _spawn_initial_citizens() -> void:
	var roles_to_spawn = [
		{"role": Citizen.Role.FARMER, "name": "Geoffrey"},
		{"role": Citizen.Role.FARMER, "name": "Matilda"},
		{"role": Citizen.Role.LUMBERJACK, "name": "Robin"},
		{"role": Citizen.Role.LUMBERJACK, "name": "Barnaby"},
		{"role": Citizen.Role.MINER, "name": "Giles"},
		{"role": Citizen.Role.BAKER, "name": "Elsbeth"},
		{"role": Citizen.Role.GUARD, "name": "Percival"}
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

	# Thermal climate & seasonal updates
	if season_manager:
		var current_temp = season_manager.calculate_current_temperature(progress)
		if player:
			player.ambient_temperature = current_temp
		if hud:
			hud.update_season_display(season_manager.get_season_name(), current_temp, season_manager.get_weather_name())
			
	# Caravan periodic arrival
	caravan_timer += delta
	if caravan_timer >= caravan_interval:
		caravan_timer = 0.0
		spawn_trade_caravan()

func _on_role_reassigned(role_name: String, _delta: int) -> void:
	var role_enum = Citizen.Role.UNASSIGNED
	match role_name:
		"farmer": role_enum = Citizen.Role.FARMER
		"lumberjack": role_enum = Citizen.Role.LUMBERJACK
		"miner": role_enum = Citizen.Role.MINER
		"baker": role_enum = Citizen.Role.BAKER
		"blacksmith": role_enum = Citizen.Role.BLACKSMITH
		"guard": role_enum = Citizen.Role.GUARD
		
	for c in citizens:
		if c.current_role != role_enum and c.current_role == Citizen.Role.UNASSIGNED:
			c.set_role(role_enum, c.position + Vector3(randf_range(-5, 5), 0, randf_range(-5, 5)))
			break

func _on_open_crafting() -> void:
	if crafting_menu:
		crafting_menu.open_menu(null)

func _on_interact_requested(target: Node3D) -> void:
	if (target is Workstation or target is TradeCaravan or target is EnchanterTable) and crafting_menu:
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

func spawn_trade_caravan() -> void:
	if active_caravans.size() > 0:
		return
		
	var caravan = TradeCaravan.new()
	var spawn_x = 36
	var spawn_z = 28
	var surface_y = voxel_world.get_surface_height(spawn_x, spawn_z) if voxel_world else 16
	caravan.position = Vector3(spawn_x + 0.5, surface_y + 1.0, spawn_z + 0.5)
	caravan.traded.connect(_on_caravan_traded)
	caravan.departed.connect(_on_caravan_departed.bind(caravan))
	add_child(caravan)
	active_caravans.append(caravan)
	if hud:
		hud.show_notification("🐪 An Exotic Trade Caravan has arrived in the realm!")

func _on_caravan_traded(item_bought: String, cost: int) -> void:
	if hud:
		hud.show_notification("💰 Traded %s for %d coins with the caravan!" % [item_bought.capitalize(), cost])

func _on_caravan_departed(caravan: TradeCaravan) -> void:
	active_caravans.erase(caravan)
	if hud:
		hud.show_notification("🐪 Trade Caravan has departed for distant lands.")

func _on_season_changed(_old_season: SeasonManager.Season, new_season: SeasonManager.Season) -> void:
	if hud and season_manager:
		hud.show_notification("🍂 Season changed to %s!" % season_manager.get_season_name(new_season))

func _on_weather_changed(new_weather: SeasonManager.Weather) -> void:
	if hud and season_manager:
		hud.show_notification("🌧️ Weather: %s" % season_manager.get_weather_name(new_weather))

