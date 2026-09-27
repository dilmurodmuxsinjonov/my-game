# scripts/economy/market_economy_manager.gd
# Voxel Lord: Feudal Realm - Milestone 5: Multi-Market Regional Economy & Dynamic Pricing
# Simulates 5 regional market hubs, universal algorithmic pricing with singularity-guarded
# elasticity (gamma = 1.25, kd = 0.85), late-winter "Hungry Gap" grain surges (1.80x-2.20x),
# and macroeconomic currency inflation.

class_name MarketEconomyManager
extends RefCounted

signal price_updated(item_id: String, hub_id: int, new_buy_price: float, new_sell_price: float)
signal market_traded(buyer_hub: int, seller_hub: int, item_id: String, amount: float, total_cost: float)
signal inflation_changed(new_inflation_rate: float)
signal hungry_gap_started(day: int, multiplier: float)

## 5 Regional Market Hubs
enum MarketHub {
	SOVEREIGN_SETTLEMENT = 0,   # Player Realm Capital: central balanced market
	NORTHERN_IRON_WARLORDS = 1, # Mountain fortress: rich in ore/steel, acute grain deficit
	COASTAL_MERCHANT_LEAGUE = 2,# Seaport league: rich in spices/salt/fabric, timber/grain demand
	HOLY_SUN_ORDER_ABBEY = 3,   # Monastic estate: wine/wax/parchment, food/grain consumer
	STEPPE_HORSE_CLANS = 4      # Nomadic clans: rich in horses/leather/meat, metallurgy deficit
}

## Mathematical Pricing Constants
const K_D: float = 0.85
const GAMMA: float = 1.25
const CLAMP_MIN_FACTOR: float = 0.20
const CLAMP_MAX_FACTOR: float = 5.00
const INNER_CLAMP_MIN: float = 0.01 # Critical singularity protector for fractional power
const GUILD_TARIFF: float = 0.15    # Standard 15% guild transaction fee
const INFLATION_ALPHA: float = 0.15 # Velocity elasticity
const STERLING_PURITY: float = 0.925

## Canonical Base Prices in Silver Coins
const BASE_PRICES: Dictionary = {
	"wheat": 1.0,
	"bread": 2.0,
	"flour": 1.5,
	"barley": 1.0,
	"logs": 1.0,
	"stone": 1.0,
	"iron_ore": 3.0,
	"copper_ore": 2.0,
	"iron_ingot": 10.0,
	"steel_ingot": 28.0,
	"tools": 15.0,
	"sword": 45.0,
	"leather": 5.0,
	"meat": 4.0,
	"fish": 3.0,
	"cured_salt": 6.0,
	"spices": 12.0,
	"fine_fabric": 15.0,
	"wine": 14.0,
	"wax": 8.0,
	"parchment": 10.0,
	"horses": 75.0,
	"rare_seeds": 8.0
}

## Staple food commodities affected by annual agricultural seasonality
const STAPLE_GRAINS: Array = [
	"wheat", "bread", "flour", "barley", "grain"
]

## Multi-market hub inventories, targets, and parameters
var hubs: Dictionary = {}
var current_inflation_rate: float = 0.0
var coin_purity: float = STERLING_PURITY

func _init() -> void:
	_setup_default_hubs()

