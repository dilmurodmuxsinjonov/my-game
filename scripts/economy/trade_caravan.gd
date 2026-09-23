class_name TradeCaravan
extends StaticBody3D

## Feudal Merchant Trade Caravan.
## Arrives periodically with draft cart and offers exotic goods (spices, salt, fabric, steel)
## in exchange for realm commodities and coins.

signal traded(item_bought: String, cost: int)
signal departed()

var model_instance: Node3D
var collision_box: CollisionShape3D
var prompt_label: Label3D

var stay_duration: float = 90.0 # Stays for 1.5 minutes
var stay_timer: float = 0.0

# Caravan wares and prices (in coins)
var wares: Dictionary = {
	"spices": {"price": 12, "stock": 5, "icon": "🌶️"},
	"cured_salt": {"price": 6, "stock": 10, "icon": "🧂"},
	"fine_fabric": {"price": 15, "stock": 6, "icon": "🧵"},
	"steel_ingot": {"price": 20, "stock": 4, "icon": "⚔️"},
	"rare_seeds": {"price": 8, "stock": 8, "icon": "🌾"}
}

# Purchase prices for kingdom surplus (what caravan pays the player)
var purchase_rates: Dictionary = {
	"bread": 2,
	"wheat": 1,
	"logs": 1,
	"stone": 1,
	"iron_ore": 3,
	"copper_ore": 2
}

func _ready() -> void:
	_setup_visuals()

func _setup_visuals() -> void:
	collision_box = CollisionShape3D.new()
	var box = BoxShape3D.new()
	box.size = Vector3(1.8, 1.8, 2.6)
	collision_box.shape = box
	collision_box.position = Vector3(0, 0.9, 0)
	add_child(collision_box)
	
	# Load Blender caravan_cart.glb
	var glb_path = "res://assets/models/caravan_cart.glb"
	if ResourceLoader.exists(glb_path):
		var scene_res = load(glb_path)
		if scene_res:
			model_instance = scene_res.instantiate()
			add_child(model_instance)
			
	# Prompt billboard
	prompt_label = Label3D.new()
	prompt_label.text = "🐪 Merchant Trade Caravan\n[E] Trade Exotic Goods"
	prompt_label.position = Vector3(0, 2.3, 0)
	prompt_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	prompt_label.font_size = 28
	prompt_label.modulate = Color(1.0, 0.85, 0.4)
	add_child(prompt_label)

func _process(delta: float) -> void:
	stay_timer += delta
	if stay_timer >= stay_duration:
		depart()

func buy_item(item_key: String, supply_chain: SupplyChain) -> bool:
	if not wares.has(item_key) or not supply_chain:
		return false
		
	var ware = wares[item_key]
	if ware["stock"] <= 0:
		return false
		
	var price = ware["price"]
	# Check if player / supply chain has enough coins
	var current_coins = supply_chain.inventory.get("coins", 0)
	if current_coins < price:
		return false
		
	supply_chain.consume_resource("coins", price)
	supply_chain.add_resource(item_key, 1)
	ware["stock"] -= 1
	emit_signal("traded", item_key, price)
	return true

func sell_resource(item_key: String, amount: int, supply_chain: SupplyChain) -> bool:
	if not purchase_rates.has(item_key) or not supply_chain:
		return false
		
	var rate = purchase_rates[item_key]
	if supply_chain.consume_resource(item_key, amount):
		var earned_coins = rate * amount
		supply_chain.add_resource("coins", earned_coins)
		return true
	return false

func depart() -> void:
	emit_signal("departed")
	queue_free()
