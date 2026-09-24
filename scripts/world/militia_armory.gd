# scripts/world/militia_armory.gd
# Voxel Lord: Feudal Realm - Milestone 20: Feudal Peasant Militia & Armory Muster System
# Inspired by Manor Lords (Burgage Levies & Weapon Stocks) and Bellwright (Militia Armaments)

class_name MilitiaArmory
extends Node3D

signal militia_mustered(squad_name: String, soldier_count: int)
signal militia_demobilized(squad_name: String, soldier_count: int)
signal armory_stock_changed(item: String, new_amount: int)

# Armory storage capacity
const MAX_EQUIPMENT_CAPACITY: int = 120

# Current weapon & protective gear inventory
var armory_stock: Dictionary = {
	"spear": 12,
	"shield": 12,
	"iron_helmet": 8,
	"gambeson": 8,
	"hunting_bow": 6,
	"arrow": 120
}

# Active mustered squads: Dictionary[squad_name, Array[Dictionary]]
var active_squads: Dictionary = {}

func _init() -> void:
	pass

func add_equipment(item: String, amount: int) -> bool:
	if not armory_stock.has(item):
		armory_stock[item] = 0
	
	var total_items: int = 0
	for count in armory_stock.values():
		total_items += count
	
	if total_items + amount > MAX_EQUIPMENT_CAPACITY:
		return false
	
	armory_stock[item] += amount
	armory_stock_changed.emit(item, armory_stock[item])
	return true

func remove_equipment(item: String, amount: int) -> bool:
	if not armory_stock.has(item) or armory_stock[item] < amount:
		return false
	armory_stock[item] -= amount
	armory_stock_changed.emit(item, armory_stock[item])
	return true

func can_equip_spearman() -> bool:
	return armory_stock.get("spear", 0) >= 1 and armory_stock.get("shield", 0) >= 1

func can_equip_archer() -> bool:
	return armory_stock.get("hunting_bow", 0) >= 1 and armory_stock.get("arrow", 0) >= 12

func muster_squad(squad_name: String, citizen_ids: Array, unit_type: String = "SPEARMAN") -> Dictionary:
	var mustered_soldiers: Array = []
	var unequipped_count: int = 0
	
	for citizen_id in citizen_ids:
		var kit_granted: bool = false
		var soldier_gear: Dictionary = {
			"citizen_id": citizen_id,
			"role": unit_type,
			"items": []
		}
		
		if unit_type == "SPEARMAN":
			if can_equip_spearman():
				remove_equipment("spear", 1)
				remove_equipment("shield", 1)
				soldier_gear["items"].append("spear")
				soldier_gear["items"].append("shield")
				
				# Optional armor piece if available
				if armory_stock.get("iron_helmet", 0) >= 1:
					remove_equipment("iron_helmet", 1)
					soldier_gear["items"].append("iron_helmet")
				elif armory_stock.get("gambeson", 0) >= 1:
					remove_equipment("gambeson", 1)
					soldier_gear["items"].append("gambeson")
				
				kit_granted = true
		elif unit_type == "ARCHER":
			if can_equip_archer():
				remove_equipment("hunting_bow", 1)
				remove_equipment("arrow", 12)
				soldier_gear["items"].append("hunting_bow")
				soldier_gear["items"].append("arrow_quiver_12")
				
				if armory_stock.get("gambeson", 0) >= 1:
					remove_equipment("gambeson", 1)
					soldier_gear["items"].append("gambeson")
				
				kit_granted = true
		
		if kit_granted:
			mustered_soldiers.append(soldier_gear)
		else:
			unequipped_count += 1
	
	active_squads[squad_name] = mustered_soldiers
	militia_mustered.emit(squad_name, mustered_soldiers.size())
	
	return {
		"squad_name": squad_name,
		"unit_type": unit_type,
		"mustered_count": mustered_soldiers.size(),
		"unequipped_count": unequipped_count,
		"combat_readiness": float(mustered_soldiers.size()) / float(max(1, citizen_ids.size()))
	}

func demobilize_squad(squad_name: String) -> int:
	if not active_squads.has(squad_name):
		return 0
	
	var squad_soldiers: Array = active_squads[squad_name]
	var returned_soldiers_count: int = squad_soldiers.size()
	
	for soldier in squad_soldiers:
		for item in soldier.get("items", []):
			if item == "arrow_quiver_12":
				# Recover partial arrows (8 out of 12)
				add_equipment("arrow", 8)
			else:
				add_equipment(item, 1)
	
	active_squads.erase(squad_name)
	militia_demobilized.emit(squad_name, returned_soldiers_count)
	return returned_soldiers_count

func get_total_squad_military_rating(squad_name: String) -> int:
	if not active_squads.has(squad_name):
		return 0
	
	var total_power: int = 0
	for soldier in active_squads[squad_name]:
		var soldier_power: int = 10 # Base peasant strength
		for item in soldier.get("items", []):
			match item:
				"spear": soldier_power += 15
				"shield": soldier_power += 12
				"hunting_bow": soldier_power += 18
				"iron_helmet": soldier_power += 10
				"gambeson": soldier_power += 8
		total_power += soldier_power
	return total_power
