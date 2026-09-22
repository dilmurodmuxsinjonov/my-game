class_name SupplyChain
extends RefCounted

## Manages kingdom inventory, production chains, tool wear, and citizen food distribution.

signal inventory_updated(item_name: String, new_amount: int)
signal morale_updated(new_morale: float)

# Stockpile inventory
var inventory: Dictionary = {
	"wheat": 20,
	"bread": 50,
	"logs": 30,
	"planks": 15,
	"stone": 25,
	"iron_ore": 0,
	"iron_ingots": 0,
	"tools": 10,
	"weapons": 5
}

# Production rates per game cycle (1 game hour)
var daily_production: Dictionary = {}
var daily_consumption: Dictionary = {}

var morale: float = 75.0 # 0.0 to 100.0%
var tax_rate: float = 0.10 # 10%

func add_resource(item: String, amount: int) -> void:
	if not inventory.has(item):
		inventory[item] = 0
	inventory[item] += amount
	emit_signal("inventory_updated", item, inventory[item])

func consume_resource(item: String, amount: int) -> bool:
	if inventory.has(item) and inventory[item] >= amount:
		inventory[item] -= amount
		emit_signal("inventory_updated", item, inventory[item])
		return true
	return false

func process_production_cycle(assigned_citizens: Dictionary) -> Dictionary:
	var report = {
		"produced": {},
		"consumed": {},
		"unfed_citizens": 0
	}
	
	# 1. Farmers produce wheat
	var farmers = assigned_citizens.get("farmer", 0)
	var wheat_produced = farmers * 4
	add_resource("wheat", wheat_produced)
	report["produced"]["wheat"] = wheat_produced
	
	# 2. Bakers turn wheat into bread (1 wheat -> 2 bread)
	var bakers = assigned_citizens.get("baker", 0)
	var wheat_needed = bakers * 2
	var wheat_used = mini(inventory.get("wheat", 0), wheat_needed)
	if wheat_used > 0:
		consume_resource("wheat", wheat_used)
		var bread_produced = wheat_used * 2
		add_resource("bread", bread_produced)
		report["produced"]["bread"] = bread_produced
		report["consumed"]["wheat"] = wheat_used

	# 3. Lumberjacks produce logs
	var lumberjacks = assigned_citizens.get("lumberjack", 0)
	var logs_produced = lumberjacks * 3
	add_resource("logs", logs_produced)
	report["produced"]["logs"] = logs_produced

	# 4. Miners produce stone and iron ore
	var miners = assigned_citizens.get("miner", 0)
	var stone_produced = miners * 3
	var iron_produced = miners * 1
	add_resource("stone", stone_produced)
	add_resource("iron_ore", iron_produced)
	report["produced"]["stone"] = stone_produced
	report["produced"]["iron_ore"] = iron_produced

	# 5. Blacksmiths turn iron ore and logs into tools & weapons
	var blacksmiths = assigned_citizens.get("blacksmith", 0)
	for i in range(blacksmiths):
		if consume_resource("iron_ore", 2) and consume_resource("logs", 1):
			add_resource("tools", 1)
			report["produced"]["tools"] = report["produced"].get("tools", 0) + 1

	# 6. Citizen food consumption (1 bread per citizen per cycle)
	var total_citizens: int = 0
	for count in assigned_citizens.values():
		total_citizens += count

	var bread_available = inventory.get("bread", 0)
	var fed_citizens = mini(bread_available, total_citizens)
	consume_resource("bread", fed_citizens)
	report["consumed"]["bread"] = fed_citizens
	
	var unfed = total_citizens - fed_citizens
	report["unfed_citizens"] = unfed

	# Update kingdom morale based on food supply and taxes
	_update_morale(unfed, total_citizens)
	return report

func _update_morale(unfed: int, total: int) -> void:
	if total == 0:
		morale = 100.0
		return
	
	var food_ratio = float(total - unfed) / float(total)
	var target_morale = (food_ratio * 90.0) + (10.0 - (tax_rate * 20.0))
	morale = lerp(morale, target_morale, 0.2)
	morale = clamp(morale, 0.0, 100.0)
	emit_signal("morale_updated", morale)
