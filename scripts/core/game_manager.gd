class_name GameManager
extends Node3D

## Master Game Coordinator for Voxel Lord: Feudal Realm.
## Links VoxelWorld, Player, Citizens, SupplyChain, Workstations, GameHUD, CraftingMenu, and RoyalLedger.

@onready var voxel_world: VoxelWorld = $VoxelWorld
@onready var player: Player = $Player
@onready var hud: GameHUD = $UI/HUD
@onready var royal_ledger: RoyalLedger = $UI/RoyalLedger
@onready var crafting_menu: CraftingMenu = $UI/CraftingMenu

const WorldAssembler = preload("res://scripts/world/world_assembler.gd")
const SaveSystem = preload("res://scripts/core/save_system.gd")
const PauseMenu = preload("res://scripts/ui/pause_menu.gd")
const AudioManager = preload("res://scripts/world/audio_manager.gd")
const QuestManager = preload("res://scripts/quests/quest_manager.gd")
const CitizenDialogue = preload("res://scripts/entities/citizen_dialogue.gd")
const QuestJournal = preload("res://scripts/ui/quest_journal.gd")
const RoyalHeraldry = preload("res://scripts/entities/royal_heraldry.gd")
const AtmosphericPostProcess = preload("res://scripts/world/atmospheric_post_process.gd")
const CastleCustomizer = preload("res://scripts/world/castle_customizer.gd")
const HeraldryCustomizerUI = preload("res://scripts/ui/heraldry_customizer_ui.gd")
const RoyalDecrees = preload("res://scripts/core/royal_decrees.gd")
const SquadronCommand = preload("res://scripts/combat/squadron_command.gd")
const DecreesCommandUI = preload("res://scripts/ui/decrees_command_ui.gd")

var save_system: SaveSystem = null
var audio_manager: AudioManager = null
var pause_menu: PauseMenu = null
var quest_manager: QuestManager = null
var citizen_dialogue: CitizenDialogue = null
var quest_journal: QuestJournal = null
var royal_heraldry: RoyalHeraldry = null
var atmospheric_system: AtmosphericPostProcess = null
var castle_customizer: CastleCustomizer = null
var heraldry_ui: HeraldryCustomizerUI = null
var royal_decrees: RoyalDecrees = null
var squadron_command: SquadronCommand = null
var decrees_ui: DecreesCommandUI = null
var diplomacy_system: DiplomacySystem = null
var diplomacy_ui: DiplomacyUI = null
var foreign_invasion_manager: ForeignInvasionManager = null
var war_room_ui: WarRoomUI = null
var tournament_manager: TournamentManager = null
var tournament_ui: TournamentUI = null
var monastery_research_system: MonasteryResearchSystem = null
var alchemy_laboratory: AlchemyLaboratory = null
var monastery_ui: MonasteryUI = null
var espionage_manager: EspionageManager = null
var espionage_ui: EspionageUI = null

var supply_chain: SupplyChain
var citizens: Array[Citizen] = []
var workstations: Array[Workstation] = []
var agriculture_manager: AgricultureManager
var threat_manager: ThreatManager
var season_manager: SeasonManager
var world_assembler: WorldAssembler = null
var current_district_index: int = 0
var active_caravans: Array[TradeCaravan] = []
var caravan_timer: float = 0.0
var caravan_interval: float = 160.0

# Game day/night simulation
var day_timer: float = 0.0
var day_duration: float = 120.0 # 2 minutes per full day cycle
var sun_light: DirectionalLight3D
var is_royal_alarm_active: bool = false

