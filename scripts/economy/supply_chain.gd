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
	"meat": 15,
	"cabbage": 10,
	"onion": 8,
	"carrot": 8,
	"sliced_cabbage": 0,
	"minced_beef": 0,
	"diced_onion": 0,
	"cabbage_stew": 0,
	"shepherd_pie": 0,
	"rock_salt": 10,
	"cured_meat": 0,
	"smoked_meat": 0,
	"compost": 0,
	"logs": 30,
	"planks": 15,
	"stone": 25,
	"coal": 12,
	"iron_ore": 6,
	"copper_ore": 4,
	"crushed_iron": 0,
	"crushed_copper": 0,
	"iron_ingots": 2,
	"copper_ingot": 0,
	"steel_ingot": 4,
	"tools": 10,
	"weapons": 5,
	"silver_ore": 0,
	"silver_ingot": 0,
	"support_beam": 4,
	"prospector_pick": 1,
	"mine_cart": 0,
	"mining_rail": 0,
	"ruby": 0,
	"sapphire": 0,
	"topaz": 0,
	"deep_gem": 0,
	"boss_trophy": 0,
	"gem_cutting_table": 0,
	"charcoal": 0,
	"iron_bloom": 0,
	"wrought_iron_ingot": 0,
	"tin_ore": 2,
	"tin_ingot": 0,
	"bronze_ingot": 0,
	"ceramic_mold": 2,
	"cast_bronze_blade": 0,
	"cast_bronze_pickaxe": 0,
	"bloomery": 0,
	"charcoal_pit": 0,
	"crucible": 0,
	"iron_sheet": 0,
	"copper_sheet": 0,
	"gold_coins": 50,
	"conveyor_belt": 0,
	"chute": 0,
	"mechanical_press": 0,
	"town_hall_desk": 0,
	"treasury_vault": 0,
	"guard_post": 0,
	"seared_brick": 16,
	"smeltery_controller": 0,
	"casting_basin": 0,
	"casting_table": 0,
	"bronze_block": 0,
	"steel_block": 0,
	"iron_block": 0
}

func salt_meat(amount: int) -> bool:
	if consume_resource("meat", amount) and consume_resource("rock_salt", amount):
		add_resource("cured_meat", amount)
		return true
	return false

func smoke_meat(amount: int) -> bool:
	var wood_needed = maxi(1, int(ceil(float(amount) / 2.0)))
	if consume_resource("meat", amount) and consume_resource("logs", wood_needed):
		add_resource("smoked_meat", amount)
		return true
	return false

func smelt_crushed_iron(amount: int = 1) -> bool:
	if inventory.get("crushed_iron", 0) >= amount and inventory.get("coal", 0) >= amount:
		consume_resource("crushed_iron", amount)
		consume_resource("coal", amount)
		add_resource("iron_ingots", amount * 2) # Double yield
		return true
	return false

func smelt_crushed_copper(amount: int = 1) -> bool:
	if inventory.get("crushed_copper", 0) >= amount and inventory.get("coal", 0) >= amount:
		consume_resource("crushed_copper", amount)
		consume_resource("coal", amount)
		add_resource("copper_ingot", amount * 2) # Double yield
		return true
	return false

func cook_cabbage_stew(amount: int = 1) -> bool:
	if inventory.get("sliced_cabbage", 0) >= amount and inventory.get("minced_beef", 0) >= amount and inventory.get("diced_onion", 0) >= amount:
		consume_resource("sliced_cabbage", amount)
		consume_resource("minced_beef", amount)
		consume_resource("diced_onion", amount)
		add_resource("cabbage_stew", amount * 2)
		return true
	return false

func cook_shepherd_pie(amount: int = 1) -> bool:
	if inventory.get("minced_beef", 0) >= amount and inventory.get("diced_onion", 0) >= amount and inventory.get("bread", 0) >= amount:
		consume_resource("minced_beef", amount)
		consume_resource("diced_onion", amount)
		consume_resource("bread", amount)
		add_resource("shepherd_pie", amount * 2)
		return true
	return false

func craft_support_beams(amount: int = 1) -> bool:
	var wood_needed = amount * 4
	if inventory.get("planks", 0) >= wood_needed:
		consume_resource("planks", wood_needed)
		add_resource("support_beam", amount * 2)
		return true
	return false

