class_name SupplyChain
extends RefCounted

## Manages kingdom inventory, production chains, tool wear, and citizen food distribution.
## Includes RimWorld-style 'Do Until X' production threshold management.

signal inventory_updated(item_name: String, new_amount: int)
signal morale_updated(new_morale: float)
signal quota_changed(item_name: String, target_qty: int, mode: int)

enum QuotaMode {
	DO_FOREVER = 0,
	DO_UNTIL_X = 1,
	PAUSED = 2
}

# Production Quotas ("Do Until X")
var quotas: Dictionary = {
	"bread": 50,
	"tools": 10,
	"weapons": 5,
	"iron_ingots": 20
}
var quota_modes: Dictionary = {
	"bread": QuotaMode.DO_UNTIL_X,
	"tools": QuotaMode.DO_UNTIL_X,
	"weapons": QuotaMode.DO_UNTIL_X,
	"iron_ingots": QuotaMode.DO_FOREVER
}

# Stockpile inventory
var inventory: Dictionary = {
	"wheat": 20,
	"bread": 50,
	"logs": 30,
	"planks": 15,
	"stone": 25,
	"coal": 12,
	"iron_ore": 6,
	"copper_ore": 4,
	"iron_ingots": 2,
	"copper_ingot": 0,
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

func get_resource(item: String) -> int:
	return inventory.get(item, 0)

func set_quota(item: String, target_amount: int, mode: QuotaMode = QuotaMode.DO_UNTIL_X) -> void:
	quotas[item] = maxi(0, target_amount)
	quota_modes[item] = mode
	emit_signal("quota_changed", item, quotas[item], mode)

func get_quota(item: String) -> int:
	return quotas.get(item, 999999)

func get_quota_mode(item: String) -> QuotaMode:
	return quota_modes.get(item, QuotaMode.DO_FOREVER)

func is_quota_reached(item: String) -> bool:
	var mode = get_quota_mode(item)
	if mode == QuotaMode.PAUSED:
		return true
	if mode == QuotaMode.DO_FOREVER:
		return false
	var current = get_resource(item)
	var limit = get_quota(item)
	return current >= limit

func can_produce(item: String) -> bool:
	return not is_quota_reached(item)

func process_production_cycle(assigned_citizens: Dictionary) -> Dictionary:
	var report = {
		"produced": {},
		"consumed": {},
		"unfed_citizens": 0,
		"paused_by_quota": []
	}
	
	# 1. Farmers produce wheat
	var farmers = assigned_citizens.get("farmer", 0)
	var wheat_produced = farmers * 4
	add_resource("wheat", wheat_produced)
	report["produced"]["wheat"] = wheat_produced
	
	# 2. Bakers turn wheat into bread (1 wheat -> 2 bread) respecting quota
	var bakers = assigned_citizens.get("baker", 0)
	if can_produce("bread"):
		var wheat_needed = bakers * 2
		if get_quota_mode("bread") == QuotaMode.DO_UNTIL_X:
			var needed_bread = maxi(0, get_quota("bread") - get_resource("bread"))
			var max_wheat = int(ceil(float(needed_bread) / 2.0))
			wheat_needed = mini(wheat_needed, max_wheat)
			
		var wheat_used = mini(inventory.get("wheat", 0), wheat_needed)
		if wheat_used > 0:
			consume_resource("wheat", wheat_used)
			var bread_produced = wheat_used * 2
			add_resource("bread", bread_produced)
			report["produced"]["bread"] = bread_produced
			report["consumed"]["wheat"] = wheat_used
	else:
		report["paused_by_quota"].append("bread")

	# 3. Lumberjacks produce logs
	var lumberjacks = assigned_citizens.get("lumberjack", 0)
	var logs_produced = lumberjacks * 3
	add_resource("logs", logs_produced)
	report["produced"]["logs"] = logs_produced

	# 4. Miners produce stone, coal, and iron ore
	var miners = assigned_citizens.get("miner", 0)
	var stone_produced = miners * 3
	var iron_produced = miners * 1
	var coal_produced = miners * 2
	add_resource("stone", stone_produced)
	add_resource("iron_ore", iron_produced)
	add_resource("coal", coal_produced)
	report["produced"]["stone"] = stone_produced
	report["produced"]["iron_ore"] = iron_produced
	report["produced"]["coal"] = coal_produced

	# 5. Blacksmiths turn iron ore/ingots and logs into tools & weapons respecting quotas
	var blacksmiths = assigned_citizens.get("blacksmith", 0)
	for i in range(blacksmiths):
		if can_produce("tools"):
			if consume_resource("iron_ore", 2) and consume_resource("logs", 1):
				add_resource("tools", 1)
				report["produced"]["tools"] = report["produced"].get("tools", 0) + 1
		else:
			if not "tools" in report["paused_by_quota"]:
				report["paused_by_quota"].append("tools")

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
