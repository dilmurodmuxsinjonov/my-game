class_name AgronomySoilManager
extends Node

## Manages voxel-level NPK soil chemistry, Liebig's Law of the Minimum yield calculation,
## 9-crop depletion rates, legume Nitrogen fixation, monoculture blight,
## canonical 4-year crop rotations, and organic soil amendments.
## Aligns with MASTER_GDD.md §§36, 37 and PROJECT.md M3 interface contracts.

signal soil_depleted(pos: Vector3i, scarcest_element: String)
signal monoculture_blight_outbreak(pos: Vector3i)
signal rotation_year_advanced(new_year: int)

# Farmland position (Vector3i or normalized key) -> FarmlandSoilData
var soil_registry: Dictionary = {}
var current_rotation_year: int = 0 # 0 = Wheat, 1 = Barley, 2 = Legumes, 3 = Fallow

# --- Farmland Soil State Data Structure ---
class FarmlandSoilData extends RefCounted:
	var pos: Vector3i
	var nitrogen: float = 100.0   # N % [0.0, 120.0]
	var phosphorus: float = 100.0 # P % [0.0, 120.0]
	var potassium: float = 100.0  # K % [0.0, 120.0]
	var moisture: float = 60.0    # Moisture % [0.0, 100.0]
	var compaction: float = 0.0   # Compaction % [0.0, 100.0]
	var consecutive_crop_id: String = ""
	var consecutive_plantings: int = 0
	var has_terra_preta: bool = false
	var rotation_cycle: int = 0

# --- 9-Crop NPK Depletion & Demand Master Matrix ---
const CROP_NPK_PROFILE: Dictionary = {
	"wheat":   {"N_demand": 100.0, "P_demand": 60.0, "K_demand": 60.0,  "dN": 14.0,  "dP": 8.0,  "dK": 8.0,  "base_yield": 8},
	"barley":  {"N_demand": 80.0,  "P_demand": 60.0, "K_demand": 50.0,  "dN": 12.0,  "dP": 8.0,  "dK": 6.0,  "base_yield": 7},
	"rye":     {"N_demand": 60.0,  "P_demand": 40.0, "K_demand": 40.0,  "dN": 8.0,   "dP": 5.0,  "dK": 5.0,  "base_yield": 6},
	"cabbage": {"N_demand": 70.0,  "P_demand": 50.0, "K_demand": 120.0, "dN": 8.0,   "dP": 6.0,  "dK": 16.0, "base_yield": 12},
	"turnip":  {"N_demand": 40.0,  "P_demand": 40.0, "K_demand": 40.0,  "dN": 5.0,   "dP": 5.0,  "dK": 5.0,  "base_yield": 14},
	"carrot":  {"N_demand": 50.0,  "P_demand": 70.0, "K_demand": 40.0,  "dN": 6.0,   "dP": 8.0,  "dK": 5.0,  "base_yield": 10},
	"flax":    {"N_demand": 80.0,  "P_demand": 80.0, "K_demand": 80.0,  "dN": 10.0,  "dP": 10.0, "dK": 10.0, "base_yield": 6},
	"hops":    {"N_demand": 90.0,  "P_demand": 80.0, "K_demand": 90.0,  "dN": 12.0,  "dP": 10.0, "dK": 12.0, "base_yield": 10},
	"peas":    {"N_demand": 20.0,  "P_demand": 30.0, "K_demand": 30.0,  "dN": -22.0, "dP": 2.0,  "dK": 2.0,  "base_yield": 6}
}

# Aliases for flexible crop identification
const CROP_ALIASES: Dictionary = {
	"crop_wheat": "wheat",
	"crop_barley": "barley",
	"crop_rye": "rye",
	"crop_cabbage": "cabbage",
	"crop_turnip": "turnip",
	"crop_carrot": "carrot",
	"crop_flax": "flax",
	"crop_hops": "hops",
	"crop_peas": "peas",
	"legumes": "peas",
	"roots": "turnip"
}

