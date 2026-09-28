# scripts/world/atmospheric_post_process.gd
# Voxel Lord: Feudal Realm - Milestone 46: Atmospheric Shaders & Visual Realism
# Manages volumetric fog, skybox lighting curves, seasonal foliage tinting, and altitude weather effects.

class_name AtmosphericPostProcess
extends Node

signal atmosphere_updated(params: Dictionary)

enum Season {
	SPRING = 0,
	SUMMER = 1,
	AUTUMN = 2,
	WINTER = 3
}

enum Weather {
	CLEAR = 0,
	CLOUDY = 1,
	RAIN = 2,
	FOG = 3,
	SNOW = 4
}

# Foliage tints by season
const SEASON_FOLIAGE_TINTS: Dictionary = {
	Season.SPRING: Color(0.38, 0.78, 0.26, 1.0),  # Fresh lime green
	Season.SUMMER: Color(0.18, 0.54, 0.15, 1.0),  # Deep lush emerald
	Season.AUTUMN: Color(0.86, 0.46, 0.12, 1.0),  # Auburn golden orange
	Season.WINTER: Color(0.82, 0.88, 0.94, 1.0)   # Frosted rime snow white
}

# Base fog parameters by weather
const WEATHER_FOG_BASE: Dictionary = {
	Weather.CLEAR: {"density": 0.0006, "energy": 1.0, "wetness": 0.0, "frost": 0.0},
	Weather.CLOUDY: {"density": 0.0022, "energy": 0.75, "wetness": 0.1, "frost": 0.0},
	Weather.RAIN: {"density": 0.0075, "energy": 0.45, "wetness": 0.95, "frost": 0.0},
	Weather.FOG: {"density": 0.0280, "energy": 0.30, "wetness": 0.40, "frost": 0.0},
	Weather.SNOW: {"density": 0.0160, "energy": 0.55, "wetness": 0.15, "frost": 0.90}
}

# Sky colors for day phases
const SKY_COLORS: Dictionary = {
	"dawn_zenith": Color(0.35, 0.42, 0.65, 1.0),
	"dawn_horizon": Color(0.95, 0.60, 0.35, 1.0),
	"noon_zenith": Color(0.40, 0.65, 0.92, 1.0),
	"noon_horizon": Color(0.70, 0.82, 0.95, 1.0),
	"dusk_zenith": Color(0.25, 0.28, 0.52, 1.0),
	"dusk_horizon": Color(0.88, 0.40, 0.22, 1.0),
	"night_zenith": Color(0.04, 0.05, 0.12, 1.0),
	"night_horizon": Color(0.08, 0.10, 0.18, 1.0)
}

func calculate_sun_position(day_progress: float) -> Dictionary:
	# day_progress in [0.0, 1.0]
	# 0.0 = dawn (horizon), 0.25 = noon (zenith), 0.5 = dusk (horizon), 0.75 = midnight (nadir)
	var angle_rad = day_progress * TAU
	var pitch = sin(angle_rad)
	var yaw = cos(angle_rad)
	
	var is_day = pitch > -0.05
	var raw_sun_energy = clampf(pitch, 0.0, 1.0)
	var sun_dir = Vector3(yaw, -maxf(pitch, 0.05), 0.35).normalized()
	
	return {
		"pitch": pitch,
		"yaw": yaw,
		"is_day": is_day,
		"sun_energy": raw_sun_energy,
		"direction": sun_dir
	}

func get_seasonal_foliage_tint(season: int, day_in_season: int = 15, season_length: int = 30) -> Color:
	var s_curr = season % 4
	var s_next = (s_curr + 1) % 4
	var t = clampf(float(day_in_season) / float(max(season_length, 1)), 0.0, 1.0)
	
	var col_curr: Color = SEASON_FOLIAGE_TINTS.get(s_curr, Color.GREEN)
	var col_next: Color = SEASON_FOLIAGE_TINTS.get(s_next, Color.GREEN)
	
	return col_curr.lerp(col_next, t * 0.5)

func calculate_fog_parameters(weather: int, altitude: float, is_night: bool) -> Dictionary:
	var w_cfg = WEATHER_FOG_BASE.get(weather, WEATHER_FOG_BASE[Weather.CLEAR])
	var base_density: float = w_cfg["density"]
	
	# Altitude gradient: valleys (low y) have higher condensation/fog, peaks are clearer
	var alt_factor = clampf(1.0 - (altitude - 16.0) / 48.0, 0.4, 1.8)
	var final_density = base_density * alt_factor
	
	# Fog color depends on night vs day
	var fog_color: Color
	if is_night:
		fog_color = Color(0.08, 0.10, 0.16, 1.0)
	else:
		match weather:
			Weather.CLEAR:
				fog_color = Color(0.72, 0.80, 0.90, 1.0)
			Weather.CLOUDY:
				fog_color = Color(0.65, 0.68, 0.72, 1.0)
			Weather.RAIN:
				fog_color = Color(0.48, 0.52, 0.58, 1.0)
			Weather.FOG:
				fog_color = Color(0.78, 0.80, 0.82, 1.0)
			Weather.SNOW:
				fog_color = Color(0.85, 0.88, 0.92, 1.0)
			_:
				fog_color = Color(0.7, 0.7, 0.7, 1.0)
	
	return {
		"density": final_density,
		"color": fog_color,
		"wetness": w_cfg["wetness"],
		"frost": w_cfg["frost"]
	}

