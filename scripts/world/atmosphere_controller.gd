class_name AtmosphereController
extends Node

## AtmosphereController: Diurnal Lighting, Rayleigh Scattering, and Volumetric Fog
## Milestone 4 / R4: Photorealistic PBR Surfaces & Dynamic Atmosphere
##
## Controls:
## 1. Astronomical and diurnal solar elevation angle (theta_sun)
## 2. Diurnal volumetric fog density modulation and forward Mie scattering
## 3. Atmospheric Rayleigh scattering spectrum for direct sunlight and "God rays"
## 4. Integration with Godot 4.3 Environment and DirectionalLight3D

signal time_of_day_updated(diurnal_time: float, sun_elevation_deg: float)
signal phase_changed(phase_name: String)
signal atmosphere_updated(fog_density: float, sun_color: Color)

enum WeatherType {
	CLEAR = 0,
	RAIN = 1,
	SNOW = 2,
	THUNDERSTORM = 3,
	BLIZZARD = 4
}

enum DiurnalPhase {
	NIGHT = 0,
	DAWN = 1,
	MORNING = 2,
	NOON = 3,
	DUSK = 4
}

# =========================================================================
# Configuration & References
# =========================================================================
@export var world_environment: WorldEnvironment
@export var sun_light: DirectionalLight3D

## Normalized diurnal time in [0.0, 1.0)
## 0.00 = Midnight (00:00), 0.25 = Dawn (06:00), 0.50 = Solar Noon (12:00), 0.75 = Dusk (18:00)
@export_range(0.0, 1.0) var diurnal_time: float = 0.25

## Real seconds per full 24-hour in-game day (default 1440.0s = 24 real minutes)
@export var day_duration_seconds: float = 1440.0

## Geographic latitude (temperate feudal realm default 52.0° North)
@export var latitude_degrees: float = 52.0

## Solar declination angle (-23.44° winter to +23.44° summer; 0.0° equinox)
@export var solar_declination_degrees: float = 0.0

## Maximum peak solar elevation angle in degrees (default 62.0° summer peak)
@export var max_sun_elevation: float = 62.0

## Active weather condition affecting atmospheric density
@export var current_weather: WeatherType = WeatherType.CLEAR

## Whether diurnal time advances automatically in _process
@export var auto_advance: bool = true

## If true, uses rigorous astronomical latitude/declination formula;
## if false, uses smooth 0° to 62° sinusoidal elevation model matching GDD spec.
@export var use_astronomical_model: bool = false

# =========================================================================
# Runtime State
# =========================================================================
var current_sun_elevation_deg: float = 0.0
var current_fog_density: float = 0.075
var current_mie_anisotropy: float = 0.78
var current_fog_color: Color = Color(0.95, 0.82, 0.65)
var current_sun_color: Color = Color(1.0, 0.65, 0.35)
var current_sun_energy: float = 1.0
var current_god_ray_energy: float = 1.8
var current_phase_name: String = "Dawn"

func _ready() -> void:
	_update_sun_and_atmosphere()

func _process(delta: float) -> void:
	if auto_advance and day_duration_seconds > 0.0:
		diurnal_time = fmod(diurnal_time + (delta / day_duration_seconds), 1.0)
		_update_sun_and_atmosphere()

# =========================================================================
# Core Mathematical Interfaces
# =========================================================================

## Calculates the solar elevation angle theta_sun in degrees based on time of day.
## Accepts either hour_of_day in [0.0, 24.0] or normalized diurnal time in [0.0, 1.0].
func calculate_solar_zenith(hour_of_day: float) -> float:
	var t_day: float = hour_of_day
	if hour_of_day > 1.0:
		t_day = fmod(hour_of_day / 24.0, 1.0)
	return calculate_sun_elevation(t_day)

## Calculates solar elevation angle theta_sun in degrees for normalized diurnal time t_day in [0.0, 1.0).
func calculate_sun_elevation(t_day: float) -> float:
	if use_astronomical_model:
		var phi = deg_to_rad(latitude_degrees)
		var delta = deg_to_rad(solar_declination_degrees)
		var hour_angle = (t_day - 0.50) * TAU
		var sin_elev = sin(delta) * sin(phi) + cos(delta) * cos(phi) * cos(hour_angle)
		sin_elev = clampf(sin_elev, -1.0, 1.0)
		return rad_to_deg(asin(sin_elev))
	else:
		# Standard canonical sinusoidal model matching GDD and survey specifications:
		# Dawn (0.25) = 0.0°, Noon (0.50) = +62.0°, Dusk (0.75) = 0.0°, Midnight (0.0/1.0) = -62.0°
		return sin((t_day - 0.25) * TAU) * max_sun_elevation

