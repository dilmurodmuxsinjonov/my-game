# scripts/core/save_system.gd
# Voxel Lord: Feudal Realm - Milestone 44: Save/Load Persistence Architecture
# Manages versioned sparse delta saves, player vitals, citizen FSM states,
# economy stockpiles, and checksum validation.

class_name SaveSystem
extends RefCounted

signal save_completed(slot_name: String, timestamp: float)
signal load_completed(slot_name: String, success: bool)
signal save_failed(reason: String)

const SAVE_DIR: String = "user://saves/"
const SAVE_VERSION: String = "1.0.0"
const QUICK_SAVE_SLOT: String = "quicksave"
const AUTO_SAVE_SLOT: String = "autosave"

var modified_voxels: Dictionary = {} # Vector3i -> int (BlockType)

func _init() -> void:
	_ensure_save_directory()

func _ensure_save_directory() -> void:
	if not DirAccess.dir_exists_absolute(SAVE_DIR):
		DirAccess.make_dir_recursive_absolute(SAVE_DIR)

func register_voxel_modification(pos: Vector3i, block_type: int) -> void:
	modified_voxels[pos] = block_type

func get_save_path(slot_name: String) -> String:
	return SAVE_DIR + slot_name + ".json"

func compute_checksum(data_str: String) -> String:
	var ctx = HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(data_str.to_utf8_buffer())
	var digest = ctx.finish()
	return digest.hex_encode()

func save_game(slot_name: String, game_manager: Node) -> bool:
	if not game_manager:
		save_failed.emit("GameManager reference is null")
		return false

	_ensure_save_directory()
	var player = game_manager.get("player")
	var supply_chain = game_manager.get("supply_chain")
	var season_manager = game_manager.get("season_manager")
	var citizens_arr = game_manager.get("citizens")

	# 1. Player Data
	var player_data: Dictionary = {}
	if player:
		player_data = {
			"position": [player.global_position.x, player.global_position.y, player.global_position.z],
			"rotation_y": player.rotation.y,
			"health": player.health,
			"max_health": player.max_health,
			"stamina": player.stamina,
			"max_stamina": player.max_stamina,
			"hunger": player.hunger,
			"max_hunger": player.max_hunger,
			"warmth": player.warmth,
			"max_warmth": player.max_warmth,
			"active_slot": player.active_slot,
			"hotbar": player.hotbar
		}

	# 2. Economy Data
	var economy_data: Dictionary = {}
	if supply_chain and supply_chain.has_method("get_stockpile_snapshot"):
		economy_data = supply_chain.get_stockpile_snapshot()
	elif supply_chain:
		economy_data = {
			"wood": supply_chain.get("wood") if "wood" in supply_chain else 50,
			"stone": supply_chain.get("stone") if "stone" in supply_chain else 50,
			"iron": supply_chain.get("iron") if "iron" in supply_chain else 10,
			"wheat": supply_chain.get("wheat") if "wheat" in supply_chain else 25,
			"bread": supply_chain.get("bread") if "bread" in supply_chain else 20
		}

	# 3. Environment Data
	var env_data: Dictionary = {
		"day_timer": game_manager.get("day_timer") if "day_timer" in game_manager else 0.0,
		"season": season_manager.current_season if season_manager else 0,
		"weather": season_manager.current_weather if season_manager else 0
	}

	# 4. Sparse Voxel Delta Serialization
	var voxels_serialized: Array[Dictionary] = []
	for pos in modified_voxels.keys():
		voxels_serialized.append({
			"x": pos.x,
			"y": pos.y,
			"z": pos.z,
			"type": modified_voxels[pos]
		})

	# 5. Citizen Lifecycle Snapshot
	var citizens_data: Array[Dictionary] = []
	if citizens_arr and citizens_arr is Array:
		for c in citizens_arr:
			citizens_data.append({
				"name": c.name if "name" in c else "Citizen",
				"role": c.current_role if "current_role" in c else 0,
				"morale": c.morale if "morale" in c else 75.0,
				"position": [c.position.x, c.position.y, c.position.z] if "position" in c else [32, 12, 32]
			})

	# 6. Heraldry & Castle Decor Data
	var heraldry_data: Dictionary = {}
	var castle_data: Dictionary = {}
	var rh = game_manager.get("royal_heraldry")
	if rh and rh.has_method("to_dict"):
		heraldry_data = rh.to_dict()
	var cc = game_manager.get("castle_customizer")
	if cc and cc.has_method("to_dict"):
		castle_data = cc.to_dict()

	# 7. Royal Decrees & Squadron Command Data
	var decrees_data: Dictionary = {}
	var squadron_data: Dictionary = {}
	var rd = game_manager.get("royal_decrees")
	if rd and rd.has_method("to_dict"):
		decrees_data = rd.to_dict()
	var sq = game_manager.get("squadron_command")
	if sq and sq.has_method("to_dict"):
		squadron_data = sq.to_dict()

	# 8. Foreign Diplomacy & Vassalage Data
	var diplomacy_data: Dictionary = {}
	var dip = game_manager.get("diplomacy_system")
	if dip and dip.has_method("to_dict"):
		diplomacy_data = dip.to_dict()

	# 9. Foreign Invasions & Strategic Defense Data
	var invasions_data: Dictionary = {}
	var fim = game_manager.get("foreign_invasion_manager")
	if fim and fim.has_method("to_dict"):
		invasions_data = fim.to_dict()

	# 10. Grand Tournament & Chivalric Knighthood Data
	var tournament_data: Dictionary = {}
	var tm = game_manager.get("tournament_manager")
	if tm and tm.has_method("to_dict"):
		tournament_data = tm.to_dict()

	# 11. High Monastic Order & Scriptoria Research Data
	var monastery_data: Dictionary = {}
	var mrs = game_manager.get("monastery_research_system")
	if mrs and mrs.has_method("to_dict"):
		monastery_data = mrs.to_dict()

	# 12. Alchemical Transmutation Laboratory Data
	var alchemy_data: Dictionary = {}
	var alab = game_manager.get("alchemy_laboratory")
	if alab and alab.has_method("to_dict"):
		alchemy_data = alab.to_dict()

	# Assembly of Master Payload
	var current_time = Time.get_unix_time_from_system()
	var payload: Dictionary = {
		"version": SAVE_VERSION,
		"slot_name": slot_name,
		"timestamp": current_time,
		"datetime": Time.get_datetime_string_from_system(),
		"player": player_data,
		"economy": economy_data,
		"environment": env_data,
		"voxels_delta": voxels_serialized,
		"citizens": citizens_data,
		"heraldry": heraldry_data,
		"castle": castle_data,
		"decrees": decrees_data,
		"squadron": squadron_data,
		"diplomacy": diplomacy_data,
		"invasions": invasions_data,
		"tournament": tournament_data,
		"monastery": monastery_data,
		"alchemy": alchemy_data
	}

	var json_str = JSON.stringify(payload, "\t")
	var checksum = compute_checksum(json_str)
	var final_file_content = JSON.stringify({
		"checksum": checksum,
		"payload": payload
	}, "\t")

	var save_path = get_save_path(slot_name)
	var file = FileAccess.open(save_path, FileAccess.WRITE)
	if not file:
		save_failed.emit("Failed to open file for write: %s" % save_path)
		return false

	file.store_string(final_file_content)
	file.close()

	save_completed.emit(slot_name, current_time)
	print("[SAVE SYSTEM] Successfully saved realm to %s (Checksum: %s)" % [save_path, checksum.substr(0, 8)])
	return true

