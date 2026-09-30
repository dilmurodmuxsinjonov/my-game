# scripts/combat/tournament_manager.gd
# Voxel Lord: Feudal Realm - Milestone 50: Grand Feudal Jousting Tournament & Chivalric Knighthood
# Coordinates knightly tournament disciplines (Joust, Foot Melee, Archery Contest, Champion Duel),
# arena grandstand wagers, chivalric knighthood feats, and realm feasts.

class_name TournamentManager
extends Node

signal discipline_started(discipline: String, participant: String, opponent: String)
signal joust_pass_completed(pass_num: int, player_pts: int, opp_pts: int, player_unhorsed: bool, opp_unhorsed: bool)
signal melee_round_completed(round_num: int, winner: String, player_hp: float, opp_hp: float)
signal archery_shot_recorded(shot_num: int, distance: float, wind: float, score: int)
signal tournament_victorious(discipline: String, victor: String, prize_gold: int, honor_awarded: int)
signal wager_placed(wager_id: String, champion_id: String, amount: int, potential_payout: int)
signal wager_resolved(wager_id: String, won: bool, payout: int)
signal chivalric_title_unlocked(title: String, honor: int)
signal grand_feast_hosted(morale_boost: float, guests_count: int)

enum DisciplineType {
	JOUST,
	MELEE,
	ARCHERY,
	CHAMPION_DUEL
}

# Grand Tournament AI Champions Roster
var champions: Dictionary = {}

# Active Match State
var active_discipline: String = ""
var current_match: Dictionary = {}

# Chivalry, Honor & Titles
var chivalric_honor: int = 0
var current_title: String = "Page of the Realm"
var unlocked_titles: Array[String] = ["Page of the Realm"]

# Tournament History & Statistics
var total_tournaments_won: int = 0
var total_jousts_won: int = 0
var total_melees_won: int = 0
var total_archery_won: int = 0
var total_duels_won: int = 0
var grand_feasts_hosted: int = 0

# Arena Grandstand & Active Wagers
var grandstand_excitement: float = 75.0 # 0.0 to 100.0%
var active_wagers: Array[Dictionary] = []
var completed_wagers: Array[Dictionary] = []

# Title thresholds
const TITLE_THRESHOLDS: Array[Dictionary] = [
	{"honor": 0, "title": "Page of the Realm", "icon": "🛡️"},
	{"honor": 100, "title": "Squire of the High Seat", "icon": "🗡️"},
	{"honor": 250, "title": "Knight of the Gilded Spur", "icon": "⚔️"},
	{"honor": 500, "title": "Knight Banneret of the Crown", "icon": "🚩"},
	{"honor": 1000, "title": "Grandmaster of Chivalry & Sovereign Defender", "icon": "👑"}
]

func _init() -> void:
	init_default_champions()

func init_default_champions() -> void:
	champions = {
		"sir_roland": {
			"id": "sir_roland",
			"name": "Sir Roland the Ironclad",
			"realm": "Kingdom of Valoria",
			"title": "The Unyielding Bulwark",
			"joust_skill": 90,
			"melee_skill": 92,
			"archery_skill": 45,
			"chivalry": 95,
			"odds": 1.75,
			"icon": "🛡️"
		},
		"lady_gwendolyn": {
			"id": "lady_gwendolyn",
			"name": "Lady Gwendolyn the Swift",
			"realm": "Barony of Silvercoast",
			"title": "The Silver Falcon",
			"joust_skill": 82,
			"melee_skill": 75,
			"archery_skill": 96,
			"chivalry": 90,
			"odds": 2.10,
			"icon": "🏹"
		},
		"lord_valerie": {
			"id": "lord_valerie",
			"name": "Lord Valerie the Falcon",
			"realm": "Duchy of Ashfell",
			"title": "The Azure Knight",
			"joust_skill": 86,
			"melee_skill": 80,
			"archery_skill": 70,
			"chivalry": 80,
			"odds": 2.25,
			"icon": "🦅"
		},
		"brother_bartholomew": {
			"id": "brother_bartholomew",
			"name": "Brother Bartholomew the Steadfast",
			"realm": "Sunken Mire Monastic Order",
			"title": "The Resolute Templar",
			"joust_skill": 70,
			"melee_skill": 88,
			"archery_skill": 55,
			"chivalry": 98,
			"odds": 2.50,
			"icon": "✝️"
		},
		"prince_alden": {
			"id": "prince_alden",
			"name": "Prince Alden of Valoria",
			"realm": "Crown Prince of the High Realm",
			"title": "Grand Sovereign Champion",
			"joust_skill": 94,
			"melee_skill": 90,
			"archery_skill": 88,
			"chivalry": 92,
			"odds": 1.50,
			"icon": "👑"
		}
	}