## Initialize the 5 distinct regional market hubs with historical trade specializations
func _setup_default_hubs() -> void:
	hubs[MarketHub.SOVEREIGN_SETTLEMENT] = {
		"hub_id": MarketHub.SOVEREIGN_SETTLEMENT,
		"name": "Sovereign Settlement",
		"population": 120,
		"inventory": {
			"wheat": 800.0, "bread": 500.0, "logs": 400.0, "stone": 300.0,
			"iron_ore": 150.0, "tools": 50.0, "spices": 20.0, "cured_salt": 50.0,
			"fine_fabric": 40.0, "wine": 30.0, "meat": 100.0, "leather": 60.0
		},
		"target_stock": {
			"wheat": 800.0, "bread": 500.0, "logs": 400.0, "stone": 300.0,
			"iron_ore": 150.0, "tools": 50.0, "spices": 20.0, "cured_salt": 50.0,
			"fine_fabric": 40.0, "wine": 30.0, "meat": 100.0, "leather": 60.0
		}
	}

	hubs[MarketHub.NORTHERN_IRON_WARLORDS] = {
		"hub_id": MarketHub.NORTHERN_IRON_WARLORDS,
		"name": "Northern Iron Warlords",
		"population": 180,
		"inventory": {
			"iron_ore": 1200.0, "steel_ingot": 450.0, "tools": 220.0, "sword": 160.0,
			"wheat": 40.0, "bread": 15.0, "wine": 10.0, "cured_salt": 80.0
		},
		"target_stock": {
			"iron_ore": 500.0, "steel_ingot": 200.0, "tools": 100.0, "sword": 80.0,
			"wheat": 1000.0, "bread": 700.0, "wine": 120.0, "cured_salt": 150.0
		}
	}

	hubs[MarketHub.COASTAL_MERCHANT_LEAGUE] = {
		"hub_id": MarketHub.COASTAL_MERCHANT_LEAGUE,
		"name": "Coastal Merchant League",
		"population": 250,
		"inventory": {
			"spices": 600.0, "cured_salt": 950.0, "fine_fabric": 480.0, "fish": 750.0,
			"logs": 35.0, "stone": 45.0, "wheat": 220.0, "tools": 40.0
		},
		"target_stock": {
			"spices": 150.0, "cured_salt": 250.0, "fine_fabric": 120.0, "fish": 200.0,
			"logs": 650.0, "stone": 500.0, "wheat": 1300.0, "tools": 180.0
		}
	}

	hubs[MarketHub.HOLY_SUN_ORDER_ABBEY] = {
		"hub_id": MarketHub.HOLY_SUN_ORDER_ABBEY,
		"name": "Holy Sun Order Abbey",
		"population": 90,
		"inventory": {
			"wine": 700.0, "wax": 450.0, "parchment": 320.0,
			"wheat": 80.0, "bread": 35.0, "iron_ingot": 15.0, "tools": 12.0
		},
		"target_stock": {
			"wine": 150.0, "wax": 100.0, "parchment": 80.0,
			"wheat": 550.0, "bread": 400.0, "iron_ingot": 120.0, "tools": 90.0
		}
	}

	hubs[MarketHub.STEPPE_HORSE_CLANS] = {
		"hub_id": MarketHub.STEPPE_HORSE_CLANS,
		"name": "Steppe Horse Clans",
		"population": 140,
		"inventory": {
			"horses": 350.0, "leather": 800.0, "meat": 900.0,
			"steel_ingot": 5.0, "tools": 12.0, "sword": 8.0, "wheat": 90.0
		},
		"target_stock": {
			"horses": 80.0, "leather": 200.0, "meat": 250.0,
			"steel_ingot": 160.0, "tools": 130.0, "sword": 90.0, "wheat": 600.0
		}
	}

## Get canonical base price for an item
static func get_base_price(item_id: String) -> float:
	return BASE_PRICES.get(item_id, 10.0)

## Core universal algorithmic pricing equation (Buy Price)
## Incorporates gamma = 1.25, kd = 0.85, inner max(0.01, ...) singularity guard,
## and hard clamping to [0.20 * P_base, 5.00 * P_base].
static func calculate_buy_price(
	base_price: float,
	current_stock: float,
	target_stock: float,
	seasonal_modifier: float = 1.0,
	reputation_modifier: float = 1.0,
	inflation_rate: float = 0.0
) -> float:
	var safe_target: float = maxf(1.0, target_stock)
	var safe_current: float = maxf(0.0, current_stock)
	var stock_ratio: float = (safe_target - safe_current) / safe_target

	# Inner linear term with critical singularity protector:
	# Avoids negative base into fractional power (gamma=1.25) which crashes math engines
	var inner_base: float = maxf(INNER_CLAMP_MIN, 1.0 + K_D * stock_ratio)
	var elasticity_factor: float = pow(inner_base, GAMMA)

	var raw_price: float = base_price * elasticity_factor * seasonal_modifier * reputation_modifier * (1.0 + inflation_rate)
	var min_bound: float = CLAMP_MIN_FACTOR * base_price
	var max_bound: float = CLAMP_MAX_FACTOR * base_price

	return clampf(raw_price, min_bound, max_bound)

