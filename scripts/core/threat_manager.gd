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

var wave_timer: float = 0.0
var wave_interval: float = 150.0 # 2.5 minutes between threat cycles
var threat_score: float = 10.0

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
	
	spawn_raid(bandit_count)

func spawn_raid(count: int) -> void:
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
			
	emit_signal("raid_spawned", count)

func _on_bandit_defeated(bandit: Bandit, loot: Dictionary) -> void:
	active_bandits.erase(bandit)
	if supply_chain:
		for item in loot.keys():
			supply_chain.add_resource(item, loot[item])
			
	emit_signal("bandit_slain", loot)
	if active_bandits.is_empty():
		emit_signal("raid_defeated")
