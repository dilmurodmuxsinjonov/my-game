# tests/test_feudal_resource_economy.py
# Voxel Lord: Feudal Realm - Automated Test Suite for Feudal Resources, Supply Chains & Economy
# Tests Raw Resource Ingestion, Production Pipelines, Preservation Kinetics, Market Elasticity, and Macro Stress.

import unittest
import math
import random
import copy


class FeudalSupplyChainMock:
    """Accurate Python reference oracle matching scripts/economy/supply_chain.gd."""

    class QuotaMode:
        DO_FOREVER = 0
        DO_UNTIL_X = 1
        PAUSED = 2

    def __init__(self):
        self.inventory = {
            "wheat": 20, "bread": 50, "meat": 15, "cabbage": 10, "onion": 8, "carrot": 8,
            "sliced_cabbage": 0, "minced_beef": 0, "diced_onion": 0, "cabbage_stew": 0, "shepherd_pie": 0,
            "rock_salt": 10, "cured_meat": 0, "smoked_meat": 0, "logs": 30, "planks": 15, "stone": 25,
            "coal": 12, "iron_ore": 6, "copper_ore": 4, "crushed_iron": 0, "crushed_copper": 0,
            "iron_ingots": 2, "copper_ingot": 0, "steel_ingot": 4, "tools": 10, "weapons": 5,
            "tin_ore": 2, "tin_ingot": 0, "bronze_ingot": 0, "ceramic_mold": 2, "cast_bronze_blade": 0,
            "gold_coins": 50, "raw_wool": 8, "woolen_tunic": 0, "honeycomb": 6, "beeswax": 4,
            "honey_mead": 0, "beeswax_candle": 0, "iron_bloom": 0, "wrought_iron_ingot": 0
        }
        self.quotas = {"bread": 50, "tools": 10, "weapons": 5, "iron_ingots": 20}
        self.quota_modes = {
            "bread": self.QuotaMode.DO_UNTIL_X,
            "tools": self.QuotaMode.DO_UNTIL_X,
            "weapons": self.QuotaMode.DO_UNTIL_X,
            "iron_ingots": self.QuotaMode.DO_FOREVER
        }
        self.morale = 75.0
        self.tax_rate = 0.10

    def add_resource(self, item: str, amount: int) -> None:
        if amount <= 0:
            return
        self.inventory[item] = self.inventory.get(item, 0) + amount

    def consume_resource(self, item: str, amount: int) -> bool:
        if amount < 0:
            return False
        if amount == 0:
            return True
        if self.inventory.get(item, 0) >= amount:
            self.inventory[item] -= amount
            return True
        return False

    def get_resource(self, item: str) -> int:
        return self.inventory.get(item, 0)

    def has_resource(self, item: str, amount: int = 1) -> bool:
        if amount <= 0:
            return True
        return self.get_resource(item) >= amount

    def get_stockpile_snapshot(self) -> dict:
        return copy.deepcopy(self.inventory)

    def restore_stockpile_snapshot(self, snapshot: dict) -> None:
        if not snapshot:
            return
        for item, qty in snapshot.items():
            self.inventory[item] = int(qty)

    def set_quota(self, item: str, target_amount: int, mode: int = QuotaMode.DO_UNTIL_X) -> None:
        self.quotas[item] = max(0, target_amount)
        self.quota_modes[item] = mode

    def get_quota(self, item: str) -> int:
        return self.quotas.get(item, 999999)

    def get_quota_mode(self, item: str) -> int:
        return self.quota_modes.get(item, self.QuotaMode.DO_FOREVER)

    def is_quota_reached(self, item: str) -> bool:
        mode = self.get_quota_mode(item)
        if mode == self.QuotaMode.PAUSED:
            return True
        if mode == self.QuotaMode.DO_FOREVER:
            return False
        return self.get_resource(item) >= self.get_quota(item)

    def can_produce(self, item: str) -> bool:
        return not self.is_quota_reached(item)

    # Multi-Stage Production Functions
    def salt_meat(self, amount: int) -> bool:
        if self.consume_resource("meat", amount) and self.consume_resource("rock_salt", amount):
            self.add_resource("cured_meat", amount)
            return True
        return False

    def smoke_meat(self, amount: int) -> bool:
        wood_needed = max(1, math.ceil(amount / 2.0))
        if self.consume_resource("meat", amount) and self.consume_resource("logs", wood_needed):
            self.add_resource("smoked_meat", amount)
            return True
        return False

    def cook_cabbage_stew(self, amount: int = 1) -> bool:
        if (self.inventory.get("sliced_cabbage", 0) >= amount and
                self.inventory.get("minced_beef", 0) >= amount and
                self.inventory.get("diced_onion", 0) >= amount):
            self.consume_resource("sliced_cabbage", amount)
            self.consume_resource("minced_beef", amount)
            self.consume_resource("diced_onion", amount)
            self.add_resource("cabbage_stew", amount * 2)
            return True
        return False

    def cook_shepherd_pie(self, amount: int = 1) -> bool:
        if (self.inventory.get("minced_beef", 0) >= amount and
                self.inventory.get("diced_onion", 0) >= amount and
                self.inventory.get("bread", 0) >= amount):
            self.consume_resource("minced_beef", amount)
            self.consume_resource("diced_onion", amount)
            self.consume_resource("bread", amount)
            self.add_resource("shepherd_pie", amount * 2)
            return True
        return False

    def smelt_iron_bloom(self, batches: int = 1) -> bool:
        ore_needed = batches * 2
        fuel_needed = batches * 2
        if self.inventory.get("iron_ore", 0) >= ore_needed and self.inventory.get("coal", 0) >= fuel_needed:
            self.consume_resource("iron_ore", ore_needed)
            self.consume_resource("coal", fuel_needed)
            self.add_resource("iron_bloom", batches)
            return True
        return False

    def refine_bloom_on_anvil(self, batches: int = 1) -> bool:
        if self.inventory.get("iron_bloom", 0) >= batches:
            self.consume_resource("iron_bloom", batches)
            self.add_resource("wrought_iron_ingot", batches)
            return True
        return False

    def smelt_steel(self, batches: int = 1) -> bool:
        if self.inventory.get("wrought_iron_ingot", 0) >= batches and self.inventory.get("coal", 0) >= (batches * 2):
            self.consume_resource("wrought_iron_ingot", batches)
            self.consume_resource("coal", batches * 2)
            self.add_resource("steel_ingot", batches)
            return True
        return False

    def cast_bronze_tool(self, mold_type: str) -> bool:
        if self.inventory.get("copper_ingot", 0) >= 7 and self.inventory.get("tin_ingot", 0) >= 1 and self.inventory.get("ceramic_mold", 0) >= 1:
            self.consume_resource("copper_ingot", 7)
            self.consume_resource("tin_ingot", 1)
            if mold_type == "sword_blade":
                self.add_resource("cast_bronze_blade", 1)
            elif mold_type == "pickaxe_head":
                self.add_resource("cast_bronze_pickaxe", 1)
            else:
                self.add_resource("bronze_ingot", 8)
            return True
        return False

    def ferment_honey_mead(self, amount: int = 1) -> bool:
        if self.inventory.get("honeycomb", 0) >= (amount * 2):
            self.consume_resource("honeycomb", amount * 2)
            self.add_resource("honey_mead", amount)
            return True
        return False

    def craft_beeswax_candle(self, amount: int = 1) -> bool:
        if self.inventory.get("beeswax", 0) >= amount:
            self.consume_resource("beeswax", amount)
            self.add_resource("beeswax_candle", amount * 2)
            return True
        return False

    def weave_woolen_tunic(self, amount: int = 1) -> bool:
        if self.inventory.get("raw_wool", 0) >= (amount * 4):
            self.consume_resource("raw_wool", amount * 4)
            self.add_resource("woolen_tunic", amount)
            return True
        return False

    def process_production_cycle(self, assigned_citizens: dict) -> dict:
        report = {
            "produced": {},
            "consumed": {},
            "unfed_citizens": 0,
            "paused_by_quota": []
        }

        # 1. Farmers produce wheat
        farmers = assigned_citizens.get("farmer", 0)
        wheat_produced = farmers * 4
        self.add_resource("wheat", wheat_produced)
        report["produced"]["wheat"] = wheat_produced

        # 2. Bakers turn wheat into bread respecting quota
        bakers = assigned_citizens.get("baker", 0)
        if self.can_produce("bread"):
            wheat_needed = bakers * 2
            if self.get_quota_mode("bread") == self.QuotaMode.DO_UNTIL_X:
                needed_bread = max(0, self.get_quota("bread") - self.get_resource("bread"))
                max_wheat = math.ceil(needed_bread / 2.0)
                wheat_needed = min(wheat_needed, max_wheat)

            wheat_used = min(self.inventory.get("wheat", 0), wheat_needed)
            if wheat_used > 0:
                self.consume_resource("wheat", wheat_used)
                bread_produced = wheat_used * 2
                self.add_resource("bread", bread_produced)
                report["produced"]["bread"] = bread_produced
                report["consumed"]["wheat"] = wheat_used
        else:
            report["paused_by_quota"].append("bread")

        # 3. Lumberjacks produce logs
        lumberjacks = assigned_citizens.get("lumberjack", 0)
        logs_produced = lumberjacks * 3
        self.add_resource("logs", logs_produced)
        report["produced"]["logs"] = logs_produced

        # 4. Miners produce stone, coal, iron_ore
        miners = assigned_citizens.get("miner", 0)
        stone_produced = miners * 3
        iron_produced = miners * 1
        coal_produced = miners * 2
        self.add_resource("stone", stone_produced)
        self.add_resource("iron_ore", iron_produced)
        self.add_resource("coal", coal_produced)
        report["produced"]["stone"] = stone_produced
        report["produced"]["iron_ore"] = iron_produced
        report["produced"]["coal"] = coal_produced

        # 5. Blacksmiths make tools
        blacksmiths = assigned_citizens.get("blacksmith", 0)
        for _ in range(blacksmiths):
            if self.can_produce("tools"):
                if self.consume_resource("iron_ore", 2) and self.consume_resource("logs", 1):
                    self.add_resource("tools", 1)
                    report["produced"]["tools"] = report["produced"].get("tools", 0) + 1
            else:
                if "tools" not in report["paused_by_quota"]:
                    report["paused_by_quota"].append("tools")

        # 6. Citizen food consumption
        total_citizens = sum(assigned_citizens.values())
        bread_available = self.inventory.get("bread", 0)
        fed_citizens = min(bread_available, total_citizens)
        self.consume_resource("bread", fed_citizens)
        report["consumed"]["bread"] = fed_citizens

        unfed = total_citizens - fed_citizens
        report["unfed_citizens"] = unfed

        self._update_morale(unfed, total_citizens)
        return report

    def _update_morale(self, unfed: int, total: int) -> None:
        if total == 0:
            self.morale = 100.0
            return
        food_ratio = (total - unfed) / total
        target_morale = (food_ratio * 90.0) + (10.0 - (self.tax_rate * 20.0))
        self.morale = self.morale + 0.2 * (target_morale - self.morale)
        self.morale = max(0.0, min(100.0, self.morale))

    # Persistence
    def to_dict(self) -> dict:
        return {
            "stockpile": self.get_stockpile_snapshot(),
            "quotas": dict(self.quotas),
            "quota_modes": dict(self.quota_modes),
            "morale": self.morale,
            "tax_rate": self.tax_rate
        }

    def from_dict(self, data: dict) -> None:
        if not data:
            return
        if "stockpile" in data:
            self.restore_stockpile_snapshot(data["stockpile"])
        elif "inventory" in data:
            self.restore_stockpile_snapshot(data["inventory"])
        if "quotas" in data:
            self.quotas.update({k: int(v) for k, v in data["quotas"].items()})
        if "quota_modes" in data:
            self.quota_modes.update({k: int(v) for k, v in data["quota_modes"].items()})
        self.morale = data.get("morale", 75.0)
        self.tax_rate = data.get("tax_rate", 0.10)


