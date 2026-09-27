# scripts/mechanisms/celestial_orrery.gd
class_name CelestialOrrery
extends RefCounted

## Kinetic Clockwork Celestial Orrery & Astrological Resonance Engine
## Precision brass epicyclic gear train planetarium driven by kinetic power.
## Models celestial orbital mechanics, calculates planetary alignments/conjunctions,
## and radiates kingdom-wide astrological resonance bonuses.
## Implements MASTER_GDD Section 3, Section 87 (Grand Feasts) & Create Mod kinetic interop.

signal war_conjunction_state_changed(is_active: bool)
signal artisan_conjunction_state_changed(is_active: bool)
signal grand_conjunction_triggered()

const REQUIRED_POWER_SU: float = 16.0
const MIN_SPEED_RPM: float = 16.0
const CONJUNCTION_TOLERANCE_DEG: float = 15.0 # Max angular separation for conjunction
const GRAND_CONJUNCTION_ARC_DEG: float = 35.0 # Max arc containing all planets

# Kinetic drive status
var is_active: bool = false
var input_power_su: float = 0.0
var input_rpm: float = 0.0

# Planetary orbital angles in degrees [0.0, 360.0)
var pos_mercury_deg: float = 40.0
var pos_venus_deg: float = 130.0
var pos_earth_deg: float = 220.0
var pos_moon_deg: float = 45.0 # Relative to Earth
var pos_mars_deg: float = 310.0
var pos_saturn_deg: float = 75.0

# Orbital velocity rates per in-game day (degrees / game day)
# In Voxel Lord: 1 game day = 1,440 game minutes = 1,440 real seconds
const VEL_MERCURY_DEG_PER_DAY: float = 150.0
const VEL_VENUS_DEG_PER_DAY: float = 58.0
const VEL_EARTH_DEG_PER_DAY: float = 12.85714 # 360 deg / 28 days
const VEL_MOON_DEG_PER_DAY: float = 51.42857  # 360 deg / 7 days (lunar month)
const VEL_MARS_DEG_PER_DAY: float = 6.8433
const VEL_SATURN_DEG_PER_DAY: float = 0.4363

# Active resonance states
var war_conjunction_active: bool = false       # Earth-Mars alignment
var artisan_conjunction_active: bool = false   # Earth-Venus alignment
var grand_conjunction_active: bool = false     # All 5 planets aligned
var total_grand_conjunctions: int = 0

## Advance the kinetic orrery gear train by delta_seconds
## 1.0 real second = 1.0 game minute = 1/1440 of a game day
func update_kinetic(delta_seconds: float, power_su: float, rpm: float) -> void:
	input_power_su = power_su
	input_rpm = absf(rpm)
	is_active = (input_power_su >= REQUIRED_POWER_SU and input_rpm >= MIN_SPEED_RPM)

	if not is_active or delta_seconds <= 0.0:
		return

	# Speed multiplier based on input RPM (nominal at 32 RPM)
	var speed_mult: float = input_rpm / 32.0
	var day_fraction: float = (delta_seconds / 1440.0) * speed_mult

	# Update planet angles
	pos_mercury_deg = fmod(pos_mercury_deg + VEL_MERCURY_DEG_PER_DAY * day_fraction, 360.0)
	pos_venus_deg = fmod(pos_venus_deg + VEL_VENUS_DEG_PER_DAY * day_fraction, 360.0)
	pos_earth_deg = fmod(pos_earth_deg + VEL_EARTH_DEG_PER_DAY * day_fraction, 360.0)
	pos_moon_deg = fmod(pos_moon_deg + VEL_MOON_DEG_PER_DAY * day_fraction, 360.0)
	pos_mars_deg = fmod(pos_mars_deg + VEL_MARS_DEG_PER_DAY * day_fraction, 360.0)
	pos_saturn_deg = fmod(pos_saturn_deg + VEL_SATURN_DEG_PER_DAY * day_fraction, 360.0)

	_evaluate_astrological_conjunctions()

## Calculate angular difference between two angles in [0, 360)
func _angular_distance(a: float, b: float) -> float:
	var diff: float = absf(a - b)
	if diff > 180.0:
		diff = 360.0 - diff
	return diff

func _evaluate_astrological_conjunctions() -> void:
	# 1. War Conjunction: Earth & Mars
	var dist_mars: float = _angular_distance(pos_earth_deg, pos_mars_deg)
	var new_war_state: bool = (dist_mars <= CONJUNCTION_TOLERANCE_DEG)
	if new_war_state != war_conjunction_active:
		war_conjunction_active = new_war_state
		war_conjunction_state_changed.emit(war_conjunction_active)

	# 2. Artisan Conjunction: Earth & Venus
	var dist_venus: float = _angular_distance(pos_earth_deg, pos_venus_deg)
	var new_artisan_state: bool = (dist_venus <= CONJUNCTION_TOLERANCE_DEG)
	if new_artisan_state != artisan_conjunction_active:
		artisan_conjunction_active = new_artisan_state
		artisan_conjunction_state_changed.emit(artisan_conjunction_active)

	# 3. Grand Conjunction: All 5 planets within a narrow arc
	var angles: Array[float] = [pos_mercury_deg, pos_venus_deg, pos_earth_deg, pos_mars_deg, pos_saturn_deg]
	angles.sort()
	var min_arc: float = 360.0
	for i in range(angles.size()):
		var arc: float = 0.0
		if i == 0:
			arc = angles[angles.size() - 1] - angles[0]
		else:
			arc = 360.0 - (angles[i] - angles[i - 1])
		min_arc = minf(min_arc, arc)

	var new_grand_state: bool = (min_arc <= GRAND_CONJUNCTION_ARC_DEG)
	if new_grand_state and not grand_conjunction_active:
		grand_conjunction_active = true
		total_grand_conjunctions += 1
		grand_conjunction_triggered.emit()
	elif not new_grand_state:
		grand_conjunction_active = false

## Returns active kingdom buff modifiers
func get_kingdom_resonance_buffs() -> Dictionary:
	var buffs: Dictionary = {
		"combat_morale_bonus": 0.0,
		"foundry_smelt_yield_bonus": 0.0,
		"citizen_happiness_bonus": 0.0,
		"artisan_craft_speed_bonus": 0.0,
		"kingdom_production_bonus": 0.0,
		"harvest_yield_multiplier": 1.0
	}

	if war_conjunction_active:
		buffs["combat_morale_bonus"] = 0.20 # +20% army morale
		buffs["foundry_smelt_yield_bonus"] = 0.25 # +25% iron/steel blast yield

	if artisan_conjunction_active:
		buffs["citizen_happiness_bonus"] = 0.25 # +25% happiness
		buffs["artisan_craft_speed_bonus"] = 0.30 # +30% luxury & lapidary speed

	if grand_conjunction_active:
		buffs["kingdom_production_bonus"] = 0.50 # +50% all production
		buffs["harvest_yield_multiplier"] = 2.0  # Double harvest yield
		buffs["citizen_happiness_bonus"] += 0.15

	return buffs
