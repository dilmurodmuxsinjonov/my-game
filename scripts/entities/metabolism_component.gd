class_name MetabolismComponent
extends Node

## Manages citizen caloric expenditure, 3-pillar macronutrient tracking,
## thermoregulation, and deficiency disease pathogenesis (Scurvy, Fatigue, Hypothermia).
## Aligns with MASTER_GDD.md §§18, 40, 41, 68 and Project Interface Contracts.

signal deficiency_disease_triggered(disease_name: String, stage: int)
signal deficiency_disease_cured(disease_name: String)
signal citizen_collapsed(reason: String)
signal caloric_depleted()
signal hypothermia_stage_changed(stage: int)

@export var citizen: CharacterBody3D

# --- Caloric Energy Reserve ---
var max_calories: float = 15000.0        # Saturation ceiling (adipose reserves)
var current_calories: float = 2400.0     # Nominal 1-day baseline (kcal)
const BMR_HOURLY: float = 75.0           # 1,800 kcal / 24 hours = 75 kcal/hr
const BMR_PER_SECOND: float = 1800.0 / 86400.0 # ~0.020833 kcal/sec
const STARVATION_DAMAGE_HOURLY: float = 2.5 # HP lost per hour at 0 calories

# --- 3 Nutritional Pillars (0.0% to 100.0%) ---
var carbs: float = 80.0
var protein: float = 80.0
var vitamins: float = 80.0

const HALF_LIFE_CARBS_HOURS: float = 18.0    # 18 game hours
const HALF_LIFE_PROTEIN_HOURS: float = 72.0  # 72 game hours (3 days)
const HALF_LIFE_VITAMIN_HOURS: float = 120.0 # 120 game hours (5 days)

# Real-time frame half-lives (assuming 60s per game hour)
const HALF_LIFE_CARBS_SEC: float = 18.0 * 60.0
const HALF_LIFE_PROTEIN_SEC: float = 72.0 * 60.0
const HALF_LIFE_VITAMIN_SEC: float = 120.0 * 60.0

# --- Disease & Deficiency States ---
# Scurvy (Singa) stages: 0 = healthy, 1 = lethargy/no healing, 2 = spontaneous bleeding, 3 = fatal hemorrhage
var scurvy_stage: int = 0
var scurvy_timer_sec: float = 0.0          # Elapsed time with vitamins < 15%
var scurvy_timer_hours: float = 0.0

# Fatigue (Glycogen exhaustion)
var is_fatigued: bool = false
var stamina_recovery_mult: float = 1.0
var work_speed_mult: float = 1.0
var move_speed_mult: float = 1.0

# Hypothermia & Thermoregulation
var body_temperature: float = 37.0         # Core body temperature in Celsius
var hypothermia_stage: int = 0             # 0: Normal, 1: Chilled, 2: Moderate, 3: Severe/Coma
var clothing_clo: float = 1.0              # Clo value (1.0 = standard woolens)
var wetness: float = 0.0                   # Surface wetness [0.0, 1.0]