func _ready() -> void:
	supply_chain = SupplyChain.new()
	sun_light = $DirectionalLight3D
	
	# Initialize Agriculture, Threat & Season Systems
	agriculture_manager = AgricultureManager.new(voxel_world, supply_chain)
	agriculture_manager.name = "AgricultureManager"
	add_child(agriculture_manager)
	agriculture_manager.crop_matured.connect(_on_crop_matured)
	agriculture_manager.crop_harvested.connect(_on_crop_harvested)

	threat_manager = ThreatManager.new(voxel_world, supply_chain)
	threat_manager.name = "ThreatManager"
	add_child(threat_manager)
	threat_manager.raid_spawned.connect(_on_raid_spawned)
	threat_manager.raid_defeated.connect(_on_raid_defeated)
	threat_manager.bandit_slain.connect(_on_bandit_slain)
	
	season_manager = SeasonManager.new(agriculture_manager)
	season_manager.name = "SeasonManager"
	add_child(season_manager)
	season_manager.season_changed.connect(_on_season_changed)
	season_manager.weather_changed.connect(_on_weather_changed)
	
	# Initialize Audio System
	audio_manager = AudioManager.new()
	audio_manager.name = "AudioManager"
	add_child(audio_manager)

	# Initialize Persistence System
	save_system = SaveSystem.new()
	
	# Wire up player
	if player:
		player.voxel_world = voxel_world
		player.supply_chain = supply_chain
		threat_manager.player_ref = player
		player.open_crafting_requested.connect(_on_open_crafting)
		player.interact_requested.connect(_on_interact_requested)
		player.block_action_performed.connect(_on_player_block_action)
		player.war_horn_sounded.connect(_on_war_horn_sounded)
		player.cycle_district_requested.connect(_on_cycle_district)
		player.toggle_ledger_requested.connect(_on_toggle_ledger)
		player.toggle_pause_requested.connect(_on_toggle_pause)
		player.quick_save_requested.connect(_on_quick_save)
		player.quick_load_requested.connect(_on_quick_load)
		player.footstep_stepped.connect(_on_player_footstep)
		player.toggle_journal_requested.connect(_on_toggle_journal)
		player.toggle_heraldry_requested.connect(_on_toggle_heraldry)
		player.toggle_decrees_requested.connect(_on_toggle_decrees)
		player.toggle_diplomacy_requested.connect(_on_toggle_diplomacy)
		player.toggle_war_room_requested.connect(_on_toggle_war_room)
		player.toggle_tournament_requested.connect(_on_toggle_tournament)
		player.toggle_monastery_requested.connect(_on_toggle_monastery)
		player.toggle_espionage_requested.connect(_on_toggle_espionage)
		
		# Position player on top of surface terrain at spawn
		var spawn_x = 32
		var spawn_z = 32
		var surface_y = voxel_world.get_surface_height(spawn_x, spawn_z)
		player.global_position = Vector3(spawn_x + 0.5, surface_y + 2.0, spawn_z + 0.5)
		player.respawn_position = player.global_position
		
		if hud:
			hud.bind_player(player)
			
	# Wire up UI
	if royal_ledger:
		royal_ledger.supply_chain = supply_chain
		royal_ledger.role_reassigned.connect(_on_role_reassigned)

	if crafting_menu:
		crafting_menu.player = player
		crafting_menu.supply_chain = supply_chain
		crafting_menu.item_crafted.connect(_on_item_crafted)

	# Setup Pause & Settings Menu
	pause_menu = get_node_or_null("UI/PauseMenu") as PauseMenu
	if not pause_menu:
		pause_menu = PauseMenu.new()
		pause_menu.name = "PauseMenu"
		var ui_node = get_node_or_null("UI")
		if ui_node:
			ui_node.add_child(pause_menu)
		else:
			add_child(pause_menu)
	pause_menu.save_system = save_system
	pause_menu.resume_requested.connect(_on_menu_resumed)
	pause_menu.save_requested.connect(_on_menu_save_requested)
	pause_menu.load_requested.connect(_on_menu_load_requested)
	pause_menu.settings_applied.connect(_on_settings_applied)

	# Initialize Quest Progression System
	quest_manager = QuestManager.new()
	quest_manager.name = "QuestManager"
	add_child(quest_manager)
	quest_manager.quest_completed.connect(_on_quest_completed)
	quest_manager.monarch_title_promoted.connect(_on_monarch_title_promoted)
	quest_manager.realm_victory_achieved.connect(_on_realm_victory_achieved)

	# Initialize Citizen Dialogue UI
	citizen_dialogue = get_node_or_null("UI/CitizenDialogue") as CitizenDialogue
	if not citizen_dialogue:
		citizen_dialogue = CitizenDialogue.new()
		citizen_dialogue.name = "CitizenDialogue"
		var ui_node_d = get_node_or_null("UI")
		if ui_node_d:
			ui_node_d.add_child(citizen_dialogue)
		else:
			add_child(citizen_dialogue)
	citizen_dialogue.supply_chain = supply_chain

	# Initialize Quest Journal UI
	quest_journal = get_node_or_null("UI/QuestJournal") as QuestJournal
	if not quest_journal:
		quest_journal = QuestJournal.new()
		quest_journal.name = "QuestJournal"
		var ui_node_j = get_node_or_null("UI")
		if ui_node_j:
			ui_node_j.add_child(quest_journal)
		else:
			add_child(quest_journal)
	quest_journal.quest_manager = quest_manager
	quest_journal.supply_chain = supply_chain

	# Initialize Royal Heraldry, Castle Decor & Atmospheric Systems
	royal_heraldry = RoyalHeraldry.new()
	royal_heraldry.name = "RoyalHeraldry"
	add_child(royal_heraldry)
	royal_heraldry.heraldry_changed.connect(_on_heraldry_updated)

	castle_customizer = CastleCustomizer.new()
	castle_customizer.name = "CastleCustomizer"
	add_child(castle_customizer)

	atmospheric_system = AtmosphericPostProcess.new()
	atmospheric_system.name = "AtmosphericPostProcess"
	add_child(atmospheric_system)

	# Wire up Heraldry UI
	heraldry_ui = get_node_or_null("UI/HeraldryCustomizerUI") as HeraldryCustomizerUI
	if not heraldry_ui:
		heraldry_ui = HeraldryCustomizerUI.new()
		heraldry_ui.name = "HeraldryCustomizerUI"
		var ui_node_h = get_node_or_null("UI")
		if ui_node_h:
			ui_node_h.add_child(heraldry_ui)
		else:
			add_child(heraldry_ui)
	heraldry_ui.setup(royal_heraldry, castle_customizer, supply_chain)

	# Initialize Royal Decrees & Garrison Squadron Command
	royal_decrees = RoyalDecrees.new()
	royal_decrees.name = "RoyalDecrees"
	add_child(royal_decrees)
	royal_decrees.decree_proclaimed.connect(_on_decree_proclaimed)
	royal_decrees.decree_expired.connect(_on_decree_expired)

	squadron_command = SquadronCommand.new()
	squadron_command.name = "SquadronCommand"
	add_child(squadron_command)
	squadron_command.stance_changed.connect(_on_squad_stance_changed)
	squadron_command.formation_changed.connect(_on_squad_formation_changed)

	# Wire up Decrees & Military Command UI
	decrees_ui = get_node_or_null("UI/DecreesCommandUI") as DecreesCommandUI
	if not decrees_ui:
		decrees_ui = DecreesCommandUI.new()
		decrees_ui.name = "DecreesCommandUI"
		var ui_node_dec = get_node_or_null("UI")
		if ui_node_dec:
			ui_node_dec.add_child(decrees_ui)
		else:
			add_child(decrees_ui)
	decrees_ui.setup(royal_decrees, squadron_command, supply_chain, quest_manager)
	decrees_ui.rally_requested.connect(_on_squad_rally_requested)

	# Initialize Foreign Diplomacy & Vassalage System
	diplomacy_system = DiplomacySystem.new()
	diplomacy_system.name = "DiplomacySystem"
	add_child(diplomacy_system)
	diplomacy_system.tribute_received.connect(_on_vassal_tribute_received)
	diplomacy_system.war_declared.connect(_on_diplomatic_war_declared)

	# Wire up Chancery UI
	diplomacy_ui = get_node_or_null("UI/DiplomacyUI") as DiplomacyUI
	if not diplomacy_ui:
		diplomacy_ui = DiplomacyUI.new()
		diplomacy_ui.name = "DiplomacyUI"
		var ui_node_dip = get_node_or_null("UI")
		if ui_node_dip:
			ui_node_dip.add_child(diplomacy_ui)
		else:
			add_child(diplomacy_ui)
	diplomacy_ui.setup(diplomacy_system, supply_chain)

	# Initialize Strategic Foreign Invasion & Siege Defense Engine
	foreign_invasion_manager = ForeignInvasionManager.new()
	foreign_invasion_manager.name = "ForeignInvasionManager"
	add_child(foreign_invasion_manager)
	foreign_invasion_manager.invasion_begun.connect(_on_invasion_begun)
	foreign_invasion_manager.outpost_attacked.connect(_on_outpost_attacked)
	foreign_invasion_manager.outpost_breached.connect(_on_outpost_breached)
	foreign_invasion_manager.battalion_routed.connect(_on_battalion_routed)

	# Wire up Royal War Room UI
	war_room_ui = get_node_or_null("UI/WarRoomUI") as WarRoomUI
	if not war_room_ui:
		war_room_ui = WarRoomUI.new()
		war_room_ui.name = "WarRoomUI"
		var ui_node_wr = get_node_or_null("UI")
		if ui_node_wr:
			ui_node_wr.add_child(war_room_ui)
		else:
			add_child(war_room_ui)
	war_room_ui.setup(foreign_invasion_manager, squadron_command, supply_chain)
	war_room_ui.rally_alarm_requested.connect(_on_war_horn_sounded)

	# Initialize Grand Feudal Tournament & Chivalric Knighthood System
	tournament_manager = TournamentManager.new()
	tournament_manager.name = "TournamentManager"
	add_child(tournament_manager)
	tournament_manager.tournament_victorious.connect(_on_tournament_victorious)
	tournament_manager.grand_feast_hosted.connect(_on_grand_feast_hosted)
	tournament_manager.chivalric_title_unlocked.connect(_on_chivalric_title_unlocked)

	# Wire up Grand Tournament UI
	tournament_ui = get_node_or_null("UI/TournamentUI") as TournamentUI
	if not tournament_ui:
		tournament_ui = TournamentUI.new()
		tournament_ui.name = "TournamentUI"
		var ui_node_tr = get_node_or_null("UI")
		if ui_node_tr:
			ui_node_tr.add_child(tournament_ui)
		else:
			add_child(tournament_ui)
	tournament_ui.setup(tournament_manager, supply_chain)

	# Initialize High Scholastic Monastic Order & Scriptoria Tech Tree
	monastery_research_system = MonasteryResearchSystem.new()
	monastery_research_system.name = "MonasteryResearchSystem"
	add_child(monastery_research_system)
	monastery_research_system.research_completed.connect(_on_monastery_research_completed)
	monastery_research_system.relic_enshrined.connect(_on_relic_enshrined)
	monastery_research_system.abbey_bell_rung.connect(_on_abbey_bell_rung)

	# Initialize Alchemical Transmutation Laboratory
	alchemy_laboratory = AlchemyLaboratory.new()
	alchemy_laboratory.name = "AlchemyLaboratory"
	add_child(alchemy_laboratory)
	alchemy_laboratory.potion_brewed.connect(_on_alchemy_potion_brewed)
	alchemy_laboratory.metal_transmuted.connect(_on_alchemy_metal_transmuted)

	# Wire up Monastery & Alchemy UI
	monastery_ui = get_node_or_null("UI/MonasteryUI") as MonasteryUI
	if not monastery_ui:
		monastery_ui = MonasteryUI.new()
		monastery_ui.name = "MonasteryUI"
		var ui_node_mo = get_node_or_null("UI")
		if ui_node_mo:
			ui_node_mo.add_child(monastery_ui)
		else:
			add_child(monastery_ui)
	monastery_ui.setup(monastery_research_system, alchemy_laboratory, supply_chain)

	# Initialize Royal Spymaster & Shadow Intrigue Network (Milestone 52)
	espionage_manager = EspionageManager.new()
	espionage_manager.name = "EspionageManager"
	add_child(espionage_manager)
	espionage_manager.agent_recruited.connect(_on_espionage_agent_recruited)
	espionage_manager.operation_resolved.connect(_on_espionage_op_resolved)
	espionage_manager.counter_intel_triggered.connect(_on_counter_intel_triggered)
	espionage_manager.prisoner_interrogated.connect(_on_prisoner_interrogated)

	# Wire up Espionage UI
	espionage_ui = get_node_or_null("UI/EspionageUI") as EspionageUI
	if not espionage_ui:
		espionage_ui = EspionageUI.new()
		espionage_ui.name = "EspionageUI"
		var ui_node_esp = get_node_or_null("UI")
		if ui_node_esp:
			ui_node_esp.add_child(espionage_ui)
		else:
			add_child(espionage_ui)
	espionage_ui.set_espionage_manager(espionage_manager, supply_chain)
		
	# Spawn initial workstations, citizens, and trade caravan
	_spawn_initial_workstations()
	_spawn_initial_citizens()
	spawn_trade_caravan()
	
	# Assemble all 112 3D models across 8 feudal districts
	world_assembler = WorldAssembler.new(voxel_world, self)
	world_assembler.name = "WorldAssembler"
	add_child(world_assembler)
	world_assembler.assemble_complete_realm()
	
	print("[GAME MANAGER] Voxel Lord realm successfully initialized!")

