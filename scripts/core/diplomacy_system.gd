# scripts/core/diplomacy_system.gd
# Voxel Lord: Feudal Realm - Milestone 48: Kingdom Diplomacy & Vassal Tribute System
# Manages foreign realms, diplomatic opinions, feudal treaties, emissary caravans,
# tribute demands, and vassalage relationships.

class_name DiplomacySystem
extends Node

enum RelationshipStatus {
	WAR,        # opinion <= -40 (Raids, hostilities, embargo)
	HOSTILE,    # -40 < opinion <= -10 (Tense, no trade)
	NEUTRAL,    # -10 < opinion <= 29 (Basic trade allowed)
	FRIENDLY,   # 30 <= opinion <= 69 (Open commerce, gift bonuses)
	ALLIED,     # 70 <= opinion <= 90 (Defensive military pact, joint defense)
	VASSAL      # opinion >= 91 or vassalage sworn (Periodic tribute delivery)
}

enum TreatyType {
	NON_AGGRESSION,      # No raids for duration (300s)
	TRADE_CONCORDAT,     # Passive trade income (+15% trade bonus, +0.05 opinion/sec)
	DEFENSIVE_LEAGUE,    # Military reinforcement during attacks
	VASSALAGE_CHARTER    # Periodic tribute payments and feudal fealty
}

signal opinion_changed(faction_id: String, old_val: float, new_val: float, status: RelationshipStatus)
signal treaty_signed(faction_id: String, treaty_type: TreatyType)
signal treaty_broken(faction_id: String, treaty_type: TreatyType, penalty: float)
signal war_declared(faction_id: String, aggressor_is_player: bool)
signal peace_concluded(faction_id: String)
signal tribute_received(faction_id: String, resources: Dictionary)
signal tribute_demanded(faction_id: String, resources: Dictionary, accepted: bool)
signal emissary_arrived(faction_id: String, emissary_event: Dictionary)

# Factions Registry
var factions: Dictionary = {}

# Emissary Event cooldowns
var emissary_timer: float = 0.0
const EMISSARY_INTERVAL: float = 120.0 # An emissary arrives every 2 minutes

func _init() -> void:
	init_default_factions()

func init_default_factions() -> void:
	factions = {
		"valoria": {
			"id": "valoria",
			"name": "Duchy of Valoria",
			"ruler": "Grand Duke Alden IV",
			"archetype": "Feudal Martial",
			"icon": "🛡️",
			"banner_color": "#3a5ba0",
			"opinion": 15.0,
			"base_opinion": 15.0,
			"military_strength": 180.0,
			"economic_wealth": 240.0,
			"demands": "food",
			"offers": "iron_ingots",
			"is_vassal": false,
			"vassal_tribute_timer": 0.0,
			"vassal_tribute_interval": 90.0,
			"active_treaties": {}, # TreatyType -> remaining_seconds
			"last_gift_time": 0.0,
			"tribute_package": {"iron_ingots": 6, "gold_coins": 20, "tools": 3}
		},
		"silvercoast": {
			"id": "silvercoast",
			"name": "Silvercoast Trade League",
			"ruler": "High Doge Lorenzo",
			"archetype": "Mercantile Guild",
			"icon": "⛵",
			"banner_color": "#d4af37",
			"opinion": 10.0,
			"base_opinion": 10.0,
			"military_strength": 110.0,
			"economic_wealth": 500.0,
			"demands": "timber",
			"offers": "gold_coins",
			"is_vassal": false,
			"vassal_tribute_timer": 0.0,
			"vassal_tribute_interval": 80.0,
			"active_treaties": {},
			"last_gift_time": 0.0,
			"tribute_package": {"gold_coins": 50, "luxury_wine": 2, "salt": 8}
		},
		"ashfell": {
			"id": "ashfell",
			"name": "Ashfell Mountain Clans",
			"ruler": "Chieftain Torvold Ironfang",
			"archetype": "Raider Confederation",
			"icon": "⚔️",
			"banner_color": "#8b0000",
			"opinion": -25.0,
			"base_opinion": -25.0,
			"military_strength": 160.0,
			"economic_wealth": 140.0,
			"demands": "beer",
			"offers": "stone",
			"is_vassal": false,
			"vassal_tribute_timer": 0.0,
			"vassal_tribute_interval": 100.0,
			"active_treaties": {},
			"last_gift_time": 0.0,
			"tribute_package": {"stone": 25, "iron_ore": 12, "gold_coins": 15}
		},
		"sunken_mire": {
			"id": "sunken_mire",
			"name": "Barony of the Sunken Mire",
			"ruler": "Baroness Elspeth the Recluse",
			"archetype": "Agrarian Isolationist",
			"icon": "🌿",
			"banner_color": "#2e8b57",
			"opinion": 0.0,
			"base_opinion": 0.0,
			"military_strength": 90.0,
			"economic_wealth": 200.0,
			"demands": "tools",
			"offers": "medicine",
			"is_vassal": false,
			"vassal_tribute_timer": 0.0,
			"vassal_tribute_interval": 90.0,
			"active_treaties": {},
			"last_gift_time": 0.0,
			"tribute_package": {"medicine": 5, "herbs": 15, "food": 20}
		}
	}

