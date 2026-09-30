# scripts/combat/espionage_manager.gd
# Voxel Lord: Feudal Realm - Milestone 52: Royal Spymaster Court Intrigue & Shadow Espionage Network
# Manages covert shadow agents, infiltration into rival courts, siege sabotage, technology theft,
# domestic counter-intelligence, and dungeon interrogations.

class_name EspionageManager
extends Node

signal agent_recruited(agent_id: String, agent_name: String, agent_type: String)
signal operation_launched(op_id: String, target_realm: String, agent_id: String)
signal operation_resolved(op_id: String, success: bool, outcome_desc: String, rewards: Dictionary)
signal counter_intel_triggered(threat_title: String, thwarted: bool)
signal prisoner_interrogated(prisoner_id: String, secrets_revealed: String)
signal daily_upkeep_processed(total_cost: int, paid_count: int, unpaid_count: int)

# Agent Archetypes Catalog
var agent_archetypes: Dictionary = {}

# Intrigue Operations Catalog
var operations_catalog: Dictionary = {}

# Active Shadow Network State
var recruited_agents: Dictionary = {} # agent_id -> Dictionary
var active_operations: Array[Dictionary] = [] # list of ongoing operations
var captured_prisoners: Array[Dictionary] = [] # captive foreign agents
var citadel_security_rating: float = 65.0 # 0.0 to 100.0% counter-intelligence rating
var court_suspicion: float = 10.0 # 0.0 to 100.0%
var total_operations_completed: int = 0
var successful_operations_count: int = 0
var plots_thwarted_count: int = 0

func _init() -> void:
	init_archetypes()
	init_operations_catalog()

func init_archetypes() -> void:
	agent_archetypes = {
		"informant": {
			"type": "informant",
			"name": "Whispering Tavern Informant",
			"cost_gold": 30,
			"upkeep_daily": 2,
			"stealth_bonus": 0.15,
			"desc": "Low-profile eyes and ears in town squares and foreign border inns.",
			"icon": "👂"
		},
		"saboteur": {
			"type": "saboteur",
			"name": "Infiltration Sapper & Saboteur",
			"cost_gold": 60,
			"upkeep_daily": 4,
			"sabotage_bonus": 0.35,
			"desc": "Expert in arson, ballistics rigging, and spiking enemy siege catapults.",
			"icon": "🗡️"
		},
		"master_spy": {
			"type": "master_spy",
			"name": "Shadow Courtier & Master Provocateur",
			"cost_gold": 120,
			"upkeep_daily": 8,
			"intel_bonus": 0.45,
			"desc": "Elite court infiltrator capable of falsifying treaties and stealing secrets.",
			"icon": "🎭"
		}
	}

func init_operations_catalog() -> void:
	operations_catalog = {
		"gather_invasion_intel": {
			"id": "gather_invasion_intel",
			"name": "Uncover Military Invasion War Plans",
			"cost_gold": 25,
			"duration": 45.0, # seconds
			"base_success_chance": 0.80,
			"risk_capture": 0.15,
			"desc": "Infiltrate foreign war councils to determine exact attack target and siege engines.",
			"icon": "🗺️"
		},
		"sabotage_siege_weapons": {
			"id": "sabotage_siege_weapons",
			"name": "Spike Battering Rams & Burn Pitch Depots",
			"cost_gold": 45,
			"duration": 60.0,
			"base_success_chance": 0.65,
			"risk_capture": 0.25,
			"desc": "Disables enemy siege engineering, reducing battalion power by 40%.",
			"icon": "💥"
		},
		"steal_scholastic_tech": {
			"id": "steal_scholastic_tech",
			"name": "Pilfer Monastic Scriptoria Parchments",
			"cost_gold": 60,
			"duration": 75.0,
			"base_success_chance": 0.60,
			"risk_capture": 0.30,
			"desc": "Steals ancient engineering parchments, granting +120 scholastic research points.",
			"icon": "📜"
		},
		"incite_border_revolt": {
			"id": "incite_border_revolt",
			"name": "Sow Dissidence & Bribe Border Troops",
			"cost_gold": 80,
			"duration": 90.0,
			"base_success_chance": 0.55,
			"risk_capture": 0.35,
			"desc": "Instigates peasant revolt in rival province, recruiting +3 deserters to royal guard.",
			"icon": "🔥"
		}
	}

func _process(delta: float) -> void:
	# Progress active operations
	var finished_ops: Array[Dictionary] = []
	for op in active_operations:
		op["timer"] -= delta
		if op["timer"] <= 0.0:
			finished_ops.append(op)

	for op in finished_ops:
		resolve_operation(op)
		active_operations.erase(op)

