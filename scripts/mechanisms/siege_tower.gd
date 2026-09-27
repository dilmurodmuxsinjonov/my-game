# scripts/mechanisms/siege_tower.gd
# Voxel Lord: Feudal Realm - Milestone 34: Mobile Assault Belfry Siege Tower
# 8-meter multi-tiered wheeled timber tower with archery slit hoardings and drop assault bridge.

class_name SiegeTower
extends Node3D

signal state_changed(new_state: TowerState)
signal bridge_deployed()
signal troops_disembarked(count: int)
signal damaged(current_hp: float, max_hp: float)
signal destroyed()

enum TowerState {
	IDLE,
	APPROACHING,
	AT_WALL,
	BRIDGE_DEPLOYED
}

const MAX_HP: float = 800.0
const MAX_PUSH_CREW: int = 6
const MIN_PUSH_CREW: int = 3
const MAX_ARCHERS: int = 4
const MAX_STORM_TROOPS: int = 8
const BRIDGE_LOWER_TIME: float = 2.0     # 2.0s for assault gangplank to drop onto battlements
const HOARDING_DEFENSE_RATE: float = 0.70 # 70% arrow deflection for troops inside

@export var current_state: TowerState = TowerState.IDLE
@export var current_hp: float = MAX_HP
@export var push_crew: int = 6
@export var archer_count: int = 4
@export var storm_troop_count: int = 8
@export var is_bridge_lowered: bool = false

var bridge_timer: float = 0.0
var disembark_timer: float = 0.0

func _init(p_crew: int = 6, p_archers: int = 4, p_troops: int = 8) -> void:
	push_crew = clamp(p_crew, 0, MAX_PUSH_CREW)
	archer_count = clamp(p_archers, 0, MAX_ARCHERS)
	storm_troop_count = clamp(p_troops, 0, MAX_STORM_TROOPS)
	current_hp = MAX_HP
	current_state = TowerState.IDLE
	is_bridge_lowered = false

func can_roll() -> bool:
	return current_hp > 0.0 and push_crew >= MIN_PUSH_CREW and current_state != TowerState.BRIDGE_DEPLOYED

func get_movement_speed() -> float:
	if not can_roll():
		return 0.0
	# 0.6 m/s with full 6 crew, 0.3 m/s with 3 crew
	return 0.1 * float(push_crew)

func reach_wall() -> bool:
	if current_hp <= 0.0:
		return false
	current_state = TowerState.AT_WALL
	state_changed.emit(current_state)
	return true

func deploy_assault_bridge() -> bool:
	if current_state != TowerState.AT_WALL or is_bridge_lowered:
		return false
	bridge_timer = 0.0
	return true

func process_tick(delta: float) -> int:
	# Returns number of troops disembarked onto ramparts this tick
	if current_hp <= 0.0:
		return 0

	var disembarked_this_tick: int = 0

	if current_state == TowerState.AT_WALL and not is_bridge_lowered:
		bridge_timer += delta
		if bridge_timer >= BRIDGE_LOWER_TIME:
			is_bridge_lowered = true
			current_state = TowerState.BRIDGE_DEPLOYED
			state_changed.emit(current_state)
			bridge_deployed.emit()

	elif current_state == TowerState.BRIDGE_DEPLOYED and storm_troop_count > 0:
		# Disembark at 2 troops per second (1 troop every 0.5s)
		disembark_timer += delta
		while disembark_timer >= 0.5 and storm_troop_count > 0:
			disembark_timer -= 0.5
			storm_troop_count -= 1
			disembarked_this_tick += 1

		if disembarked_this_tick > 0:
			troops_disembarked.emit(disembarked_this_tick)

	return disembarked_this_tick

func take_damage(raw_damage: float, is_missile: bool = false) -> float:
	if current_hp <= 0.0:
		return 0.0

	var actual_damage: float = raw_damage
	if is_missile:
		actual_damage *= (1.0 - HOARDING_DEFENSE_RATE) # Only 30% penetrates

	current_hp = max(0.0, current_hp - actual_damage)
	damaged.emit(current_hp, MAX_HP)

	if current_hp <= 0.0:
		current_state = TowerState.IDLE
		destroyed.emit()

	return actual_damage