# ---------------------------------------------------------
# Discipline 1: Royal Joust of Peace (Lance Tilt Mechanics)
# ---------------------------------------------------------
func start_joust_match(opponent_id: String = "sir_roland") -> Dictionary:
	var opp = champions.get(opponent_id, champions["sir_roland"])
	active_discipline = "joust"
	current_match = {
		"discipline": "joust",
		"opponent_id": opponent_id,
		"opponent_name": opp.get("name", "Sir Roland"),
		"current_pass": 1,
		"max_passes": 3,
		"player_score": 0,
		"opponent_score": 0,
		"player_unhorsed": false,
		"opponent_unhorsed": false,
		"is_finished": false,
		"history": []
	}
	discipline_started.emit("joust", "Monarch", opp.get("name", "Opponent"))
	return current_match

func execute_joust_pass(target_zone: String = "shield", timing_factor: float = 0.85) -> Dictionary:
	if active_discipline != "joust" or current_match.is_empty() or current_match.get("is_finished", false):
		return {"error": "No active joust match"}

	var opp = champions.get(current_match["opponent_id"], champions["sir_roland"])
	var opp_skill = float(opp.get("joust_skill", 80))
	var pass_num = current_match["current_pass"]

	# Target mechanics:
	# "helm": High difficulty, 40% unhorsing chance on good timing, 3 points.
	# "shield": Standard chivalric tilt target, 75% clean lance break, 2 points.
	# "breastplate": Solid core impact, 30% unhorsing chance, 1 point.
	var hit_success = timing_factor >= 0.40
	var clean_lance_break = false
	var opp_unhorsed = false
	var player_pts = 0

	if hit_success:
		match target_zone:
			"helm":
				if timing_factor >= 0.70:
					player_pts = 3
					clean_lance_break = true
					if timing_factor >= 0.85 or randf() < 0.45:
						opp_unhorsed = true
				else:
					player_pts = 1
			"shield":
				player_pts = 2
				clean_lance_break = (timing_factor >= 0.50)
				if timing_factor >= 0.90:
					opp_unhorsed = true
			"breastplate":
				player_pts = 1
				clean_lance_break = true
				if timing_factor >= 0.80 and randf() < 0.35:
					opp_unhorsed = true
			_:
				player_pts = 1

	# Opponent lance tilt AI calculation
	var opp_roll = randf() * 100.0 + (opp_skill * 0.2)
	var opp_pts = 0
	var player_unhorsed = false

	if opp_roll >= 70.0:
		opp_pts = 2
		if opp_roll >= 110.0 and timing_factor < 0.60:
			player_unhorsed = true
	elif opp_roll >= 40.0:
		opp_pts = 1

	current_match["player_score"] += player_pts
	current_match["opponent_score"] += opp_pts

	var pass_record = {
		"pass": pass_num,
		"target": target_zone,
		"timing": timing_factor,
		"player_pts": player_pts,
		"opp_pts": opp_pts,
		"clean_break": clean_lance_break,
		"opp_unhorsed": opp_unhorsed,
		"player_unhorsed": player_unhorsed
	}
	current_match["history"].append(pass_record)

	joust_pass_completed.emit(pass_num, player_pts, opp_pts, player_unhorsed, opp_unhorsed)

	# Check match conclusion
	if opp_unhorsed or player_unhorsed or pass_num >= current_match["max_passes"]:
		current_match["is_finished"] = true
		var player_won = false
		if opp_unhorsed and not player_unhorsed:
			player_won = true
		elif player_unhorsed and not opp_unhorsed:
			player_won = false
		else:
			player_won = current_match["player_score"] > current_match["opponent_score"]

		var victor = "Monarch" if player_won else current_match["opponent_name"]
		var prize = 75 if player_won else 15
		var honor_gain = 35 if player_won else 10
		if opp_unhorsed:
			honor_gain += 25 # Spectacular unhorsing chivalric bonus!

		if player_won:
			total_jousts_won += 1
			total_tournaments_won += 1
			add_chivalric_honor(honor_gain)

		_resolve_wagers_for_match(victor, current_match["opponent_id"])
		tournament_victorious.emit("joust", victor, prize, honor_gain if player_won else 0)

	else:
		current_match["current_pass"] += 1

	return pass_record

