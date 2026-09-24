class_name CrownTribute
extends RefCounted

## Royal Crown Tribute & Sheriff System (External Economic Pressure).
## Inspired by Medieval Dynasty and Bellwright:
## The Crown Sheriff visits seasonally to collect feudal land & demographic taxes.
## Defaulting triggers the Crown's Punitive Expedition (Royal Enforcers).

signal tribute_assessed(amount_due: int, due_day: int)
signal sheriff_arrived(amount_due: int)
signal tribute_paid(amount: int, remaining_gold: int)
signal payment_defaulted(failed_count: int, punitive_raid_triggered: bool)

const BASE_TRIBUTE: int = 40 # Base sovereign charter tax
const TAX_PER_BUILDING: int = 5 # Land occupancy fee
const TAX_PER_CITIZEN: int = 2 # Poll tax

var current_cycle_day: int = 1
var cycle_duration_days: int = 7 # Every season (7 in-game days)
var tribute_due: int = 0
var is_sheriff_visiting: bool = false
var failed_payments: int = 0
var punitive_expedition_active: bool = false

func calculate_tribute(total_buildings: int, total_citizens: int) -> int:
	var total = BASE_TRIBUTE + (total_buildings * TAX_PER_BUILDING) + (total_citizens * TAX_PER_CITIZEN)
	tribute_due = total
	emit_signal("tribute_assessed", tribute_due, cycle_duration_days)
	return tribute_due

func advance_day(total_buildings: int, total_citizens: int) -> void:
	current_cycle_day += 1
	if current_cycle_day >= cycle_duration_days:
		calculate_tribute(total_buildings, total_citizens)
		is_sheriff_visiting = true
		emit_signal("sheriff_arrived", tribute_due)

func pay_tribute(treasury_vault: TreasuryVault) -> bool:
	if not is_sheriff_visiting:
		return false
	if treasury_vault.treasury_gold >= tribute_due:
		treasury_vault.treasury_gold -= tribute_due
		var paid_amount = tribute_due
		is_sheriff_visiting = false
		current_cycle_day = 0
		failed_payments = 0
		punitive_expedition_active = false
		emit_signal("tribute_paid", paid_amount, treasury_vault.treasury_gold)
		return true
	return false

func default_payment() -> void:
	if not is_sheriff_visiting:
		return
	failed_payments += 1
	is_sheriff_visiting = false
	current_cycle_day = 0
	
	# After 2 consecutive defaulted tributes, Crown sends punitive army
	if failed_payments >= 2:
		punitive_expedition_active = true
	emit_signal("payment_defaulted", failed_payments, punitive_expedition_active)
