class_name SeasonManager
extends Node

## Season & Weather Simulation Engine.
## Controls 4-season progression (Spring, Summer, Autumn, Winter),
## dynamic temperature calculation, precipitation (Rain/Snow), and environmental impacts.

signal season_changed(old_season: Season, new_season: Season)
signal weather_changed(new_weather: Weather)
signal temperature_changed(temp_celsius: float)
signal precipitation_tick(weather_type: Weather)

enum Season {
	SPRING = 0,
	SUMMER = 1,
	AUTUMN = 2,
	WINTER = 3
}

enum Weather {
	CLEAR = 0,
	RAIN = 1,
	SNOW = 2,
	THUNDERSTORM = 3
}

# Configuration
var season_duration: float = 120.0 # 2 minutes per season (8 minute full year)
var current_season: Season = Season.SPRING
var current_weather: Weather = Weather.CLEAR
var current_temperature: float = 16.0 # Celsius

var season_timer: float = 0.0
var weather_timer: float = 0.0
var weather_duration: float = 45.0 # Seconds per weather state

# References
var agriculture_manager: AgricultureManager
var sun_light: DirectionalLight3D

# Base temperatures per season (°C)
const SEASON_BASE_TEMPS: Dictionary = {
	Season.SPRING: 16.0,
	Season.SUMMER: 28.0,
	Season.AUTUMN: 11.0,
	Season.WINTER: -6.0
}

func _init(p_agri: AgricultureManager = null) -> void:
	agriculture_manager = p_agri

func _ready() -> void:
	_calculate_temperature(0.5)

func _process(delta: float) -> void:
	_tick_season(delta)
	_tick_weather(delta)

func _tick_season(delta: float) -> void:
	season_timer += delta
	if season_timer >= season_duration:
		season_timer = 0.0
		var old = current_season
		current_season = ((int(current_season) + 1) % 4) as Season
		emit_signal("season_changed", old, current_season)
		_pick_seasonal_weather()

func _tick_weather(delta: float) -> void:
	weather_timer += delta
	if weather_timer >= weather_duration:
		weather_timer = 0.0
		_pick_seasonal_weather()
		
	# Apply precipitation effects periodically
	if current_weather == Weather.RAIN or current_weather == Weather.THUNDERSTORM:
		_apply_rain_hydration()
		emit_signal("precipitation_tick", current_weather)
	elif current_weather == Weather.SNOW:
		emit_signal("precipitation_tick", current_weather)

func _pick_seasonal_weather() -> void:
	var roll = randf()
	var new_weather = Weather.CLEAR
	
	match current_season:
		Season.SPRING:
			if roll < 0.45: new_weather = Weather.RAIN
			elif roll < 0.60: new_weather = Weather.THUNDERSTORM
			else: new_weather = Weather.CLEAR
		Season.SUMMER:
			if roll < 0.20: new_weather = Weather.THUNDERSTORM
			else: new_weather = Weather.CLEAR
		Season.AUTUMN:
			if roll < 0.50: new_weather = Weather.RAIN
			else: new_weather = Weather.CLEAR
		Season.WINTER:
			if roll < 0.65: new_weather = Weather.SNOW
			else: new_weather = Weather.CLEAR
			
	if new_weather != current_weather:
		current_weather = new_weather
		emit_signal("weather_changed", current_weather)

func calculate_current_temperature(day_progress: float = 0.5) -> float:
	var base = SEASON_BASE_TEMPS.get(current_season, 15.0)
	
	# Diurnal variation: -5°C at night, +5°C at midday
	var diurnal = sin((day_progress - 0.25) * TAU) * 5.0
	
	# Weather impact
	var weather_mod = 0.0
	match current_weather:
		Weather.RAIN: weather_mod = -4.0
		Weather.THUNDERSTORM: weather_mod = -6.0
		Weather.SNOW: weather_mod = -8.0
		
	current_temperature = base + diurnal + weather_mod
	emit_signal("temperature_changed", current_temperature)
	return current_temperature

func _calculate_temperature(day_progress: float) -> void:
	calculate_current_temperature(day_progress)

func _apply_rain_hydration() -> void:
	if not agriculture_manager:
		return
	# Rain hydrates all active crops in the realm
	for pos in agriculture_manager.active_crops.keys():
		agriculture_manager.active_crops[pos]["hydrated"] = true

func get_season_name(s: Season = current_season) -> String:
	match s:
		Season.SPRING: return "Spring"
		Season.SUMMER: return "Summer"
		Season.AUTUMN: return "Autumn"
		Season.WINTER: return "Winter"
		_: return "Spring"

func get_weather_name(w: Weather = current_weather) -> String:
	match w:
		Weather.CLEAR: return "Clear"
		Weather.RAIN: return "Gentle Rain"
		Weather.SNOW: return "Heavy Snowfall"
		Weather.THUNDERSTORM: return "Thunderstorm"
		_: return "Clear"