func get_faction(faction_id: String) -> Dictionary:
	return factions.get(faction_id, {})

func get_all_factions() -> Dictionary:
	return factions

func get_relationship_status(faction_id: String) -> RelationshipStatus:
	var f = get_faction(faction_id)
	if f.is_empty():
		return RelationshipStatus.NEUTRAL
	
	if f.get("is_vassal", false):
		return RelationshipStatus.VASSAL

	var op = f.get("opinion", 0.0)
	if op <= -40.0:
		return RelationshipStatus.WAR
	elif op <= -10.0:
		return RelationshipStatus.HOSTILE
	elif op <= 29.0:
		return RelationshipStatus.NEUTRAL
	elif op <= 69.0:
		return RelationshipStatus.FRIENDLY
	elif op <= 90.0:
		return RelationshipStatus.ALLIED
	else:
		return RelationshipStatus.VASSAL

func get_status_name(status: RelationshipStatus) -> String:
	match status:
		RelationshipStatus.WAR:
			return "War ⚔️"
		RelationshipStatus.HOSTILE:
			return "Hostile ⚠️"
		RelationshipStatus.NEUTRAL:
			return "Neutral ⚖️"
		RelationshipStatus.FRIENDLY:
			return "Friendly 🕊️"
		RelationshipStatus.ALLIED:
			return "Allied 🛡️"
		RelationshipStatus.VASSAL:
			return "Vassal Fealty 👑"
		_:
			return "Unknown"

func get_treaty_name(treaty_type: TreatyType) -> String:
	match treaty_type:
		TreatyType.NON_AGGRESSION:
			return "Non-Aggression Pact"
		TreatyType.TRADE_CONCORDAT:
			return "Trade Concordat"
		TreatyType.DEFENSIVE_LEAGUE:
			return "Defensive Military League"
		TreatyType.VASSALAGE_CHARTER:
			return "Vassalage Fealty Charter"
		_:
			return "Unknown Treaty"

func modify_opinion(faction_id: String, delta: float, reason: String = "") -> float:
	if not factions.has(faction_id):
		return 0.0
	
	var old_val: float = factions[faction_id]["opinion"]
	var new_val: float = clampf(old_val + delta, -100.0, 100.0)
	factions[faction_id]["opinion"] = new_val
	
	var new_status = get_relationship_status(faction_id)
	emit_signal("opinion_changed", faction_id, old_val, new_val, new_status)
	return new_val