func craft_prospector_pick(amount: int = 1) -> bool:
	if inventory.get("planks", 0) >= (amount * 2) and (inventory.get("copper_ingot", 0) >= (amount * 2) or inventory.get("iron_ingots", 0) >= (amount * 2)):
		consume_resource("planks", amount * 2)
		if inventory.get("copper_ingot", 0) >= (amount * 2):
			consume_resource("copper_ingot", amount * 2)
		else:
			consume_resource("iron_ingots", amount * 2)
		add_resource("prospector_pick", amount)
		return true
	return false

func craft_mine_cart(amount: int = 1) -> bool:
	var iron_needed = amount * 5
	var wood_needed = amount * 4
	if inventory.get("iron_ingots", 0) >= iron_needed and inventory.get("planks", 0) >= wood_needed:
		consume_resource("iron_ingots", iron_needed)
		consume_resource("planks", wood_needed)
		add_resource("mine_cart", amount)
		return true
	return false

func craft_mining_rails(amount: int = 1) -> bool:
	var iron_needed = amount * 6
	var wood_needed = amount * 1
	if inventory.get("iron_ingots", 0) >= iron_needed and inventory.get("planks", 0) >= wood_needed:
		consume_resource("iron_ingots", iron_needed)
		consume_resource("planks", wood_needed)
		add_resource("mining_rail", amount * 16)
		return true
	return false

func smelt_silver_ore(amount: int = 1) -> bool:
	if inventory.get("silver_ore", 0) >= amount and inventory.get("coal", 0) >= amount:
		consume_resource("silver_ore", amount)
		consume_resource("coal", amount)
		add_resource("silver_ingot", amount)
		return true
	return false

func craft_gem_cutting_table(amount: int = 1) -> bool:
	var wood_needed = amount * 4
	var iron_needed = amount * 2
	var stone_needed = amount * 1
	if inventory.get("planks", 0) >= wood_needed and inventory.get("iron_ingots", 0) >= iron_needed and inventory.get("stone", 0) >= stone_needed:
		consume_resource("planks", wood_needed)
		consume_resource("iron_ingots", iron_needed)
		consume_resource("stone", stone_needed)
		add_resource("gem_cutting_table", amount)
		return true
	return false

func cut_gemstone(gem_name: String) -> bool:
	if inventory.get("gems", 0) >= 1:
		consume_resource("gems", 1)
		add_resource(gem_name, 1)
		return true
	return false

func place_trophy() -> bool:
	if consume_resource("boss_trophy", 1):
		morale = minf(100.0, morale + 10.0)
		morale_updated.emit(morale)
		return true
	return false

func craft_bloomery(amount: int = 1) -> bool:
	var stone_needed = amount * 8
	var iron_needed = amount * 2
	if inventory.get("stone", 0) >= stone_needed and inventory.get("iron_ingots", 0) >= iron_needed:
		consume_resource("stone", stone_needed)
		consume_resource("iron_ingots", iron_needed)
		add_resource("bloomery", amount)
		return true
	return false

func craft_charcoal_pit(amount: int = 1) -> bool:
	var logs_needed = amount * 4
	if inventory.get("logs", 0) >= logs_needed:
		consume_resource("logs", logs_needed)
		add_resource("charcoal_pit", amount)
		return true
	return false

func craft_crucible(amount: int = 1) -> bool:
	var stone_needed = amount * 4
	if inventory.get("stone", 0) >= stone_needed:
		consume_resource("stone", stone_needed)
		add_resource("crucible", amount)
		return true
	return false

func smelt_iron_bloom(batches: int = 1) -> bool:
	var ore_needed = batches * 2
	var fuel_needed = batches * 2
	if inventory.get("iron_ore", 0) >= ore_needed and inventory.get("charcoal", 0) >= fuel_needed:
		consume_resource("iron_ore", ore_needed)
		consume_resource("charcoal", fuel_needed)
		add_resource("iron_bloom", batches)
		return true
	return false

func refine_bloom_on_anvil(batches: int = 1) -> bool:
	if inventory.get("iron_bloom", 0) >= batches:
		consume_resource("iron_bloom", batches)
		add_resource("wrought_iron_ingot", batches)
		return true
	return false

func cast_bronze_tool(mold_type: String) -> bool:
	if inventory.get("copper_ingot", 0) >= 7 and inventory.get("tin_ingot", 0) >= 1 and inventory.get("ceramic_mold", 0) >= 1:
		consume_resource("copper_ingot", 7)
		consume_resource("tin_ingot", 1)
		if mold_type == "sword_blade":
			add_resource("cast_bronze_blade", 1)
		elif mold_type == "pickaxe_head":
			add_resource("cast_bronze_pickaxe", 1)
		else:
			add_resource("bronze_ingot", 8)
		return true
	return false