func _spawn_initial_workstations() -> void:
	# 1. Carpentry Workbench
	var wb = Workstation.new(Workstation.StationType.WORKBENCH)
	var wb_y = voxel_world.get_surface_height(34, 32)
	wb.position = Vector3(34.5, wb_y + 1.0, 32.5)
	add_child(wb)
	workstations.append(wb)

	# 2. Settlement Campfire with warm glow
	var cf = Workstation.new(Workstation.StationType.CAMPFIRE)
	var cf_y = voxel_world.get_surface_height(32, 29)
	cf.position = Vector3(32.5, cf_y + 1.0, 29.5)
	add_child(cf)
	workstations.append(cf)

	# 3. Timber Stockpile Crate
	var cr = Workstation.new(Workstation.StationType.CRATE)
	var cr_y = voxel_world.get_surface_height(36, 32)
	cr.position = Vector3(36.5, cr_y + 1.0, 32.5)
	add_child(cr)
	workstations.append(cr)

	# 4. Stone Bloomery Furnace
	var fn = Workstation.new(Workstation.StationType.FURNACE)
	var fn_y = voxel_world.get_surface_height(30, 32)
	fn.position = Vector3(30.5, fn_y + 1.0, 32.5)
	add_child(fn)
	workstations.append(fn)

	# 5. Defensive Watchtower
	var wt = Watchtower.new()
	var wt_y = voxel_world.get_surface_height(28, 28)
	wt.position = Vector3(28.5, wt_y + 0.1, 28.5)
	add_child(wt)

	# 6. Arcane Enchanter's Table
	var et = EnchanterTable.new()
	var et_y = voxel_world.get_surface_height(34, 30)
	et.position = Vector3(34.5, et_y + 0.1, 30.5)
	add_child(et)

	# 7. Farmer's Delight Hearth Cooking Pot
	var cp = CookingPot.new()
	var cp_y = voxel_world.get_surface_height(32, 34)
	cp.position = Vector3(32.5, cp_y + 0.1, 34.5)
	add_child(cp)

	# 8. Create-Style Kinetic Windmill & Milling Tower
	var wm = Windmill.new()
	wm.supply_chain = supply_chain
	var wm_y = voxel_world.get_surface_height(38, 38)
	wm.position = Vector3(38.5, wm_y + 0.1, 38.5)
	add_child(wm)

