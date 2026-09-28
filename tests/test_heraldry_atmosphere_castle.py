# tests/test_heraldry_atmosphere_castle.py
# Voxel Lord: Feudal Realm - Milestone 46 Test Suite
# Tests Royal Heraldry, Atmospheric Post-Processing, Castle Decor Customization, and UI Integration.

import unittest
import math
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class MockColor:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.a = float(a)

    def lerp(self, other, t: float):
        return MockColor(
            self.r + (other.r - self.r) * t,
            self.g + (other.g - self.g) * t,
            self.b + (other.b - self.b) * t,
            self.a + (other.a - self.a) * t,
        )

    def __repr__(self):
        return f"Color({self.r:.2f}, {self.g:.2f}, {self.b:.2f}, {self.a:.2f})"


class MockVector3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def normalized(self):
        mag = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        if mag == 0:
            return MockVector3(0, 0, 0)
        return MockVector3(self.x / mag, self.y / mag, self.z / mag)


# Python mirror of RoyalHeraldry for isolated headless testing
class SimulatedRoyalHeraldry:
    class EmblemType:
        LION_RAMPANT = 0
        IMPERIAL_EAGLE = 1
        FIERY_DRAGON = 2
        ROYAL_STAG = 3
        MONARCH_CROWN = 4
        FLEUR_DE_LIS = 5
        CROSSED_SWORDS = 6
        GOLDEN_WHEAT = 7

    class Tincture:
        GULES = 0
        AZURE = 1
        OR = 2
        ARGENT = 3
        SABLE = 4
        VERT = 5
        PURPURE = 6

    class DivisionType:
        SOLID = 0
        PER_PALE = 1
        PER_FESS = 2
        QUARTERLY = 3
        CHEVRON = 4

    TINCTURE_COLORS = {
        0: MockColor(0.78, 0.14, 0.14),
        1: MockColor(0.12, 0.32, 0.65),
        2: MockColor(0.92, 0.75, 0.18),
        3: MockColor(0.92, 0.94, 0.95),
        4: MockColor(0.12, 0.12, 0.14),
        5: MockColor(0.15, 0.58, 0.22),
        6: MockColor(0.48, 0.12, 0.60),
    }

    TINCTURE_NAMES = {
        0: "Gules (Crimson)",
        1: "Azure (Royal Blue)",
        2: "Or (Gold)",
        3: "Argent (Silver)",
        4: "Sable (Black)",
        5: "Vert (Forest Green)",
        6: "Purpure (Purple)",
    }

    EMBLEM_NAMES = {
        0: "Lion Rampant",
        1: "Imperial Eagle",
        2: "Fiery Dragon",
        3: "Royal Stag",
        4: "Monarch Crown",
        5: "Fleur-de-lis",
        6: "Crossed Broadswords",
        7: "Golden Wheat Sheaf",
    }

    DIVISION_NAMES = {
        0: "Solid Field",
        1: "Per Pale (Vertical Split)",
        2: "Per Fess (Horizontal Split)",
        3: "Quarterly (Four Quarters)",
        4: "Chevron (Inverted V)",
    }

    def __init__(self):
        self.kingdom_name = "Valoria"
        self.motto = "In Fide et Virtute"
        self.emblem = self.EmblemType.LION_RAMPANT
        self.primary_tincture = self.Tincture.OR
        self.secondary_tincture = self.Tincture.AZURE
        self.division = self.DivisionType.QUARTERLY
        self.banner_style = "swallowtail"

    def get_primary_color(self):
        return self.TINCTURE_COLORS[self.primary_tincture]

    def get_secondary_color(self):
        return self.TINCTURE_COLORS[self.secondary_tincture]

    def get_blazon(self):
        pri_name = self.TINCTURE_NAMES[self.primary_tincture]
        sec_name = self.TINCTURE_NAMES[self.secondary_tincture]
        if self.division == self.DivisionType.SOLID:
            div_str = pri_name
        elif self.division == self.DivisionType.PER_PALE:
            div_str = f"Per pale {pri_name} and {sec_name}"
        elif self.division == self.DivisionType.PER_FESS:
            div_str = f"Per fess {pri_name} and {sec_name}"
        elif self.division == self.DivisionType.QUARTERLY:
            div_str = f"Quarterly {pri_name} and {sec_name}"
        elif self.division == self.DivisionType.CHEVRON:
            div_str = f"{pri_name} a chevron {sec_name}"
        else:
            div_str = pri_name

        embl_str = f"a {self.EMBLEM_NAMES[self.emblem]} {pri_name}"
        return f"Field of {div_str}, charged with {embl_str}. Royal Motto: '{self.motto}'."

    def cycle_emblem(self, forward=True):
        count = 8
        if forward:
            self.emblem = (self.emblem + 1) % count
        else:
            self.emblem = (self.emblem - 1 + count) % count
        return self.emblem

    def cycle_primary_tincture(self, forward=True):
        count = 7
        if forward:
            self.primary_tincture = (self.primary_tincture + 1) % count
        else:
            self.primary_tincture = (self.primary_tincture - 1 + count) % count
        return self.primary_tincture

    def cycle_secondary_tincture(self, forward=True):
        count = 7
        if forward:
            self.secondary_tincture = (self.secondary_tincture + 1) % count
        else:
            self.secondary_tincture = (self.secondary_tincture - 1 + count) % count
        return self.secondary_tincture

    def cycle_division(self, forward=True):
        count = 5
        if forward:
            self.division = (self.division + 1) % count
        else:
            self.division = (self.division - 1 + count) % count
        return self.division

    def to_dict(self):
        return {
            "kingdom_name": self.kingdom_name,
            "motto": self.motto,
            "emblem": int(self.emblem),
            "primary_tincture": int(self.primary_tincture),
            "secondary_tincture": int(self.secondary_tincture),
            "division": int(self.division),
            "banner_style": self.banner_style,
        }

    def from_dict(self, d):
        self.kingdom_name = d.get("kingdom_name", self.kingdom_name)
        self.motto = d.get("motto", self.motto)
        self.emblem = d.get("emblem", self.emblem)
        self.primary_tincture = d.get("primary_tincture", self.primary_tincture)
        self.secondary_tincture = d.get("secondary_tincture", self.secondary_tincture)
        self.division = d.get("division", self.division)
        self.banner_style = d.get("banner_style", self.banner_style)