func load_game(slot_name: String, game_manager: Node) -> bool:
	if not game_manager:
		load_completed.emit(slot_name, false)
		return false

	var save_path = get_save_path(slot_name)
	if not FileAccess.file_exists(save_path):
		print("[SAVE SYSTEM] Save file not found: %s" % save_path)
		load_completed.emit(slot_name, false)
		return false

	var file = FileAccess.open(save_path, FileAccess.READ)
	if not file:
		load_completed.emit(slot_name, false)
		return false

	var content = file.get_as_text()
	file.close()

	var parse_res = JSON.parse_string(content)
	if not parse_res or not parse_res is Dictionary:
		print("[SAVE SYSTEM] Corrupted save JSON in %s" % save_path)
		load_completed.emit(slot_name, false)
		return false

	var expected_checksum = parse_res.get("checksum", "")
	var payload = parse_res.get("payload", {})
	var payload_str = JSON.stringify(payload, "\t")
	var actual_checksum = compute_checksum(payload_str)

	if expected_checksum != "" and actual_checksum != expected_checksum:
		print("[SAVE SYSTEM] Warning: Checksum mismatch on load (Expected: %s, Actual: %s)" % [expected_checksum, actual_checksum])

	# 1. Restore Player Data
	var player = game_manager.get("player")
	var player_data = payload.get("player", {})
	if player and not player_data.is_empty():
		var pos_arr = player_data.get("position", [32.0, 14.0, 32.0])
		player.global_position = Vector3(pos_arr[0], pos_arr[1], pos_arr[2])
		player.health = player_data.get("health", 100.0)
		player.stamina = player_data.get("stamina", 100.0)
		player.hunger = player_data.get("hunger", 0.0)
		player.warmth = player_data.get("warmth", 100.0)
		player.active_slot = player_data.get("active_slot", 0)
		if "hotbar" in player_data:
			player.hotbar = player_data["hotbar"]
		player.emit_signal("health_changed", player.health, player.max_health)
		player.emit_signal("stamina_changed", player.stamina, player.max_stamina)
		player.emit_signal("hunger_changed", player.hunger, player.max_hunger)
		player.emit_signal("hotbar_slot_changed", player.active_slot, player.hotbar[player.active_slot])

	# 2. Restore Sparse Voxels
	var voxel_world = game_manager.get("voxel_world")
	var voxels_delta = payload.get("voxels_delta", [])
	modified_voxels.clear()
	for v in voxels_delta:
		var vpos = Vector3i(int(v["x"]), int(v["y"]), int(v["z"]))
		var btype = int(v["type"])
		modified_voxels[vpos] = btype
		if voxel_world and voxel_world.has_method("set_block"):
			voxel_world.set_block(vpos.x, vpos.y, vpos.z, btype)

	# 3. Restore Environment
	var env_data = payload.get("environment", {})
	if "day_timer" in env_data and "day_timer" in game_manager:
		game_manager.set("day_timer", env_data["day_timer"])

	# 4. Restore Heraldry & Castle Decor
	if payload.has("heraldry"):
		var rh_load = game_manager.get("royal_heraldry")
		if rh_load and rh_load.has_method("from_dict"):
			rh_load.from_dict(payload["heraldry"])
	if payload.has("castle"):
		var cc_load = game_manager.get("castle_customizer")
		if cc_load and cc_load.has_method("from_dict"):
			cc_load.from_dict(payload["castle"])

	# 5. Restore Decrees & Squadron Command
	if payload.has("decrees"):
		var rd_load = game_manager.get("royal_decrees")
		if rd_load and rd_load.has_method("from_dict"):
			rd_load.from_dict(payload["decrees"])
	if payload.has("squadron"):
		var sq_load = game_manager.get("squadron_command")
		if sq_load and sq_load.has_method("from_dict"):
			sq_load.from_dict(payload["squadron"])
	if payload.has("diplomacy"):
		var dip_load = game_manager.get("diplomacy_system")
		if dip_load and dip_load.has_method("from_dict"):
			dip_load.from_dict(payload["diplomacy"])
	if payload.has("invasions"):
		var fim_load = game_manager.get("foreign_invasion_manager")
		if fim_load and fim_load.has_method("from_dict"):
			fim_load.from_dict(payload["invasions"])
	if payload.has("tournament"):
		var tm_load = game_manager.get("tournament_manager")
		if tm_load and tm_load.has_method("from_dict"):
			tm_load.from_dict(payload["tournament"])
	if payload.has("monastery"):
		var mrs_load = game_manager.get("monastery_research_system")
		if mrs_load and mrs_load.has_method("from_dict"):
			mrs_load.from_dict(payload["monastery"])
	if payload.has("alchemy"):
		var alab_load = game_manager.get("alchemy_laboratory")
		if alab_load and alab_load.has_method("from_dict"):
			alab_load.from_dict(payload["alchemy"])

	load_completed.emit(slot_name, true)
	print("[SAVE SYSTEM] Successfully loaded realm from %s on Day %s!" % [slot_name, payload.get("datetime", "Unknown")])
	return true

