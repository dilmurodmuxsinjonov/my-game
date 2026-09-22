class_name VoxelChunk
extends StaticBody3D

## Handles 3D voxel block storage and optimized mesh generation with face culling.

const CHUNK_SIZE_X: int = 16
const CHUNK_SIZE_Y: int = 32
const CHUNK_SIZE_Z: int = 16

enum BlockType {
	AIR = 0,
	DIRT = 1,
	GRASS = 2,
	STONE = 3,
	WOOD = 4,
	LEAVES = 5,
	IRON_ORE = 6
}

var blocks: Array = []
var mesh_instance: MeshInstance3D
var collision_shape: CollisionShape3D

func _init() -> void:
	# Initialize 3D array flattened
	blocks.resize(CHUNK_SIZE_X * CHUNK_SIZE_Y * CHUNK_SIZE_Z)
	blocks.fill(BlockType.AIR)

func _ready() -> void:
	mesh_instance = MeshInstance3D.new()
	collision_shape = CollisionShape3D.new()
	add_child(mesh_instance)
	add_child(collision_shape)

func get_block(x: int, y: int, z: int) -> int:
	if x < 0 or x >= CHUNK_SIZE_X or y < 0 or y >= CHUNK_SIZE_Y or z < 0 or z >= CHUNK_SIZE_Z:
		return BlockType.AIR
	return blocks[x + y * CHUNK_SIZE_X + z * CHUNK_SIZE_X * CHUNK_SIZE_Y]

func set_block(x: int, y: int, z: int, type: int) -> void:
	if x >= 0 and x < CHUNK_SIZE_X and y >= 0 and y < CHUNK_SIZE_Y and z >= 0 and z < CHUNK_SIZE_Z:
		blocks[x + y * CHUNK_SIZE_X + z * CHUNK_SIZE_X * CHUNK_SIZE_Y] = type

func build_mesh() -> void:
	var surface_tool = SurfaceTool.new()
	surface_tool.begin(Mesh.PRIMITIVE_TRIANGLES)
	
	for x in range(CHUNK_SIZE_X):
		for y in range(CHUNK_SIZE_Y):
			for z in range(CHUNK_SIZE_Z):
				var block = get_block(x, y, z)
				if block == BlockType.AIR:
					continue
				_add_culled_cube(surface_tool, x, y, z, block)

	surface_tool.generate_normals()
	var mesh = surface_tool.commit()
	mesh_instance.mesh = mesh
	
	# Generate collision
	if mesh:
		collision_shape.shape = mesh.create_trimesh_shape()

func _add_culled_cube(st: SurfaceTool, x: int, y: int, z: int, block_type: int) -> void:
	var pos = Vector3(x, y, z)
	
	# Check 6 adjacent neighbors (Face culling optimization)
	if get_block(x, y + 1, z) == BlockType.AIR: # Top
		_create_face(st, pos, [Vector3(0,1,0), Vector3(1,1,0), Vector3(1,1,1), Vector3(0,1,1)], block_type)
	if get_block(x, y - 1, z) == BlockType.AIR: # Bottom
		_create_face(st, pos, [Vector3(0,0,1), Vector3(1,0,1), Vector3(1,0,0), Vector3(0,0,0)], block_type)
	if get_block(x, y, z + 1) == BlockType.AIR: # South
		_create_face(st, pos, [Vector3(0,0,1), Vector3(1,0,1), Vector3(1,1,1), Vector3(0,1,1)], block_type)
	if get_block(x, y, z - 1) == BlockType.AIR: # North
		_create_face(st, pos, [Vector3(1,0,0), Vector3(0,0,0), Vector3(0,1,0), Vector3(1,1,0)], block_type)
	if get_block(x + 1, y, z) == BlockType.AIR: # East
		_create_face(st, pos, [Vector3(1,0,1), Vector3(1,0,0), Vector3(1,1,0), Vector3(1,1,1)], block_type)
	if get_block(x - 1, y, z) == BlockType.AIR: # West
		_create_face(st, pos, [Vector3(0,0,0), Vector3(0,0,1), Vector3(0,1,1), Vector3(0,1,0)], block_type)

func _create_face(st: SurfaceTool, offset: Vector3, v: Array, block_type: int) -> void:
	var color = _get_block_color(block_type)
	st.set_color(color)
	
	# Triangle 1
	st.add_vertex(offset + v[0])
	st.add_vertex(offset + v[1])
	st.add_vertex(offset + v[2])
	# Triangle 2
	st.add_vertex(offset + v[0])
	st.add_vertex(offset + v[2])
	st.add_vertex(offset + v[3])

func _get_block_color(type: int) -> Color:
	match type:
		BlockType.GRASS: return Color(0.25, 0.65, 0.20)
		BlockType.DIRT: return Color(0.45, 0.28, 0.15)
		BlockType.STONE: return Color(0.55, 0.55, 0.55)
		BlockType.WOOD: return Color(0.40, 0.25, 0.10)
		BlockType.LEAVES: return Color(0.18, 0.50, 0.15)
		BlockType.IRON_ORE: return Color(0.70, 0.60, 0.50)
		_: return Color.WHITE
