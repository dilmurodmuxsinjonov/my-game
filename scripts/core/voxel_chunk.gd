class_name VoxelChunk
extends StaticBody3D

## High-performance voxel chunk handling 16x32x16 voxel blocks with 6-face culling,
## vertex color lighting, and dynamic trimesh collision generation.

const CHUNK_SIZE_X: int = 16
const CHUNK_SIZE_Y: int = 32
const CHUNK_SIZE_Z: int = 16
const TOTAL_BLOCKS: int = CHUNK_SIZE_X * CHUNK_SIZE_Y * CHUNK_SIZE_Z

enum BlockType {
	AIR = 0,
	DIRT = 1,
	GRASS = 2,
	STONE = 3,
	WOOD = 4,
	LEAVES = 5,
	IRON_ORE = 6,
	COAL_ORE = 7,
	GOLD_ORE = 8,
	COBBLESTONE = 9,
	PLANKS = 10,
	WATER = 11,
	GLASS = 12,
	FARMLAND = 13,
	WHEAT_CROP = 14,
	COPPER_ORE = 15,
	STONE_BRICKS = 16,
	SUPPORT_BEAM = 17,
	DEEP_GEM_ORE = 18,
	WOODEN_PALISADE = 19,
	STONE_BATTLEMENT = 20,
	WOODEN_GATE = 21,
	ROCK_SALT_ORE = 22,
	SILVER_ORE = 23,
	MINING_RAIL = 24
}

# Block properties
const BLOCK_HARDNESS: Dictionary = {
	BlockType.AIR: 0.0,
	BlockType.DIRT: 0.5,
	BlockType.GRASS: 0.6,
	BlockType.STONE: 1.5,
	BlockType.WOOD: 1.0,
	BlockType.LEAVES: 0.2,
	BlockType.IRON_ORE: 2.5,
	BlockType.COAL_ORE: 1.8,
	BlockType.GOLD_ORE: 2.8,
	BlockType.COBBLESTONE: 1.4,
	BlockType.PLANKS: 0.8,
	BlockType.WATER: 0.0,
	BlockType.GLASS: 0.3,
	BlockType.FARMLAND: 0.5,
	BlockType.WHEAT_CROP: 0.1,
	BlockType.COPPER_ORE: 2.0,
	BlockType.STONE_BRICKS: 2.2,
	BlockType.SUPPORT_BEAM: 1.2,
	BlockType.DEEP_GEM_ORE: 3.5,
	BlockType.WOODEN_PALISADE: 2.5,
	BlockType.STONE_BATTLEMENT: 3.0,
	BlockType.WOODEN_GATE: 1.8,
	BlockType.ROCK_SALT_ORE: 1.6,
	BlockType.SILVER_ORE: 2.6,
	BlockType.MINING_RAIL: 1.0
}

# Chunk grid coordinate (e.g. (0,0), (1,0))
var chunk_pos: Vector2i = Vector2i.ZERO

# 3D block array flattened for performance
var blocks: PackedByteArray = PackedByteArray()
var is_dirty: bool = true

var mesh_instance: MeshInstance3D
var collision_shape: CollisionShape3D
var static_material: StandardMaterial3D

func _init(p_chunk_pos: Vector2i = Vector2i.ZERO) -> void:
	chunk_pos = p_chunk_pos
	blocks.resize(TOTAL_BLOCKS)
	blocks.fill(BlockType.AIR)
	position = Vector3(chunk_pos.x * CHUNK_SIZE_X, 0, chunk_pos.y * CHUNK_SIZE_Z)

func _ready() -> void:
	mesh_instance = MeshInstance3D.new()
	collision_shape = CollisionShape3D.new()
	add_child(mesh_instance)
	add_child(collision_shape)
	
	# Create shared voxel vertex color material
	static_material = StandardMaterial3D.new()
	static_material.vertex_color_use_as_albedo = true
	static_material.roughness = 0.85
	static_material.metallic_specular = 0.15
	mesh_instance.material_override = static_material

func _get_index(x: int, y: int, z: int) -> int:
	return x + (y * CHUNK_SIZE_X) + (z * CHUNK_SIZE_X * CHUNK_SIZE_Y)

func get_block(x: int, y: int, z: int) -> int:
	if x < 0 or x >= CHUNK_SIZE_X or y < 0 or y >= CHUNK_SIZE_Y or z < 0 or z >= CHUNK_SIZE_Z:
		return BlockType.AIR
	return blocks[_get_index(x, y, z)]

func set_block(x: int, y: int, z: int, type: int) -> void:
	if x >= 0 and x < CHUNK_SIZE_X and y >= 0 and y < CHUNK_SIZE_Y and z >= 0 and z < CHUNK_SIZE_Z:
		blocks[_get_index(x, y, z)] = type
		is_dirty = true

func is_solid(type: int) -> bool:
	return type != BlockType.AIR and type != BlockType.WATER and type != BlockType.WHEAT_CROP and type != BlockType.MINING_RAIL

func is_transparent(type: int) -> bool:
	return type == BlockType.AIR or type == BlockType.WATER or type == BlockType.LEAVES or type == BlockType.GLASS or type == BlockType.WHEAT_CROP or type == BlockType.MINING_RAIL

