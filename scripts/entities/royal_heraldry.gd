# scripts/entities/royal_heraldry.gd
# Voxel Lord: Feudal Realm - Milestone 46: Royal Heraldry & Castle Customization
# Manages royal coat of arms, heraldic charges, tinctures, blazons, and kingdom banner styling.

class_name RoyalHeraldry
extends Node

signal heraldry_changed(blazon: String, primary_color: Color, secondary_color: Color)

enum EmblemType {
	LION_RAMPANT,
	IMPERIAL_EAGLE,
	FIERY_DRAGON,
	ROYAL_STAG,
	MONARCH_CROWN,
	FLEUR_DE_LIS,
	CROSSED_SWORDS,
	GOLDEN_WHEAT
}

enum Tincture {
	GULES,    # Crimson Red
	AZURE,    # Royal Cobalt Blue
	OR,       # Radiant Gold
	ARGENT,   # Pure Silver White
	SABLE,    # Raven Black
	VERT,     # Forest Emerald Green
	PURPURE   # Imperial Tyrian Purple
}

enum DivisionType {
	SOLID,
	PER_PALE,    # Vertical split
	PER_FESS,    # Horizontal split
	QUARTERLY,   # Four quarters
	CHEVRON      # Inverted V
}

const TINCTURE_COLORS: Dictionary = {
	Tincture.GULES: Color(0.78, 0.14, 0.14, 1.0),
	Tincture.AZURE: Color(0.12, 0.32, 0.65, 1.0),
	Tincture.OR: Color(0.92, 0.75, 0.18, 1.0),
	Tincture.ARGENT: Color(0.92, 0.94, 0.95, 1.0),
	Tincture.SABLE: Color(0.12, 0.12, 0.14, 1.0),
	Tincture.VERT: Color(0.15, 0.58, 0.22, 1.0),
	Tincture.PURPURE: Color(0.48, 0.12, 0.60, 1.0)
}

const TINCTURE_NAMES: Dictionary = {
	Tincture.GULES: "Gules (Crimson)",
	Tincture.AZURE: "Azure (Royal Blue)",
	Tincture.OR: "Or (Gold)",
	Tincture.ARGENT: "Argent (Silver)",
	Tincture.SABLE: "Sable (Black)",
	Tincture.VERT: "Vert (Forest Green)",
	Tincture.PURPURE: "Purpure (Purple)"
}

const EMBLEM_NAMES: Dictionary = {
	EmblemType.LION_RAMPANT: "Lion Rampant",
	EmblemType.IMPERIAL_EAGLE: "Imperial Eagle",
	EmblemType.FIERY_DRAGON: "Fiery Dragon",
	EmblemType.ROYAL_STAG: "Royal Stag",
	EmblemType.MONARCH_CROWN: "Monarch Crown",
	EmblemType.FLEUR_DE_LIS: "Fleur-de-lis",
	EmblemType.CROSSED_SWORDS: "Crossed Broadswords",
	EmblemType.GOLDEN_WHEAT: "Golden Wheat Sheaf"
}

const DIVISION_NAMES: Dictionary = {
	DivisionType.SOLID: "Solid Field",
	DivisionType.PER_PALE: "Per Pale (Vertical Split)",
	DivisionType.PER_FESS: "Per Fess (Horizontal Split)",
	DivisionType.QUARTERLY: "Quarterly (Four Quarters)",
	DivisionType.CHEVRON: "Chevron (Inverted V)"
}

@export var kingdom_name: String = "Valoria"
@export var motto: String = "In Fide et Virtute"
@export var emblem: EmblemType = EmblemType.LION_RAMPANT
@export var primary_tincture: Tincture = Tincture.OR
@export var secondary_tincture: Tincture = Tincture.AZURE
@export var division: DivisionType = DivisionType.QUARTERLY
@export var banner_style: String = "swallowtail"

func _init(
	p_name: String = "Valoria",
	p_motto: String = "In Fide et Virtute",
	p_emblem: EmblemType = EmblemType.LION_RAMPANT,
	p_pri: Tincture = Tincture.OR,
	p_sec: Tincture = Tincture.AZURE,
	p_div: DivisionType = DivisionType.QUARTERLY
) -> void:
	kingdom_name = p_name
	motto = p_motto
	emblem = p_emblem
	primary_tincture = p_pri
	secondary_tincture = p_sec
	division = p_div

func configure(
	p_name: String,
	p_motto: String,
	p_emblem: EmblemType,
	p_pri: Tincture,
	p_sec: Tincture,
	p_div: DivisionType,
	p_style: String = "swallowtail"
) -> void:
	kingdom_name = p_name
	motto = p_motto
	emblem = p_emblem
	primary_tincture = p_pri
	secondary_tincture = p_sec
	division = p_div
	banner_style = p_style
	heraldry_changed.emit(get_blazon(), get_primary_color(), get_secondary_color())