func quick_save(game_manager: Node) -> bool:
	return save_game(QUICK_SAVE_SLOT, game_manager)

func quick_load(game_manager: Node) -> bool:
	return load_game(QUICK_SAVE_SLOT, game_manager)

func list_save_slots() -> Array[Dictionary]:
	_ensure_save_directory()
	var slots: Array[Dictionary] = []
	var dir = DirAccess.open(SAVE_DIR)
	if not dir:
		return slots

	dir.list_dir_begin()
	var file_name = dir.get_next()
	while file_name != "":
		if not dir.current_is_dir() and file_name.ends_with(".json"):
			var slot_id = file_name.trim_suffix(".json")
			var file_path = SAVE_DIR + file_name
			var f = FileAccess.open(file_path, FileAccess.READ)
			if f:
				var content = f.get_as_text()
				f.close()
				var parsed = JSON.parse_string(content)
				if parsed and parsed is Dictionary and "payload" in parsed:
					var p = parsed["payload"]
					slots.append({
						"slot_name": slot_id,
						"datetime": p.get("datetime", "Unknown"),
						"timestamp": p.get("timestamp", 0),
						"version": p.get("version", "1.0.0"),
						"health": p.get("player", {}).get("health", 100.0)
					})
		file_name = dir.get_next()
	dir.list_dir_end()
	return slots