# ---------------------------------------------------------
# Discipline 2: Grand Foot Melee (Arena Steel Clash)
# ---------------------------------------------------------
func start_melee_match(opponent_id: String = "brother_bartholomew") -> Dictionary:
	var opp = champions.get(opponent_id, champions["brother_bartholomew"])
	active_discipline = "melee"
	current_match = {
		"discipline": "melee",
		"opponent_id": opponent_id,
		"opponent_name": opp.get("name", "Bartholomew"),
		"round": 1,
		"player_hp": 100.0,
		"opponent_hp": 100.0,
		"player_stamina": 100.0,
		"opponent_stamina": 100.0,
		"is_finished": false,
		"rounds_won_player": 0,
		"rounds_won_opp": 0
	}
	discipline_started.emit("melee", "Monarch", opp.get("name", "Opponent"))
	return current_match

func execute_melee_action(action: String = "strike") -> Dictionary:
	if active_discipline != "melee" or current_match.is_empty() or current_match.get("is_finished", false):
		return {"error": "No active melee match"}

	var opp = champions.get(current_match["opponent_id"], champions["brother_bartholomew"])
	var opp_skill = float(opp.get("melee_skill", 80))

	var player_dmg = 0.0
	var opp_dmg = 0.0
	var stam_cost = 15.0

	match action:
		"strike":
			player_dmg = 20.0 + randf_range(2.0, 8.0)
			stam_cost = 12.0
		"heavy_cleave":
			player_dmg = 35.0 + randf_range(5.0, 15.0)
			stam_cost = 25.0
		"parry":
			player_dmg = 10.0
			stam_cost = 8.0
		"shield_bash":
			player_dmg = 18.0 + randf_range(1.0, 5.0)
			stam_cost = 18.0
		_:
			player_dmg = 15.0

	# Opponent action & counter-strike
	var opp_roll = randf() * 100.0 + (opp_skill * 0.15)
	if action == "parry":
		opp_dmg = 5.0 # Greatly reduced damage on parry
	elif opp_roll >= 75.0:
		opp_dmg = 22.0 + randf_range(3.0, 10.0)
	elif opp_roll >= 40.0:
		opp_dmg = 14.0 + randf_range(1.0, 6.0)
	else:
		opp_dmg = 8.0

	current_match["opponent_hp"] = maxf(0.0, current_match["opponent_hp"] - player_dmg)
	current_match["player_hp"] = maxf(0.0, current_match["player_hp"] - opp_dmg)
	current_match["player_stamina"] = maxf(0.0, current_match["player_stamina"] - stam_cost + 5.0)

	var winner = ""
	if current_match["opponent_hp"] <= 0.0 or current_match["player_hp"] <= 0.0:
		current_match["is_finished"] = true
		var player_won = current_match["opponent_hp"] <= 0.0 and current_match["player_hp"] > 0.0
		winner = "Monarch" if player_won else current_match["opponent_name"]

		var prize = 80 if player_won else 20
		var honor_gain = 40 if player_won else 10
		if player_won:
			total_melees_won += 1
			total_tournaments_won += 1
			add_chivalric_honor(honor_gain)

		_resolve_wagers_for_match(winner, current_match["opponent_id"])
		tournament_victorious.emit("melee", winner, prize, honor_gain if player_won else 0)
	else:
		current_match["round"] += 1

	melee_round_completed.emit(current_match["round"], winner, current_match["player_hp"], current_match["opponent_hp"])

	return {
		"action": action,
		"player_damage": player_dmg,
		"opp_damage": opp_dmg,
		"player_hp": current_match["player_hp"],
		"opponent_hp": current_match["opponent_hp"],
		"is_finished": current_match["is_finished"]
	}