func _spawn_initial_citizens() -> void:
	var roles_to_spawn = [
		{"role": Citizen.Role.FARMER, "name": "Geoffrey"},
		{"role": Citizen.Role.FARMER, "name": "Matilda"},
		{"role": Citizen.Role.LUMBERJACK, "name": "Robin"},
		{"role": Citizen.Role.LUMBERJACK, "name": "Barnaby"},
		{"role": Citizen.Role.MINER, "name": "Giles"},
		{"role": Citizen.Role.BAKER, "name": "Elsbeth"},
		{"role": Citizen.Role.GUARD, "name": "Percival"}
	]
	
	var spawn_center = Vector3(32, 0, 32)
	
	for info in roles_to_spawn:
		var citizen = Citizen.new()
		citizen.citizen_name = info["name"]
		citizen.voxel_world = voxel_world
		citizen.supply_chain = supply_chain
		
		var rx = randf_range(-6.0, 6.0)
		var rz = randf_range(-6.0, 6.0)
		var cx = int(spawn_center.x + rx)
		var cz = int(spawn_center.z + rz)
		var cy = voxel_world.get_surface_height(cx, cz)
		
		citizen.position = Vector3(cx + 0.5, cy + 1.2, cz + 0.5)
		add_child(citizen)
		citizens.append(citizen)
		
		# Set initial work target near workstations
		var work_target = citizen.position + Vector3(randf_range(-4, 4), 0, randf_range(-4, 4))
		citizen.set_role(info["role"], work_target)

func _process(delta: float) -> void:
	# Day/Night lighting rotation
	day_timer += delta
	var progress = fmod(day_timer, day_duration) / day_duration
	var angle_rad = progress * TAU
	if sun_light:
		sun_light.rotation.x = angle_rad - (PI * 0.5)
		# Dim sun at night
		var sun_height = sin(angle_rad)
		sun_light.light_energy = maxf(0.1, sun_height * 1.2)
		if audio_manager:
			audio_manager.set_day_night(sun_height < 0.0)

	# Atmospheric Simulation & Visual Shaders
	if atmospheric_system and season_manager and player:
		var env_node = get_node_or_null("WorldEnvironment") as WorldEnvironment
		var atmo_params = atmospheric_system.evaluate_atmosphere(
			progress,
			season_manager.current_season,
			season_manager.current_weather,
			player.global_position
		)
		if env_node and sun_light:
			atmospheric_system.apply_to_environment(env_node, sun_light, atmo_params)

	# Update Royal Decrees timers
	if royal_decrees:
		royal_decrees.update_timers(delta)

	# Update Foreign Diplomacy & Vassal Tributes
	if diplomacy_system:
		diplomacy_system.process_diplomacy(delta, supply_chain)

	# Update Strategic Foreign Invasions & Frontier Sieges
	if foreign_invasion_manager:
		foreign_invasion_manager.process_invasions(delta, diplomacy_system)

	# Thermal climate & seasonal updates
	if season_manager:
		var current_temp = season_manager.calculate_current_temperature(progress)
		if player:
			player.ambient_temperature = current_temp
		if hud:
			hud.update_season_display(season_manager.get_season_name(), current_temp, season_manager.get_weather_name())
			
	# Update HUD Realism Debug Info
	if hud and player:
		var fps = Engine.get_frames_per_second()
		var dname = _get_current_district_name(player.global_position)
		var bname = "Temperate Forest"
		if voxel_world and voxel_world.biome_manager:
			var btype = voxel_world.biome_manager.get_biome(int(player.global_position.x), int(player.global_position.z))
			bname = voxel_world.biome_manager.get_biome_name(btype)
		hud.update_debug_info(float(fps), player.global_position, dname, bname)

	# Caravan periodic arrival
	caravan_timer += delta
	if caravan_timer >= caravan_interval:
		caravan_timer = 0.0
		spawn_trade_caravan()

