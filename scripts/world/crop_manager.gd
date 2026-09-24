class_name CropManager
extends RefCounted

## Farmer's Delight Multi-Crop & Crop Rotation Management Engine.
## Handles crop families, soil fertility enhancement via Rich Compost,
## and realistic crop rotation yield bonuses vs. monoculture soil exhaustion.

enum CropType {
	WHEAT = 0,    # Gramineae (Grains)
	CABBAGE = 1,  # Brassicaceae (Leafy greens)
	ONION = 2,    # Amaryllidaceae (Alliums)
	CARROT = 3    # Apiaceae (Root vegetables)
}

# Key: Vector3i farmland position, Value: Array[int] of previous crop types
var plot_history: Dictionary = {}

# Key: Vector3i farmland position, Value: bool (is enriched with compost)
var rich_soil_plots: Dictionary = {}

func fertilize_plot(plot_pos: Vector3i) -> void:
	rich_soil_plots[plot_pos] = true

func is_plot_rich(plot_pos: Vector3i) -> bool:
	return rich_soil_plots.get(plot_pos, false)

func record_crop_harvest(plot_pos: Vector3i, crop: CropType) -> void:
	if not plot_history.has(plot_pos):
		plot_history[plot_pos] = []
	var history: Array = plot_history[plot_pos]
	history.append(crop)
	# Keep only last 5 crops
	if history.size() > 5:
		history.pop_front()

func get_growth_rate_multiplier(plot_pos: Vector3i, crop: CropType) -> float:
	var mult: float = 1.0
	
	# Rich Compost soil provides 2x growth speed
	if is_plot_rich(plot_pos):
		mult *= 2.0
		
	# Crop rotation check
	var history: Array = plot_history.get(plot_pos, [])
	if history.size() >= 1:
		var last_crop = history[-1]
		if last_crop != crop:
			# Positive crop rotation restores soil nutrients
			mult += 0.25
		elif history.size() >= 2 and history[-2] == crop:
			# Monoculture exhaustion penalty
			mult = maxf(0.5, mult - 0.20)
			
	return mult

func get_harvest_yield(plot_pos: Vector3i, crop: CropType) -> int:
	var base_yield: int = 2
	
	if is_plot_rich(plot_pos):
		base_yield += 1
		
	var history: Array = plot_history.get(plot_pos, [])
	if history.size() >= 1 and history[-1] != crop:
		# Crop rotation bonus yield
		base_yield += 1
	elif history.size() >= 2 and history[-1] == crop and history[-2] == crop:
		# Monoculture depletion penalty
		base_yield = maxi(1, base_yield - 1)
		
	return base_yield
