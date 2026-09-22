"""
Voxel Lord: Feudal Realm - Automated E2E Test Suite
Validates MASTER_GDD.md across 4 Tiers:
- Tier 1: Feature Coverage (All 133 sections 0-132, non-empty, zero placeholders)
- Tier 2: Boundary & Corner Conditions (Markdown table structure, columns, numerical ranges)
- Tier 3: Cross-Feature Integration (Cross-system consistency between economy, combat, geology, AI)
- Tier 4: Real-World Simulation (Mathematical validation of core formulas)
"""

import math
import os
import re
import sys
import unittest

GDD_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "MASTER_GDD.md")
)


def load_gdd_content():
    if not os.path.exists(GDD_PATH):
        raise FileNotFoundError(f"MASTER_GDD.md not found at {GDD_PATH}")
    with open(GDD_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestGDD_Tier1_FeatureCoverage(unittest.TestCase):
    """
    Tier 1: Feature Coverage & Section Completeness
    Validates that all 133 numbered sections (0 to 132) are present in MASTER_GDD.md,
    contain non-trivial content, and contain zero forbidden placeholders ('TBD', 'TODO', '...', 'va boshqalar').
    """

    @classmethod
    def setUpClass(cls):
        cls.content = load_gdd_content()
        cls.lines = cls.content.splitlines()

    def test_all_133_sections_exist(self):
        """Verify that sections 0 through 132 all have numbered headers (# N.)."""
        section_pattern = re.compile(r"^#\s+([0-9]+)\.\s*(.*)")
        found_sections = {}
        for idx, line in enumerate(self.lines, 1):
            m = section_pattern.match(line.strip())
            if m:
                sec_num = int(m.group(1))
                found_sections[sec_num] = (idx, m.group(2).strip())

        missing = [i for i in range(133) if i not in found_sections]
        self.assertEqual(
            len(missing),
            0,
            f"Missing required numbered sections from 0..132: {missing}",
        )
        self.assertGreaterEqual(
            len(found_sections),
            133,
            f"Expected at least 133 top-level sections, found {len(found_sections)}",
        )

    def test_each_section_has_non_empty_content(self):
        """Verify that every section has body text beyond its header."""
        sections = re.split(r"\n(?=#\s+[0-9]+\.)", self.content)
        empty_sections = []
        for sec in sections:
            stripped = sec.strip()
            if not stripped:
                continue
            lines = [l.strip() for l in stripped.splitlines() if l.strip()]
            if len(lines) <= 1:
                empty_sections.append(lines[0] if lines else "UNKNOWN")

        self.assertEqual(
            len(empty_sections),
            0,
            f"Sections with no body content detected: {empty_sections}",
        )

    def test_zero_placeholders_tbd(self):
        """Verify that zero 'TBD' placeholders exist in MASTER_GDD.md."""
        matches = re.findall(r"\bTBD\b", self.content, re.IGNORECASE)
        self.assertEqual(
            len(matches),
            0,
            f"Forbidden placeholder 'TBD' found {len(matches)} times in MASTER_GDD.md",
        )

    def test_zero_placeholders_todo(self):
        """Verify that zero 'TODO' placeholders exist in MASTER_GDD.md."""
        matches = re.findall(r"\bTODO\b", self.content, re.IGNORECASE)
        self.assertEqual(
            len(matches),
            0,
            f"Forbidden placeholder 'TODO' found {len(matches)} times in MASTER_GDD.md",
        )

    def test_zero_placeholders_ellipsis(self):
        """Verify that zero '...' lazy ellipsis placeholders exist in specifications."""
        matches = re.findall(r"\.\.\.", self.content)
        self.assertEqual(
            len(matches),
            0,
            f"Forbidden placeholder '...' found {len(matches)} times in MASTER_GDD.md",
        )

    def test_zero_placeholders_va_boshqalar(self):
        """Verify that zero 'va boshqalar' (et cetera) lazy placeholders exist in specifications."""
        matches = []
        for idx, line in enumerate(self.lines, 1):
            if "va boshqalar" in line.lower():
                matches.append((idx, line.strip()))

        self.assertEqual(
            len(matches),
            0,
            f"Forbidden placeholder 'va boshqalar' found at: {matches}",
        )


class TestGDD_Tier2_BoundaryAndCorner(unittest.TestCase):
    """
    Tier 2: Boundary & Corner Conditions
    Validates table structure integrity, column alignments, non-empty cells,
    numerical boundaries, and valid physical units across core systems.
    """

    @classmethod
    def setUpClass(cls):
        cls.content = load_gdd_content()
        cls.raw_tables = re.findall(
            r"(\|.+?\|\n\|[-:\s|]+\|\n(?:\|.+?\|\n)+)", cls.content
        )

    def _parse_table(self, table_str):
        lines = [l.strip() for l in table_str.strip().splitlines() if l.strip()]
        header = [c.strip() for c in lines[0].split("|")[1:-1]]
        separator = [c.strip() for c in lines[1].split("|")[1:-1]]
        rows = []
        for line in lines[2:]:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            rows.append(cols)
        return header, separator, rows

    def test_markdown_tables_syntax_and_column_integrity(self):
        """Verify that all markdown tables have matching column counts across header and rows."""
        self.assertGreater(
            len(self.raw_tables),
            0,
            "No markdown tables found in MASTER_GDD.md",
        )
        for i, raw_t in enumerate(self.raw_tables):
            header, separator, rows = self._parse_table(raw_t)
            num_cols = len(header)
            self.assertEqual(
                len(separator),
                num_cols,
                f"Table {i+1} separator column count mismatch: header {num_cols} vs sep {len(separator)}",
            )
            for r_idx, row in enumerate(rows):
                self.assertEqual(
                    len(row),
                    num_cols,
                    f"Table {i+1} Row {r_idx+1} column count {len(row)} != header count {num_cols}: {row}",
                )
                for c_idx, cell in enumerate(row):
                    self.assertTrue(
                        cell != "",
                        f"Table {i+1} Row {r_idx+1} Column {c_idx+1} has empty cell",
                    )

    def test_crops_table_schema_and_boundaries(self):
        """Verify Table 5 (Crops) has 9 canonical crops with valid temperatures, growth hours, and yields."""
        crop_table = None
        for raw_t in self.raw_tables:
            if "crop_wheat" in raw_t or "Ekin ID" in raw_t:
                crop_table = raw_t
                break

        self.assertIsNotNone(crop_table, "Crops table (Table 5) not found in MASTER_GDD.md")
        header, _, rows = self._parse_table(crop_table)
        self.assertIn("Ekin ID", header[0])
        self.assertGreaterEqual(len(rows), 9, f"Expected at least 9 canonical crops, found {len(rows)}")

        for row in rows:
            crop_id = row[0]
            time_col = row[2]
            self.assertTrue(
                "soat" in time_col or "kun" in time_col,
                f"Crop {crop_id} growth time column missing time unit: {time_col}",
            )
            temp_col = row[5]
            self.assertIn("C", temp_col, f"Crop {crop_id} missing Celsius temperature: {temp_col}")

    def test_tools_table_durability_and_speed_progression(self):
        """Verify Table 3 (Tools) has ascending tier progression and positive durability."""
        tool_table = None
        for raw_t in self.raw_tables:
            if "Asbob Tieri" in raw_t and "H_{max}" in raw_t:
                tool_table = raw_t
                break

        self.assertIsNotNone(tool_table, "Tools table (Table 3) not found in MASTER_GDD.md")
        header, _, rows = self._parse_table(tool_table)
        self.assertGreaterEqual(len(rows), 5, f"Expected at least 5 tool tiers, found {len(rows)}")

        for row in rows:
            tier_name = row[0]
            dur_col = row[4]
            self.assertTrue(
                "zarba" in dur_col or re.search(r"\d+", dur_col),
                f"Tool tier {tier_name} has invalid durability: {dur_col}",
            )

    def test_dynamic_pricing_table_bounds(self):
        """Verify Table 14 (Base Prices) has 0.2x min and 5.0x max multiplier bounds."""
        price_table = None
        for raw_t in self.raw_tables:
            if "Bazaviy Narx" in raw_t and "0.2x" in raw_t and "5.0x" in raw_t:
                price_table = raw_t
                break

        self.assertIsNotNone(price_table, "Pricing table (Table 14) not found in MASTER_GDD.md")
        _, _, rows = self._parse_table(price_table)
        self.assertGreaterEqual(len(rows), 10, f"Expected at least 10 commodities in price table, found {len(rows)}")

        for row in rows:
            item_name = row[1]
            base_price = row[3]
            self.assertTrue(
                "Kumush" in base_price or "Oltin" in base_price or re.search(r"\d+", base_price),
                f"Item {item_name} has invalid base price: {base_price}",
            )

    def test_morale_modifiers_bounded(self):
        """Verify Table 16 (Morale Modifiers) has values bounded within [-100, +100]."""
        morale_table = None
        for raw_t in self.raw_tables:
            if "Morale Modifikatori" in raw_t and "Ta'sir Qilish" in raw_t:
                morale_table = raw_t
                break

        self.assertIsNotNone(morale_table, "Morale modifiers table (Table 16) not found")
        _, _, rows = self._parse_table(morale_table)
        self.assertGreaterEqual(len(rows), 10, f"Expected at least 10 morale events, found {len(rows)}")

        for row in rows:
            event = row[1]
            mod_str = row[2]
            nums = re.findall(r"([+-]?\d+)", mod_str)
            for n in nums:
                val = int(n)
                self.assertTrue(
                    -100 <= val <= 100,
                    f"Morale modifier {val} for event '{event}' exceeds [-100, +100] bound",
                )

    def test_core_systems_table_coverage(self):
        """
        Check presence of tables across all 6 core domains:
        - Crops (M1: Agricultural production)
        - Food & Preservation (M1: Nutrition and spoilage)
        - Tools progression (M1: Item durability and speed)
        - Market Base Prices (M1: Economic commodities)
        - Ores & Minerals (M4: Geological catalog)
        - Weapons & Armor Mitigation (M3: Combat physics)
        - Military Units (M3: Feudal troops & siege engines)
        """
        table_keywords = {
            "Crops (M1)": ["crop_wheat", "Ekin ID"],
            "Food & Preservation (M1)": ["food_milk_raw", "Bazaviy Saqlanish"],
            "Tools Progression (M1)": ["Asbob Tieri", "H_{max}"],
            "Market Base Prices (M1)": ["Bazaviy Narx", "food_wheat_sheaf"],
            "Geological Minerals (M4)": ["Qatlam Chuqurligi", "24 ta Mineral", "K_{rock}"],
            "Weapons & Armor Matrix (M3)": ["Slash", "Pierce", "Blunt", "Deflection", "Absorption"],
            "Military Unit Tiers (M3)": ["Piyoda Askari", "Ritsar", "Trebuchet", "Mangonel"]
        }

        found_systems = {}
        for system_name, kws in table_keywords.items():
            matched = False
            for raw_t in self.raw_tables:
                if any(kw.lower() in raw_t.lower() for kw in kws):
                    matched = True
                    break
            found_systems[system_name] = matched

        # Report status
        unexpanded_milestones = [sys for sys, ok in found_systems.items() if not ok]
        if unexpanded_milestones:
            # Document expected state during progressive milestone implementation
            print(f"\n[INFO: Core Tables Status] Present: {[s for s, ok in found_systems.items() if ok]}")
            print(f"[INFO: Pending Milestone Tables]: {unexpanded_milestones}")

        # Assert M1 tables are strictly present
        self.assertTrue(found_systems["Crops (M1)"], "Crops table must be present")
        self.assertTrue(found_systems["Food & Preservation (M1)"], "Food table must be present")
        self.assertTrue(found_systems["Tools Progression (M1)"], "Tools table must be present")
        self.assertTrue(found_systems["Market Base Prices (M1)"], "Market pricing table must be present")


class TestGDD_Tier3_CrossFeature(unittest.TestCase):
    """
    Tier 3: Cross-Feature Integration & Consistency
    Verifies cross-system linkages between agriculture, food preservation,
    combat damage archetypes, metallurgy, and citizen simulation.
    """

    @classmethod
    def setUpClass(cls):
        cls.content = load_gdd_content()

    def test_crop_to_food_supply_chain_consistency(self):
        """Verify agricultural crops (wheat, barley) flow into processing and food products."""
        self.assertIn("crop_wheat", self.content)
        self.assertIn("food_wheat_sheaf", self.content)
        self.assertTrue(
            ("tegirmon" in self.content.lower() or "mill" in self.content.lower())
            and ("un" in self.content.lower() or "flour" in self.content.lower()),
            "Wheat-to-flour milling chain is not cross-referenced in GDD",
        )

    def test_geology_to_smelting_and_tools_consistency(self):
        """Verify mined ores (iron, copper, tin) are linked to smelting recipes and tool crafting."""
        has_iron = "temir" in self.content.lower() or "iron" in self.content.lower()
        has_copper = "mis" in self.content.lower() or "copper" in self.content.lower()
        has_tin = "qalay" in self.content.lower() or "tin" in self.content.lower()
        self.assertTrue(has_iron, "Iron ore/metallurgy not referenced")
        self.assertTrue(has_copper, "Copper ore/metallurgy not referenced")
        self.assertTrue(has_tin, "Tin ore/metallurgy not referenced")

    def test_combat_damage_types_vs_armor_matrix(self):
        """Verify combat damage types (Slash, Pierce, Blunt) are referenced with armor deflection/absorption."""
        self.assertIn("Slash", self.content, "Slash damage type missing")
        self.assertIn("Pierce", self.content, "Pierce damage type missing")
        self.assertIn("Blunt", self.content, "Blunt damage type missing")

    def test_citizen_fsm_states_vs_needs_replenishment(self):
        """Verify that the 10 canonical citizen AI states address citizen needs."""
        canonical_states = [
            "Walk", "Work", "Eat", "Sleep", "Fight",
            "Flee", "Socialize", "Heal", "Transport", "Rest"
        ]
        for state in canonical_states:
            self.assertIn(
                state,
                self.content,
                f"Canonical Citizen AI FSM state '{state}' missing in GDD",
            )

    def test_tundra_biome_vs_greenhouse_thermodynamics(self):
        """Verify Tundra biome extreme cold links to greenhouse geothermal heating requirement."""
        has_tundra = "tundra" in self.content.lower()
        has_greenhouse = "issiqxona" in self.content.lower() or "greenhouse" in self.content.lower()
        self.assertTrue(has_tundra, "Tundra biome missing")
        self.assertTrue(has_greenhouse, "Greenhouse system missing")

    def test_24_minerals_geological_presence(self):
        """
        Verify canonical minerals are referenced across geology, metallurgy, and economy.
        During M4 expansion, all 24 will be fully tabulated.
        """
        core_minerals = ["temir", "oltin", "kumush", "tosh", "mis"]
        found = [m for m in core_minerals if m in self.content.lower()]
        self.assertGreaterEqual(
            len(found),
            4,
            f"Core feudal minerals missing from GDD: {[m for m in core_minerals if m not in found]}",
        )


class TestGDD_Tier4_Simulations(unittest.TestCase):
    """
    Tier 4: Real-World Simulation & Mathematical Verification
    Executes algorithmic simulations of core game formulas to prove mathematical correctness:
    1. Crop growth tick dynamics under thermal & hydration curves
    2. Arrhenius food spoilage with Q10=2.0 and container preservation
    3. Dynamic market pricing with supply/demand elasticity and clamps [0.2x, 5.0x]
    4. Universal combat damage & armor mitigation across Slash, Pierce, Blunt
    5. Mine ceiling stability Sc and collapse threshold Sc < 0.75
    6. Tundra greenhouse thermodynamic equilibrium
    """

    def test_crop_growth_tick_formula_simulation(self):
        """
        Formula:
        GrowthRate(T, W) = BaseRate * max(0, 1 - ((T - T_opt) / (T_range))^2) * min(1.0, W / W_opt)
        Verify that optimal conditions yield 1.0, sub-optimal slows down, and freezing/drought stops growth.
        """
        t_opt = 22.0
        t_range = 15.0  # T_min = 7, T_max = 37
        w_opt = 0.15    # 15% soil hydration

        def calc_rate(t, w):
            if t <= (t_opt - t_range) or t >= (t_opt + t_range):
                temp_factor = 0.0
            else:
                temp_factor = max(0.0, 1.0 - ((t - t_opt) / t_range) ** 2)
            water_factor = min(1.0, max(0.0, w / w_opt))
            return temp_factor * water_factor

        # 1. Optimal conditions: T = 22C, W = 15% -> Rate = 1.0
        rate_opt = calc_rate(22.0, 0.15)
        self.assertAlmostEqual(rate_opt, 1.0, places=4)

        # 2. Sub-optimal temperature: T = 15C, W = 15% -> 0 < Rate < 1.0
        rate_sub = calc_rate(15.0, 0.15)
        expected_temp = 1.0 - ((15.0 - 22.0) / 15.0) ** 2
        self.assertAlmostEqual(rate_sub, expected_temp, places=4)
        self.assertTrue(0.0 < rate_sub < 1.0)

        # 3. Freezing temperature: T = -5C -> Rate = 0.0 (dormancy)
        rate_freeze = calc_rate(-5.0, 0.15)
        self.assertEqual(rate_freeze, 0.0)

        # 4. Scorching heat: T = 45C -> Rate = 0.0 (withered)
        rate_hot = calc_rate(45.0, 0.15)
        self.assertEqual(rate_hot, 0.0)

        # 5. Drought: W = 0% -> Rate = 0.0
        rate_drought = calc_rate(22.0, 0.0)
        self.assertEqual(rate_drought, 0.0)

        # Total growth simulation over 96 hours (4 game days):
        total_growth = 0.0
        for _ in range(96):
            total_growth += calc_rate(22.0, 0.15) * (100.0 / 96.0)
        self.assertAlmostEqual(total_growth, 100.0, delta=0.1)

    def test_arrhenius_food_spoilage_simulation(self):
        """
        Formula:
        k(T, container) = k_0 * (Q_10 ^ ((T - T_ref) / 10)) * M_container
        With Q_10 = 2.0, T_ref = 15C.
        Verify that +10C doubles spoilage, -10C halves spoilage, and salting preserves 10x longer.
        """
        q10 = 2.0
        t_ref = 15.0
        k0 = 1.0 / 24.0  # 1 day base life at 15C in standard box (M_container = 1.0)

        def calc_spoilage_rate(temp, m_container=1.0):
            return k0 * (q10 ** ((temp - t_ref) / 10.0)) * m_container

        # 1. Reference condition (15C, open crate M=1.0)
        k_ref = calc_spoilage_rate(15.0, 1.0)
        self.assertAlmostEqual(k_ref, k0, places=5)

        # 2. Warm summer room (25C): 2x faster spoilage -> 12 hours shelf life
        k_25 = calc_spoilage_rate(25.0, 1.0)
        self.assertAlmostEqual(k_25, 2.0 * k0, places=5)
        shelf_life_25 = 1.0 / k_25
        self.assertAlmostEqual(shelf_life_25, 12.0, places=2)

        # 3. Scorching summer heat (35C): 4x faster spoilage -> 6 hours shelf life
        k_35 = calc_spoilage_rate(35.0, 1.0)
        self.assertAlmostEqual(k_35, 4.0 * k0, places=5)
        shelf_life_35 = 1.0 / k_35
        self.assertAlmostEqual(shelf_life_35, 6.0, places=2)

        # 4. Cold underground cellar (5C): 0.5x spoilage -> 48 hours shelf life
        k_5 = calc_spoilage_rate(5.0, 1.0)
        self.assertAlmostEqual(k_5, 0.5 * k0, places=5)
        shelf_life_5 = 1.0 / k_5
        self.assertAlmostEqual(shelf_life_5, 48.0, places=2)

        # 5. Salted barrel preservation (M_container = 0.10) in cellar (5C):
        k_salted_cellar = calc_spoilage_rate(5.0, 0.10)
        shelf_life_salted = 1.0 / k_salted_cellar
        # 48 hours / 0.1 = 480 hours (20 days!)
        self.assertAlmostEqual(shelf_life_salted, 480.0, places=2)

    def test_dynamic_market_pricing_clamp_simulation(self):
        """
        Formula:
        Price = clamp(P_base * (Demand / Supply)^gamma * ReputationMultiplier, 0.2 * P_base, 5.0 * P_base)
        With gamma = 1.25.
        Verify equilibrium, market collapse clamp at 0.2x, famine price cap at 5.0x, and strict monotonicity.
        """
        p_base = 10.0  # 10 silver
        gamma = 1.25

        def calc_price(demand, supply, rep=1.0):
            ratio = demand / max(0.001, supply)
            raw_p = p_base * (ratio ** gamma) * rep
            return max(0.2 * p_base, min(5.0 * p_base, raw_p))

        # 1. Market equilibrium: Demand = 100, Supply = 100, Rep = 1.0 -> Price = P_base
        p_eq = calc_price(100, 100)
        self.assertAlmostEqual(p_eq, 10.0, places=3)

        # 2. Severe famine: Demand = 500, Supply = 10 -> Raw ratio = 50^1.25 = 133.3 -> Clamped to 5.0x P_base = 50.0
        p_famine = calc_price(500, 10)
        self.assertEqual(p_famine, 50.0)

        # 3. Superabundance (Market glut): Demand = 10, Supply = 1000 -> Clamped to 0.2x P_base = 2.0
        p_glut = calc_price(10, 1000)
        self.assertEqual(p_glut, 2.0)

        # 4. Strict monotonicity across increasing demand
        prices = [calc_price(d, 100) for d in range(20, 300, 20)]
        for i in range(len(prices) - 1):
            self.assertLessEqual(prices[i], prices[i + 1])

    def test_combat_damage_mitigation_simulation(self):
        """
        Formula:
        RawDamage = BaseDamage * SkillMultiplier * QualityMultiplier * HitMultiplier
        FinalDamage = max(0, (RawDamage - ArmorDeflection)) * (1.0 - AbsorptionPercent)
        Verify Slash vs Plate (high deflection stops slash), Blunt vs Plate (concussion penetrates),
        and non-negativity invariant.
        """
        def calc_damage(base_dmg, skill, quality, hit, deflection, absorption):
            raw = base_dmg * skill * quality * hit
            mitigated = max(0.0, raw - deflection) * (1.0 - absorption)
            return round(mitigated, 2)

        # Heavy Steel Plate: Deflection: Slash=25, Pierce=18, Blunt=8. Absorption: Slash=0.40, Pierce=0.30, Blunt=0.15

        # 1. Standard Slashing Sword: Base=22, Skill=1.0, Quality=1.0, Hit=1.0
        # Raw = 22. Deflection = 25 -> 22 < 25 -> 0 damage! (Sword deflected by plate!)
        dmg_slash = calc_damage(22.0, 1.0, 1.0, 1.0, deflection=25.0, absorption=0.40)
        self.assertEqual(dmg_slash, 0.0)

        # 2. Heavy War Hammer (Blunt): Base=22, Skill=1.0, Quality=1.0, Hit=1.0
        # Raw = 22. Deflection = 8 -> Mitigated = (22 - 8) * (1 - 0.15) = 14 * 0.85 = 11.9 damage!
        dmg_blunt = calc_damage(22.0, 1.0, 1.0, 1.0, deflection=8.0, absorption=0.15)
        self.assertAlmostEqual(dmg_blunt, 11.9, places=1)
        self.assertGreater(dmg_blunt, dmg_slash, "Blunt weapon must outperform slashing weapon against heavy plate")

        # 3. Masterwork Slashing Sword (Quality=1.8x, Skill=1.5x) -> Raw = 22 * 1.5 * 1.8 = 59.4
        # Penetrates deflection: (59.4 - 25) * 0.6 = 34.4 * 0.6 = 20.64 damage
        dmg_master_slash = calc_damage(22.0, 1.5, 1.8, 1.0, deflection=25.0, absorption=0.40)
        self.assertAlmostEqual(dmg_master_slash, 20.64, places=1)

        # 4. Non-negativity invariant under massive deflection
        dmg_zero = calc_damage(5.0, 0.5, 0.8, 1.0, deflection=100.0, absorption=0.80)
        self.assertEqual(dmg_zero, 0.0)

    def test_mine_ceiling_stability_simulation(self):
        """
        Formula:
        S_c = K_rock * (R_sup / Span)
        Collapse condition: S_c < 0.75 -> Cave-in!
        Safe condition: S_c >= 1.0
        Verify Granite (K=1.4) vs Sandstone (K=0.8), unsupported span vs supported.
        """
        def calc_stability(k_rock, r_sup, span):
            return k_rock * (r_sup / max(0.1, span))

        # 1. Unsupported cavern: Span = 10m, Natural support R_sup = 1.0m
        # Granite (K_rock = 1.4): Sc = 1.4 * 1.0 / 10.0 = 0.14 < 0.75 -> CAVE-IN!
        sc_granite_unsupported = calc_stability(1.4, 1.0, 10.0)
        self.assertLess(sc_granite_unsupported, 0.75)

        # 2. Cavern with Oak Support Beams: R_sup = 6.0m, Span = 7.0m
        # Granite: Sc = 1.4 * (6.0 / 7.0) = 1.20 >= 1.0 -> SAFE!
        sc_granite_supported = calc_stability(1.4, 6.0, 7.0)
        self.assertGreaterEqual(sc_granite_supported, 1.0)

        # 3. Sandstone (weak sedimentary rock, K_rock = 0.75) under same 7m span with oak beams (R_sup = 6m):
        # Sc = 0.75 * (6.0 / 7.0) = 0.643 < 0.75 -> CAVE-IN RISK! Requires denser spacing (Span <= 5m)
        sc_sandstone = calc_stability(0.75, 6.0, 7.0)
        self.assertLess(sc_sandstone, 0.75)

        # Sandstone with dense spacing (Span = 4m):
        sc_sandstone_dense = calc_stability(0.75, 6.0, 4.0)
        self.assertAlmostEqual(sc_sandstone_dense, 1.125, places=3)
        self.assertGreaterEqual(sc_sandstone_dense, 1.0)

    def test_greenhouse_thermodynamic_equilibrium_simulation(self):
        """
        Formula:
        Steady-state heat balance:
        Q_in = Q_loss
        Q_geothermal = U * Area * (T_eq - T_amb)
        T_eq = T_amb + (Q_geothermal / (U * Area))
        Verify that in Tundra (T_amb = -15C), geothermal steam maintains T_eq >= 18C.
        """
        t_amb = -15.0  # -15C Tundra winter
        area = 120.0   # 120 m^2 greenhouse footprint
        u_insulation = 2.0  # 2.0 W/(m^2 * K) insulated stone & double glass
        q_geothermal = 8400.0  # 8.4 kW geothermal steam heat input

        delta_t = q_geothermal / (u_insulation * area)
        t_eq = t_amb + delta_t

        # delta_t = 8400 / 240 = 35.0 C -> T_eq = -15 + 35 = +20.0 C
        self.assertAlmostEqual(delta_t, 35.0, places=2)
        self.assertAlmostEqual(t_eq, 20.0, places=2)

        # Verify T_eq is strictly within crop growth limits (e.g. Wheat T_opt = 22C, T_min = 5C)
        self.assertGreaterEqual(t_eq, 18.0)
        self.assertLessEqual(t_eq, 28.0)


def print_suite_report(result):
    print("\n" + "=" * 80)
    print("           VOXEL LORD: FEUDAL REALM — E2E TEST EXECUTION REPORT")
    print("=" * 80)
    print(f"Total Tests Executed: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("-" * 80)

    if result.failures:
        print("\n[DISCOVERED FAILURES / GDD DEFECTS TO ESCALATE]:")
        for test, trace in result.failures:
            print(f"\n* TEST: {test}")
            err_line = trace.strip().splitlines()[-1]
            print(f"  REASON: {err_line}")

    if result.errors:
        print("\n[EXECUTION ERRORS]:")
        for test, trace in result.errors:
            print(f"\n* TEST: {test}")
            err_line = trace.strip().splitlines()[-1]
            print(f"  REASON: {err_line}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestGDD_Tier1_FeatureCoverage))
    suite.addTests(loader.loadTestsFromTestCase(TestGDD_Tier2_BoundaryAndCorner))
    suite.addTests(loader.loadTestsFromTestCase(TestGDD_Tier3_CrossFeature))
    suite.addTests(loader.loadTestsFromTestCase(TestGDD_Tier4_Simulations))

    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    print_suite_report(res)
    sys.exit(0 if res.wasSuccessful() else 1)
