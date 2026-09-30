# scripts/combat/foreign_invasion_manager.gd
# Voxel Lord: Feudal Realm - Milestone 49: Foreign Invasions & Strategic Siege Warfare
# Coordinates hostile kingdom invasion battalions, siege sappers, border outposts,
# and tactical battlefield garrison defense.

class_name ForeignInvasionManager
extends Node

signal invasion_begun(battalion_id: String, faction_id: String, target_outpost: String)
signal outpost_attacked(outpost_id: String, damage: float, defenders_left: int)
signal outpost_breached(outpost_id: String)
signal battalion_routed(battalion_id: String, casualties: int)
signal pitch_cauldron_ignited(outpost_id: String)
signal militia_mustered(outpost_id: String, count: int)

# 4 Frontier Strategic Outposts
var outposts: Dictionary = {}

# Active Invasions: battalion_id -> Dictionary
var active_battalions: Dictionary = {}

var invasion_check_timer: float = 0.0
const INVASION_CHECK_INTERVAL: float = 45.0 # Check for invasion triggers every 45s

func _init() -> void:
	init_default_outposts()

func init_default_outposts() -> void:
	outposts = {
		"north_redoubt": {
			"id": "north_redoubt",
			"name": "Northern Vanguard Redoubt",
			"pos": Vector3(32.0, 14.0, 10.0),
			"district": "citadel",
			"health": 150.0,
			"max_health": 150.0,
			"garrison_count": 4,
			"has_pitch_cauldron": true,
			"pitch_ready": true,
			"status": "Defended 🛡️"
		},
		"east_watch": {
			"id": "east_watch",
			"name": "Eastern Coastline Watchtower",
			"pos": Vector3(60.0, 10.0, 32.0),
			"district": "harbor",
			"health": 120.0,
			"max_health": 120.0,
			"garrison_count": 3,
			"has_pitch_cauldron": false,
			"pitch_ready": false,
			"status": "Defended 🛡️"
		},
		"west_bastion": {
			"id": "west_bastion",
			"name": "Western Highlands Bastion",
			"pos": Vector3(10.0, 8.0, 32.0),
			"district": "mining",
			"health": 140.0,
			"max_health": 140.0,
			"garrison_count": 3,
			"has_pitch_cauldron": true,
			"pitch_ready": true,
			"status": "Defended 🛡️"
		},
		"south_gate": {
			"id": "south_gate",
			"name": "Southern Frontier Palisade Gate",
			"pos": Vector3(32.0, 11.0, 60.0),
			"district": "wilderness",
			"health": 100.0,
			"max_health": 100.0,
			"garrison_count": 2,
			"has_pitch_cauldron": false,
			"pitch_ready": false,
			"status": "Defended 🛡️"
		}
	}

func get_outpost(outpost_id: String) -> Dictionary:
	return outposts.get(outpost_id, {})

func get_all_outposts() -> Dictionary:
	return outposts

func get_active_battalions() -> Dictionary:
	return active_battalions

func trigger_invasion(faction_id: String, target_outpost: String = "") -> String:
	if not outposts.has(target_outpost):
		var keys = outposts.keys()
		target_outpost = keys[randi() % keys.size()]

	var timestamp = int(Time.get_unix_time_from_system())
	var b_id = "%s_invader_%d" % [faction_id, timestamp]

	var leader_name = "Warlord Torvold" if faction_id == "ashfell" else ("Knight Commander Valen" if faction_id == "valoria" else "Captain Corvo")
	var troops = 14 if faction_id == "ashfell" else (16 if faction_id == "valoria" else 12)
	var siege = "battering_ram" if faction_id == "valoria" else ("explosive_keg" if faction_id == "ashfell" else "siege_ballista")
	var combat_pwr = 180.0 if faction_id == "valoria" else (160.0 if faction_id == "ashfell" else 130.0)

	var battalion = {
		"id": b_id,
		"faction_id": faction_id,
		"leader": leader_name,
		"troop_count": troops,
		"initial_troops": troops,
		"siege_engine": siege,
		"target_outpost": target_outpost,
		"progress": 0.0, # 0.0 (distant border) to 1.0 (breaching walls)
		"march_speed": 0.02, # takes 50 seconds to arrive
		"combat_power": combat_pwr,
		"status": "Marching on Frontier"
	}

	active_battalions[b_id] = battalion
	outposts[target_outpost]["status"] = "Hostiles Approaching ⚠️"

	emit_signal("invasion_begun", b_id, faction_id, target_outpost)
	return b_id