class FoodPreservationKineticsOracle:
    """Calculates Arrhenius thermal decay rates, humidity acceleration, and container shelf life."""

    Q10: float = 2.0
    T_REF: float = 15.0 # Celsius reference

    CONTAINER_FACTORS = {
        "OPEN_GROUND": 1.50,
        "WOODEN_CHEST": 1.00,
        "CLAY_AMPHORA": 0.60,
        "STILT_GRANARY": 0.25,
        "COLD_CELLAR": 0.25,
        "ICEHOUSE_VAULT": 0.10
    }

    PRESERVATION_FACTORS = {
        "NONE": 1.00,
        "PICKLED": 0.14,
        "SMOKED": 0.10,
        "SALTED": 0.07,
        "DEHYDRATED": 0.08
    }

    BASE_SHELF_LIFE_HOURS = {
        "fresh_meat": 72.0,
        "bread": 144.0,
        "cabbage": 168.0,
        "carrot": 240.0,
        "berries": 72.0,
        "smoked_meat": 360.0,
        "cured_meat": 576.0,
        "pickled_veg": 720.0
    }

    @classmethod
    def calculate_decay_rate(cls, temp_celsius: float, rel_humidity: float, container: str, mode: str) -> float:
        # Arrhenius factor
        k_temp = cls.Q10 ** ((temp_celsius - cls.T_REF) / 10.0)
        # Humidity factor (exponential moisture acceleration)
        k_humid = 1.0 + max(0.0, (rel_humidity - 50.0) / 50.0) * 0.8
        # Container multiplier
        k_cont = cls.CONTAINER_FACTORS.get(container, 1.0)
        # Preservation multiplier
        k_pres = cls.PRESERVATION_FACTORS.get(mode, 1.0)

        return k_temp * k_humid * k_cont * k_pres


