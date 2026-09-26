# scripts/world/crypt_dungeon.gd
# Voxel Lord: Feudal Realm - Milestone 28: Subterranean Crypt Dungeon Generation
# Procedural multi-chamber underground tombs, light occlusion, and guardian alert triggers.

class_name CryptDungeon
extends RefCounted

signal guardian_awakened(room_id: String, guardian_type: String)
signal room_discovered(room_id: String, room_type: String)

enum RoomType {
	ENTRANCE_VESTIBULE,
	PILLARED_GALLERY,
	BURIAL_CHAMBER,
	CORRIDOR
}

var dungeon_seed: int = 1337
var entry_position: Vector3 = Vector3(0, -20, 0)
var ambient_light_level: float = 0.05
var ambient_fog_density: float = 0.04
var rooms: Array[Dictionary] = []

func _init(p_seed: int = 1337, p_entry: Vector3 = Vector3(0, -20, 0)) -> void:
	dungeon_seed = p_seed
	entry_position = p_entry

func generate_crypt(room_count: int = 4) -> Dictionary:
	rooms.clear()
	var rng = RandomNumberGenerator.new()
	rng.seed = dungeon_seed

	# 1. Entrance Vestibule
	var vestibule = {
		"id": "room_0_vestibule",
		"type": "ENTRANCE_VESTIBULE",
		"position": entry_position,
		"size": Vector3(8, 4, 8),
		"sarcophagi_count": 0,
		"sconces_count": 2,
		"guardians": [],
		"cleared": true
	}
	rooms.append(vestibule)

	# 2. Sequential subterranean chambers connected by depth
	var current_pos = entry_position + Vector3(0, -2, 10)
	for i in range(1, room_count):
		var r_type: String
		var sarc_count: int = 0
		var sconce_count: int = 1
		var guardians: Array = []

		if i == room_count - 1:
			r_type = "BURIAL_CHAMBER"
			sarc_count = 2
			sconce_count = 4
			guardians.append("CryptSkeletonKnight")
			guardians.append("CryptDraugr")
		elif i % 2 == 1:
			r_type = "PILLARED_GALLERY"
			sarc_count = 1
			sconce_count = 3
			guardians.append("CryptSkeletonArcher")
		else:
			r_type = "CORRIDOR"
			sconce_count = 1

		var room_data = {
			"id": f"room_{i}_{r_type.to_lower()}",
			"type": r_type,
			"position": current_pos,
			"size": Vector3(10, 4, 12) if r_type == "BURIAL_CHAMBER" else Vector3(6, 3, 8),
			"sarcophagi_count": sarc_count,
			"sconces_count": sconce_count,
			"guardians": guardians,
			"cleared": false
		}
		rooms.append(room_data)
		current_pos += Vector3(rng.randf_range(-4, 4), -1.5, 12)

	return {
		"total_rooms": rooms.size(),
		"rooms": rooms,
		"ambient_light": ambient_light_level,
		"fog_density": ambient_fog_density
	}

func trigger_room_alert(room_id: String) -> Array:
	var awakened: Array = []
	for r in rooms:
		if r["id"] == room_id and not r["cleared"]:
			for g in r["guardians"]:
				awakened.append(g)
				guardian_awakened.emit(room_id, g)
	return awakened

func clear_room(room_id: String) -> bool:
	for r in rooms:
		if r["id"] == room_id:
			r["cleared"] = true
			return true
	return false

func is_player_in_darkness(player_pos: Vector3, active_lights: Array) -> bool:
	for light in active_lights:
		if light.get("lit", false):
			var dist = player_pos.distance_to(light.get("pos", Vector3.ZERO))
			if dist <= light.get("radius", 6.0):
				return false # Player illuminated
	return true # Pitch black