func assign_guards_to_outpost(outpost_id: String, count: int) -> bool:
	if not outposts.has(outpost_id):
		return false
	outposts[outpost_id]["garrison_count"] += count
	return true

func muster_peasant_militia(outpost_id: String, supply_chain = null) -> Dictionary:
	if not outposts.has(outpost_id):
		return {"success": false, "message": "Unknown outpost"}

	if supply_chain:
		var bread = supply_chain.get_resource("bread")
		var iron = supply_chain.get_resource("iron_ingots")
		if bread < 15 or iron < 8:
			return {"success": false, "message": "Need 15 Bread and 8 Iron Ingots to muster militia"}
		supply_chain.consume_resource("bread", 15)
		supply_chain.consume_resource("iron_ingots", 8)

	var mustered_count = 4
	outposts[outpost_id]["garrison_count"] += mustered_count
	emit_signal("militia_mustered", outpost_id, mustered_count)
	return {"success": true, "message": "Mustered %d Peasant Militiamen to %s!" % [mustered_count, outposts[outpost_id]["name"]]}

func arm_boiling_pitch(outpost_id: String, supply_chain = null) -> Dictionary:
	if not outposts.has(outpost_id):
		return {"success": false, "message": "Unknown outpost"}
	var op = outposts[outpost_id]
	if not op.get("has_pitch_cauldron", false):
		return {"success": false, "message": "No pitch cauldron installed at this fortification"}
	if op.get("pitch_ready", false):
		return {"success": false, "message": "Boiling pitch is already armed and boiling"}

	if supply_chain:
		var coal = supply_chain.get_resource("coal")
		if coal < 5:
			return {"success": false, "message": "Need 5 Coal to heat pitch cauldron"}
		supply_chain.consume_resource("coal", 5)

	op["pitch_ready"] = true
	return {"success": true, "message": "Boiling pitch cauldrons fired up and armed!"}

func unleash_boiling_pitch(outpost_id: String) -> Dictionary:
	if not outposts.has(outpost_id):
		return {"success": false, "damage": 0.0}
	var op = outposts[outpost_id]
	if not op.get("pitch_ready", false):
		return {"success": false, "damage": 0.0}

	op["pitch_ready"] = false
	var dmg = 65.0
	emit_signal("pitch_cauldron_ignited", outpost_id)

	# Damage any active battalion currently assaulting this outpost
	for b_id in active_battalions.keys():
		var b = active_battalions[b_id]
		if b.get("target_outpost") == outpost_id and b.get("progress", 0.0) >= 0.8:
			var casualties = 4
			b["troop_count"] = maxi(0, b["troop_count"] - casualties)
			b["combat_power"] = maxf(10.0, b["combat_power"] - dmg)

	return {"success": true, "damage": dmg}

func process_invasions(delta: float, diplomacy_system = null) -> void:
	# 1. Check if any war factions should trigger invasions
	invasion_check_timer += delta
	if invasion_check_timer >= INVASION_CHECK_INTERVAL:
		invasion_check_timer = 0.0
		if diplomacy_system:
			var factions = diplomacy_system.get_all_factions()
			for f_id in factions.keys():
				if diplomacy_system.get_relationship_status(f_id) == DiplomacySystem.RelationshipStatus.WAR:
					if active_battalions.size() < 2 and randf() < 0.6:
						trigger_invasion(f_id)

	# 2. Advance active marching battalions
	var routed_battalions = []
	for b_id in active_battalions.keys():
		var b = active_battalions[b_id]
		var target_op_id = b["target_outpost"]
		var op = outposts.get(target_op_id, {})

		if b["progress"] < 1.0:
			b["progress"] = minf(1.0, b["progress"] + delta * b["march_speed"])
			if b["progress"] >= 1.0:
				b["status"] = "Assaulting Fortification Breaches!"
				if not op.is_empty():
					op["status"] = "Under Violent Siege ⚔️"
		else:
			# Combat Resolution Tick
			_resolve_siege_tick(b_id, delta)

		if b.get("troop_count", 0) <= 0 or b.get("combat_power", 0.0) <= 0.0:
			routed_battalions.append(b_id)

	for r_id in routed_battalions:
		var b = active_battalions[r_id]
		var total_cas = b.get("initial_troops", 10) - b.get("troop_count", 0)
		var op_id = b.get("target_outpost", "")
		if outposts.has(op_id) and outposts[op_id]["health"] > 0:
			outposts[op_id]["status"] = "Defended 🛡️"
		active_battalions.erase(r_id)
		emit_signal("battalion_routed", r_id, total_cas)