func craft_conveyor_belt(amount: int = 1) -> bool:
	var iron_needed = amount * 1
	var leather_needed = amount * 1
	if inventory.get("iron_ingots", 0) >= iron_needed and inventory.get("leather", 0) >= leather_needed:
		consume_resource("iron_ingots", iron_needed)
		consume_resource("leather", leather_needed)
		add_resource("conveyor_belt", amount)
		return true
	return false

func craft_chute(amount: int = 1) -> bool:
	var iron_needed = amount * 2
	if inventory.get("iron_ingots", 0) >= iron_needed:
		consume_resource("iron_ingots", iron_needed)
		add_resource("chute", amount)
		return true
	return false

func craft_mechanical_press(amount: int = 1) -> bool:
	var iron_needed = amount * 4
	var stone_needed = amount * 4
	if inventory.get("iron_ingots", 0) >= iron_needed and inventory.get("stone", 0) >= stone_needed:
		consume_resource("iron_ingots", iron_needed)
		consume_resource("stone", stone_needed)
		add_resource("mechanical_press", amount)
		return true
	return false

func stamp_coins(amount: int = 1) -> bool:
	if inventory.get("gold_ingot", 0) >= amount:
		consume_resource("gold_ingot", amount)
		add_resource("gold_coins", amount * 10)
		return true
	return false

func stamp_iron_sheets(amount: int = 1) -> bool:
	if inventory.get("wrought_iron_ingot", 0) >= amount:
		consume_resource("wrought_iron_ingot", amount)
		add_resource("iron_sheet", amount)
		return true
	elif inventory.get("iron_ingots", 0) >= amount:
		consume_resource("iron_ingots", amount)
		add_resource("iron_sheet", amount)
		return true
	return false

func craft_town_hall_desk(amount: int = 1) -> bool:
	var wood_needed = amount * 6
	var iron_needed = amount * 2
	if inventory.get("planks", 0) >= wood_needed and inventory.get("iron_ingots", 0) >= iron_needed:
		consume_resource("planks", wood_needed)
		consume_resource("iron_ingots", iron_needed)
		add_resource("town_hall_desk", amount)
		return true
	return false

func craft_treasury_vault(amount: int = 1) -> bool:
	var stone_needed = amount * 8
	var iron_needed = amount * 4
	if inventory.get("stone", 0) >= stone_needed and inventory.get("iron_ingots", 0) >= iron_needed:
		consume_resource("stone", stone_needed)
		consume_resource("iron_ingots", iron_needed)
		add_resource("treasury_vault", amount)
		return true
	return false

func craft_guard_post(amount: int = 1) -> bool:
	var wood_needed = amount * 4
	var iron_needed = amount * 2
	if inventory.get("logs", 0) >= wood_needed and inventory.get("iron_ingots", 0) >= iron_needed:
		consume_resource("logs", wood_needed)
		consume_resource("iron_ingots", iron_needed)
		add_resource("guard_post", amount)
		return true
	return false

func craft_seared_brick(amount: int = 4) -> bool:
	var stone_needed = amount
	var coal_needed = int(ceil(float(amount) / 4.0))
	if inventory.get("stone", 0) >= stone_needed and inventory.get("coal", 0) >= coal_needed:
		consume_resource("stone", stone_needed)
		consume_resource("coal", coal_needed)
		add_resource("seared_brick", amount)
		return true
	return false

func craft_smeltery_controller(amount: int = 1) -> bool:
	var brick_needed = amount * 8
	var cu_needed = amount * 1
	if inventory.get("seared_brick", 0) >= brick_needed and inventory.get("copper_ingot", 0) >= cu_needed:
		consume_resource("seared_brick", brick_needed)
		consume_resource("copper_ingot", cu_needed)
		add_resource("smeltery_controller", amount)
		return true
	return false

func craft_casting_basin(amount: int = 1) -> bool:
	var brick_needed = amount * 7
	if inventory.get("seared_brick", 0) >= brick_needed:
		consume_resource("seared_brick", brick_needed)
		add_resource("casting_basin", amount)
		return true
	return false

func craft_casting_table(amount: int = 1) -> bool:
	var brick_needed = amount * 7
	if inventory.get("seared_brick", 0) >= brick_needed:
		consume_resource("seared_brick", brick_needed)
		add_resource("casting_table", amount)
		return true
	return false

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
