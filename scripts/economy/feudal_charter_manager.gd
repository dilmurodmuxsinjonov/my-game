# scripts/economy/feudal_charter_manager.gd
# Voxel Lord: Feudal Realm - Milestone 5: Historical Feudal Socio-Economics
# Manages the 5 distinct medieval social strata charters, legal rights,
# corvée obligations, tax brackets, military service, and revolt triggers.

class_name FeudalCharterManager
extends RefCounted

## Signals for social unrest and charter issuance
signal strata_revolted(strata_type: int, reason: String, revolt_type: String)
signal charter_issued(strata_type: int, charter_name: String)
signal tax_collected(strata_type: int, amount: float)

## 5 Distinct Medieval Social Strata Tiers
enum StrataTier {
	SERF = 0,
	YEOMAN = 1,
	GUILD_ARTISAN = 2,
	CLERGY = 3,
	NOBILITY = 4
}

## Charter registry caching the 5 canonical legal charters
static var _charter_cache: Dictionary = {}

static func _get_or_init_charters() -> Dictionary:
	if not _charter_cache.is_empty():
		return _charter_cache

	# 1. SERF: Manorial Labor Charter
	_charter_cache[StrataTier.SERF] = {
		"strata_type": StrataTier.SERF,
		"strata_name": "Serf",
		"charter_name": "Manorial Labor Charter",
		"owes_corvee_labor": true,
		"corvee_days_per_week": 3,
		"corvee_labor_hours": 24.0, # 3 days * 8 hours/day
		"is_tied_to_soil": true,
		"can_own_allodial_land": false,
		"can_trade_at_market": false,
		"must_serve_militia": false,
		"military_service_days_max": 0,
		"benefit_of_clergy": false,
		"has_high_justice": false,
		"sanctuary_days": 0,
		"quality_bonus": 0.0,
		"tax_tolerance": 0.25, # Revolts if direct taxation exceeds 25%
		"tax_bracket": {
			"min_tax": 0.05,
			"standard_tax": 0.15,
			"max_tax": 0.25,
			"tolerance": 0.25
		},
		"jurisdiction": "Hallmoot Manorial Court",
		"rights_and_protections": [
			"Customary strips in open demesne fields",
			"Right to forage fallen timber (by hook or by crook)",
			"Sanctuary in castle bailey during military raids"
		],
		"obligations": [
			"3 days per week corvée labor on lord's demesne",
			"Banality fee for lord's mill, oven, and winepress",
			"Merchet fine for marriage outside the manor",
			"Heriot mortuary death duty"
		],
		"revolt_trigger": "Jacquerie Revolt",
		"revolt_triggers": [
			"Tax rate exceeds 25%",
			"Food rationing drops below 1200 kcal/day (starvation > 3 days)",
			"Demesne corvée labor exceeds 4 days/week"
		],
		"revolt_description": "Agrarian peasant jacquerie revolt over oppressive corvée labor, starvation, or extortionate tax.",
		"base_morale": 50.0
	}

	# 2. YEOMAN: Freehold Yeomanry Charter
	_charter_cache[StrataTier.YEOMAN] = {
		"strata_type": StrataTier.YEOMAN,
		"strata_name": "Yeoman",
		"charter_name": "Freehold Yeomanry Charter",
		"owes_corvee_labor": false,
		"corvee_days_per_week": 0,
		"corvee_labor_hours": 0.0,
		"is_tied_to_soil": false,
		"can_own_allodial_land": true,
		"can_trade_at_market": true,
		"must_serve_militia": true,
		"military_service_days_max": 90, # Max 90 days/yr royal archer muster
		"benefit_of_clergy": false,
		"has_high_justice": false,
		"sanctuary_days": 0,
		"quality_bonus": 0.0,
		"tax_tolerance": 0.20, # Revolts if tax exceeds 20%
		"tax_bracket": {
			"min_tax": 0.05,
			"standard_tax": 0.10,
			"max_tax": 0.20,
			"tolerance": 0.20
		},
		"jurisdiction": "Royal Assize Common Law Court",
		"rights_and_protections": [
			"Freehold leasehold rights without arbitrary dispossession",
			"Right to sell agricultural surplus directly at borough markets",
			"Right to bear personal weapons (longbow, billhook, dagger)"
		],
		"obligations": [
			"Fixed annual cash quit-rent (cens)",
			"Mandatory weekly archery training at village butts",
			"Royal militia levy service up to 90 days per year"
		],
		"revolt_trigger": "Yeoman Tax Strike",
		"revolt_triggers": [
			"Direct tax exceeds 20%",
			"Royal militia muster exceeds 90 days/year",
			"Illegal royal enclosure of customary common pastures"
		],
		"revolt_description": "Yeoman archery skirmishes and tax strike over illegal enclosures, animal requisition, or muster exceeding 90 days.",
		"base_morale": 65.0
	}

	# 3. GUILD ARTISAN: Master Guild Incorporation Charter
	_charter_cache[StrataTier.GUILD_ARTISAN] = {
		"strata_type": StrataTier.GUILD_ARTISAN,
		"strata_name": "Guild Artisan",
		"charter_name": "Master Guild Incorporation Charter",
		"owes_corvee_labor": false,
		"corvee_days_per_week": 0,
		"corvee_labor_hours": 0.0,
		"is_tied_to_soil": false,
		"can_own_allodial_land": true,
		"can_trade_at_market": true,
		"must_serve_militia": false,
		"military_service_days_max": 0,
		"benefit_of_clergy": false,
		"has_high_justice": false,
		"sanctuary_days": 0,
		"quality_bonus": 0.20, # +20% quality certification bonus
		"craft_monopoly": true,
		"tax_tolerance": 0.15, # Revolts if tax exceeds 15%
		"tax_bracket": {
			"min_tax": 0.05,
			"standard_tax": 0.10,
			"max_tax": 0.15,
			"tolerance": 0.15
		},
		"jurisdiction": "Borough Court & Guild Wardens",
		"rights_and_protections": [
			"Exclusive urban craft manufacturing monopoly within borough limits",
			"Right to establish minimum trade price floors and quality standards",
			"Civic franchise: right to elect Guild Aldermen and sit on Town Council"
		],
		"obligations": [
			"Payment of municipal guild dues and booth tolls",
			"Supervision of 7-year apprentice indentures",
			"Compliance with civic production quotas and workshop regulations"
		],
		"revolt_trigger": "General Craft Strike",
		"revolt_triggers": [
			"Direct tax exceeds 15%",
			"Crown permits unlicensed foreign manufactured imports (voids guild monopoly)",
			"Crown imposes confiscatory price ceilings below guild cost floors"
		],
		"revolt_description": "Artisans lock workshops and forge doors over foreign manufacture dumping or infringement on guild monopoly.",
		"base_morale": 70.0
	}

	# 4. CLERGY: Ecclesiastical Diocesan Charter
	_charter_cache[StrataTier.CLERGY] = {
		"strata_type": StrataTier.CLERGY,
		"strata_name": "Clergy",
		"charter_name": "Ecclesiastical Diocesan Charter",
		"owes_corvee_labor": false,
		"corvee_days_per_week": 0,
		"corvee_labor_hours": 0.0,
		"is_tied_to_soil": false,
		"can_own_allodial_land": true,
		"can_trade_at_market": true,
		"must_serve_militia": false,
		"military_service_days_max": 0,
		"benefit_of_clergy": true, # Immune from secular criminal courts
		"has_high_justice": false,
		"sanctuary_days": 40, # 40 days holy sanctuary right
		"tithe_rate": 0.10, # Mandatory 10% tithe collected from parish
		"quality_bonus": 0.0,
		"tax_tolerance": 0.05, # Exempt from secular taxes; revolts if tax > 5%
		"tax_bracket": {
			"min_tax": 0.0,
			"standard_tax": 0.0,
			"max_tax": 0.05,
			"tolerance": 0.05
		},
		"jurisdiction": "Ecclesiastical Diocesan Court (Canon Law)",
		"rights_and_protections": [
			"Benefit of Clergy: immunity from secular criminal prosecution",
			"Right of Sanctuary: 40-day immunity on consecrated church grounds",
			"Collection of parish Church Tithe (decima, 10% of harvest/produce)"
		],
		"obligations": [
			"Conduct daily liturgy, masses, and divine intercessory prayers",
			"Administration of holy sacraments, mortuary rites, and parish hospice",
			"Maintenance of scriptoriums and canon law jurisprudence"
		],
		"revolt_trigger": "Ecclesiastical Interdict & Excommunication",
		"revolt_triggers": [
			"Imposition of secular taxation on glebe lands exceeding 5%",
			"Secular arrest of clerics on consecrated chapel ground",
			"Crown confiscation or despoliation of abbey treasures and relics"
		],
		"revolt_description": "Church declares interdict (halting rites and burials) and excommunication over secular arrest or despoiled glebe lands.",
		"base_morale": 80.0
	}

	# 5. NOBILITY: Seigneurial Fiefdom Patent
	_charter_cache[StrataTier.NOBILITY] = {
		"strata_type": StrataTier.NOBILITY,
		"strata_name": "Nobility",
		"charter_name": "Seigneurial Fiefdom Patent",
		"owes_corvee_labor": false,
		"corvee_days_per_week": 0,
		"corvee_labor_hours": 0.0,
		"is_tied_to_soil": false,
		"can_own_allodial_land": true,
		"can_trade_at_market": true,
		"must_serve_militia": true,
		"military_service_days_max": 40, # 40 days annual knightly campaign service
		"benefit_of_clergy": false,
		"has_high_justice": true, # High & Low Justice: power of pit and gallows
		"sanctuary_days": 0,
		"banality_tolls_allowed": true,
		"quality_bonus": 0.0,
		"tax_tolerance": 0.10, # Feudal dues only; revolts if tax exceeds 10%
		"tax_bracket": {
			"min_tax": 0.0,
			"standard_tax": 0.05,
			"max_tax": 0.10,
			"tolerance": 0.10
		},
		"jurisdiction": "Curia Regis & Noble Peer Jury",
		"rights_and_protections": [
			"High and Low Justice over manorial tenants (pit and gallows)",
			"Right to levy river bridge tolls, market stallages, and banalities",
			"Exclusive venery and venison hunting rights in royal forests"
		],
		"obligations": [
			"Feudal military campaign service: 40 days per year with knightly retinue",
			"Fealty oath and castle guard duties to the sovereign crown",
			"Attendance at the King's Great Council (Curia Regis)"
		],
		"revolt_trigger": "Baronial Rebellion & Civil War",
		"revolt_triggers": [
			"Crown tax or feudal tallage exceeds 10%",
			"Vassal fealty oath score drops below 15",
			"Encroachment on seigneurial jurisdictional autonomy or peer trial"
		],
		"revolt_description": "Noble barons wage civil war to depose monarch if fealty drops below 15 or seigneurial rights are encroached.",
		"base_morale": 85.0
	}

	return _charter_cache