# Nutritional Catalog (Master Balance Table)
const FOOD_NUTRITION_CATALOG: Dictionary = {
	"food_bread":          {"calories": 320.0, "carbs": 45.0, "protein": 6.0,  "vitamins": 0.0},
	"bread":               {"calories": 320.0, "carbs": 45.0, "protein": 6.0,  "vitamins": 0.0},
	"food_grain_porridge": {"calories": 280.0, "carbs": 40.0, "protein": 8.0,  "vitamins": 2.0},
	"porridge":            {"calories": 280.0, "carbs": 40.0, "protein": 8.0,  "vitamins": 2.0},
	"food_meat_raw":       {"calories": 240.0, "carbs": 0.0,  "protein": 35.0, "vitamins": 1.0},
	"fresh_meat":          {"calories": 240.0, "carbs": 0.0,  "protein": 35.0, "vitamins": 1.0},
	"food_roast_meat":     {"calories": 380.0, "carbs": 0.0,  "protein": 48.0, "vitamins": 2.0},
	"roast_meat":          {"calories": 380.0, "carbs": 0.0,  "protein": 48.0, "vitamins": 2.0},
	"food_fish_stew":      {"calories": 340.0, "carbs": 15.0, "protein": 36.0, "vitamins": 8.0},
	"vegetable_broth":     {"calories": 160.0, "carbs": 20.0, "protein": 4.0,  "vitamins": 25.0},
	"hearty_stew":         {"calories": 360.0, "carbs": 25.0, "protein": 38.0, "vitamins": 12.0},
	"food_cheese":         {"calories": 410.0, "carbs": 4.0,  "protein": 32.0, "vitamins": 6.0},
	"cheese":              {"calories": 410.0, "carbs": 4.0,  "protein": 32.0, "vitamins": 6.0},
	"food_peas_boiled":    {"calories": 310.0, "carbs": 28.0, "protein": 24.0, "vitamins": 14.0},
	"food_cabbage_raw":    {"calories": 60.0,  "carbs": 8.0,  "protein": 2.0,  "vitamins": 40.0},
	"cabbage":             {"calories": 60.0,  "carbs": 8.0,  "protein": 2.0,  "vitamins": 40.0},
	"food_carrot_raw":     {"calories": 75.0,  "carbs": 12.0, "protein": 1.5,  "vitamins": 35.0},
	"carrot":              {"calories": 75.0,  "carbs": 12.0, "protein": 1.5,  "vitamins": 35.0},
	"food_berries_fresh":  {"calories": 90.0,  "carbs": 16.0, "protein": 1.0,  "vitamins": 55.0},
	"berries":             {"calories": 90.0,  "carbs": 16.0, "protein": 1.0,  "vitamins": 55.0},
	"food_pickled_veg":    {"calories": 85.0,  "carbs": 10.0, "protein": 2.0,  "vitamins": 65.0},
	"pickled_veg":         {"calories": 85.0,  "carbs": 10.0, "protein": 2.0,  "vitamins": 65.0},
	"food_smoked_meat":    {"calories": 420.0, "carbs": 0.0,  "protein": 52.0, "vitamins": 0.0},
	"smoked_meat":         {"calories": 420.0, "carbs": 0.0,  "protein": 52.0, "vitamins": 0.0},
	"food_salted_meat":    {"calories": 390.0, "carbs": 0.0,  "protein": 50.0, "vitamins": 0.0},
	"cured_meat":          {"calories": 390.0, "carbs": 0.0,  "protein": 50.0, "vitamins": 0.0}
}

func _ready() -> void:
	if not citizen and get_parent() is CharacterBody3D:
		citizen = get_parent()

func _process(delta: float) -> void:
	_tick_caloric_expenditure_realtime(delta)
	_tick_macronutrient_decay_realtime(delta)
	_tick_thermoregulation_realtime(delta)
	_evaluate_diseases_realtime(delta)

# --- Real-Time Process Ticks ---

func _tick_caloric_expenditure_realtime(delta: float) -> void:
	var state_code = 0
	if citizen:
		state_code = int(citizen.get("current_state"))
	var activity_mult = get_activity_multiplier(state_code)
	
	# Shivering thermogenesis
	var shivering_burn_hourly = calculate_shivering_burn_hourly(body_temperature)
	var shivering_burn_sec = shivering_burn_hourly / 3600.0
	
	var total_burn_sec = BMR_PER_SECOND * activity_mult + shivering_burn_sec
	var total_burn = total_burn_sec * delta
	
	current_calories = maxf(0.0, current_calories - total_burn)
	
	if current_calories <= 0.0:
		emit_signal("caloric_depleted")
		if citizen and citizen.has_method("take_damage"):
			citizen.take_damage(STARVATION_DAMAGE_HOURLY * (delta / 3600.0))

func _tick_macronutrient_decay_realtime(delta: float) -> void:
	# First-order exponential decay
	carbs = maxf(0.0, carbs - (0.693147 / HALF_LIFE_CARBS_SEC) * carbs * delta)
	protein = maxf(0.0, protein - (0.693147 / HALF_LIFE_PROTEIN_SEC) * protein * delta)
	vitamins = maxf(0.0, vitamins - (0.693147 / HALF_LIFE_VITAMIN_SEC) * vitamins * delta)

func _tick_thermoregulation_realtime(delta: float) -> void:
	var ambient_temp = 16.0
	if is_inside_tree() and get_tree().root:
		var season_mgr = get_tree().root.find_child("SeasonManager", true, false)
		if season_mgr and "current_temperature" in season_mgr:
			ambient_temp = float(season_mgr.current_temperature)
	
	var effective_clo = maxf(0.1, clothing_clo * (1.0 - 0.75 * wetness))
	var thermal_inertia = 2700.0 # 45 minutes time constant
	var temp_diff = ambient_temp - body_temperature
	body_temperature += (temp_diff / thermal_inertia) * (1.0 / effective_clo) * delta
	body_temperature = clampf(body_temperature, 20.0, 42.0)
	
	_update_hypothermia_stage(delta / 3600.0)