class MarketPricingElasticityOracle:
    """Calculates universal algorithmic pricing with singularity guard and late winter Hungry Gap."""

    K_D: float = 0.85
    GAMMA: float = 1.25
    CLAMP_MIN: float = 0.20
    CLAMP_MAX: float = 5.00
    INNER_MIN: float = 0.01

    @classmethod
    def calculate_price(cls, base_price: float, supply: float, demand: float, is_hungry_gap: bool = False) -> float:
        ratio = demand / max(cls.INNER_MIN, supply)
        multiplier = 1.0 + cls.K_D * (math.pow(ratio, cls.GAMMA) - 1.0)
        multiplier = max(cls.CLAMP_MIN, min(cls.CLAMP_MAX, multiplier))

        if is_hungry_gap:
            multiplier = min(cls.CLAMP_MAX, multiplier * 2.0)

        return base_price * multiplier


# ==============================================================================
# UNIT TEST SUITES
# ==============================================================================

class TestRawResourceIngestionAndGuards(unittest.TestCase):
    """Tier 1: Core Resource Inventory, Bounds Checking & Non-Negativity."""

    def setUp(self):
        self.sc = FeudalSupplyChainMock()

    def test_initial_stockpile_presence(self):
        """Verify baseline initial supplies are loaded correctly."""
        self.assertEqual(self.sc.get_resource("wheat"), 20)
        self.assertEqual(self.sc.get_resource("bread"), 50)
        self.assertEqual(self.sc.get_resource("logs"), 30)
        self.assertEqual(self.sc.get_resource("iron_ore"), 6)
        self.assertEqual(self.sc.get_resource("gold_coins"), 50)

    def test_add_resource_positive(self):
        """Positive amounts increment inventory as expected."""
        self.sc.add_resource("stone", 15)
        self.assertEqual(self.sc.get_resource("stone"), 40)

    def test_add_resource_negative_guard(self):
        """Adding zero or negative amounts is strictly rejected with no change."""
        self.sc.add_resource("stone", -20)
        self.assertEqual(self.sc.get_resource("stone"), 25)
        self.sc.add_resource("stone", 0)
        self.assertEqual(self.sc.get_resource("stone"), 25)

    def test_consume_resource_sufficient(self):
        """Consuming <= current stockpile succeeds and decrements count."""
        success = self.sc.consume_resource("logs", 10)
        self.assertTrue(success)
        self.assertEqual(self.sc.get_resource("logs"), 20)

    def test_consume_resource_insufficient(self):
        """Consuming > stockpile fails and leaves stockpile untouched."""
        success = self.sc.consume_resource("iron_ore", 99)
        self.assertFalse(success)
        self.assertEqual(self.sc.get_resource("iron_ore"), 6)

    def test_consume_resource_negative_exploit_guard(self):
        """Consuming negative numbers returns False and cannot create free items."""
        success = self.sc.consume_resource("gold_coins", -50)
        self.assertFalse(success)
        self.assertEqual(self.sc.get_resource("gold_coins"), 50)

    def test_has_resource_query(self):
        """has_resource accurately reflects availability."""
        self.assertTrue(self.sc.has_resource("bread", 25))
        self.assertTrue(self.sc.has_resource("bread", 50))
        self.assertFalse(self.sc.has_resource("bread", 51))
        self.assertTrue(self.sc.has_resource("bread", 0))

    def test_stockpile_snapshot_isolation(self):
        """Mutating snapshot dict must not alter the internal supply chain state."""
        snap = self.sc.get_stockpile_snapshot()
        snap["gold_coins"] = 999999
        self.assertEqual(self.sc.get_resource("gold_coins"), 50)


