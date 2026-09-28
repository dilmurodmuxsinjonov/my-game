# scripts/quests/quest_manager.gd
# Voxel Lord: Feudal Realm - Milestone 45: Feudal Quest & Progression Ledger
# Manages historical monarch questlines, objective validation, feudal renown,
# and royal victory coronation.

class_name QuestManager
extends Node

signal quest_started(quest_id: String, title: String)
signal objective_progress_updated(quest_id: String, obj_index: int, current: int, required: int)
signal quest_completed(quest_id: String, title: String, reward_renown: int)
signal monarch_title_promoted(new_title: String, total_renown: int)
signal realm_victory_achieved(total_renown: int)

enum QuestStatus {
	LOCKED,
	ACTIVE,
	COMPLETED
}

const MONARCH_TITLES: Array[Dictionary] = [
	{"threshold": 0, "title": "Exiled Monarch"},
	{"threshold": 100, "title": "Lord of the Frontier"},
	{"threshold": 350, "title": "Baron of the Realm"},
	{"threshold": 800, "title": "Count of the Trade Lands"},
	{"threshold": 1500, "title": "Duke of High Metallurgy"},
	{"threshold": 2500, "title": "Sovereign King of the Feudal Realm"}
]

var total_renown: int = 0
var current_title_index: int = 0
var is_victory_achieved: bool = false

# Master Quest Catalog
var quests: Dictionary = {
	"quest_1_foundations": {
		"id": "quest_1_foundations",
		"title": "I. Foundations of the Realm",
		"description": "Establish a foothold in the wilderness. Gather timber and stone, and kindle a communal hearth.",
		"reward_renown": 100,
		"status": QuestStatus.ACTIVE,
		"objectives": [
			{"desc": "Harvest Wood Voxels", "key": "harvest_wood", "current": 0, "required": 10},
			{"desc": "Mine Stone or Cobblestone", "key": "mine_stone", "current": 0, "required": 10},
			{"desc": "Reassign a Citizen Duty", "key": "reassign_citizen", "current": 0, "required": 1}
		]
	},
	"quest_2_bread_and_iron": {
		"id": "quest_2_bread_and_iron",
		"title": "II. Bread & Iron",
		"description": "Sustain your subjects with agriculture and unlock metallurgy at the bloomery furnace.",
		"reward_renown": 250,
		"status": QuestStatus.LOCKED,
		"objectives": [
			{"desc": "Till Farmland Plots", "key": "till_farmland", "current": 0, "required": 4},
			{"desc": "Harvest Matured Wheat", "key": "harvest_wheat", "current": 0, "required": 4},
			{"desc": "Smelt Raw Ore at Furnace", "key": "smelt_ore", "current": 0, "required": 3}
		]
	},
	"quest_3_steam_industry": {
		"id": "quest_3_steam_industry",
		"title": "III. High-Pressure Industry",
		"description": "Inspect the Steam & Forge quarter and ignite the industrial blast furnace.",
		"reward_renown": 450,
		"status": QuestStatus.LOCKED,
		"objectives": [
			{"desc": "Travel to Steam & Forge Quarter", "key": "visit_steam_district", "current": 0, "required": 1},
			{"desc": "Stoke Furnace Firebox", "key": "stoke_furnace", "current": 0, "required": 1},
			{"desc": "Craft Iron or Steel Component", "key": "craft_iron_item", "current": 0, "required": 2}
		]
	},
	"quest_4_maritime_fleet": {
		"id": "quest_4_maritime_fleet",
		"title": "IV. Maritime Trade Fleet",
		"description": "Expand commerce to distant shores through the docks and trade caravans.",
		"reward_renown": 700,
		"status": QuestStatus.LOCKED,
		"objectives": [
			{"desc": "Visit Maritime Harbor & Docks", "key": "visit_harbor_district", "current": 0, "required": 1},
			{"desc": "Trade with Exotic Caravan", "key": "caravan_trade", "current": 0, "required": 1},
			{"desc": "Inspect Fluyt Cargo Ship", "key": "inspect_ship", "current": 0, "required": 1}
		]
	},
	"quest_5_clockwork_astronomy": {
		"id": "quest_5_clockwork_astronomy",
		"title": "V. Renaissance Clockwork",
		"description": "Unlock celestial knowledge and precision clockwork at the high observatory.",
		"reward_renown": 1000,
		"status": QuestStatus.LOCKED,
		"objectives": [
			{"desc": "Ascend to Clockwork Observatory", "key": "visit_observatory", "current": 0, "required": 1},
			{"desc": "Inspect Prague Astronomical Clock", "key": "inspect_clock", "current": 0, "required": 1},
			{"desc": "Explore Subterranean Mining Rail", "key": "visit_mining_district", "current": 0, "required": 1}
		]
	},
	"quest_6_sovereign_coronation": {
		"id": "quest_6_sovereign_coronation",
		"title": "VI. The Sovereign Coronation",
		"description": "Defend the realm against bandit incursions, rally your militia, and claim sovereign kingship.",
		"reward_renown": 1500,
		"status": QuestStatus.LOCKED,
		"objectives": [
			{"desc": "Sound the Royal War Horn", "key": "sound_war_horn", "current": 0, "required": 1},
			{"desc": "Repel Frontier Bandit Threat", "key": "repel_bandit", "current": 0, "required": 1},
			{"desc": "Amass 2,500 Total Renown", "key": "accumulate_renown", "current": 0, "required": 1}
		]
	}
}

