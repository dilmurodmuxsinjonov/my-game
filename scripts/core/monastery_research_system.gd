# scripts/core/monastery_research_system.gd
# Voxel Lord: Feudal Realm - Milestone 51: High Scholastic Monastic Order & Scriptoria Tech Tree
# Manages illuminated manuscript research, scholastic technologies, enshrinement of sacred holy relics,
# and monastic divine blessings.

class_name MonasteryResearchSystem
extends Node

signal research_started(tech_id: String, tech_name: String, required_points: int)
signal research_progress_updated(tech_id: String, current_points: float, max_points: float)
signal research_completed(tech_id: String, tech_name: String)
signal relic_enshrined(relic_id: String, relic_name: String, altar_slot: int)
signal relic_removed(relic_id: String, altar_slot: int)
signal abbey_bell_rung(blessing_name: String)

# Technologies catalog
var technologies: Dictionary = {}

# Relics catalog
var relics: Dictionary = {}

# Monastic Research State
var scholar_points: float = 0.0
var assigned_monk_scribes: int = 3
var current_research_id: String = ""
var research_progress: Dictionary = {} # tech_id -> float
var unlocked_techs: Array[String] = []

# Altar Relic Sanctuaries (3 Altar Slots)
var active_altar_relics: Dictionary = {
	0: "",
	1: "",
	2: ""
}
var discovered_relics: Array[String] = ["true_hearth_shard", "st_columba_tome", "perpetual_chalice"]

# Abbey Liturgy & Bell
var bell_blessing_active: bool = false
var bell_blessing_timer: float = 0.0
const BELL_BLESSING_DURATION: float = 180.0 # 3 minutes duration

func _init() -> void:
	init_technologies()
	init_relics()

func init_technologies() -> void:
	technologies = {
		"norfolk_genetics": {
			"id": "norfolk_genetics",
			"name": "Norfolk Four-Course Agronomy Genetics",
			"cost": 100,
			"desc": "+25% crop growth velocity, +15% soil nitrogen & phosphorus retention.",
			"icon": "🌾",
			"effects": {"crop_growth_mult": 1.25, "soil_retention_mult": 1.15}
		},
		"blast_catalysts": {
			"id": "blast_catalysts",
			"name": "Thermodynamic Blast Furnace Flux Catalysts",
			"cost": 150,
			"desc": "+30% smelting speed, unlocks crucible steel folded blade crafting.",
			"icon": "🔥",
			"effects": {"smelt_speed_mult": 1.30, "crucible_unlocked": true}
		},
		"counterweight_ballistics": {
			"id": "counterweight_ballistics",
			"name": "Gravitational Counterweight Ballistics",
			"cost": 200,
			"desc": "+35% siege weapon damage, increases trebuchet trajectory range to 250m.",
			"icon": "🎯",
			"effects": {"siege_damage_mult": 1.35, "trebuchet_range": 250.0}
		},
		"deep_shaft_geology": {
			"id": "deep_shaft_geology",
			"name": "Deep Subterranean Geological Surveying",
			"cost": 180,
			"desc": "+25% rare gem & silver ore extraction yield from mining shafts.",
			"icon": "💎",
			"effects": {"mining_gem_bonus": 1.25}
		},
		"guild_charters": {
			"id": "guild_charters",
			"name": "Imperial Artisan Guild Charters",
			"cost": 220,
			"desc": "+20% craft batch yield, -15% trading prices with merchant caravans.",
			"icon": "📜",
			"effects": {"craft_yield_mult": 1.20, "trade_discount": 0.15}
		},
		"sacred_architecture": {
			"id": "sacred_architecture",
			"name": "Gothic Monastic Vaulting & Flying Buttresses",
			"cost": 250,
			"desc": "+30% structural integrity load threshold before ceiling collapse.",
			"icon": "🏛️",
			"effects": {"structural_load_mult": 1.30}
		}
	}

func init_relics() -> void:
	relics = {
		"true_hearth_shard": {
			"id": "true_hearth_shard",
			"name": "Shard of the True Hearth",
			"desc": "Spiritual ember of the ancient founding hearth. Prevents hypothermia and grants +15% warmth.",
			"icon": "🔥",
			"blessing": {"warmth_bonus": 15.0, "frost_immunity": true}
		},
		"first_monarch_crown": {
			"id": "first_monarch_crown",
			"name": "Crown of the First Sovereign",
			"desc": "Golden circlet worn by the kingdom's founder. Grants +25% sovereign renown and +10 opinion.",
			"icon": "👑",
			"blessing": {"renown_mult": 1.25, "diplomatic_opinion": 10.0}
		},
		"st_columba_tome": {
			"id": "st_columba_tome",
			"name": "Tome of St. Columba",
			"desc": "Sacred illuminated parchment. Accelerates scriptoria research speed by +40%.",
			"icon": "📖",
			"blessing": {"research_speed_mult": 1.40}
		},
		"perpetual_chalice": {
			"id": "perpetual_chalice",
			"name": "Chalice of Perpetual Abundance",
			"desc": "Holy vessel sanctifying water and wheat. +20% farm harvest yield and -25% citizen hunger drain.",
			"icon": "🏆",
			"blessing": {"harvest_bonus": 1.20, "hunger_drain_mult": 0.75}
		},
		"holy_light_banner": {
			"id": "holy_light_banner",
			"name": "Banner of the Holy Light",
			"desc": "Consecrated silver silk standard. Grants +20% garrison morale and repels nighttime raiders.",
			"icon": "🚩",
			"blessing": {"garrison_morale_bonus": 20.0, "raid_suppression": 0.30}
		}
	}

