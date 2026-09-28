# scripts/world/world_assembler.gd
# Voxel Lord: Feudal Realm - Milestone 43: Master World Assembler
# Unites all 112 3D models across 8 distinct historical feudal districts,
# connecting road networks, workstations, fortifications, and agriculture.

class_name WorldAssembler
extends Node3D

signal district_assembled(district_name: String, center_pos: Vector3)
signal world_assembly_completed(total_structures: int, district_count: int)

enum DistrictType {
	CITADEL,
	TOWN_SQUARE,
	STEAM_AND_FORGE,
	HARBOR_AND_DOCKS,
	MINING_RAIL,
	OBSERVATORY,
	AGRICULTURE_NORFOLK,
	WILDERNESS_OUTPOSTS
}

const DISTRICT_NAMES: Dictionary = {
	DistrictType.CITADEL: "Royal Citadel & Fortifications",
	DistrictType.TOWN_SQUARE: "Medieval Town & Market Square",
	DistrictType.STEAM_AND_FORGE: "High-Pressure Steam & Heavy Metallurgy Quarter",
	DistrictType.HARBOR_AND_DOCKS: "Maritime Harbor, Slipway & Quayside",
	DistrictType.MINING_RAIL: "Subterranean Mining & Steam Rail Terminal",
	DistrictType.OBSERVATORY: "Renaissance Clockwork Observatory",
	DistrictType.AGRICULTURE_NORFOLK: "Norfolk 4-Year Crop Rotation Agronomy",
	DistrictType.WILDERNESS_OUTPOSTS: "Frontier Redoubts, Bandit Lairs & Crypts"
}

# District Center Coordinates (in Voxel World Units, for 64x64 to 128x128 grid)
const DISTRICT_CENTERS: Dictionary = {
	DistrictType.CITADEL: Vector3(32.0, 0.0, 32.0),
	DistrictType.TOWN_SQUARE: Vector3(48.0, 0.0, 32.0),
	DistrictType.STEAM_AND_FORGE: Vector3(48.0, 0.0, 48.0),
	DistrictType.HARBOR_AND_DOCKS: Vector3(64.0, 0.0, 16.0),
	DistrictType.MINING_RAIL: Vector3(16.0, 0.0, 16.0),
	DistrictType.OBSERVATORY: Vector3(32.0, 0.0, 56.0),
	DistrictType.AGRICULTURE_NORFOLK: Vector3(16.0, 0.0, 48.0),
	DistrictType.WILDERNESS_OUTPOSTS: Vector3(60.0, 0.0, 60.0)
}