var active_quest_id: String = "quest_1_foundations"

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_update_title()

func get_active_quest() -> Dictionary:
	if quests.has(active_quest_id):
		return quests[active_quest_id]
	return {}

func get_all_quests() -> Array[Dictionary]:
	var list: Array[Dictionary] = []
	for qid in ["quest_1_foundations", "quest_2_bread_and_iron", "quest_3_steam_industry",
				"quest_4_maritime_fleet", "quest_5_clockwork_astronomy", "quest_6_sovereign_coronation"]:
		if quests.has(qid):
			list.append(quests[qid])
	return list

func record_progress(objective_key: String, count: int = 1) -> void:
	if not quests.has(active_quest_id):
		return

	var q = quests[active_quest_id]
	if q["status"] != QuestStatus.ACTIVE:
		return

	var all_completed = true
	var idx = 0
	for obj in q["objectives"]:
		if obj["key"] == objective_key:
			obj["current"] = mini(obj["required"], obj["current"] + count)
			objective_progress_updated.emit(active_quest_id, idx, obj["current"], obj["required"])

		if obj["current"] < obj["required"]:
			all_completed = false
		idx += 1

	if all_completed:
		_complete_active_quest()

func _complete_active_quest() -> void:
	var q = quests[active_quest_id]
	q["status"] = QuestStatus.COMPLETED
	var reward = q.get("reward_renown", 100)
	total_renown += reward
	quest_completed.emit(active_quest_id, q["title"], reward)
	_update_title()

	# Advance to next quest
	var next_map = {
		"quest_1_foundations": "quest_2_bread_and_iron",
		"quest_2_bread_and_iron": "quest_3_steam_industry",
		"quest_3_steam_industry": "quest_4_maritime_fleet",
		"quest_4_maritime_fleet": "quest_5_clockwork_astronomy",
		"quest_5_clockwork_astronomy": "quest_6_sovereign_coronation"
	}

	if next_map.has(active_quest_id):
		active_quest_id = next_map[active_quest_id]
		var next_q = quests[active_quest_id]
		next_q["status"] = QuestStatus.ACTIVE
		quest_started.emit(active_quest_id, next_q["title"])
	else:
		# Final victory condition met!
		if not is_victory_achieved:
			is_victory_achieved = true
			realm_victory_achieved.emit(total_renown)

func _update_title() -> void:
	var best_title = MONARCH_TITLES[0]["title"]
	var best_idx = 0
	for i in range(MONARCH_TITLES.size()):
		var entry = MONARCH_TITLES[i]
		if total_renown >= entry["threshold"]:
			best_title = entry["title"]
			best_idx = i

	if best_idx > current_title_index:
		current_title_index = best_idx
		monarch_title_promoted.emit(best_title, total_renown)

func get_monarch_title() -> String:
	return MONARCH_TITLES[current_title_index]["title"]

func get_quest_summary_text() -> String:
	var q = get_active_quest()
	if q.is_empty():
		return "All Feudal Deeds Complete - Sovereign Victorious!"
	var text = "[%s]\n" % q["title"]
	for obj in q["objectives"]:
		var check = "✓" if obj["current"] >= obj["required"] else "○"
		text += " %s %s: (%d/%d)\n" % [check, obj["desc"], obj["current"], obj["required"]]
	return text.strip_edges()
