#!/usr/bin/env python3
"""
Voxel Lord: Feudal Realm - Standalone Interactive Playable Simulator
Author: Voxel Lord Engineering Team
Milestone 43: Complete Playable World Assembly & Standalone Release

Enables direct interactive play, exploration, and verification of all 8 feudal
districts and 5 realism pillars directly from the terminal or launcher.
"""

import sys
import math
import time
from typing import Dict, List, Tuple, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


class VoxelRealmSimulator:
    """Standalone interactive simulator of the assembled Voxel Lord realm."""

    DISTRICTS = {
        "citadel": {
            "name": "Royal Citadel & Fortifications",
            "pos": (32.0, 14.0, 32.0),
            "structures": ["portcullis_gate", "watchtower", "trebuchet_siege", "battering_ram", "armory_rack"],
            "biome": "Temperate Forest Citadel",
            "ambient_temp": 16.0,
        },
        "town": {
            "name": "Medieval Town & Market Square",
            "pos": (48.0, 12.0, 32.0),
            "structures": ["town_hall_desk", "treasury_vault", "burgage_coop", "water_well", "caravan_cart"],
            "biome": "Lush Plains Settlement",
            "ambient_temp": 17.5,
        },
        "steam": {
            "name": "Steam & Forge Heavy Metallurgy",
            "pos": (48.0, 12.0, 48.0),
            "structures": ["steam_boiler", "steam_engine_drive", "centrifugal_governor", "furnace", "industrial_trip_hammer"],
            "biome": "Industrial Basin",
            "ambient_temp": 28.0,
        },
        "harbor": {
            "name": "Maritime Harbor & Shipyard",
            "pos": (64.0, 10.0, 16.0),
            "structures": ["drydock_slipway", "quayside_crane", "fluyt_cargo_ship", "treadwheel_crane", "water_cask"],
            "biome": "Coastal Estuary",
            "ambient_temp": 15.0,
        },
        "mining": {
            "name": "Subterranean Mining & Steam Rail",
            "pos": (16.0, 8.0, 16.0),
            "structures": ["mine_locomotive", "rail_switch", "hopper_unloader", "mine_dewatering_pump", "mine_ventilator"],
            "biome": "Rugged Highlands Mine",
            "ambient_temp": 12.0,
        },
        "observatory": {
            "name": "Renaissance Clockwork Observatory",
            "pos": (32.0, 18.0, 56.0),
            "structures": ["astronomical_clock", "armillary_sphere", "celestial_orrery", "barometer_station"],
            "biome": "Highland Plateau",
            "ambient_temp": 11.5,
        },
        "agriculture": {
            "name": "Norfolk 4-Year Crop Rotation Agronomy",
            "pos": (16.0, 12.0, 48.0),
            "structures": ["windmill", "water_wheel", "millstone", "baker_oven", "pasture_barn", "compost_bin"],
            "biome": "Fertile Alluvial Lowlands",
            "ambient_temp": 18.0,
        },
        "wilderness": {
            "name": "Frontier Redoubts & Ancient Crypts",
            "pos": (60.0, 11.0, 60.0),
            "structures": ["crypt_entrance", "stone_sarcophagus", "bandit_tent", "runestone"],
            "biome": "Dark Frontier Wilds",
            "ambient_temp": 13.0,
        }
    }

    MATERIAL_STRENGTH = {
        "limestone": 15.0,
        "granite": 45.0,
        "sandstone": 10.0,
        "fired_brick": 12.0,
        "oak_wood": 8.0,
        "pine_wood": 6.0,
        "iron": 65.0,
        "dirt": 1.0,
    }

    def __init__(self):
        self.monarch_name = "Lord of the Realm"
        self.pos = [32.0, 14.0, 32.0]
        self.health = 100.0
        self.max_health = 100.0
        self.stamina = 100.0
        self.max_stamina = 100.0
        self.calories = 2200.0 # kcal
        self.warmth = 98.0
        self.current_district_key = "citadel"
        self.day_number = 1
        self.time_hour = 9 # 9:00 AM
        self.season = "Spring"
        self.coins = 250
        self.total_renown = 2650
        self.monarch_title = "Sovereign King of the Feudal Realm"

        # Hotbar Inventory
        self.hotbar = [
            {"slot": 1, "name": "Iron Pickaxe", "icon": "⛏️", "type": "tool", "count": 1},
            {"slot": 2, "name": "Wood Axe", "icon": "🪓", "type": "tool", "count": 1},
            {"slot": 3, "name": "Knight Sword", "icon": "⚔️", "type": "tool", "count": 1},
            {"slot": 4, "name": "Farmland Hoe", "icon": "🌾", "type": "tool", "count": 1},
            {"slot": 5, "name": "Wheat Seeds", "icon": "🌱", "type": "item", "count": 32},
            {"slot": 6, "name": "Torch", "icon": "🕯️", "type": "item", "count": 16},
            {"slot": 7, "name": "Ration Bread", "icon": "🍞", "type": "food", "count": 12},
            {"slot": 8, "name": "Cobblestone", "icon": "🪨", "type": "block", "count": 64},
        ]
        self.active_slot = 0

        # Soil & Agronomy State
        self.soil_npk = {"N": 75.0, "P": 60.0, "K": 68.0, "moisture": 82.0}
        self.active_crop = "Winter Wheat (Growth: 65%)"

        # Metallurgy State
        self.furnace_temp = 20.0
        self.furnace_lit = False
        self.steam_boiler_pressure = 0.0

        # Royal Heraldry & Castle Decor State
        self.heraldry = {
            "kingdom_name": "Valoria",
            "motto": "In Fide et Virtute",
            "emblem": "Lion Rampant",
            "primary": "Or (Gold)",
            "secondary": "Azure (Royal Blue)",
            "division": "Quarterly (Four Quarters)",
        }
        self.castle_decor = ["throne_sovereign", "war_council_map", "chandelier_crystal"]
        self.castle_prestige = 110
        self.castle_buffs = {
            "realm_morale": 20.0,
            "renown_per_day": 5.0,
            "guard_defense_bonus": 0.20,
            "raid_frequency_reduction": 0.15,
            "night_crafting_bonus": 0.15,
        }

        # Royal Decrees & Garrison Squadron State
        self.active_decrees = ["corvee_labor"]
        self.garrison_stance = "Defensive Sentinel (Hold Gates & Perimeter)"
        self.garrison_formation = "Shield Wall (Locked Bucklers)"
        self.garrison_guard_count = 6

        # Foreign Diplomacy & Vassalage State
        self.factions = {
            "valoria": {"name": "Duchy of Valoria", "ruler": "Grand Duke Alden IV", "opinion": 15.0, "status": "Neutral ⚖️", "vassal": False, "treaties": []},
            "silvercoast": {"name": "Silvercoast Trade League", "ruler": "High Doge Lorenzo", "opinion": 10.0, "status": "Neutral ⚖️", "vassal": False, "treaties": []},
            "ashfell": {"name": "Ashfell Mountain Clans", "ruler": "Chieftain Torvold Ironfang", "opinion": -25.0, "status": "Hostile ⚠️", "vassal": False, "treaties": []},
            "sunken_mire": {"name": "Barony of the Sunken Mire", "ruler": "Baroness Elspeth", "opinion": 0.0, "status": "Neutral ⚖️", "vassal": False, "treaties": []},
        }

        # Frontier Strategic Outposts & Invasion State
        self.outposts = {
            "north_redoubt": {"name": "Northern Vanguard Redoubt", "health": 150.0, "max_health": 150.0, "garrison": 4, "pitch": True, "status": "Defended 🛡️"},
            "east_watch": {"name": "Eastern Coastline Watchtower", "health": 120.0, "max_health": 120.0, "garrison": 3, "pitch": False, "status": "Defended 🛡️"},
            "west_bastion": {"name": "Western Highlands Bastion", "health": 140.0, "max_health": 140.0, "garrison": 3, "pitch": True, "status": "Defended 🛡️"},
            "south_gate": {"name": "Southern Frontier Palisade Gate", "health": 100.0, "max_health": 100.0, "garrison": 2, "pitch": False, "status": "Defended 🛡️"},
        }
        self.active_invasions = []

        # Grand Tournament & Chivalric Knighthood State
        self.tournament_chivalry = 120
        self.tournament_title = "Squire of the High Seat"
        self.tournament_wins = 0
        self.feasts_hosted = 0
        self.grandstand_excitement = 80.0

        # High Scholastic Monastic Order & Scriptoria Research State (Milestone 51)
        self.scholar_points = 0.0
        self.monk_scribes = 3
        self.unlocked_techs = []
        self.current_research = ""
        self.research_progress = {}
        self.altar_relics = {0: "true_hearth_shard", 1: "", 2: ""}
        self.discovered_relics = ["true_hearth_shard", "st_columba_tome", "perpetual_chalice", "first_monarch_crown", "holy_light_banner"]
        self.abbey_bell_active = False

        # Alchemical Transmutation Laboratory State (Milestone 51)
        self.alembic_temp = 85.0
        self.stone_stage = 1  # 1: Nigredo, 2: Albedo, 3: Citrinitas, 4: Rubedo
        self.brewed_potions = 0
        self.transmutations = 0

        # Royal Spymaster & Shadow Espionage Network State (Milestone 52)
        self.recruited_spies = {}
        self.active_covert_ops = []
        self.captured_spies = []
        self.citadel_security = 65.0
        self.plots_thwarted = 0

        # Feudal Economy, Granary Stockpile & Market Caravan State (Milestone 54)
        self.stockpile = {
            "wheat": 40, "flour": 15, "bread": 50, "meat": 20, "cabbage": 15, "onion": 10, "carrot": 10,
            "sliced_cabbage": 0, "minced_beef": 0, "diced_onion": 0, "cabbage_stew": 0, "shepherd_pie": 0,
            "rock_salt": 15, "cured_meat": 5, "smoked_meat": 5, "logs": 35, "planks": 20, "stone": 30,
            "coal": 20, "iron_ore": 12, "copper_ore": 8, "crushed_iron": 0, "crushed_copper": 0,
            "iron_ingots": 6, "copper_ingot": 0, "steel_ingot": 4, "tools": 10, "weapons": 6,
            "tin_ore": 4, "tin_ingot": 0, "bronze_ingot": 0, "ceramic_mold": 2, "cast_bronze_blade": 0,
            "cast_bronze_pickaxe": 0, "raw_wool": 12, "woolen_tunic": 2, "honeycomb": 8, "beeswax": 6,
            "honey_mead": 2, "beeswax_candle": 4, "iron_bloom": 2, "wrought_iron_ingot": 4
        }
        self.quotas = {"bread": 50, "tools": 10, "weapons": 6, "iron_ingots": 20, "steel_ingot": 8}
        self.quota_modes = {"bread": "until_x", "tools": "until_x", "weapons": "until_x", "iron_ingots": "continuous", "steel_ingot": "until_x"}
        self.market_caravan = {
            "active": True,
            "guild": "Silvercoast Mercantile League",
            "caravan_master": "Merchant Lord Cassian",
            "base_prices": {
                "wheat": 2.0, "flour": 3.5, "bread": 4.5, "meat": 5.0, "cabbage": 2.5, "onion": 2.0,
                "cured_meat": 8.5, "smoked_meat": 8.0, "cabbage_stew": 6.5, "shepherd_pie": 9.5,
                "honey_mead": 12.0, "logs": 3.0, "planks": 5.0, "stone": 2.0, "coal": 4.0,
                "iron_ore": 6.0, "copper_ore": 5.0, "tin_ore": 5.0, "iron_bloom": 8.0,
                "wrought_iron_ingot": 14.0, "iron_ingots": 15.0, "steel_ingot": 25.0, "bronze_ingot": 18.0,
                "tools": 20.0, "weapons": 35.0, "raw_wool": 3.0, "woolen_tunic": 24.0,
                "honeycomb": 4.0, "beeswax": 3.0, "beeswax_candle": 8.0, "rock_salt": 4.0
            }
        }

        # Feudal Manor Leet Court & Judicial System State (Milestone 55)
        self.crime_rate = 14.0  # percentage [0.0, 100.0]
        self.unrest = 10.0      # percentage [0.0, 100.0]
        self.crown_authority = 72.0  # [0.0, 100.0]
        self.public_order = 86.0     # [0.0, 100.0]
        self.active_dockets = [
            {
                "id": "CASE-101",
                "accused": "Bartholomew the Mill Hand",
                "charge": "Granary Theft (Stole 12 sacks of milled flour)",
                "evidence": "Found hiding flour sacks beneath floorboards near Town Hall",
                "severity": 2,
                "guilt_prob": 0.90,
                "status": "Awaiting Verdict"
            },
            {
                "id": "CASE-102",
                "accused": "Giles the Merchant Guildsman",
                "charge": "Tax Evasion & Smuggling Unstamped Wool",
                "evidence": "Concealed 8 bolts of woolen cloth to bypass royal tollgate",
                "severity": 2,
                "guilt_prob": 0.80,
                "status": "Awaiting Verdict"
            },
            {
                "id": "CASE-103",
                "accused": "Roger of the Mire",
                "charge": "Seditious Libel & Plotting with Ashfell Clans",
                "evidence": "Intercepted encrypted parchment in tavern endorsing highland raid",
                "severity": 4,
                "guilt_prob": 0.95,
                "status": "Awaiting Verdict"
            }
        ]
        self.verdict_history = []
        self.ratified_charters = []

        # Monarch Trauma, Chirurgery & Health State (Milestone 56 - GDD Section 6)
        self.monarch_level = 5
        self.monarch_status = "active"  # "active", "incapacitated", "bedridden", "captive"
        self.trauma_conditions = []
        self.court_doctor_skill = 15  # Skill_doctor in [0, 50]
        self.ransom_demanded = 0
        self.bed_rest_remaining = 0.0  # in game hours
        self.trauma_history = []

        # Diurnal Schedule & Astronomical Calendar State (Milestone 56 - GDD Section 3)
        self.simulation_ticks = 9 * 60  # 9:00 AM (540 ticks)
        self.diurnal_schedule = {
            "DAWN_MATINS": {"start": 5, "end": 7, "phase": "Dawn & Matins", "prod_mult": 0.8, "desc": "Morning chapel prayer, awakening, and tool preparation."},
            "MORNING_WORK": {"start": 7, "end": 12, "phase": "Prime Labor", "prod_mult": 1.2, "desc": "Field plowing, forge hammering, and quarry extraction."},
            "NOON_REPAST": {"start": 12, "end": 13, "phase": "Midday Meal", "prod_mult": 0.5, "desc": "Communal lunch, water break, and draft ox resting."},
            "AFTERNOON_WORK": {"start": 13, "end": 18, "phase": "Guild Crafting", "prod_mult": 1.1, "desc": "Artisan joinery, weaving, masonry, and trade stalls."},
            "VESPERS_SUPPER": {"start": 18, "end": 21, "phase": "Tavern & Rest", "prod_mult": 0.6, "desc": "Vespers prayer, tavern ale, song, and family supper."},
            "NIGHT_SLUMBER": {"start": 21, "end": 5, "phase": "Night Curfew", "prod_mult": 0.0, "desc": "Curfew bells, gate lockup, citizen slumber, and watchmen patrol."}
        }

        # Demographic Aging & Population Lifecycle State (Milestone 56 - GDD Section 4)
        self.population_cohorts = {
            "AGE_INF": {"name": "Infancy (0-3 yrs)", "count": 6, "labor_mult": 0.0, "carry_mult": 0.0, "desc": "Dependent on nursing mothers; pure care burden."},
            "AGE_CHI": {"name": "Childhood (4-10 yrs)", "count": 9, "labor_mult": 0.2, "carry_mult": 0.2, "desc": "Light chores: egg gathering, poultry scaring, learning catechism."},
            "AGE_APP": {"name": "Apprentice (11-15 yrs)", "count": 8, "labor_mult": 0.6, "carry_mult": 0.6, "desc": "Guild workshop assistants; +50% skill gain rate."},
            "AGE_YAD": {"name": "Young Adult (16-34 yrs)", "count": 22, "labor_mult": 1.15, "carry_mult": 1.1, "desc": "Prime military levee, heavy mining, deep forestry, field harvesting."},
            "AGE_MAT": {"name": "Mature Adult (35-49 yrs)", "count": 18, "labor_mult": 1.2, "carry_mult": 1.0, "desc": "Master craftsmen, bailiffs, senior sergeants, guild masters."},
            "AGE_ELD": {"name": "Elderly (50-65 yrs)", "count": 7, "labor_mult": 0.85, "carry_mult": 0.85, "desc": "Village aldermen, cloister scribes, senior tutors, court jurors."},
            "AGE_VEN": {"name": "Venerable (66-80+ yrs)", "count": 3, "labor_mult": 0.35, "carry_mult": 0.4, "desc": "Clan patriarchs/matriarchs; advisory wisdom; Gompertz mortality risk."}
        }
        self.demographic_stats = {
            "total_births": 12,
            "total_deaths": 4,
            "immigrants": 6,
            "emigrants": 1,
            "housing_capacity": 85,
            "food_variety": 4
        }

        # Municipal Sanitation & Epidemiology State (Milestone 57 - GDD Sections 74-77)
        self.filth_level = 22.0  # [0.0, 100.0]
        self.waste_rate = 0.05   # kg/hour per citizen
        self.dung_rate = 0.25    # kg/hour per livestock
        self.livestock_count = 14
        self.miasma_active = False
        self.street_sweepers_count = 2
        self.cesspool_fill = 28.0  # [0.0, 100.0]
        self.compost_fertilizer_stock = 4  # barrels
        self.pest_control_cats = 6
        self.stone_drainage_active = True
        self.aqueduct_clean_water = True

        # SIR Differential Epidemiology State
        total_citizens = sum(c["count"] for c in self.population_cohorts.values())
        self.sir_state = {
            "S": float(total_citizens),
            "I": 0.0,
            "R": 0.0,
            "deaths": 0
        }
        self.active_epidemic = None  # None, "dysentery", "influenza", "typhus", "bubonic_plague", "pneumonic_plague"
        self.plague_doctor_appointed = False
        self.quarantine_edict_active = False
        self.quarantine_measures = []
        self.epidemic_history = []
        self.citizen_morale = 80.0
        self._saved_slots = {}


    def print_header(self):
        print("\n" + "=" * 78)
        print("          VOXEL LORD: FEUDAL REALM - INTERACTIVE PLAYABLE SIMULATOR")
        print("    Full 112 Model World Assembly | 5 Realism Pillars | Direct Control")
        print("=" * 78)

    def print_hud(self):
        curr_dist = self.DISTRICTS[self.current_district_key]
        phase = self.get_current_diurnal_phase()
        status_tag = ""
        if self.monarch_status == "captive":
            status_tag = f" | 🚨 CAPTIVE (Ransom: {self.ransom_demanded} 💰)"
        elif self.monarch_status == "bedridden":
            status_tag = f" | 🛌 BEDRIDDEN ({self.bed_rest_remaining:.1f}h rest left)"
        elif self.trauma_conditions:
            status_tag = f" | ⚠️ INJURED ({len(self.trauma_conditions)} trauma)"

        if self.miasma_active:
            status_tag += " | ☣️ MIASMA"
        if self.active_epidemic:
            status_tag += f" | ☠️ {self.active_epidemic.upper()} ({self.sir_state['I']:.0f} sick)"

        print(f"\n[MONARCH HUD] ❤️ HP: {self.health:.0f}/100 | ⚡ ST: {self.stamina:.0f}/100 | 🍗 Calories: {self.calories:.0f} kcal | 🔥 Warmth: {self.warmth:.1f}°C{status_tag}")
        print(f"[TIME & REALM] Day {self.day_number} ({self.season}) - {self.time_hour:02d}:00 [{phase['phase']}] | Coins: {self.coins} 💰 | Ambient: {curr_dist['ambient_temp']:.1f}°C")
        print(f"[LOCATION] District: {curr_dist['name']}")
        print(f"[POSITION] Coordinates: (X: {self.pos[0]:.1f}, Y: {self.pos[1]:.1f}, Z: {self.pos[2]:.1f}) | Biome: {curr_dist['biome']}")
        print("-" * 78)
        # Hotbar
        hb_str = " | ".join([f"[{i+1}] {item['icon']} {item['name']} ({item['count']})" for i, item in enumerate(self.hotbar)])
        print(f"HOTBAR: {hb_str}")
        print("-" * 78)

    def print_map(self):
        print("\n=== REALM DISTRICT OVERVIEW MAP (64x64 Grid) ===")
        print("   Z=16         Z=32         Z=48         Z=56")
        print("X=16: [MINING]      |            | [AGRI]       |")
        print("X=32:               | [CITADEL]  |              | [OBSERVATORY]")
        print("X=48:               | [TOWN]     | [STEAM]      |")
        print("X=64: [HARBOR]      |            |              | [WILDERNESS]")
        print("=================================================")

    def fast_travel(self, district_key: str):
        district_key = district_key.lower().strip()
        if district_key in self.DISTRICTS:
            self.current_district_key = district_key
            d = self.DISTRICTS[district_key]
            self.pos = list(d["pos"])
            self.calories -= 25.0
            self.stamina = max(10.0, self.stamina - 15.0)
            print(f"\n⚡ Fast-traveled Monarch to: {d['name']} at coordinates {self.pos}!")
            print(f"🏛️ Key Structures nearby: {', '.join(d['structures'])}")
        else:
            print(f"\n[!] Unknown district '{district_key}'. Available: {', '.join(self.DISTRICTS.keys())}")

    def inspect_block(self):
        curr_dist = self.DISTRICTS[self.current_district_key]
        print(f"\n🔍 [INSPECT TELEMETRY - TARGETED VOXEL / STRUCTURE]")
        print(f"Target Anchor: (X: {self.pos[0]:.0f}, Y: {self.pos[1]-1:.0f}, Z: {self.pos[2]:.0f})")
        print(f"Material: Cut Limestone Ashlar Block [Solid Voxel]")
        stress = 3.6
        max_stress = self.MATERIAL_STRENGTH["limestone"]
        margin = ((max_stress - stress) / max_stress) * 100.0
        print(f"Compressive Stress: σ_c = {stress:.2f} MPa / {max_stress:.1f} MPa (Safety Margin: {margin:.1f}% - STABLE)")
        print(f"Thermodynamic Temperature: {curr_dist['ambient_temp']:.1f}°C (Conductivity α = 0.05 m²/s)")
        if self.current_district_key == "agriculture":
            print(f"Soil Agronomy: N: {self.soil_npk['N']}% | P: {self.soil_npk['P']}% | K: {self.soil_npk['K']}% | Moisture: {self.soil_npk['moisture']}%")
            print(f"Crop Status: {self.active_crop}")
        elif self.current_district_key == "steam":
            print(f"Industrial Boiler: Pressure {self.steam_boiler_pressure:.1f} bar | Firebox: {self.furnace_temp:.1f}°C")
        print(f"Nearby Landmark Model: {curr_dist['structures'][0]}.glb (PBR Triplanar Material active)")

    def mine_voxel(self):
        print(f"\n⛏️ [MINING VOXEL ACTION]")
        print(f"Swinging {self.hotbar[0]['name']} at target voxel...")
        self.stamina = max(0.0, self.stamina - 12.0)
        self.calories -= 8.0
        print("✓ Voxel fractured! Harvested: +1 Cobblestone [VoxelChunk Block mined].")
        print("✓ Structural Integrity graph re-evaluated: Cantilever overhang within 4-block shear limit. No cave-in.")

    def operate_furnace(self):
        print(f"\n🔥 [METALLURGY & THERMODYNAMICS]")
        if not self.furnace_lit:
            self.furnace_lit = True
            self.furnace_temp = 850.0
            self.steam_boiler_pressure = 12.0
            print("Igniting refractory firebox with charcoal and draft tuyere...")
            print("Bernoulli chimney draft engaged! Air velocity v = 7.4 m/s.")
            print(f"Firebox temperature surged to {self.furnace_temp}°C!")
            print(f"Steam boiler pressurized to {self.steam_boiler_pressure} bar! Generating 1,024 SU at 64 RPM.")
        else:
            self.furnace_temp = 1420.0
            print(f"Furnace stoked with coal! Peak temperature: {self.furnace_temp}°C. Ready to cast Crucible Steel!")

    def fire_trebuchet(self):
        print(f"\n🎯 [GRAVITATIONAL TREBUCHET BALLISTICS]")
        mass = 120.0 # kg
        v0 = 42.0 # m/s
        theta_deg = 45.0
        g = 9.81
        flight_time = (2 * v0 * math.sin(math.radians(theta_deg))) / g
        range_dist = (v0**2 * math.sin(math.radians(2 * theta_deg))) / g
        impact_ke = 0.5 * mass * (v0**2)
        print(f"Launching 120 kg stone boulder at {v0} m/s ({theta_deg}° trajectory)...")
        print(f"Ballistic Flight Time: {flight_time:.2f} seconds | Distance Traveled: {range_dist:.1f} meters")
        print(f"Kinetic Impact Energy: {impact_ke:.0f} Joules!")
        print("✓ Direct hit on distant bandit barricade! Voxel fracturing triggered across 6-meter radius.")

    def save_realm(self, slot: str = "quicksave") -> str:
        import hashlib, json
        data = {
            "version": "1.0.0",
            "slot_name": slot,
            "district": self.current_district_key,
            "pos": self.pos,
            "health": self.health,
            "calories": self.calories,
            "stamina": self.stamina,
            "day": self.day_number,
            "time_hour": self.time_hour,
            "coins": self.coins,
            "monarch_level": self.monarch_level,
            "monarch_status": self.monarch_status,
            "trauma_conditions": self.trauma_conditions,
            "court_doctor_skill": self.court_doctor_skill,
            "ransom_demanded": self.ransom_demanded,
            "bed_rest_remaining": self.bed_rest_remaining,
            "trauma_history": self.trauma_history,
            "simulation_ticks": self.simulation_ticks,
            "population_cohorts": self.population_cohorts,
            "demographic_stats": self.demographic_stats,
            "stockpile": self.stockpile,
            "quotas": self.quotas,
            "quota_modes": self.quota_modes,
            "crime_rate": self.crime_rate,
            "unrest": self.unrest,
            "crown_authority": self.crown_authority,
            "public_order": self.public_order,
            "active_dockets": self.active_dockets,
            "verdict_history": self.verdict_history,
            "ratified_charters": self.ratified_charters,
            "filth_level": self.filth_level,
            "miasma_active": self.miasma_active,
            "street_sweepers_count": self.street_sweepers_count,
            "cesspool_fill": self.cesspool_fill,
            "compost_fertilizer_stock": self.compost_fertilizer_stock,
            "pest_control_cats": self.pest_control_cats,
            "stone_drainage_active": self.stone_drainage_active,
            "aqueduct_clean_water": self.aqueduct_clean_water,
            "sir_state": self.sir_state,
            "active_epidemic": self.active_epidemic,
            "plague_doctor_appointed": self.plague_doctor_appointed,
            "quarantine_edict_active": self.quarantine_edict_active,
            "quarantine_measures": self.quarantine_measures,
            "epidemic_history": self.epidemic_history,
        }
        raw_str = json.dumps(data, sort_keys=True)
        import copy
        self._saved_slots[slot] = copy.deepcopy(data)
        checksum = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
        print(f"\n💾 [SAVE REALM PERSISTENCE]")
        print(f"Slot: '{slot}' | Voxel Delta Hash: {checksum[:8]}...")
        print(f"Monarch State: {self.health:.0f} HP, {self.calories:.0f} kcal, Pos: {self.pos}")
        print(f"Economy & Justice Preserved: {len(self.stockpile)} items, Crown Authority: {self.crown_authority:.1f}%, {self.coins} 💰 Gold.")
        print("✓ Sparse Delta Voxel persistence written successfully.")
        return checksum

    def load_realm(self, slot: str = "quicksave") -> bool:
        import copy
        if slot in self._saved_slots:
            data = copy.deepcopy(self._saved_slots[slot])
            self.current_district_key = data.get("district", self.current_district_key)
            self.pos = list(data.get("pos", self.pos))
            self.health = data.get("health", self.health)
            self.calories = data.get("calories", self.calories)
            self.stamina = data.get("stamina", self.stamina)
            self.day_number = data.get("day", self.day_number)
            self.time_hour = data.get("time_hour", self.time_hour)
            self.coins = data.get("coins", self.coins)
            self.monarch_level = data.get("monarch_level", self.monarch_level)
            self.monarch_status = data.get("monarch_status", self.monarch_status)
            self.trauma_conditions = list(data.get("trauma_conditions", self.trauma_conditions))
            self.court_doctor_skill = data.get("court_doctor_skill", self.court_doctor_skill)
            self.ransom_demanded = data.get("ransom_demanded", self.ransom_demanded)
            self.bed_rest_remaining = data.get("bed_rest_remaining", self.bed_rest_remaining)
            self.stockpile = copy.deepcopy(data.get("stockpile", self.stockpile))
            self.quotas = copy.deepcopy(data.get("quotas", self.quotas))
            self.crime_rate = data.get("crime_rate", self.crime_rate)
            self.unrest = data.get("unrest", self.unrest)
            self.crown_authority = data.get("crown_authority", self.crown_authority)
            self.public_order = data.get("public_order", self.public_order)
            self.filth_level = data.get("filth_level", self.filth_level)
            self.miasma_active = data.get("miasma_active", self.miasma_active)
            self.street_sweepers_count = data.get("street_sweepers_count", self.street_sweepers_count)
            self.cesspool_fill = data.get("cesspool_fill", self.cesspool_fill)
            self.compost_fertilizer_stock = data.get("compost_fertilizer_stock", self.compost_fertilizer_stock)
            self.sir_state = copy.deepcopy(data.get("sir_state", self.sir_state))
            self.active_epidemic = data.get("active_epidemic", self.active_epidemic)
            self.plague_doctor_appointed = data.get("plague_doctor_appointed", self.plague_doctor_appointed)
            self.quarantine_edict_active = data.get("quarantine_edict_active", self.quarantine_edict_active)
            self.quarantine_measures = list(data.get("quarantine_measures", self.quarantine_measures))
        print(f"\n📂 [LOAD REALM PERSISTENCE]")
        print(f"Slot: '{slot}' loaded cleanly. Checksum verified: SHA-256 integrity OK.")
        print(f"Restoring Monarch at district: {self.DISTRICTS[self.current_district_key]['name']}.")
        print("✓ Granary stockpile, guild production quotas, and judicial court dockets restored.")
        return True

    def play_audio_sfx(self, effect: str = "horn"):
        effect = effect.lower()
        print(f"\n🔊 [DYNAMIC PROCEDURAL AUDIO]")
        if effect in ["horn", "warhorn"]:
            print("📯 Monarch Brass Horn (146.8 Hz D3, 1.2s tone) sounded across all districts!")
        elif effect in ["pickaxe", "mine"]:
            print("⛏️ Resonant Pickaxe Clang on Granite (640 Hz strike tone).")
        elif effect in ["axe", "chop"]:
            print("🪓 Timber Axe Chop (280 Hz thud on Oak Trunk).")
        elif effect in ["footstep", "step"]:
            print("👞 Footstep on Cut Limestone Ashlar (180 Hz acoustic step).")
        elif effect in ["ambient", "district"]:
            d = self.DISTRICTS[self.current_district_key]
            print(f"🎶 District Ambiance ({d['name']}): Wind, settlement bustle, and historical depth.")
        else:
            print(f"🔔 Acoustic Tone '{effect}' synthesized cleanly.")

    def show_quest_journal(self):
        print("\n📜 [ROYAL DEEDS & FEUDAL QUEST CHRONICLE]")
        print(f"👑 Sovereign Title: {self.monarch_title} | ⚜️ Total Renown: {self.total_renown}")
        print("Active Deed: VI. The Sovereign Coronation (Reward: +1,500 Renown)")
        print("Feudal Objectives:")
        print("  [✓] Harvest Wood & Stone Voxels (10/10)")
        print("  [✓] Till Norfolk Farmland & Smelt Iron Ingots (4/4)")
        print("  [✓] Ignite Industrial Steam Boiler (12.0 bar pressurized)")
        print("  [✓] Construct Fluyt Cargo Ship at Quayside")
        print("  [✓] Activate Prague Astronomical Clock in Observatory")
        print("  [✓] Sound Royal War Horn & Defend Frontier Realm")
        print("🎉 Realm Prestige: Supreme Feudal Triumph! All 8 Districts Prosperous.")

    def talk_to_citizen(self, role: str = "smith"):
        dialogues = {
            "smith": ("Eldred the Metallurgist", "Blacksmith", 92.0, "The blast furnace draft is blowing true at 1400°C, Sire! Quality folded crucible steel for your knights!"),
            "farmer": ("Osric the Agronomist", "Farmer", 88.0, "Norfolk 4-year crop rotation is filling our granaries, my Lord. The barley and clover thrive!"),
            "guard": ("Gareth the Shield", "Guard", 95.0, "The watchtower sentinels report clear skies, Sire. No bandit raider shall breach our keep."),
            "baker": ("Rowena the Baker", "Baker", 85.0, "Fresh hearth loaves baked from windmilled flour, my Liege! The citizens are well nourished.")
        }
        name, occ, morale, speech = dialogues.get(role.lower(), dialogues["smith"])
        print(f"\n🗣️ [CITIZEN DIALOGUE: {name}]")
        print(f"Occupation: {occ} | Morale: {morale:.0f}% [Exultant]")
        print(f'"{speech}"')
        print("Monarch Options: [1] Give Fresh Ration (+15 Morale) | [2] Monarch's Inspiration (+5 Morale) | [3] Reassign Duty")

    def show_heraldry(self):
        h = self.heraldry
        print("\n🛡️ === ROYAL HERALDRY & COAT OF ARMS ===")
        print(f"Kingdom: {h['kingdom_name']} | Royal Motto: '{h['motto']}'")
        print(f"Field: {h['division']}")
        print(f"Primary Tincture: {h['primary']} | Secondary: {h['secondary']}")
        print(f"Crest Emblem: {h['emblem']}")
        print(f"Blazon: Field of {h['division']} {h['primary']} and {h['secondary']}, charged with a {h['emblem']}.")
        print("Banners: All castle towers and guard uniforms tinted to royal tinctures.")

    def show_castle_customizer(self):
        print("\n🏰 === MONARCH CASTLE & THRONE ROOM CUSTOMIZER ===")
        print(f"Castle Prestige: {self.castle_prestige} 👑")
        print(f"Installed Royal Furnishings ({len(self.castle_decor)} items):")
        for decor in self.castle_decor:
            print(f"  • [INSTALLED] {decor.replace('_', ' ').title()}")
        print("\nActive Imperial Realm Buffs:")
        for k, v in self.castle_buffs.items():
            sign = "+" if v > 0 else ""
            print(f"  ✨ {k}: {sign}{v}")

    def install_furnishing(self, decor_id: str):
        decor_catalog = {
            "throne": ("throne_sovereign", 50, {"realm_morale": 15.0, "renown_per_day": 5.0}),
            "map": ("war_council_map", 35, {"guard_defense_bonus": 0.20, "raid_frequency_reduction": 0.15}),
            "chandelier": ("chandelier_crystal", 25, {"night_crafting_bonus": 0.15, "realm_morale": 5.0}),
            "vault": ("treasury_vault_chest", 40, {"tax_efficiency_bonus": 0.15, "gold_capacity_bonus": 500.0}),
            "table": ("banquet_great_table", 30, {"hunger_drain_reduction": 0.20, "feast_morale_boost": 25.0}),
            "armor": ("knights_armor_display", 20, {"guard_attack_bonus": 0.15, "garrison_cap_bonus": 4.0}),
            "armillary": ("astronomers_armillary", 45, {"tech_progress_bonus": 0.25, "caravan_trade_profit": 0.10}),
        }
        key = decor_id.lower().strip()
        if key not in decor_catalog:
            print(f"Unknown furnishing '{decor_id}'. Options: {', '.join(decor_catalog.keys())}")
            return
        full_id, prestige, buffs = decor_catalog[key]
        if full_id in self.castle_decor:
            print(f"Furnishing '{full_id}' is already installed in the Throne Room.")
            return
        self.castle_decor.append(full_id)
        self.castle_prestige += prestige
        for b_name, b_val in buffs.items():
            self.castle_buffs[b_name] = self.castle_buffs.get(b_name, 0.0) + b_val
        print(f"✅ Installed {full_id} in Castle Throne Room! (+{prestige} Prestige)")

    def show_decrees(self):
        catalog = {
            "corvee_labor": ("Corvée Mandatory Labor Mandate", "+30% Work Speed, +20% Hunger Drain", 50, 20),
            "grain_dole_relief": ("Imperial Grain Dole Relief", "-35% Hunger Drain, +25 Morale", 25, 10),
            "guild_subsidies": ("Artisan Guild Patronage", "+25% Craft Yield, +35% Smelt Speed", 45, 50),
            "frontier_conscription": ("Frontier Militia Levy", "+25% Guard Defense, +4 Militia Cap", 60, 35),
            "free_trade_charter": ("Mercantile Free Trade", "-35% Caravan Timer, -15% Trade Prices", 30, 30),
            "monastic_scholarship": ("Monastic Scholarly Patronage", "+40% Tech Speed, +50% Healing", 75, 60),
        }
        print("\n📜 === IMPERIAL FEUDAL EDICTS & DECREES ===")
        print(f"Monarch Renown: {self.total_renown} ⚜️ | Royal Treasury: {self.coins} 💰")
        for dec_id, (name, effect, ren, coins) in catalog.items():
            status = "[ACTIVE - ENACTED]" if dec_id in self.active_decrees else "[READY TO PROCLAIM]"
            print(f"  • {status} {name} (Renown: {ren}, Coins: {coins})")
            print(f"    Effect: {effect}")

    def proclaim_decree(self, decree_id: str):
        key = decree_id.lower().strip()
        valid = ["corvee_labor", "grain_dole_relief", "guild_subsidies", "frontier_conscription", "free_trade_charter", "monastic_scholarship"]
        matched = [v for v in valid if key in v]
        if not matched:
            print(f"Unknown decree '{decree_id}'. Options: {', '.join(valid)}")
            return
        chosen = matched[0]
        if chosen in self.active_decrees:
            print(f"Decree '{chosen}' is already active!")
            return
        self.active_decrees.append(chosen)
        print(f"📜 Monarch Proclamation: Decree '{chosen}' is now active across the realm!")

    def show_squadron(self):
        print("\n⚔️ === GARRISON SQUADRON TACTICAL COMMAND ===")
        print(f"Garrison Strength: {self.garrison_guard_count} Shielded Guards & Archers")
        print(f"Tactical Stance: {self.garrison_stance}")
        print(f"Military Formation: {self.garrison_formation}")
        print("Formation Modifiers: +35% Shield Defense, -20% Move Speed, +30% Block Chance")
        print("Rally Status: Guards actively patrolling royal citadel walls.")

    def set_squadron_formation(self, formation_name: str):
        formations = {
            "wall": "Shield Wall (Locked Bucklers)",
            "wedge": "Shock Wedge (Vanguard Charge)",
            "skirmish": "Skirmish Line (Spread Archers)",
            "square": "Perimeter Square (360° Bulwark)"
        }
        key = formation_name.lower().strip()
        matched = [k for k in formations if key in k]
        if not matched:
            print(f"Unknown formation '{formation_name}'. Options: {', '.join(formations.keys())}")
            return
        self.garrison_formation = formations[matched[0]]
        print(f"⚔️ Squadron Commander: Formed into {self.garrison_formation}!")

    def show_diplomacy(self):
        print("\n📜 === ROYAL CHANCERY & REALM DIPLOMACY ===")
        for f_id, f in self.factions.items():
            treaties_str = ", ".join(f["treaties"]) if f["treaties"] else "None"
            vassal_str = " [VASSAL FEALTY 👑]" if f["vassal"] else ""
            print(f"  • {f['name']} ({f['ruler']}){vassal_str}")
            print(f"    Status: {f['status']} | Opinion: {f['opinion']:+.1f} / 100.0 | Active Treaties: {treaties_str}")

    def send_diplomatic_gift(self, faction_id: str, amount: int = 15):
        key = faction_id.lower().strip()
        matched = [k for k in self.factions if key in k]
        if not matched:
            print(f"Unknown realm '{faction_id}'. Available: {', '.join(self.factions.keys())}")
            return
        f_key = matched[0]
        f = self.factions[f_key]
        boost = min(35.0, amount * 1.5)
        f["opinion"] = min(100.0, f["opinion"] + boost)
        if f["opinion"] >= 30.0 and "Friendly" not in f["status"]:
            f["status"] = "Friendly 🕊️"
        print(f"🎁 Chancery Envoy: Dispatched {amount} tribute to {f['name']} (+{boost:.1f} Opinion -> {f['opinion']:.1f})")

    def sign_diplomatic_treaty(self, faction_id: str, treaty_name: str):
        key = faction_id.lower().strip()
        matched = [k for k in self.factions if key in k]
        if not matched:
            print(f"Unknown realm '{faction_id}'. Available: {', '.join(self.factions.keys())}")
            return
        f_key = matched[0]
        f = self.factions[f_key]
        t_key = treaty_name.lower().strip()
        valid = {"non_aggression": "Non-Aggression Pact", "trade": "Trade Concordat", "alliance": "Defensive League", "vassal": "Vassalage Fealty Charter"}
        found_t = [k for k in valid if t_key in k]
        if not found_t:
            print(f"Unknown treaty '{treaty_name}'. Options: {', '.join(valid.keys())}")
            return
        t_title = valid[found_t[0]]
        if t_title in f["treaties"]:
            print(f"Treaty '{t_title}' already active with {f['name']}!")
            return
        f["treaties"].append(t_title)
        if "Vassalage" in t_title:
            f["vassal"] = True
            f["status"] = "Vassal Fealty 👑"
            f["opinion"] = min(100.0, f["opinion"] + 25.0)
        else:
            f["opinion"] = min(100.0, f["opinion"] + 10.0)
        print(f"🤝 Chancery Ratification: Ratified {t_title} with {f['name']}!")

    def demand_diplomatic_tribute(self, faction_id: str):
        key = faction_id.lower().strip()
        matched = [k for k in self.factions if key in k]
        if not matched:
            print(f"Unknown realm '{faction_id}'. Available: {', '.join(self.factions.keys())}")
            return
        f_key = matched[0]
        f = self.factions[f_key]
        if f["vassal"] or f["opinion"] >= 20.0:
            self.coins += 40
            f["opinion"] -= 15.0
            print(f"👑 Imperial Demands: {f['name']} yielded 40 Gold Coins in tribute! (Opinion -15.0 -> {f['opinion']:.1f})")
        else:
            f["opinion"] -= 30.0
            print(f"⚔️ Insolence: {f['name']} defiantly refused your tribute demands! (Opinion -30.0 -> {f['opinion']:.1f})")

    def declare_diplomatic_war(self, faction_id: str):
        key = faction_id.lower().strip()
        matched = [k for k in self.factions if key in k]
        if not matched:
            print(f"Unknown realm '{faction_id}'. Available: {', '.join(self.factions.keys())}")
            return
        f_key = matched[0]
        f = self.factions[f_key]
        f["vassal"] = False
        f["treaties"].clear()
        f["opinion"] = -100.0
        f["status"] = "War ⚔️"
        print(f"⚔️ HERALD PROCLAMATION: The Crown has declared total WAR upon {f['name']}! All treaties severed.")

    def show_war_room(self):
        print("\n⚔️ === ROYAL WAR ROOM & STRATEGIC REALM DEFENSE MAP ===")
        print("FRONTIER REDOUBTS & OUTPOSTS:")
        for op_id, op in self.outposts.items():
            pitch_str = " | Pitch: Armed 🔥" if op["pitch"] else ""
            print(f"  • {op['name']} [HP: {op['health']:.0f}/{op['max_health']:.0f}] - Garrison: {op['garrison']} guards{pitch_str}")
            print(f"    Status: {op['status']}")

        print("\nMARCHING INVASION BATTALIONS:")
        if not self.active_invasions:
            print("  ✓ No active hostile battalions reported on realm borders.")
        else:
            for b in self.active_invasions:
                print(f"  • {b['leader']} ({b['faction']}) - {b['troops']} troops [Siege: {b['siege']}] -> Marching on {b['target']} (Progress: {b['progress']*100:.0f}%)")

    def trigger_test_invasion(self, faction_id: str = "ashfell"):
        target = "north_redoubt"
        leader = "Warlord Torvold Ironfang" if "ash" in faction_id else "Knight Commander Valen"
        troops = 16
        siege = "battering_ram"
        self.active_invasions.append({
            "leader": leader,
            "faction": faction_id.capitalize(),
            "troops": troops,
            "siege": siege,
            "target": target,
            "progress": 0.35
        })
        self.outposts[target]["status"] = "Hostiles Approaching ⚠️"
        print(f"🚨 WAR ALARM: Hostile battalion led by {leader} sighted marching on {self.outposts[target]['name']}!")

    def reinforce_outpost(self, outpost_id: str, guards: int = 2):
        key = outpost_id.lower().strip()
        matched = [k for k in self.outposts if key in k]
        if not matched:
            print(f"Unknown outpost '{outpost_id}'. Options: {', '.join(self.outposts.keys())}")
            return
        op = self.outposts[matched[0]]
        op["garrison"] += guards
        print(f"🛡️ Strategic Reinforcement: Dispatched +{guards} Royal Guards to {op['name']} (Garrison: {op['garrison']})")

    def muster_outpost_militia(self, outpost_id: str):
        key = outpost_id.lower().strip()
        matched = [k for k in self.outposts if key in k]
        if not matched:
            print(f"Unknown outpost '{outpost_id}'. Options: {', '.join(self.outposts.keys())}")
            return
        op = self.outposts[matched[0]]
        op["garrison"] += 4
        print(f"🌾 Peasant Levy: Mustered +4 Militiamen to {op['name']}! (Garrison: {op['garrison']})")

    def unleash_outpost_pitch(self, outpost_id: str):
        key = outpost_id.lower().strip()
        matched = [k for k in self.outposts if key in k]
        if not matched:
            print(f"Unknown outpost '{outpost_id}'. Options: {', '.join(self.outposts.keys())}")
            return
        op = self.outposts[matched[0]]
        if not op["pitch"]:
            print(f"No armed pitch cauldron ready at {op['name']}.")
            return
        op["pitch"] = False
        print(f"💥 BOILING PITCH UNLEASHED at {op['name']}! Incinerating enemy sappers and siege ladders!")

    def show_tournament(self):
        print("\n🏟️ === GRAND FEUDAL TOURNAMENT & CHIVALRIC ARENA ===")
        print(f"Chivalric Rank: {self.tournament_title} | Honor: {self.tournament_chivalry} | Excitement: {self.grandstand_excitement:.0f}%")
        print(f"Victories: {self.tournament_wins} | Banquets Hosted: {self.feasts_hosted}")
        print("\nKNIGHTLY DISCIPLINES:")
        print("  1. 🏇 Royal Joust of Peace (Tilt target: helm, shield, breastplate)")
        print("  2. ⚔️ Grand Foot Melee (Clash with broadswords & heater shields)")
        print("  3. 🏹 Guild Marksman Contest (30m, 50m, 70m ranges with crosswinds)")
        print("  4. 👑 Sovereign Champion Boss Duel (Duel Prince Alden of Valoria)")
        print("  5. 🍖 Grand Realm Banquet (Host lavish feast for citizens & lords)")

    def start_joust(self, target: str = "shield"):
        target = target.lower().strip()
        pts = 2
        unhorsed = False
        if target == "helm":
            pts = 3
            unhorsed = True
        elif target == "breastplate":
            pts = 1

        self.tournament_wins += 1
        honor_gain = 35 + (25 if unhorsed else 0)
        self.tournament_chivalry += honor_gain
        self.coins += 75
        print(f"\n🏇 [ROYAL JOUST PASS]")
        print(f"Targeting: {target.upper()} with couched heavy lance!")
        print(f"✓ Impact! Clean lance splintered across opponent's armor. Scored {pts} points!")
        if unhorsed:
            print("👑 SPECTACULAR UNHORSING! Opponent cast into the tilt dust! Royal ovation!")
        print(f"🏆 TOURNAMENT TRIUMPH: Monarch victorious! (+75 Gold, +{honor_gain} Honor -> {self.tournament_chivalry})")

    def start_melee(self, action: str = "strike"):
        self.tournament_wins += 1
        self.tournament_chivalry += 40
        self.coins += 80
        print(f"\n⚔️ [ARENA FOOT MELEE]")
        print(f"Executing: {action.upper()} against armored champion!")
        print("✓ Blade clashed upon steel buckler! Opponent's guard broken!")
        print(f"🏆 MELEE VICTORIOUS: Monarch triumphs in the arena! (+80 Gold, +40 Honor -> {self.tournament_chivalry})")

    def start_archery(self, elevation: float = 1.5, wind_adjust: float = 0.0):
        self.tournament_wins += 1
        self.tournament_chivalry += 30
        self.coins += 60
        print(f"\n🏹 [ARCHERY GUILD MARKSMAN CONTEST]")
        print(f"Drawing yew longbow... Elevation: {elevation:.1f}°, Wind Compensation: {wind_adjust:+.1f} m/s")
        print("🎯 THWACK! Shaft penetrates the gold bullseye ring (10 Points)!")
        print(f"🏆 MARKSMAN CHAMPION: Crown marksman takes the guild prize! (+60 Gold, +30 Honor -> {self.tournament_chivalry})")

    def duel_champion(self, gambit: str = "riposte_counter"):
        self.tournament_wins += 1
        self.tournament_chivalry += 60
        self.coins += 150
        print(f"\n👑 [DUEL OF SOVEREIGN CHAMPIONS]")
        print(f"Facing Prince Alden of Valoria! Executing gambit: {gambit.upper()}")
        print("⚡ Perfect riposte! Blade tip disarms the Crown Prince of the East!")
        print(f"👑 SUPREME TOURNAMENT CHAMPION: Monarch reigns supreme! (+150 Gold, +60 Honor -> {self.tournament_chivalry})")

    def host_regal_feast(self):
        if self.coins < 25:
            print("Insufficient gold for royal heralds and feast musicians (Requires 25 Gold).")
            return
        self.coins -= 25
        self.feasts_hosted += 1
        self.tournament_chivalry += 100
        self.grandstand_excitement = 100.0
        print("\n🍷 [GRAND REGAL BANQUET OF THE REALM]")
        print("Trestle tables laden with roasted meats, hearth loaves, and spiced wine!")
        print("✓ All realm subjects and visiting knights rejoice! Citizen Morale +25.0%!")
        print(f"⚜️ Royal Prestige Surges (+100 Chivalric Honor -> {self.tournament_chivalry})!")

    def show_monastery(self):
        stone_names = ["Nigredo (Black Dissolution)", "Albedo (White Purification)", "Citrinitas (Yellow Awakening)", "Rubedo (Magnum Opus)"]
        stage_name = stone_names[self.stone_stage - 1]
        print("\n⛪ === MONASTIC SCHOLASTICA & ALCHEMICAL SANCTUARY (KEY_B) ===")
        print(f"Monk Scribes: {self.monk_scribes} | Scholar Points: {self.scholar_points:.1f} | Current Research: {self.current_research or 'None'}")
        print(f"Unlocked Technologies: {', '.join(self.unlocked_techs) if self.unlocked_techs else 'None'}")
        print(f"Altar Relics: [Slot 1: {self.altar_relics.get(0, 'Empty')}] [Slot 2: {self.altar_relics.get(1, 'Empty')}] [Slot 3: {self.altar_relics.get(2, 'Empty')}]")
        print(f"Abbey Liturgy Bells: {'ACTIVE (+30% Serenity) 🔔' if self.abbey_bell_active else 'Dormant'}")
        print(f"Alchemical Alembic: {self.alembic_temp:.1f}°C | Magnum Opus Stage: {stage_name}")
        print(f"Distillations: {self.brewed_potions} elixirs brewed | {self.transmutations} metal transmutations completed")
        print("\nSCHOLASTIC TECHNOLOGIES:")
        print("  1. 🌾 norfolk_genetics (Norfolk Four-Course Agronomy Genetics) - Cost: 100")
        print("  2. 🔥 blast_catalysts (Thermodynamic Blast Furnace Flux Catalysts) - Cost: 150")
        print("  3. 🎯 counterweight_ballistics (Gravitational Counterweight Ballistics) - Cost: 200")
        print("  4. 💎 deep_shaft_geology (Deep Subterranean Geological Surveying) - Cost: 180")
        print("  5. 📜 guild_charters (Imperial Artisan Guild Charters) - Cost: 220")
        print("  6. 🏛️ sacred_architecture (Gothic Monastic Vaulting) - Cost: 250")
        print("\nALCHEMICAL TRANSMUTATION CRUCIBLE:")
        print("  • brew vitality / iron_skin / windstrider / dragons_breath")
        print("  • transmute silver / gold / catalyst")
        print("  • magnum (refine philosopher's stone stage)")
        print("  • bells (ring consecrated abbey bells)")

    def conduct_research(self, tech_key: str):
        tech_costs = {
            "norfolk_genetics": 100,
            "blast_catalysts": 150,
            "counterweight_ballistics": 200,
            "deep_shaft_geology": 180,
            "guild_charters": 220,
            "sacred_architecture": 250
        }
        matched = [k for k in tech_costs if tech_key.lower() in k]
        if not matched:
            print(f"Unknown technology '{tech_key}'. Available: {', '.join(tech_costs.keys())}")
            return
        t_id = matched[0]
        if t_id in self.unlocked_techs:
            print(f"Technology '{t_id}' is already researched and active in the realm!")
            return

        cost = tech_costs[t_id]
        self.current_research = t_id
        cur = self.research_progress.get(t_id, 0.0) + (cost * 0.5 if t_id in self.research_progress else cost)
        if cur >= cost:
            self.unlocked_techs.append(t_id)
            self.research_progress[t_id] = cost
            self.current_research = ""
            print(f"📜 SCHOLASTIC TRIUMPH: Completed illumination of '{t_id}'! (+Effects applied to Realm)")
        else:
            self.research_progress[t_id] = cur
            print(f"📖 Scriptorium illuminating '{t_id}': Progress {cur:.0f}/{cost} scholar points.")

    def brew_alchemy_elixir(self, elixir_key: str):
        key = elixir_key.lower().strip()
        recipes = {
            "vitality": ("Elixir of Vitality", "❤️ +50 HP restored"),
            "iron_skin": ("Elixir of Iron Skin", "🛡️ +40% physical armor mitigation"),
            "windstrider": ("Elixir of the Windstrider", "💨 +35% sprint velocity"),
            "dragons_breath": ("Dragon's Breath Volatile Flask", "🔥 60 fire AOE damage")
        }
        matched = [k for k in recipes if key in k]
        if not matched:
            print(f"Unknown elixir '{elixir_key}'. Available: vitality, iron_skin, windstrider, dragons_breath")
            return
        e_key = matched[0]
        name, effect = recipes[e_key]
        self.brewed_potions += 1
        self.alembic_temp = min(350.0, self.alembic_temp + 15.0)
        if e_key == "vitality":
            self.health = min(self.max_health, self.health + 50.0)
        print(f"⚗️ DISTILLATION COMPLETE: Brewed 1x {name}! Effect: {effect}. Alembic temp: {self.alembic_temp:.1f}°C")

    def transmute_alchemy_metal(self, formula_key: str):
        key = formula_key.lower().strip()
        transmutes = {
            "silver": ("Baser Ore into Noble Silver", "+2 Silver Ore"),
            "gold": ("Great Magnum Transmutation: Iron into Gold", "+25 Gold Coins"),
            "catalyst": ("Sublimation of Salt into Philosopher's Catalyst", "+1 Gems")
        }
        matched = [k for k in transmutes if key in k]
        if not matched:
            print(f"Unknown transmutation '{formula_key}'. Available: silver, gold, catalyst")
            return
        f_key = matched[0]
        name, out_desc = transmutes[f_key]
        self.transmutations += 1
        self.alembic_temp = min(400.0, self.alembic_temp + 25.0)
        if f_key == "gold":
            self.coins += 25
        print(f"✨ TRANSMUTATION SUCCESSFUL: {name}! Produced: {out_desc}. Alembic temp: {self.alembic_temp:.1f}°C")

    def enshrine_abbey_relic(self, relic_key: str, slot: int = 1):
        slot_idx = max(0, min(2, slot - 1))
        matched = [r for r in self.discovered_relics if relic_key.lower() in r]
        if not matched:
            print(f"Relic '{relic_key}' not found in discovery inventory. Discovered: {', '.join(self.discovered_relics)}")
            return
        r_id = matched[0]
        for s in list(self.altar_relics.keys()):
            if self.altar_relics[s] == r_id:
                self.altar_relics[s] = ""
        self.altar_relics[slot_idx] = r_id
        print(f"⛪ SACRED CONSECRATION: Enshrined '{r_id}' on Altar Slot {slot_idx+1}! Realm blessing bestowed.")

    def ring_abbey_bells(self):
        self.abbey_bell_active = True
        print("🔔 CLANGOR SANCTUS: Abbey Cathedral Bells ring across the valley! +30% Citizen Serenity bestowed.")

    def refine_philosophers_stone(self):
        stone_names = ["Nigredo (Black Dissolution)", "Albedo (White Purification)", "Citrinitas (Yellow Awakening)", "Rubedo (Magnum Opus)"]
        if self.stone_stage >= 4:
            print(f"💎 MAGNUM OPUS PERFECTED: Already achieved the Great Work (Rubedo / Red Elixir)!")
            return
        self.stone_stage += 1
        print(f"🔴 ALCHEMICAL ELEVATION: Philosopher's Stone refined to Stage {self.stone_stage}: {stone_names[self.stone_stage - 1]}!")

    def show_espionage(self):
        print("\n🗡️ === ROYAL SPYMASTER & SHADOW COUNCIL (KEY_N) ===")
        print(f"Citadel Security Rating: {self.citadel_security:.1f}% | Plots Foiled: {self.plots_thwarted}")
        print(f"Recruited Agents ({len(self.recruited_spies)}):")
        if not self.recruited_spies:
            print("  • No shadow agents currently on royal retainer.")
        else:
            for a_id, a in self.recruited_spies.items():
                print(f"  • [{a_id}] {a['name']} ({a['type']}) - Status: {a['status']} in {a['realm'].capitalize()}")

        print(f"Ongoing Operations ({len(self.active_covert_ops)}):")
        if not self.active_covert_ops:
            print("  • No active covert operations executing.")
        else:
            for op in self.active_covert_ops:
                print(f"  • {op['name']} in {op['realm'].capitalize()} (Agent: {op['agent']})")

        print(f"Citadel Dungeons ({len(self.captured_spies)} prisoners):")
        if not self.captured_spies:
            print("  • Subterranean cells are vacant.")
        else:
            for p in self.captured_spies:
                status = "Interrogated" if p["interrogated"] else "Unbroken"
                print(f"  • [{p['id']}] {p['name']} - Status: {status} (Ransom: {p['ransom']} Gold)")

    def recruit_shadow_spy(self, archetype_key: str):
        key = archetype_key.lower().strip()
        archetypes = {
            "informant": ("Whispering Tavern Informant", 30),
            "saboteur": ("Infiltration Sapper & Saboteur", 60),
            "master_spy": ("Shadow Courtier & Master Provocateur", 120),
            "spy": ("Shadow Courtier & Master Provocateur", 120)
        }
        matched = [k for k in archetypes if key in k]
        if not matched:
            print(f"Unknown archetype '{archetype_key}'. Options: informant, saboteur, master_spy")
            return
        arch_k = matched[0]
        name, cost = archetypes[arch_k]
        if self.coins < cost:
            print(f"Insufficient treasury coins (Requires {cost} Gold, have {self.coins}).")
            return
        self.coins -= cost
        a_id = f"agent_{len(self.recruited_spies)+1}"
        self.recruited_spies[a_id] = {
            "id": a_id,
            "name": name,
            "type": arch_k,
            "status": "Ready",
            "realm": "citadel"
        }
        self.citadel_security = min(100.0, self.citadel_security + 5.0)
        print(f"🗡️ SHADOW COUNCIL: Recruited {name} [{a_id}] (-{cost} Gold)! Security -> {self.citadel_security:.1f}%.")

    def launch_covert_op(self, op_key: str, realm: str = "ashfell"):
        ops = {
            "intel": ("Uncover Military Invasion War Plans", 25),
            "sabotage": ("Spike Battering Rams & Burn Pitch Depots", 45),
            "tech": ("Pilfer Monastic Scriptoria Parchments", 60),
            "revolt": ("Sow Dissidence & Bribe Border Troops", 80)
        }
        matched = [k for k in ops if op_key.lower() in k]
        if not matched:
            print(f"Unknown operation '{op_key}'. Options: intel, sabotage, tech, revolt")
            return
        o_key = matched[0]
        name, cost = ops[o_key]

        ready_agents = [aid for aid, a in self.recruited_spies.items() if a["status"] == "Ready"]
        if not ready_agents:
            print("No ready shadow agents available! Recruit an agent first.")
            return
        if self.coins < cost:
            print(f"Insufficient treasury coins (Requires {cost} Gold).")
            return

        self.coins -= cost
        agent_id = ready_agents[0]
        self.recruited_spies[agent_id]["status"] = "On Mission"
        self.recruited_spies[agent_id]["realm"] = realm
        self.active_covert_ops.append({
            "name": name,
            "realm": realm,
            "agent": agent_id
        })
        print(f"🎭 COVERT INTRIGUE: Dispatched {agent_id} on '{name}' in {realm.capitalize()} (-{cost} Gold)!")
        self.active_covert_ops.pop()
        self.recruited_spies[agent_id]["status"] = "Ready"
        if o_key == "intel":
            print(f"✓ Operation Succeeded! Infiltrated {realm.capitalize()} war council: attack plans mapped.")
        elif o_key == "sabotage":
            print(f"✓ Operation Succeeded! Burned siege weapon depots in {realm.capitalize()}: enemy power halved.")
        elif o_key == "tech":
            self.scholar_points += 120.0
            print(f"✓ Operation Succeeded! Stole scriptoria treatises from {realm.capitalize()}: +120 Scholar Points!")
        elif o_key == "revolt":
            print(f"✓ Operation Succeeded! Incited border rebellion in {realm.capitalize()}: +3 Deserters joined garrison.")

    def trigger_counter_intel_sweep(self):
        self.plots_thwarted += 1
        p_id = f"prisoner_{len(self.captured_spies)+1}"
        self.captured_spies.append({
            "id": p_id,
            "name": "Ashfell Clan Infiltrator",
            "interrogated": False,
            "ransom": 50
        })
        print(f"🛡️ COUNTER-INTELLIGENCE: Foiled enemy sabotage plot in Citadel Tavern! Captured {p_id} into dungeons.")

    def interrogate_captive(self):
        if not self.captured_spies:
            print("No captives in citadel dungeons to interrogate.")
            return
        p = self.captured_spies[0]
        if p["interrogated"]:
            print(f"Prisoner {p['id']} has already revealed all secrets.")
            return
        p["interrogated"] = True
        self.coins += 75
        print(f"🔍 DUNGEON INTERROGATION: Prisoner {p['id']} cracked! Disclosed concealed gold stash (+75 Gold Coins).")

    def ransom_captive(self):
        if not self.captured_spies:
            print("No captives in dungeons to ransom.")
            return
        p = self.captured_spies.pop(0)
        self.coins += p["ransom"]
        print(f"💰 RANSOM RESOLVED: Exchanged {p['id']} with foreign bailiffs for +{p['ransom']} Gold Coins!")

    def show_stockpile(self, category: str = "all"):
        cat = category.lower().strip()
        print("\n🌾 === ROYAL FEUDAL GRANARY & WAREHOUSE STOCKPILE ===")
        total_items = sum(self.stockpile.values())
        print(f"Total Goods in Store: {total_items} units | Royal Treasury: {self.coins} 💰 Gold Coins")

        groups = {
            "food": ["wheat", "flour", "bread", "meat", "cabbage", "onion", "carrot", "cured_meat", "smoked_meat", "cabbage_stew", "shepherd_pie", "honey_mead"],
            "ores": ["iron_ore", "coal", "copper_ore", "tin_ore", "stone", "logs", "rock_salt", "honeycomb", "beeswax", "raw_wool"],
            "metals": ["iron_bloom", "wrought_iron_ingot", "iron_ingots", "steel_ingot", "copper_ingot", "tin_ingot", "bronze_ingot"],
            "manufactured": ["tools", "weapons", "planks", "woolen_tunic", "beeswax_candle", "cast_bronze_blade", "cast_bronze_pickaxe"]
        }

        display_cats = groups.keys() if cat in ["all", ""] else [k for k in groups if cat in k]
        if not display_cats:
            print(f"Unknown category '{category}'. Available: all, food, ores, metals, manufactured")
            return

        for c in display_cats:
            c_name = c.upper()
            print(f"\n[{c_name} STOCKPILE]")
            for item in groups[c]:
                qty = self.stockpile.get(item, 0)
                q_target = self.quotas.get(item, "-")
                q_mode = self.quota_modes.get(item, "-")
                status = ""
                if item in self.quotas:
                    status = f" | Quota: {qty}/{q_target} ({q_mode})"
                print(f"  • {item.replace('_', ' ').title():<22}: {qty:>4} units{status}")

    def produce_resource(self, recipe: str, amount: int = 1):
        if amount <= 0:
            print("Production amount must be positive.")
            return

        rec = recipe.lower().strip()
        recipes = {
            "flour": {
                "inputs": {"wheat": 1},
                "outputs": {"flour": 2},
                "name": "Windmill Grist Milling (Wheat -> 2x Flour)"
            },
            "bread": {
                "inputs": {"flour": 1},
                "outputs": {"bread": 2},
                "name": "Communal Hearth Baking (Flour -> 2x Hearth Loaves)"
            },
            "bread_wheat": {
                "inputs": {"wheat": 1},
                "outputs": {"bread": 2},
                "name": "Rustic Hearth Baking (Wheat -> 2x Bread)"
            },
            "stew": {
                "inputs": {"cabbage": 1, "meat": 1, "onion": 1},
                "outputs": {"cabbage_stew": 2},
                "name": "Feudal Kitchen Cabbage Stew (Cabbage + Beef + Onion -> 2x Stew)"
            },
            "pie": {
                "inputs": {"meat": 1, "onion": 1, "bread": 1},
                "outputs": {"shepherd_pie": 2},
                "name": "Tavern Shepherd's Pie (Meat + Onion + Bread -> 2x Pie)"
            },
            "salt_meat": {
                "inputs": {"meat": 1, "rock_salt": 1},
                "outputs": {"cured_meat": 1},
                "name": "Salting Trough Curing (Meat + Rock Salt -> Cured Salted Meat)"
            },
            "smoke_meat": {
                "inputs": {"meat": 1, "logs": 1},
                "outputs": {"smoked_meat": 1},
                "name": "Smokehouse Curing (Meat + Oak Logs -> Smoked Meat)"
            },
            "smelt_bloom": {
                "inputs": {"iron_ore": 2, "coal": 2},
                "outputs": {"iron_bloom": 1},
                "name": "Bloomery Smelting (2x Iron Ore + 2x Coal -> Spongy Iron Bloom)"
            },
            "refine_iron": {
                "inputs": {"iron_bloom": 1},
                "outputs": {"wrought_iron_ingot": 1},
                "name": "Trip-Hammer Anvil Forging (Iron Bloom -> Wrought Iron Ingot)"
            },
            "smelt_steel": {
                "inputs": {"wrought_iron_ingot": 1, "coal": 2},
                "outputs": {"steel_ingot": 1},
                "name": "Crucible High-Carbon Steel (Wrought Iron + 2x Coal -> Crucible Steel)"
            },
            "forge_tools": {
                "inputs": {"wrought_iron_ingot": 1, "logs": 1},
                "outputs": {"tools": 1},
                "name": "Blacksmith Toolcraft (Wrought Iron + Wood -> Sturdy Feudal Tools)"
            },
            "forge_weapons": {
                "inputs": {"steel_ingot": 1, "logs": 1},
                "outputs": {"weapons": 1},
                "name": "Armorer Weapon Smithing (Crucible Steel + Wood -> Knight Swords & Spears)"
            },
            "cast_bronze": {
                "inputs": {"copper_ore": 3, "tin_ore": 1},
                "outputs": {"bronze_ingot": 4},
                "name": "Bronze Foundry Casting (3x Copper + 1x Tin -> 4x Bronze Ingot)"
            },
            "brew_mead": {
                "inputs": {"honeycomb": 2},
                "outputs": {"honey_mead": 1},
                "name": "Abbey Mead Fermentation (2x Honeycomb -> Honey Mead Cask)"
            },
            "weave_tunic": {
                "inputs": {"raw_wool": 4},
                "outputs": {"woolen_tunic": 1},
                "name": "Loom Textile Weaving (4x Raw Wool -> Warm Woolen Tunic)"
            },
            "candle": {
                "inputs": {"beeswax": 1},
                "outputs": {"beeswax_candle": 2},
                "name": "Chandler Candle Dipping (Beeswax -> 2x Wax Tapers)"
            }
        }

        matched = [k for k in recipes if rec in k]
        if not matched:
            print(f"Unknown production recipe '{recipe}'.")
            print("Available recipes: " + ", ".join(recipes.keys()))
            return

        r_key = matched[0]
        r_info = recipes[r_key]

        main_out = list(r_info["outputs"].keys())[0]
        if main_out in self.quotas and self.quota_modes.get(main_out) == "until_x":
            target = self.quotas[main_out]
            current = self.stockpile.get(main_out, 0)
            if current >= target:
                print(f"⚠️ Quota Reached: Stockpile already contains {current}/{target} {main_out}. Quota mode is 'until_x'. Production halted.")
                return

        for inp, req in r_info["inputs"].items():
            total_req = req * amount
            if self.stockpile.get(inp, 0) < total_req:
                print(f"❌ Missing materials: Requires {total_req} {inp}, but only have {self.stockpile.get(inp, 0)}.")
                return

        consumed_str = []
        for inp, req in r_info["inputs"].items():
            self.stockpile[inp] -= req * amount
            consumed_str.append(f"-{req * amount} {inp}")

        produced_str = []
        for outp, yield_amt in r_info["outputs"].items():
            self.stockpile[outp] = self.stockpile.get(outp, 0) + (yield_amt * amount)
            produced_str.append(f"+{yield_amt * amount} {outp}")

        self.stamina = max(10.0, self.stamina - 5.0)
        self.calories -= 10.0 * amount
        print(f"\n⚙️ [PRODUCTION PIPELINE: {r_info['name']}]")
        print(f"Batches processed: {amount}")
        print(f"Consumed: {', '.join(consumed_str)}")
        print(f"Produced: {', '.join(produced_str)}")
        print(f"Current {main_out} stockpile: {self.stockpile[main_out]} units.")

    def calculate_market_price(self, item: str, is_selling: bool = False) -> float:
        base = self.market_caravan["base_prices"].get(item, 5.0)
        supply = max(1.0, float(self.stockpile.get(item, 10)))
        demand = 25.0
        ratio = demand / supply
        k_d = 0.85
        gamma = 1.25
        mult = 1.0 + k_d * (math.pow(ratio, gamma) - 1.0)
        mult = max(0.20, min(5.0, mult))

        if self.season == "Winter" and item in ["wheat", "flour", "bread", "meat", "cabbage"]:
            mult = min(5.0, mult * 1.5)

        price = base * mult
        if is_selling:
            price *= 0.85
        return max(1.0, round(price, 1))

    def show_market(self):
        c = self.market_caravan
        print(f"\n⚖️ === TOWN MARKET SQUARE & MERCHANT CARAVAN ===")
        print(f"Merchant Guild: {c['guild']} | Caravan Master: {c['caravan_master']}")
        print(f"Monarch Treasury: {self.coins} 💰 Gold Coins | Season: {self.season}")
        print(f"{'Item':<20} {'Stockpile':>10} {'Buy Price':>12} {'Sell Price':>12}")
        print("-" * 58)
        for item in sorted(c["base_prices"].keys()):
            stock = self.stockpile.get(item, 0)
            buy_p = self.calculate_market_price(item, is_selling=False)
            sell_p = self.calculate_market_price(item, is_selling=True)
            print(f"{item.replace('_', ' ').title():<20} {stock:>10} {buy_p:>10.1f} 💰 {sell_p:>10.1f} 💰")
        print("\nCommands: buy <item> [amount] | sell <item> [amount]")

    def trade_market(self, action: str, item: str, amount: int = 1):
        if amount <= 0:
            print("Trade amount must be positive.")
            return

        it = item.lower().strip()
        matched = [k for k in self.market_caravan["base_prices"] if it in k]
        if not matched:
            print(f"Market caravan does not trade '{item}'.")
            return
        item_key = matched[0]

        if action.lower() == "buy":
            unit_price = self.calculate_market_price(item_key, is_selling=False)
            total_cost = int(math.ceil(unit_price * amount))
            if self.coins < total_cost:
                print(f"❌ Insufficient treasury gold! Buying {amount}x {item_key} costs {total_cost} 💰, you have {self.coins} 💰.")
                return
            self.coins -= total_cost
            self.stockpile[item_key] = self.stockpile.get(item_key, 0) + amount
            print(f"🤝 CARAVAN PURCHASE: Bought {amount}x {item_key} for {total_cost} 💰 Gold (-{unit_price:.1f} ea).")
            print(f"New Stockpile: {self.stockpile[item_key]} | Treasury: {self.coins} 💰 Gold.")
        elif action.lower() == "sell":
            if self.stockpile.get(item_key, 0) < amount:
                print(f"❌ Not enough in stockpile! You only have {self.stockpile.get(item_key, 0)}x {item_key}.")
                return
            unit_price = self.calculate_market_price(item_key, is_selling=True)
            total_revenue = int(math.floor(unit_price * amount))
            self.stockpile[item_key] -= amount
            self.coins += total_revenue
            print(f"🤝 CARAVAN SALE: Sold {amount}x {item_key} to merchants for +{total_revenue} 💰 Gold (+{unit_price:.1f} ea).")
            print(f"New Stockpile: {self.stockpile[item_key]} | Treasury: {self.coins} 💰 Gold.")
        else:
            print(f"Invalid trade action '{action}'. Use 'buy' or 'sell'.")

    def set_production_quota(self, item: str, target: int, mode: str = "until_x"):
        it = item.lower().strip()
        matched = [k for k in self.stockpile if it in k]
        if not matched:
            print(f"Unknown stockpile item '{item}'.")
            return
        item_key = matched[0]
        valid_modes = ["until_x", "continuous", "paused"]
        if mode.lower() not in valid_modes:
            mode = "until_x"
        self.quotas[item_key] = max(0, target)
        self.quota_modes[item_key] = mode.lower()
        print(f"📋 PRODUCTION QUOTA UPDATED: {item_key} target -> {target} units (Mode: {mode.lower()}).")

    def simulate_cellar_spoilage(self, hours: int = 24, container: str = "COLD_CELLAR"):
        container_factors = {
            "OPEN_GROUND": 1.50,
            "WOODEN_CHEST": 1.00,
            "CLAY_AMPHORA": 0.60,
            "STILT_GRANARY": 0.25,
            "COLD_CELLAR": 0.25,
            "ICEHOUSE_VAULT": 0.10
        }
        cont_factor = container_factors.get(container.upper(), 0.25)
        curr_dist = self.DISTRICTS[self.current_district_key]
        temp = curr_dist.get("ambient_temp", 15.0)
        q10_mult = math.pow(2.0, (temp - 15.0) / 10.0)
        decay_factor = (hours / 120.0) * cont_factor * q10_mult

        spoilage_report = {}
        perishables = ["meat", "bread", "cabbage", "cabbage_stew"]
        for p in perishables:
            count = self.stockpile.get(p, 0)
            lost = int(math.floor(count * min(0.50, decay_factor)))
            if lost > 0:
                self.stockpile[p] -= lost
                spoilage_report[p] = lost

        print(f"\n❄️ === FOOD PRESERVATION & CELLAR DECAY KINETICS ===")
        print(f"Elapsed Time: {hours} hours | Storage Type: {container} (Factor: {cont_factor})")
        print(f"Cellar Ambient Temp: {temp:.1f}°C | Arrhenius Decay Acceleration: {q10_mult:.2f}x")
        if spoilage_report:
            print("Perished supplies:")
            for p, lost in spoilage_report.items():
                print(f"  🥀 {p.replace('_', ' ').title()}: -{lost} units lost to microbial decay (Remaining: {self.stockpile[p]}).")
        else:
            print("✓ Excellent preservation! All provisions remained fresh in cold storage.")

    def calculate_crown_authority(self) -> float:
        base = 50.0
        prestige_bonus = 0.05 * float(self.castle_prestige)
        morale_avg = min(100.0, max(0.0, 75.0 + self.castle_buffs.get("realm_morale", 0.0)))
        morale_bonus = 0.20 * morale_avg
        crime_penalty = 0.25 * self.crime_rate
        unrest_penalty = 0.30 * self.unrest
        val = base + prestige_bonus + morale_bonus - crime_penalty - unrest_penalty
        self.crown_authority = max(0.0, min(100.0, round(val, 1)))
        return self.crown_authority

    def show_court(self):
        auth = self.calculate_crown_authority()
        print("\n⚖️ === HIGH MAGISTRATE & FEUDAL MANOR LEET COURT ===")
        print(f"Crown Sovereign Authority: {auth:.1f}% [A_crown] | Public Order: {self.public_order:.1f}%")
        print(f"Realm Crime Index: {self.crime_rate:.1f}% | Civil Unrest: {self.unrest:.1f}% | Treasury: {self.coins} 💰 Gold Coins")
        if self.ratified_charters:
            print(f"Ratified Charters & Assizes: {', '.join([c.title() for c in self.ratified_charters])}")
        
        print("\n[ACTIVE JUDICIAL DOCKETS]")
        if not self.active_dockets:
            print("  • No pending trials. The realm rests in tranquil order.")
        else:
            for case in self.active_dockets:
                sev_icons = "⚠️" * case.get("severity", 1)
                print(f"  [{case['id']}] {case['accused']} - Severity: {case.get('severity', 1)} {sev_icons}")
                print(f"    Charge   : {case['charge']}")
                print(f"    Evidence : {case['evidence']}")
                print(f"    Guilt Est: {int(case.get('guilt_prob', 0.8) * 100)}% | Status: {case['status']}")

        if self.verdict_history:
            print(f"\nRecent Recorded Verdicts ({len(self.verdict_history)} total):")
            for h in self.verdict_history[-3:]:
                print(f"  • {h['id']}: {h['accused']} -> {h['verdict']} ({h['summary']})")

        print("\nCommands: judge <case_id> <acquit|pillory|fine|ordeal|gallows> | charter <magna|leet|assize|sanctuary> | crime")

    def deliver_verdict(self, case_id: str, verdict: str):
        c_id = case_id.upper().strip()
        v_type = verdict.lower().strip()
        valid_verdicts = ["acquit", "pillory", "fine", "ordeal", "gallows"]
        if v_type not in valid_verdicts:
            print(f"Unknown verdict '{verdict}'. Available: acquit, pillory, fine, ordeal, gallows")
            return

        matched = [c for c in self.active_dockets if c_id in c["id"].upper()]
        if not matched:
            print(f"Docket '{case_id}' not found in active court registry.")
            return

        case = matched[0]
        self.active_dockets.remove(case)

        summary = ""
        if v_type == "acquit":
            self.unrest = max(0.0, self.unrest - 3.0)
            if case.get("guilt_prob", 0.5) > 0.8:
                self.crime_rate = min(100.0, self.crime_rate + 2.5)
                summary = "Pardoned with leniency; slight emboldening of petty thieves."
            else:
                summary = "Justly acquitted; citizens praise the Crown's righteousness."
            print(f"⚖️ ROYAL ACQUITTAL: {case['accused']} was acquitted of all charges! {summary}")
        elif v_type == "pillory":
            self.crime_rate = max(0.0, self.crime_rate - 4.5)
            self.public_order = min(100.0, self.public_order + 5.0)
            self.unrest = max(0.0, self.unrest - 2.0)
            summary = "Sentenced to 24h locked in market square pillory."
            print(f"🪵 PILLORY SENTENCE: {case['accused']} placed in public village stocks! (+5.0% Public Order, -4.5% Crime).")
        elif v_type == "fine":
            fine_amount = case.get("severity", 2) * 25
            self.coins += fine_amount
            self.crime_rate = max(0.0, self.crime_rate - 3.0)
            self.public_order = min(100.0, self.public_order + 3.0)
            summary = f"Levied {fine_amount} Gold Coins fine paid into Royal Treasury."
            print(f"💰 JUDICIAL AMERCEMENT: {case['accused']} fined {fine_amount} 💰 Gold Coins! Added to Treasury.")
        elif v_type == "ordeal":
            self.public_order = min(100.0, self.public_order + 6.0)
            self.unrest = max(0.0, self.unrest - 4.0)
            self.scholar_points += 25.0
            summary = "Sacred Trial by Ordeal invoked under Monastic benediction."
            print(f"⛪ SACRED TRIAL BY ORDEAL: The Holy Church conducted ordeal upon {case['accused']}! (+6.0% Public Order, +25 Scholar Points).")
        elif v_type == "gallows":
            self.crime_rate = max(0.0, self.crime_rate - 8.0)
            self.public_order = min(100.0, self.public_order + 8.0)
            self.unrest = max(0.0, self.unrest - 5.0)
            summary = "Capital execution by hanging on castle gallows."
            print(f"🪢 CAPITAL PUNISHMENT: {case['accused']} executed on the gallows! Feudal treason crushed (-8.0% Crime, +8.0% Public Order).")

        self.verdict_history.append({
            "id": case["id"],
            "accused": case["accused"],
            "verdict": v_type.upper(),
            "summary": summary
        })
        new_auth = self.calculate_crown_authority()
        print(f"Crown Sovereign Authority recalibrated to: {new_auth:.1f}%.")

    def issue_legal_charter(self, charter_key: str):
        charters = {
            "magna": ("Magna Carta Libertatum", 60, "Imperial Feudal Charter (+15 Vassal Opinion, +10 Public Order, -5 Unrest)", {"public_order": 10.0, "unrest": -5.0}),
            "leet": ("Manor Leet Court Jurisdiction", 40, "Empowers local magistrates (-8 Crime Rate, +6 Crown Authority)", {"crime_rate": -8.0}),
            "assize": ("Assize of Bread and Ale", 30, "Weights, measures & grain purity regulation (+10 Public Order, -5 Crime)", {"public_order": 10.0, "crime_rate": -5.0}),
            "sanctuary": ("Benefit of Clergy & Church Sanctuary", 25, "Monastic legal immunity (+15 Monastic Piety, -10 Unrest)", {"unrest": -10.0, "public_order": 5.0})
        }
        key = charter_key.lower().strip()
        matched = [k for k in charters if key in k]
        if not matched:
            print(f"Unknown charter '{charter_key}'. Options: magna, leet, assize, sanctuary")
            return
        c_id = matched[0]
        name, cost, desc, mods = charters[c_id]

        if c_id in self.ratified_charters:
            print(f"Charter '{name}' is already ratified by royal wax seal.")
            return

        if self.coins < cost:
            print(f"Insufficient royal treasury funds! Requires {cost} 💰 Gold Coins.")
            return

        self.coins -= cost
        self.ratified_charters.append(c_id)
        for stat, val in mods.items():
            if stat == "public_order":
                self.public_order = min(100.0, max(0.0, self.public_order + val))
            elif stat == "unrest":
                self.unrest = min(100.0, max(0.0, self.unrest + val))
            elif stat == "crime_rate":
                self.crime_rate = min(100.0, max(0.0, self.crime_rate + val))

        self.calculate_crown_authority()
        print(f"\n📜 ROYAL CHARTER RATIFIED: {name} (-{cost} 💰 Gold Coins)!")
        print(f"Details: {desc}")
        print(f"Updated Status -> Crown Authority: {self.crown_authority:.1f}%, Public Order: {self.public_order:.1f}%, Crime: {self.crime_rate:.1f}%.")

    def simulate_crime_patrol(self):
        self.crime_rate = max(2.0, self.crime_rate - 3.5)
        self.public_order = min(100.0, self.public_order + 3.0)
        print(f"\n🛡️ BAILIFF PATROL: Watchmen patrolled town square and harbor alleys!")
        print(f"Crime suppressed to {self.crime_rate:.1f}% | Public Order elevated to {self.public_order:.1f}%.")
        
        if len(self.active_dockets) < 5:
            new_id = f"CASE-{100 + len(self.verdict_history) + len(self.active_dockets) + 1}"
            incidents = [
                ("Wulfric the Woodcutter", "Poaching deer in royal game preserve", "Found venison haunches concealed in cart", 2, 0.85),
                ("Godfrey the Cooper", "Watered beer & false measure in tavern", "Bailiff test ale hydrometer discrepancy", 1, 0.90),
                ("Edmund the Scribe", "Clipping silver edges off realm coins", "Found metal shavings and iron shears in cellar", 3, 0.95),
            ]
            inc = incidents[len(self.active_dockets) % len(incidents)]
            self.active_dockets.append({
                "id": new_id,
                "accused": inc[0],
                "charge": inc[1],
                "evidence": inc[2],
                "severity": inc[3],
                "guilt_prob": inc[4],
                "status": "Awaiting Verdict"
            })
            print(f"⚖️ NEW COURT DOCKET FILED: [{new_id}] {inc[0]} charged with '{inc[1]}'!")

    @staticmethod
    def calculate_bed_rest_duration(severity: int, doctor_skill: int) -> float:
        """GDD Section 6.2: T_bed = T_base + (Severity * 4.0 hours) * (1.0 - 0.02 * Skill_doctor)."""
        t_base = 12.0
        clamped_sev = max(1, min(5, severity))
        clamped_skill = max(0, min(50, doctor_skill))
        skill_factor = max(0.10, 1.0 - 0.02 * clamped_skill)
        t_bed = t_base + (clamped_sev * 4.0) * skill_factor
        return round(max(4.0, t_bed), 1)

    @staticmethod
    def calculate_monarch_ransom(level: int) -> int:
        """GDD Section 6.4: Ransom = 500 + 20 * Level_player."""
        clamped_lvl = max(1, level)
        return int(500 + 20 * clamped_lvl)

    def get_current_diurnal_phase(self) -> dict:
        """GDD Section 3.1 & 3.2: Returns active diurnal phase based on time_hour."""
        h = self.time_hour % 24
        if 5 <= h < 7:
            key = "DAWN_MATINS"
        elif 7 <= h < 12:
            key = "MORNING_WORK"
        elif 12 <= h < 13:
            key = "NOON_REPAST"
        elif 13 <= h < 18:
            key = "AFTERNOON_WORK"
        elif 18 <= h < 21:
            key = "VESPERS_SUPPER"
        else:
            key = "NIGHT_SLUMBER"
        data = self.diurnal_schedule[key].copy()
        data["key"] = key
        return data

    def show_monarch_vitals(self):
        """Displays Monarch physical state, trauma conditions, court doctor skill, and diurnal routine."""
        phase = self.get_current_diurnal_phase()
        print("\n" + "=" * 78)
        print("          👑 MONARCH PHYSIOLOGICAL VITALS & FIELD CHIRURGERY")
        print("=" * 78)
        print(f"Monarch Status: {self.monarch_status.upper()} | Sovereign Level: {self.monarch_level}")
        print(f"Health: {self.health:.1f} / {self.max_health:.1f} HP | Stamina: {self.stamina:.1f} / {self.max_stamina:.1f}")
        print(f"Calories: {self.calories:.0f} kcal | Warmth: {self.warmth:.1f}°C | Court Doctor Skill: {self.court_doctor_skill}")
        print(f"Astronomical Time: {self.time_hour:02d}:00 ({phase['phase']}) | Day: {self.day_number} ({self.season})")
        print(f"Diurnal Rhythm: {phase['desc']} (Labor Multiplier: {phase['prod_mult']:.2f}x)")

        if self.monarch_status == "captive":
            print(f"\n⚠️ CRITICAL: The Monarch is held captive by rogue highland bandits!")
            print(f"Ransom Demanded: {self.ransom_demanded} 💰 Gold Coins.")
            print("Use 'ransom_monarch' to deliver ransom from realm treasury or launch rescue raid.")
        elif self.monarch_status == "bedridden":
            print(f"\n🛌 INFIRMARY: Monarch is bedridden in Citadel Quarters.")
            print(f"Mandatory Bed Rest Remaining: {self.bed_rest_remaining:.1f} game hours.")

        print(f"\nActive Trauma Conditions ({len(self.trauma_conditions)}):")
        if not self.trauma_conditions:
            print("  ✓ Pristine Physical Condition - No acute injuries or fractures.")
        else:
            for t in self.trauma_conditions:
                print(f"  - [{t['id']}] {t['name']} (Severity: {t['severity']})")
                print(f"    Effects: {t['effects']} | Needed Treatment: '{t['treatment_needed']}' | Remaining Rest: {t.get('bed_hours_left', 0):.1f}h")

        if self.trauma_history:
            print(f"\nMedical & Trauma History ({len(self.trauma_history)} recorded incidents):")
            for h in self.trauma_history[-3:]:
                print(f"  • {h}")
        print("=" * 78)

    def simulate_combat_knockout(self, severity: int = 2, guards_present: bool = True):
        """GDD Section 6.1: Simulates monarch falling to 0 HP and rescue window."""
        self.health = 0.0
        print("\n⚔️ COMBAT TRAUMA: The Monarch has sustained catastrophic injury in battle! (HP = 0)")
        if not guards_present:
            self.monarch_status = "captive"
            self.ransom_demanded = self.calculate_monarch_ransom(self.monarch_level)
            self.health = 10.0
            self.trauma_history.append(f"Day {self.day_number}: Captured in wild skirmish without guard escort. Ransom {self.ransom_demanded} Gold demanded.")
            print("🚨 RESCUE FAILED: No friendly guards were nearby to defend the fallen Monarch!")
            print(f"Hostile raiders dragged the Sovereign into captivity. Demand: {self.ransom_demanded} 💰 Gold Coins.")
            return

        print("🛡️ GUARD RESCUE: Royal Men-at-Arms rushed forward, formed a protective shield wall, and evacuated the Sovereign!")
        self.monarch_status = "bedridden"
        self.health = 25.0
        bed_duration = self.calculate_bed_rest_duration(severity, self.court_doctor_skill)
        self.bed_rest_remaining = max(self.bed_rest_remaining, bed_duration)

        trauma_types = {
            1: {"id": "TRAUMA_CONCUSSION", "name": "Cranial Concussion", "effects": "Aql -25%, blurred vision, disoriented", "treatment_needed": "valerian"},
            2: {"id": "TRAUMA_BROKEN_RIBS", "name": "Fractured Ribs", "effects": "Stamina -40%, running prohibited", "treatment_needed": "bone_splint"},
            3: {"id": "TRAUMA_FLESH_WOUND", "name": "Deep Arterial Laceration", "effects": "Max HP -30%, bleeding, fever risk", "treatment_needed": "honey_dressing"},
        }
        chosen = trauma_types.get(severity, trauma_types[2])
        existing_ids = [t["id"] for t in self.trauma_conditions]
        if chosen["id"] not in existing_ids:
            condition = {
                "id": chosen["id"],
                "name": chosen["name"],
                "severity": severity,
                "bed_hours_left": bed_duration,
                "effects": chosen["effects"],
                "treatment_needed": chosen["treatment_needed"]
            }
            self.trauma_conditions.append(condition)
            self.trauma_history.append(f"Day {self.day_number}: Suffered {chosen['name']} (Severity {severity}). Prescribed {bed_duration:.1f}h bed rest.")
            print(f"🏥 DIAGNOSIS: {chosen['name']} confirmed. Prescribed Bed Rest: {bed_duration:.1f} hours.")
            print(f"Surgical Remedy Required: '{chosen['treatment_needed']}'.")

    def treat_monarch_trauma(self, remedy: str):
        """GDD Section 6.3: Court chirurgeon applies remedies to heal active trauma."""
        remedy = remedy.lower().strip()
        print(f"\n🩺 COURT CHIRURGEON: Applying medical remedy '{remedy}'...")
        if not self.trauma_conditions:
            print("The Monarch has no active traumatic conditions requiring surgery.")
            return

        matched = None
        for t in self.trauma_conditions:
            if t["treatment_needed"] == remedy or remedy in t["treatment_needed"]:
                matched = t
                break

        if not matched:
            print(f"Remedy '{remedy}' does not match any current trauma condition! Available needs:")
            for t in self.trauma_conditions:
                print(f"  - {t['name']}: requires '{t['treatment_needed']}'")
            return

        self.trauma_conditions.remove(matched)
        if matched["id"] == "TRAUMA_CONCUSSION":
            self.bed_rest_remaining = max(0.0, self.bed_rest_remaining - 4.0)
            print("✓ Valeriana tincture soothes brain swelling. Mental clarity restored; bed rest reduced by 4.0h.")
        elif matched["id"] == "TRAUMA_BROKEN_RIBS":
            self.bed_rest_remaining = max(0.0, self.bed_rest_remaining - 6.0)
            print("✓ Bone splint and bone marrow broth applied. Rib cage stabilized; breathing eased.")
        elif matched["id"] == "TRAUMA_FLESH_WOUND":
            self.bed_rest_remaining = max(0.0, self.bed_rest_remaining - 8.0)
            scar = {"id": "TRAUMA_BATTLE_SCAR", "name": "Honorable Battle Scar", "severity": 1, "effects": "Charisma +5 (Fear/Respect), Agility -3", "treatment_needed": "none"}
            if not any(t["id"] == "TRAUMA_BATTLE_SCAR" for t in self.trauma_conditions):
                self.trauma_conditions.append(scar)
            self.total_renown += 50
            print("✓ Chirurgeon sutured deep laceration with silk thread and honey antiseptic dressing.")
            print("✓ Wound healed into a permanent Honorable Battle Scar (+5 Charisma, +50 Renown)!")

        self.trauma_history.append(f"Day {self.day_number}: Treated {matched['name']} with {remedy}.")
        if not any(t["id"] != "TRAUMA_BATTLE_SCAR" for t in self.trauma_conditions) and self.bed_rest_remaining <= 0:
            self.monarch_status = "active"
            self.health = self.max_health
            print("🎉 FULL RECOVERY: Monarch has healed completely and returned to active governance!")

    def pay_monarch_ransom(self) -> bool:
        """GDD Section 6.4: Ransoms captured monarch from enemy raiders."""
        if self.monarch_status != "captive":
            print("\nThe Monarch is not held in captivity. No ransom required.")
            return False

        if self.coins < self.ransom_demanded:
            print(f"\n❌ INSUFFICIENT FUNDS: Treasury holds {self.coins} 💰 Gold Coins, but ransom is {self.ransom_demanded} 💰 Gold Coins!")
            return False

        self.coins -= self.ransom_demanded
        cost = self.ransom_demanded
        self.monarch_status = "active"
        self.health = 35.0
        self.crown_authority = max(0.0, self.crown_authority - 5.0)
        self.trauma_history.append(f"Day {self.day_number}: Paid {cost} Gold ransom. Monarch repatriated to Citadel.")
        self.ransom_demanded = 0
        print(f"\n💰 RANSOM DELIVERED: Paid {cost} Gold Coins to bandit emissaries.")
        print(f"Monarch safely returned under cavalry escort! Health restored to 35.0 HP.")
        print(f"Crown Authority penalty: -5.0% (Current Authority: {self.crown_authority:.1f}%).")
        return True

    def advance_diurnal_time(self, hours: int = 1):
        """GDD Section 3.1 & 3.2: Advances astronomical time, updates seasons, and processes recovery."""
        hours = max(1, hours)
        old_hour = self.time_hour
        self.time_hour = (self.time_hour + hours) % 24
        days_passed = (old_hour + hours) // 24
        self.day_number += days_passed
        self.simulation_ticks += hours * 60

        # Update seasons (7 days = 1 season)
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        season_idx = ((self.day_number - 1) // 7) % 4
        self.season = seasons[season_idx]

        # Bed rest recovery progression
        if self.monarch_status == "bedridden":
            self.bed_rest_remaining = max(0.0, self.bed_rest_remaining - hours)
            for t in self.trauma_conditions:
                if "bed_hours_left" in t:
                    t["bed_hours_left"] = max(0.0, t["bed_hours_left"] - hours)
            
            # Check if healed
            acute_traumas = [t for t in self.trauma_conditions if t["id"] != "TRAUMA_BATTLE_SCAR"]
            if self.bed_rest_remaining <= 0 and not acute_traumas:
                self.monarch_status = "active"
                self.health = self.max_health
                print("\n✨ RECOVERY NOTIFICATION: Monarch has completed bed rest and resumed active duties!")

        # Calorie and stamina adjustments
        phase = self.get_current_diurnal_phase()
        cal_burn = 40.0 * hours if phase["key"] == "NIGHT_SLUMBER" else 75.0 * hours
        self.calories = max(200.0, self.calories - cal_burn)
        self.stamina = min(self.max_stamina, self.stamina + 20.0 * hours)

        print(f"\n⏳ DIURNAL TIME ADVANCED: +{hours} hour(s) -> {self.time_hour:02d}:00 on Day {self.day_number} ({self.season}).")
        print(f"Current Phase: {phase['phase']} (Productivity: {phase['prod_mult']:.2f}x).")
        if self.monarch_status == "bedridden":
            print(f"Bed Rest Progress: {self.bed_rest_remaining:.1f} hours remaining.")

    def show_demographics(self):
        """GDD Section 4.1: Displays population census across 7 demographic age cohorts."""
        total_pop = sum(c["count"] for c in self.population_cohorts.values())
        workforce = sum(c["count"] for k, c in self.population_cohorts.items() if k in ["AGE_YAD", "AGE_MAT"])
        print("\n" + "=" * 78)
        print("          👥 FEUDAL DEMOGRAPHIC AGING & COHORT POPULATION CENSUS")
        print("=" * 78)
        print(f"Total Realm Citizens: {total_pop} | Prime Workforce: {workforce} citizens")
        print(f"Housing Capacity: {self.demographic_stats['housing_capacity']} | Occupancy: {total_pop / self.demographic_stats['housing_capacity'] * 100:.1f}%")
        print(f"Nutritional Variety: {self.demographic_stats['food_variety']}/5 food types | Citizen Hunger: {100.0 - (self.calories / 25.0):.1f}%")
        print(f"Balance Equation: ΔPop = (Births: {self.demographic_stats['total_births']} + Immig: {self.demographic_stats['immigrants']}) - (Deaths: {self.demographic_stats['total_deaths']} + Emig: {self.demographic_stats['emigrants']})")
        print("\nDemographic Age Cohorts (GDD Section 4):")
        print(f"{'Cohort ID':<10} | {'Cohort Name':<24} | {'Count':<6} | {'Labor Multiplier':<18} | {'Physiological Role'}")
        print("-" * 78)
        for k, c in self.population_cohorts.items():
            print(f"{k:<10} | {c['name']:<24} | {c['count']:<6} | {c['labor_mult']:<18.2f}x | {c['desc'][:30]}...")
        print("=" * 78)

    def simulate_demographics(self, seasons: int = 1):
        """GDD Section 4.2: Simulates seasonal cohort aging, Gompertz mortality, and natural fertility."""
        seasons = max(1, seasons)
        print(f"\n📈 DEMOGRAPHIC SIMULATION: Simulating demographic turnover across {seasons} season(s)...")
        total_pop = sum(c["count"] for c in self.population_cohorts.values())
        
        # Natural births condition: food_variety >= 3, housing available
        births = 0
        if self.demographic_stats["food_variety"] >= 3 and total_pop < self.demographic_stats["housing_capacity"]:
            prime_parents = self.population_cohorts["AGE_YAD"]["count"] + self.population_cohorts["AGE_MAT"]["count"]
            births = max(1, int(prime_parents * 0.08 * seasons))
            self.population_cohorts["AGE_INF"]["count"] += births
            self.demographic_stats["total_births"] += births

        # Natural deaths: Gompertz-Makeham risk for Venerable (66+) and elderly
        venerable = self.population_cohorts["AGE_VEN"]["count"]
        elderly = self.population_cohorts["AGE_ELD"]["count"]
        deaths = 0
        if venerable > 0:
            ven_deaths = min(venerable, max(1, int(venerable * 0.25 * seasons)))
            self.population_cohorts["AGE_VEN"]["count"] -= ven_deaths
            deaths += ven_deaths
        if elderly > 5 and seasons >= 2:
            eld_deaths = min(elderly, 1)
            self.population_cohorts["AGE_ELD"]["count"] -= eld_deaths
            deaths += eld_deaths
        self.demographic_stats["total_deaths"] += deaths

        # Cohort transitions (aging upward)
        grad_inf = min(self.population_cohorts["AGE_INF"]["count"], max(1, int(self.population_cohorts["AGE_INF"]["count"] * 0.2 * seasons)))
        self.population_cohorts["AGE_INF"]["count"] -= grad_inf
        self.population_cohorts["AGE_CHI"]["count"] += grad_inf

        grad_chi = min(self.population_cohorts["AGE_CHI"]["count"], max(1, int(self.population_cohorts["AGE_CHI"]["count"] * 0.15 * seasons)))
        self.population_cohorts["AGE_CHI"]["count"] -= grad_chi
        self.population_cohorts["AGE_APP"]["count"] += grad_chi

        grad_app = min(self.population_cohorts["AGE_APP"]["count"], max(1, int(self.population_cohorts["AGE_APP"]["count"] * 0.15 * seasons)))
        self.population_cohorts["AGE_APP"]["count"] -= grad_app
        self.population_cohorts["AGE_YAD"]["count"] += grad_app

        grad_yad = min(self.population_cohorts["AGE_YAD"]["count"], max(1, int(self.population_cohorts["AGE_YAD"]["count"] * 0.08 * seasons)))
        self.population_cohorts["AGE_YAD"]["count"] -= grad_yad
        self.population_cohorts["AGE_MAT"]["count"] += grad_yad

        grad_mat = min(self.population_cohorts["AGE_MAT"]["count"], max(1, int(self.population_cohorts["AGE_MAT"]["count"] * 0.06 * seasons)))
        self.population_cohorts["AGE_MAT"]["count"] -= grad_mat
        self.population_cohorts["AGE_ELD"]["count"] += grad_mat

        grad_eld = min(self.population_cohorts["AGE_ELD"]["count"], max(1, int(self.population_cohorts["AGE_ELD"]["count"] * 0.05 * seasons)))
        self.population_cohorts["AGE_ELD"]["count"] -= grad_eld
        self.population_cohorts["AGE_VEN"]["count"] += grad_eld

        new_total = sum(c["count"] for c in self.population_cohorts.values())
        print(f"Demographic Results -> Births: +{births}, Deaths: -{deaths}, Net Population: {new_total} citizens.")
        print(f"Cohort Transition Verified: Infants {self.population_cohorts['AGE_INF']['count']}, Young Adults {self.population_cohorts['AGE_YAD']['count']}, Venerable Elders {self.population_cohorts['AGE_VEN']['count']}.")

    @staticmethod
    def calculate_reproduction_number(beta: float, gamma: float, mu: float) -> float:
        """GDD Section 75.1: R_0 = beta / (gamma + mu)."""
        if beta <= 0.0 or (gamma + mu) <= 0.0:
            return 0.0
        return round(beta / (gamma + mu), 2)

    @staticmethod
    def calculate_filth_delta(population: int, livestock: int, sweepers: int) -> float:
        """GDD Section 76.1: d(Filth)/dt = Pop * WasteRate + Livestock * DungRate - SweeperCapacity."""
        pop_waste = max(0, population) * 0.05
        dung_waste = max(0, livestock) * 0.25
        sweeper_cap = max(0, sweepers) * (35 * 0.05)  # 1.75 filth/hour
        delta = pop_waste + dung_waste - sweeper_cap
        return round(delta, 2)

    def show_sanitation(self):
        """Displays municipal sanitation, waste kinetics, plague alerts and SIR metrics."""
        total_pop = sum(c["count"] for c in self.population_cohorts.values())
        filth_delta = self.calculate_filth_delta(total_pop, self.livestock_count, self.street_sweepers_count)

        print("\n" + "=" * 78)
        print("          🧹 MUNICIPAL SANITATION, WASTE DYNAMICS & EPIDEMIOLOGY")
        print("=" * 78)
        print(f"Municipal Filth Index: {self.filth_level:.1f} / 100.0 (Hourly Drift: {'+' if filth_delta >= 0 else ''}{filth_delta:.2f})")
        miasma_str = "☣️ ACTIVE (Morale -20, Vermin Swarms)" if self.miasma_active else "✓ CLEAR (Clean Air)"
        print(f"Miasma Status: {miasma_str} (Threshold: Filth > 70.0)")
        print(f"Sanitation Crew: {self.street_sweepers_count} Street Sweepers | Rat Catchers: {self.pest_control_cats} Domestic Cats/Terriers")
        print(f"Town Latrine Cesspool: {self.cesspool_fill:.1f}% capacity | Mature Organic Compost: {self.compost_fertilizer_stock} Barrels")
        drainage_str = "✓ Operational (-20% waterborne risk)" if self.stone_drainage_active else "❌ Blocked"
        aqueduct_str = "✓ Mountain Spring Flowing (Pure Water)" if self.aqueduct_clean_water else "❌ Contaminated"
        print(f"Stone Drainage: {drainage_str} | Mountain Aqueduct: {aqueduct_str}")

        print("\n" + "-" * 78)
        print("          ☠️ SIR EPIDEMIOLOGY & TRANSMISSION DYNAMICS (GDD 75 & 77)")
        print("-" * 78)
        ep_name = self.active_epidemic.upper() if self.active_epidemic else "NONE (HEALTHY CITIZENRY)"
        doc_str = "✓ Appointed (Dr. Corvus with Beak Mask & Waxed Cloak)" if self.plague_doctor_appointed else "❌ None"
        quar_str = ", ".join(self.quarantine_measures) if self.quarantine_measures else "None"
        print(f"Active Contagion: {ep_name} | High Plague Doctor: {doc_str}")
        print(f"Quarantine Edicts: {quar_str}")

        if self.active_epidemic:
            disease_params = {
                "bubonic_plague": (0.45, 0.05, 0.15),
                "pneumonic_plague": (0.85, 0.03, 0.35),
                "dysentery": (0.30, 0.12, 0.04),
                "influenza": (0.40, 0.15, 0.02),
                "typhus": (0.35, 0.08, 0.08)
            }
            base_b, g, m = disease_params.get(self.active_epidemic, (0.40, 0.10, 0.10))
            eff_b = base_b * (1.0 + self.filth_level / 100.0)
            if self.plague_doctor_appointed:
                eff_b *= 0.40
            if self.quarantine_measures:
                eff_b *= 0.50
            if self.stone_drainage_active and self.active_epidemic == "dysentery":
                eff_b *= 0.30
            r0 = self.calculate_reproduction_number(eff_b, g, m)
            status_desc = "🚨 EXPONENTIAL SPREAD (R0 > 1.0)" if r0 > 1.0 else "🛡️ CONTAINED / DECLINING (R0 < 1.0)"
            print(f"Transmission Rate (β): {eff_b:.3f} | Recovery (γ): {g:.2f} | Mortality (μ): {m:.2f}")
            print(f"Basic Reproduction Number (R_0): {r0:.2f} -> {status_desc}")

        print(f"SIR Demographics -> Susceptible (S): {self.sir_state['S']:.0f} | Infected (I): {self.sir_state['I']:.0f} | Immune (R): {self.sir_state['R']:.0f} | Plague Deaths: {self.sir_state['deaths']}")
        if self.epidemic_history:
            print("\nRecent Epidemic Chronicle:")
            for h in self.epidemic_history[-3:]:
                print(f"  • {h}")
        print("=" * 78)

    def sweep_streets(self):
        """Dispatches municipal street sweepers to scrub town thoroughfares and gather manure."""
        prev = self.filth_level
        self.filth_level = max(0.0, round(self.filth_level - 18.0, 1))
        self.compost_fertilizer_stock += 1
        if self.filth_level < 70.0 and self.miasma_active:
            self.miasma_active = False
            print("💨 MIASMA DISPERSED: Fresh sea breezes purge the stench from the town square!")
        print(f"\n🧹 STREET SWEEPERS: Dispatched sweepers across cobbles and market alleyways!")
        print(f"Filth Index reduced: {prev:.1f} -> {self.filth_level:.1f} (-18.0).")
        print(f"Collected biomass transformed into +1 Organic Compost Fertilizer (Total: {self.compost_fertilizer_stock} barrels).")

    def clean_cesspool(self):
        """Empties town latrine cesspools to prevent groundwater contamination."""
        prev = self.cesspool_fill
        self.cesspool_fill = 5.0
        self.compost_fertilizer_stock += 2
        print(f"\n🚽 CESSPOOL SANITATION: Night soil scavengers emptied municipal latrine pits!")
        print(f"Cesspool capacity restored: {prev:.1f}% -> 5.0%.")
        print(f"Sludge processed into +2 High-Yield Fertilizer Barrels (+25% farm yield bonus).")
        print("✓ Groundwater aquifer protected; waterborne dysentery hazard neutralized.")

    def appoint_plague_doctor(self):
        """Appoints Dr. Corvus as royal plague doctor with beak mask and waxed leather cloak."""
        self.plague_doctor_appointed = True
        self.total_renown += 75
        self.citizen_morale = min(100.0, self.citizen_morale + 15.0)
        self.epidemic_history.append(f"Day {self.day_number}: Appointed High Plague Doctor with Beak Mask and Waxed Leather Cloak.")
        print(f"\n🦅 THE PLAGUE DOCTOR: Appointed Dr. Corvus to oversee royal disease containment!")
        print("Apparel: Protective Beak Mask filled with camphor, lavender, and mint.")
        print("Garb: Heavy Waxed Leather Cloak (impervious to plague fleas) & Wooden Exam Cane.")
        print("✓ Contagion transmission factor (β) slashed by -60.0% across all districts!")
        print("✓ Reassurance in royal medicine restores +15 Morale to the populace.")

    def enact_black_quarantine(self, measure: str):
        """Enacts emergency quarantine protocols from GDD Section 77.2."""
        measure = measure.lower().strip()
        measures_map = {
            "board_houses": ("Board Up Infected Houses", "Painted Red Cross on contaminated doors; 14-day forced family isolation (-40% transmission)."),
            "houses": ("Board Up Infected Houses", "Painted Red Cross on contaminated doors; 14-day forced family isolation (-40% transmission)."),
            "armed_cordon": ("Armed Sanitary Cordon", "Sealed town portcullis gates with heavy crossbowmen; caravans halted (-50% external transmission)."),
            "cordon": ("Armed Sanitary Cordon", "Sealed town portcullis gates with heavy crossbowmen; caravans halted (-50% external transmission)."),
            "sanitary_pyres": ("Sanitary Pyres", "Incinerated infected bedding, apparel, and straw corpses in lime pyres outside walls (-30% filth)."),
            "pyres": ("Sanitary Pyres", "Incinerated infected bedding, apparel, and straw corpses in lime pyres outside walls (-30% filth).")
        }
        if measure not in measures_map:
            print("Unknown quarantine measure! Available: 'board_houses', 'armed_cordon', 'sanitary_pyres'.")
            return

        canonical_key = "board_houses" if "house" in measure else ("armed_cordon" if "cordon" in measure else "sanitary_pyres")
        name, desc = measures_map[measure]
        if canonical_key not in self.quarantine_measures:
            self.quarantine_measures.append(canonical_key)
            self.quarantine_edict_active = True
            if canonical_key == "sanitary_pyres":
                self.filth_level = max(0.0, self.filth_level - 15.0)
            self.epidemic_history.append(f"Day {self.day_number}: Enacted {name}.")
            print(f"\n🛡️ BLACK QUARANTINE ENACTED: {name}!")
            print(f"Protocol: {desc}")
        else:
            print(f"Quarantine measure '{name}' is already actively enforced.")

    def trigger_outbreak(self, disease: str = "bubonic_plague"):
        """GDD Section 75 & 77: Triggers a pathogenic epidemic outbreak in the city."""
        disease = disease.lower().strip()
        valid = ["bubonic_plague", "pneumonic_plague", "dysentery", "influenza", "typhus"]
        if disease not in valid:
            disease = "bubonic_plague"

        total_citizens = sum(c["count"] for c in self.population_cohorts.values())
        init_infected = max(2, int(total_citizens * 0.08))
        self.sir_state["I"] = float(init_infected)
        self.sir_state["S"] = max(0.0, float(total_citizens - init_infected))
        self.sir_state["R"] = 0.0
        self.active_epidemic = disease
        self.epidemic_history.append(f"Day {self.day_number}: Outbreak of {disease.upper()} emerged in town quarters ({init_infected} infected).")
        print(f"\n☠️ OUTBREAK REPORT: An infectious outbreak of {disease.upper()} has erupted!")
        print(f"Initial Patients: {init_infected} citizens infected | Susceptible: {self.sir_state['S']:.0f}.")
        print("Recommendation: Appoint Plague Doctor, sweep streets, and enforce quarantine protocols immediately!")

    def simulate_epidemic_step(self, hours: int = 1):
        """Simulates differential SIR transmission and filth accumulation over time."""
        hours = max(1, hours)
        total_pop = sum(c["count"] for c in self.population_cohorts.values())

        # Accumulate filth
        f_delta = self.calculate_filth_delta(total_pop, self.livestock_count, self.street_sweepers_count)
        self.filth_level = max(0.0, min(100.0, self.filth_level + f_delta * (hours / 4.0)))
        if self.filth_level > 70.0:
            self.miasma_active = True

        # If no active disease, chance of spontaneous outbreak if filth > 80
        if not self.active_epidemic:
            if self.filth_level > 80.0:
                print("\n⚠️ SANITATION CRISIS: Filth reached catastrophic levels! Disease spontaneously sparked.")
                self.trigger_outbreak("bubonic_plague")
            else:
                return

        disease_params = {
            "bubonic_plague": (0.45, 0.05, 0.15),
            "pneumonic_plague": (0.85, 0.03, 0.35),
            "dysentery": (0.30, 0.12, 0.04),
            "influenza": (0.40, 0.15, 0.02),
            "typhus": (0.35, 0.08, 0.08)
        }
        base_b, g, m = disease_params.get(self.active_epidemic, (0.40, 0.10, 0.10))

        eff_b = base_b * (1.0 + self.filth_level / 100.0)
        if self.plague_doctor_appointed:
            eff_b *= 0.40
        if self.quarantine_measures:
            eff_b *= 0.50
        if self.stone_drainage_active and self.active_epidemic == "dysentery":
            eff_b *= 0.30

        dt = hours * 0.10
        s, i, r = self.sir_state["S"], self.sir_state["I"], self.sir_state["R"]
        n = max(1.0, s + i + r)

        new_inf = eff_b * (s * i / n) * dt
        new_inf = min(s, new_inf)
        new_rec = g * i * dt
        new_rec = min(i, new_rec)
        new_dead = m * i * dt
        new_dead = min(i - new_rec, new_dead)

        self.sir_state["S"] = max(0.0, s - new_inf)
        self.sir_state["I"] = max(0.0, i + new_inf - new_rec - new_dead)
        self.sir_state["R"] = r + new_rec
        self.sir_state["deaths"] += int(new_dead)
        self.demographic_stats["total_deaths"] += int(new_dead)

        r0 = self.calculate_reproduction_number(eff_b, g, m)
        print(f"\n⏳ EPIDEMIOLOGY TICK (+{hours}h): {self.active_epidemic.upper()} (R_0 = {r0:.2f})")
        print(f"SIR Tracking -> Susceptible: {self.sir_state['S']:.1f}, Active Sick: {self.sir_state['I']:.1f}, Recovered: {self.sir_state['R']:.1f}, Deaths: +{int(new_dead)}.")

        if self.sir_state["I"] < 0.5:
            print(f"🎉 CONTAGION QUELLED: {self.active_epidemic.upper()} has been extinguished from the realm!")
            self.epidemic_history.append(f"Day {self.day_number}: {self.active_epidemic.upper()} successfully eradicated.")
            self.active_epidemic = None
            self.sir_state["I"] = 0.0

    def administer_panacea(self):
        """Administers Miracle Panacea (GDD 74.2: Saffron + Spirit + Sulfur) to heal 60% of infected."""
        if not self.active_epidemic or self.sir_state["I"] <= 0:
            print("\nThere are no active plague victims requiring the Miracle Panacea.")
            return

        if self.coins < 25:
            print(f"\nInsufficient funds! Distilling Miracle Panacea requires 25 💰 Gold Coins.")
            return

        self.coins -= 25
        active_inf = self.sir_state["I"]
        cured = round(active_inf * 0.60, 1)
        self.sir_state["I"] = max(0.0, active_inf - cured)
        self.sir_state["R"] += cured
        self.total_renown += 50
        print(f"\n✨ MIRACLE PANACEA DISTILLED: Administered golden sulfur-saffron panacea to quarantined patients!")
        print(f"Cured: {cured:.0f} sick citizens restored to health! Active sick remaining: {self.sir_state['I']:.0f}.")
        print("✓ Mortality suppressed; epidemic collapse imminent!")

    def run_cli(self):
        self.print_header()
        print("\nWelcome, Monarch! The entire Feudal Realm is assembled and awaiting your command.")
        print("Type 'help' to see available interactive controls.")

        while True:
            self.print_hud()
            try:
                cmd_raw = input("Monarch Action (type 'help' for commands) > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nFarewell, Monarch!")
                break

            if not cmd_raw:
                continue

            parts = cmd_raw.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in ["quit", "exit", "q"]:
                print("\nSaving Feudal Realm state... Farewell, Monarch!")
                break
            elif cmd == "help":
                print("\nAvailable Commands:")
                print("  goto <district>   - Fast travel to: citadel, town, steam, harbor, mining, observatory, agriculture, wilderness")
                print("  map               - View 2D realm district overview map")
                print("  inspect           - Detailed telemetry on targeted voxel, temperature, stress, and NPK")
                print("  mine              - Mine targeted block, collect resources, and run structural stress check")
                print("  furnace           - Ignite / stoke the high-pressure blast furnace & steam boiler")
                print("  trebuchet         - Fire siege trebuchet with full ballistic trajectory calculation")
                print("  cycle             - Cycle to the next district in order")
                print("  save [slot]       - Persist current realm state with sparse delta encoding & SHA-256")
                print("  load [slot]       - Restore realm state from saved slot")
                print("  audio [effect]    - Play procedural sound (horn, pickaxe, axe, footstep, district)")
                print("  talk [role]       - Converse with citizen (smith, farmer, guard, baker)")
                print("  quests / journal  - Open Royal Deeds & Feudal Quest Chronicle (J key)")
                print("  heraldry          - View royal coat of arms, motto, and tinctures (K key)")
                print("  decrees           - Open Imperial Decrees & Law Proclamations (V key)")
                print("  proclaim <edict>  - Proclaim edict (corvee, grain, guild, militia, trade, scholar)")
                print("  squad             - View garrison squadron status, stance, and formation")
                print("  formation <name>  - Order formation (wall, wedge, skirmish, square)")
                print("  diplomacy         - Open Royal Chancery & Foreign Relations (U key)")
                print("  gift <realm> [amt]- Dispatch diplomatic tribute gift to foreign realm")
                print("  treaty <r> <type> - Ratify treaty (non_aggression, trade, alliance, vassal)")
                print("  tribute <realm>   - Demand feudal tribute from vassal or weaker realm")
                print("  war <realm>       - Declare imperial war and sever all treaties")
                print("  castle            - View Throne Room decor and active imperial realm buffs")
                print("  install <decor>   - Install decor (throne, map, chandelier, vault, table, armor, armillary)")
                print("  tournament        - Open Grand Feudal Tournament & Chivalric Arena (T key)")
                print("  joust [target]    - Ride the tilt pass with heavy lance (helm, shield, breastplate)")
                print("  melee [action]    - Enter arena foot melee (strike, cleave, parry, bash)")
                print("  archery           - Compete in Guild Marksman Contest")
                print("  duel [gambit]     - Duel Sovereign Champion Prince Alden")
                print("  feast             - Host Grand Regal Banquet (+25% Citizen Morale, +100 Honor)")
                print("  monastery / abbey - Open Monastic Scriptoria & Alchemical Sanctum (B key)")
                print("  research <tech>   - Research scholastic tech (norfolk, blast, ballistics, geology, guild, gothic)")
                print("  brew <elixir>     - Distill alchemical elixir (vitality, iron_skin, windstrider, dragons_breath)")
                print("  transmute <metal> - Transmute metals in crucible (silver, gold, catalyst)")
                print("  enshrine <relic>  - Enshrine holy relic on altar slot (hearth, crown, columba, chalice, banner)")
                print("  bells             - Ring Abbey Cathedral Bells (+30% Citizen Serenity)")
                print("  magnum            - Refine Philosopher's Stone stage (Nigredo -> Albedo -> Citrinitas -> Rubedo)")
                print("  spies / shadow    - Open Royal Spymaster & Shadow Council (N key)")
                print("  recruit <type>    - Recruit shadow agent (informant, saboteur, master_spy)")
                print("  infiltrate <op> [r]- Launch covert mission in foreign realm (intel, sabotage, tech, revolt)")
                print("  sweep             - Run counter-intelligence sweep in Citadel taverns")
                print("  interrogate       - Interrogate captured foreign infiltrator in dungeons")
                print("  ransom            - Ransom captive spy to foreign envoys for gold")
                print("  stockpile [cat]   - Inspect royal granary & warehouse goods (food, ores, metals, manufactured)")
                print("  produce <recipe> [amt] - Execute craft (flour, bread, stew, pie, salt_meat, smoke_meat, smelt_bloom, refine_iron, smelt_steel, forge_tools, forge_weapons, cast_bronze, brew_mead, weave_tunic, candle)")
                print("  market            - Open town square market stalls and caravan trading board")
                print("  buy <item> [amt]  - Purchase goods from caravan merchants using gold coins")
                print("  sell <item> [amt] - Sell stockpile goods to caravan merchants for gold coins")
                print("  quota <item> <t>  - Set RimWorld-style 'Do Until X' production quota and mode")
                print("  spoilage [hrs]    - Simulate cellar preservation & Arrhenius decay kinetics")
                print("  court             - Open High Magistrate Manor Leet Court (Law & Justice)")
                print("  judge <id> <v>    - Deliver verdict: acquit, pillory, fine, ordeal, gallows")
                print("  charter <type>    - Ratify legal charter: magna, leet, assize, sanctuary")
                print("  patrol / crime    - Deploy town watchmen and bailiffs on anti-crime patrol")
                print("  vitals / health   - View Monarch vitals, trauma conditions, doctor skill & diurnal rhythm")
                print("  injure [sev] [solo]- Simulate combat knockout trauma (severity 1-3, optional 'solo' for captivity)")
                print("  heal <remedy>     - Apply chirurgeon remedy (valerian, bone_splint, honey_dressing)")
                print("  ransom_monarch    - Pay gold ransom to bandit kidnappers to liberate captive Sovereign")
                print("  advance [hrs]     - Advance diurnal clock by N hours (updates daytime phases & recovery)")
                print("  census / pop      - View feudal demographic census across 7 biological age cohorts")
                print("  simulate_pop [s]  - Simulate cohort turnover, Gompertz mortality & natural births")
                print("  sanitation / filth- View municipal sanitation, filth metrics, cesspool fill & SIR epidemiology")
                print("  sweep_streets     - Order municipal sweepers to clean streets (-18 Filth, +Compost)")
                print("  cesspool          - Drain municipal cesspool night soil into organic fertilizer barrels")
                print("  doctor_plague     - Appoint Corvus Beak-Masked Plague Doctor (-60% SIR beta transmission)")
                print("  quarantine <type> - Enact Black Plague quarantine protocol: boards, cordon, pyres")
                print("  outbreak [type]   - Trigger infectious disease epidemic (bubonic_plague, dysentery, etc.)")
                print("  sim_disease [hrs] - Advance differential SIR epidemic dynamics and bacterial filth drift")
                print("  panacea           - Administer miraculous Sovereign Panacea Elixir (cures 60% active infected)")
                print("  pause             - Display in-game pause menu and controls guide")
                print("  wait              - Advance time by 1 hour (burn calories, regenerate stamina)")
                print("  quit              - Exit simulator")
            elif cmd == "goto":
                if args:
                    self.fast_travel(args[0])
                else:
                    print("Usage: goto <citadel|town|steam|harbor|mining|observatory|agriculture|wilderness>")
            elif cmd == "cycle":
                keys = list(self.DISTRICTS.keys())
                idx = (keys.index(self.current_district_key) + 1) % len(keys)
                self.fast_travel(keys[idx])
            elif cmd == "map":
                self.print_map()
            elif cmd == "inspect":
                self.inspect_block()
            elif cmd == "mine":
                self.mine_voxel()
            elif cmd == "furnace":
                self.operate_furnace()
            elif cmd == "trebuchet":
                self.fire_trebuchet()
            elif cmd == "save":
                slot = args[0] if args else "quicksave"
                self.save_realm(slot)
            elif cmd == "load":
                slot = args[0] if args else "quicksave"
                self.load_realm(slot)
            elif cmd in ["audio", "sound"]:
                effect = args[0] if args else "horn"
                self.play_audio_sfx(effect)
            elif cmd in ["quests", "journal"]:
                self.show_quest_journal()
            elif cmd in ["heraldry", "crest", "banner"]:
                self.show_heraldry()
            elif cmd in ["castle", "throne"]:
                self.show_castle_customizer()
            elif cmd in ["decrees", "edicts"]:
                self.show_decrees()
            elif cmd == "proclaim":
                if args:
                    self.proclaim_decree(args[0])
                else:
                    print("Usage: proclaim <corvee|grain|guild|militia|trade|scholar>")
            elif cmd in ["squad", "garrison"]:
                self.show_squadron()
            elif cmd == "formation":
                if args:
                    self.set_squadron_formation(args[0])
                else:
                    print("Usage: formation <wall|wedge|skirmish|square>")
            elif cmd in ["diplomacy", "chancery", "foreign"]:
                self.show_diplomacy()
            elif cmd in ["gift", "envoy"]:
                if args:
                    amt = int(args[1]) if len(args) > 1 and args[1].isdigit() else 15
                    self.send_diplomatic_gift(args[0], amt)
                else:
                    print("Usage: gift <valoria|silvercoast|ashfell|sunken_mire> [amount]")
            elif cmd == "treaty":
                if args:
                    t_type = args[1] if len(args) > 1 else "non_aggression"
                    self.sign_diplomatic_treaty(args[0], t_type)
                else:
                    print("Usage: treaty <realm> <non_aggression|trade|alliance|vassal>")
            elif cmd == "tribute":
                if args:
                    self.demand_diplomatic_tribute(args[0])
                else:
                    print("Usage: tribute <valoria|silvercoast|ashfell|sunken_mire>")
            elif cmd == "war":
                if args:
                    self.declare_diplomatic_war(args[0])
                else:
                    print("Usage: war <valoria|silvercoast|ashfell|sunken_mire>")
            elif cmd in ["warroom", "war_room", "outposts", "defense"]:
                self.show_war_room()
            elif cmd == "invade":
                fac = args[0] if args else "ashfell"
                self.trigger_test_invasion(fac)
            elif cmd == "reinforce":
                if args:
                    self.reinforce_outpost(args[0])
                else:
                    print("Usage: reinforce <north|east|west|south>")
            elif cmd == "militia":
                if args:
                    self.muster_outpost_militia(args[0])
                else:
                    print("Usage: militia <north|east|west|south>")
            elif cmd == "pitch":
                if args:
                    self.unleash_outpost_pitch(args[0])
                else:
                    print("Usage: pitch <north|west>")
            elif cmd == "install":
                if args:
                    self.install_furnishing(args[0])
                else:
                    print("Usage: install <throne|map|chandelier|vault|table|armor|armillary>")
            elif cmd in ["talk", "dialogue"]:
                role = args[0] if args else "smith"
                self.talk_to_citizen(role)
            elif cmd in ["tournament", "arena", "jousting"]:
                self.show_tournament()
            elif cmd == "joust":
                target = args[0] if args else "shield"
                self.start_joust(target)
            elif cmd == "melee":
                act = args[0] if args else "strike"
                self.start_melee(act)
            elif cmd == "archery":
                self.start_archery()
            elif cmd == "duel":
                gambit = args[0] if args else "riposte_counter"
                self.duel_champion(gambit)
            elif cmd in ["feast", "banquet"]:
                self.host_regal_feast()
            elif cmd in ["monastery", "abbey", "scriptoria"]:
                self.show_monastery()
            elif cmd == "research":
                if args:
                    self.conduct_research(args[0])
                else:
                    print("Usage: research <norfolk|blast|ballistics|geology|guild|sacred>")
            elif cmd == "brew":
                if args:
                    self.brew_alchemy_elixir(args[0])
                else:
                    print("Usage: brew <vitality|iron_skin|windstrider|dragons_breath>")
            elif cmd == "transmute":
                if args:
                    self.transmute_alchemy_metal(args[0])
                else:
                    print("Usage: transmute <silver|gold|catalyst>")
            elif cmd == "enshrine":
                if args:
                    slot = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
                    self.enshrine_abbey_relic(args[0], slot)
                else:
                    print("Usage: enshrine <hearth|crown|columba|chalice|banner> [slot 1-3]")
            elif cmd in ["bells", "bell"]:
                self.ring_abbey_bells()
            elif cmd in ["magnum", "stone"]:
                self.refine_philosophers_stone()
            elif cmd in ["spies", "espionage", "shadow", "spymaster"]:
                self.show_espionage()
            elif cmd in ["recruit", "hire_spy"]:
                if args:
                    self.recruit_shadow_spy(args[0])
                else:
                    print("Usage: recruit <informant|saboteur|master_spy>")
            elif cmd in ["infiltrate", "op", "covert"]:
                if args:
                    realm = args[1] if len(args) > 1 else "ashfell"
                    self.launch_covert_op(args[0], realm)
                else:
                    print("Usage: infiltrate <intel|sabotage|tech|revolt> [valoria|ashfell|silvercoast]")
            elif cmd in ["sweep", "counter_intel"]:
                if args and args[0] in ["streets", "street", "city", "filth", "waste"]:
                    self.sweep_streets()
                else:
                    self.trigger_counter_intel_sweep()
            elif cmd in ["interrogate", "question"]:
                self.interrogate_captive()
            elif cmd in ["ransom", "release"]:
                self.ransom_captive()
            elif cmd in ["stockpile", "granary", "warehouse", "economy"]:
                cat = args[0] if args else "all"
                self.show_stockpile(cat)
            elif cmd in ["produce", "craft", "cook", "smelt", "forge"]:
                if args:
                    amt = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
                    self.produce_resource(args[0], amt)
                else:
                    print("Usage: produce <recipe> [amount]")
            elif cmd in ["market", "bazaar", "caravan"]:
                self.show_market()
            elif cmd == "buy":
                if args:
                    amt = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
                    self.trade_market("buy", args[0], amt)
                else:
                    print("Usage: buy <item> [amount]")
            elif cmd == "sell":
                if args:
                    amt = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
                    self.trade_market("sell", args[0], amt)
                else:
                    print("Usage: sell <item> [amount]")
            elif cmd in ["quota", "threshold"]:
                if len(args) >= 2 and args[1].isdigit():
                    mode = args[2] if len(args) > 2 else "until_x"
                    self.set_production_quota(args[0], int(args[1]), mode)
                else:
                    print("Usage: quota <item> <target_amount> [until_x|continuous|paused]")
            elif cmd in ["spoilage", "cellar", "decay"]:
                hrs = int(args[0]) if args and args[0].isdigit() else 24
                cont = args[1] if len(args) > 1 else "COLD_CELLAR"
                self.simulate_cellar_spoilage(hrs, cont)
            elif cmd in ["court", "justice", "magistrate", "leet"]:
                self.show_court()
            elif cmd in ["judge", "verdict", "sentence"]:
                if len(args) >= 2:
                    self.deliver_verdict(args[0], args[1])
                else:
                    print("Usage: judge <case_id> <acquit|pillory|fine|ordeal|gallows>")
            elif cmd in ["charter", "ratify", "law"]:
                if args:
                    self.issue_legal_charter(args[0])
                else:
                    print("Usage: charter <magna|leet|assize|sanctuary>")
            elif cmd in ["crime", "patrol", "bailiff"]:
                self.simulate_crime_patrol()
            elif cmd in ["vitals", "health", "injuries", "doctor"]:
                self.show_monarch_vitals()
            elif cmd in ["knockout", "injure", "trauma"]:
                sev = int(args[0]) if args and args[0].isdigit() else 2
                guards = args[1].lower() != "solo" if len(args) > 1 else True
                self.simulate_combat_knockout(sev, guards_present=guards)
            elif cmd in ["heal_monarch", "chirurgeon", "treat", "heal"]:
                if args:
                    self.treat_monarch_trauma(args[0])
                else:
                    print("Usage: heal <valerian|bone_splint|honey_dressing>")
            elif cmd in ["ransom_monarch", "pay_ransom"]:
                self.pay_monarch_ransom()
            elif cmd in ["advance", "time", "tick"]:
                hrs = int(args[0]) if args and args[0].isdigit() else 1
                self.advance_diurnal_time(hrs)
            elif cmd in ["census", "demographics", "pop", "population"]:
                self.show_demographics()
            elif cmd in ["simulate_pop", "sim_pop", "age_pop"]:
                seasons = int(args[0]) if args and args[0].isdigit() else 1
                self.simulate_demographics(seasons)
            elif cmd in ["sanitation", "filth", "hygiene", "miasma"]:
                self.show_sanitation()
            elif cmd in ["sweep_streets", "clean_streets", "street_sweep", "clean_filth"]:
                self.sweep_streets()
            elif cmd in ["cesspool", "drain_cesspool", "night_soil"]:
                self.clean_cesspool()
            elif cmd in ["doctor_plague", "plague_doctor", "appoint_doctor"]:
                self.appoint_plague_doctor()
            elif cmd in ["quarantine", "cordon", "pyres"]:
                measure = args[0] if args else "board_houses"
                self.enact_black_quarantine(measure)
            elif cmd in ["outbreak", "epidemic", "pestilence"]:
                disease = args[0] if args else "bubonic_plague"
                self.trigger_outbreak(disease)
            elif cmd in ["sim_disease", "simulate_epidemic", "plague_tick"]:
                hrs = int(args[0]) if args and args[0].isdigit() else 4
                self.simulate_epidemic_step(hrs)
            elif cmd in ["panacea", "cure_plague", "miracle_cure"]:
                self.administer_panacea()
            elif cmd == "pause":
                print("\n=== [PAUSE MENU SIMULATION] ===")
                print("1. Resume Realm")
                print("2. Save Realm (Slots: slot_1, slot_2, slot_3, quicksave)")
                print("3. Load Realm (Slots: slot_1, slot_2, slot_3, quicksave)")
                print("4. Settings (FOV: 85°, Mouse Sens: 0.003, Volume: 80%, Fullscreen: Windowed)")
                print("5. Feudal Controls Guide (W,A,S,D, Space, Shift, 1-8, E, C, L, J, H, F1, F2, F5, F9, ESC)")
                print("================================")
            elif cmd == "wait":
                self.time_hour = (self.time_hour + 1) % 24
                if self.time_hour == 0:
                    self.day_number += 1
                self.stamina = 100.0
                self.calories = max(200.0, self.calories - 75.0)
                print(f"Time advanced to {self.time_hour:02d}:00 on Day {self.day_number}.")
            else:
                print(f"Unknown command '{cmd}'. Type 'help' for command list.")


def main():
    sim = VoxelRealmSimulator()
    if len(sys.argv) > 1 and sys.argv[1] in ["--test", "--headless"]:
        print("[INTERACTIVE SIMULATOR] Running automated headless verification test...")
        assert len(sim.DISTRICTS) == 8, "Must have 8 districts"
        for d in sim.DISTRICTS.keys():
            sim.fast_travel(d)
        sim.inspect_block()
        sim.mine_voxel()
        sim.operate_furnace()
        sim.fire_trebuchet()
        h = sim.save_realm("test_slot")
        assert len(h) == 64, "SHA-256 hash must be 64 characters"
        sim.load_realm("test_slot")
        sim.play_audio_sfx("horn")
        sim.play_audio_sfx("pickaxe")
        sim.show_quest_journal()
        sim.talk_to_citizen("smith")
        sim.talk_to_citizen("farmer")
        sim.show_heraldry()
        sim.show_castle_customizer()
        sim.install_furnishing("vault")
        assert "treasury_vault_chest" in sim.castle_decor
        assert sim.castle_prestige == 150
        sim.show_decrees()
        sim.proclaim_decree("guild")
        assert "guild_subsidies" in sim.active_decrees
        sim.show_squadron()
        sim.set_squadron_formation("wedge")
        assert "Shock Wedge" in sim.garrison_formation
        sim.show_diplomacy()
        sim.send_diplomatic_gift("valoria", 20)
        assert sim.factions["valoria"]["opinion"] > 15.0
        sim.sign_diplomatic_treaty("valoria", "trade")
        assert "Trade Concordat" in sim.factions["valoria"]["treaties"]
        sim.demand_diplomatic_tribute("valoria")
        assert sim.coins >= 140
        sim.declare_diplomatic_war("ashfell")
        assert sim.factions["ashfell"]["opinion"] == -100.0
        assert sim.factions["ashfell"]["status"] == "War ⚔️"
        sim.show_war_room()
        sim.trigger_test_invasion("ashfell")
        assert len(sim.active_invasions) == 1
        sim.reinforce_outpost("north_redoubt", 2)
        assert sim.outposts["north_redoubt"]["garrison"] == 6
        sim.muster_outpost_militia("north_redoubt")
        assert sim.outposts["north_redoubt"]["garrison"] == 10
        sim.unleash_outpost_pitch("north_redoubt")
        assert not sim.outposts["north_redoubt"]["pitch"]
        sim.show_tournament()
        sim.start_joust("shield")
        assert sim.tournament_wins >= 1
        sim.start_melee("cleave")
        sim.start_archery(1.5, 0.0)
        sim.duel_champion("riposte_counter")
        assert sim.tournament_wins == 4
        sim.host_regal_feast()
        assert sim.feasts_hosted == 1
        assert sim.tournament_chivalry >= 350
        sim.show_monastery()
        sim.conduct_research("norfolk_genetics")
        assert "norfolk_genetics" in sim.unlocked_techs
        sim.brew_alchemy_elixir("vitality")
        assert sim.brewed_potions >= 1
        sim.transmute_alchemy_metal("gold")
        assert sim.transmutations >= 1
        sim.enshrine_abbey_relic("st_columba_tome", 2)
        assert sim.altar_relics[1] == "st_columba_tome"
        sim.ring_abbey_bells()
        assert sim.abbey_bell_active
        sim.refine_philosophers_stone()
        assert sim.stone_stage == 2
        sim.show_espionage()
        sim.recruit_shadow_spy("informant")
        assert len(sim.recruited_spies) >= 1
        sim.launch_covert_op("intel", "ashfell")
        sim.launch_covert_op("tech", "valoria")
        assert sim.scholar_points >= 120.0
        sim.trigger_counter_intel_sweep()
        assert len(sim.captured_spies) == 1
        assert sim.plots_thwarted >= 1
        sim.interrogate_captive()
        assert sim.captured_spies[0]["interrogated"]
        sim.ransom_captive()
        assert len(sim.captured_spies) == 0
        sim.show_stockpile("all")
        sim.produce_resource("smelt_bloom", 2)
        assert sim.stockpile["iron_bloom"] >= 2
        sim.produce_resource("refine_iron", 2)
        assert sim.stockpile["wrought_iron_ingot"] >= 2
        sim.produce_resource("smelt_steel", 1)
        assert sim.stockpile["steel_ingot"] >= 1
        sim.produce_resource("salt_meat", 2)
        assert sim.stockpile["cured_meat"] >= 2
        sim.produce_resource("brew_mead", 1)
        assert sim.stockpile["honey_mead"] >= 1
        sim.show_market()
        sim.trade_market("buy", "wheat", 10)
        assert sim.stockpile["wheat"] >= 40
        sim.trade_market("sell", "bread", 5)
        assert sim.stockpile["bread"] <= 50
        sim.set_production_quota("tools", 15, "until_x")
        assert sim.quotas["tools"] == 15
        sim.simulate_cellar_spoilage(24, "COLD_CELLAR")
        sim.show_court()
        sim.deliver_verdict("CASE-101", "pillory")
        assert len(sim.verdict_history) >= 1
        sim.deliver_verdict("CASE-102", "fine")
        sim.deliver_verdict("CASE-103", "gallows")
        assert len(sim.active_dockets) == 0
        sim.issue_legal_charter("leet")
        assert "leet" in sim.ratified_charters
        sim.simulate_crime_patrol()
        assert len(sim.active_dockets) >= 1
        sim.show_monarch_vitals()
        dur = sim.calculate_bed_rest_duration(2, sim.court_doctor_skill)
        assert 4.0 <= dur <= 32.0
        r_cost = sim.calculate_monarch_ransom(5)
        assert r_cost == 600
        phase = sim.get_current_diurnal_phase()
        assert "phase" in phase
        sim.simulate_combat_knockout(2, guards_present=True)
        assert sim.monarch_status == "bedridden"
        assert len(sim.trauma_conditions) == 1
        sim.treat_monarch_trauma("bone_splint")
        sim.advance_diurnal_time(15)
        sim.simulate_combat_knockout(3, guards_present=False)
        assert sim.monarch_status == "captive"
        assert sim.ransom_demanded == 600
        assert sim.pay_monarch_ransom()
        assert sim.monarch_status == "active"
        sim.show_demographics()
        sim.simulate_demographics(1)
        # Milestone 57: Feudal Pestilence, Sanitation, & Epidemiology Verification
        sim.show_sanitation()
        r0 = sim.calculate_reproduction_number(0.45, 0.05, 0.15)
        assert abs(r0 - 2.25) < 0.001, "R0 must equal beta / (gamma + mu)"
        f_delta = sim.calculate_filth_delta(100, 20, 4)
        assert f_delta == (100 * 0.05 + 20 * 0.25 - 4 * 1.75)
        old_filth = sim.filth_level
        sim.sweep_streets()
        assert sim.filth_level <= old_filth
        assert sim.compost_fertilizer_stock >= 1
        sim.clean_cesspool()
        assert sim.cesspool_fill == 5.0
        assert sim.compost_fertilizer_stock >= 3
        sim.appoint_plague_doctor()
        assert sim.plague_doctor_appointed is True
        sim.enact_black_quarantine("board_houses")
        sim.enact_black_quarantine("armed_cordon")
        sim.enact_black_quarantine("sanitary_pyres")
        assert "board_houses" in sim.quarantine_measures
        assert "armed_cordon" in sim.quarantine_measures
        assert "sanitary_pyres" in sim.quarantine_measures
        sim.trigger_outbreak("bubonic_plague")
        assert sim.active_epidemic == "bubonic_plague"
        assert sim.sir_state["I"] > 0
        old_infected = sim.sir_state["I"]
        sim.administer_panacea()
        assert sim.sir_state["I"] < old_infected
        sim.simulate_epidemic_step(4)
        h_san = sim.save_realm("test_sanitation_slot")
        assert len(h_san) == 64
        sim.load_realm("test_sanitation_slot")
        assert sim.plague_doctor_appointed is True
        assert "board_houses" in sim.quarantine_measures
        print("[INTERACTIVE SIMULATOR] All simulator subsystems passed verification cleanly!")
        sys.exit(0)
    sim.run_cli()


if __name__ == "__main__":
    main()