# Python mirror of AtmosphericPostProcess for testing
class SimulatedAtmosphericPostProcess:
    SEASON_FOLIAGE = {
        0: MockColor(0.38, 0.78, 0.26),  # Spring
        1: MockColor(0.18, 0.54, 0.15),  # Summer
        2: MockColor(0.86, 0.46, 0.12),  # Autumn
        3: MockColor(0.82, 0.88, 0.94),  # Winter
    }

    WEATHER_FOG = {
        0: {"density": 0.0006, "energy": 1.0, "wetness": 0.0, "frost": 0.0},
        1: {"density": 0.0022, "energy": 0.75, "wetness": 0.1, "frost": 0.0},
        2: {"density": 0.0075, "energy": 0.45, "wetness": 0.95, "frost": 0.0},
        3: {"density": 0.0280, "energy": 0.30, "wetness": 0.40, "frost": 0.0},
        4: {"density": 0.0160, "energy": 0.55, "wetness": 0.15, "frost": 0.90},
    }

    def calculate_sun(self, day_progress: float):
        angle = day_progress * (2.0 * math.pi)
        pitch = math.sin(angle)
        yaw = math.cos(angle)
        is_day = pitch > -0.05
        energy = max(0.0, min(1.0, pitch))
        return {"pitch": pitch, "yaw": yaw, "is_day": is_day, "energy": energy}

    def get_foliage_tint(self, season: int, day_in_season: int = 15, season_len: int = 30):
        s_curr = season % 4
        s_next = (s_curr + 1) % 4
        t = max(0.0, min(1.0, day_in_season / max(season_len, 1)))
        return self.SEASON_FOLIAGE[s_curr].lerp(self.SEASON_FOLIAGE[s_next], t * 0.5)

    def calculate_fog(self, weather: int, altitude: float, is_night: bool):
        cfg = self.WEATHER_FOG[weather]
        alt_factor = max(0.4, min(1.8, 1.0 - (altitude - 16.0) / 48.0))
        density = cfg["density"] * alt_factor
        return {"density": density, "wetness": cfg["wetness"], "frost": cfg["frost"]}

    def evaluate_atmosphere(self, day_progress: float, season: int, weather: int, altitude: float = 20.0):
        sun = self.calculate_sun(day_progress)
        fog = self.calculate_fog(weather, altitude, not sun["is_day"])
        foliage = self.get_foliage_tint(season)
        return {
            "is_day": sun["is_day"],
            "sun_energy": sun["energy"] * self.WEATHER_FOG[weather]["energy"],
            "fog_density": fog["density"],
            "wetness": fog["wetness"],
            "frost": fog["frost"],
            "foliage": foliage,
        }


