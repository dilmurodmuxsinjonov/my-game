class_name TreasuryVault
extends StaticBody3D

## Feudal Royal Treasury Vault & Tax Bureau.
## Secure strongbox managing the kingdom's physical coinage (Gold Coins).
## Coordinates the daily/weekly feudal taxation cycle, military guard payroll,
## and royal festival morale subsidies.

signal taxes_collected(total_collected: int, new_balance: int)
signal payroll_disbursed(guards_paid: int, success: bool)
signal festival_hosted(morale_gain: float)

@export var tax_rate: float = 0.10 # 10% standard feudal tax
@export var guard_wage: int = 1 # 1 gold coin per guard per cycle

var supply_chain: SupplyChain = null
var stored_coins: int = 50

var model_instance: Node3D = null
var collision_box: CollisionShape3D = null
var prompt_label: Label3D = null
var coin_light: OmniLight3D = null

func _ready() -> void:
	add_to_group("interactive_workstations")
	add_to_group("treasury_safes")
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.5, 1.1, 1.1)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.55, 0)
	add_child(collision_box)

	var glb_path = "res://assets/models/treasury_vault.glb"
	if ResourceLoader.exists(glb_path):
		var res = load(glb_path)
		if res:
			model_instance = res.instantiate()
			add_child(model_instance)

	coin_light = OmniLight3D.new()
	coin_light.light_color = Color(1.0, 0.85, 0.2)
	coin_light.light_energy = 1.2
	coin_light.omni_range = 3.5
	coin_light.position = Vector3(0, 0.8, 0)
	add_child(coin_light)

	prompt_label = Label3D.new()
	prompt_label.text = "🪙 Royal Treasury Vault\nStored: %d Coins\n[E] Manage Taxes & Payroll" % stored_coins
	prompt_label.position = Vector3(0, 1.4, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 20
	prompt_label.modulate = Color(1.0, 0.85, 0.2)
	add_child(prompt_label)

func deposit_coins(amount: int) -> void:
	stored_coins += amount
	if supply_chain:
		supply_chain.add_resource("gold_coins", amount)
	_update_prompt()

func collect_taxes(employed_citizens: int) -> Dictionary:
	var revenue = calculate_tax_revenue(employed_citizens, tax_rate)
	stored_coins += revenue
	if supply_chain:
		supply_chain.add_resource("gold_coins", revenue)
		
	var morale_delta = calculate_tax_morale_impact(tax_rate)
	if supply_chain:
		supply_chain.morale = clampf(supply_chain.morale + morale_delta, 0.0, 100.0)
		supply_chain.morale_updated.emit(supply_chain.morale)

	emit_signal("taxes_collected", revenue, stored_coins)
	_update_prompt()
	return {
		"revenue": revenue,
		"total_coins": stored_coins,
		"morale_delta": morale_delta,
		"message": "Collected %d gold coins from %d employed subjects." % [revenue, employed_citizens]
	}

func disburse_guard_payroll(guard_count: int) -> Dictionary:
	var total_wages = calculate_payroll_cost(guard_count, guard_wage)
	var available = stored_coins
	if supply_chain:
		available = supply_chain.inventory.get("gold_coins", stored_coins)

	if available >= total_wages:
		stored_coins = maxi(0, stored_coins - total_wages)
		if supply_chain:
			supply_chain.consume_resource("gold_coins", total_wages)
		emit_signal("payroll_disbursed", guard_count, true)
		_update_prompt()
		return {
			"success": true,
			"wages_paid": total_wages,
			"guards_paid": guard_count,
			"message": "Paid %d gold coins in military wages to %d garrison guards." % [total_wages, guard_count]
		}
	else:
		# Unpaid military crisis!
		if supply_chain:
			supply_chain.morale = clampf(supply_chain.morale - 25.0, 0.0, 100.0)
			supply_chain.morale_updated.emit(supply_chain.morale)
		emit_signal("payroll_disbursed", 0, false)
		_update_prompt()
		return {
			"success": false,
			"wages_paid": 0,
			"guards_paid": 0,
			"message": "⚠️ TREASURY INSOLVENT! Unable to pay garrison guards! Morale collapsed by -25."
		}

func host_royal_festival() -> Dictionary:
	var festival_cost = 20
	var available = stored_coins
	if supply_chain:
		available = supply_chain.inventory.get("gold_coins", stored_coins)

	if available >= festival_cost:
		stored_coins -= festival_cost
		if supply_chain:
			supply_chain.consume_resource("gold_coins", festival_cost)
			supply_chain.morale = minf(100.0, supply_chain.morale + 25.0)
			supply_chain.morale_updated.emit(supply_chain.morale)
		emit_signal("festival_hosted", 25.0)
		_update_prompt()
		return {
			"success": true,
			"morale_gain": 25.0,
			"message": "Hosted a grand royal tournament & feast! Kingdom morale boosted by +25."
		}
	return {"success": false, "message": "Requires 20 Gold Coins in treasury to fund a royal festival."}

func _update_prompt() -> void:
	if not prompt_label:
		return
	var bal = stored_coins
	if supply_chain:
		bal = supply_chain.inventory.get("gold_coins", stored_coins)
	prompt_label.text = "🪙 Royal Treasury Vault\nStored: %d Coins | Tax: %.0f%%\n[E] Taxation & Payroll" % [bal, tax_rate * 100.0]
	prompt_label.modulate = Color(1.0, 0.85, 0.2) if bal >= 10 else Color(1.0, 0.4, 0.3)

# --- Static Simulation & Balance Calculations ---

static func calculate_tax_revenue(employed_count: int, rate: float) -> int:
	## Base 2 coins per employed subject * tax rate multiplier (1.0 at 10%)
	var base_per_citizen = 2.0
	var multiplier = rate / 0.10
	return int(round(float(employed_count) * base_per_citizen * multiplier))

static func calculate_payroll_cost(guard_count: int, wage_per_guard: int = 1) -> int:
	return guard_count * wage_per_guard

static func calculate_tax_morale_impact(rate: float) -> float:
	## Standard tax (10%): 0.0 impact
	## Low tax (<5%): +10.0 morale boost
	## Heavy tax (20%): -10.0 morale drop
	## Tyrannical tax (>30%): -25.0 morale crash
	if rate <= 0.05:
		return 10.0
	elif rate <= 0.12:
		return 0.0
	elif rate <= 0.20:
		return -10.0
	else:
		return -25.0