class TestMultiStageProductionPipelines(unittest.TestCase):
    """Tier 2: Multi-Tier Production Chains & Crafting Conversions."""

    def setUp(self):
        self.sc = FeudalSupplyChainMock()

    def test_bloomery_to_wrought_iron_and_steel(self):
        """Verify ore+coal -> iron bloom -> wrought iron -> steel ingot chain."""
        # 1. Smelt bloom (needs 2 ore, 2 coal)
        self.sc.inventory["iron_ore"] = 4
        self.sc.inventory["coal"] = 8
        self.assertTrue(self.sc.smelt_iron_bloom(2))
        self.assertEqual(self.sc.get_resource("iron_bloom"), 2)
        self.assertEqual(self.sc.get_resource("iron_ore"), 0)
        self.assertEqual(self.sc.get_resource("coal"), 4)

        # 2. Refine on anvil -> wrought iron
        self.assertTrue(self.sc.refine_bloom_on_anvil(2))
        self.assertEqual(self.sc.get_resource("iron_bloom"), 0)
        self.assertEqual(self.sc.get_resource("wrought_iron_ingot"), 2)

        # 3. Smelt steel (needs 2 coal per wrought iron)
        self.assertTrue(self.sc.smelt_steel(2))
        self.assertEqual(self.sc.get_resource("wrought_iron_ingot"), 0)
        self.assertEqual(self.sc.get_resource("steel_ingot"), 6) # 4 original + 2 new
        self.assertEqual(self.sc.get_resource("coal"), 0)

    def test_bronze_casting_with_ceramic_mold(self):
        """Verify 7 Cu + 1 Sn + 1 Mold -> Cast Bronze Blade."""
        self.sc.inventory["copper_ingot"] = 14
        self.sc.inventory["tin_ingot"] = 2
        self.sc.inventory["ceramic_mold"] = 2

        self.assertTrue(self.sc.cast_bronze_tool("sword_blade"))
        self.assertEqual(self.sc.get_resource("cast_bronze_blade"), 1)
        self.assertEqual(self.sc.get_resource("copper_ingot"), 7)
        self.assertEqual(self.sc.get_resource("tin_ingot"), 1)

    def test_culinary_cabbage_stew_and_shepherd_pie(self):
        """Verify multi-ingredient food recipes double output volume."""
        self.sc.inventory["sliced_cabbage"] = 3
        self.sc.inventory["minced_beef"] = 5
        self.sc.inventory["diced_onion"] = 5

        # Cook 2 batches cabbage stew
        self.assertTrue(self.sc.cook_cabbage_stew(2))
        self.assertEqual(self.sc.get_resource("cabbage_stew"), 4) # 2 * 2
        self.assertEqual(self.sc.get_resource("sliced_cabbage"), 1)

        # Cook 2 batches shepherd pie
        self.assertTrue(self.sc.cook_shepherd_pie(2))
        self.assertEqual(self.sc.get_resource("shepherd_pie"), 4)

    def test_salting_and_smoking_meat_preservation(self):
        """Meat salting with halite salt and smoking with hardwood logs."""
        self.sc.inventory["meat"] = 10
        self.sc.inventory["rock_salt"] = 10
        self.sc.inventory["logs"] = 10

        self.assertTrue(self.sc.salt_meat(4))
        self.assertEqual(self.sc.get_resource("cured_meat"), 4)
        self.assertEqual(self.sc.get_resource("meat"), 6)
        self.assertEqual(self.sc.get_resource("rock_salt"), 6)

        self.assertTrue(self.sc.smoke_meat(4))
        self.assertEqual(self.sc.get_resource("smoked_meat"), 4)
        self.assertEqual(self.sc.get_resource("meat"), 2)

    def test_textile_and_apiary_fermentation(self):
        """Raw wool weaving and honey mead fermentation."""
        self.assertTrue(self.sc.weave_woolen_tunic(2)) # 2 tunics * 4 wool = 8 wool
        self.assertEqual(self.sc.get_resource("woolen_tunic"), 2)
        self.assertEqual(self.sc.get_resource("raw_wool"), 0)

        self.assertTrue(self.sc.ferment_honey_mead(2)) # 2 mead * 2 comb = 4 comb
        self.assertEqual(self.sc.get_resource("honey_mead"), 2)
        self.assertEqual(self.sc.get_resource("honeycomb"), 2)


