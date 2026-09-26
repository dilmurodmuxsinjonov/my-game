# scripts/world/flour_silo.gd
# Voxel Lord: Feudal Realm - Milestone 30: Elevated Flour Silo & Granary Storage
# Moisture-sealed timber silo, vermin mitigation, and gravity discharge chute.

class_name FlourSilo
extends RefCounted

signal flour_deposited(silo_id: String, amount: int, total: int)
signal flour_dispensed(silo_id: String, amount: int, remaining: int)
signal flour_spoiled(silo_id: String, spoiled_amount: int)

var silo_id: String = "flour_silo_1"
var max_capacity: int = 120
var stored_flour: int = 40
var spoilage_mitigation_rate: float = 0.85 # 85% reduction in environmental decay

func _init(p_id: String = "flour_silo_1", initial_flour: int = 40) -> void:
	silo_id = p_id
	stored_flour = clamp(initial_flour, 0, max_capacity)

func deposit_flour(amount: int) -> int:
	var space = max_capacity - stored_flour
	var accepted = min(amount, space)
	stored_flour += accepted
	flour_deposited.emit(silo_id, accepted, stored_flour)
	return accepted

func dispense_to_cart(requested: int) -> int:
	var dispensed = min(requested, stored_flour)
	stored_flour -= dispensed
	flour_dispensed.emit(silo_id, dispensed, stored_flour)
	return dispensed

func calculate_monthly_spoilage(ambient_humidity: float = 0.6) -> int:
	if stored_flour <= 0:
		return 0
	# Base unsealed spoilage would be ~15% per month
	var unsealed_spoilage = float(stored_flour) * 0.15 * ambient_humidity
	# Sealed silo mitigates 85% of that spoilage
	var mitigated_spoilage = unsealed_spoilage * (1.0 - spoilage_mitigation_rate)
	var spoiled_sacks = int(round(mitigated_spoilage))

	if spoiled_sacks > 0:
		stored_flour = max(0, stored_flour - spoiled_sacks)
		flour_spoiled.emit(silo_id, spoiled_sacks)

	return spoiled_sacks

func get_fill_percentage() -> float:
	return (float(stored_flour) / float(max_capacity)) * 100.0
