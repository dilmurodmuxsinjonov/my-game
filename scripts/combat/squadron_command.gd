# scripts/combat/squadron_command.gd
# Voxel Lord: Feudal Realm - Milestone 47: Tactical Garrison Squadron Command
# Manages military guard formations, tactical stances, rally cries, and combat coordinate offsets.

class_name SquadronCommand
extends Node

signal stance_changed(new_stance: int, stance_name: String)
signal formation_changed(new_formation: int, formation_name: String)
signal squad_rallied(guard_count: int, rally_pos: Vector3)

enum TacticalStance {
	DEFENSIVE_SENTINEL = 0,
	AGGRESSIVE_ASSAULT = 1,
	MONARCH_ESCORT = 2
}

enum FormationType {
	SHIELD_WALL = 0,
	SHOCK_WEDGE = 1,
	SKIRMISH_LINE = 2,
	PERIMETER_SQUARE = 3
}

const STANCE_NAMES: Dictionary = {
	TacticalStance.DEFENSIVE_SENTINEL: "Defensive Sentinel (Hold Gates & Perimeter)",
	TacticalStance.AGGRESSIVE_ASSAULT: "Aggressive Assault (Hunt Raiders & Camps)",
	TacticalStance.MONARCH_ESCORT: "Monarch Escort (Royal Bodyguard Formation)"
}

const FORMATION_NAMES: Dictionary = {
	FormationType.SHIELD_WALL: "Shield Wall (Locked Bucklers)",
	FormationType.SHOCK_WEDGE: "Shock Wedge (Vanguard Charge)",
	FormationType.SKIRMISH_LINE: "Skirmish Line (Spread Archers)",
	FormationType.PERIMETER_SQUARE: "Perimeter Square (360° Bulwark)"
}

const FORMATION_BONUSES: Dictionary = {
	FormationType.SHIELD_WALL: {
		"defense_bonus": 0.35,
		"speed_mult": 0.80,
		"block_chance": 0.30
	},
	FormationType.SHOCK_WEDGE: {
		"attack_bonus": 0.40,
		"speed_mult": 1.10,
		"charge_knockback": 2.5
	},
	FormationType.SKIRMISH_LINE: {
		"attack_speed_bonus": 0.25,
		"speed_mult": 1.05,
		"aoe_resistance": 0.50
	},
	FormationType.PERIMETER_SQUARE: {
		"defense_bonus": 0.20,
		"speed_mult": 0.90,
		"perimeter_coverage": 1.0
	}
}

var current_stance: TacticalStance = TacticalStance.DEFENSIVE_SENTINEL
var current_formation: FormationType = FormationType.SHIELD_WALL
var rally_position: Vector3 = Vector3(32, 12, 32)
var guard_morale: float = 100.0

func set_stance(stance: TacticalStance) -> void:
	current_stance = stance
	stance_changed.emit(int(current_stance), get_stance_name(current_stance))

func set_formation(formation: FormationType) -> void:
	current_formation = formation
	formation_changed.emit(int(current_formation), get_formation_name(current_formation))

func cycle_stance(forward: bool = true) -> TacticalStance:
	var count = TacticalStance.size()
	var cur = int(current_stance)
	if forward:
		cur = (cur + 1) % count
	else:
		cur = (cur - 1 + count) % count
	current_stance = cur as TacticalStance
	stance_changed.emit(int(current_stance), get_stance_name(current_stance))
	return current_stance

func cycle_formation(forward: bool = true) -> FormationType:
	var count = FormationType.size()
	var cur = int(current_formation)
	if forward:
		cur = (cur + 1) % count
	else:
		cur = (cur - 1 + count) % count
	current_formation = cur as FormationType
	formation_changed.emit(int(current_formation), get_formation_name(current_formation))
	return current_formation

func get_stance_name(s: TacticalStance = current_stance) -> String:
	return STANCE_NAMES.get(s, "Unknown Stance")

func get_formation_name(f: FormationType = current_formation) -> String:
	return FORMATION_NAMES.get(f, "Unknown Formation")

func get_formation_modifiers() -> Dictionary:
	return FORMATION_BONUSES.get(current_formation, {})

func get_formation_offsets(unit_count: int) -> Array[Vector3]:
	var offsets: Array[Vector3] = []
	if unit_count <= 0:
		return offsets
	
	match current_formation:
		FormationType.SHIELD_WALL:
			# Single line abreast perpendicular to facing
			var half_width = (unit_count - 1) * 0.75
			for i in range(unit_count):
				offsets.append(Vector3(i * 1.5 - half_width, 0, 1.2))
		
		FormationType.SHOCK_WEDGE:
			# V-shape wedge facing forward
			offsets.append(Vector3(0, 0, 2.0)) # Point
			for i in range(1, unit_count):
				var side = 1.0 if (i % 2 == 1) else -1.0
				var rank = float((i + 1) / 2)
				offsets.append(Vector3(side * rank * 1.4, 0, 2.0 - rank * 1.2))
		
		FormationType.SKIRMISH_LINE:
			# Wide dispersed rank
			var half_width = (unit_count - 1) * 1.5
			for i in range(unit_count):
				offsets.append(Vector3(i * 3.0 - half_width, 0, (i % 2) * 0.8))
		
		FormationType.PERIMETER_SQUARE:
			# Guard circle / square around center
			var radius = 2.5
			var step = TAU / float(max(unit_count, 1))
			for i in range(unit_count):
				offsets.append(Vector3(cos(i * step) * radius, 0, sin(i * step) * radius))
	
	return offsets

func issue_rally_call(monarch_pos: Vector3, citizens: Array = []) -> int:
	rally_position = monarch_pos
	var rallied_count = 0
	for c in citizens:
		# Check if citizen is guard / warrior or has method
		if "current_role" in c and c.current_role == 5: # Guard role
			rallied_count += 1
			if c.has_method("set_work_target"):
				c.set_work_target(monarch_pos)
			if c.has_method("boost_morale"):
				c.boost_morale(10.0)
	
	squad_rallied.emit(rallied_count, monarch_pos)
	return rallied_count

func to_dict() -> Dictionary:
	return {
		"stance": int(current_stance),
		"formation": int(current_formation),
		"guard_morale": guard_morale
	}

func from_dict(d: Dictionary) -> void:
	if d.has("stance"):
		current_stance = d["stance"] as TacticalStance
	if d.has("formation"):
		current_formation = d["formation"] as FormationType
	if d.has("guard_morale"):
		guard_morale = float(d["guard_morale"])
	stance_changed.emit(int(current_stance), get_stance_name(current_stance))
	formation_changed.emit(int(current_formation), get_formation_name(current_formation))
