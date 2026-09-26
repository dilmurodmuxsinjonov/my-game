# scripts/world/portcullis_gate.gd
# Voxel Lord: Feudal Realm - Milestone 23: Fortified Castle Portcullis Gate
# Inspired by Stronghold (Gatehouses & Portcullis) and Mount & Blade II (Siege Gate Breaching)

class_name PortcullisGate
extends Node3D

signal portcullis_opened()
signal portcullis_closed()
signal portcullis_damaged(current_hp: float, max_hp: float)
signal gate_destroyed()
signal enemies_crushed(damage: float, count: int)

const MAX_HP: float = 500.0
const CRUSH_DAMAGE: float = 80.0
const WINCH_DURATION_SECONDS: float = 3.0

var current_hp: float = MAX_HP
var is_open: bool = false
var is_moving: bool = false
var motion_progress: float = 0.0 # 0.0 = fully closed, 1.0 = fully open
var motion_target: float = 0.0

func _init() -> void:
	current_hp = MAX_HP
	is_open = false
	motion_progress = 0.0
	motion_target = 0.0

func open_portcullis() -> bool:
	if current_hp <= 0.0:
		return false
	if is_open and motion_progress >= 1.0:
		return false
	
	motion_target = 1.0
	is_moving = true
	return true

func close_portcullis() -> bool:
	if current_hp <= 0.0:
		return false
	if not is_open and motion_progress <= 0.0:
		return false
	
	motion_target = 0.0
	is_moving = true
	return true

func toggle_portcullis() -> bool:
	if is_open or motion_target > 0.5:
		return close_portcullis()
	else:
		return open_portcullis()

func update_winch(delta: float, enemies_underneath_count: int = 0) -> Dictionary:
	var crushed_result: Dictionary = {"crushed": false, "damage": 0.0, "count": 0}
	if not is_moving:
		return crushed_result
	
	var step: float = delta / WINCH_DURATION_SECONDS
	if motion_target > motion_progress:
		motion_progress = minf(1.0, motion_progress + step)
		if motion_progress >= 1.0:
			motion_progress = 1.0
			is_moving = false
			is_open = true
			portcullis_opened.emit()
	else:
		motion_progress = maxf(0.0, motion_progress - step)
		# If lowering gate and enemies are caught directly underneath
		if enemies_underneath_count > 0 and motion_progress < 0.3:
			crushed_result = {
				"crushed": true,
				"damage": CRUSH_DAMAGE,
				"count": enemies_underneath_count
			}
			enemies_crushed.emit(CRUSH_DAMAGE, enemies_underneath_count)
			
		if motion_progress <= 0.0:
			motion_progress = 0.0
			is_moving = false
			is_open = false
			portcullis_closed.emit()
			
	return crushed_result

func take_damage(amount: float, damage_type: String = "blunt") -> float:
	if current_hp <= 0.0:
		return 0.0
	
	var multiplier: float = 1.0
	match damage_type:
		"blunt":
			multiplier = 0.50 # 50% resistance against battering rams and hammers
		"pierce":
			multiplier = 0.20 # 80% deflection against arrows and spears
		"slash":
			multiplier = 0.30 # 70% deflection against swords/axes
		"siege":
			multiplier = 1.25 # Vulnerable to heavy siege artillery boulders
		_:
			multiplier = 1.0
	
	var actual_damage: float = amount * multiplier
	current_hp = maxf(0.0, current_hp - actual_damage)
	portcullis_damaged.emit(current_hp, MAX_HP)
	
	if current_hp <= 0.0:
		is_open = true
		gate_destroyed.emit()
		
	return actual_damage

func repair_gate(amount: float) -> float:
	if current_hp >= MAX_HP:
		return 0.0
	var prev: float = current_hp
	current_hp = minf(MAX_HP, current_hp + amount)
	return current_hp - prev