func calculate_sky_colors(day_progress: float, weather: int) -> Dictionary:
	var z_col: Color
	var h_col: Color
	var ambient_energy: float = 0.85
	
	# Day phase interpolation
	if day_progress < 0.2:
		# Dawn to morning
		var t = day_progress / 0.2
		z_col = SKY_COLORS["dawn_zenith"].lerp(SKY_COLORS["noon_zenith"], t)
		h_col = SKY_COLORS["dawn_horizon"].lerp(SKY_COLORS["noon_horizon"], t)
		ambient_energy = lerpf(0.4, 0.9, t)
	elif day_progress < 0.45:
		# Noon full daylight
		z_col = SKY_COLORS["noon_zenith"]
		h_col = SKY_COLORS["noon_horizon"]
		ambient_energy = 1.0
	elif day_progress < 0.65:
		# Dusk sunset
		var t = (day_progress - 0.45) / 0.2
		z_col = SKY_COLORS["noon_zenith"].lerp(SKY_COLORS["dusk_zenith"], t)
		h_col = SKY_COLORS["noon_horizon"].lerp(SKY_COLORS["dusk_horizon"], t)
		ambient_energy = lerpf(0.9, 0.35, t)
	else:
		# Night
		var t = minf((day_progress - 0.65) / 0.35, 1.0)
		z_col = SKY_COLORS["dusk_zenith"].lerp(SKY_COLORS["night_zenith"], t)
		h_col = SKY_COLORS["dusk_horizon"].lerp(SKY_COLORS["night_horizon"], t)
		ambient_energy = lerpf(0.35, 0.15, t)
	
	# Weather attenuation
	var w_cfg = WEATHER_FOG_BASE.get(weather, WEATHER_FOG_BASE[Weather.CLEAR])
	ambient_energy *= w_cfg["energy"]
	
	return {
		"zenith_color": z_col,
		"horizon_color": h_col,
		"ambient_energy": ambient_energy
	}

func evaluate_atmosphere(
	day_progress: float,
	season: int,
	weather: int,
	player_pos: Vector3 = Vector3(32, 20, 32),
	day_in_season: int = 15,
	season_length: int = 30
) -> Dictionary:
	var sun_data = calculate_sun_position(day_progress)
	var sky_data = calculate_sky_colors(day_progress, weather)
	var fog_data = calculate_fog_parameters(weather, player_pos.y, not sun_data["is_day"])
	var foliage_tint = get_seasonal_foliage_tint(season, day_in_season, season_length)
	
	var params = {
		"day_progress": day_progress,
		"season": season,
		"weather": weather,
		"sun_direction": sun_data["direction"],
		"sun_energy": sun_data["sun_energy"] * WEATHER_FOG_BASE[weather]["energy"],
		"is_day": sun_data["is_day"],
		"sky_zenith": sky_data["zenith_color"],
		"sky_horizon": sky_data["horizon_color"],
		"ambient_energy": sky_data["ambient_energy"],
		"fog_density": fog_data["density"],
		"fog_color": fog_data["color"],
		"wetness_factor": fog_data["wetness"],
		"frost_factor": fog_data["frost"],
		"foliage_tint": foliage_tint
	}
	
	atmosphere_updated.emit(params)
	return params

func apply_to_environment(world_env: WorldEnvironment, sun_light: DirectionalLight3D, params: Dictionary) -> void:
	if not world_env or not world_env.environment:
		return
	
	var env = world_env.environment
	env.background_mode = Environment.BG_COLOR
	env.background_color = params.get("sky_horizon", Color(0.5, 0.7, 0.9))
	env.ambient_light_energy = params.get("ambient_energy", 0.8)
	env.ambient_light_color = params.get("sky_zenith", Color(0.6, 0.7, 0.8))
	
	# Volumetric fog parameters
	env.volumetric_fog_enabled = true
	env.volumetric_fog_density = params.get("fog_density", 0.001)
	env.volumetric_fog_albedo = params.get("fog_color", Color.WHITE)
	
	if sun_light:
		sun_light.light_energy = params.get("sun_energy", 1.0)
		var dir: Vector3 = params.get("sun_direction", Vector3(0.5, -0.7, 0.5))
		if dir.length_squared() > 0.01:
			sun_light.look_at(sun_light.global_position + dir, Vector3.UP)
