# scripts/mechanisms/astronomical_clock.gd
class_name AstronomicalClock
extends RefCounted

## Prague-Style Astronomical Clock & Calendar Simulation Mechanism
## Implements GDD Section 3 (Astronomical Time & Calendar), Section 70 (Blood Moon Cataclysm),
## and Section 87 (Seasonal Feasts & Astronomical Events).
## Driven by mechanical verge-and-foliot escapement with kinetic wind assist.

signal hour_chime(hour_num: int, total_strikes: int)
signal blood_moon_warning(hours_remaining: float)
signal season_changed(new_season: int, season_name: String)
signal day_passed(new_day: int, total_days_elapsed: int)

enum Season {
	SPRING = 0,
	SUMMER = 1,
	AUTUMN = 2,
	WINTER = 3
}

const SEASON_NAMES: Array[String] = ["Spring", "Summer", "Autumn", "Winter"]
const DAYS_PER_SEASON: int = 7
const DAYS_PER_YEAR: int = 28 # 4 seasons * 7 days (GDD Section 3.2 & 38.1)
const MINUTES_PER_HOUR: int = 60
const HOURS_PER_DAY: int = 24
const BLOOD_MOON_DAY: int = 28 # Cataclysm on the 28th day night (GDD Section 70)

# Time registers
var minute: int = 0
var hour: int = 6 # Starts at sunrise (06:00)
var day: int = 1  # 1..28
var season: Season = Season.SPRING
var year: int = 1
var total_days_elapsed: int = 1

# Kinetic & escapement drive
var gravity_counterweight_pct: float = 100.0 # 0.0 to 100.0%
var kinetic_connected: bool = false
var input_power_su: float = 0.0
var input_rpm: float = 0.0
const REQUIRED_SU: float = 16.0
const MIN_RPM: float = 16.0

# Blood Moon & Event states
var blood_moon_warning_active: bool = false
var is_blood_moon_tonight: bool = false
var last_chime_hour: int = -1

# Astrolabe coordinates
var solar_hour_angle_deg: float = 0.0
var solar_declination_deg: float = 0.0
var lunar_phase: float = 0.0 # 0.0 (New Moon) to 1.0 (Cycle Complete, 0.5 = Full Moon)

func _init(start_hour: int = 6, start_day: int = 1) -> void:
	hour = clampi(start_hour, 0, 23)
	day = clampi(start_day, 1, DAYS_PER_YEAR)
	_update_season()
	_update_celestial_coords()

func connect_kinetic_power(power_su: float, rpm: float) -> void:
	input_power_su = power_su
	input_rpm = absf(rpm)
	kinetic_connected = (input_power_su >= REQUIRED_SU and input_rpm >= MIN_RPM)
	if kinetic_connected:
		gravity_counterweight_pct = 100.0 # Kinetic drive auto-winds weight

func disconnect_kinetic_power() -> void:
	input_power_su = 0.0
	input_rpm = 0.0
	kinetic_connected = false

func is_running() -> bool:
	return kinetic_connected or gravity_counterweight_pct > 0.0

## Advance astronomical clockwork by delta_real_seconds
## In Voxel Lord: 1.0 real second = 1.0 game minute (60x time scale, GDD Section 3.1)
func advance_time(delta_real_seconds: float) -> void:
	if delta_real_seconds <= 0.0:
		return
	
	if not is_running():
		return # Clock stopped due to lack of gravity weight descent or kinetic drive

	# Gravity counterweight depletion if not driven by continuous kinetic shaft
	if not kinetic_connected:
		# 100% capacity lasts 24 in-game hours = 1,440 game minutes (1,440 real seconds)
		gravity_counterweight_pct = maxf(0.0, gravity_counterweight_pct - (delta_real_seconds / 1440.0) * 100.0)

	var minutes_to_add: int = int(delta_real_seconds)
	if minutes_to_add < 1:
		minutes_to_add = 1 # Step at least 1 minute per tick call

	for _m in range(minutes_to_add):
		minute += 1
		if minute >= MINUTES_PER_HOUR:
			minute = 0
			_advance_hour()

	_update_celestial_coords()

func _advance_hour() -> void:
	hour += 1
	var strikes: int = hour if hour <= 12 else (hour - 12)
	if strikes == 0:
		strikes = 12
	last_chime_hour = hour
	hour_chime.emit(hour, strikes)

	if hour >= HOURS_PER_DAY:
		hour = 0
		_advance_day()

func _advance_day() -> void:
	day += 1
	total_days_elapsed += 1
	var old_season: Season = season

	if day > DAYS_PER_YEAR:
		day = 1
		year += 1

	_update_season()
	if season != old_season:
		season_changed.emit(season, get_season_name())

	day_passed.emit(day, total_days_elapsed)

	# Check Blood Moon warning (Day 27 at or after 20:00 -> warning active)
	_check_blood_moon_schedule()

func _update_season() -> void:
	# 28 days: Days 1-7 = Spring, 8-14 = Summer, 15-21 = Autumn, 22-28 = Winter
	var season_index: int = (day - 1) / DAYS_PER_SEASON
	season = Season.values()[clampi(season_index, 0, 3)]

func _check_blood_moon_schedule() -> void:
	# Blood Moon occurs on night of Day 28 (20:00 to 04:00 next day)
	is_blood_moon_tonight = (day == BLOOD_MOON_DAY and (hour >= 20 or hour < 4))

	# Early warning alarm fires 24h prior: Day 27 at 20:00 onwards
	if day == (BLOOD_MOON_DAY - 1) and hour >= 20:
		blood_moon_warning_active = true
		var hours_until_blood_moon: float = float(24 - (hour - 20))
		blood_moon_warning.emit(hours_until_blood_moon)
	elif day == BLOOD_MOON_DAY:
		blood_moon_warning_active = true
	else:
		blood_moon_warning_active = false

func _update_celestial_coords() -> void:
	# Solar hour angle: 0 at noon (12:00), 180 at midnight (00:00), 15 deg per hour
	var time_in_hours: float = float(hour) + float(minute) / 60.0
	solar_hour_angle_deg = (time_in_hours - 12.0) * 15.0

	# Solar declination based on 28-day year cycle:
	# Spring Equinox (Day 1): 0 deg, Summer Solstice (Day 8): +23.4 deg,
	# Autumn Equinox (Day 15): 0 deg, Winter Solstice (Day 22): -23.4 deg
	var year_fraction: float = float(day - 1 + (time_in_hours / 24.0)) / float(DAYS_PER_YEAR)
	solar_declination_deg = 23.44 * sin(year_fraction * 2.0 * PI)

	# Lunar phase: full 28-day lunar month synchronized with the feudal year
	# Day 1: New Moon (0.0), Day 14: Full Moon (0.5), Day 28: Blood Moon Eclipse (1.0 / 0.0)
	lunar_phase = year_fraction

func get_season_name() -> String:
	return SEASON_NAMES[season]

func get_time_string() -> String:
	return "%02d:%02d, Day %d (%s), Year %d" % [hour, minute, day, get_season_name(), year]

func rewound_gravity_weights() -> void:
	gravity_counterweight_pct = 100.0

func get_days_until_blood_moon() -> int:
	if day <= BLOOD_MOON_DAY:
		return BLOOD_MOON_DAY - day
	return DAYS_PER_YEAR - day + BLOOD_MOON_DAY