## Calculate merchant Sell Price paid to players / suppliers
## Applies guild transaction tariff and merchant bartering skill
static func calculate_sell_price(
	buy_price: float,
	guild_tariff: float = GUILD_TARIFF,
	merchant_skill: float = 50.0
) -> float:
	var skill_discount: float = 1.0 - 0.20 * (1.0 - clampf(merchant_skill / 100.0, 0.0, 1.0))
	return buy_price * (1.0 - guild_tariff) * skill_discount

## Interface contract matching PROJECT.md:
## calculate_price(item_id: String, hub_id: int, current_stock: float, target_stock: float, season: int) -> float
func calculate_price(
	item_id: String,
	_hub_id: int,
	current_stock: float,
	target_stock: float,
	season: int
) -> float:
	var base_p: float = get_base_price(item_id)
	# Map season (0=Spring, 1=Summer, 2=Autumn, 3=Winter) to canonical mid-season day
	var day_map = [5, 11, 18, 26] # Day 26 represents Late Winter Hungry Gap
	var day = day_map[clampi(season, 0, 3)]
	var m_season = get_seasonal_modifier(item_id, day)
	return calculate_buy_price(base_p, current_stock, target_stock, m_season, 1.0, current_inflation_rate)

## Calculates seasonal price multiplier factoring the late-winter "Hungry Gap"
## Day t in [1, 28] (Spring 1-7, Summer 8-14, Autumn 15-21, Winter 22-28)
static func get_seasonal_modifier(item_id: String, day_of_year: int) -> float:
	# Only staple grains and bread experience significant agricultural seasonality
	if not STAPLE_GRAINS.has(item_id.to_lower()):
		return 1.0

	var d: int = posmod(day_of_year - 1, 28) + 1 # Normalize to 1..28

	# Late Winter (Days 24-28) & Early Spring (Days 1-3): The "Hungry Gap" (1.80x - 2.20x)
	if d >= 24 or d <= 3:
		# Peak scarcity at winter's end (Day 26 = 2.0x, Day 28 = 2.20x)
		if d >= 24:
			return 1.80 + 0.10 * (d - 24) # 1.80, 1.90, 2.00, 2.10, 2.20
		else:
			return 2.20 - 0.15 * (d - 1)  # 2.20, 2.05, 1.90

	# Spring Sowing (Days 4-7): Grain reserved for seed; elevated prices (1.30x - 1.50x)
	elif d >= 4 and d <= 7:
		return 1.40

	# Summer Growth (Days 8-14): Stable moderate prices (1.00x - 1.10x)
	elif d >= 8 and d <= 14:
		return 1.05

	# Autumn Harvest Glut (Days 15-21): Massive harvest supply drops prices (0.60x - 0.75x)
	elif d >= 15 and d <= 21:
		return 0.65

	# Early Winter (Days 22-23): Cold sets in, storage consumption begins (1.20x - 1.50x)
	elif d >= 22 and d <= 23:
		return 1.35

	return 1.0

## Macroeconomic inflation rate based on coin circulation, economic output, and debasement
static func calculate_inflation_rate(
	circulating_coins: float,
	target_economic_valuation: float,
	mint_purity: float = STERLING_PURITY
) -> float:
	var safe_target = maxf(1.0, target_economic_valuation)
	var excess_ratio = (circulating_coins - safe_target) / safe_target
	var debasement_penalty = maxf(0.0, (STERLING_PURITY - mint_purity) / STERLING_PURITY) * 0.50
	var raw_inflation = excess_ratio * INFLATION_ALPHA + debasement_penalty
	return clampf(raw_inflation, -0.10, 0.40)