# ---------------------------------------------------------
# Discipline 3: Archery Guild Marksman Contest
# ---------------------------------------------------------
func start_archery_contest(opponent_id: String = "lady_gwendolyn") -> Dictionary:
	var opp = champions.get(opponent_id, champions["lady_gwendolyn"])
	active_discipline = "archery"
	current_match = {
		"discipline": "archery",
		"opponent_id": opponent_id,
		"opponent_name": opp.get("name", "Lady Gwendolyn"),
		"current_shot": 1,
		"max_shots": 3,
		"player_total_score": 0,
		"opp_total_score": 0,
		"current_distance": 30.0, # 30m, 50m, 70m
		"current_wind": randf_range(-4.0, 4.0),
		"history": [],
		"is_finished": false
	}
	discipline_started.emit("archery", "Monarch", opp.get("name", "Opponent"))
	return current_match

func shoot_archery_arrow(aim_elevation: float = 0.0, wind_compensation: float = 0.0) -> Dictionary:
	if active_discipline != "archery" or current_match.is_empty() or current_match.get("is_finished", false):
		return {"error": "No active archery contest"}

	var shot_num = current_match["current_shot"]
	var dist = current_match["current_distance"]
	var wind = current_match["current_wind"]
	var opp = champions.get(current_match["opponent_id"], champions["lady_gwendolyn"])
	var opp_archery_skill = float(opp.get("archery_skill", 85))

	# Player shot score calculation
	var wind_err = absf(wind - wind_compensation)
	var elev_err = absf(aim_elevation - (dist * 0.05)) # Target elevation arc

	var total_deviation = wind_err * 1.5 + elev_err * 2.0
	var player_score = 0
	if total_deviation < 1.0:
		player_score = 10 # Bullseye!
	elif total_deviation < 2.5:
		player_score = 7 # Inner Ring
	elif total_deviation < 4.5:
		player_score = 5 # Middle Ring
	elif total_deviation < 7.0:
		player_score = 2 # Outer Ring
	else:
		player_score = 0 # Complete Miss

	# Opponent shot calculation
	var opp_err = randf_range(0.5, 4.0) * (100.0 / maxf(1.0, opp_archery_skill))
	var opp_score = 0
	if opp_err < 1.2:
		opp_score = 10
	elif opp_err < 2.8:
		opp_score = 7
	elif opp_err < 5.0:
		opp_score = 5
	else:
		opp_score = 2

	current_match["player_total_score"] += player_score
	current_match["opp_total_score"] += opp_score

	var record = {
		"shot": shot_num,
		"distance": dist,
		"wind": wind,
		"player_score": player_score,
		"opp_score": opp_score
	}
	current_match["history"].append(record)

	archery_shot_recorded.emit(shot_num, dist, wind, player_score)

	if shot_num >= current_match["max_shots"]:
		current_match["is_finished"] = true
		var player_won = current_match["player_total_score"] >= current_match["opp_total_score"]
		var victor = "Monarch" if player_won else current_match["opponent_name"]
		var prize = 60 if player_won else 15
		var honor = 30 if player_won else 10

		if player_won:
			total_archery_won += 1
			total_tournaments_won += 1
			add_chivalric_honor(honor)

		_resolve_wagers_for_match(victor, current_match["opponent_id"])
		tournament_victorious.emit("archery", victor, prize, honor if player_won else 0)
	else:
		current_match["current_shot"] += 1
		# Next round distance progression (30m -> 50m -> 70m)
		current_match["current_distance"] += 20.0
		current_match["current_wind"] = randf_range(-5.0, 5.0)

	return record