func _on_cycle_district() -> void:
	if not world_assembler or not player or not voxel_world:
		return
	var districts = WorldAssembler.DISTRICT_NAMES.keys()
	current_district_index = (current_district_index + 1) % districts.size()
	var dtype = districts[current_district_index]
	var center = world_assembler.get_district_center(dtype)
	var surface_y = voxel_world.get_surface_height(int(center.x), int(center.z))
	player.global_position = Vector3(center.x + 0.5, surface_y + 2.0, center.z + 0.5)
	var dname = WorldAssembler.DISTRICT_NAMES.get(dtype, "District")
	if hud:
		hud.show_notification("⚡ Fast Traveled to: %s" % dname)
	if audio_manager:
		var district_key = "CITADEL"
		match dtype:
			WorldAssembler.DistrictType.CITADEL: district_key = "CITADEL"
			WorldAssembler.DistrictType.TOWN_SQUARE: district_key = "TOWN_SQUARE"
			WorldAssembler.DistrictType.STEAM_AND_FORGE: district_key = "STEAM_AND_FORGE"
			WorldAssembler.DistrictType.HARBOR_AND_DOCKS: district_key = "HARBOR_AND_DOCKS"
			WorldAssembler.DistrictType.MINING_RAIL: district_key = "MINING_RAIL"
			WorldAssembler.DistrictType.OBSERVATORY: district_key = "OBSERVATORY"
			WorldAssembler.DistrictType.AGRICULTURE_NORFOLK: district_key = "AGRICULTURE_NORFOLK"
			WorldAssembler.DistrictType.WILDERNESS_OUTPOSTS: district_key = "WILDERNESS_OUTPOSTS"
		audio_manager.set_district_ambiance(district_key)

	if quest_manager:
		match dtype:
			WorldAssembler.DistrictType.STEAM_AND_FORGE:
				quest_manager.record_progress("visit_steam_district", 1)
			WorldAssembler.DistrictType.HARBOR_AND_DOCKS:
				quest_manager.record_progress("visit_harbor_district", 1)
			WorldAssembler.DistrictType.OBSERVATORY:
				quest_manager.record_progress("visit_observatory", 1)
			WorldAssembler.DistrictType.MINING_RAIL:
				quest_manager.record_progress("visit_mining_district", 1)

func _on_toggle_ledger() -> void:
	if royal_ledger:
		royal_ledger.visible = not royal_ledger.visible
		if royal_ledger.visible:
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		else:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _get_current_district_name(pos: Vector3) -> String:
	if not world_assembler:
		return "Unknown Frontier"
	var closest_dist: float = 99999.0
	var closest_name: String = "Wilderness Realm"
	for dtype in WorldAssembler.DISTRICT_CENTERS.keys():
		var center = WorldAssembler.DISTRICT_CENTERS[dtype]
		var dist = pos.distance_to(center)
		if dist < closest_dist:
			closest_dist = dist
			closest_name = WorldAssembler.DISTRICT_NAMES[dtype]
	return closest_name

func _on_role_reassigned(role_name: String, _delta: int) -> void:
	var role_enum = Citizen.Role.UNASSIGNED
	match role_name:
		"farmer": role_enum = Citizen.Role.FARMER
		"lumberjack": role_enum = Citizen.Role.LUMBERJACK
		"miner": role_enum = Citizen.Role.MINER
		"baker": role_enum = Citizen.Role.BAKER
		"blacksmith": role_enum = Citizen.Role.BLACKSMITH
		"guard": role_enum = Citizen.Role.GUARD
		
	for c in citizens:
		if c.current_role != role_enum and c.current_role == Citizen.Role.UNASSIGNED:
			c.set_role(role_enum, c.position + Vector3(randf_range(-5, 5), 0, randf_range(-5, 5)))
			if quest_manager:
				quest_manager.record_progress("reassign_citizen", 1)
			break

func _on_open_crafting() -> void:
	if crafting_menu:
		crafting_menu.open_menu(null)

func _on_interact_requested(target: Node3D) -> void:
	if target is Citizen and citizen_dialogue:
		var is_winter = (season_manager and season_manager.current_season == SeasonManager.Season.WINTER)
		citizen_dialogue.open_dialogue(target, is_winter)
		if audio_manager:
			audio_manager.play_ui_click()
		return
	if (target is Workstation or target is TradeCaravan or target is EnchanterTable or target is CookingPot) and crafting_menu:
		crafting_menu.open_menu(target)

func _on_war_horn_sounded() -> void:
	is_royal_alarm_active = not is_royal_alarm_active
	var hearth_pos = Vector3(32, voxel_world.get_surface_height(32, 32), 32) if voxel_world else Vector3(32, 16, 32)
	for c in citizens:
		c.on_royal_alarm(is_royal_alarm_active, hearth_pos)
	if audio_manager:
		audio_manager.play_war_horn()
	if squadron_command and player:
		squadron_command.issue_rally_call(player.global_position, citizens)
	if quest_manager:
		quest_manager.record_progress("sound_war_horn", 1)
		
	if hud:
		if is_royal_alarm_active:
			hud.show_notification("📯 THE ROYAL WAR HORN SOUNDS! All Civilians Retreat to the Keep!")
		else:
			hud.show_notification("📯 ALL CLEAR! Citizens resume daily feudal duties.")

