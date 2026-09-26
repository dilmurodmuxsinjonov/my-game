# scripts/world/biome_manager.gd
# Voxel Lord: Feudal Realm - Milestone 25: Multi-Biome World Generation & 3D Cave Carving

class_name BiomeManager
extends RefCounted

enum BiomeType {
	PLAINS = 0,
	FOREST = 1,
	HIGHLANDS = 2,
	RIVER_VALLEY = 3
}

const SEA_LEVEL: int = 6
const HIGHLAND_SNOW_LEVEL: int = 22

# Biome properties
const BIOME_NAMES: Dictionary = {
	BiomeType.PLAINS: "Verdant Plains",
	BiomeType.FOREST: "Deep Oak Forest",
	BiomeType.HIGHLANDS: "Rocky Highlands",
	BiomeType.RIVER_VALLEY: "River Basin"
}

var temp_noise: FastNoiseLite
var moisture_noise: FastNoiseLite
var continental_noise: FastNoiseLite
var cave_noise: FastNoiseLite

func _init(seed_val: int = 1337) -> void:
	temp_noise = FastNoiseLite.new()
	temp_noise.seed = seed_val + 301
	temp_noise.frequency = 0.015

	moisture_noise = FastNoiseLite.new()
	moisture_noise.seed = seed_val + 402
	moisture_noise.frequency = 0.018

	continental_noise = FastNoiseLite.new()
	continental_noise.seed = seed_val + 503
	continental_noise.frequency = 0.020

	cave_noise = FastNoiseLite.new()
	cave_noise.seed = seed_val + 604
	cave_noise.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	cave_noise.frequency = 0.045
	cave_noise.fractal_octaves = 2

func get_biome(world_x: int, world_z: int) -> BiomeType:
	var cont: float = continental_noise.get_noise_2d(float(world_x), float(world_z))
	var moist: float = moisture_noise.get_noise_2d(float(world_x), float(world_z))
	var temp: float = temp_noise.get_noise_2d(float(world_x), float(world_z))

	# Low continentalness = River basin or lake
	if cont < -0.25:
		return BiomeType.RIVER_VALLEY
	
	# High elevation / rocky ridge
	if cont > 0.35:
		return BiomeType.HIGHLANDS
	
	# Moist & temperate = Deep Forest
	if moist > 0.10:
		return BiomeType.FOREST
	
	# Default = Fertile Plains
	return BiomeType.PLAINS

func calculate_surface_height(world_x: int, world_z: int, base_height: int = 12) -> int:
	var biome = get_biome(world_x, world_z)
	var cont: float = continental_noise.get_noise_2d(float(world_x), float(world_z))

	match biome:
		BiomeType.RIVER_VALLEY:
			return clampi(int(SEA_LEVEL + cont * 2.0), 3, SEA_LEVEL + 2)
		BiomeType.HIGHLANDS:
			return clampi(int(base_height + 6.0 + cont * 10.0), 16, 28)
		BiomeType.FOREST:
			return clampi(int(base_height + cont * 4.0), 10, 18)
		BiomeType.PLAINS, _:
			return clampi(int(base_height + cont * 3.0), 8, 16)

func get_surface_block(biome: BiomeType, height_y: int) -> int:
	match biome:
		BiomeType.RIVER_VALLEY:
			if height_y <= SEA_LEVEL:
				return VoxelChunk.BlockType.SAND if "SAND" in VoxelChunk.BlockType else VoxelChunk.BlockType.DIRT
			return VoxelChunk.BlockType.GRASS
		BiomeType.HIGHLANDS:
			if height_y >= HIGHLAND_SNOW_LEVEL:
				return VoxelChunk.BlockType.STONE # Alpine snow line
			return VoxelChunk.BlockType.STONE if height_y > 18 else VoxelChunk.BlockType.GRASS
		BiomeType.FOREST, BiomeType.PLAINS, _:
			return VoxelChunk.BlockType.GRASS

func is_cave_air(world_x: int, world_y: int, world_z: int, surface_y: int) -> bool:
	# Caves carve only underground, beneath surface soil
	if world_y >= surface_y - 2 or world_y < 2:
		return false
	
	var c_sample = cave_noise.get_noise_3d(float(world_x), float(world_y), float(world_z))
	# Worm-like cavern tunnel: noise close to 0 carves open air
	return absf(c_sample) < 0.11