func can_sign_treaty(faction_id: String, treaty_type: TreatyType) -> Dictionary:
	if not factions.has(faction_id):
		return {"allowed": false, "reason": "Unknown faction", "cost_gold": 0}
	
	var f = factions[faction_id]
	var op = f.get("opinion", 0.0)
	var active = f.get("active_treaties", {})
	
	if active.has(treaty_type):
		return {"allowed": false, "reason": "Treaty already active", "cost_gold": 0}
	
	var cur_status = get_relationship_status(faction_id)
	if cur_status == RelationshipStatus.WAR:
		return {"allowed": false, "reason": "Cannot sign treaty while at war! Sue for peace first.", "cost_gold": 0}

	match treaty_type:
		TreatyType.NON_AGGRESSION:
			if op < 0.0:
				return {"allowed": false, "reason": "Requires Neutral or higher opinion (>= 0)", "cost_gold": 25}
			return {"allowed": true, "reason": "Eligible for Non-Aggression Pact", "cost_gold": 25}
			
		TreatyType.TRADE_CONCORDAT:
			if op < 20.0:
				return {"allowed": false, "reason": "Requires at least +20 opinion for commerce treaty", "cost_gold": 45}
			return {"allowed": true, "reason": "Eligible for Trade Concordat", "cost_gold": 45}
			
		TreatyType.DEFENSIVE_LEAGUE:
			if op < 50.0:
				return {"allowed": false, "reason": "Requires Friendly disposition (>= +50 opinion)", "cost_gold": 80}
			return {"allowed": true, "reason": "Eligible for Defensive Military League", "cost_gold": 80}
			
		TreatyType.VASSALAGE_CHARTER:
			if f.get("is_vassal", false):
				return {"allowed": false, "reason": "Faction is already your vassal", "cost_gold": 0}
			if op < 80.0:
				return {"allowed": false, "reason": "Requires Allied relationship (>= +80 opinion) to peacefully vassalize", "cost_gold": 150}
			return {"allowed": true, "reason": "Eligible to establish Vassalage Charter", "cost_gold": 150}
			
		_:
			return {"allowed": false, "reason": "Invalid treaty type", "cost_gold": 0}

func sign_treaty(faction_id: String, treaty_type: TreatyType, treasury_gold: int) -> bool:
	var check = can_sign_treaty(faction_id, treaty_type)
	if not check.get("allowed", false):
		return false
	
	var cost = check.get("cost_gold", 0)
	if treasury_gold < cost:
		return false
	
	var f = factions[faction_id]
	var duration: float = 300.0 # 5 minutes default duration
	if treaty_type == TreatyType.VASSALAGE_CHARTER:
		duration = -1.0 # Permanent until broken
		f["is_vassal"] = true
		f["vassal_tribute_timer"] = 0.0
		modify_opinion(faction_id, 20.0, "Vassalage chartered")
	elif treaty_type == TreatyType.TRADE_CONCORDAT:
		duration = 400.0
		modify_opinion(faction_id, 10.0, "Trade treaty signed")
	elif treaty_type == TreatyType.DEFENSIVE_LEAGUE:
		duration = 360.0
		modify_opinion(faction_id, 15.0, "Defensive alliance enacted")
	elif treaty_type == TreatyType.NON_AGGRESSION:
		duration = 300.0
		modify_opinion(faction_id, 8.0, "Non-aggression pact agreed")

	f["active_treaties"][treaty_type] = duration
	emit_signal("treaty_signed", faction_id, treaty_type)
	return true

func break_treaty(faction_id: String, treaty_type: TreatyType) -> bool:
	if not factions.has(faction_id):
		return false
	var f = factions[faction_id]
	if not f["active_treaties"].has(treaty_type):
		return false
	
	f["active_treaties"].erase(treaty_type)
	if treaty_type == TreatyType.VASSALAGE_CHARTER:
		f["is_vassal"] = false
		
	var penalty = -35.0
	modify_opinion(faction_id, penalty, "Dishonorable treaty breach")
	emit_signal("treaty_broken", faction_id, treaty_type, penalty)
	return true

func declare_war(faction_id: String) -> bool:
	if not factions.has(faction_id):
		return false
	var f = factions[faction_id]
	f["is_vassal"] = false
	f["active_treaties"].clear()
	f["opinion"] = -100.0
	emit_signal("war_declared", faction_id, true)
	emit_signal("opinion_changed", faction_id, f["opinion"], -100.0, RelationshipStatus.WAR)
	return true