func _on_item_crafted(recipe_name: String, _item: Dictionary) -> void:
	if audio_manager:
		audio_manager.play_craft_success()
	if quest_manager:
		var r_low = recipe_name.to_lower()
		if r_low.contains("ingot") or r_low.contains("iron"):
			quest_manager.record_progress("smelt_ore", 1)
			quest_manager.record_progress("craft_iron_item", 1)
	if hud:
		hud.show_notification("Crafted %s" % recipe_name)

func _on_player_block_action(action: String, pos: Vector3i, btype: int) -> void:
	match action:
		"place":
			if audio_manager:
				audio_manager.play_block_place()
			if save_system:
				save_system.register_voxel_modification(pos, btype)
		"mine":
			if audio_manager:
				audio_manager.play_pickaxe_hit()
			if save_system:
				save_system.register_voxel_modification(pos, 0)
			if quest_manager:
				if btype == VoxelChunk.BlockType.WOOD or btype == VoxelChunk.BlockType.PLANKS:
					quest_manager.record_progress("harvest_wood", 1)
				elif btype == VoxelChunk.BlockType.STONE or btype == VoxelChunk.BlockType.COBBLESTONE:
					quest_manager.record_progress("mine_stone", 1)
				elif btype == VoxelChunk.BlockType.WHEAT_CROP:
					quest_manager.record_progress("harvest_wheat", 1)
			if btype == VoxelChunk.BlockType.WHEAT_CROP and agriculture_manager:
				agriculture_manager.harvest_crop(pos)
		"till":
			if audio_manager:
				audio_manager.play_footstep(AudioManager.SURFACE_MUD)
			if save_system:
				save_system.register_voxel_modification(pos, VoxelChunk.BlockType.FARMLAND)
			if quest_manager:
				quest_manager.record_progress("till_farmland", 1)
			if agriculture_manager:
				agriculture_manager.register_farmland(pos)
		"plant":
			if audio_manager:
				audio_manager.play_footstep(AudioManager.SURFACE_GRASS)
			if agriculture_manager:
				agriculture_manager.plant_crop(pos, "wheat")

func _on_crop_matured(pos: Vector3i) -> void:
	# Dispatch available farmer to harvest
	for c in citizens:
		if c.current_role == Citizen.Role.FARMER:
			if c.current_state == Citizen.State.IDLE or c.current_state == Citizen.State.WANDER:
				c._navigate_to(Vector3(pos.x + 0.5, pos.y, pos.z + 0.5), Citizen.State.HARVESTING)
				break

func _on_crop_harvested(_pos: Vector3i, yield_data: Dictionary) -> void:
	if hud:
		hud.show_notification("🌾 Harvest: +%d Wheat, +%d Seeds" % [yield_data.get("wheat", 2), yield_data.get("seeds", 1)])

func _on_raid_spawned(count: int) -> void:
	if hud:
		hud.show_notification("⚠️ Bandit Raid approaching! %d Raiders spotted!" % count)

func _on_raid_defeated() -> void:
	if quest_manager:
		quest_manager.record_progress("repel_bandit", 1)
	if hud:
		hud.show_notification("⚔️ Raid Repelled! The Realm is Secure.")

func _on_bandit_slain(_loot: Dictionary) -> void:
	if hud:
		hud.show_notification("☠️ Bandit Slain! Spoils gathered.")

func spawn_trade_caravan() -> void:
	if active_caravans.size() > 0:
		return
		
	var caravan = TradeCaravan.new()
	var spawn_x = 36
	var spawn_z = 28
	var surface_y = voxel_world.get_surface_height(spawn_x, spawn_z) if voxel_world else 16
	caravan.position = Vector3(spawn_x + 0.5, surface_y + 1.0, spawn_z + 0.5)
	caravan.traded.connect(_on_caravan_traded)
	caravan.departed.connect(_on_caravan_departed.bind(caravan))
	add_child(caravan)
	active_caravans.append(caravan)
	if hud:
		hud.show_notification("🐪 An Exotic Trade Caravan has arrived in the realm!")

func _on_caravan_traded(item_bought: String, cost: int) -> void:
	if quest_manager:
		quest_manager.record_progress("caravan_trade", 1)
	if hud:
		hud.show_notification("💰 Traded %s for %d coins with the caravan!" % [item_bought.capitalize(), cost])

func _on_caravan_departed(caravan: TradeCaravan) -> void:
	active_caravans.erase(caravan)
	if hud:
		hud.show_notification("🐪 Trade Caravan has departed for distant lands.")

func _on_season_changed(_old_season: SeasonManager.Season, new_season: SeasonManager.Season) -> void:
	if hud and season_manager:
		hud.show_notification("🍂 Season changed to %s!" % season_manager.get_season_name(new_season))

func _on_weather_changed(new_weather: SeasonManager.Weather) -> void:
	if hud and season_manager:
		hud.show_notification("🌧️ Weather: %s" % season_manager.get_weather_name(new_weather))

func _on_toggle_pause() -> void:
	if pause_menu:
		pause_menu.toggle_pause_menu()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_quick_save() -> void:
	if save_system:
		var ok = save_system.quick_save(self)
		if hud:
			if ok:
				hud.show_notification("💾 Realm Quick-Saved! (Slot: quicksave)")
			else:
				hud.show_notification("⚠️ Quick-Save Failed!")
		if audio_manager:
			audio_manager.play_ui_click()