# ---------------------------------------------------------
# Discipline 4: Duel of Sovereign Champions (Boss Duel)
# ---------------------------------------------------------
func start_champion_duel(opponent_id: String = "prince_alden") -> Dictionary:
	var opp = champions.get(opponent_id, champions["prince_alden"])
	active_discipline = "champion_duel"
	current_match = {
		"discipline": "champion_duel",
		"opponent_id": opponent_id,
		"opponent_name": opp.get("name", "Prince Alden"),
		"player_hp": 120.0,
		"opponent_hp": 150.0,
		"turn": 1,
		"is_finished": false
	}
	discipline_started.emit("champion_duel", "Monarch", opp.get("name", "Opponent"))
	return current_match

func execute_duel_gambit(gambit_type: String = "feint_and_thrust") -> Dictionary:
	if active_discipline != "champion_duel" or current_match.is_empty() or current_match.get("is_finished", false):
		return {"error": "No active champion duel"}

	var p_dmg = 0.0
	var o_dmg = 0.0

	match gambit_type:
		"feint_and_thrust":
			p_dmg = 32.0 + randf_range(2.0, 10.0)
			o_dmg = 18.0 + randf_range(0.0, 6.0)
		"riposte_counter":
			p_dmg = 45.0 + randf_range(5.0, 15.0)
			o_dmg = 8.0 # High payoff counter
		"defensive_guard":
			p_dmg = 12.0
			o_dmg = 4.0 # Solid defense
		_:
			p_dmg = 20.0
			o_dmg = 15.0

	current_match["opponent_hp"] = maxf(0.0, current_match["opponent_hp"] - p_dmg)
	current_match["player_hp"] = maxf(0.0, current_match["player_hp"] - o_dmg)

	var victor = ""
	if current_match["opponent_hp"] <= 0.0 or current_match["player_hp"] <= 0.0:
		current_match["is_finished"] = true
		var player_won = current_match["opponent_hp"] <= 0.0 and current_match["player_hp"] > 0.0
		victor = "Monarch" if player_won else current_match["opponent_name"]
		var prize = 150 if player_won else 30
		var honor = 60 if player_won else 15

		if player_won:
			total_duels_won += 1
			total_tournaments_won += 1
			add_chivalric_honor(honor)

		_resolve_wagers_for_match(victor, current_match["opponent_id"])
		tournament_victorious.emit("champion_duel", victor, prize, honor if player_won else 0)
	else:
		current_match["turn"] += 1

	return {
		"gambit": gambit_type,
		"player_damage": p_dmg,
		"opponent_damage": o_dmg,
		"player_hp": current_match["player_hp"],
		"opponent_hp": current_match["opponent_hp"],
		"is_finished": current_match["is_finished"]
	}

# ---------------------------------------------------------
# Arena Grandstand & Wager System
# ---------------------------------------------------------
func place_wager(champion_id: String, amount: int) -> Dictionary:
	var champ = champions.get(champion_id)
	if not champ:
		return {"success": false, "reason": "Unknown champion"}

	if amount <= 0:
		return {"success": false, "reason": "Invalid amount"}

	var odds = float(champ.get("odds", 2.0))
	var potential_payout = int(amount * odds)
	var wager_id = "wager_%d" % (active_wagers.size() + completed_wagers.size() + 1)

	var wager = {
		"id": wager_id,
		"champion_id": champion_id,
		"champion_name": champ.get("name", champion_id),
		"amount": amount,
		"odds": odds,
		"potential_payout": potential_payout,
		"status": "pending"
	}
	active_wagers.append(wager)
	wager_placed.emit(wager_id, champion_id, amount, potential_payout)
	return {"success": true, "wager": wager}

