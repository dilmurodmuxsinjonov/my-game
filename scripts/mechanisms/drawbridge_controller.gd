# scripts/mechanisms/drawbridge_controller.gd
# Voxel Lord: Feudal Realm - Milestone 33: Castle Moat Drawbridge Winch & Platform
# Heavy timber and iron drawbridge spanning moat defenses, driven manually or via kinetic shafts.

class_name DrawbridgeController
extends Node3D

signal state_changed(new_state: BridgeState)
signal chain_damaged(chain_id: int, current_hp: float, max_hp: float)
signal bridge_collapsed(crush_damage: float)

enum BridgeState {
	CLOSED,   # Fully lowered (horizontal, 0 deg) - pedestrians can cross
	OPENING,  # Raising upward towards vertical
	OPEN,     # Fully raised (vertical, 90 deg) - moat impassable, gate defended
	CLOSING,  # Lowering downward towards horizontal
	BROKEN    # Chains severed; platform collapsed into moat
}

const MAX_CHAIN_HP: float = 800.0
const MANUAL_DURATION: float = 12.0     # 12s for manual crank by guards
const KINETIC_DURATION: float = 3.5     # 3.5s when powered by kinetic drive shaft
const CRUSH_DAMAGE: float = 120.0       # Crushing damage if collapsed onto units below
const KINETIC_LOAD_SU: float = 64.0     # Kinetic network stress unit load when active

@export var current_state: BridgeState = BridgeState.CLOSED
@export var current_angle: float = 0.0  # 0.0 (horizontal) to 90.0 (vertical)
@export var is_kinetic_powered: bool = false
@export var input_rpm: float = 0.0

var chain_hp: Array[float] = [MAX_CHAIN_HP, MAX_CHAIN_HP] # [Left Chain, Right Chain]
var is_collapsed: bool = false
var target_state: BridgeState = BridgeState.CLOSED

func _init(p_start_state: BridgeState = BridgeState.CLOSED) -> void:
	current_state = p_start_state
	target_state = p_start_state
	current_angle = 90.0 if p_start_state == BridgeState.OPEN else 0.0
	chain_hp = [MAX_CHAIN_HP, MAX_CHAIN_HP]
	is_collapsed = false

func raise_bridge() -> void:
	if current_state == BridgeState.BROKEN:
		return
	if current_state != BridgeState.OPEN and current_state != BridgeState.OPENING:
		target_state = BridgeState.OPEN
		current_state = BridgeState.OPENING
		state_changed.emit(current_state)

func lower_bridge() -> void:
	if current_state == BridgeState.BROKEN:
		return
	if current_state != BridgeState.CLOSED and current_state != BridgeState.CLOSING:
		target_state = BridgeState.CLOSED
		current_state = BridgeState.CLOSING
		state_changed.emit(current_state)

func toggle_bridge() -> void:
	if current_state == BridgeState.CLOSED or current_state == BridgeState.CLOSING:
		raise_bridge()
	elif current_state == BridgeState.OPEN or current_state == BridgeState.OPENING:
		lower_bridge()

func damage_chain(chain_idx: int, amount: float) -> void:
	if chain_idx < 0 or chain_idx >= chain_hp.size():
		return
	if is_collapsed:
		return
		
	chain_hp[chain_idx] = max(0.0, chain_hp[chain_idx] - amount)
	chain_damaged.emit(chain_idx, chain_hp[chain_idx], MAX_CHAIN_HP)
	
	# If either or both chains snap completely under tension
	if chain_hp[0] <= 0.0 and chain_hp[1] <= 0.0:
		_trigger_catastrophic_collapse()

func _trigger_catastrophic_collapse() -> void:
	is_collapsed = true
	current_state = BridgeState.BROKEN
	current_angle = 0.0 # Falls flat onto moat bed
	bridge_collapsed.emit(CRUSH_DAMAGE)
	state_changed.emit(current_state)

func repair_chains() -> void:
	chain_hp = [MAX_CHAIN_HP, MAX_CHAIN_HP]
	is_collapsed = false
	current_state = BridgeState.CLOSED
	current_angle = 0.0
	state_changed.emit(current_state)

func update_kinetics(rpm: float) -> void:
	input_rpm = rpm
	is_kinetic_powered = abs(input_rpm) >= 12.0

func get_active_speed_deg_per_sec() -> float:
	var duration: float = KINETIC_DURATION if (is_kinetic_powered and abs(input_rpm) > 0.0) else MANUAL_DURATION
	return 90.0 / duration

func process_tick(delta: float) -> void:
	if current_state == BridgeState.BROKEN:
		return
		
	var speed: float = get_active_speed_deg_per_sec()
	
	if current_state == BridgeState.OPENING:
		current_angle = min(90.0, current_angle + speed * delta)
		if current_angle >= 90.0:
			current_state = BridgeState.OPEN
			state_changed.emit(current_state)
	elif current_state == BridgeState.CLOSING:
		current_angle = max(0.0, current_angle - speed * delta)
		if current_angle <= 0.0:
			current_state = BridgeState.CLOSED
			state_changed.emit(current_state)

func get_progress_ratio() -> float:
	return clamp(current_angle / 90.0, 0.0, 1.0)

func is_traversable() -> bool:
	return current_state == BridgeState.CLOSED and current_angle <= 2.0 and not is_collapsed

func get_kinetic_load() -> float:
	if current_state == BridgeState.OPENING or current_state == BridgeState.CLOSING:
		return KINETIC_LOAD_SU if is_kinetic_powered else 0.0
	return 0.0
