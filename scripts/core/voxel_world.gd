class_name VoxelWorld
extends Node3D

const GeologyManager = preload("res://scripts/world/geology_manager.gd")
const BiomeManager = preload("res://scripts/world/biome_manager.gd")

## Manages 3D voxel terrain generation using FastNoiseLite, chunk streaming,
## world-space block modifications (mining/placing), and multi-chunk boundary meshing.

signal block_mined(world_pos: Vector3i, block_type: int)
signal block_placed(world_pos: Vector3i, block_type: int)
signal cave_in_occurred(origin: Vector3i, affected_blocks: Array[Vector3i], damage: float)

@export var world_size_chunks: Vector2i = Vector2i(4, 4) # 4x4 chunks = 64x64 blocks
@export var terrain_seed: int = 1337
@export var base_height: int = 12
@export var height_scale: float = 8.0

var chunks: Dictionary = {} # Vector2i -> VoxelChunk
var noise: FastNoiseLite
var tree_noise: FastNoiseLite
var ore_noise: FastNoiseLite
var geology_manager: GeologyManager = GeologyManager.new()
var biome_manager: BiomeManager = null

func _ready() -> void:
	_init_noise()
	generate_world()

func _init_noise() -> void:
	noise = FastNoiseLite.new()
	noise.seed = terrain_seed
	noise.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	noise.frequency = 0.025
	noise.fractal_octaves = 3
	noise.fractal_lacunarity = 2.0
	noise.fractal_gain = 0.5
	
	tree_noise = FastNoiseLite.new()
	tree_noise.seed = terrain_seed + 101
	tree_noise.frequency = 0.12
	
	ore_noise = FastNoiseLite.new()
	ore_noise.seed = terrain_seed + 202
	ore_noise.frequency = 0.08

	biome_manager = BiomeManager.new(terrain_seed)

func generate_world() -> void:
	# Step 1: Instantiate chunks and populate block arrays
	for cx in range(world_size_chunks.x):
		for cz in range(world_size_chunks.y):
			var cpos = Vector2i(cx, cz)
			var chunk = VoxelChunk.new(cpos)
			chunk.name = "Chunk_%d_%d" % [cx, cz]
			add_child(chunk)
			chunks[cpos] = chunk
			_generate_chunk_terrain(chunk, cpos)
			
	# Step 2: Spawn procedural vegetation (trees)
	_generate_trees()
	
	# Step 3: Build meshes for all chunks
	for chunk in chunks.values():
		chunk.build_mesh()

func _generate_chunk_terrain(chunk: VoxelChunk, cpos: Vector2i) -> void:
	var start_x = cpos.x * VoxelChunk.CHUNK_SIZE_X
	var start_z = cpos.y * VoxelChunk.CHUNK_SIZE_Z
	
	for lx in range(VoxelChunk.CHUNK_SIZE_X):
		for lz in range(VoxelChunk.CHUNK_SIZE_Z):
			var wx = start_x + lx
			var wz = start_z + lz
			
			var biome = biome_manager.get_biome(wx, wz) if biome_manager else BiomeManager.BiomeType.PLAINS
			var surface_y = biome_manager.calculate_surface_height(wx, wz, base_height) if biome_manager else clampi(int(base_height + noise.get_noise_2d(float(wx), float(wz)) * height_scale), 2, VoxelChunk.CHUNK_SIZE_Y - 8)
			var surface_block = biome_manager.get_surface_block(biome, surface_y) if biome_manager else VoxelChunk.BlockType.GRASS
			
			for ly in range(VoxelChunk.CHUNK_SIZE_Y):
				if ly > surface_y:
					# Water bodies & rivers at sea level
					if ly <= BiomeManager.SEA_LEVEL:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.WATER)
					else:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.AIR)
				elif ly == surface_y:
					chunk.set_block(lx, ly, lz, surface_block)
				elif ly >= surface_y - 2:
					chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.DIRT)
				else:
					# 3D Subterranean Cave Carving
					if biome_manager and biome_manager.is_cave_air(wx, ly, wz, surface_y):
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.AIR)
						continue
						
					# Underground geological strata & mineral deposits
					var ore_sample = ore_noise.get_noise_3d(float(wx), float(ly), float(wz))
					if ly < 5 and ore_sample > 0.48:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.DEEP_GEM_ORE)
					elif ly < 8 and ore_sample > 0.42:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.GOLD_ORE)
					elif ly >= 4 and ly < 10 and ore_sample > 0.44:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.SILVER_ORE)
					elif ly < 15 and ore_sample > 0.35:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.IRON_ORE)
					elif ly >= 10 and ly < 18 and ore_sample > 0.38:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.ROCK_SALT_ORE)
					elif ly < 20 and ore_sample > 0.30:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.COPPER_ORE)
					elif ly < 25 and ore_sample > 0.25:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.COAL_ORE)
					else:
						chunk.set_block(lx, ly, lz, VoxelChunk.BlockType.STONE)

func _generate_trees() -> void:
	var max_x = world_size_chunks.x * VoxelChunk.CHUNK_SIZE_X
	var max_z = world_size_chunks.y * VoxelChunk.CHUNK_SIZE_Z
	
	# Spawn trees where tree_noise is high, away from chunk edges
	for wx in range(3, max_x - 3, 4):
		for wz in range(3, max_z - 3, 4):
			var t_sample = tree_noise.get_noise_2d(float(wx), float(wz))
			if t_sample > 0.35:
				var surface_y = get_surface_height(wx, wz)
				if surface_y >= 3 and surface_y < VoxelChunk.CHUNK_SIZE_Y - 7:
					_spawn_tree(Vector3i(wx, surface_y + 1, wz))

