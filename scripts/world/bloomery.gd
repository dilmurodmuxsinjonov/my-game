class_name Bloomery
extends StaticBody3D

## TerraFirmaCraft-style Refractory Shaft Bloomery Smelting Furnace.
## Unlike simple campfires, true iron cannot melt into liquid in early medieval furnaces.
## The Bloomery operates at 1200°C - 1450°C using Charcoal fuel to chemically reduce
## Iron Ore (or Crushed Iron) in a low-oxygen atmosphere into a spongy, porous "Iron Bloom"
## consisting of metallic iron interspersed with silicate slag.
## The Iron Bloom must then be hammered on an Anvil or under a Trip Hammer to consolidate
## it into pure Wrought Iron Ingots.

signal bloom_smelted(bloom_count: int)
signal temperature_changed(current_temp: float, target_temp: float)

enum SmelterState {
	IDLE = 0,
	HEATING = 1,
	SMELTING = 2,
	READY_FOR_TAP = 3
}

const MIN_SMELT_TEMP: float = 1200.0 # °C required for iron oxide reduction
const MAX_TEMP: float = 1450.0 # °C with charcoal forced air draft
const HEAT_RATE: float = 45.0 # °C per second
const COOL_RATE: float = 20.0 # °C per second
const SMELT_CYCLE_DURATION: float = 6.0 # Seconds per bloom cycle

var supply_chain: SupplyChain = null
var current_state: SmelterState = SmelterState.IDLE
var current_temperature: float = 20.0 # Ambient temperature
var target_temperature: float = 20.0
var charcoal_fuel: int = 0
var iron_ore_loaded: int = 0
var blooms_ready: int = 0
var smelt_timer: float = 0.0