func _on_quick_load() -> void:
	if save_system:
		var ok = save_system.quick_load(self)
		if hud:
			if ok:
				hud.show_notification("📂 Realm Quick-Loaded Successfully!")
			else:
				hud.show_notification("⚠️ Quick-Load Failed - No Save Found!")
		if audio_manager:
			audio_manager.play_ui_click()

func _on_player_footstep(block_type: int, is_sprinting: bool) -> void:
	if audio_manager:
		audio_manager.play_footstep_for_block(block_type, is_sprinting)

func _on_menu_resumed() -> void:
	if audio_manager:
		audio_manager.play_ui_click()

func _on_menu_save_requested(slot_name: String) -> void:
	if save_system:
		var ok = save_system.save_game(slot_name, self)
		if hud:
			hud.show_notification("💾 Saved to [%s] (%s)" % [slot_name, "OK" if ok else "FAILED"])
		if audio_manager:
			audio_manager.play_ui_click()

func _on_menu_load_requested(slot_name: String) -> void:
	if save_system:
		var ok = save_system.load_game(slot_name, self)
		if hud:
			hud.show_notification("📂 Loaded from [%s] (%s)" % [slot_name, "OK" if ok else "FAILED"])
		if audio_manager:
			audio_manager.play_ui_click()

func _on_settings_applied(settings_dict: Dictionary) -> void:
	if player and "mouse_sensitivity" in settings_dict:
		player.MOUSE_SENSITIVITY = settings_dict["mouse_sensitivity"]
	if player and player.camera and "fov" in settings_dict:
		player.camera.fov = settings_dict["fov"]
	if audio_manager and "volume" in settings_dict:
		audio_manager.apply_volume_settings(settings_dict["volume"])
	if hud:
		hud.show_notification("⚙️ Settings Applied!")

func _on_toggle_journal() -> void:
	if quest_journal:
		quest_journal.toggle_journal()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_quest_completed(_quest_id: String, title: String, reward_renown: int) -> void:
	if hud:
		hud.show_notification("🏆 DEED ACCOMPLISHED: %s (+%d Renown)!" % [title, reward_renown])
	if audio_manager:
		audio_manager.play_craft_success()

func _on_monarch_title_promoted(new_title: String, _total_renown: int) -> void:
	if hud:
		hud.show_notification("👑 ROYAL CORONATION! You are now: %s!" % new_title)
	if audio_manager:
		audio_manager.play_war_horn()

func _on_realm_victory_achieved(_total_renown: int) -> void:
	if hud:
		hud.show_notification("🎉 SUPREME REALM VICTORY! All Feudal Deeds Complete!")
	if audio_manager:
		audio_manager.play_war_horn()

func _on_toggle_heraldry() -> void:
	if heraldry_ui:
		heraldry_ui.toggle_menu()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_heraldry_updated(_blazon: String, _pri: Color, _sec: Color) -> void:
	if hud:
		hud.show_notification("🛡️ Royal Coat of Arms & Castle Banners Updated!")
	if audio_manager:
		audio_manager.play_craft_success()

func _on_toggle_decrees() -> void:
	if decrees_ui:
		decrees_ui.toggle_menu()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_decree_proclaimed(_decree_id: String, decree_name: String) -> void:
	if hud:
		hud.show_notification("📜 IMPERIAL EDICT PROCLAIMED: %s!" % decree_name)
	if audio_manager:
		audio_manager.play_war_horn()

func _on_decree_expired(_decree_id: String, decree_name: String) -> void:
	if hud:
		hud.show_notification("⌛ Imperial Edict Expired: %s." % decree_name)

func _on_squad_stance_changed(_new_stance: int, stance_name: String) -> void:
	if hud:
		hud.show_notification("🛡️ Garrison Stance: %s" % stance_name)

func _on_squad_formation_changed(_new_form: int, form_name: String) -> void:
	if hud:
		hud.show_notification("⚔️ Military Formation: %s" % form_name)

func _on_squad_rally_requested() -> void:
	if squadron_command and player:
		var count = squadron_command.issue_rally_call(player.global_position, citizens)
		if hud:
			hud.show_notification("📯 Rallied %d Garrison Guards to Monarch!" % count)
		if audio_manager:
			audio_manager.play_war_horn()

func _on_toggle_diplomacy() -> void:
	if diplomacy_ui:
		diplomacy_ui.toggle_chancery()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_vassal_tribute_received(faction_id: String, _resources: Dictionary) -> void:
	if hud and diplomacy_system:
		var f = diplomacy_system.get_faction(faction_id)
		var fname = f.get("name", faction_id)
		hud.show_notification("👑 Vassal Tribute received from %s!" % fname)
	if audio_manager:
		audio_manager.play_craft_success()

func _on_diplomatic_war_declared(faction_id: String, _aggressor: bool) -> void:
	if hud and diplomacy_system:
		var f = diplomacy_system.get_faction(faction_id)
		var fname = f.get("name", faction_id)
		hud.show_notification("⚔️ WAR DECLARED! %s is now an enemy of the realm!" % fname)
	if audio_manager:
		audio_manager.play_war_horn()

func _on_toggle_war_room() -> void:
	if war_room_ui:
		war_room_ui.toggle_war_room()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_invasion_begun(_battalion_id: String, faction_id: String, target_outpost: String) -> void:
	if hud and foreign_invasion_manager:
		var op = foreign_invasion_manager.get_outpost(target_outpost)
		var op_name = op.get("name", target_outpost)
		hud.show_notification("🚨 BORDER INVASION! %s battalion marching towards %s!" % [faction_id.capitalize(), op_name])
	if audio_manager:
		audio_manager.play_war_horn()

