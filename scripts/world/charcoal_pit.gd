class_name CharcoalPit
extends StaticBody3D

## TerraFirmaCraft-style Earthen Charcoal Burning Pit.
## High-temperature smelting in Bloomeries requires Charcoal (>1400°C), as raw wood
## cannot achieve reducing temperatures and contains excessive moisture.
## Players stack timber logs into an earthen trench or mound, seal the mound with clay/dirt sods,
## and ignite a controlled low-oxygen smoldering burn (Pyrolysis).
## If properly sealed, 100% of logs convert into high-grade Charcoal.
## If unsealed, the fire burns with open oxygen, reducing all timber to useless ash.

signal pyrolysis_started()
signal pyrolysis_completed(charcoal_amount: int)
signal charcoal_harvested(amount: int)

enum PitState {
	EMPTY = 0,
	LOADED = 1,
	BURNING = 2,
	READY = 3,
	BURNT_OUT_ASH = 4
}

const BURN_TIME: float = 8.0 # Smoldering duration in seconds
const LOG_TO_CHARCOAL_RATIO: int = 1 # 1 log -> 1 high-grade charcoal under seal

var supply_chain: SupplyChain = null
var current_state: PitState = PitState.EMPTY
var logs_stacked: int = 0
var charcoal_produced: int = 0
var is_sealed: bool = true # Must be covered with earth/clay
var burn_timer: float = 0.0

var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null
var ember_light: OmniLight3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(2.2, 1.2, 2.2)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.6, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/charcoal_pit.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	ember_light = OmniLight3D.new()
	ember_light.light_color = Color(1.0, 0.35, 0.05)
	ember_light.light_energy = 0.0
	ember_light.omni_range = 4.0
	ember_light.position = Vector3(0, 0.8, 0)
	add_child(ember_light)

	prompt_label = Label3D.new()
	prompt_label.text = "🪵 TFC Charcoal Pit\n[E] Stack Logs (0/8)"
	prompt_label.position = Vector3(0, 1.6, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 20
	prompt_label.modulate = Color(0.9, 0.7, 0.4)
	add_child(prompt_label)

func stack_logs(count: int) -> bool:
	if current_state != PitState.EMPTY and current_state != PitState.LOADED:
		return false
	logs_stacked += count
	current_state = PitState.LOADED
	_update_prompt()
	return true

func set_sealed(sealed: bool) -> void:
	is_sealed = sealed
	_update_prompt()

func ignite() -> bool:
	if current_state != PitState.LOADED or logs_stacked <= 0:
		return false
	current_state = PitState.BURNING
	burn_timer = 0.0
	if ember_light:
		ember_light.light_energy = 1.8
	emit_signal("pyrolysis_started")
	_update_prompt()
	return true

func _process(delta: float) -> void:
	if current_state == PitState.BURNING:
		burn_timer += delta
		# Subtle ember pulse
		if ember_light:
			ember_light.light_energy = 1.6 + sin(burn_timer * 4.0) * 0.4
			
		if burn_timer >= BURN_TIME:
			if is_sealed:
				current_state = PitState.READY
				charcoal_produced = logs_stacked * LOG_TO_CHARCOAL_RATIO
				logs_stacked = 0
				emit_signal("pyrolysis_completed", charcoal_produced)
			else:
				current_state = PitState.BURNT_OUT_ASH
				charcoal_produced = 0
				logs_stacked = 0
			
			if ember_light:
				ember_light.light_energy = 0.3
			_update_prompt()

func harvest() -> Dictionary:
	if current_state == PitState.READY:
		var harvested = charcoal_produced
		charcoal_produced = 0
		current_state = PitState.EMPTY
		if supply_chain:
			supply_chain.add_resource("charcoal", harvested)
		emit_signal("charcoal_harvested", harvested)
		_update_prompt()
		return {
			"success": true,
			"charcoal": harvested,
			"message": "Harvested %d High-Grade Charcoal from the smothered pit!" % harvested
		}
	elif current_state == PitState.BURNT_OUT_ASH:
		current_state = PitState.EMPTY
		_update_prompt()
		return {
			"success": false,
			"charcoal": 0,
			"message": "The pit was unsealed during burning! All wood was consumed to worthless ash."
		}
	return {"success": false, "charcoal": 0, "message": "Nothing ready to harvest."}

func _update_prompt() -> void:
	if not prompt_label:
		return
	match current_state:
		PitState.EMPTY:
			prompt_label.text = "🪵 TFC Charcoal Pit (Empty)\n[E] Stack Timber Logs"
			prompt_label.modulate = Color(0.9, 0.7, 0.4)
		PitState.LOADED:
			var seal_txt = "Sealed (Clay/Dirt Sod)" if is_sealed else "⚠️ UNSEALED"
			prompt_label.text = "🪵 TFC Charcoal Pit (%d Logs)\nStatus: %s\n[E] Ignite Smolder" % [logs_stacked, seal_txt]
			prompt_label.modulate = Color(0.6, 0.9, 0.4) if is_sealed else Color(1.0, 0.4, 0.3)
		PitState.BURNING:
			prompt_label.text = "🔥 Smoldering Pyrolysis in Progress...\nTime: %.1fs / %.1fs" % [burn_timer, BURN_TIME]
			prompt_label.modulate = Color(1.0, 0.45, 0.1)
		PitState.READY:
			prompt_label.text = "✨ Charcoal Burn Complete!\nReady: %d High-Grade Charcoal\n[E] Uncover & Harvest" % charcoal_produced
			prompt_label.modulate = Color(0.3, 0.95, 0.6)
		PitState.BURNT_OUT_ASH:
			prompt_label.text = "💨 Burnt to Ash (Excess Oxygen!)\n[E] Clear Ash Residue"
			prompt_label.modulate = Color(0.6, 0.6, 0.6)

# --- Static Simulation & Balance Calculations ---

static func calculate_charcoal_yield(logs_count: int, sealed: bool) -> int:
	if not sealed:
		return 0 # All logs burn to ash if oxygen is freely available
	return logs_count * LOG_TO_CHARCOAL_RATIO