## Fetch charter dictionary for a given strata type
static func get_strata_charter(strata_type: int) -> Dictionary:
	var charters = _get_or_init_charters()
	if charters.has(strata_type):
		return charters[strata_type].duplicate(true)
	# Fallback to serf
	return charters[StrataTier.SERF].duplicate(true)

## Fetch all 5 strata charters
static func get_all_charters() -> Dictionary:
	return _get_or_init_charters().duplicate(true)

## Fetch charter by its exact charter name string
static func get_charter_by_name(charter_name: String) -> Dictionary:
	var charters = _get_or_init_charters()
	for strata in charters.values():
		if strata.get("charter_name", "") == charter_name:
			return strata.duplicate(true)
	return {}

## Calculate tax due from citizen income based on strata tax bracket
static func calculate_tax_due(strata_type: int, gross_income: float, custom_rate: float = -1.0) -> float:
	if gross_income <= 0.0:
		return 0.0
	var charter = get_strata_charter(strata_type)
	var rate: float
	if custom_rate >= 0.0:
		rate = custom_rate
	else:
		rate = charter.get("tax_bracket", {}).get("standard_tax", 0.10)
	return gross_income * rate

## Evaluates whether current realm conditions trigger a revolt for the given strata
static func evaluate_revolt_risk(
	strata_type: int,
	current_tax_rate: float,
	starvation_days: int = 0,
	military_days: int = 0,
	fealty: float = 100.0,
	privileges_violated: bool = false,
	work_days_per_week: int = 3
) -> Dictionary:
	var charter = get_strata_charter(strata_type)
	var tolerance = charter.get("tax_tolerance", 0.20)
	var is_revolting: bool = false
	var trigger_reason: String = ""

	# Check Tax Tolerance
	if current_tax_rate > tolerance:
		is_revolting = true
		trigger_reason = "Tax rate (%.1f%%) exceeds %s tolerance (%.1f%%)." % [
			current_tax_rate * 100.0,
			charter["strata_name"],
			tolerance * 100.0
		]

	# Strata-specific trigger evaluations
	match strata_type:
		StrataTier.SERF:
			if starvation_days >= 3:
				is_revolting = true
				trigger_reason = "Serfs starving for %d days triggers Jacquerie Revolt." % starvation_days
			elif work_days_per_week > 4:
				is_revolting = true
				trigger_reason = "Excessive corvée labor (%d days/week > 4) triggers peasant uprising." % work_days_per_week

		StrataTier.YEOMAN:
			var max_muster = charter.get("military_service_days_max", 90)
			if military_days > max_muster:
				is_revolting = true
				trigger_reason = "Royal military muster (%d days) exceeds Yeoman statutory limit (%d days)." % [military_days, max_muster]
			elif privileges_violated:
				is_revolting = true
				trigger_reason = "Illegal enclosure of common pasture lands triggers Yeoman tax strike."

		StrataTier.GUILD_ARTISAN:
			if privileges_violated:
				is_revolting = true
				trigger_reason = "Unlicensed foreign manufacturing imports void craft monopoly, triggering General Craft Strike."

		StrataTier.CLERGY:
			if privileges_violated or current_tax_rate > 0.05:
				is_revolting = true
				trigger_reason = "Violation of benefit of clergy or secular taxation on glebe lands triggers Interdict."

		StrataTier.NOBILITY:
			if fealty < 15.0:
				is_revolting = true
				trigger_reason = "Baronial fealty dropped to %.1f (< 15.0), triggering civil war." % fealty
			elif privileges_violated:
				is_revolting = true
				trigger_reason = "Encroachment on seigneurial High Justice autonomy triggers Baronial rebellion."

	var revolt_type = charter.get("revolt_trigger", "Civil Unrest")
	var unrest_score: float = 0.0
	if is_revolting:
		unrest_score = 100.0
	else:
		# Partial unrest calculation based on proximity to thresholds
		var tax_ratio = clampf(current_tax_rate / maxf(0.01, tolerance), 0.0, 1.0)
		unrest_score = tax_ratio * 50.0

	return {
		"revolting": is_revolting,
		"trigger": trigger_reason,
		"revolt_type": revolt_type,
		"unrest_level": unrest_score,
		"strata_type": strata_type,
		"charter_name": charter["charter_name"]
	}