func get_tincture_color(t: Tincture) -> Color:
	return TINCTURE_COLORS.get(t, Color.WHITE)

func get_primary_color() -> Color:
	return get_tincture_color(primary_tincture)

func get_secondary_color() -> Color:
	return get_tincture_color(secondary_tincture)

func get_tincture_name(t: Tincture) -> String:
	return TINCTURE_NAMES.get(t, "Unknown Tincture")

func get_emblem_name(e: EmblemType = emblem) -> String:
	return EMBLEM_NAMES.get(e, "Unknown Emblem")

func get_division_name(d: DivisionType = division) -> String:
	return DIVISION_NAMES.get(d, "Solid")

func get_blazon() -> String:
	var div_str = ""
	match division:
		DivisionType.SOLID:
			div_str = get_tincture_name(primary_tincture)
		DivisionType.PER_PALE:
			div_str = "Per pale " + get_tincture_name(primary_tincture) + " and " + get_tincture_name(secondary_tincture)
		DivisionType.PER_FESS:
			div_str = "Per fess " + get_tincture_name(primary_tincture) + " and " + get_tincture_name(secondary_tincture)
		DivisionType.QUARTERLY:
			div_str = "Quarterly " + get_tincture_name(primary_tincture) + " and " + get_tincture_name(secondary_tincture)
		DivisionType.CHEVRON:
			div_str = get_tincture_name(primary_tincture) + " a chevron " + get_tincture_name(secondary_tincture)
	
	var embl_str = "a " + get_emblem_name(emblem) + " " + get_tincture_name(primary_tincture)
	return "Field of " + div_str + ", charged with " + embl_str + ". Royal Motto: '" + motto + "'."

func create_banner_material() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = get_primary_color()
	mat.roughness = 0.85
	mat.metallic = 0.05
	return mat

func apply_to_citizen(citizen: Node) -> void:
	if not citizen:
		return
	if citizen.has_method("set_uniform_color"):
		citizen.call("set_uniform_color", get_primary_color(), get_secondary_color())
	elif citizen.has_node("MeshInstance3D"):
		var mesh_inst = citizen.get_node("MeshInstance3D") as MeshInstance3D
		if mesh_inst and mesh_inst.material_override is StandardMaterial3D:
			mesh_inst.material_override.albedo_color = get_primary_color()

func cycle_emblem(forward: bool = true) -> EmblemType:
	var count = EmblemType.size()
	var current = int(emblem)
	if forward:
		current = (current + 1) % count
	else:
		current = (current - 1 + count) % count
	emblem = current as EmblemType
	heraldry_changed.emit(get_blazon(), get_primary_color(), get_secondary_color())
	return emblem

func cycle_primary_tincture(forward: bool = true) -> Tincture:
	var count = Tincture.size()
	var current = int(primary_tincture)
	if forward:
		current = (current + 1) % count
	else:
		current = (current - 1 + count) % count
	primary_tincture = current as Tincture
	heraldry_changed.emit(get_blazon(), get_primary_color(), get_secondary_color())
	return primary_tincture

func cycle_secondary_tincture(forward: bool = true) -> Tincture:
	var count = Tincture.size()
	var current = int(secondary_tincture)
	if forward:
		current = (current + 1) % count
	else:
		current = (current - 1 + count) % count
	secondary_tincture = current as Tincture
	heraldry_changed.emit(get_blazon(), get_primary_color(), get_secondary_color())
	return secondary_tincture

func cycle_division(forward: bool = true) -> DivisionType:
	var count = DivisionType.size()
	var current = int(division)
	if forward:
		current = (current + 1) % count
	else:
		current = (current - 1 + count) % count
	division = current as DivisionType
	heraldry_changed.emit(get_blazon(), get_primary_color(), get_secondary_color())
	return division

func to_dict() -> Dictionary:
	return {
		"kingdom_name": kingdom_name,
		"motto": motto,
		"emblem": int(emblem),
		"primary_tincture": int(primary_tincture),
		"secondary_tincture": int(secondary_tincture),
		"division": int(division),
		"banner_style": banner_style
	}

func from_dict(d: Dictionary) -> void:
	if d.has("kingdom_name"):
		kingdom_name = d["kingdom_name"]
	if d.has("motto"):
		motto = d["motto"]
	if d.has("emblem"):
		emblem = d["emblem"] as EmblemType
	if d.has("primary_tincture"):
		primary_tincture = d["primary_tincture"] as Tincture
	if d.has("secondary_tincture"):
		secondary_tincture = d["secondary_tincture"] as Tincture
	if d.has("division"):
		division = d["division"] as DivisionType
	if d.has("banner_style"):
		banner_style = d["banner_style"]
	heraldry_changed.emit(get_blazon(), get_primary_color(), get_secondary_color())