# Complete Catalog of 112 GLB Models mapped to Districts
const MODEL_DISTRICT_MAP: Dictionary = {
	# 1. Citadel
	"watchtower": DistrictType.CITADEL,
	"portcullis_gate": DistrictType.CITADEL,
	"drawbridge_platform": DistrictType.CITADEL,
	"drawbridge_winch": DistrictType.CITADEL,
	"masonry_buttress": DistrictType.CITADEL,
	"spiked_barricade": DistrictType.CITADEL,
	"trebuchet_siege": DistrictType.CITADEL,
	"battering_ram": DistrictType.CITADEL,
	"siege_tower": DistrictType.CITADEL,
	"catapult": DistrictType.CITADEL,
	"pitch_cauldron": DistrictType.CITADEL,
	"guard_post": DistrictType.CITADEL,
	"armory_rack": DistrictType.CITADEL,
	"training_dummy": DistrictType.CITADEL,
	"war_horn": DistrictType.CITADEL,
	"outpost_banner": DistrictType.CITADEL,
	"sword": DistrictType.CITADEL,
	"arrow": DistrictType.CITADEL,
	"hunting_bow": DistrictType.CITADEL,

	# 2. Town Square
	"town_hall_desk": DistrictType.TOWN_SQUARE,
	"treasury_vault": DistrictType.TOWN_SQUARE,
	"architect_desk": DistrictType.TOWN_SQUARE,
	"burgage_coop": DistrictType.TOWN_SQUARE,
	"water_well": DistrictType.TOWN_SQUARE,
	"caravan_cart": DistrictType.TOWN_SQUARE,
	"tax_sheriff_cart": DistrictType.TOWN_SQUARE,
	"wheelbarrow": DistrictType.TOWN_SQUARE,
	"crate": DistrictType.TOWN_SQUARE,
	"loot_chest": DistrictType.TOWN_SQUARE,
	"paved_road_tile": DistrictType.TOWN_SQUARE,
	"road_signpost": DistrictType.TOWN_SQUARE,
	"street_lamp": DistrictType.TOWN_SQUARE,
	"wall_sconce": DistrictType.TOWN_SQUARE,
	"candle_candelabra": DistrictType.TOWN_SQUARE,
	"citizen": DistrictType.TOWN_SQUARE,

	# 3. Steam & Forge
	"steam_boiler": DistrictType.STEAM_AND_FORGE,
	"steam_engine_drive": DistrictType.STEAM_AND_FORGE,
	"centrifugal_governor": DistrictType.STEAM_AND_FORGE,
	"furnace": DistrictType.STEAM_AND_FORGE,
	"furnace_tuyere": DistrictType.STEAM_AND_FORGE,
	"mechanical_bellows": DistrictType.STEAM_AND_FORGE,
	"industrial_trip_hammer": DistrictType.STEAM_AND_FORGE,
	"smeltery_controller": DistrictType.STEAM_AND_FORGE,
	"casting_basin": DistrictType.STEAM_AND_FORGE,
	"casting_table": DistrictType.STEAM_AND_FORGE,
	"crucible": DistrictType.STEAM_AND_FORGE,
	"bloomery": DistrictType.STEAM_AND_FORGE,
	"anvil": DistrictType.STEAM_AND_FORGE,
	"trip_hammer": DistrictType.STEAM_AND_FORGE,
	"charcoal_pit": DistrictType.STEAM_AND_FORGE,
	"mechanical_press": DistrictType.STEAM_AND_FORGE,
	"drive_shaft": DistrictType.STEAM_AND_FORGE,
	"bevel_gearbox": DistrictType.STEAM_AND_FORGE,
	"mechanical_clutch": DistrictType.STEAM_AND_FORGE,
	"conveyor_belt": DistrictType.STEAM_AND_FORGE,
	"chute": DistrictType.STEAM_AND_FORGE,
	"pickaxe": DistrictType.STEAM_AND_FORGE,

	# 4. Harbor & Docks
	"drydock_slipway": DistrictType.HARBOR_AND_DOCKS,
	"quayside_crane": DistrictType.HARBOR_AND_DOCKS,
	"fluyt_cargo_ship": DistrictType.HARBOR_AND_DOCKS,
	"treadwheel_crane": DistrictType.HARBOR_AND_DOCKS,
	"water_cask": DistrictType.HARBOR_AND_DOCKS,

	# 5. Mining & Rail
	"mine_locomotive": DistrictType.MINING_RAIL,
	"rail_switch": DistrictType.MINING_RAIL,
	"hopper_unloader": DistrictType.MINING_RAIL,
	"mine_dewatering_pump": DistrictType.MINING_RAIL,
	"mine_ventilator": DistrictType.MINING_RAIL,
	"mining_capstan": DistrictType.MINING_RAIL,
	"mine_cart": DistrictType.MINING_RAIL,
	"support_beam": DistrictType.MINING_RAIL,
	"mining_lantern": DistrictType.MINING_RAIL,
	"prospector_pick": DistrictType.MINING_RAIL,

	# 6. Observatory & Science
	"astronomical_clock": DistrictType.OBSERVATORY,
	"armillary_sphere": DistrictType.OBSERVATORY,
	"celestial_orrery": DistrictType.OBSERVATORY,
	"barometer_station": DistrictType.OBSERVATORY,
	"weather_vane": DistrictType.OBSERVATORY,
	"enchanter_table": DistrictType.OBSERVATORY,
	"gem_cutting_table": DistrictType.OBSERVATORY,

	# 7. Agriculture (Norfolk)
	"windmill": DistrictType.AGRICULTURE_NORFOLK,
	"stone_windmill": DistrictType.AGRICULTURE_NORFOLK,
	"water_wheel": DistrictType.AGRICULTURE_NORFOLK,
	"millstone": DistrictType.AGRICULTURE_NORFOLK,
	"baker_oven": DistrictType.AGRICULTURE_NORFOLK,
	"flour_silo": DistrictType.AGRICULTURE_NORFOLK,
	"compost_bin": DistrictType.AGRICULTURE_NORFOLK,
	"pasture_barn": DistrictType.AGRICULTURE_NORFOLK,
	"sheep_pen": DistrictType.AGRICULTURE_NORFOLK,
	"feeding_trough": DistrictType.AGRICULTURE_NORFOLK,
	"beehive_skep": DistrictType.AGRICULTURE_NORFOLK,
	"mead_fermenter": DistrictType.AGRICULTURE_NORFOLK,
	"apothecary_bench": DistrictType.AGRICULTURE_NORFOLK,
	"medicine_chest": DistrictType.AGRICULTURE_NORFOLK,
	"infirmary_bed": DistrictType.AGRICULTURE_NORFOLK,
	"hunting_lodge": DistrictType.AGRICULTURE_NORFOLK,
	"fur_drying_rack": DistrictType.AGRICULTURE_NORFOLK,
	"smoke_rack": DistrictType.AGRICULTURE_NORFOLK,
	"tannery_vat": DistrictType.AGRICULTURE_NORFOLK,
	"cutting_board": DistrictType.AGRICULTURE_NORFOLK,
	"cooking_pot": DistrictType.AGRICULTURE_NORFOLK,
	"campfire": DistrictType.AGRICULTURE_NORFOLK,
	"axe": DistrictType.AGRICULTURE_NORFOLK,
	"workbench": DistrictType.AGRICULTURE_NORFOLK,
	"aqueduct_pipe": DistrictType.AGRICULTURE_NORFOLK,

	# 8. Wilderness & Frontiers
	"crypt_entrance": DistrictType.WILDERNESS_OUTPOSTS,
	"stone_sarcophagus": DistrictType.WILDERNESS_OUTPOSTS,
	"funeral_pyre": DistrictType.WILDERNESS_OUTPOSTS,
	"runestone": DistrictType.WILDERNESS_OUTPOSTS,
	"bandit_tent": DistrictType.WILDERNESS_OUTPOSTS,
	"bandit": DistrictType.WILDERNESS_OUTPOSTS,
	"bandit_warlord": DistrictType.WILDERNESS_OUTPOSTS,
	"boss_trophy": DistrictType.WILDERNESS_OUTPOSTS
}