## Calculate reputation pricing modifier (50 is neutral 1.0x, 100 is 0.75x, 0 is 1.25x)
static func calculate_reputation_modifier(reputation: float) -> float:
	var rep = clampf(reputation, 0.0, 100.0)
	return 1.0 - 0.25 * ((rep - 50.0) / 50.0)

## Fetch current dynamic buy price for an item at a specific regional hub
func get_item_buy_price(
	item_id: String,
	hub_id: int,
	day_of_year: int = 14,
	reputation: float = 50.0
) -> float:
	if not hubs.has(hub_id):
		hub_id = MarketHub.SOVEREIGN_SETTLEMENT

	var hub = hubs[hub_id]
	var base_p = get_base_price(item_id)
	var current_s = hub["inventory"].get(item_id, hub["target_stock"].get(item_id, 100.0))
	var target_s = hub["target_stock"].get(item_id, 100.0)
	var m_season = get_seasonal_modifier(item_id, day_of_year)
	var m_rep = calculate_reputation_modifier(reputation)

	return calculate_buy_price(base_p, current_s, target_s, m_season, m_rep, current_inflation_rate)

## Fetch current dynamic sell price paid to seller for an item at a specific regional hub
func get_item_sell_price(
	item_id: String,
	hub_id: int,
	day_of_year: int = 14,
	reputation: float = 50.0,
	merchant_skill: float = 50.0
) -> float:
	var buy_p = get_item_buy_price(item_id, hub_id, day_of_year, reputation)
	return calculate_sell_price(buy_p, GUILD_TARIFF, merchant_skill)

## Update inventory stock for a commodity at a given hub
func update_hub_inventory(hub_id: int, item_id: String, delta_stock: float) -> void:
	if not hubs.has(hub_id):
		return
	var inv = hubs[hub_id]["inventory"]
	var current = inv.get(item_id, 0.0)
	inv[item_id] = maxf(0.0, current + delta_stock)

	# Emit signal with updated prices
	var new_buy = get_item_buy_price(item_id, hub_id)
	var new_sell = calculate_sell_price(new_buy)
	price_updated.emit(item_id, hub_id, new_buy, new_sell)

## Get complete hub dictionary
func get_hub_data(hub_id: int) -> Dictionary:
	if hubs.has(hub_id):
		return hubs[hub_id].duplicate(true)
	return {}

## Get all 5 hubs
func get_all_hubs() -> Dictionary:
	return hubs.duplicate(true)

## Execute inter-hub trade transaction
func execute_hub_trade(
	buyer_hub_id: int,
	seller_hub_id: int,
	item_id: String,
	amount: float,
	day_of_year: int = 14
) -> Dictionary:
	if not hubs.has(buyer_hub_id) or not hubs.has(seller_hub_id) or amount <= 0.0:
		return {"success": false, "reason": "Invalid hub or non-positive amount"}

	var seller_inv = hubs[seller_hub_id]["inventory"]
	var available = seller_inv.get(item_id, 0.0)
	if available < amount:
		return {"success": false, "reason": "Insufficient stock at seller hub"}

	var unit_price = get_item_buy_price(item_id, buyer_hub_id, day_of_year)
	var total_cost = unit_price * amount

	# Transfer inventory
	seller_inv[item_id] -= amount
	var buyer_inv = hubs[buyer_hub_id]["inventory"]
	buyer_inv[item_id] = buyer_inv.get(item_id, 0.0) + amount

	market_traded.emit(buyer_hub_id, seller_hub_id, item_id, amount, total_cost)

	return {
		"success": true,
		"item_id": item_id,
		"amount": amount,
		"unit_price": unit_price,
		"total_cost": total_cost,
		"buyer_hub": buyer_hub_id,
		"seller_hub": seller_hub_id
	}
