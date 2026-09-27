# scripts/physics/ballistic_realism.gd
# Voxel Lord: Feudal Realm - Milestone 31 & Realism Architecture R1
# Ballistic Realism, Barometric Air Density Decay & Aerodynamic Drag Engine
# Computes altitude air density rho(y), aerodynamic drag a_d, crosswind drift,
# kinetic energy dissipation, and trajectory integration for arrows, bolts, and siege boulders.

class_name BallisticRealism
extends RefCounted

const SEA_LEVEL_AIR_DENSITY: float = 1.225 # kg / m^3 at standard sea level (15°C)
const SCALE_HEIGHT: float = 8500.0         # Tropospheric scale height in meters
const GRAVITY: Vector3 = Vector3(0.0, -9.80665, 0.0)

# Projectile ballistic profiles: mass (kg), cross-sectional area A (m^2), drag coefficient Cd, armor penetration
const PROJECTILE_PROFILES: Dictionary = {
	"bodkin_arrow": {"mass": 0.050, "area": 0.00015, "drag_coeff": 0.045, "penetration_factor": 1.4},
	"broadhead_arrow": {"mass": 0.065, "area": 0.00035, "drag_coeff": 0.060, "penetration_factor": 1.0},
	"standard_arrow": {"mass": 0.045, "area": 0.00050, "drag_coeff": 0.400, "penetration_factor": 1.2},
	"arrow": {"mass": 0.045, "area": 0.00050, "drag_coeff": 0.400, "penetration_factor": 1.2},
	"heavy_crossbow_bolt": {"mass": 0.080, "area": 0.00020, "drag_coeff": 0.050, "penetration_factor": 1.6},
	"crossbow_bolt": {"mass": 0.080, "area": 0.00020, "drag_coeff": 0.050, "penetration_factor": 1.6},
	"catapult_boulder": {"mass": 40.0, "area": 0.080, "drag_coeff": 0.450, "penetration_factor": 2.5},
	"fire_boulder": {"mass": 40.0, "area": 0.080, "drag_coeff": 0.450, "penetration_factor": 2.5},
	"trebuchet_stone": {"mass": 100.0, "area": 0.125, "drag_coeff": 0.470, "penetration_factor": 3.5},
	"trebuchet_boulder": {"mass": 130.0, "area": 0.150, "drag_coeff": 0.470, "penetration_factor": 3.5}
}

## Returns barometric air density at a given altitude y: rho(y) = rho_0 * exp(-y / H)
static func get_air_density_at_altitude(altitude_y: float) -> float:
	var alt = max(0.0, altitude_y)
	return SEA_LEVEL_AIR_DENSITY * exp(-alt / SCALE_HEIGHT)

## Computes aerodynamic drag acceleration vector:
## a_drag = - (1 / 2m) * rho(y) * Cd * A * |v_rel| * v_rel
static func compute_aerodynamic_acceleration(
	velocity: Vector3,
	wind_velocity: Vector3 = Vector3.ZERO,
	altitude_y: float = 0.0,
	projectile_type: String = "bodkin_arrow"
) -> Vector3:
	var profile = PROJECTILE_PROFILES.get(projectile_type.to_lower(), PROJECTILE_PROFILES["bodkin_arrow"])
	var mass: float = profile["mass"]
	var area: float = profile["area"]
	var drag_coeff: float = profile["drag_coeff"]

	var air_density = get_air_density_at_altitude(altitude_y)
	
	# Relative airflow velocity accounting for crosswind: v_rel = v - v_wind
	var v_rel = velocity - wind_velocity
	var speed_rel = v_rel.length()

	if speed_rel < 0.0001:
		return Vector3.ZERO

	# Drag force magnitude: Fd = 0.5 * rho * v_rel^2 * Cd * A
	var drag_force_mag = 0.5 * air_density * (speed_rel * speed_rel) * drag_coeff * area
	var drag_direction = -v_rel.normalized()
	var drag_force = drag_direction * drag_force_mag

	# Acceleration = F / m
	return drag_force / mass

## Simulates a single physics time step combining gravity and aerodynamic drag
static func simulate_trajectory_step(
	pos: Vector3,
	vel: Vector3,
	wind_vel: Vector3 = Vector3.ZERO,
	dt: float = 0.02,
	projectile_type: String = "bodkin_arrow"
) -> Dictionary:
	var drag_acc = compute_aerodynamic_acceleration(vel, wind_vel, pos.y, projectile_type)
	var total_acc = GRAVITY + drag_acc

	# Semi-implicit Euler / Verlet integration
	var next_vel = vel + total_acc * dt
	var next_pos = pos + next_vel * dt

	return {
		"position": next_pos,
		"velocity": next_vel,
		"drag_acceleration": drag_acc,
		"total_acceleration": total_acc
	}

## Interface Contract: BallisticRealism.integrate_trajectory(start_pos: Vector3, initial_vel: Vector3, projectile_type: String, dt: float) -> Array[Vector3]
## Generates full 3D ballistic trajectory path points until ground impact or max_steps
static func integrate_trajectory(
	start_pos: Vector3,
	initial_vel: Vector3,
	projectile_type: String = "bodkin_arrow",
	dt: float = 0.05,
	max_steps: int = 250,
	wind_vel: Vector3 = Vector3.ZERO
) -> Array[Vector3]:
	var path: Array[Vector3] = [start_pos]
	var cur_pos = start_pos
	var cur_vel = initial_vel
	
	for _i in range(max_steps):
		var step = simulate_trajectory_step(cur_pos, cur_vel, wind_vel, dt, projectile_type)
		cur_pos = step["position"]
		cur_vel = step["velocity"]
		path.append(cur_pos)
		
		# Ground collision cutoff
		if cur_pos.y <= 0.0:
			break
			
	return path

## Computes kinetic energy in Joules: Ek = 0.5 * m * v^2
static func calculate_kinetic_energy(mass_kg: float, velocity: Vector3) -> float:
	var speed = velocity.length()
	return 0.5 * mass_kg * (speed * speed)

## Computes impact damage from kinetic energy: Damage = Ek * 0.05
static func calculate_impact_damage(kinetic_energy_joules: float) -> float:
	return kinetic_energy_joules * 0.05

## Calculates armor penetration and damage against armored targets
static func calculate_impact_penetration(
	velocity: Vector3,
	projectile_type: String,
	target_armor_rating: float
) -> Dictionary:
	var profile = PROJECTILE_PROFILES.get(projectile_type.to_lower(), PROJECTILE_PROFILES["bodkin_arrow"])
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