var voxel_world: VoxelWorld
var game_manager: GameManager
var assembled_structures: Array[Dictionary] = []
var district_nodes: Dictionary = {} # DistrictType -> Node3D

func _init(p_voxel_world: VoxelWorld = null, p_game_manager: GameManager = null) -> void:
	voxel_world = p_voxel_world
	game_manager = p_game_manager

func assemble_complete_realm() -> Dictionary:
	print("[WORLD ASSEMBLER] Initiating Total Realism World Assembly across 8 historical districts...")
	assembled_structures.clear()

	for dtype in DISTRICT_NAMES.keys():
		var district_node = Node3D.new()
		district_node.name = "District_%s" % DISTRICT_NAMES[dtype].replace(" ", "_")
		add_child(district_node)
		district_nodes[dtype] = district_node

	# Assemble each district
	_assemble_citadel()
	_assemble_town_square()
	_assemble_steam_and_forge()
	_assemble_harbor_and_docks()
	_assemble_mining_rail()
	_assemble_observatory()
	_assemble_agriculture_norfolk()
	_assemble_wilderness_outposts()

	var summary = {
		"total_structures": assembled_structures.size(),
		"total_districts": DISTRICT_NAMES.size(),
		"models_placed": assembled_structures.size(),
		"citadel_center": DISTRICT_CENTERS[DistrictType.CITADEL],
		"town_center": DISTRICT_CENTERS[DistrictType.TOWN_SQUARE],
		"steam_center": DISTRICT_CENTERS[DistrictType.STEAM_AND_FORGE],
		"harbor_center": DISTRICT_CENTERS[DistrictType.HARBOR_AND_DOCKS],
		"mining_center": DISTRICT_CENTERS[DistrictType.MINING_RAIL],
		"observatory_center": DISTRICT_CENTERS[DistrictType.OBSERVATORY],
		"agriculture_center": DISTRICT_CENTERS[DistrictType.AGRICULTURE_NORFOLK],
		"wilderness_center": DISTRICT_CENTERS[DistrictType.WILDERNESS_OUTPOSTS]
	}

	world_assembly_completed.emit(summary.total_structures, summary.total_districts)
	print("[WORLD ASSEMBLER] Successfully assembled %d structures across %d feudal districts!" % [summary.total_structures, summary.total_districts])
	return summary

func _get_surface_y(x: float, z: float) -> float:
	if voxel_world:
		return float(voxel_world.get_surface_height(int(x), int(z)))
	return 12.0