class TestFoodPreservationKinetics(unittest.TestCase):
    """Tier 3: Spoilage Kinetics, Arrhenius Thermal Scaling, and Cellar Vaults."""

    def test_arrhenius_temperature_doubling(self):
        """Decay rate doubles when temperature increases by 10°C (Q10 = 2.0)."""
        rate_15c = FoodPreservationKineticsOracle.calculate_decay_rate(15.0, 50.0, "WOODEN_CHEST", "NONE")
        rate_25c = FoodPreservationKineticsOracle.calculate_decay_rate(25.0, 50.0, "WOODEN_CHEST", "NONE")
        rate_35c = FoodPreservationKineticsOracle.calculate_decay_rate(35.0, 50.0, "WOODEN_CHEST", "NONE")

        self.assertAlmostEqual(rate_15c, 1.0, places=3)
        self.assertAlmostEqual(rate_25c, 2.0, places=3)
        self.assertAlmostEqual(rate_35c, 4.0, places=3)

    def test_subterranean_cold_cellar_and_icehouse(self):
        """Cold cellars reduce decay by 75% (0.25x), icehouses by 90% (0.10x)."""
        decay_chest = FoodPreservationKineticsOracle.calculate_decay_rate(15.0, 50.0, "WOODEN_CHEST", "NONE")
        decay_cellar = FoodPreservationKineticsOracle.calculate_decay_rate(15.0, 50.0, "COLD_CELLAR", "NONE")
        decay_icehouse = FoodPreservationKineticsOracle.calculate_decay_rate(15.0, 50.0, "ICEHOUSE_VAULT", "NONE")

        self.assertEqual(decay_cellar, decay_chest * 0.25)
        self.assertEqual(decay_icehouse, decay_chest * 0.10)

    def test_preservation_modes_shelf_life_extension(self):
        """Salted meat has ~14x shelf life (0.07x decay) compared to raw."""
        decay_raw = FoodPreservationKineticsOracle.calculate_decay_rate(15.0, 50.0, "WOODEN_CHEST", "NONE")
        decay_smoked = FoodPreservationKineticsOracle.calculate_decay_rate(15.0, 50.0, "WOODEN_CHEST", "SMOKED")
        decay_salted = FoodPreservationKineticsOracle.calculate_decay_rate(15.0, 50.0, "WOODEN_CHEST", "SALTED")

        self.assertEqual(decay_smoked, decay_raw * 0.10)
        self.assertEqual(decay_salted, decay_raw * 0.07)


