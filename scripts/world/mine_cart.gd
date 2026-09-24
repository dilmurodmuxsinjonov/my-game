class_name MineCart
extends Node3D

## Underground Ore Transport Minecart (Milestone 13).
## Transports heavy mineral payloads (up to 30 ores/stone chunks) along mining rails
## and subterranean shafts, reducing inventory clutter and assisting Hauler citizens.

signal cargo_changed(total_cargo: int, max_capacity: int)
signal dumped_cargo(items_dumped: Dictionary)

const MAX_CAPACITY: int = 30
const BASE_SPEED: float = 3.0
const RAIL_SPEED_MULTIPLIER: float = 2.5 # 2.5x speed boost on mining rails
const DECELERATION: float = 2.0

var cargo: Dictionary = {} # item_name: count
var velocity: Vector3 = Vector3.ZERO
var is_on_rails: bool = false

var model_instance: Node3D

func _ready() -> void:
	_load_model()

func _load_model() -> void:
	var glb_path = "res://assets/models/mine_cart.glb"
	if ResourceLoader.exists(glb_path):
		var scene = load(glb_path)
		if scene:
			model_instance = scene.instantiate()
			add_child(model_instance)

func _physics_process(delta: float) -> void:
	if velocity.length_squared() > 0.001:
		var speed_mult = RAIL_SPEED_MULTIPLIER if is_on_rails else 1.0
		global_position += velocity * speed_mult * delta
		velocity = velocity.move_toward(Vector3.ZERO, DECELERATION * delta)

## Push the minecart in a specific direction (by player or citizen)
func push(direction: Vector3, force: float = 6.0) -> void:
	var dir_flat = Vector3(direction.x, 0.0, direction.z).normalized()
	velocity = dir_flat * force

## Add ore or raw stone cargo into the cart
func load_cargo(item_name: String, amount: int) -> int:
	var current_total = get_total_cargo()
	var space_available = MAX_CAPACITY - current_total
	if space_available <= 0:
		return 0 # Full
		
	var to_add = mini(amount, space_available)
	cargo[item_name] = cargo.get(item_name, 0) + to_add
	cargo_changed.emit(get_total_cargo(), MAX_CAPACITY)
	return to_add

## Unload all cargo into an inventory / supply chain stockpile
func unload_all() -> Dictionary:
	var dumped = cargo.duplicate()
	cargo.clear()
	cargo_changed.emit(0, MAX_CAPACITY)
	dumped_cargo.emit(dumped)
	return dumped

## Get total amount of cargo currently stored
func get_total_cargo() -> int:
	var total: int = 0
	for count in cargo.values():
		total += int(count)
	return total

## Check if the minecart is on a rail block in the voxel world
func update_rail_status(world: VoxelWorld) -> void:
	if not world:
		is_on_rails = false
		return
		
	var block_pos = Vector3i(int(floor(global_position.x)), int(floor(global_position.y)), int(floor(global_position.z)))
	var current_block = world.get_block_world(block_pos)
	var below_block = world.get_block_world(block_pos + Vector3i(0, -1, 0))
	
	is_on_rails = (current_block == VoxelChunk.BlockType.MINING_RAIL or below_block == VoxelChunk.BlockType.MINING_RAIL)
