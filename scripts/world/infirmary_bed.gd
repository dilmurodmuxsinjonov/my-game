# scripts/world/infirmary_bed.gd
# Voxel Lord: Feudal Realm - Milestone 21: Infirmary Hospital Bed & Surgical Triage
# Inspired by RimWorld (Hospital Beds & Tend Quality) and Going Medieval (Convalescence)

class_name InfirmaryBed
extends Node3D

signal patient_admitted(patient_id: String, hp: float, infected: bool)
signal patient_treated(patient_id: String, remedy_used: String, new_hp: float, infection_cured: bool)
signal patient_discharged(patient_id: String, morale_bonus: int)

var supply_chain: Node = null

var is_occupied: bool = false
var current_patient_id: String = ""
var patient_hp: float = 100.0
var patient_max_hp: float = 100.0
var has_infection: bool = false
var has_bleeding: bool = false
var physician_assigned: bool = true

const BASE_RECOVERY_RATE: float = 2.5 # HP per minute
const PHYSICIAN_BONUS_RATE: float = 1.5
const MORALE_RECOVERY_BONUS: int = 8

func _init() -> void:
	pass

func admit_patient(patient_id: String, current_hp: float, max_hp: float, infected: bool = false, bleeding: bool = false) -> bool:
	if is_occupied:
		return false
	
	is_occupied = true
	current_patient_id = patient_id
	patient_hp = clampf(current_hp, 1.0, max_hp)
	patient_max_hp = max_hp
	has_infection = infected
	has_bleeding = bleeding
	
	patient_admitted.emit(patient_id, patient_hp, has_infection)
	return true

func apply_remedy(remedy_type: String) -> Dictionary:
	if not is_occupied:
		return {"success": false, "reason": "NO_PATIENT"}
	
	var hp_restored: float = 0.0
	var cured_infection: bool = false
	var stopped_bleeding: bool = false
	
	match remedy_type:
		"sterile_bandage":
			hp_restored = 15.0
			if has_bleeding:
				has_bleeding = false
				stopped_bleeding = true
		"herbal_poultice":
			hp_restored = 30.0
			if has_infection:
				has_infection = false
				cured_infection = true
		"plague_antidote":
			hp_restored = 45.0
			has_infection = false
			has_bleeding = false
			cured_infection = true
			stopped_bleeding = true
		_:
			return {"success": false, "reason": "UNKNOWN_REMEDY"}
	
	patient_hp = minf(patient_max_hp, patient_hp + hp_restored)
	patient_treated.emit(current_patient_id, remedy_type, patient_hp, cured_infection)
	
	var discharged: bool = false
	if patient_hp >= patient_max_hp and not has_infection and not has_bleeding:
		discharge_patient()
		discharged = true
	
	return {
		"success": true,
		"remedy": remedy_type,
		"new_hp": patient_hp,
		"infection_cured": cured_infection,
		"bleeding_stopped": stopped_bleeding,
		"discharged": discharged
	}

func process_rest(minutes: float) -> float:
	if not is_occupied:
		return 0.0
	
	var rate: float = BASE_RECOVERY_RATE
	if physician_assigned:
		rate += PHYSICIAN_BONUS_RATE
	
	# Infections halve natural rest recovery until treated with poultice
	if has_infection:
		rate *= 0.5
	
	var gained: float = rate * minutes
	patient_hp = minf(patient_max_hp, patient_hp + gained)
	
	if patient_hp >= patient_max_hp and not has_infection and not has_bleeding:
		discharge_patient()
	
	return patient_hp

func discharge_patient() -> String:
	if not is_occupied:
		return ""
	
	var discharged_id: String = current_patient_id
	is_occupied = false
	current_patient_id = ""
	has_infection = false
	has_bleeding = false
	
	patient_discharged.emit(discharged_id, MORALE_RECOVERY_BONUS)
	return discharged_id