func _normalize_pos(p: Variant) -> Vector3i:
	if p is Vector3i:
		return p
	elif p is Vector2i:
		return Vector3i(p.x, 0, p.y)
	elif p is Vector3:
		return Vector3i(int(floor(p.x)), int(floor(p.y)), int(floor(p.z)))
	elif p is Vector2:
		return Vector3i(int(floor(p.x)), 0, int(floor(p.y)))
	return Vector3i.ZERO

func _get_crop_key(crop_id: String) -> String:
	var lower = crop_id.to_lower().strip_edges()
	if CROP_ALIASES.has(lower):
		return CROP_ALIASES[lower]
	if CROP_NPK_PROFILE.has(lower):
		return lower
	# Search prefix
	for k in CROP_NPK_PROFILE.keys():
		if k in lower:
			return k
	return "wheat"

func register_farmland(pos: Variant) -> FarmlandSoilData:
	var vpos = _normalize_pos(pos)
	if not soil_registry.has(vpos):
		var data = FarmlandSoilData.new()
		data.pos = vpos
		soil_registry[vpos] = data
	return soil_registry[vpos]

func get_soil_data(pos: Variant) -> FarmlandSoilData:
	var vpos = _normalize_pos(pos)
	if not soil_registry.has(vpos):
		return register_farmland(vpos)
	return soil_registry[vpos]

# --- PROJECT.md M3 Interface Contract ---

## Applies Liebig's Law of the Minimum: min(N/N_req, P/P_req, K/K_req)
## Returns yield multiplier scalar (e.g. 1.0 for 100% satisfied demand)
func calculate_yield_multiplier(pos: Variant, crop_id: String) -> float:
	var soil = get_soil_data(pos)
	var crop_key = _get_crop_key(crop_id)
	var profile = CROP_NPK_PROFILE.get(crop_key, CROP_NPK_PROFILE["wheat"])
	
	var ratio_n = soil.nitrogen / profile["N_demand"]
	var ratio_p = soil.phosphorus / profile["P_demand"]
	var ratio_k = soil.potassium / profile["K_demand"]
	
	var min_ratio = minf(ratio_n, minf(ratio_p, ratio_k))
	return maxf(0.10, min_ratio)

## Returns effective fertility percentage [10.0%, 120.0%]
func calculate_effective_fertility(pos: Variant, crop_id: String) -> float:
	var min_ratio = calculate_yield_multiplier(pos, crop_id)
	return clampf(min_ratio * 100.0, 10.0, 120.0)

# --- Harvest & Crop Cycle Processing ---

func process_harvest(pos: Variant, crop_id: String, farmer_skill: int = 1) -> Dictionary:
	var vpos = _normalize_pos(pos)
	var soil = get_soil_data(vpos)
	var crop_key = _get_crop_key(crop_id)
	var profile = CROP_NPK_PROFILE.get(crop_key, CROP_NPK_PROFILE["wheat"])
	
	# Monoculture tracking
	if soil.consecutive_crop_id == crop_key:
		soil.consecutive_plantings += 1
		if soil.consecutive_plantings >= 3:
			emit_signal("monoculture_blight_outbreak", vpos)
			return {"yield": 0, "blight": true, "fertility_post": 0.0}
	else:
		soil.consecutive_crop_id = crop_key
		soil.consecutive_plantings = 1

	var penalty_mult = 1.0 + 0.50 * (soil.consecutive_plantings - 1)
	var max_cap = 120.0 if soil.has_terra_preta else 100.0

	# Apply nutrient drain or fixation
	var dn = profile["dN"]
	var dp = profile["dP"]
	var dk = profile["dK"]
	
	if dn < 0.0:
		# Biological Nitrogen Fixation (Legumes restore Nitrogen!)
		soil.nitrogen = minf(max_cap, soil.nitrogen - dn)
	else:
		soil.nitrogen = clampf(soil.nitrogen - dn * penalty_mult, 0.0, max_cap)
		
	soil.phosphorus = clampf(soil.phosphorus - dp * penalty_mult, 0.0, max_cap)
	soil.potassium = clampf(soil.potassium - dk * penalty_mult, 0.0, max_cap)

	# Scarcity alert if any nutrient collapses below 15%
	if soil.nitrogen < 15.0:
		emit_signal("soil_depleted", vpos, "Nitrogen")
	elif soil.phosphorus < 15.0:
		emit_signal("soil_depleted", vpos, "Phosphorus")
	elif soil.potassium < 15.0:
		emit_signal("soil_depleted", vpos, "Potassium")

	# Liebig yield calculation
	var yield_mult = calculate_yield_multiplier(vpos, crop_key)
	var fertility = clampf(yield_mult * 100.0, 10.0, 120.0)
	var base_y = profile["base_yield"]
	var final_yield = int(floor(base_y * (0.50 + 0.50 * (fertility / 100.0)) * (1.0 + 0.05 * farmer_skill)))
	
	return {
		"yield": max(1, final_yield),
		"fertility_post": fertility,
		"blight": false,
		"nitrogen": soil.nitrogen,
		"phosphorus": soil.phosphorus,
		"potassium": soil.potassium
	}