func _place_landmark(model_name: String, district_type: DistrictType, local_offset: Vector3, rotation_y: float = 0.0) -> Node3D:
	var base_pos = DISTRICT_CENTERS.get(district_type, Vector3.ZERO)
	var target_x = base_pos.x + local_offset.x
	var target_z = base_pos.z + local_offset.z
	var surface_y = _get_surface_y(target_x, target_z) + local_offset.y
	var world_pos = Vector3(target_x, surface_y, target_z)

	var landmark_node = Node3D.new()
	landmark_node.name = "%s_%d" % [model_name, assembled_structures.size()]
	landmark_node.position = world_pos
	landmark_node.rotation.y = rotation_y

	# Try loading GLB model if available in resource loader
	var glb_path = "res://assets/models/%s.glb" % model_name
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res and scene_res is PackedScene:
			var instance = scene_res.instantiate()
			landmark_node.add_child(instance)

	var parent_node = district_nodes.get(district_type, self)
	parent_node.add_child(landmark_node)

	var structure_meta = {
		"name": model_name,
		"district": district_type,
		"district_name": DISTRICT_NAMES[district_type],
		"position": world_pos,
		"rotation_y": rotation_y,
		"node": landmark_node
	}
	assembled_structures.append(structure_meta)
	return landmark_node

# -------------------------------------------------------------
# District Assemblers
# -------------------------------------------------------------