func _resolve_wagers_for_match(victor_name: String, opp_id: String) -> void:
	var remaining: Array[Dictionary] = []
	for w in active_wagers:
		var won = false
		if victor_name == "Monarch" and w["champion_id"] == "monarch":
			won = true
		elif w["champion_id"] == opp_id and victor_name == w["champion_name"]:
			won = true

		w["status"] = "won" if won else "lost"
		var payout = w["potential_payout"] if won else 0
		w["payout"] = payout
		completed_wagers.append(w)
		wager_resolved.emit(w["id"], won, payout)
	active_wagers.clear()

# ---------------------------------------------------------
# Chivalric Honor & Knighthood Feats
# ---------------------------------------------------------
func add_chivalric_honor(amount: int) -> void:
	chivalric_honor += amount
	_check_title_promotion()

func _check_title_promotion() -> void:
	for entry in TITLE_THRESHOLDS:
		if chivalric_honor >= entry["honor"] and not unlocked_titles.has(entry["title"]):
			unlocked_titles.append(entry["title"])
			current_title = entry["title"]
			chivalric_title_unlocked.emit(entry["title"], chivalric_honor)

# ---------------------------------------------------------
# Grand Feudal Realm Feast (Banquet of the Realm)
# ---------------------------------------------------------
func host_grand_feast(supply_chain: SupplyChain = null) -> Dictionary:
	var bread_cost = 15
	var gold_cost = 25

	if supply_chain:
		if supply_chain.get_resource("bread") < bread_cost:
			return {"success": false, "reason": "Insufficient bread for grand banquet (Requires %d Bread)" % bread_cost}
		if supply_chain.get_resource("gold_coins") < gold_cost:
			return {"success": false, "reason": "Insufficient gold for feast heralds (Requires %d Gold)" % gold_cost}

		supply_chain.consume_resource("bread", bread_cost)
		supply_chain.consume_resource("gold_coins", gold_cost)

	grand_feasts_hosted += 1
	var morale_boost = 25.0
	var guests = 45 + randi() % 20

	add_chivalric_honor(100) # Hosting lavish feast awards 100 chivalric honor!
	grandstand_excitement = minf(100.0, grandstand_excitement + 20.0)

	grand_feast_hosted.emit(morale_boost, guests)
	return {
		"success": true,
		"morale_boost": morale_boost,
		"guests_count": guests,
		"honor_awarded": 100
	}

# ---------------------------------------------------------
# Serialization / Deserialization (Save System Integration)
# ---------------------------------------------------------
func to_dict() -> Dictionary:
	return {
		"chivalric_honor": chivalric_honor,
		"current_title": current_title,
		"unlocked_titles": unlocked_titles,
		"total_tournaments_won": total_tournaments_won,
		"total_jousts_won": total_jousts_won,
		"total_melees_won": total_melees_won,
		"total_archery_won": total_archery_won,
		"total_duels_won": total_duels_won,
		"grand_feasts_hosted": grand_feasts_hosted,
		"grandstand_excitement": grandstand_excitement,
		"active_wagers": active_wagers,
		"completed_wagers": completed_wagers
	}

func from_dict(data: Dictionary) -> void:
	if data.is_empty():
		return
	chivalric_honor = data.get("chivalric_honor", 0)
	current_title = data.get("current_title", "Page of the Realm")
	if data.has("unlocked_titles"):
		unlocked_titles.clear()
		for t in data["unlocked_titles"]:
			unlocked_titles.append(str(t))
	total_tournaments_won = data.get("total_tournaments_won", 0)
	total_jousts_won = data.get("total_jousts_won", 0)
	total_melees_won = data.get("total_melees_won", 0)
	total_archery_won = data.get("total_archery_won", 0)
	total_duels_won = data.get("total_duels_won", 0)
	grand_feasts_hosted = data.get("grand_feasts_hosted", 0)
	grandstand_excitement = data.get("grandstand_excitement", 75.0)
	if data.has("active_wagers"):
		active_wagers.clear()
		for w in data["active_wagers"]:
			active_wagers.append(w)
	if data.has("completed_wagers"):
		completed_wagers.clear()
		for cw in data["completed_wagers"]:
			completed_wagers.append(cw)