## Calculates diurnal volumetric fog density based on solar elevation and weather conditions.
## Follows physical cooling-condensation curves: high morning radiation fog, midday dissipation.
func calculate_fog_density(sun_deg: float, weather_type: int = 0) -> float:
	var base_fog: float
	if sun_deg >= 0.0 and sun_deg < 20.0:
		# Dawn Golden Hour / Morning Radiation Mist
		var factor = (20.0 - sun_deg) / 20.0
		base_fog = lerpf(0.006, 0.075, factor)
	elif sun_deg >= 20.0:
		# Midday Thermal Dissipation (crystal clear visibility)
		base_fog = 0.006
	elif sun_deg >= -15.0 and sun_deg < 0.0:
		# Dusk Purplish/Amber Valley Mist
		var factor = (sun_deg + 15.0) / 15.0
		base_fog = lerpf(0.020, 0.045, factor)
	else:
		# Nocturnal Ambient Cold Haze
		base_fog = 0.020

	# Weather modifier additions
	var weather_boost: float = 0.0
	match weather_type:
		WeatherType.RAIN:
			weather_boost = 0.035
		WeatherType.SNOW:
			weather_boost = 0.070
		WeatherType.THUNDERSTORM:
			weather_boost = 0.060
		WeatherType.BLIZZARD:
			weather_boost = 0.110

	return clampf(base_fog + weather_boost, 0.005, 0.150)

## Computes forward Mie scattering anisotropy g in [0.0, 1.0].
## High anisotropy (0.78) during dawn/dusk creates pronounced forward-scattered "God rays".
func calculate_mie_anisotropy(sun_deg: float) -> float:
	if sun_deg >= 0.0 and sun_deg < 20.0:
		# Dawn peak forward scattering
		return 0.78
	elif sun_deg >= 20.0 and sun_deg < 45.0:
		# Morning transition
		var factor = (45.0 - sun_deg) / 25.0
		return lerpf(0.45, 0.65, factor)
	elif sun_deg >= 45.0:
		# Solar noon diffuse scattering
		return 0.45
	elif sun_deg >= -15.0 and sun_deg < 0.0:
		# Golden dusk
		return 0.74
	else:
		# Night
		return 0.30

## Computes volumetric fog albedo color across diurnal cycle.
func calculate_fog_color(sun_deg: float) -> Color:
	if sun_deg >= 0.0 and sun_deg < 20.0:
		# Dawn: Warm golden amber
		var factor = (20.0 - sun_deg) / 20.0
		return Color(0.88, 0.92, 0.98).lerp(Color(0.95, 0.82, 0.65), factor)
	elif sun_deg >= 20.0 and sun_deg < 45.0:
		# Morning transition
		var factor = (45.0 - sun_deg) / 25.0
		return Color(0.88, 0.92, 0.98).lerp(Color(0.85, 0.88, 0.92), factor)
	elif sun_deg >= 45.0:
		# Midday: Crisp sky blue tint
		return Color(0.88, 0.92, 0.98)
	elif sun_deg >= -15.0 and sun_deg < 0.0:
		# Dusk: Purplish amber
		var factor = (sun_deg + 15.0) / 15.0
		return Color(0.12, 0.16, 0.26).lerp(Color(0.92, 0.55, 0.42), factor)
	else:
		# Night: Deep nocturnal indigo
		return Color(0.12, 0.16, 0.26)

## Computes direct sunlight color based on atmospheric Rayleigh scattering.
## Low sun angles travel through deep airmass, scattering blue light and transmitting red/gold.
func calculate_sun_color(sun_deg: float) -> Color:
	if sun_deg >= 0.0 and sun_deg < 15.0:
		# Dawn: Deep orange-gold
		var factor = (15.0 - sun_deg) / 15.0
		return Color(1.0, 0.90, 0.75).lerp(Color(1.0, 0.65, 0.35), factor)
	elif sun_deg >= 15.0 and sun_deg < 45.0:
		# Morning: Warm yellowish white
		var factor = (45.0 - sun_deg) / 30.0
		return Color(1.0, 0.98, 0.95).lerp(Color(1.0, 0.90, 0.75), factor)
	elif sun_deg >= 45.0:
		# Noon: Brilliant white
		return Color(1.0, 0.98, 0.95)
	elif sun_deg >= -10.0 and sun_deg < 0.0:
		# Dusk: Deep scarlet-amber
		var factor = (sun_deg + 10.0) / 10.0
		return Color(0.20, 0.25, 0.45).lerp(Color(1.0, 0.48, 0.22), factor)
	else:
		# Nocturnal: Cool moonlight
		return Color(0.20, 0.25, 0.45)