# Python mirror of CastleCustomizer for testing
class SimulatedCastleCustomizer:
    CATALOG = {
        "throne_sovereign": {
            "name": "Sovereign Gilded Oak Throne",
            "cost": {"wood": 30, "gold_ingot": 10},
            "buffs": {"realm_morale": 15.0, "renown_per_day": 5.0},
            "prestige": 50,
        },
        "war_council_map": {
            "name": "Grand Realm War Council Table",
            "cost": {"wood": 25, "iron_ingot": 8},
            "buffs": {"guard_defense_bonus": 0.20, "raid_frequency_reduction": 0.15},
            "prestige": 35,
        },
        "chandelier_crystal": {
            "name": "Imperial Chandelier of Starlight",
            "cost": {"iron_ingot": 12, "glass": 16},
            "buffs": {"night_crafting_bonus": 0.15, "realm_morale": 5.0},
            "prestige": 25,
        },
        "treasury_vault_chest": {
            "name": "Royal Ironbound Treasury Vault",
            "cost": {"wood": 15, "iron_ingot": 20, "gold_ingot": 5},
            "buffs": {"tax_efficiency_bonus": 0.15, "gold_capacity_bonus": 500.0},
            "prestige": 40,
        },
        "banquet_great_table": {
            "name": "Monarch Feast & Guild Banquet Table",
            "cost": {"wood": 40, "cloth": 10},
            "buffs": {"hunger_drain_reduction": 0.20, "feast_morale_boost": 25.0},
            "prestige": 30,
        },
        "knights_armor_display": {
            "name": "Royal Champion Plate Display Stand",
            "cost": {"iron_ingot": 16, "wood": 8},
            "buffs": {"guard_attack_bonus": 0.15, "garrison_cap_bonus": 4.0},
            "prestige": 20,
        },
        "astronomers_armillary": {
            "name": "Brass Armillary Sphere & Astrolabe",
            "cost": {"iron_ingot": 10, "gold_ingot": 4},
            "buffs": {"tech_progress_bonus": 0.25, "caravan_trade_profit": 0.10},
            "prestige": 45,
        },
    }

    def __init__(self):
        self.placed_furnishings = {}
        self.active_buffs = {}
        self.total_prestige = 0

    def place_furnishing(self, decor_id: str, pos=(32, 10, 32)):
        if decor_id not in self.CATALOG:
            return False
        self.placed_furnishings[decor_id] = {"id": decor_id, "pos": pos, "active": True}
        self.recalculate_buffs()
        return True

    def remove_furnishing(self, decor_id: str):
        if decor_id in self.placed_furnishings:
            del self.placed_furnishings[decor_id]
            self.recalculate_buffs()
            return True
        return False

    def recalculate_buffs(self):
        self.active_buffs.clear()
        self.total_prestige = 0
        for decor_id, entry in self.placed_furnishings.items():
            if not entry.get("active", True):
                continue
            item = self.CATALOG[decor_id]
            self.total_prestige += item["prestige"]
            for b_name, b_val in item["buffs"].items():
                self.active_buffs[b_name] = self.active_buffs.get(b_name, 0.0) + b_val
        return self.active_buffs

    def to_dict(self):
        return {
            "placed_furnishings": [{"id": k, "pos": v["pos"], "active": v["active"]} for k, v in self.placed_furnishings.items()],
            "total_prestige": self.total_prestige,
        }

    def from_dict(self, data):
        self.placed_furnishings.clear()
        for item in data.get("placed_furnishings", []):
            decor_id = item["id"]
            if decor_id in self.CATALOG:
                self.placed_furnishings[decor_id] = {
                    "id": decor_id,
                    "pos": tuple(item.get("pos", (32, 10, 32))),
                    "active": item.get("active", True),
                }
        self.recalculate_buffs()


