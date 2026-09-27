# scripts/mechanisms/rail_switch.gd
class_name RailSwitch
extends Node3D

# Turnout Rail Switch with Counterweighted Ground-Throw Stand
# Inspired by Railcraft, Create Mod, and Vintage Story
# Controls rolling stock routing across track junctions and rail sidings.

signal route_switched(new_route: String)
signal signal_aspect_changed(aspect: String)
signal derailment_hazard(reason: String)

enum Route {
	STRAIGHT,
	DIVERGING
}

@export var switch_id: String = "switch_01"
@export var current_route: Route = Route.STRAIGHT
@export var target_route: Route = Route.STRAIGHT
@export var throw_duration_s: float = 0.6 # Time to slide point blades
@export var max_diverging_speed_m_s: float = 2.5 # Speed limit through curved frog

var transition_progress: float = 0.0 # 0.0 (fully straight) to 1.0 (fully diverging)
var is_locked: bool = false # Interlocked during train occupancy
var is_occupied: bool = false
var trailing_spring_capable: bool = true
var spring_deflected: bool = false

func _init(id: String = "switch_01", initial_route: Route = Route.STRAIGHT):
	switch_id = id
	current_route = initial_route
	target_route = initial_route
	transition_progress = 1.0 if initial_route == Route.DIVERGING else 0.0

func throw_switch(to_diverging: bool) -> bool:
	if is_locked or is_occupied:
		return false
	target_route = Route.DIVERGING if to_diverging else Route.STRAIGHT
	return true

func toggle_switch() -> bool:
	if is_locked or is_occupied:
		return false
	target_route = Route.STRAIGHT if current_route == Route.DIVERGING else Route.DIVERGING
	return true

func set_train_occupancy(occupied: bool) -> void:
	is_occupied = occupied
	is_locked = occupied

func get_signal_aspect() -> String:
	if transition_progress > 0.0 and transition_progress < 1.0:
		return "RED_TRANSIT"
	elif current_route == Route.STRAIGHT:
		return "GREEN_CLEAR"
	else:
		return "YELLOW_DIVERGING"

func check_approach(facing_point: bool, approaching_branch: String, train_speed_m_s: float) -> Dictionary:
	var can_proceed: bool = true
	var speed_safe: bool = true
	var hazard_reason: String = ""

	if transition_progress > 0.0 and transition_progress < 1.0:
		can_proceed = false
		hazard_reason = "Points in mid-throw transit"
		derailment_hazard.emit(hazard_reason)
		return {"safe": false, "reason": hazard_reason, "target_track": "NONE"}

	if facing_point:
		# Facing movement: train goes where points point
		var destination_track: String = "DIVERGING" if current_route == Route.DIVERGING else "STRAIGHT"
		if current_route == Route.DIVERGING and train_speed_m_s > max_diverging_speed_m_s:
			speed_safe = false
			hazard_reason = "Excessive speed through diverging frog (%0.1f m/s > %0.1f m/s)" % [train_speed_m_s, max_diverging_speed_m_s]
			derailment_hazard.emit(hazard_reason)

		return {
			"safe": speed_safe,
			"target_track": destination_track,
			"reason": hazard_reason,
			"aspect": get_signal_aspect()
		}
	else:
		# Trailing movement: train comes from branch onto single trunk
		var route_aligned: bool = (approaching_branch == "STRAIGHT" and current_route == Route.STRAIGHT) or \
								  (approaching_branch == "DIVERGING" and current_route == Route.DIVERGING)
		if not route_aligned:
			if trailing_spring_capable:
				spring_deflected = true
				return {
					"safe": true,
					"target_track": "TRUNK",
					"reason": "Spring points deflected safely",
					"aspect": "SPRING_YIELD"
				}
			else:
				hazard_reason = "Trailing movement split non-spring points (derailment)"
				derailment_hazard.emit(hazard_reason)
				return {
					"safe": false,
					"target_track": "NONE",
					"reason": hazard_reason,
					"aspect": "RED_SPLIT"
				}

		return {
			"safe": true,
			"target_track": "TRUNK",
			"reason": "Route perfectly aligned",
			"aspect": get_signal_aspect()
		}

func process_switch(delta: float) -> Dictionary:
	var target_val: float = 1.0 if target_route == Route.DIVERGING else 0.0
	if abs(transition_progress - target_val) > 0.001:
		var step: float = (1.0 / throw_duration_s) * delta
		transition_progress = move_toward(transition_progress, target_val, step)
		if transition_progress >= 0.999:
			transition_progress = 1.0
			current_route = Route.DIVERGING
			route_switched.emit("DIVERGING")
			signal_aspect_changed.emit(get_signal_aspect())
		elif transition_progress <= 0.001:
			transition_progress = 0.0
			current_route = Route.STRAIGHT
			route_switched.emit("STRAIGHT")
			signal_aspect_changed.emit(get_signal_aspect())
	else:
		spring_deflected = false

	return {
		"current_route": "DIVERGING" if current_route == Route.DIVERGING else "STRAIGHT",
		"target_route": "DIVERGING" if target_route == Route.DIVERGING else "STRAIGHT",
		"transition_progress": transition_progress,
		"signal_aspect": get_signal_aspect(),
		"is_locked": is_locked,
		"is_occupied": is_occupied,
		"spring_deflected": spring_deflected
	}