## Check if a citizen of this strata can legally relocate / leave the demesne
static func can_citizen_relocate(strata_type: int, has_manumission: bool = false) -> bool:
	var charter = get_strata_charter(strata_type)
	if charter.get("is_tied_to_soil", false):
		return has_manumission # Serfs need formal manumission or lord permission
	return true # Free strata can relocate freely

## Check if citizen of this strata can participate in open market trading
static func can_trade_at_market(strata_type: int) -> bool:
	var charter = get_strata_charter(strata_type)
	return charter.get("can_trade_at_market", false)

## Fetch weekly corvée labor hours owed by strata
static func get_corvee_labor_hours(strata_type: int) -> float:
	var charter = get_strata_charter(strata_type)
	return charter.get("corvee_labor_hours", 0.0)

## Fetch maximum annual military duty days for strata
static func get_military_duty_days(strata_type: int) -> int:
	var charter = get_strata_charter(strata_type)
	return charter.get("military_service_days_max", 0)

## Fetch tax rate tolerance before revolt
static func get_tax_tolerance(strata_type: int) -> float:
	var charter = get_strata_charter(strata_type)
	return charter.get("tax_tolerance", 0.20)

## Check whether strata enjoys Benefit of Clergy
static func has_benefit_of_clergy(strata_type: int) -> bool:
	var charter = get_strata_charter(strata_type)
	return charter.get("benefit_of_clergy", false)

## Check whether strata exercises High Justice (pit and gallows)
static func has_high_justice(strata_type: int) -> bool:
	var charter = get_strata_charter(strata_type)
	return charter.get("has_high_justice", false)