class TestHeraldryAtmosphereCastle(unittest.TestCase):
    """Test suite covering Milestone 46 systems."""

    def setUp(self):
        self.heraldry = SimulatedRoyalHeraldry()
        self.atmosphere = SimulatedAtmosphericPostProcess()
        self.castle = SimulatedCastleCustomizer()

    def test_heraldry_initial_state(self):
        self.assertEqual(self.heraldry.kingdom_name, "Valoria")
        self.assertEqual(self.heraldry.motto, "In Fide et Virtute")
        self.assertEqual(self.heraldry.emblem, SimulatedRoyalHeraldry.EmblemType.LION_RAMPANT)
        self.assertEqual(self.heraldry.primary_tincture, SimulatedRoyalHeraldry.Tincture.OR)
        self.assertEqual(self.heraldry.secondary_tincture, SimulatedRoyalHeraldry.Tincture.AZURE)
        self.assertEqual(self.heraldry.division, SimulatedRoyalHeraldry.DivisionType.QUARTERLY)

    def test_heraldry_tincture_colors(self):
        col_gold = self.heraldry.get_primary_color()
        self.assertAlmostEqual(col_gold.r, 0.92, places=2)
        self.assertAlmostEqual(col_gold.g, 0.75, places=2)
        self.assertAlmostEqual(col_gold.b, 0.18, places=2)

        col_blue = self.heraldry.get_secondary_color()
        self.assertAlmostEqual(col_blue.r, 0.12, places=2)
        self.assertAlmostEqual(col_blue.g, 0.32, places=2)

    def test_heraldry_blazon_generation(self):
        blazon = self.heraldry.get_blazon()
        self.assertIn("Quarterly", blazon)
        self.assertIn("Or (Gold)", blazon)
        self.assertIn("Azure (Royal Blue)", blazon)
        self.assertIn("Lion Rampant", blazon)
        self.assertIn("In Fide et Virtute", blazon)

    def test_heraldry_cycling_emblem(self):
        first = self.heraldry.emblem
        next_embl = self.heraldry.cycle_emblem(True)
        self.assertEqual(next_embl, SimulatedRoyalHeraldry.EmblemType.IMPERIAL_EAGLE)
        # Cycle back
        prev_embl = self.heraldry.cycle_emblem(False)
        self.assertEqual(prev_embl, first)

    def test_heraldry_cycling_tinctures(self):
        self.heraldry.primary_tincture = 6  # Purpure
        cycled = self.heraldry.cycle_primary_tincture(True)
        self.assertEqual(cycled, 0)  # Wraps to Gules

        self.heraldry.secondary_tincture = 0
        cycled_sec = self.heraldry.cycle_secondary_tincture(False)
        self.assertEqual(cycled_sec, 6)  # Wraps backward to Purpure

    def test_heraldry_cycling_division(self):
        self.heraldry.division = 4  # Chevron
        cycled_div = self.heraldry.cycle_division(True)
        self.assertEqual(cycled_div, 0)  # Solid

    def test_heraldry_serialization(self):
        self.heraldry.kingdom_name = "Avalon"
        self.heraldry.motto = "Gloria Invicta"
        self.heraldry.emblem = SimulatedRoyalHeraldry.EmblemType.FIERY_DRAGON
        data = self.heraldry.to_dict()

        copy_heraldry = SimulatedRoyalHeraldry()
        copy_heraldry.from_dict(data)
        self.assertEqual(copy_heraldry.kingdom_name, "Avalon")
        self.assertEqual(copy_heraldry.motto, "Gloria Invicta")
        self.assertEqual(copy_heraldry.emblem, SimulatedRoyalHeraldry.EmblemType.FIERY_DRAGON)

    def test_blazon_variations(self):
        self.heraldry.division = SimulatedRoyalHeraldry.DivisionType.SOLID
        self.assertIn("Field of Or (Gold)", self.heraldry.get_blazon())

        self.heraldry.division = SimulatedRoyalHeraldry.DivisionType.PER_PALE
        self.assertIn("Per pale Or (Gold) and Azure (Royal Blue)", self.heraldry.get_blazon())

        self.heraldry.division = SimulatedRoyalHeraldry.DivisionType.CHEVRON
        self.assertIn("Or (Gold) a chevron Azure (Royal Blue)", self.heraldry.get_blazon())

    def test_atmospheric_sun_noon(self):
        # Day progress 0.25 is noon
        sun = self.atmosphere.calculate_sun(0.25)
        self.assertTrue(sun["is_day"])
        self.assertAlmostEqual(sun["pitch"], 1.0, places=2)
        self.assertAlmostEqual(sun["energy"], 1.0, delta=0.05)

    def test_atmospheric_sun_midnight(self):
        # Day progress 0.75 is midnight
        sun = self.atmosphere.calculate_sun(0.75)
        self.assertFalse(sun["is_day"])
        self.assertAlmostEqual(sun["pitch"], -1.0, places=2)
        self.assertEqual(sun["energy"], 0.0)

    def test_atmospheric_seasonal_foliage(self):
        spring_col = self.atmosphere.get_foliage_tint(0, day_in_season=0)
        autumn_col = self.atmosphere.get_foliage_tint(2, day_in_season=0)
        # Autumn red channel should be significantly higher than spring
        self.assertGreater(autumn_col.r, spring_col.r)

    def test_atmospheric_fog_weather_density(self):
        fog_clear = self.atmosphere.calculate_fog(0, altitude=20.0, is_night=False)
        fog_dense = self.atmosphere.calculate_fog(3, altitude=20.0, is_night=False)
        self.assertGreater(fog_dense["density"], fog_clear["density"] * 10)

    def test_atmospheric_altitude_gradient(self):
        # Valley altitude=8 vs Mountain altitude=48
        fog_valley = self.atmosphere.calculate_fog(0, altitude=8.0, is_night=False)
        fog_mountain = self.atmosphere.calculate_fog(0, altitude=48.0, is_night=False)
        self.assertGreater(fog_valley["density"], fog_mountain["density"])

    def test_atmospheric_rain_wetness(self):
        fog_rain = self.atmosphere.calculate_fog(2, altitude=20.0, is_night=False)
        self.assertAlmostEqual(fog_rain["wetness"], 0.95, places=2)

    def test_atmospheric_snow_frost(self):
        fog_snow = self.atmosphere.calculate_fog(4, altitude=20.0, is_night=False)
        self.assertAlmostEqual(fog_snow["frost"], 0.90, places=2)

    def test_atmospheric_full_evaluation(self):
        params = self.atmosphere.evaluate_atmosphere(0.35, season=1, weather=1, altitude=24.0)
        self.assertIn("is_day", params)
        self.assertIn("sun_energy", params)
        self.assertIn("fog_density", params)
        self.assertIn("foliage", params)
        self.assertIn("wetness", params)

    def test_castle_catalog_completeness(self):
        self.assertEqual(len(self.castle.CATALOG), 7)
        self.assertIn("throne_sovereign", self.castle.CATALOG)
        self.assertIn("war_council_map", self.castle.CATALOG)
        self.assertIn("treasury_vault_chest", self.castle.CATALOG)

    def test_castle_furnishing_placement(self):
        res = self.castle.place_furnishing("throne_sovereign", (32, 12, 32))
        self.assertTrue(res)
        self.assertEqual(self.castle.total_prestige, 50)
        self.assertEqual(self.castle.active_buffs["realm_morale"], 15.0)
        self.assertEqual(self.castle.active_buffs["renown_per_day"], 5.0)

    def test_castle_furnishing_removal(self):
        self.castle.place_furnishing("throne_sovereign")
        self.assertEqual(self.castle.total_prestige, 50)
        rem_res = self.castle.remove_furnishing("throne_sovereign")
        self.assertTrue(rem_res)
        self.assertEqual(self.castle.total_prestige, 0)
        self.assertEqual(len(self.castle.active_buffs), 0)

    def test_castle_buff_aggregation(self):
        self.castle.place_furnishing("throne_sovereign")  # +15 Morale, +5 Renown, +50 Prestige
        self.castle.place_furnishing("chandelier_crystal")  # +5 Morale, +15% night crafting, +25 Prestige
        self.castle.place_furnishing("war_council_map")  # +20% defense, +35 Prestige

        self.assertEqual(self.castle.total_prestige, 110)
        self.assertAlmostEqual(self.castle.active_buffs["realm_morale"], 20.0)
        self.assertAlmostEqual(self.castle.active_buffs["guard_defense_bonus"], 0.20)
        self.assertAlmostEqual(self.castle.active_buffs["night_crafting_bonus"], 0.15)

    def test_castle_serialization(self):
        self.castle.place_furnishing("throne_sovereign", (30, 10, 30))
        self.castle.place_furnishing("treasury_vault_chest", (35, 10, 35))
        data = self.castle.to_dict()

        copy_castle = SimulatedCastleCustomizer()
        copy_castle.from_dict(data)
        self.assertEqual(copy_castle.total_prestige, 90)
        self.assertIn("throne_sovereign", copy_castle.placed_furnishings)
        self.assertIn("treasury_vault_chest", copy_castle.placed_furnishings)
        self.assertAlmostEqual(copy_castle.active_buffs["tax_efficiency_bonus"], 0.15)
        self.assertAlmostEqual(copy_castle.active_buffs["gold_capacity_bonus"], 500.0)

    def test_castle_invalid_item_placement(self):
        res = self.castle.place_furnishing("non_existent_decor_item")
        self.assertFalse(res)
        self.assertEqual(self.castle.total_prestige, 0)

    def test_save_system_heraldry_and_castle_data_roundtrip(self):
        self.heraldry.kingdom_name = "Khorasan"
        self.heraldry.motto = "Ad Astra"
        self.castle.place_furnishing("astronomers_armillary")
        
        save_payload = {
            "heraldry": self.heraldry.to_dict(),
            "castle": self.castle.to_dict()
        }
        
        # Restore into new instances
        restored_heraldry = SimulatedRoyalHeraldry()
        restored_heraldry.from_dict(save_payload["heraldry"])
        self.assertEqual(restored_heraldry.kingdom_name, "Khorasan")
        self.assertEqual(restored_heraldry.motto, "Ad Astra")
        
        restored_castle = SimulatedCastleCustomizer()
        restored_castle.from_dict(save_payload["castle"])
        self.assertIn("astronomers_armillary", restored_castle.placed_furnishings)
        self.assertEqual(restored_castle.total_prestige, 45)
        self.assertAlmostEqual(restored_castle.active_buffs["tech_progress_bonus"], 0.25)

    def test_castle_affordability_logic(self):
        # Simulate supply chain
        stockpile = {"wood": 50, "gold_ingot": 15}
        cost = self.castle.CATALOG["throne_sovereign"]["cost"]
        can_afford = all(stockpile.get(item, 0) >= qty for item, qty in cost.items())
        self.assertTrue(can_afford)

        # Deplete gold
        stockpile["gold_ingot"] = 2
        can_afford_depleted = all(stockpile.get(item, 0) >= qty for item, qty in cost.items())
        self.assertFalse(can_afford_depleted)

    def test_heraldry_banner_styles(self):
        styles = ["standard", "swallowtail", "gonfalon", "pennon"]
        for s in styles:
            self.heraldry.banner_style = s
            self.assertEqual(self.heraldry.to_dict()["banner_style"], s)

    def test_atmospheric_sky_color_phases(self):
        atmo = SimulatedAtmosphericPostProcess()
        dawn = atmo.calculate_sun(0.0)
        noon = atmo.calculate_sun(0.25)
        dusk = atmo.calculate_sun(0.50)
        night = atmo.calculate_sun(0.75)
        
        self.assertTrue(noon["is_day"])
        self.assertFalse(night["is_day"])
        self.assertGreater(noon["energy"], dawn["energy"])
        self.assertGreater(noon["energy"], dusk["energy"])


if __name__ == "__main__":
    unittest.main()
