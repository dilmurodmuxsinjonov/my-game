class_name BlueprintConstruction
extends Node3D

## MineColonies-Style Holographic Blueprint & Construction Site.
## Manages holographic ghost visualization, multi-stage material delivery,
## progressive voxel construction by Citizen Builders, and structure instantiation.

signal construction_started(blueprint: BlueprintConstruction)
signal material_delivered(blueprint: BlueprintConstruction, resource: String, amount: int)
signal build_progressed(blueprint: BlueprintConstruction, progress_percent: float)
signal construction_completed(blueprint: BlueprintConstruction)

@export var structure_id: String = "cottage"
@export var display_name: String = "Worker Cottage"
@export var bounds_size: Vector3 = Vector3(4.0, 3.0, 4.0)

# Resource Requirements (MineColonies style)
@export var required_resources: Dictionary = {
	"logs": 8,
	"stone": 12
}
var delivered_resources: Dictionary = {}

# Construction Progress
var total_build_steps: int = 10
var completed_build_steps: int = 0
var is_completed: bool = false

# Voxel layout definitions (relative offset -> block_type)
var voxel_layout: Array[Dictionary] = []

# Node references
var ghost_mesh: MeshInstance3D
var status_billboard: Label3D
var progress_bar_mesh: MeshInstance3D

func _ready() -> void:
	add_to_group("blueprints")
	_init_delivered_dict()
	_setup_holographic_visuals()
	_update_billboard()
	emit_signal("construction_started", self)

func _init_delivered_dict() -> void:
	for res in required_resources.keys():
		if not delivered_resources.has(res):
			delivered_resources[res] = 0

func _setup_holographic_visuals() -> void:
	# Holographic semi-transparent bounding box
	ghost_mesh = MeshInstance3D.new()
	var box = BoxMesh.new()
	box.size = bounds_size
	ghost_mesh.mesh = box
	ghost_mesh.position = Vector3(0, bounds_size.y * 0.5, 0)
	
	var mat = StandardMaterial3D.new()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_color = Color(0.15, 0.75, 1.0, 0.28) # Cyan blueprint hologram
	mat.emission_enabled = true
	mat.emission = Color(0.05, 0.4, 0.8)
	mat.emission_energy_multiplier = 0.5
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	ghost_mesh.material_override = mat
	add_child(ghost_mesh)
	
	# Overhead Status Billboard
	status_billboard = Label3D.new()
	status_billboard.position = Vector3(0, bounds_size.y + 0.9, 0)
	status_billboard.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	status_billboard.font_size = 24
	status_billboard.modulate = Color(1.0, 0.9, 0.4)
	add_child(status_billboard)

func deliver_material(resource: String, amount: int) -> int:
	if is_completed or amount <= 0:
		return 0
	if not required_resources.has(resource):
		return 0
		
	var needed = required_resources[resource] - delivered_resources.get(resource, 0)
	if needed <= 0:
		return 0
		
	var accepted = mini(amount, needed)
	delivered_resources[resource] = delivered_resources.get(resource, 0) + accepted
	_update_billboard()
	emit_signal("material_delivered", self, resource, accepted)
	return accepted

func has_all_materials() -> bool:
	for res in required_resources.keys():
		if delivered_resources.get(res, 0) < required_resources[res]:
			return false
	return true

func get_missing_materials() -> Dictionary:
	var missing: Dictionary = {}
	for res in required_resources.keys():
		var diff = required_resources[res] - delivered_resources.get(res, 0)
		if diff > 0:
			missing[res] = diff
	return missing

func advance_construction(amount: float = 1.0) -> bool:
	if is_completed:
		return false
	if not has_all_materials():
		return false
		
	completed_build_steps = mini(total_build_steps, completed_build_steps + int(ceil(amount)))
	var pct = float(completed_build_steps) / float(total_build_steps) * 100.0
	_update_billboard()
	emit_signal("build_progressed", self, pct)
	
	if completed_build_steps >= total_build_steps:
		complete_construction()
		return true
	return false

func complete_construction(voxel_world: VoxelWorld = null) -> void:
	if is_completed:
		return
	is_completed = true
	remove_from_group("blueprints")
	
	# Materialize actual voxels if voxel_world is provided
	if voxel_world and not voxel_layout.is_empty():
		var origin = Vector3i(int(floor(global_position.x)), int(floor(global_position.y)), int(floor(global_position.z)))
		for item in voxel_layout:
			var offset: Vector3i = item.get("pos", Vector3i.ZERO)
			var b_type: int = item.get("type", 1) # 1 = stone / wood
			voxel_world.set_block(origin.x + offset.x, origin.y + offset.y, origin.z + offset.z, b_type)
			
	# Update visuals to solid / completed state
	if ghost_mesh:
		var mat = StandardMaterial3D.new()
		mat.albedo_color = Color(0.2, 0.9, 0.4, 0.8) # Gold/green completion flash
		ghost_mesh.material_override = mat
		
	if status_billboard:
		status_billboard.text = "%s\n[COMPLETED]" % display_name
		status_billboard.modulate = Color(0.3, 1.0, 0.4)
		
	emit_signal("construction_completed", self)

func _update_billboard() -> void:
	if not status_billboard:
		return
		
	if is_completed:
		status_billboard.text = "%s\n[COMPLETED]" % display_name
		return
		
	var lines: Array[String] = []
	lines.append("Blueprint: %s" % display_name)
	
	var mat_strs: Array[String] = []
	for res in required_resources.keys():
		var cur = delivered_resources.get(res, 0)
		var req = required_resources[res]
		mat_strs.append("%s: %d/%d" % [res.capitalize(), cur, req])
	lines.append(" | ".join(mat_strs))
	
	var pct = int(float(completed_build_steps) / float(total_build_steps) * 100.0)
	lines.append("Construction: %d%%" % pct)
	
	status_billboard.text = "\n".join(lines)
