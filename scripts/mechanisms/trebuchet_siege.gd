# scripts/mechanisms/trebuchet_siege.gd
# Voxel Lord: Feudal Realm - Milestone 34: Counterweight Trebuchet Siege Engine
# Massive hinged counterweight siege artillery hurling heavy stones, incendiary pitch, or diseased carcasses.

class_name TrebuchetSiege
extends Node3D

signal state_changed(new_state: TrebuchetState)
signal fired(projectile_type: ProjectileType, target_pos: Vector3, damage: float)
signal reloaded()

enum TrebuchetState {
	READY,
	AIMING,
	FIRING,
	RELOADING
}

enum ProjectileType {
	STONE_BOULDER,    # 320 structural damage, 8m shockwave
	INCENDIARY_PITCH, # 240 structural damage, 120 fire burn over 10s, 10m burn radius
	COW_CARCASS       # Biological warfare: plague cloud, -30 morale in 15m radius
}

const MIN_RANGE_METERS: float = 40.0
const MAX_RANGE_METERS: float = 140.0
const MANUAL_RELOAD_TIME: float = 15.0   # 15s with 3 engineers manual winch winding
const KINETIC_RELOAD_TIME: float = 4.5   # 4.5s when powered by kinetic drive shaft
const KINETIC_LOAD_SU: float = 80.0      # Kinetic stress units required during reload
const REQUIRED_CREW: int = 3

@export var current_state: TrebuchetState = TrebuchetState.READY
@export var assigned_crew: int = 3
@export var current_ammo_type: ProjectileType = ProjectileType.STONE_BOULDER
@export var is_kinetic_powered: bool = false
@export var input_rpm: float = 0.0

var reload_timer: float = 0.0
var ammo_inventory: Dictionary = {
	ProjectileType.STONE_BOULDER: 10,
	ProjectileType.INCENDIARY_PITCH: 4,
	ProjectileType.COW_CARCASS: 2
}

func _init(p_start_crew: int = 3) -> void:
	assigned_crew = p_start_crew
	current_state = TrebuchetState.READY
	current_ammo_type = ProjectileType.STONE_BOULDER
	reload_timer = 0.0

func set_projectile_type(type: ProjectileType) -> void:
	current_ammo_type = type

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	is_kinetic_powered = abs(input_rpm) >= 16.0

func can_fire_at_target(distance: float) -> bool:
	if current_state != TrebuchetState.READY:
		return false
	if distance < MIN_RANGE_METERS or distance > MAX_RANGE_METERS:
		return false
	if ammo_inventory.get(current_ammo_type, 0) <= 0:
		return false
	if not is_kinetic_powered and assigned_crew < REQUIRED_CREW:
		return false
	return true

func fire_at_target(target_dist: float) -> Dictionary:
	if not can_fire_at_target(target_dist):
		return {"success": False, "damage": 0.0, "reason": "Cannot fire"}

	ammo_inventory[current_ammo_type] -= 1
	current_state = TrebuchetState.FIRING
	state_changed.emit(current_state)

	var damage: float = 320.0
	var aoe_radius: float = 8.0
	var fire_dps: float = 0.0
	var morale_penalty: float = 0.0

	if current_ammo_type == ProjectileType.INCENDIARY_PITCH:
		damage = 240.0
		aoe_radius = 10.0
		fire_dps = 12.0
	elif current_ammo_type == ProjectileType.COW_CARCASS:
		damage = 50.0
		aoe_radius = 15.0
		morale_penalty = -30.0

	# Begin reload cycle
	current_state = TrebuchetState.RELOADING
	state_changed.emit(current_state)
	reload_timer = 0.0

	return {
		"success": True,
		"projectile": current_ammo_type,
		"damage": damage,
		"aoe_radius": aoe_radius,
		"fire_dps": fire_dps,
		"morale_penalty": morale_penalty
	}

func get_reload_duration() -> float:
	if is_kinetic_powered and abs(input_rpm) > 0.0:
		return KINETIC_RELOAD_TIME
	return MANUAL_RELOAD_TIME

func process_tick(delta: float) -> void:
	if current_state == TrebuchetState.RELOADING:
		var target_duration: float = get_reload_duration()
		reload_timer += delta
		if reload_timer >= target_duration:
			reload_timer = 0.0
			current_state = TrebuchetState.READY
			state_changed.emit(current_state)
			reloaded.emit()

func get_kinetic_load() -> float:
	if current_state == TrebuchetState.RELOADING and is_kinetic_powered:
		return KINETIC_LOAD_SU
	return 0.0