## Computes direct light illuminance intensity factoring atmospheric extinction.
func calculate_sun_energy(sun_deg: float) -> float:
	if sun_deg > 15.0:
		return 1.20
	elif sun_deg >= 0.0:
		var factor = sun_deg / 15.0
		return lerpf(0.50, 1.20, factor)
	elif sun_deg >= -12.0:
		var factor = (sun_deg + 12.0) / 12.0
		return lerpf(0.05, 0.50, factor)
	else:
		# Moon light
		return 0.08

## Calculates wavelength-dependent Rayleigh scattering optical depth and God ray transmittance.
func calculate_rayleigh_scattering(sun_deg: float) -> Dictionary:
	var safe_elev = maxf(sun_deg, 1.0)
	var airmass = 1.0 / maxf(sin(deg_to_rad(safe_elev)), 0.04)

	# Rayleigh scattering coefficients (proportional to 1 / lambda^4)
	# Red: 680nm, Green: 550nm, Blue: 440nm
	var tau_red = 0.058 * airmass
	var tau_green = 0.135 * airmass
	var tau_blue = 0.332 * airmass

	var trans_red = exp(-tau_red)
	var trans_green = exp(-tau_green)
	var trans_blue = exp(-tau_blue)

	var god_ray_boost = 1.0
	if sun_deg >= 0.0 and sun_deg < 20.0:
		god_ray_boost = lerpf(1.0, 2.2, (20.0 - sun_deg) / 20.0)
	elif sun_deg >= -10.0 and sun_deg < 0.0:
		god_ray_boost = lerpf(1.0, 1.8, (sun_deg + 10.0) / 10.0)

	return {
		"airmass": airmass,
		"transmittance": Vector3(trans_red, trans_green, trans_blue),
		"god_ray_energy": god_ray_boost,
		"direct_color": Color(trans_red, trans_green, trans_blue)
	}

## Returns textual description of current diurnal phase.
func get_diurnal_phase(sun_deg: float) -> String:
	if sun_deg >= 0.0 and sun_deg < 15.0:
		return "Dawn (Subh)"
	elif sun_deg >= 15.0 and sun_deg < 45.0:
		return "Morning"
	elif sun_deg >= 45.0:
		return "Solar Noon (Peshin)"
	elif sun_deg >= -15.0 and sun_deg < 0.0:
		return "Golden Dusk (Shom)"
	else:
		return "Nocturnal Deep (Tun)"

# =========================================================================
# Internal Update & Synchronizer
# =========================================================================

func _update_sun_and_atmosphere() -> void:
	# Check SeasonManager for dynamic weather synchronization if present
	var season_mgr = null
	if is_inside_tree() and get_tree().root:
		season_mgr = get_tree().root.find_child("SeasonManager", true, false)
	if season_mgr and "current_weather" in season_mgr:
		current_weather = season_mgr.current_weather as WeatherType

	# 1. Solar Elevation Calculation
	current_sun_elevation_deg = calculate_sun_elevation(diurnal_time)

	# 2. Atmospheric & Volumetric Fog Modulation
	current_fog_density = calculate_fog_density(current_sun_elevation_deg, current_weather)
	current_mie_anisotropy = calculate_mie_anisotropy(current_sun_elevation_deg)
	current_fog_color = calculate_fog_color(current_sun_elevation_deg)

	# 3. Rayleigh Scattering & Sun Illumination
	var rayleigh = calculate_rayleigh_scattering(current_sun_elevation_deg)
	current_sun_color = calculate_sun_color(current_sun_elevation_deg)
	current_sun_energy = calculate_sun_energy(current_sun_elevation_deg)
	current_god_ray_energy = rayleigh["god_ray_energy"]

	var old_phase = current_phase_name
	current_phase_name = get_diurnal_phase(current_sun_elevation_deg)
	if old_phase != current_phase_name:
		emit_signal("phase_changed", current_phase_name)

	# 4. Apply to DirectionalLight3D
	if sun_light:
		sun_light.rotation_degrees.x = -current_sun_elevation_deg
		sun_light.rotation_degrees.y = diurnal_time * 360.0
		sun_light.light_color = current_sun_color
		sun_light.light_energy = current_sun_energy
		if "light_volumetric_fog_energy" in sun_light:
			sun_light.set("light_volumetric_fog_energy", current_god_ray_energy)

	# 5. Apply to WorldEnvironment
	if world_environment and world_environment.environment:
		var env = world_environment.environment
		env.volumetric_fog_enabled = true
		env.volumetric_fog_density = current_fog_density
		env.volumetric_fog_anisotropy = current_mie_anisotropy
		env.volumetric_fog_albedo = current_fog_color

	emit_signal("time_of_day_updated", diurnal_time, current_sun_elevation_deg)
	emit_signal("atmosphere_updated", current_fog_density, current_sun_color)