class TestProductionQuotasAndMorale(unittest.TestCase):
    """Tier 4: Do Until X Quotas, Citizen Feeding, and Morale Dynamics."""

    def setUp(self):
        self.sc = FeudalSupplyChainMock()

    def test_do_until_x_quota_cap(self):
        """Bakers halt bread production when target quota is reached."""
        self.sc.set_quota("bread", 50, FeudalSupplyChainMock.QuotaMode.DO_UNTIL_X)
        self.sc.inventory["bread"] = 50
        self.assertFalse(self.sc.can_produce("bread"))

        # Consume 10 bread -> can produce again
        self.sc.consume_resource("bread", 10)
        self.assertTrue(self.sc.can_produce("bread"))

    def test_paused_quota_mode(self):
        """Paused quota mode prohibits production immediately."""
        self.sc.set_quota("weapons", 100, FeudalSupplyChainMock.QuotaMode.PAUSED)
        self.assertFalse(self.sc.can_produce("weapons"))

    def test_citizen_feeding_and_starvation_morale(self):
        """When citizens go hungry, morale drops towards unfed ratio."""
        assigned = {"farmer": 5, "miner": 5, "lumberjack": 5} # 15 citizens total
        self.sc.inventory["bread"] = 5 # Only 5 bread available, 10 unfed

        initial_morale = self.sc.morale
        report = self.sc.process_production_cycle(assigned)

        self.assertEqual(report["unfed_citizens"], 10)
        self.assertEqual(report["consumed"]["bread"], 5)
        self.assertLess(self.sc.morale, initial_morale)