func _evaluate_diseases_realtime(delta: float) -> void:
	# Scurvy progression
	if vitamins < 15.0:
		scurvy_timer_sec += delta
		var days_deficient = scurvy_timer_sec / 1440.0 # 1 game day = 1440s (24m)
		if days_deficient >= 7.0 and scurvy_stage < 3:
			scurvy_stage = 3
			emit_signal("deficiency_disease_triggered", "Scurvy", 3)
		elif days_deficient >= 5.0 and scurvy_stage < 2:
			scurvy_stage = 2
			emit_signal("deficiency_disease_triggered", "Scurvy", 2)
		elif days_deficient >= 3.0 and scurvy_stage < 1:
			scurvy_stage = 1
			emit_signal("deficiency_disease_triggered", "Scurvy", 1)
	else:
		if scurvy_stage > 0:
			scurvy_stage = 0
			scurvy_timer_sec = 0.0
			scurvy_timer_hours = 0.0
			emit_signal("deficiency_disease_cured", "Scurvy")

	# Scurvy symptoms application
	if scurvy_stage == 2 and citizen and citizen.has_method("take_damage"):
		citizen.take_damage(0.5 * (delta / 3600.0))
	elif scurvy_stage == 3 and citizen and citizen.has_method("take_damage"):
		citizen.take_damage(2.5 * (delta / 3600.0))
		if "max_health" in citizen:
			citizen.max_health = minf(citizen.max_health, 25.0)

	# Fatigue & Glycogen Exhaustion
	if carbs < 10.0 and not is_fatigued:
		is_fatigued = true
		work_speed_mult = 0.50
		move_speed_mult = 0.60
		stamina_recovery_mult = 0.50
		emit_signal("citizen_collapsed", "Carbohydrate Exhaustion")
	elif carbs >= 25.0 and is_fatigued:
		is_fatigued = false
		work_speed_mult = 1.0
		move_speed_mult = 1.0
		stamina_recovery_mult = 1.0

# --- Interface Contract Method (PROJECT.md M3) ---

## Computes TEE = BMR * ActivityMult + ShiveringBurn; decays carbs, proteins, vitamins;
## returns updated health, stamina, and deficiency disease metrics.
func tick_metabolism(delta_hours: float, activity_state: int = 0, ambient_temp: float = 16.0) -> Dictionary:
	var activity_mult = get_activity_multiplier(activity_state)
	var shivering_burn_hourly = calculate_shivering_burn_hourly(body_temperature)
	var tee_hourly = (BMR_HOURLY * activity_mult) + shivering_burn_hourly
	var total_calories_spent = tee_hourly * delta_hours
	
	current_calories = maxf(0.0, current_calories - total_calories_spent)
	
	var damage_taken = 0.0
	if current_calories <= 0.0:
		emit_signal("caloric_depleted")
		damage_taken += STARVATION_DAMAGE_HOURLY * delta_hours

	# First-order exponential decay across hours
	carbs = maxf(0.0, carbs * pow(0.5, delta_hours / HALF_LIFE_CARBS_HOURS))
	protein = maxf(0.0, protein * pow(0.5, delta_hours / HALF_LIFE_PROTEIN_HOURS))
	vitamins = maxf(0.0, vitamins * pow(0.5, delta_hours / HALF_LIFE_VITAMIN_HOURS))

	# Thermoregulation across delta_hours
	var effective_clo = maxf(0.1, clothing_clo * (1.0 - 0.75 * wetness))
	var thermal_inertia_hours = 0.75 # 45 minutes
	var temp_diff = ambient_temp - body_temperature
	body_temperature += (temp_diff / thermal_inertia_hours) * (1.0 / effective_clo) * delta_hours
	body_temperature = clampf(body_temperature, 20.0, 42.0)
	
	_update_hypothermia_stage(delta_hours)
	
	if hypothermia_stage == 3:
		# Fatal freezing damage (15 HP per 10s = 5400 HP/hr)
		damage_taken += 5400.0 * delta_hours

	# Scurvy progression
	if vitamins < 15.0:
		scurvy_timer_hours += delta_hours
		var days_deficient = scurvy_timer_hours / 24.0
		if days_deficient >= 7.0 and scurvy_stage < 3:
			scurvy_stage = 3
			emit_signal("deficiency_disease_triggered", "Scurvy", 3)
		elif days_deficient >= 5.0 and scurvy_stage < 2:
			scurvy_stage = 2
			emit_signal("deficiency_disease_triggered", "Scurvy", 2)
		elif days_deficient >= 3.0 and scurvy_stage < 1:
			scurvy_stage = 1
			emit_signal("deficiency_disease_triggered", "Scurvy", 1)
	else:
		if scurvy_stage > 0:
			scurvy_stage = 0
			scurvy_timer_hours = 0.0
			scurvy_timer_sec = 0.0
			emit_signal("deficiency_disease_cured", "Scurvy")

	if scurvy_stage == 2:
		damage_taken += 0.5 * delta_hours
	elif scurvy_stage == 3:
		damage_taken += 2.5 * delta_hours

	# Fatigue check
	if carbs < 10.0 and not is_fatigued:
		is_fatigued = true
		work_speed_mult = 0.50
		move_speed_mult = 0.60
		stamina_recovery_mult = 0.50
		emit_signal("citizen_collapsed", "Carbohydrate Exhaustion")
	elif carbs >= 25.0 and is_fatigued:
		is_fatigued = false
		work_speed_mult = 1.0
		move_speed_mult = 1.0
		stamina_recovery_mult = 1.0

	if citizen and citizen.has_method("take_damage") and damage_taken > 0.0:
		citizen.take_damage(damage_taken)

	return {
		"current_calories": current_calories,
		"tee_hourly": tee_hourly,
		"carbs": carbs,
		"protein": protein,
		"vitamins": vitamins,
		"body_temperature": body_temperature,
		"scurvy_stage": scurvy_stage,
		"is_fatigued": is_fatigued,
		"hypothermia_stage": hypothermia_stage,
		"damage_taken": damage_taken,
		"work_speed_mult": work_speed_mult,
		"move_speed_mult": move_speed_mult,
		"can_heal": can_heal()
	}

