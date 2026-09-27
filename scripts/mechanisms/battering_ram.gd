# scripts/mechanisms/battering_ram.gd
# Voxel Lord: Feudal Realm - Milestone 34: Armored Wheeled Battering Ram Penthouse
# Four-wheeled timber shed covered in rawhides housing a chain-suspended oak battering ram.

class_name BatteringRam
extends Node3D

signal state_changed(new_state: RamState)
signal impact_delivered(damage: float)
signal damaged(current_hp: float, max_hp: float)
signal destroyed()

enum RamState {
	IDLE,
	ROLLING,
	SWINGING,
	STRIKING
}

const MAX_HP: float = 600.0
const STRIKE_DAMAGE: float = 180.0
const SWING_CYCLE_TIME: float = 3.2     # seconds per back-and-forth swing cycle
const MAX_CREW: int = 4
const MIN_CREW: int = 2
const ARROW_DEFLECTION_RATE: float = 0.80 # 80% missile damage ignored by rawhide roof
const FIRE_RESISTANCE_RATE: float = 0.50   # 50% boiling pitch fire mitigation

@export var current_state: RamState = RamState.IDLE
@export var current_hp: float = MAX_HP
@export var assigned_crew: int = 4

var swing_timer: float = 0.0
var total_strikes_delivered: int = 0

func _init(p_start_crew: int = 4) -> void:
	assigned_crew = clamp(p_start_crew, 0, MAX_CREW)
	current_hp = MAX_HP
	current_state = RamState.IDLE
	swing_timer = 0.0
	total_strikes_delivered = 0

func set_crew(count: int) -> void:
	assigned_crew = clamp(count, 0, MAX_CREW)

func can_operate() -> bool:
	return current_hp > 0.0 and assigned_crew >= MIN_CREW

func get_movement_speed() -> float:
	if not can_operate():
		return 0.0
	# 0.8 m/s with full 4 crew, 0.4 m/s with 2 crew
	return 0.2 * float(assigned_crew)

func start_swinging() -> bool:
	if not can_operate():
		return false
	current_state = RamState.SWINGING
	swing_timer = 0.0
	state_changed.emit(current_state)
	return true

func stop_swinging() -> void:
	if current_state != RamState.IDLE:
		current_state = RamState.IDLE
		swing_timer = 0.0
		state_changed.emit(current_state)

func process_tick(delta: float) -> float:
	# Returns damage dealt if a strike lands this tick, else 0.0
	if not can_operate() or current_state != RamState.SWINGING:
		return 0.0

	swing_timer += delta
	if swing_timer >= SWING_CYCLE_TIME:
		swing_timer -= SWING_CYCLE_TIME
		total_strikes_delivered += 1
		impact_delivered.emit(STRIKE_DAMAGE)
		return STRIKE_DAMAGE

	return 0.0

func take_damage(raw_damage: float, is_missile: bool = false, is_fire: bool = false) -> float:
	if current_hp <= 0.0:
		return 0.0

	var actual_damage: float = raw_damage
	if is_missile:
		actual_damage *= (1.0 - ARROW_DEFLECTION_RATE) # Only 20% penetrates
	elif is_fire:
		actual_damage *= (1.0 - FIRE_RESISTANCE_RATE)   # Only 50% penetrates

	current_hp = max(0.0, current_hp - actual_damage)
	damaged.emit(current_hp, MAX_HP)

	if current_hp <= 0.0:
		current_state = RamState.IDLE
		destroyed.emit()

	return actual_damage