# ----------------- Agent Recruitment -----------------
func recruit_agent(archetype_type: String, agent_custom_name: String = "", supply_chain: SupplyChain = null) -> Dictionary:
	if not agent_archetypes.has(archetype_type):
		return {"success": false, "reason": "Unknown agent archetype"}

	var arch = agent_archetypes[archetype_type]
	var cost = arch["cost_gold"]

	if supply_chain:
		if supply_chain.get_resource("gold_coins") < cost:
			return {"success": false, "reason": "Insufficient gold (Requires %d Gold)" % cost}
		supply_chain.consume_resource("gold_coins", cost)

	var agent_id = "agent_%d" % (recruited_agents.size() + 1)
	var final_name = agent_custom_name
	if final_name == "":
		final_name = "%s of the Shadow" % arch["name"]

	var agent = {
		"id": agent_id,
		"name": final_name,
		"type": archetype_type,
		"stationed_realm": "domestic_citadel", # or "valoria", "ashfell", "silvercoast", etc.
		"status": "Ready", # "Ready", "On Mission", "Captured"
		"experience": 0,
		"stealth_rating": 50.0 + (arch.get("stealth_bonus", 0.0) * 100.0),
		"sabotage_rating": 40.0 + (arch.get("sabotage_bonus", 0.0) * 100.0)
	}

	recruited_agents[agent_id] = agent
	citadel_security_rating = minf(100.0, citadel_security_rating + 5.0)
	agent_recruited.emit(agent_id, final_name, archetype_type)

	return {
		"success": true,
		"agent": agent
	}

# ----------------- Covert Intrigue Operations -----------------
func launch_operation(op_id: String, target_realm: String, agent_id: String, supply_chain: SupplyChain = null) -> Dictionary:
	if not operations_catalog.has(op_id):
		return {"success": false, "reason": "Unknown covert operation"}
	if not recruited_agents.has(agent_id):
		return {"success": false, "reason": "Agent not found"}

	var agent = recruited_agents[agent_id]
	if agent["status"] != "Ready":
		return {"success": false, "reason": "Agent is currently busy or unavailable"}

	var op_def = operations_catalog[op_id]
	var cost = op_def["cost_gold"]

	if supply_chain:
		if supply_chain.get_resource("gold_coins") < cost:
			return {"success": false, "reason": "Insufficient treasury coins (Requires %d Gold)" % cost}
		supply_chain.consume_resource("gold_coins", cost)

	agent["status"] = "On Mission"
	agent["stationed_realm"] = target_realm

	var op_instance = {
		"instance_id": "op_inst_%d" % (total_operations_completed + active_operations.size() + 1),
		"op_id": op_id,
		"target_realm": target_realm,
		"agent_id": agent_id,
		"timer": op_def["duration"],
		"total_duration": op_def["duration"],
		"base_success": op_def["base_success_chance"],
		"risk_capture": op_def["risk_capture"]
	}

	active_operations.append(op_instance)
	operation_launched.emit(op_id, target_realm, agent_id)

	return {
		"success": true,
		"operation": op_instance
	}

func resolve_operation(op: Dictionary) -> void:
	total_operations_completed += 1
	var agent_id = op["agent_id"]
	var agent = recruited_agents.get(agent_id)
	var op_def = operations_catalog.get(op["op_id"], {})

	var success_chance = op["base_success"]
	if agent:
		if op["op_id"] == "sabotage_siege_weapons":
			success_chance += (agent.get("sabotage_rating", 40.0) / 200.0)
		else:
			success_chance += (agent.get("stealth_rating", 50.0) / 200.0)

	# Pseudo-random / deterministic outcome threshold
	var rng_roll = 0.50 # baseline deterministic check
	var is_success = rng_roll <= success_chance
	var rewards: Dictionary = {}
	var desc = ""

	if is_success:
		successful_operations_count += 1
		if agent:
			agent["status"] = "Ready"
			agent["experience"] += 25

		if op["op_id"] == "gather_invasion_intel":
			desc = "Revealed classified war council plans in %s! Attack vector identified." % op["target_realm"].capitalize()
			rewards = {"intel_accuracy": 1.0, "invasion_revealed": true}
		elif op["op_id"] == "sabotage_siege_weapons":
			desc = "Saboteurs set fire to siege ram depot in %s! Enemy siege strength halved." % op["target_realm"].capitalize()
			rewards = {"enemy_siege_penalty": 0.40, "delay_ticks": 60.0}
		elif op["op_id"] == "steal_scholastic_tech":
			desc = "Stole illuminated parchment treatises from %s scriptorium! +120 Scholar Points." % op["target_realm"].capitalize()
			rewards = {"scholar_points": 120.0}
		elif op["op_id"] == "incite_border_revolt":
			desc = "Peasant revolt ignited in %s! Three veteran border guards defected to our citadel." % op["target_realm"].capitalize()
			rewards = {"recruited_guards": 3}
	else:
		# Check if captured
		if agent:
			agent["status"] = "Captured"
			agent["stationed_realm"] = "foreign_dungeon"
		desc = "Operation in %s was compromised! Agent was captured by foreign bailiffs." % op["target_realm"].capitalize()
		rewards = {"captured": true}

	operation_resolved.emit(op["op_id"], is_success, desc, rewards)

