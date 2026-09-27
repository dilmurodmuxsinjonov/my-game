class_name TradeCaravan
extends StaticBody3D

## Feudal Merchant Trade Caravan.
## Arrives periodically with draft cart and offers exotic goods (spices, salt, fabric, steel)
## in exchange for realm commodities and coins.
## Upgraded for Milestone 5 with multi-market regional routing, route security risk calculations,
## bandit ambush interception mechanics, and armed escort protection.

signal traded(item_bought: String, cost: int)
signal departed()
signal caravan_ambushed(loss_fraction: float, cargo_lost: Dictionary)
signal caravan_arrived(destination_hub_id: int, delivered_cargo: Dictionary)
signal escort_hired(guard_count: int, total_cost: float)

var model_instance: Node3D
var collision_box: CollisionShape3D
var prompt_label: Label3D

var stay_duration: float = 90.0 # Stays for 1.5 minutes
var stay_timer: float = 0.0

# Caravan wares and prices (in coins)
var wares: Dictionary = {
	"spices": {"price": 12, "stock": 5, "icon": "🌶️"},
	"cured_salt": {"price": 6, "stock": 10, "icon": "🧂"},
	"fine_fabric": {"price": 15, "stock": 6, "icon": "🧵"},
	"steel_ingot": {"price": 20, "stock": 4, "icon": "⚔️"},
	"rare_seeds": {"price": 8, "stock": 8, "icon": "🌾"}
}

# Purchase prices for kingdom surplus (what caravan pays the player)
var purchase_rates: Dictionary = {
	"bread": 2,
	"wheat": 1,
	"logs": 1,
	"stone": 1,
	"iron_ore": 3,
	"copper_ore": 2
}

