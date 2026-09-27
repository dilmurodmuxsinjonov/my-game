# scripts/mechanisms/armillary_sphere.gd
class_name ArmillarySphere
extends RefCounted

## Pivoting Brass Armillary Sphere & Astrolabe Observatory
## Precision observational instrument for measuring celestial coordinates,
## compiling maritime navigational charts, and forecasting seasonal weather extremes.
## Bridges Milestone 38 (Maritime Commerce) and MASTER_GDD Sections 3, 38 & 110.

signal observation_completed(chart_data: Dictionary)
signal weather_forecast_updated(forecast_type: String, days_ahead: int, description: String)

const OBSERVER_LATITUDE_DEG: float = 52.0 # Temperate realm latitude (GDD Section 3.3)
const OBSERVATION_TIME_REQUIRED: float = 60.0 # 60 in-game minutes (real seconds) to map stars

# Operational state
var is_observing: bool = false
var observation_progress_sec: float = 0.0
var total_charts_compiled: int = 0
var observer_skill_level: float = 1.0 # 1.0 = apprentice, 2.0 = master royal astronomer

# Astronomical calculations
var last_solar_altitude_deg: float = 0.0
var last_solar_azimuth_deg: float = 0.0
var current_forecast: String = "FAIR_WEATHER"

func start_observation(skill_level: float = 1.0) -> bool:
	if is_observing:
		return false
	is_observing = true
	observer_skill_level = clampf(skill_level, 0.5, 3.0)
	return true

func cancel_observation() -> void:
	is_observing = false
	observation_progress_sec = 0.0

## Advance observation and celestial calculations
func update(delta_seconds: float, clock: AstronomicalClock) -> Dictionary:
	if clock != null:
		_calculate_solar_position(clock)
		_update_weather_forecast(clock)

	if is_observing:
		observation_progress_sec += delta_seconds * observer_skill_level
		if observation_progress_sec >= OBSERVATION_TIME_REQUIRED:
			is_observing = false
			observation_progress_sec = 0.0
			total_charts_compiled += 1
			var chart: Dictionary = _generate_celestial_chart()
			observation_completed.emit(chart)
			return chart

	return {}

## Solar Altitude Equation: sin(alpha) = sin(phi)*sin(delta) + cos(phi)*cos(delta)*cos(H)
func _calculate_solar_position(clock: AstronomicalClock) -> void:
	var phi_rad: float = deg_to_rad(OBSERVER_LATITUDE_DEG)
	var delta_rad: float = deg_to_rad(clock.solar_declination_deg)
	var h_rad: float = deg_to_rad(clock.solar_hour_angle_deg)

	var sin_alpha: float = sin(phi_rad) * sin(delta_rad) + cos(phi_rad) * cos(delta_rad) * cos(h_rad)
	sin_alpha = clampf(sin_alpha, -1.0, 1.0)
	last_solar_altitude_deg = rad_to_deg(asin(sin_alpha))

	# Azimuth calculation
	if cos(deg_to_rad(last_solar_altitude_deg)) != 0.0:
		var cos_az: float = (sin(delta_rad) - sin(phi_rad) * sin_alpha) / (cos(phi_rad) * cos(deg_to_rad(last_solar_altitude_deg)))
		cos_az = clampf(cos_az, -1.0, 1.0)
		var az_deg: float = rad_to_deg(acos(cos_az))
		if clock.solar_hour_angle_deg > 0.0:
			az_deg = 360.0 - az_deg
		last_solar_azimuth_deg = az_deg

## Forecast seasonal weather extremes 1 to 3 days ahead
func _update_weather_forecast(clock: AstronomicalClock) -> void:
	var old_forecast: String = current_forecast
	var day: int = clock.day
	var season: AstronomicalClock.Season = clock.season

	if season == AstronomicalClock.Season.AUTUMN and day >= 19:
		current_forecast = "HARD_FROST_WARNING"
		if old_forecast != current_forecast:
			weather_forecast_updated.emit(current_forecast, 22 - day, "Hard frost approaching; winter dormancy will freeze unheated crops.")
	elif season == AstronomicalClock.Season.SUMMER and day >= 10 and day <= 13:
		current_forecast = "DROUGHT_HEATWAVE_WARNING"
		if old_forecast != current_forecast:
			weather_forecast_updated.emit(current_forecast, 14 - day, "Intense solar radiation; well water consumption will surge by 50%.")
	elif season == AstronomicalClock.Season.SPRING and day <= 3:
		current_forecast = "MONSOONAL_SQUALL_WARNING"
		if old_forecast != current_forecast:
			weather_forecast_updated.emit(current_forecast, 4 - day, "Equinoctial sea squalls; unsheltered vessels risk damage without stellar charts.")
	else:
		current_forecast = "FAIR_WEATHER"

func _generate_celestial_chart() -> Dictionary:
	var quality_score: float = clampf(1.0 + (observer_skill_level - 1.0) * 0.25, 0.8, 2.0)
	return {
		"item_id": "celestial_chart",
		"item_name": "Stellar Navigational Chart",
		"quality": quality_score,
		"voyage_speed_bonus": 0.30 * quality_score, # +30% to +60% voyage speed
		"trade_profit_bonus": 0.50 * quality_score, # +50% to +100% market profits
		"storm_deviation_immunity": true,          # Zero course loss during maritime storms
		"uses_remaining": 5                        # Valid for 5 overseas expeditions
	}

## Applies a compiled celestial chart to a vessel (e.g. FluytCargoShip from Milestone 38)
func apply_chart_to_vessel(vessel_state: Dictionary, chart: Dictionary) -> Dictionary:
	if chart.is_empty() or not chart.has("voyage_speed_bonus"):
		return vessel_state

	var updated: Dictionary = vessel_state.duplicate()
	var base_duration: float = updated.get("voyage_duration_sec", 300.0)
	var speed_mult: float = 1.0 + float(chart.get("voyage_speed_bonus", 0.30))
	updated["voyage_duration_sec"] = base_duration / speed_mult
	updated["profit_multiplier"] = updated.get("profit_multiplier", 1.0) * (1.0 + float(chart.get("trade_profit_bonus", 0.50)))
	updated["storm_safe"] = bool(chart.get("storm_deviation_immunity", true))
	return updated
