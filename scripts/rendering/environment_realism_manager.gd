# scripts/rendering/environment_realism_manager.gd
# Voxel Lord: Feudal Realm - Milestone 31: Atmospheric Realism & Dynamic Environment
# Manages Kelvin color temperature progression, Rayleigh/Mie atmospheric fog,
# and surface shader uniforms for rain puddle wetness and snow accumulation.

class_name EnvironmentRealismManager
extends RefCounted

signal weather_changed(new_weather: String, fog_density: float)
signal sun_temperature_updated(kelvin: float, light_color: Color)
signal surface_state_updated(rain_wetness: float, snow_accumulation: float)

enum WeatherState { CLEAR, MIST, RAIN, BLIZZARD }

const WEATHER_FOG_PROFILES: Dictionary = {
	WeatherState.CLEAR: {"density": 0.005, "scattering": 0.15, "name": "clear"},
	WeatherState.MIST: {"density": 0.035, "scattering": 0.40, "name": "mist"},
	WeatherState.RAIN: {"density": 0.065, "scattering": 0.65, "name": "rain"},
	WeatherState.BLIZZARD: {"density": 0.120, "scattering": 0.85, "name": "blizzard"}
}

var current_weather: WeatherState = WeatherState.CLEAR
var current_sun_kelvin: float = 6500.0
var current_sun_color: Color = Color(1.0, 0.98, 0.95)

var rain_wetness: float = 0.0 # [0.0, 1.0] sent to voxel_pbr_triplanar.gdshader
var snow_accumulation: float = 0.0 # [0.0, 1.0] sent to voxel_pbr_triplanar.gdshader

func set_time_of_day(hour: float) -> void:
	# 24-hour cycle: 6.0 = dawn (3200K), 12.0 = noon (6500K), 18.0 = sunset (2600K), 24.0/0.0 = night (12000K)
	var normalized_hour = fmod(hour, 24.0)
	if normalized_hour < 0.0:
		normalized_hour += 24.0

	var target_kelvin: float = 6500.0
	if normalized_hour >= 5.0 and normalized_hour < 7.0:
		# Dawn transition: 12000K -> 3200K -> 5000K
		var t = (normalized_hour - 5.0) / 2.0
		target_kelvin = lerp(4000.0, 5500.0, t)
	elif normalized_hour >= 7.0 and normalized_hour < 16.0:
		# Daylight: peaks at 6500K midday
		var t = 1.0 - abs(normalized_hour - 11.5) / 4.5
		target_kelvin = lerp(5500.0, 6500.0, clamp(t, 0.0, 1.0))
	elif normalized_hour >= 16.0 and normalized_hour < 19.5:
		# Golden hour & Sunset: 5500K down to 2600K warm glow
		var t = (normalized_hour - 16.0) / 3.5
		target_kelvin = lerp(5500.0, 2600.0, t)
	else:
		# Night: 12000K cool starlight/moonlight
		target_kelvin = 12000.0

	current_sun_kelvin = target_kelvin
	current_sun_color = kelvin_to_rgb(current_sun_kelvin)
	sun_temperature_updated.emit(current_sun_kelvin, current_sun_color)

func set_weather(weather: WeatherState) -> void:
	current_weather = weather
	var profile = WEATHER_FOG_PROFILES.get(weather, WEATHER_FOG_PROFILES[WeatherState.CLEAR])
	weather_changed.emit(profile["name"], profile["density"])

func update_surface_states(delta_seconds: float, ambient_temp_celsius: float) -> void:
	match current_weather:
		WeatherState.RAIN:
			# Wetness builds up, snow melts if above freezing
			rain_wetness = min(1.0, rain_wetness + 0.05 * delta_seconds)
			if ambient_temp_celsius > 0.0:
				snow_accumulation = max(0.0, snow_accumulation - 0.04 * delta_seconds)
		WeatherState.BLIZZARD:
			# Snow accumulates rapidly in sub-zero blizzard
			if ambient_temp_celsius <= 0.0:
				snow_accumulation = min(1.0, snow_accumulation + 0.03 * delta_seconds)
			rain_wetness = max(0.0, rain_wetness - 0.02 * delta_seconds)
		WeatherState.CLEAR:
			# Drying out and melting
			rain_wetness = max(0.0, rain_wetness - 0.02 * delta_seconds)
			if ambient_temp_celsius > 0.0:
				snow_accumulation = max(0.0, snow_accumulation - 0.01 * delta_seconds)
		WeatherState.MIST:
			# Moderate mist maintains slight dampness
			rain_wetness = clamp(rain_wetness, 0.15, 0.4)

	surface_state_updated.emit(rain_wetness, snow_accumulation)

func kelvin_to_rgb(k: float) -> Color:
	# Standard Tanner Helland algorithm for blackbody / color temperature approximation
	var temp = clamp(k, 1000.0, 40000.0) / 100.0
	var red: float
	var green: float
	var blue: float

	# Red
	if temp <= 66.0:
		red = 255.0
	else:
		red = temp - 60.0
		red = 329.698727446 * pow(red, -0.1332047592)
		red = clamp(red, 0.0, 255.0)

	# Green
	if temp <= 66.0:
		green = temp
		green = 99.4708025861 * log(green) - 161.1195681661
		green = clamp(green, 0.0, 255.0)
	else:
		green = temp - 60.0
		green = 288.1221695283 * pow(green, -0.0755148492)
		green = clamp(green, 0.0, 255.0)

	# Blue
	if temp >= 66.0:
		blue = 255.0
	elif temp <= 19.0:
		blue = 0.0
	else:
		blue = temp - 10.0
		blue = 138.5177312231 * log(blue) - 305.0447927307
		blue = clamp(blue, 0.0, 255.0)

	return Color(red / 255.0, green / 255.0, blue / 255.0)