func _assemble_citadel() -> void:
	var dt = DistrictType.CITADEL
	_place_landmark("portcullis_gate", dt, Vector3(0.0, 0.0, -8.0))
	_place_landmark("drawbridge_platform", dt, Vector3(0.0, 0.0, -11.0))
	_place_landmark("drawbridge_winch", dt, Vector3(2.5, 0.0, -8.0))
	_place_landmark("watchtower", dt, Vector3(-10.0, 0.0, -10.0))
	_place_landmark("watchtower", dt, Vector3(10.0, 0.0, -10.0))
	_place_landmark("watchtower", dt, Vector3(-10.0, 0.0, 10.0))
	_place_landmark("watchtower", dt, Vector3(10.0, 0.0, 10.0))
	_place_landmark("masonry_buttress", dt, Vector3(-10.0, 0.0, 0.0))
	_place_landmark("masonry_buttress", dt, Vector3(10.0, 0.0, 0.0))
	_place_landmark("trebuchet_siege", dt, Vector3(-6.0, 0.0, 6.0))
	_place_landmark("battering_ram", dt, Vector3(0.0, 0.0, 8.0))
	_place_landmark("siege_tower", dt, Vector3(6.0, 0.0, 6.0))
	_place_landmark("catapult", dt, Vector3(-4.0, 0.0, -2.0))
	_place_landmark("pitch_cauldron", dt, Vector3(2.0, 3.0, -8.0))
	_place_landmark("guard_post", dt, Vector3(4.0, 0.0, -4.0))
	_place_landmark("armory_rack", dt, Vector3(-4.0, 0.0, -4.0))
	_place_landmark("training_dummy", dt, Vector3(-2.0, 0.0, 2.0))
	_place_landmark("war_horn", dt, Vector3(0.0, 1.0, 0.0))
	_place_landmark("outpost_banner", dt, Vector3(0.0, 4.0, -8.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func _assemble_town_square() -> void:
	var dt = DistrictType.TOWN_SQUARE
	_place_landmark("town_hall_desk", dt, Vector3(0.0, 0.0, 0.0))
	_place_landmark("treasury_vault", dt, Vector3(4.0, 0.0, -2.0))
	_place_landmark("architect_desk", dt, Vector3(-4.0, 0.0, -2.0))
	_place_landmark("water_well", dt, Vector3(0.0, 0.0, 6.0))
	_place_landmark("burgage_coop", dt, Vector3(-8.0, 0.0, 4.0))
	_place_landmark("burgage_coop", dt, Vector3(8.0, 0.0, 4.0))
	_place_landmark("caravan_cart", dt, Vector3(-4.0, 0.0, 8.0))
	_place_landmark("tax_sheriff_cart", dt, Vector3(4.0, 0.0, 8.0))
	_place_landmark("wheelbarrow", dt, Vector3(-2.0, 0.0, 5.0))
	_place_landmark("crate", dt, Vector3(3.0, 0.0, 4.0))
	_place_landmark("loot_chest", dt, Vector3(4.5, 0.0, -1.0))
	_place_landmark("road_signpost", dt, Vector3(0.0, 0.0, 10.0))
	_place_landmark("street_lamp", dt, Vector3(-3.0, 0.0, 0.0))
	_place_landmark("street_lamp", dt, Vector3(3.0, 0.0, 0.0))
	_place_landmark("paved_road_tile", dt, Vector3(0.0, 0.0, 3.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func _assemble_steam_and_forge() -> void:
	var dt = DistrictType.STEAM_AND_FORGE
	_place_landmark("steam_boiler", dt, Vector3(0.0, 0.0, 0.0))
	_place_landmark("steam_engine_drive", dt, Vector3(3.5, 0.0, 0.0))
	_place_landmark("centrifugal_governor", dt, Vector3(3.5, 0.0, 2.5))
	_place_landmark("furnace", dt, Vector3(-4.0, 0.0, 0.0))
	_place_landmark("furnace_tuyere", dt, Vector3(-4.0, 0.0, 1.5))
	_place_landmark("mechanical_bellows", dt, Vector3(-4.0, 0.0, 3.0))
	_place_landmark("industrial_trip_hammer", dt, Vector3(0.0, 0.0, 4.5))
	_place_landmark("smeltery_controller", dt, Vector3(-2.0, 0.0, -3.0))
	_place_landmark("bloomery", dt, Vector3(-4.5, 0.0, -3.0))
	_place_landmark("anvil", dt, Vector3(2.0, 0.0, -3.0))
	_place_landmark("crucible", dt, Vector3(-1.0, 0.0, -1.5))
	_place_landmark("casting_basin", dt, Vector3(1.0, 0.0, -1.5))
	_place_landmark("casting_table", dt, Vector3(2.5, 0.0, -1.5))
	_place_landmark("charcoal_pit", dt, Vector3(-6.0, 0.0, 4.0))
	_place_landmark("mechanical_press", dt, Vector3(5.5, 0.0, 4.0))
	_place_landmark("drive_shaft", dt, Vector3(2.0, 0.0, 1.5))
	_place_landmark("bevel_gearbox", dt, Vector3(0.0, 0.0, 2.5))
	_place_landmark("mechanical_clutch", dt, Vector3(1.0, 0.0, 2.5))
	_place_landmark("conveyor_belt", dt, Vector3(-1.5, 0.0, 5.0))
	_place_landmark("chute", dt, Vector3(-1.5, 1.5, 6.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func _assemble_harbor_and_docks() -> void:
	var dt = DistrictType.HARBOR_AND_DOCKS
	_place_landmark("drydock_slipway", dt, Vector3(0.0, 0.0, 0.0))
	_place_landmark("fluyt_cargo_ship", dt, Vector3(0.0, -0.5, -6.0))
	_place_landmark("quayside_crane", dt, Vector3(5.0, 0.0, 2.0))
	_place_landmark("treadwheel_crane", dt, Vector3(-5.0, 0.0, 2.0))
	_place_landmark("water_cask", dt, Vector3(3.0, 0.0, 4.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func _assemble_mining_rail() -> void:
	var dt = DistrictType.MINING_RAIL
	_place_landmark("mine_locomotive", dt, Vector3(0.0, 0.0, 0.0))
	_place_landmark("mine_cart", dt, Vector3(0.0, 0.0, 3.5))
	_place_landmark("rail_switch", dt, Vector3(0.0, 0.0, -4.0))
	_place_landmark("hopper_unloader", dt, Vector3(4.0, 0.0, 0.0))
	_place_landmark("mine_dewatering_pump", dt, Vector3(-4.0, 0.0, 2.0))
	_place_landmark("mine_ventilator", dt, Vector3(-4.0, 0.0, -2.0))
	_place_landmark("mining_capstan", dt, Vector3(0.0, 0.0, 7.0))
	_place_landmark("support_beam", dt, Vector3(-2.0, 0.0, -5.0))
	_place_landmark("mining_lantern", dt, Vector3(1.5, 1.5, 0.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func _assemble_observatory() -> void:
	var dt = DistrictType.OBSERVATORY
	_place_landmark("astronomical_clock", dt, Vector3(0.0, 0.0, 0.0))
	_place_landmark("armillary_sphere", dt, Vector3(4.0, 0.0, 2.0))
	_place_landmark("celestial_orrery", dt, Vector3(-4.0, 0.0, 2.0))
	_place_landmark("barometer_station", dt, Vector3(3.0, 0.0, -3.0))
	_place_landmark("weather_vane", dt, Vector3(0.0, 4.5, 0.0))
	_place_landmark("enchanter_table", dt, Vector3(-3.0, 0.0, -3.0))
	_place_landmark("gem_cutting_table", dt, Vector3(0.0, 0.0, 4.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func _assemble_agriculture_norfolk() -> void:
	var dt = DistrictType.AGRICULTURE_NORFOLK
	_place_landmark("windmill", dt, Vector3(0.0, 0.0, 0.0))
	_place_landmark("stone_windmill", dt, Vector3(8.0, 0.0, 0.0))
	_place_landmark("water_wheel", dt, Vector3(-6.0, 0.0, -4.0))
	_place_landmark("millstone", dt, Vector3(1.5, 0.0, 2.0))
	_place_landmark("baker_oven", dt, Vector3(4.0, 0.0, 3.0))
	_place_landmark("flour_silo", dt, Vector3(-3.0, 0.0, 2.0))
	_place_landmark("compost_bin", dt, Vector3(-5.0, 0.0, 5.0))
	_place_landmark("pasture_barn", dt, Vector3(6.0, 0.0, -6.0))
	_place_landmark("sheep_pen", dt, Vector3(10.0, 0.0, -6.0))
	_place_landmark("feeding_trough", dt, Vector3(8.0, 0.0, -4.0))
	_place_landmark("beehive_skep", dt, Vector3(-6.0, 0.0, 8.0))
	_place_landmark("mead_fermenter", dt, Vector3(-4.0, 0.0, 8.0))
	_place_landmark("hunting_lodge", dt, Vector3(-8.0, 0.0, 0.0))
	_place_landmark("fur_drying_rack", dt, Vector3(-10.0, 0.0, 2.0))
	_place_landmark("smoke_rack", dt, Vector3(-8.0, 0.0, 4.0))
	_place_landmark("tannery_vat", dt, Vector3(-10.0, 0.0, -2.0))
	_place_landmark("apothecary_bench", dt, Vector3(3.0, 0.0, 6.0))
	_place_landmark("medicine_chest", dt, Vector3(4.5, 0.0, 6.0))
	_place_landmark("infirmary_bed", dt, Vector3(6.0, 0.0, 6.0))
	_place_landmark("campfire", dt, Vector3(0.0, 0.0, 6.0))
	_place_landmark("cooking_pot", dt, Vector3(0.0, 0.5, 6.0))
	_place_landmark("cutting_board", dt, Vector3(1.5, 0.0, 6.0))
	_place_landmark("workbench", dt, Vector3(0.0, 0.0, -4.0))
	_place_landmark("aqueduct_pipe", dt, Vector3(-6.0, 0.0, -2.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func _assemble_wilderness_outposts() -> void:
	var dt = DistrictType.WILDERNESS_OUTPOSTS
	_place_landmark("crypt_entrance", dt, Vector3(0.0, 0.0, 0.0))
	_place_landmark("stone_sarcophagus", dt, Vector3(0.0, 0.0, 3.0))
	_place_landmark("funeral_pyre", dt, Vector3(-4.0, 0.0, -2.0))
	_place_landmark("runestone", dt, Vector3(4.0, 0.0, -2.0))
	_place_landmark("bandit_tent", dt, Vector3(6.0, 0.0, 4.0))
	_place_landmark("bandit_warlord", dt, Vector3(6.0, 0.0, 6.0))
	_place_landmark("spiked_barricade", dt, Vector3(3.0, 0.0, 3.0))
	_place_landmark("boss_trophy", dt, Vector3(0.0, 1.0, 0.0))
	district_assembled.emit(DISTRICT_NAMES[dt], DISTRICT_CENTERS[dt])

func get_district_center(district_type: DistrictType) -> Vector3:
	return DISTRICT_CENTERS.get(district_type, Vector3(32.0, 12.0, 32.0))

func get_district_info(district_type: DistrictType) -> Dictionary:
	var center = get_district_center(district_type)
	var name_str = DISTRICT_NAMES.get(district_type, "Unknown District")
	var count = 0
	for s in assembled_structures:
		if s.district == district_type:
			count += 1
	return {
		"type": district_type,
		"name": name_str,
		"center": center,
		"structure_count": count
	}
