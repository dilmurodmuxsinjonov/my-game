# scripts/physics/ballistic_realism.gd
# Voxel Lord: Feudal Realm - Milestone 31: Ballistic Realism, Aerodynamic Drag & Crosswind Physics
# Computes barometric air density, aerodynamic drag, crosswind trajectory deflection,
# and kinetic energy armor penetration for arrows, bolts, and trebuchet boulders.

class_name BallisticRealism
extends RefCounted

const SEA_LEVEL_AIR_DENSITY: float = 1.225 # kg / m^3 at standard sea level (15°C)
const SCALE_HEIGHT: float = 8500.0         # Tropospheric scale height in meters
const GRAVITY: Vector3 = Vector3(0.0, -9.80665, 0.0)

# Projectile ballistic profiles: mass (kg), cross-sectional area A (m^2), drag coefficient Cd
const PROJECTILE_PROFILES: Dictionary = {
	"bodkin_arrow": {"mass": 0.050, "area": 0.00015, "drag_coeff": 0.045, "penetration_factor": 1.4},
	"broadhead_arrow": {"mass": 0.065, "area": 0.00035, "drag_coeff": 0.060, "penetration_factor": 1.0},
	"heavy_crossbow_bolt": {"mass": 0.080, "area": 0.00020, "drag_coeff": 0.050, "penetration_factor": 1.6},
	"trebuchet_stone": {"mass": 100.0, "area": 0.125, "drag_coeff": 0.470, "penetration_factor": 3.5}
}

static func get_air_density_at_altitude(altitude_y: float) -> float:
	# Barometric formula: rho(y) = rho_0 * exp(-y / H)
	var alt = max(0.0, altitude_y)
	return SEA_LEVEL_AIR_DENSITY * exp(-alt / SCALE_HEIGHT)

static func compute_aerodynamic_acceleration(
	velocity: Vector3,
	wind_velocity: Vector3,
	altitude_y: float,
	projectile_type: String = "bodkin_arrow"
) -> Vector3:
	var profile = PROJECTILE_PROFILES.get(projectile_type, PROJECTILE_PROFILES["bodkin_arrow"])
	var mass: float = profile["mass"]
	var area: float = profile["area"]
	var drag_coeff: float = profile["drag_coeff"]

	var air_density = get_air_density_at_altitude(altitude_y)
	# Relative airflow velocity accounting for crosswind
	var v_rel = velocity - wind_velocity
	var speed_rel = v_rel.length()

	if speed_rel < 0.001:
		return Vector3.ZERO

	# Drag force magnitude: Fd = 0.5 * rho * v^2 * Cd * A
	var drag_force_mag = 0.5 * air_density * (speed_rel * speed_rel) * drag_coeff * area
	var drag_direction = -v_rel.normalized()
	var drag_force = drag_direction * drag_force_mag

	# Acceleration = F / m
	return drag_force / mass

static func simulate_trajectory_step(
	pos: Vector3,
	vel: Vector3,
	wind_vel: Vector3,
	dt: float,
	projectile_type: String = "bodkin_arrow"
) -> Dictionary:
	# Predicts next position and velocity with gravity and aerodynamic drag
	var drag_acc = compute_aerodynamic_acceleration(vel, wind_vel, pos.y, projectile_type)
	var total_acc = GRAVITY + drag_acc

	var next_vel = vel + total_acc * dt
	var next_pos = pos + (vel + next_vel) * 0.5 * dt # Heun / Verlet step

	return {
		"position": next_pos,
		"velocity": next_vel,
		"drag_acceleration": drag_acc
	}

static func calculate_impact_penetration(
	velocity: Vector3,
	projectile_type: String,
	target_armor_rating: float
) -> Dictionary:
	var profile = PROJECTILE_PROFILES.get(projectile_type, PROJECTILE_PROFILES["bodkin_arrow"])
	var mass: float = profile["mass"]
	var pen_factor: float = profile["penetration_factor"]

	var speed = velocity.length()
	var kinetic_energy = 0.5 * mass * (speed * speed) # Joules

	# Armor penetration threshold: effective penetrating damage after armor resistance
	var effective_damage = max(0.0, (kinetic_energy * pen_factor) - (target_armor_rating * 1.5))
	var is_penetrated = effective_damage > 0.0

	return {
		"impact_speed_mps": speed,
		"kinetic_energy_joules": kinetic_energy,
		"effective_damage": effective_damage,
		"is_penetrated": is_penetrated
	}
