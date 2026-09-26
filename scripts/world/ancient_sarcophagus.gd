# scripts/world/ancient_sarcophagus.gd
# Voxel Lord: Feudal Realm - Milestone 28: Ancient Stone Sarcophagus & Relics
# Interactive sealed limestone tombs with prying mechanics, traps, and historical relics.

class_name AncientSarcophagus
extends RefCounted

signal prying_started(sarcophagus_id: String)
signal prying_progress_updated(sarcophagus_id: String, progress: float)
signal sarcophagus_opened(sarcophagus_id: String, relics: Array)
signal trap_triggered(sarcophagus_id: String, trap_type: String, damage: int)

enum SarcophagusState {
	SEALED,
	PRYING,
	OPENED,
	LOOTED
}

var sarcophagus_id: String = "sarcophagus_1"
var state: int = SarcophagusState.SEALED
var prying_progress: float = 0.0
var base_prying_rate: float = 12.0 # % per second
var trap_type: String = "POISON_DARTS" # "NONE", "POISON_DARTS", "COLLAPSE_DUST"
var trap_disarmed: bool = false
var relics: Array[Dictionary] = []

func _init(p_id: String = "sarcophagus_1", p_trap: String = "POISON_DARTS") -> void:
	sarcophagus_id = p_id
	trap_type = p_trap
	_generate_relic_loot()

func _generate_relic_loot() -> void:
	relics.clear()
	relics.append({
		"item_id": "ancient_steel_schematic",
		"name": "Ancient Damascus Steel Blueprint",
		"type": "TECHNOLOGY_BLUEPRINT",
		"value": 45,
		"lore": "Lost metallurgical secrets of the first feudal empire."
	})
	relics.append({
		"item_id": "lost_king_signet",
		"name": "Signet Ring of King Alden",
		"type": "NOBLE_RELIC",
		"prestige_bonus": 20,
		"diplomacy_vassal_bonus": 15,
		"value": 60
	})
	relics.append({
		"item_id": "ancient_coins",
		"name": "Ancient Gilded Sovereigns",
		"type": "CURRENCY",
		"amount": 25,
		"value": 25
	})

func start_prying() -> bool:
	if state != SarcophagusState.SEALED:
		return false
	state = SarcophagusState.PRYING
	prying_started.emit(sarcophagus_id)
	return true

func disarm_trap(rogue_skill: int = 50) -> bool:
	if trap_type == "NONE" or trap_disarmed:
		return true
	if rogue_skill >= 40:
		trap_disarmed = true
		return true
	return false

func advance_prying(delta: float, has_iron_crowbar: bool = false) -> Dictionary:
	if state != SarcophagusState.PRYING:
		return {"state": state, "opened": false, "trap_triggered": false}

	var rate = base_prying_rate * (2.2 if has_iron_crowbar else 1.0)
	prying_progress = min(100.0, prying_progress + rate * delta)
	prying_progress_updated.emit(sarcophagus_id, prying_progress)

	var did_open = false
	var did_trap = false

	if prying_progress >= 100.0:
		state = SarcophagusState.OPENED
		did_open = true

		if trap_type != "NONE" and not trap_disarmed:
			did_trap = true
			var trap_damage = 25 if trap_type == "POISON_DARTS" else 15
			trap_triggered.emit(sarcophagus_id, trap_type, trap_damage)

		sarcophagus_opened.emit(sarcophagus_id, relics)

	return {
		"state": state,
		"progress": prying_progress,
		"opened": did_open,
		"trap_triggered": did_trap
	}

func loot_relics() -> Array[Dictionary]:
	if state == SarcophagusState.OPENED:
		state = SarcophagusState.LOOTED
		var looted_items = relics.duplicate()
		relics.clear()
		return looted_items
	return []
