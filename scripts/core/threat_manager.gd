class_name ThreatManager
extends Node

## Threat & Warfare Coordinator.
## Computes realm threat scaling and spawns bandit raiding parties targeting citizens and stockpiles.

signal raid_spawned(bandit_count: int)
signal raid_defeated()
signal bandit_slain(loot: Dictionary)

var voxel_world: VoxelWorld
var supply_chain: SupplyChain
var player_ref: Node3D
var active_bandits: Array[Bandit] = []
var active_warlords: Array[BanditWarlord] = []

var wave_timer: float = 0.0
var wave_interval: float = 150.0 # 2.5 minutes between threat cycles
var threat_score: float = 10.0
var raid_wave_count: int = 0

func _init(p_world: VoxelWorld = null, p_supply: SupplyChain = null) -> void:
	voxel_world = p_world
	supply_chain = p_supply

func _process(delta: float) -> void:
	wave_timer += delta
	if wave_timer >= wave_interval:
		wave_timer = 0.0
		_evaluate_threat_and_spawn()

func _evaluate_threat_and_spawn() -> void:
	if not voxel_world:
		return
		
	# GDD Threat formula: Threat = Base + (Pop * 1.5) + (StockpileValue * 0.05)
	var pop = 6
	var stockpile_val = 50.0
	if supply_chain:
		stockpile_val = float(supply_chain.inventory.get("bread", 0) + supply_chain.inventory.get("iron_ore", 0) * 2)
		
	threat_score = 10.0 + (pop * 1.5) + (stockpile_val * 0.05)
	var bandit_count = clampi(int(threat_score / 15.0), 1, 4)
	
	raid_wave_count += 1
	var spawn_boss = (raid_wave_count % 2 == 0) or threat_score >= 30.0
	spawn_raid(bandit_count, spawn_boss)

func spawn_raid(count: int, spawn_boss: bool = false) -> void:
	if not voxel_world:
		return
		
	# Spawn at perimeter edge
	var edge_x = 6
	var edge_z = 6
	var edge_y = voxel_world.get_surface_height(edge_x, edge_z)
	
	for i in range(count):
		var bandit = Bandit.new()
		bandit.voxel_world = voxel_world
		var spawn_pos = Vector3(edge_x + i * 2, edge_y + 1.2, edge_z + i)
		bandit.position = spawn_pos
		
		# Connect defeat
		bandit.defeated.connect(_on_bandit_defeated)
		
		get_parent().add_child(bandit)
		active_bandits.append(bandit)
		
		# Set target to player or settlement center
		if player_ref:
			bandit.set_target(player_ref)

	if spawn_boss:
		var warlord = BanditWarlord.new()
		warlord.voxel_world = voxel_world
		warlord.position = Vector3(edge_x - 2, edge_y + 1.2, edge_z - 2)
		warlord.defeated.connect(_on_warlord_defeated)
		get_parent().add_child(warlord)
		active_warlords.append(warlord)
		if player_ref:
			warlord.set_target(player_ref)
			
	emit_signal("raid_spawned", count + (1 if spawn_boss else 0))

func _on_bandit_defeated(bandit: Bandit, loot: Dictionary) -> void:
	active_bandits.erase(bandit)
	if supply_chain:
		for item in loot.keys():
			supply_chain.add_resource(item, loot[item])
			
	emit_signal("bandit_slain", loot)
	_check_raid_over()

func _on_warlord_defeated(warlord: BanditWarlord, loot: Dictionary) -> void:
	active_warlords.erase(warlord)
	if supply_chain:
		for item in loot.keys():
			supply_chain.add_resource(item, loot[item])
			
	emit_signal("bandit_slain", loot)
	_check_raid_over()

func _check_raid_over() -> void:
	if active_bandits.is_empty() and active_warlords.is_empty():
		emit_signal("raid_defeated")