func sue_for_peace(faction_id: String, indemnity_gold: int) -> bool:
	if not factions.has(faction_id):
		return false
	var f = factions[faction_id]
	if get_relationship_status(faction_id) != RelationshipStatus.WAR:
		return false
	
	var required_gold = int(f.get("military_strength", 100.0) * 0.5)
	if indemnity_gold < required_gold:
		return false
	
	f["opinion"] = -15.0 # Elevated to hostile/neutral threshold
	emit_signal("peace_concluded", faction_id)
	emit_signal("opinion_changed", faction_id, -100.0, -15.0, RelationshipStatus.HOSTILE)
	return true

func send_gift(faction_id: String, resource_name: String, amount: int, available_stock: int) -> Dictionary:
	if not factions.has(faction_id):
		return {"success": false, "opinion_boost": 0.0, "message": "Faction not found"}
	
	if amount <= 0 or available_stock < amount:
		return {"success": false, "opinion_boost": 0.0, "message": "Insufficient resources to gift"}
	
	var f = factions[faction_id]
	var multiplier = 1.0
	if f.get("demands", "") == resource_name or (resource_name == "bread" and f.get("demands") == "food") or (resource_name == "logs" and f.get("demands") == "timber"):
		multiplier = 1.75
	elif resource_name == "gold_coins":
		multiplier = 1.4
	
	var boost = (amount * 1.5) * multiplier
	boost = clampf(boost, 2.0, 35.0)
	modify_opinion(faction_id, boost, "Envoy tribute gift received")
	
	return {
		"success": true,
		"opinion_boost": boost,
		"message": "Envoy gifted %d %s to %s (+%.1f opinion)" % [amount, resource_name, f["name"], boost]
	}

func demand_tribute(faction_id: String, resource_name: String, amount: int, player_military_strength: float) -> Dictionary:
	if not factions.has(faction_id):
		return {"accepted": false, "amount_received": 0, "opinion_penalty": 0.0, "reason": "Faction not found"}
	
	var f = factions[faction_id]
	var target_mil = f.get("military_strength", 100.0)
	var is_vassal = f.get("is_vassal", false)
	
	# If vassal, they are obliged to comply unless opinion is below -20
	if is_vassal:
		var penalty = -10.0
		modify_opinion(faction_id, penalty, "Monarch tribute extortion")
		emit_signal("tribute_demanded", faction_id, {resource_name: amount}, true)
		return {
			"accepted": true,
			"amount_received": amount,
			"opinion_penalty": penalty,
			"reason": "Vassal complied with imperial demand"
		}
	
	# If not vassal, military intimidation check
	if player_military_strength > (target_mil * 1.4):
		var penalty = -25.0
		modify_opinion(faction_id, penalty, "Extorted by military menace")
		emit_signal("tribute_demanded", faction_id, {resource_name: amount}, true)
		return {
			"accepted": true,
			"amount_received": amount,
			"opinion_penalty": penalty,
			"reason": "Intimidated by your superior legion and yielded tribute"
		}
	else:
		var penalty = -30.0
		modify_opinion(faction_id, penalty, "Defiant against insolent tribute demands")
		emit_signal("tribute_demanded", faction_id, {resource_name: amount}, false)
		if f["opinion"] <= -40.0:
			declare_war(faction_id)
		return {
			"accepted": false,
			"amount_received": 0,
			"opinion_penalty": penalty,
			"reason": "Faction defiantly rejected the tribute demand!"
		}

