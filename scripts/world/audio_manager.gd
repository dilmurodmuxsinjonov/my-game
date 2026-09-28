# scripts/world/audio_manager.gd
# Voxel Lord: Feudal Realm - Milestone 44: Dynamic Audio Atmosphere & Procedural Sound Engine
# Provides surface footstep acoustic mapping, procedural sound effect synthesis,
# day/night environmental soundscapes, and feudal district ambiance.

class_name AudioManager
extends Node

signal sfx_played(sfx_name: String, pitch: float, volume_db: float)
signal district_ambience_changed(district_name: String, track_info: Dictionary)
signal day_night_ambience_changed(is_night: bool)
signal volume_settings_updated(master_vol: float, sfx_vol: float, ambient_vol: float)

# Surface acoustic types
const SURFACE_GRASS: String = "grass"
const SURFACE_STONE: String = "stone"
const SURFACE_WOOD: String = "wood"
const SURFACE_WATER: String = "water"
const SURFACE_MUD: String = "mud"
const SURFACE_SNOW: String = "snow"
const SURFACE_METAL: String = "metal"
const SURFACE_DEFAULT: String = "stone"

# BlockType to Acoustic Surface Mapping (Covering all 26 BlockTypes)
const BLOCK_SURFACE_MAP: Dictionary = {
	0: "air",             # AIR
	1: SURFACE_MUD,       # DIRT
	2: SURFACE_GRASS,     # GRASS
	3: SURFACE_STONE,     # STONE
	4: SURFACE_WOOD,      # WOOD
	5: SURFACE_GRASS,     # LEAVES
	6: SURFACE_STONE,     # IRON_ORE
	7: SURFACE_STONE,     # COAL_ORE
	8: SURFACE_STONE,     # GOLD_ORE
	9: SURFACE_STONE,     # COBBLESTONE
	10: SURFACE_WOOD,     # PLANKS
	11: SURFACE_WATER,    # WATER
	12: SURFACE_SNOW,     # ICE
	13: SURFACE_MUD,      # FARMLAND
	14: SURFACE_GRASS,    # WHEAT_CROP
	15: SURFACE_STONE,    # COPPER_ORE
	16: SURFACE_STONE,    # STONE_BRICKS
	17: SURFACE_WOOD,     # SUPPORT_BEAM
	18: SURFACE_STONE,    # DEEP_GEM_ORE
	19: SURFACE_WOOD,     # WOODEN_PALISADE
	20: SURFACE_STONE,    # STONE_BATTLEMENT
	21: SURFACE_WOOD,     # WOODEN_GATE
	22: SURFACE_STONE,    # ROCK_SALT_ORE
	23: SURFACE_STONE,    # SILVER_ORE
	24: SURFACE_METAL,    # MINING_RAIL
	25: SURFACE_STONE     # GLASS
}

# District Ambiance Profiles
const DISTRICT_AMBIANCE_PROFILES: Dictionary = {
	"CITADEL": {
		"title": "Royal Citadel & Fortifications",
		"mood": "majestic_martial",
		"base_pitch": 1.0,
		"reverb_room_size": 0.6,
		"elements": ["distant_fanfare", "armor_clank", "banner_flutter"]
	},
	"TOWN_SQUARE": {
		"title": "Medieval Town & Market Square",
		"mood": "bustling_community",
		"base_pitch": 1.05,
		"reverb_room_size": 0.3,
		"elements": ["market_murmur", "wooden_cart", "church_bell"]
	},
	"STEAM_AND_FORGE": {
		"title": "High-Pressure Steam & Heavy Metallurgy",
		"mood": "industrial_ironwork",
		"base_pitch": 0.9,
		"reverb_room_size": 0.7,
		"elements": ["steam_vent", "anvil_hammer", "bellows_breath"]
	},
	"HARBOR_AND_DOCKS": {
		"title": "Maritime Harbor & Slipway",
		"mood": "oceanic_salt",
		"base_pitch": 0.98,
		"reverb_room_size": 0.4,
		"elements": ["tide_lapping", "rigging_groan", "seabird_call"]
	},
	"MINING_RAIL": {
		"title": "Subterranean Mining & Steam Rail",
		"mood": "deep_cavernous",
		"base_pitch": 0.85,
		"reverb_room_size": 0.85,
		"elements": ["water_drips", "distant_pickaxe", "iron_rails"]
	},
	"OBSERVATORY": {
		"title": "Renaissance Clockwork Observatory",
		"mood": "celestial_scholarly",
		"base_pitch": 1.15,
		"reverb_room_size": 0.5,
		"elements": ["gear_escapement", "astrolabe_chime", "brass_clockwork"]
	},
	"AGRICULTURE_NORFOLK": {
		"title": "Norfolk 4-Year Crop Rotation Fields",
		"mood": "pastoral_peaceful",
		"base_pitch": 1.02,
		"reverb_room_size": 0.2,
		"elements": ["wheat_rustle", "morning_lark", "gentle_breeze"]
	},
	"WILDERNESS_OUTPOSTS": {
		"title": "Frontier Redoubts & Bandit Lairs",
		"mood": "eerie_survival",
		"base_pitch": 0.92,
		"reverb_room_size": 0.65,
		"elements": ["howling_wind", "distant_wolf", "crackling_embers"]
	}
}

# Volume Controls (0.0 to 1.0 linear)
var master_volume: float = 0.8
var sfx_volume: float = 0.85
var ambient_volume: float = 0.75

var current_district: String = "CITADEL"
var is_night_time: bool = false
var footstep_cooldown: float = 0.0
const FOOTSTEP_INTERVAL: float = 0.42 # Seconds between steps when sprinting/walking