func _spawn_tree(base_pos: Vector3i) -> void:
	var trunk_height: int = 4
	# Wood trunk
	for ty in range(trunk_height):
		set_block_world(Vector3i(base_pos.x, base_pos.y + ty, base_pos.z), VoxelChunk.BlockType.WOOD, false)
		
	# Leaves canopy
	var leaf_base_y = base_pos.y + trunk_height - 1
	for lx in range(-2, 3):
		for lz in range(-2, 3):
			for ly in range(0, 3):
				if abs(lx) == 2 and abs(lz) == 2 and ly == 2:
					continue # Trim canopy corners
				var leaf_pos = Vector3i(base_pos.x + lx, leaf_base_y + ly, base_pos.z + lz)
				if get_block_world(leaf_pos) == VoxelChunk.BlockType.AIR:
					set_block_world(leaf_pos, VoxelChunk.BlockType.LEAVES, false)

func get_surface_height(world_x: int, world_z: int) -> int:
	var max_y = VoxelChunk.CHUNK_SIZE_Y - 1
	for y in range(max_y, -1, -1):
		var b = get_block_world(Vector3i(world_x, y, world_z))
		if b != VoxelChunk.BlockType.AIR and b != VoxelChunk.BlockType.LEAVES and b != VoxelChunk.BlockType.WATER:
			return y
	return 0

func world_to_chunk_coords(world_pos: Vector3i) -> Dictionary:
	var cx = int(floor(float(world_pos.x) / float(VoxelChunk.CHUNK_SIZE_X)))
	var cz = int(floor(float(world_pos.z) / float(VoxelChunk.CHUNK_SIZE_Z)))
	var lx = world_pos.x - (cx * VoxelChunk.CHUNK_SIZE_X)
	var lz = world_pos.z - (cz * VoxelChunk.CHUNK_SIZE_Z)
	return {
		"chunk_coords": Vector2i(cx, cz),
		"local_coords": Vector3i(lx, world_pos.y, lz)
	}

func get_block_world(world_pos: Vector3i) -> int:
	if world_pos.y < 0 or world_pos.y >= VoxelChunk.CHUNK_SIZE_Y:
		return VoxelChunk.BlockType.AIR
	var coords = world_to_chunk_coords(world_pos)
	var chunk: VoxelChunk = chunks.get(coords["chunk_coords"])
	if chunk:
		var lc: Vector3i = coords["local_coords"]
		return chunk.get_block(lc.x, lc.y, lc.z)
	return VoxelChunk.BlockType.AIR

func set_block_world(world_pos: Vector3i, type: int, auto_rebuild: bool = true) -> bool:
	if world_pos.y < 0 or world_pos.y >= VoxelChunk.CHUNK_SIZE_Y:
		return false
	var coords = world_to_chunk_coords(world_pos)
	var cpos: Vector2i = coords["chunk_coords"]
	var chunk: VoxelChunk = chunks.get(cpos)
	if not chunk:
		return false
		
	var lc: Vector3i = coords["local_coords"]
	chunk.set_block(lc.x, lc.y, lc.z, type)
	
	if auto_rebuild:
		chunk.build_mesh()
		# If on chunk boundary, rebuild neighbor chunk to update culled faces
		if lc.x == 0 and chunks.has(cpos + Vector2i(-1, 0)):
			chunks[cpos + Vector2i(-1, 0)].build_mesh()
		elif lc.x == VoxelChunk.CHUNK_SIZE_X - 1 and chunks.has(cpos + Vector2i(1, 0)):
			chunks[cpos + Vector2i(1, 0)].build_mesh()
			
		if lc.z == 0 and chunks.has(cpos + Vector2i(0, -1)):
			chunks[cpos + Vector2i(0, -1)].build_mesh()
		elif lc.z == VoxelChunk.CHUNK_SIZE_Z - 1 and chunks.has(cpos + Vector2i(0, 1)):
			chunks[cpos + Vector2i(0, 1)].build_mesh()
			
	return true

func mine_block(hit_point: Vector3, normal: Vector3) -> Dictionary:
	# Step slightly into the hit block using the inverse normal
	var center = hit_point - normal * 0.4
	var target_pos = Vector3i(int(floor(center.x)), int(floor(center.y)), int(floor(center.z)))
	var old_type = get_block_world(target_pos)
	
	if old_type != VoxelChunk.BlockType.AIR:
		set_block_world(target_pos, VoxelChunk.BlockType.AIR, true)
		emit_signal("block_mined", target_pos, old_type)
		
		# Check structural stability and cave-in risk (TerraFirmaCraft mechanics)
		var stability = geology_manager.check_mining_stability(self, target_pos, old_type)
		if stability.get("collapsed", false):
			emit_signal("cave_in_occurred", target_pos, stability["affected_blocks"], stability["damage"])
			
		return {
			"success": true,
			"pos": target_pos,
			"type": old_type,
			"stability": stability
		}
		
	return {"success": false, "pos": target_pos, "type": VoxelChunk.BlockType.AIR}

func tap_rock_with_prospector_pick(world_pos: Vector3i) -> Dictionary:
	return geology_manager.prospect_area(self, world_pos, 12)

func place_block(hit_point: Vector3, normal: Vector3, block_type: int) -> Dictionary:
	# Step outward into the air space along the normal
	var center = hit_point + normal * 0.4
	var target_pos = Vector3i(int(floor(center.x)), int(floor(center.y)), int(floor(center.z)))
	var current_type = get_block_world(target_pos)
	
	if current_type == VoxelChunk.BlockType.AIR or current_type == VoxelChunk.BlockType.WATER:
		var success = set_block_world(target_pos, block_type, true)
		if success:
			emit_signal("block_placed", target_pos, block_type)
			return {"success": true, "pos": target_pos, "type": block_type}
			
	return {"success": false, "pos": target_pos, "type": current_type}