func _resolve_siege_tick(battalion_id: String, delta: float) -> void:
	var b = active_battalions.get(battalion_id)
	if not b:
		return
	var op_id = b["target_outpost"]
	if not outposts.has(op_id):
		return
	var op = outposts[op_id]

	# Garrison defenses inflict damage on invading battalion
	var garrison = op.get("garrison_count", 0)
	var defender_dps = garrison * 8.0 * delta
	b["combat_power"] = maxf(0.0, b["combat_power"] - defender_dps)
	if defender_dps > 15.0 and randf() < 0.3:
		b["troop_count"] = maxi(0, b["troop_count"] - 1)

	# Battalion attacks outpost structure and garrison
	var siege_mult = 1.6 if b.get("siege_engine") == "battering_ram" else 1.2
	var invader_dps = (b["troop_count"] * 3.5 * siege_mult) * delta
	op["health"] = maxf(0.0, op["health"] - invader_dps)
	emit_signal("outpost_attacked", op_id, invader_dps, garrison)

	# Casualties on defenders
	if op["health"] < (op["max_health"] * 0.5) and garrison > 0 and randf() < (delta * 0.15):
		op["garrison_count"] -= 1

	# Check breach
	if op["health"] <= 0.0 and op["status"] != "Breached & Fallen 💀":
		op["status"] = "Breached & Fallen 💀"
		emit_signal("outpost_breached", op_id)

func to_dict() -> Dictionary:
	var serialized_outposts = {}
	for k in outposts.keys():
		var op = outposts[k]
		serialized_outposts[k] = {
			"health": op["health"],
			"garrison_count": op["garrison_count"],
			"pitch_ready": op.get("pitch_ready", false),
			"status": op["status"]
		}

	var serialized_battalions = {}
	for b_id in active_battalions.keys():
		var b = active_battalions[b_id]
		serialized_battalions[b_id] = {
			"faction_id": b["faction_id"],
			"leader": b["leader"],
			"troop_count": b["troop_count"],
			"initial_troops": b["initial_troops"],
			"siege_engine": b["siege_engine"],
			"target_outpost": b["target_outpost"],
			"progress": b["progress"],
			"combat_power": b["combat_power"],
			"status": b["status"]
		}

	return {
		"outposts": serialized_outposts,
		"battalions": serialized_battalions,
		"check_timer": invasion_check_timer
	}

func from_dict(data: Dictionary) -> void:
	if not data or data.is_empty():
		return
	invasion_check_timer = data.get("check_timer", 0.0)

	var loaded_outposts = data.get("outposts", {})
	for op_id in loaded_outposts.keys():
		if outposts.has(op_id):
			var src = loaded_outposts[op_id]
			outposts[op_id]["health"] = src.get("health", outposts[op_id]["health"])
			outposts[op_id]["garrison_count"] = src.get("garrison_count", outposts[op_id]["garrison_count"])
			outposts[op_id]["pitch_ready"] = src.get("pitch_ready", outposts[op_id]["pitch_ready"])
			outposts[op_id]["status"] = src.get("status", outposts[op_id]["status"])

	var loaded_battalions = data.get("battalions", {})
	active_battalions.clear()
	for b_id in loaded_battalions.keys():
		var src = loaded_battalions[b_id]
		active_battalions[b_id] = {
			"id": b_id,
			"faction_id": src.get("faction_id", "ashfell"),
			"leader": src.get("leader", "Warlord"),
			"troop_count": src.get("troop_count", 10),
			"initial_troops": src.get("initial_troops", 10),
			"siege_engine": src.get("siege_engine", "battering_ram"),
			"target_outpost": src.get("target_outpost", "north_redoubt"),
			"progress": src.get("progress", 0.0),
			"march_speed": 0.02,
			"combat_power": src.get("combat_power", 100.0),
			"status": src.get("status", "Marching")
		}