# Multi-Market Regional Logistics & Security State
var origin_hub_id: int = 0
var destination_hub_id: int = 2
var cargo_inventory: Dictionary = {}
var max_cargo_capacity: float = 1200.0 # kg
var escort_guard_count: int = 2
var escort_strength: float = 2.0 # Each guard contributes 1.0 combat strength
var base_escort_cost_per_guard: float = 25.0 # Silver coins
var caravan_speed: float = 2.5 # m/s (draft cart speed)
var route_distance_m: float = 2500.0 # meters between hubs
var route_risk: float = 0.0

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.8, 1.8, 2.6)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.9, 0)
	add_child(collision_box)

	# Load Blender caravan_cart.glb
	var glb_path = "res://assets/models/caravan_cart.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_instance = scene_res.instantiate()
			add_child(model_instance)

	# Prompt billboard
	prompt_label = Label3D.new()
	prompt_label.text = "🐪 Merchant Trade Caravan\n[E] Trade Exotic Goods"
	prompt_label.position = Vector3(0, 2.3, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 28
	prompt_label.modulate = Color(1.0, 0.85, 0.4)
	add_child(prompt_label)

func _process(delta: float) -> void:
	stay_timer += delta
	if stay_timer >= stay_duration:
		depart()

func buy_item(item_key: String, supply_chain: SupplyChain) -> bool:
	if not wares.has(item_key) or not supply_chain:
		return false

	var ware = wares[item_key]
	if ware["stock"] <= 0:
		return false

	var price = ware["price"]
	# Check if player / supply chain has enough coins
	var current_coins = supply_chain.inventory.get("coins", 0)
	if current_coins < price:
		return false

	supply_chain.consume_resource("coins", price)
	supply_chain.add_resource(item_key, 1)
	ware["stock"] -= 1
	emit_signal("traded", item_key, price)
	return true

func sell_resource(item_key: String, amount: int, supply_chain: SupplyChain) -> bool:
	if not purchase_rates.has(item_key) or not supply_chain:
		return false

	var rate = purchase_rates[item_key]
	if supply_chain.consume_resource(item_key, amount):
		var earned_coins = rate * amount
		supply_chain.add_resource("coins", earned_coins)
		return true
	return false

func depart() -> void:
	emit_signal("departed")
	queue_free()

# ==============================================================================
# REALISM SECURITY RISK, AMBUSH & LOGISTICS UPGRADES (R5)
# ==============================================================================

## Calculate individual road edge risk index
## Risk_edge = clamp((Length / 1000.0) * Threat * (1.0 - 0.70 * PatrolCoverage), 0.0, 0.95)
static func calculate_edge_risk(
	length_m: float,
	wilderness_threat: float,
	guard_patrol_coverage: float
) -> float:
	var len_factor: float = length_m / 1000.0
	var patrol_mitigation: float = 1.0 - 0.70 * clampf(guard_patrol_coverage, 0.0, 1.0)
	var raw_risk: float = len_factor * wilderness_threat * patrol_mitigation
	return clampf(raw_risk, 0.0, 0.95)

## Aggregates total route risk across all consecutive path edges
## Risk_route = 1.0 - Product(1.0 - Risk_edge(e))
static func calculate_route_risk(route_edges: Array) -> float:
	if route_edges.is_empty():
		return 0.0

	var survival_prob: float = 1.0
	for edge in route_edges:
		var edge_risk: float = 0.0
		if edge is Dictionary:
			var length_m = edge.get("length_m", 1000.0)
			var threat = edge.get("wilderness_threat", 0.5)
			var patrol = edge.get("guard_patrol_coverage", 0.0)
			edge_risk = calculate_edge_risk(length_m, threat, patrol)
		elif edge is float:
			edge_risk = clampf(edge, 0.0, 0.95)

		survival_prob *= (1.0 - edge_risk)

	return clampf(1.0 - survival_prob, 0.0, 0.99)

## Round-trip travel time calculation factoring route risk delay
## T_roundtrip = (2 * Distance / V_caravan) * (1.0 + 0.50 * Risk_route) + T_trading
static func calculate_travel_time(
	distance_m: float,
	caravan_speed_val: float,
	route_risk_val: float,
	trading_time_seconds: float = 30.0
) -> float:
	var speed = maxf(0.5, caravan_speed_val)
	var transit_time = (2.0 * distance_m) / speed
	var risk_slowdown = 1.0 + 0.50 * clampf(route_risk_val, 0.0, 1.0)
	return transit_time * risk_slowdown + trading_time_seconds

## Armed escort hire cost scaling with route danger
## Cost_escort = BaseEscort * (1.0 + 2.50 * Risk_route)
static func calculate_escort_cost(
	base_escort_cost: float,
	route_risk_val: float
) -> float:
	return base_escort_cost * (1.0 + 2.50 * clampf(route_risk_val, 0.0, 1.0))

## Resolves bandit ambush check and calculates looted cargo fraction
## LossFraction = clamp(Risk_route - 0.20 * EscortStrength, 0.0, 1.0)
func resolve_ambush(
	route_risk_val: float,
	escort_str: float,
	random_roll: float = -1.0
) -> Dictionary:
	var roll = random_roll if random_roll >= 0.0 else randf()
	var ambushed: bool = roll < route_risk_val
	var loss_fraction: float = 0.0
	var cargo_lost: Dictionary = {}
	var cargo_remaining: Dictionary = {}

	if ambushed:
		loss_fraction = clampf(route_risk_val - 0.20 * escort_str, 0.0, 1.0)
		for item in cargo_inventory.keys():
			var amount = cargo_inventory[item]
			var lost_amount = amount * loss_fraction
			var kept_amount = amount - lost_amount
			cargo_lost[item] = lost_amount
			cargo_remaining[item] = kept_amount
		# Update active inventory
		cargo_inventory = cargo_remaining.duplicate()
		caravan_ambushed.emit(loss_fraction, cargo_lost)
	else:
		cargo_remaining = cargo_inventory.duplicate()

	return {
		"ambushed": ambushed,
		"loss_fraction": loss_fraction,
		"cargo_lost": cargo_lost,
		"cargo_remaining": cargo_remaining
	}

## Load cargo units into caravan holds
func load_cargo(item_id: String, amount: float) -> void:
	if amount <= 0.0:
		return
	var current = cargo_inventory.get(item_id, 0.0)
	cargo_inventory[item_id] = current + amount

## Unload cargo units from caravan holds
func unload_cargo(item_id: String, amount: float) -> float:
	var current = cargo_inventory.get(item_id, 0.0)
	var unloaded = minf(current, amount)
	cargo_inventory[item_id] = current - unloaded
	if cargo_inventory[item_id] <= 0.0:
		cargo_inventory.erase(item_id)
	return unloaded

## Hire additional caravan guards
func hire_escorts(guard_count: int) -> bool:
	if guard_count <= 0:
		return false
	var total_hire_cost = calculate_escort_cost(base_escort_cost_per_guard * guard_count, route_risk)
	escort_guard_count += guard_count
	escort_strength += guard_count * 1.0
	escort_hired.emit(guard_count, total_hire_cost)
	return true

## Deliver remaining cargo to destination market hub, relieving local supply deficits
func deliver_to_hub(market_manager: RefCounted, dest_hub_id: int = -1) -> Dictionary:
	var target_hub = dest_hub_id if dest_hub_id >= 0 else destination_hub_id
	var delivered = cargo_inventory.duplicate()

	if market_manager and market_manager.has_method("update_hub_inventory"):
		for item in delivered.keys():
			market_manager.update_hub_inventory(target_hub, item, delivered[item])

	cargo_inventory.clear()
	caravan_arrived.emit(target_hub, delivered)
	return delivered