func _process(delta: float) -> void:
	# Passive research generation from monk scribes
	if assigned_monk_scribes > 0 and current_research_id != "":
		var speed_mult = 1.0
		# Check Tome of St. Columba blessing
		for slot in active_altar_relics.keys():
			if active_altar_relics[slot] == "st_columba_tome":
				speed_mult *= 1.40

		var points_generated = (assigned_monk_scribes * 0.75 * speed_mult) * delta
		add_research_progress(points_generated)

	# Bell blessing decay
	if bell_blessing_active:
		bell_blessing_timer -= delta
		if bell_blessing_timer <= 0.0:
			bell_blessing_active = false

func start_research(tech_id: String) -> bool:
	if not technologies.has(tech_id):
		return false
	if unlocked_techs.has(tech_id):
		return false

	current_research_id = tech_id
	if not research_progress.has(tech_id):
		research_progress[tech_id] = 0.0

	var tech = technologies[tech_id]
	research_started.emit(tech_id, tech["name"], tech["cost"])
	return true

func add_research_progress(points: float) -> void:
	if current_research_id == "":
		scholar_points += points
		return

	var tech = technologies.get(current_research_id)
	if not tech:
		return

	var cur = research_progress.get(current_research_id, 0.0) + points
	var cost = float(tech["cost"])

	if cur >= cost:
		research_progress[current_research_id] = cost
		unlocked_techs.append(current_research_id)
		var completed_tech_id = current_research_id
		current_research_id = ""
		research_completed.emit(completed_tech_id, tech["name"])
	else:
		research_progress[current_research_id] = cur
		research_progress_updated.emit(current_research_id, cur, cost)

func is_tech_unlocked(tech_id: String) -> bool:
	return unlocked_techs.has(tech_id)

func assign_monks(delta_count: int) -> int:
	assigned_monk_scribes = clampi(assigned_monk_scribes + delta_count, 0, 10)
	return assigned_monk_scribes

# ----------------- Sacred Relic Enshrinement -----------------
func enshrine_relic(slot_index: int, relic_id: String) -> bool:
	if slot_index < 0 or slot_index > 2:
		return false
	if not relics.has(relic_id):
		return false
	if not discovered_relics.has(relic_id):
		return false

	# Ensure relic is not already in another slot
	for s in active_altar_relics.keys():
		if active_altar_relics[s] == relic_id:
			active_altar_relics[s] = ""

	active_altar_relics[slot_index] = relic_id
	var r = relics[relic_id]
	relic_enshrined.emit(relic_id, r["name"], slot_index)
	return true

func remove_relic(slot_index: int) -> bool:
	if slot_index < 0 or slot_index > 2:
		return false
	var old = active_altar_relics.get(slot_index, "")
	if old != "":
		active_altar_relics[slot_index] = ""
		relic_removed.emit(old, slot_index)
		return true
	return false

func ring_abbey_bells() -> Dictionary:
	bell_blessing_active = true
	bell_blessing_timer = BELL_BLESSING_DURATION
	abbey_bell_rung.emit("Grace of the High Abbey (+30% Citizen Serenity)")
	return {
		"success": true,
		"duration": BELL_BLESSING_DURATION,
		"morale_boost": 30.0
	}

func get_active_blessings() -> Dictionary:
	var combined: Dictionary = {}
	for slot in active_altar_relics.keys():
		var rid = active_altar_relics[slot]
		if rid != "" and relics.has(rid):
			var b = relics[rid]["blessing"]
			for k in b.keys():
				combined[k] = b[k]
	if bell_blessing_active:
		combined["abbey_bell_serenity"] = 30.0
	return combined

# ----------------- Persistence -----------------
func to_dict() -> Dictionary:
	var altar_serialized: Dictionary = {}
	for s in active_altar_relics.keys():
		altar_serialized[str(s)] = active_altar_relics[s]

	return {
		"scholar_points": scholar_points,
		"assigned_monk_scribes": assigned_monk_scribes,
		"current_research_id": current_research_id,
		"research_progress": research_progress,
		"unlocked_techs": unlocked_techs,
		"active_altar_relics": altar_serialized,
		"discovered_relics": discovered_relics,
		"bell_blessing_active": bell_blessing_active,
		"bell_blessing_timer": bell_blessing_timer
	}

func from_dict(data: Dictionary) -> void:
	if data.is_empty():
		return
	scholar_points = data.get("scholar_points", 0.0)
	assigned_monk_scribes = data.get("assigned_monk_scribes", 3)
	current_research_id = data.get("current_research_id", "")
	if data.has("research_progress"):
		research_progress = data["research_progress"]
	if data.has("unlocked_techs"):
		unlocked_techs.clear()
		for t in data["unlocked_techs"]:
			unlocked_techs.append(str(t))
	if data.has("active_altar_relics"):
		for s in data["active_altar_relics"].keys():
			active_altar_relics[int(s)] = str(data["active_altar_relics"][s])
	if data.has("discovered_relics"):
		discovered_relics.clear()
		for r in data["discovered_relics"]:
			discovered_relics.append(str(r))
	bell_blessing_active = data.get("bell_blessing_active", false)
	bell_blessing_timer = data.get("bell_blessing_timer", 0.0)