# --- Calculation Helpers ---

func get_activity_multiplier(state_code: int) -> float:
	match state_code:
		7: # SLEEP
			return 0.60
		0, 1: # IDLE, WANDER / REST / SOCIALIZE
			return 1.00
		2, 8, 12: # MOVING_TO_WORK, HAULING
			return 1.50
		3, 4, 11: # WORKING, HARVESTING, BUILDING
			return 2.20
		9, 10: # FLEEING, DEFENDING / SPRINT / COMBAT
			return 3.80
		_:
			return 1.00

func calculate_shivering_burn_hourly(temp: float) -> float:
	if temp < 36.5:
		return clampf((36.5 - temp) / 4.5, 0.0, 1.0) * 120.0
	return 0.0

func _update_hypothermia_stage(delta_hours: float) -> void:
	var old_stage = hypothermia_stage
	if body_temperature >= 36.5:
		hypothermia_stage = 0
	elif body_temperature >= 35.0:
		hypothermia_stage = 1 # Chilled: shivering, +50% calorie burn
	elif body_temperature >= 32.0:
		hypothermia_stage = 2 # Moderate: shivering ceases, -35% speed, confusion
	else:
		hypothermia_stage = 3 # Severe/Coma: collapse, lethal hypothermia damage

	if hypothermia_stage != old_stage:
		emit_signal("hypothermia_stage_changed", hypothermia_stage)
		if hypothermia_stage == 3:
			emit_signal("citizen_collapsed", "Hypothermia Coma")

func can_heal() -> bool:
	return scurvy_stage == 0 and current_calories > 0.0 and hypothermia_stage < 2

func ingest_food(item_id: String, cal: float = -1.0, c: float = -1.0, p: float = -1.0, v: float = -1.0) -> void:
	var cal_to_add = cal
	var carbs_to_add = c
	var prot_to_add = p
	var vit_to_add = v
	
	if FOOD_NUTRITION_CATALOG.has(item_id):
		var profile = FOOD_NUTRITION_CATALOG[item_id]
		if cal_to_add < 0.0: cal_to_add = profile["calories"]
		if carbs_to_add < 0.0: carbs_to_add = profile["carbs"]
		if prot_to_add < 0.0: prot_to_add = profile["protein"]
		if vit_to_add < 0.0: vit_to_add = profile["vitamins"]
	else:
		# Default fallback meal
		if cal_to_add < 0.0: cal_to_add = 200.0
		if carbs_to_add < 0.0: carbs_to_add = 20.0
		if prot_to_add < 0.0: prot_to_add = 10.0
		if vit_to_add < 0.0: vit_to_add = 5.0
		
	current_calories = minf(max_calories, current_calories + cal_to_add)
	carbs = minf(100.0, carbs + carbs_to_add)
	protein = minf(100.0, protein + prot_to_add)
	vitamins = minf(100.0, vitamins + vit_to_add)

	# If vitamins restored >= 15%, clear scurvy timer
	if vitamins >= 15.0 and scurvy_stage > 0:
		scurvy_stage = 0
		scurvy_timer_sec = 0.0
		scurvy_timer_hours = 0.0
		emit_signal("deficiency_disease_cured", "Scurvy")

	if carbs >= 25.0 and is_fatigued:
		is_fatigued = false
		work_speed_mult = 1.0
		move_speed_mult = 1.0
		stamina_recovery_mult = 1.0