var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null
var hearth_light: OmniLight3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.6, 2.5, 1.6)
	collision_box.shape = box
	collision_box.position = Vector3(0, 1.25, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/bloomery.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	hearth_light = OmniLight3D.new()
	hearth_light.light_color = Color(1.0, 0.45, 0.1)
	hearth_light.light_energy = 0.0 # Turned off until lit
	hearth_light.omni_range = 5.0
	hearth_light.position = Vector3(0, 0.6, 0.5)
	add_child(hearth_light)

	prompt_label = Label3D.new()
	prompt_label.text = "🔥 TerraFirmaCraft Bloomery\n[E] Load Charcoal & Iron Ore"
	prompt_label.position = Vector3(0, 2.7, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 22
	prompt_label.modulate = Color(1.0, 0.65, 0.3)
	add_child(prompt_label)

func load_materials(charcoal_amt: int, ore_amt: int) -> bool:
	if charcoal_amt <= 0 and ore_amt <= 0:
		return false
	charcoal_fuel += charcoal_amt
	iron_ore_loaded += ore_amt
	_update_prompt()
	return true

func ignite() -> bool:
	if charcoal_fuel <= 0:
		return false
	if current_state == SmelterState.IDLE:
		current_state = SmelterState.HEATING
		target_temperature = MAX_TEMP
		_update_prompt()
		return true
	return false

func _process(delta: float) -> void:
	if current_state == SmelterState.HEATING or current_state == SmelterState.SMELTING:
		# Heat up toward target
		if current_temperature < target_temperature:
			current_temperature = minf(current_temperature + HEAT_RATE * delta, target_temperature)
			emit_signal("temperature_changed", current_temperature, target_temperature)
		
		# Hearth visual light intensity scales with temperature
		if hearth_light:
			hearth_light.light_energy = clampf((current_temperature - 200.0) / 1000.0 * 2.5, 0.0, 3.5)

		if current_temperature >= MIN_SMELT_TEMP and iron_ore_loaded >= 2 and charcoal_fuel >= 2:
			current_state = SmelterState.SMELTING
			smelt_timer += delta
			if smelt_timer >= SMELT_CYCLE_DURATION:
				smelt_timer = 0.0
				iron_ore_loaded -= 2
				charcoal_fuel -= 2
				blooms_ready += 1
				emit_signal("bloom_smelted", blooms_ready)
				
				if iron_ore_loaded < 2 or charcoal_fuel < 2:
					current_state = SmelterState.READY_FOR_TAP
		elif charcoal_fuel <= 0:
			target_temperature = 20.0
			current_state = SmelterState.IDLE
	else:
		# Cooling down
		if current_temperature > 20.0:
			current_temperature = maxf(current_temperature - COOL_RATE * delta, 20.0)
			emit_signal("temperature_changed", current_temperature, 20.0)
			if hearth_light:
				hearth_light.light_energy = clampf((current_temperature - 200.0) / 1000.0 * 2.5, 0.0, 3.5)
	
	_update_prompt()

func tap_bloom() -> Dictionary:
	if blooms_ready <= 0:
		return {"success": false, "bloom_count": 0, "message": "No iron blooms ready to tap."}
	var count = blooms_ready
	blooms_ready = 0
	if iron_ore_loaded >= 2 and charcoal_fuel >= 2 and current_temperature >= MIN_SMELT_TEMP:
		current_state = SmelterState.SMELTING
	else:
		current_state = SmelterState.IDLE
		target_temperature = 20.0
		
	if supply_chain:
		supply_chain.add_resource("iron_bloom", count)
	
	_update_prompt()
	return {
		"success": true,
		"bloom_count": count,
		"item": "iron_bloom",
		"message": "Extracted %d spongy Iron Bloom(s)! Refine on Anvil or Trip Hammer to consolidate." % count
	}

func _update_prompt() -> void:
	if not prompt_label:
		return
	match current_state:
		SmelterState.IDLE:
			prompt_label.text = "🔥 TFC Bloomery (Idle: %.0f°C)\nFuel: %d Charcoal | Ore: %d Iron\n[E] Load Fuel / Ore & Ignite" % [
				current_temperature, charcoal_fuel, iron_ore_loaded
			]
			prompt_label.modulate = Color(1.0, 0.65, 0.3)
		SmelterState.HEATING:
			prompt_label.text = "🔥 TFC Bloomery (Heating: %.0f°C / %.0f°C)\nAir Bellows Draft Active..." % [
				current_temperature, target_temperature
			]
			prompt_label.modulate = Color(1.0, 0.45, 0.15)
		SmelterState.SMELTING:
			prompt_label.text = "⚡ TFC Bloomery (Smelting: %.0f°C)\nReducing Iron Oxides -> Spongy Bloom...\nFuel: %d | Ore: %d" % [
				current_temperature, charcoal_fuel, iron_ore_loaded
			]
			prompt_label.modulate = Color(1.0, 0.3, 0.1)
		SmelterState.READY_FOR_TAP:
			prompt_label.text = "✨ TFC Bloomery (Smelt Complete!)\nReady to Tap: %d Iron Bloom(s)\n[E] Tap & Extract Spongy Bloom" % blooms_ready
			prompt_label.modulate = Color(0.4, 0.95, 0.5)

# --- Static Simulation & Balance Calculations ---

static func calculate_bloom_reduction(ore_count: int, charcoal_count: int) -> Dictionary:
	## 2x Iron Ore + 2x Charcoal = 1x Iron Bloom (Porous Metallic Sponge + Slag)
	var max_by_ore = ore_count / 2
	var max_by_fuel = charcoal_count / 2
	var potential_blooms = mini(max_by_ore, max_by_fuel)
	var ore_consumed = potential_blooms * 2
	var fuel_consumed = potential_blooms * 2
	var slag_weight = potential_blooms * 1.5 # Silicate impurities to hammer out
	
	return {
		"blooms_produced": potential_blooms,
		"ore_consumed": ore_consumed,
		"charcoal_consumed": fuel_consumed,
		"remaining_ore": ore_count - ore_consumed,
		"remaining_charcoal": charcoal_count - fuel_consumed,
		"slag_byproduct": slag_weight,
		"min_reduction_temp": MIN_SMELT_TEMP
	}

static func calculate_slag_ratio(ore_type: String) -> float:
	## Richer ores have less silicate slag
	match ore_type:
		"magnetite":
			return 0.15
		"hematite":
			return 0.25
		"limonite":
			return 0.35
		"crushed_iron":
			return 0.12 # Crushed with trip hammer removes loose gangue rock
		_:
			return 0.25