func process_diplomacy(delta: float, supply_chain = null) -> void:
	# 1. Process active treaties and vassal tributes
	for f_id in factions.keys():
		var f = factions[f_id]
		var treaties = f.get("active_treaties", {})
		var to_remove = []
		
		for t_type in treaties.keys():
			var remaining = treaties[t_type]
			if remaining > 0.0:
				remaining -= delta
				treaties[t_type] = remaining
				if remaining <= 0.0:
					to_remove.append(t_type)
					
			# Passive perks while treaty active
			if t_type == TreatyType.TRADE_CONCORDAT:
				# Passive gradual opinion increase
				modify_opinion(f_id, delta * 0.02, "Trade Concordat mutual prosperity")
				if supply_chain and randf() < (delta * 0.05):
					# Periodic merchant tariff royalty
					supply_chain.add_resource("gold_coins", 1)

		for exp_t in to_remove:
			treaties.erase(exp_t)
			emit_signal("treaty_broken", f_id, exp_t, 0.0)

		# Vassal Tribute Delivery Cycle
		if f.get("is_vassal", false):
			var v_timer = f.get("vassal_tribute_timer", 0.0) + delta
			var v_interval = f.get("vassal_tribute_interval", 90.0)
			if v_timer >= v_interval:
				v_timer = 0.0
				var pkg = f.get("tribute_package", {"gold_coins": 20})
				if supply_chain:
					for res_key in pkg.keys():
						supply_chain.add_resource(res_key, pkg[res_key])
				emit_signal("tribute_received", f_id, pkg)
			f["vassal_tribute_timer"] = v_timer

		# Natural Opinion Drift towards base_opinion
		var cur_op = f.get("opinion", 0.0)
		var base_op = f.get("base_opinion", 0.0)
		if absf(cur_op - base_op) > 0.01:
			var drift_rate = delta * 0.015 # Slow drift over time
			if cur_op > base_op:
				f["opinion"] = maxf(base_op, cur_op - drift_rate)
			else:
				f["opinion"] = minf(base_op, cur_op + drift_rate)

	# 2. Emissary Caravan Periodic Event
	emissary_timer += delta
	if emissary_timer >= EMISSARY_INTERVAL:
		emissary_timer = 0.0
		_trigger_random_emissary()

func _trigger_random_emissary() -> void:
	if factions.is_empty():
		return
	var f_keys = factions.keys()
	var pick_key = f_keys[randi() % f_keys.size()]
	var f = factions[pick_key]
	var evt = {
		"title": "Diplomatic Emissary Arrived",
		"faction": f["name"],
		"ruler": f["ruler"],
		"message": "An envoy from %s approaches your royal court with diplomatic greetings." % f["name"],
		"timestamp": Time.get_unix_time_from_system()
	}
	emit_signal("emissary_arrived", pick_key, evt)

func to_dict() -> Dictionary:
	var out_factions = {}
	for f_id in factions.keys():
		var f = factions[f_id]
		var treaties_serialized = {}
		for t in f.get("active_treaties", {}).keys():
			treaties_serialized[str(int(t))] = f["active_treaties"][t]
			
		out_factions[f_id] = {
			"opinion": f.get("opinion", 0.0),
			"base_opinion": f.get("base_opinion", 0.0),
			"military_strength": f.get("military_strength", 100.0),
			"economic_wealth": f.get("economic_wealth", 100.0),
			"is_vassal": f.get("is_vassal", false),
			"vassal_tribute_timer": f.get("vassal_tribute_timer", 0.0),
			"vassal_tribute_interval": f.get("vassal_tribute_interval", 90.0),
			"active_treaties": treaties_serialized
		}
	return {
		"factions": out_factions,
		"emissary_timer": emissary_timer
	}

func from_dict(data: Dictionary) -> void:
	if not data or data.is_empty():
		return
	emissary_timer = data.get("emissary_timer", 0.0)
	var loaded_factions = data.get("factions", {})
	for f_id in loaded_factions.keys():
		if factions.has(f_id):
			var src = loaded_factions[f_id]
			factions[f_id]["opinion"] = src.get("opinion", factions[f_id]["opinion"])
			factions[f_id]["base_opinion"] = src.get("base_opinion", factions[f_id]["base_opinion"])
			factions[f_id]["military_strength"] = src.get("military_strength", factions[f_id]["military_strength"])
			factions[f_id]["economic_wealth"] = src.get("economic_wealth", factions[f_id]["economic_wealth"])
			factions[f_id]["is_vassal"] = src.get("is_vassal", false)
			factions[f_id]["vassal_tribute_timer"] = src.get("vassal_tribute_timer", 0.0)
			factions[f_id]["vassal_tribute_interval"] = src.get("vassal_tribute_interval", 90.0)
			
			var loaded_treaties = {}
			var raw_treaties = src.get("active_treaties", {})
			for t_key in raw_treaties.keys():
				var t_int = int(t_key)
				loaded_treaties[t_int] = raw_treaties[t_key]
			factions[f_id]["active_treaties"] = loaded_treaties