# ----------------- Counter-Intelligence & Dungeons -----------------
func trigger_domestic_counter_intel_check(infiltrator_type: String = "assassin") -> Dictionary:
	var thwarted = citadel_security_rating >= 40.0
	if thwarted:
		plots_thwarted_count += 1
		var prisoner = {
			"id": "prisoner_%d" % (captured_prisoners.size() + 1),
			"name": "Captured %s from rival realm" % infiltrator_type.capitalize(),
			"interrogated": false,
			"ransom_value": 50
		}
		captured_prisoners.append(prisoner)
		counter_intel_triggered.emit("Foiled %s plot in Citadel Tavern!" % infiltrator_type.capitalize(), true)
		return {"thwarted": true, "prisoner": prisoner}
	else:
		court_suspicion = minf(100.0, court_suspicion + 20.0)
		counter_intel_triggered.emit("Enemy infiltrator breached outer bailey!", false)
		return {"thwarted": false}

func interrogate_prisoner(prisoner_id: String) -> Dictionary:
	for p in captured_prisoners:
		if p["id"] == prisoner_id:
			if p["interrogated"]:
				return {"success": false, "reason": "Captive has already divulged all their secrets."}
			p["interrogated"] = true
			var secrets = "Disclosed concealed spy networks and secret treasury stashes (+75 Gold intelligence)!"
			prisoner_interrogated.emit(prisoner_id, secrets)
			return {
				"success": true,
				"secrets": secrets,
				"coins_discovered": 75
			}
	return {"success": false, "reason": "Prisoner not found in citadel dungeons"}

func ransom_prisoner(prisoner_id: String, supply_chain: SupplyChain = null) -> bool:
	for i in range(captured_prisoners.size()):
		if captured_prisoners[i]["id"] == prisoner_id:
			var val = captured_prisoners[i]["ransom_value"]
			if supply_chain:
				supply_chain.add_resource("gold_coins", val)
			captured_prisoners.remove_at(i)
			return true
	return false

# ----------------- Daily Upkeep & Retinue Maintenance -----------------
func process_daily_upkeep(supply_chain: SupplyChain = null) -> Dictionary:
	var total_upkeep_needed: int = 0
	var paid_count: int = 0
	var unpaid_count: int = 0

	for agent_id in recruited_agents.keys():
		var agent = recruited_agents[agent_id]
		if agent.get("status") == "Captured":
			continue
		var atype = agent.get("type", "informant")
		var arch = agent_archetypes.get(atype, {})
		var upkeep = arch.get("upkeep_daily", 2)
		total_upkeep_needed += upkeep

	var current_gold = supply_chain.get_resource("gold_coins") if supply_chain else 0
	var remaining_gold = current_gold

	for agent_id in recruited_agents.keys():
		var agent = recruited_agents[agent_id]
		if agent.get("status") == "Captured":
			continue
		var atype = agent.get("type", "informant")
		var arch = agent_archetypes.get(atype, {})
		var upkeep = arch.get("upkeep_daily", 2)

		if supply_chain and remaining_gold >= upkeep:
			supply_chain.consume_resource("gold_coins", upkeep)
			remaining_gold -= upkeep
			if agent.get("status") == "Unpaid":
				agent["status"] = "Ready"
			paid_count += 1
		else:
			if agent.get("status") == "Ready":
				agent["status"] = "Unpaid"
			unpaid_count += 1

	var actual_cost_paid = current_gold - remaining_gold
	daily_upkeep_processed.emit(actual_cost_paid, paid_count, unpaid_count)

	return {
		"total_cost_needed": total_upkeep_needed,
		"cost_paid": actual_cost_paid,
		"paid_count": paid_count,
		"unpaid_count": unpaid_count,
		"all_paid": (unpaid_count == 0)
	}

# ----------------- Persistence -----------------
func to_dict() -> Dictionary:
	var agents_copy: Dictionary = {}
	for k in recruited_agents.keys():
		agents_copy[k] = recruited_agents[k].duplicate(true)

	var ops_copy: Array = []
	for op in active_operations:
		ops_copy.append(op.duplicate(true))

	var pris_copy: Array = []
	for p in captured_prisoners:
		pris_copy.append(p.duplicate(true))

	return {
		"recruited_agents": agents_copy,
		"active_operations": ops_copy,
		"captured_prisoners": pris_copy,
		"citadel_security_rating": citadel_security_rating,
		"court_suspicion": court_suspicion,
		"total_operations_completed": total_operations_completed,
		"successful_operations_count": successful_operations_count,
		"plots_thwarted_count": plots_thwarted_count
	}

func from_dict(data: Dictionary) -> void:
	if data.is_empty():
		return
	recruited_agents = data.get("recruited_agents", {})
	active_operations.clear()
	for op in data.get("active_operations", []):
		active_operations.append(op.duplicate(true))
	captured_prisoners.clear()
	for p in data.get("captured_prisoners", []):
		captured_prisoners.append(p.duplicate(true))
	citadel_security_rating = data.get("citadel_security_rating", 65.0)
	court_suspicion = data.get("court_suspicion", 10.0)
	total_operations_completed = data.get("total_operations_completed", 0)
	successful_operations_count = data.get("successful_operations_count", 0)
	plots_thwarted_count = data.get("plots_thwarted_count", 0)