# --- Canonical 4-Year Crop Rotation Engine ---

## Canonical 4-year crop rotation (Wheat -> Barley -> Legumes -> Fallow)
## Restores nitrogen and prevents monoculture penalties.
func advance_rotation_year(cycle_index: int) -> void:
	current_rotation_year = cycle_index % 4
	
	for pos in soil_registry.keys():
		var soil: FarmlandSoilData = soil_registry[pos]
		soil.rotation_cycle = current_rotation_year
		# Reset monoculture penalties at start of each rotation cycle
		soil.consecutive_crop_id = ""
		soil.consecutive_plantings = 0
		
		# In Fallow Year (Year 4 / cycle 3), apply livestock grazing regeneration (7 days equivalent)
		if current_rotation_year == 3:
			apply_fallow_regeneration(pos, true)
			# Additional fallow weathering
			apply_fallow_regeneration(pos, true)
			apply_fallow_regeneration(pos, false)
			
	emit_signal("rotation_year_advanced", current_rotation_year)

## Returns the recommended crop for a plot given its rotation phase
func get_rotation_crop_for_year(year: int) -> String:
	match year % 4:
		0: return "wheat"
		1: return "barley"
		2: return "peas" # Legumes (Rhizobia N-fixer)
		3: return "fallow"
		_: return "wheat"

# --- Soil Amendments & Organic Fertilization ---

func apply_fallow_regeneration(pos: Variant, has_livestock_grazing: bool = false) -> void:
	var vpos = _normalize_pos(pos)
	var soil = get_soil_data(vpos)
	var max_cap = 120.0 if soil.has_terra_preta else 100.0
	
	if has_livestock_grazing:
		# Natural manure/urine deposit
		soil.nitrogen = minf(max_cap, soil.nitrogen + 4.0)
		soil.phosphorus = minf(max_cap, soil.phosphorus + 2.0)
		soil.potassium = minf(max_cap, soil.potassium + 2.5)
	else:
		# Natural mineral weathering
		soil.nitrogen = minf(max_cap, soil.nitrogen + 1.5)
		soil.phosphorus = minf(max_cap, soil.phosphorus + 1.0)
		soil.potassium = minf(max_cap, soil.potassium + 1.0)

	soil.consecutive_crop_id = ""
	soil.consecutive_plantings = 0

func apply_amendment(pos: Variant, amendment_type: String) -> void:
	var vpos = _normalize_pos(pos)
	var soil = get_soil_data(vpos)
	var max_cap = 120.0 if soil.has_terra_preta else 100.0
	
	match amendment_type:
		"compost_barrel", "manure":
			soil.nitrogen = minf(max_cap, soil.nitrogen + 25.0)
			soil.phosphorus = minf(max_cap, soil.phosphorus + 20.0)
			soil.potassium = minf(max_cap, soil.potassium + 15.0)
		"wood_ash_lime", "wood_ash":
			# Unlocks Terra Preta state and boosts potash/phosphorus
			soil.has_terra_preta = true
			soil.potassium = minf(120.0, soil.potassium + 20.0)
			soil.phosphorus = minf(120.0, soil.phosphorus + 10.0)
