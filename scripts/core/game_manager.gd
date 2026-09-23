class_name GameManager
extends Node3D

## Master Game Coordinator for Voxel Lord: Feudal Realm.
## Links VoxelWorld, Player, Citizens, SupplyChain, GameHUD, and RoyalLedger.

@onready var voxel_world: VoxelWorld = $VoxelWorld
@onready var player: Player = $Player
@onready var hud: GameHUD = $UI/HUD
@onready var royal_ledger: RoyalLedger = $UI/RoyalLedger

var supply_chain: SupplyChain
var citizens: Array[Citizen] = []

# Game day/night simulation
var day_timer: float = 0.0
var day_duration: float = 120.0 # 2 minutes per full day cycle
var sun_light: DirectionalLight3D

func _ready() -> void:
	supply_chain = SupplyChain.new()
	sun_light = $DirectionalLight3D
	
	# Wire up player
	if player:
		player.voxel_world = voxel_world
		player.supply_chain = supply_chain
		
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
		
	# Spawn initial citizens
	_spawn_initial_citizens()
	
	print("[GAME MANAGER] Voxel Lord realm successfully initialized!")

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
	# Update citizen role distributions dynamically
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