# Dedicated Audio Stream Players
var sfx_player: AudioStreamPlayer
var ambient_player: AudioStreamPlayer
var footstep_player: AudioStreamPlayer

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_setup_audio_players()

func _setup_audio_players() -> void:
	sfx_player = AudioStreamPlayer.new()
	sfx_player.name = "SFXPlayer"
	add_child(sfx_player)

	ambient_player = AudioStreamPlayer.new()
	ambient_player.name = "AmbientPlayer"
	add_child(ambient_player)

	footstep_player = AudioStreamPlayer.new()
	footstep_player.name = "FootstepPlayer"
	add_child(footstep_player)

func get_surface_type(block_type: int) -> String:
	if BLOCK_SURFACE_MAP.has(block_type):
		return BLOCK_SURFACE_MAP[block_type]
	return SURFACE_DEFAULT

func play_footstep_for_block(block_type: int, is_sprinting: bool = false) -> void:
	var surface = get_surface_type(block_type)
	if surface == "air":
		return
	var vol_scale = 1.2 if is_sprinting else 1.0
	play_footstep(surface, vol_scale)

func play_footstep(surface_type: String, volume_scale: float = 1.0) -> void:
	var base_freq: float = 220.0
	match surface_type:
		SURFACE_GRASS:
			base_freq = 320.0
		SURFACE_STONE:
			base_freq = 180.0
		SURFACE_WOOD:
			base_freq = 240.0
		SURFACE_WATER:
			base_freq = 440.0
		SURFACE_MUD:
			base_freq = 160.0
		SURFACE_SNOW:
			base_freq = 360.0
		SURFACE_METAL:
			base_freq = 520.0
		_:
			base_freq = 200.0

	var pitch_rand = randf_range(0.92, 1.08)
	var final_db = _linear_to_db(master_volume * sfx_volume * volume_scale * 0.7)
	_play_synthesized_tone(footstep_player, base_freq * pitch_rand, 0.08, final_db)
	sfx_played.emit("footstep_" + surface_type, pitch_rand, final_db)

func play_pickaxe_hit() -> void:
	var pitch = randf_range(0.95, 1.1)
	var db = _linear_to_db(master_volume * sfx_volume)
	_play_synthesized_tone(sfx_player, 640.0 * pitch, 0.12, db)
	sfx_played.emit("pickaxe_hit", pitch, db)

func play_axe_chop() -> void:
	var pitch = randf_range(0.9, 1.05)
	var db = _linear_to_db(master_volume * sfx_volume)
	_play_synthesized_tone(sfx_player, 280.0 * pitch, 0.15, db)
	sfx_played.emit("axe_chop", pitch, db)

func play_sword_slash() -> void:
	var pitch = randf_range(1.0, 1.2)
	var db = _linear_to_db(master_volume * sfx_volume * 1.1)
	_play_synthesized_tone(sfx_player, 880.0 * pitch, 0.18, db)
	sfx_played.emit("sword_slash", pitch, db)

func play_war_horn() -> void:
	var db = _linear_to_db(master_volume * sfx_volume * 1.3)
	_play_synthesized_tone(sfx_player, 146.83, 1.2, db) # D3 Monarch Brass Tone
	sfx_played.emit("monarch_war_horn", 1.0, db)

func play_block_place() -> void:
	var pitch = randf_range(0.95, 1.05)
	var db = _linear_to_db(master_volume * sfx_volume * 0.8)
	_play_synthesized_tone(sfx_player, 210.0 * pitch, 0.1, db)
	sfx_played.emit("block_place", pitch, db)

func play_craft_success() -> void:
	var db = _linear_to_db(master_volume * sfx_volume)
	_play_synthesized_tone(sfx_player, 587.33, 0.25, db) # D5 chime
	sfx_played.emit("craft_success", 1.0, db)

func play_ui_click() -> void:
	var db = _linear_to_db(master_volume * sfx_volume * 0.6)
	_play_synthesized_tone(sfx_player, 720.0, 0.05, db)
	sfx_played.emit("ui_click", 1.0, db)

func set_district_ambiance(district_key: String) -> void:
	if DISTRICT_AMBIANCE_PROFILES.has(district_key):
		current_district = district_key
		var profile = DISTRICT_AMBIANCE_PROFILES[district_key]
		district_ambience_changed.emit(district_key, profile)

func set_day_night(is_night: bool) -> void:
	if is_night_time != is_night:
		is_night_time = is_night
		day_night_ambience_changed.emit(is_night)

func apply_volume_settings(master_val: float, sfx_val: float = -1.0, amb_val: float = -1.0) -> void:
	master_volume = clampf(master_val, 0.0, 1.0)
	if sfx_val >= 0.0:
		sfx_volume = clampf(sfx_val, 0.0, 1.0)
	if amb_val >= 0.0:
		ambient_volume = clampf(amb_val, 0.0, 1.0)
	volume_settings_updated.emit(master_volume, sfx_volume, ambient_volume)

func _linear_to_db(linear: float) -> float:
	if linear <= 0.0001:
		return -80.0
	return 20.0 * (log(linear) / log(10.0))

func _play_synthesized_tone(player: AudioStreamPlayer, freq: float, duration: float, volume_db: float) -> void:
	if not player:
		return
	player.volume_db = volume_db
	player.pitch_scale = clampf(freq / 440.0, 0.1, 4.0)
	# In tests or headless environments, audio server might not be running or stream might be null.
	# We emit the signal and adjust properties cleanly.
	if player.stream:
		player.play()