func build_mesh() -> void:
	var surface_tool = SurfaceTool.new()
	surface_tool.begin(Mesh.PRIMITIVE_TRIANGLES)
	
	var has_geometry: bool = false
	
	for x in range(CHUNK_SIZE_X):
		for y in range(CHUNK_SIZE_Y):
			for z in range(CHUNK_SIZE_Z):
				var block = get_block(x, y, z)
				if block == BlockType.AIR:
					continue
				
				var pos = Vector3(x, y, z)
				var color = _get_block_color(block)
				
				# Top (+Y)
				if is_transparent(get_block(x, y + 1, z)):
					_add_face(surface_tool, pos, Vector3.UP, color, [Vector3(0,1,0), Vector3(1,1,0), Vector3(1,1,1), Vector3(0,1,1)], 1.0)
					has_geometry = true
				
				# Bottom (-Y)
				if y > 0 and is_transparent(get_block(x, y - 1, z)):
					_add_face(surface_tool, pos, Vector3.DOWN, color, [Vector3(0,0,1), Vector3(1,0,1), Vector3(1,0,0), Vector3(0,0,0)], 0.5)
					has_geometry = true
				
				# South (+Z)
				if is_transparent(get_block(x, y, z + 1)):
					_add_face(surface_tool, pos, Vector3.BACK, color, [Vector3(0,0,1), Vector3(1,0,1), Vector3(1,1,1), Vector3(0,1,1)], 0.85)
					has_geometry = true
				
				# North (-Z)
				if is_transparent(get_block(x, y, z - 1)):
					_add_face(surface_tool, pos, Vector3.FORWARD, color, [Vector3(1,0,0), Vector3(0,0,0), Vector3(0,1,0), Vector3(1,1,0)], 0.85)
					has_geometry = true
				
				# East (+X)
				if is_transparent(get_block(x + 1, y, z)):
					_add_face(surface_tool, pos, Vector3.RIGHT, color, [Vector3(1,0,1), Vector3(1,0,0), Vector3(1,1,0), Vector3(1,1,1)], 0.75)
					has_geometry = true
				
				# West (-X)
				if is_transparent(get_block(x - 1, y, z)):
					_add_face(surface_tool, pos, Vector3.LEFT, color, [Vector3(0,0,0), Vector3(0,0,1), Vector3(0,1,1), Vector3(0,1,0)], 0.75)
					has_geometry = true

	if has_geometry:
		surface_tool.generate_normals()
		var mesh = surface_tool.commit()
		if mesh_instance:
			mesh_instance.mesh = mesh
		if collision_shape and mesh:
			collision_shape.shape = mesh.create_trimesh_shape()
	else:
		if mesh_instance:
			mesh_instance.mesh = null
		if collision_shape:
			collision_shape.shape = null
			
	is_dirty = false

func _add_face(st: SurfaceTool, offset: Vector3, normal: Vector3, base_color: Color, v: Array, shade: float) -> void:
	var shaded_color = base_color * shade
	shaded_color.a = 1.0
	st.set_color(shaded_color)
	st.set_normal(normal)
	
	# Quad as two triangles (0, 1, 2) and (0, 2, 3)
	st.set_uv(Vector2(0, 0))
	st.add_vertex(offset + v[0])
	st.set_uv(Vector2(1, 0))
	st.add_vertex(offset + v[1])
	st.set_uv(Vector2(1, 1))
	st.add_vertex(offset + v[2])
	
	st.set_uv(Vector2(0, 0))
	st.add_vertex(offset + v[0])
	st.set_uv(Vector2(1, 1))
	st.add_vertex(offset + v[2])
	st.set_uv(Vector2(0, 1))
	st.add_vertex(offset + v[3])

func _get_block_color(type: int) -> Color:
	match type:
		BlockType.GRASS: return Color(0.28, 0.65, 0.22)
		BlockType.DIRT: return Color(0.48, 0.32, 0.18)
		BlockType.STONE: return Color(0.52, 0.52, 0.54)
		BlockType.COBBLESTONE: return Color(0.42, 0.42, 0.44)
		BlockType.WOOD: return Color(0.40, 0.25, 0.12)
		BlockType.PLANKS: return Color(0.68, 0.52, 0.30)
		BlockType.LEAVES: return Color(0.18, 0.52, 0.15, 0.9)
		BlockType.IRON_ORE: return Color(0.72, 0.58, 0.48)
		BlockType.COAL_ORE: return Color(0.22, 0.22, 0.24)
		BlockType.GOLD_ORE: return Color(0.85, 0.75, 0.25)
		BlockType.WATER: return Color(0.15, 0.40, 0.80, 0.6)
		BlockType.GLASS: return Color(0.85, 0.92, 0.95, 0.4)
		BlockType.FARMLAND: return Color(0.35, 0.22, 0.12)
		BlockType.WHEAT_CROP: return Color(0.82, 0.75, 0.22)
		BlockType.COPPER_ORE: return Color(0.78, 0.45, 0.28)
		BlockType.STONE_BRICKS: return Color(0.60, 0.60, 0.62)
		BlockType.SUPPORT_BEAM: return Color(0.35, 0.20, 0.10)
		BlockType.DEEP_GEM_ORE: return Color(0.20, 0.85, 0.85)
		BlockType.WOODEN_PALISADE: return Color(0.32, 0.18, 0.08)
		BlockType.STONE_BATTLEMENT: return Color(0.50, 0.50, 0.52)
		BlockType.WOODEN_GATE: return Color(0.45, 0.28, 0.14)
		BlockType.ROCK_SALT_ORE: return Color(0.92, 0.85, 0.85)
		BlockType.SILVER_ORE: return Color(0.82, 0.85, 0.92)
		BlockType.MINING_RAIL: return Color(0.40, 0.32, 0.22)
		_: return Color(0.9, 0.9, 0.9)
