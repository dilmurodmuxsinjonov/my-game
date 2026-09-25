# scripts/world/apothecary_bench.gd
# Voxel Lord: Feudal Realm - Milestone 21: Apothecary Herbalist & Alchemist Bench
# Inspired by Going Medieval (Apothecary & Herbalism) and RimWorld (Herbal Medicine Production)

class_name ApothecaryBench
extends Node3D

signal medicine_crafted(remedy_type: String, quantity: int)
signal stock_updated(item: String, amount: int)

var supply_chain: Node = null

var bench_stock: Dictionary = {
	"medicinal_herbs": 16,
	"fine_fabric": 8,
	"clean_water": 12,
	"garlic": 6,
	"sterile_bandage": 4,
	"herbal_poultice": 2,
	"plague_antidote": 1
}

func _init() -> void:
	pass

func add_ingredient(item: String, amount: int) -> void:
	bench_stock[item] = bench_stock.get(item, 0) + amount
	stock_updated.emit(item, bench_stock[item])

func craft_sterile_bandage(batches: int = 1) -> int:
	# 1 fine_fabric + 1 medicinal_herbs -> 2 sterile_bandage
	if bench_stock.get("fine_fabric", 0) < batches or bench_stock.get("medicinal_herbs", 0) < batches:
		return 0
	
	bench_stock["fine_fabric"] -= batches
	bench_stock["medicinal_herbs"] -= batches
	var produced: int = batches * 2
	bench_stock["sterile_bandage"] = bench_stock.get("sterile_bandage", 0) + produced
	
	if supply_chain and supply_chain.has_method("add_resource"):
		supply_chain.add_resource("sterile_bandage", produced)
	
	medicine_crafted.emit("sterile_bandage", produced)
	return produced

func craft_herbal_poultice(batches: int = 1) -> int:
	# 2 medicinal_herbs + 1 clean_water -> 1 herbal_poultice
	var herbs_needed: int = batches * 2
	if bench_stock.get("medicinal_herbs", 0) < herbs_needed or bench_stock.get("clean_water", 0) < batches:
		return 0
	
	bench_stock["medicinal_herbs"] -= herbs_needed
	bench_stock["clean_water"] -= batches
	bench_stock["herbal_poultice"] = bench_stock.get("herbal_poultice", 0) + batches
	
	if supply_chain and supply_chain.has_method("add_resource"):
		supply_chain.add_resource("herbal_poultice", batches)
	
	medicine_crafted.emit("herbal_poultice", batches)
	return batches

func craft_plague_antidote(batches: int = 1) -> int:
	# 3 medicinal_herbs + 1 garlic -> 1 plague_antidote
	var herbs_needed: int = batches * 3
	if bench_stock.get("medicinal_herbs", 0) < herbs_needed or bench_stock.get("garlic", 0) < batches:
		return 0
	
	bench_stock["medicinal_herbs"] -= herbs_needed
	bench_stock["garlic"] -= batches
	bench_stock["plague_antidote"] = bench_stock.get("plague_antidote", 0) + batches
	
	if supply_chain and supply_chain.has_method("add_resource"):
		supply_chain.add_resource("plague_antidote", batches)
	
	medicine_crafted.emit("plague_antidote", batches)
	return batches
