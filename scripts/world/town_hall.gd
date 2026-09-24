class_name TownHall
extends StaticBody3D

## MineColonies-style Town Hall Settlement Core & Magistrate Desk.
## The central administrative and territorial anchor of the kingdom.
## Defines sovereign realm borders, tracks demographic population limits,
## manages citizen registries, and coordinates municipal workforce assignments.

signal colony_tiered_up(new_tier: int, border_radius: float)
signal citizen_registered(citizen_name: String, total_population: int)
signal role_assigned(citizen_name: String, role_name: String)

enum ColonyTier {
	HAMLET = 1,     # Border: 32m, Base Cap: 10
	VILLAGE = 2,    # Border: 48m, Base Cap: 18
	TOWNSHIP = 3,   # Border: 64m, Base Cap: 30
	ROYAL_CITY = 4  # Border: 96m, Base Cap: 50
}

@export var realm_name: String = "Valoria"
@export var current_tier: ColonyTier = ColonyTier.HAMLET

var supply_chain: SupplyChain = null
var border_radius: float = 32.0
var base_population_cap: int = 10
var built_cottages: int = 0
var registered_citizens: Array[Dictionary] = []

var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	add_to_group("civic_centers")
	border_radius = calculate_border_radius(current_tier)
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.8, 1.2, 1.2)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.6, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/town_hall_desk.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	prompt_label = Label3D.new()
	prompt_label.text = "🏛️ %s Town Hall (Tier %d)\n[E] Manage Citizen Registry & Borders" % [realm_name, current_tier]
	prompt_label.position = Vector3(0, 1.8, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 22
	prompt_label.modulate = Color(1.0, 0.85, 0.3)
	add_child(prompt_label)

func register_citizen(c_name: String, initial_role: int = 0) -> bool:
	var total_cap = get_total_capacity()
	if registered_citizens.size() >= total_cap:
		return false # Housing bottleneck
	
	registered_citizens.append({
		"name": c_name,
		"role": initial_role,
		"morale": 80.0,
		"employed": initial_role != 0
	})
	emit_signal("citizen_registered", c_name, registered_citizens.size())
	_update_prompt()
	return true

func assign_role(c_name: String, new_role: int) -> bool:
	for c in registered_citizens:
		if c["name"] == c_name:
			c["role"] = new_role
			c["employed"] = (new_role != 0)
			emit_signal("role_assigned", c_name, str(new_role))
			_update_prompt()
			return true
	return false

func register_cottage_built() -> void:
	built_cottages += 1
	_update_prompt()

func get_total_capacity() -> int:
	return calculate_housing_cap(built_cottages, current_tier)

func upgrade_settlement() -> Dictionary:
	if current_tier >= ColonyTier.ROYAL_CITY:
		return {"success": false, "message": "Colony has already achieved Royal City tier!"}

	var cost = calculate_upgrade_cost(current_tier)
	if not supply_chain:
		return {"success": false, "message": "No supply chain connected."}

	var has_wood = supply_chain.inventory.get("planks", 0) >= cost["planks"]
	var has_stone = supply_chain.inventory.get("stone_bricks", 0) >= cost.get("stone_bricks", 0)
	var has_coins = supply_chain.inventory.get("gold_coins", 0) >= cost["gold_coins"]

	if has_wood and has_stone and has_coins:
		supply_chain.consume_resource("planks", cost["planks"])
		if cost.get("stone_bricks", 0) > 0:
			supply_chain.consume_resource("stone_bricks", cost["stone_bricks"])
		supply_chain.consume_resource("gold_coins", cost["gold_coins"])

		current_tier = (current_tier + 1) as ColonyTier
		border_radius = calculate_border_radius(current_tier)
		emit_signal("colony_tiered_up", current_tier, border_radius)
		_update_prompt()
		return {
			"success": true,
			"new_tier": current_tier,
			"border_radius": border_radius,
			"message": "The Realm has ascended to Tier %d! Borders expanded to %.0fm." % [current_tier, border_radius]
		}

	return {
		"success": false,
		"message": "Insufficient resources for municipal upgrade (Requires %d Planks, %d Coins)." % [
			cost["planks"], cost["gold_coins"]
		]
	}

func _update_prompt() -> void:
	if not prompt_label:
		return
	var tier_name = "Hamlet"
	if current_tier == ColonyTier.VILLAGE: tier_name = "Village"
	elif current_tier == ColonyTier.TOWNSHIP: tier_name = "Township"
	elif current_tier == ColonyTier.ROYAL_CITY: tier_name = "Royal City"

	prompt_label.text = "🏛️ %s (%s - Tier %d)\nPop: %d/%d | Border: %.0fm\n[E] Magistrate Registry" % [
		realm_name, tier_name, current_tier, registered_citizens.size(), get_total_capacity(), border_radius
	]
	prompt_label.modulate = Color(0.4, 0.95, 0.6) if registered_citizens.size() < get_total_capacity() else Color(1.0, 0.7, 0.3)

# --- Static Simulation & Balance Calculations ---

static func calculate_border_radius(tier: int) -> float:
	match tier:
		ColonyTier.HAMLET: return 32.0
		ColonyTier.VILLAGE: return 48.0
		ColonyTier.TOWNSHIP: return 64.0
		ColonyTier.ROYAL_CITY: return 96.0
		_: return 32.0

static func calculate_housing_cap(cottages_count: int, tier: int = ColonyTier.HAMLET) -> int:
	var base_cap = 10
	if tier == ColonyTier.VILLAGE: base_cap = 18
	elif tier == ColonyTier.TOWNSHIP: base_cap = 30
	elif tier == ColonyTier.ROYAL_CITY: base_cap = 50
	# Each completed residential cottage adds +4 citizen beds
	return base_cap + (cottages_count * 4)

static func calculate_upgrade_cost(tier: int) -> Dictionary:
	match tier:
		ColonyTier.HAMLET:
			return {"planks": 16, "stone_bricks": 8, "gold_coins": 20}
		ColonyTier.VILLAGE:
			return {"planks": 32, "stone_bricks": 24, "gold_coins": 50}
		ColonyTier.TOWNSHIP:
			return {"planks": 64, "stone_bricks": 48, "gold_coins": 100}
		_:
			return {"planks": 999, "gold_coins": 999}