class TestMarketPricingAndMacroStress(unittest.TestCase):
    """Tier 5: Algorithmic Pricing, Anti-Singularity Bounds, and 1,000-Tick Stress."""

    def test_singularity_guard_zero_supply(self):
        """Zero local supply never triggers division-by-zero or NaN."""
        price = MarketPricingElasticityOracle.calculate_price(10.0, supply=0.0, demand=100.0)
        self.assertFalse(math.isnan(price))
        self.assertFalse(math.isinf(price))
        self.assertEqual(price, 10.0 * 5.0) # Clamped to max 5.0x

    def test_hungry_gap_grain_surge(self):
        """Late-winter hungry gap applies a 2.0x crisis multiplier."""
        normal_price = MarketPricingElasticityOracle.calculate_price(2.0, 50.0, 50.0, False)
        hungry_price = MarketPricingElasticityOracle.calculate_price(2.0, 50.0, 50.0, True)
        self.assertEqual(hungry_price, normal_price * 2.0)

    def test_long_term_1000_tick_economic_stress(self):
        """Simulate 1,000 extreme random economic events with zero NaN, zero negatives, and bounded morale."""
        sc = FeudalSupplyChainMock()
        rng = random.Random(42)

        for tick in range(1000):
            # Random worker assignments
            workers = {
                "farmer": rng.randint(0, 10),
                "baker": rng.randint(0, 5),
                "lumberjack": rng.randint(0, 8),
                "miner": rng.randint(0, 8),
                "blacksmith": rng.randint(0, 4)
            }
            # Production & consumption tick
            report = sc.process_production_cycle(workers)

            # Random economic disaster or windfall
            roll = rng.random()
            if roll < 0.05:
                # Rat infestation in granary: lose 50% wheat
                sc.consume_resource("wheat", sc.get_resource("wheat") // 2)
            elif roll < 0.10:
                # Trade caravan arrival: buy tools
                sc.add_resource("gold_coins", 25)
            elif roll < 0.15:
                # Feast or emergency rations
                sc.salt_meat(rng.randint(0, 3))
                sc.smoke_meat(rng.randint(0, 3))

            # Invariant verifications on every tick
            for res_name, count in sc.inventory.items():
                self.assertGreaterEqual(count, 0, f"Stockpile {res_name} went negative ({count}) on tick {tick}!")
                self.assertFalse(math.isnan(count), f"Stockpile {res_name} became NaN on tick {tick}!")

            self.assertTrue(0.0 <= sc.morale <= 100.0, f"Morale out of bounds ({sc.morale}) on tick {tick}!")


class TestResourcePersistenceRoundtrip(unittest.TestCase):
    """Tier 6: Inventory snapshot serialization & deserialization."""

    def test_serialization_roundtrip(self):
        sc_original = FeudalSupplyChainMock()
        sc_original.inventory["wheat"] = 142
        sc_original.inventory["gold_coins"] = 890
        sc_original.quotas["bread"] = 120
        sc_original.morale = 92.5

        data = sc_original.to_dict()

        sc_restored = FeudalSupplyChainMock()
        sc_restored.from_dict(data)

        self.assertEqual(sc_restored.get_resource("wheat"), 142)
        self.assertEqual(sc_restored.get_resource("gold_coins"), 890)
        self.assertEqual(sc_restored.get_quota("bread"), 120)
        self.assertEqual(sc_restored.morale, 92.5)


if __name__ == "__main__":
    unittest.main()