func _on_outpost_attacked(_outpost_id: String, _damage: float, _garrison: int) -> void:
	pass

func _on_outpost_breached(outpost_id: String) -> void:
	if hud and foreign_invasion_manager:
		var op = foreign_invasion_manager.get_outpost(outpost_id)
		var op_name = op.get("name", outpost_id)
		hud.show_notification("💀 FORTIFICATION BREACHED! %s has fallen to invaders!" % op_name)
	if audio_manager:
		audio_manager.play_war_horn()

func _on_battalion_routed(_battalion_id: String, casualties: int) -> void:
	if hud:
		hud.show_notification("⚔️ VICTORY! Hostile invasion battalion routed (%d casualties inflicted)!" % casualties)
	if audio_manager:
		audio_manager.play_craft_success()

func _on_toggle_tournament() -> void:
	if tournament_ui:
		tournament_ui.toggle_tournament_ui()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_tournament_victorious(discipline: String, victor: String, prize_gold: int, honor_awarded: int) -> void:
	if victor == "Monarch":
		if supply_chain:
			supply_chain.add_resource("gold_coins", prize_gold)
		if quest_manager:
			quest_manager.record_progress("win_tournament", 1)
		if hud:
			hud.show_notification("🏆 TOURNAMENT TRIUMPH! Victorious in %s (+%d Gold, +%d Honor)!" % [discipline.capitalize(), prize_gold, honor_awarded])
		if audio_manager:
			audio_manager.play_craft_success()
	else:
		if hud:
			hud.show_notification("⚔️ Match Concluded: %s claimed victory in %s." % [victor, discipline.capitalize()])

func _on_grand_feast_hosted(morale_boost: float, guests_count: int) -> void:
	for c in citizens:
		if "morale" in c:
			c.morale = minf(100.0, c.morale + morale_boost)
	if quest_manager:
		quest_manager.record_progress("host_grand_feast", 1)
	if hud:
		hud.show_notification("🍷 ROYAL FEAST PROCLAIMED! %d subjects celebrated (+%.0f Morale)!" % [guests_count, morale_boost])
	if audio_manager:
		audio_manager.play_craft_success()

func _on_chivalric_title_unlocked(new_title: String, _honor: int) -> void:
	if hud:
		hud.show_notification("🛡️ CHIVALRIC KNIGHTHOOD FEAT! Promoted to: %s!" % new_title)
	if audio_manager:
		audio_manager.play_craft_success()

func _on_toggle_monastery() -> void:
	if monastery_ui:
		monastery_ui.toggle_monastery_ui()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_monastery_research_completed(_tech_id: String, tech_name: String) -> void:
	if quest_manager:
		quest_manager.record_progress("complete_research", 1)
	if hud:
		hud.show_notification("📜 SCHOLASTIC TRIUMPH: %s researched!" % tech_name)
	if audio_manager:
		audio_manager.play_craft_success()

func _on_relic_enshrined(_relic_id: String, relic_name: String, slot: int) -> void:
	if hud:
		hud.show_notification("🏛️ CONSECRATED SACRED RELIC: %s enshrined upon Altar %d!" % [relic_name, slot + 1])
	if audio_manager:
		audio_manager.play_craft_success()

func _on_abbey_bell_rung(_blessing_name: String) -> void:
	for c in citizens:
		if "morale" in c:
			c.morale = minf(100.0, c.morale + 30.0)
	if hud:
		hud.show_notification("🔔 THE ABBEY BELLS TOLL! Divine peace and serenity fill the realm (+30 Morale)!")
	if audio_manager:
		audio_manager.play_war_horn()

func _on_alchemy_potion_brewed(_potion_id: String, potion_name: String, _count: int) -> void:
	if hud:
		hud.show_notification("🧪 Alchemical Draught Brewed: %s!" % potion_name)
	if audio_manager:
		audio_manager.play_craft_success()

func _on_alchemy_metal_transmuted(_formula_id: String, _input_res: String, output_res: String, output_count: int) -> void:
	if hud:
		hud.show_notification("🪙 ALCHEMICAL TRANSMUTATION! Created %d %s!" % [output_count, output_res.replace("_", " ").capitalize()])
	if audio_manager:
		audio_manager.play_craft_success()

func _on_toggle_espionage() -> void:
	if espionage_ui:
		espionage_ui.toggle_visibility()
		if audio_manager:
			audio_manager.play_ui_click()

func _on_espionage_agent_recruited(_agent_id: String, agent_name: String, _type: String) -> void:
	if hud:
		hud.show_notification("🗡️ SHADOW COUNCIL: Recruited %s to royal retainer!" % agent_name)
	if audio_manager:
		audio_manager.play_craft_success()

func _on_espionage_op_resolved(_op_id: String, success: bool, outcome_desc: String, _rewards: Dictionary) -> void:
	if hud:
		if success:
			hud.show_notification("🎭 COVERT TRIUMPH: %s" % outcome_desc)
		else:
			hud.show_notification("⚠️ COVERT BLUNDER: %s" % outcome_desc)
	if audio_manager:
		audio_manager.play_craft_success()

func _on_counter_intel_triggered(threat_title: String, thwarted: bool) -> void:
	if hud:
		if thwarted:
			hud.show_notification("🛡️ COUNTER-INTELLIGENCE: %s" % threat_title)
		else:
			hud.show_notification("🚨 SECURITY BREACH: %s" % threat_title)
	if audio_manager:
		audio_manager.play_war_horn()

func _on_prisoner_interrogated(_prisoner_id: String, secrets: String) -> void:
	if hud:
		hud.show_notification("🔍 DUNGEON INTERROGATION: %s" % secrets)
	if audio_manager:
		audio_manager.play_craft_success()





