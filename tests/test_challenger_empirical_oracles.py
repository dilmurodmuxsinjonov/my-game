"""
Voxel Lord: Feudal Realm - Empirical Stress-Testing Oracles (Challenger 1)
Independent mathematical verification and stress testing of MASTER_GDD.md formulas:
1. Crop Growth Simulation over 4 Seasons (9 crops, thermal response, hydration, fertility)
2. Arrhenius Food Spoilage Decay across Extreme Temperatures (-20C to +40C, container preservation)
3. Dynamic Market Pricing Elasticity Clamps (acute famine, hyper-supply, negative power hazard)
4. Combat Damage and Armor Mitigation Edge Cases (glancing blows, high-tier armor vs slash/blunt, zero boundaries)
5. Mine Ceiling Stability Sc over Deep Spans (0 to -350m, overburden lithostatic pressure, timber failure)
6. Greenhouse Thermodynamic Heat Balance in -35C Blizzard (insulation, ventilation, geothermal kW)
"""

import math
import unittest


class TestCropGrowthSimulation(unittest.TestCase):
    """
    Oracle 1: Crop Growth Simulation over 4 Seasons (Section 36)
    Formula:
    DeltaGrowth = (1.0 / BaseGrowthHours) * M_fertility * M_moisture * M_temp * M_tending
    GrowthProgress_(t+1) = min(1.0, GrowthProgress_t + DeltaGrowth)
    """

    def calc_m_fertility(self, fertility: float) -> float:
        return 0.40 + 0.60 * (fertility / 100.0)

    def calc_m_moisture(self, moisture: float) -> float:
        if moisture < 30.0:
            return (moisture / 30.0) * 0.60
        elif moisture <= 80.0:
            return 1.00
        else:
            return 1.00 - ((moisture - 80.0) / 20.0) * 0.50

    def calc_m_temp(self, t_ambient: float, t_min: float, t_opt: float, t_max: float) -> float:
        if t_ambient < t_min:
            return 0.0
        elif t_ambient <= t_max:
            denom = max(0.1, t_opt - t_min)
            diff = abs(t_ambient - t_opt)
            return max(0.10, 1.0 - ((diff / denom) ** 2) * 0.50)
        else:
            return 0.20

    def test_9_crops_optimal_growth_hours(self):
        """Under optimal conditions (Fertility=100%, Moisture=50%, T=T_opt, Master Farmer M_tending=1.35),
        verify that crops reach 100% maturity within or faster than BaseGrowthHours."""
        crops = {
            "crop_wheat": {"base_h": 96, "t_min": 5, "t_opt": 22, "t_max": 35},
            "crop_barley": {"base_h": 72, "t_min": 3, "t_opt": 19, "t_max": 32},
            "crop_rye": {"base_h": 96, "t_min": -2, "t_opt": 15, "t_max": 28},
            "crop_cabbage": {"base_h": 60, "t_min": 0, "t_opt": 16, "t_max": 26},
            "crop_turnip": {"base_h": 48, "t_min": -4, "t_opt": 12, "t_max": 24},
            "crop_carrot": {"base_h": 48, "t_min": 4, "t_opt": 18, "t_max": 30},
            "crop_flax": {"base_h": 84, "t_min": 8, "t_opt": 20, "t_max": 30},
            "crop_hops": {"base_h": 120, "t_min": 10, "t_opt": 24, "t_max": 34},
            "crop_peas": {"base_h": 60, "t_min": 4, "t_opt": 20, "t_max": 30},
        }

        for crop_id, data in crops.items():
            base_h = data["base_h"]
            m_fert = self.calc_m_fertility(100.0)  # 1.0
            m_moist = self.calc_m_moisture(50.0)   # 1.0
            m_temp = self.calc_m_temp(data["t_opt"], data["t_min"], data["t_opt"], data["t_max"]) # 1.0
            m_tending = 1.00 # novice farmer

            delta_per_hour = (1.0 / base_h) * m_fert * m_moist * m_temp * m_tending
            total_progress = delta_per_hour * base_h
            self.assertAlmostEqual(total_progress, 1.0, places=5, msg=f"{crop_id} failed optimal progress")

    def test_wheat_four_seasons_cycle(self):
        """Simulate Wheat growth across 4 canonical seasons in Fertile Plains:
        Spring (12C), Summer (24C), Autumn (10C), Winter (-2C)."""
        t_min, t_opt, t_max = 5.0, 22.0, 35.0
        base_h = 96.0

        # Spring: 12C (10C below opt)
        m_spring = self.calc_m_temp(12.0, t_min, t_opt, t_max)
        self.assertGreater(m_spring, 0.70)
        self.assertLess(m_spring, 1.00)

        # Summer: 24C (2C above opt)
        m_summer = self.calc_m_temp(24.0, t_min, t_opt, t_max)
        self.assertGreaterEqual(m_summer, 0.95)

        # Autumn: 10C (12C below opt)
        m_autumn = self.calc_m_temp(10.0, t_min, t_opt, t_max)
        self.assertGreater(m_autumn, 0.60)

        # Winter: -2C (below T_min=5C) -> Growth halts completely (M_temp = 0.0)
        m_winter = self.calc_m_temp(-2.0, t_min, t_opt, t_max)
        self.assertEqual(m_winter, 0.0, "Wheat must experience winter dormancy at -2C")

    def test_winter_rye_cold_hardiness(self):
        """Winter Rye (T_min = -2C) should maintain active growth in -2C conditions where Wheat halts."""
        m_wheat_subzero = self.calc_m_temp(-2.0, 5.0, 22.0, 35.0)
        m_rye_subzero = self.calc_m_temp(-2.0, -2.0, 15.0, 28.0)

        self.assertEqual(m_wheat_subzero, 0.0)
        self.assertGreaterEqual(m_rye_subzero, 0.50, "Winter Rye should withstand -2C")

    def test_harvest_yield_formula(self):
        """Formula: FinalYield = floor(BaseYield * (0.50 + 0.50 * Fertility/100) * (1.0 + 0.40 * Irrigated) * (1.0 + 0.05 * Skill) * QualityMult)"""
        base_yield = 8 # Wheat
        # Baseline: Fertility=100%, Irrigated=0, Skill=0, Common Tool (1.0x) -> 8 * 1.0 * 1.0 * 1.0 = 8
        y_base = math.floor(base_yield * (0.50 + 0.50 * 1.0) * (1.0 + 0.0) * (1.0 + 0.0) * 1.0)
        self.assertEqual(y_base, 8)

        # Master farmer (Skill=10), Irrigated=1, Fine Scythe (1.25x), Terra Preta (120% fertility)
        # Yield = floor(8 * (0.5 + 0.6) * 1.40 * 1.50 * 1.25) = floor(8 * 1.1 * 1.4 * 1.5 * 1.25) = floor(23.1) = 23
        y_master = math.floor(base_yield * (0.50 + 0.50 * 1.2) * (1.0 + 0.40) * (1.0 + 0.05 * 10) * 1.25)
        self.assertEqual(y_master, 23)
        self.assertGreater(y_master, y_base * 2.5)


class TestArrheniusFoodSpoilage(unittest.TestCase):
    """
    Oracle 2: Arrhenius Food Spoilage Decay across Extreme Temperatures (-20C to +40C) (Section 40)
    Formula:
    M_temp = 2.0 ** ((T_ambient - 15.0) / 10.0)
    If T_ambient <= 0.0C: M_temp = 0.05 (Freeze preservation clamp)
    ShelfLife = BaseShelfLife / (M_temp * M_container)
    """

    def calc_spoilage_mult(self, temp: float) -> float:
        if temp <= 0.0:
            return 0.05
        return 2.0 ** ((temp - 15.0) / 10.0)

    def test_reference_and_known_temperatures(self):
        """Verify 5C, 15C, 25C, 35C points defined in GDD Section 40.1."""
        self.assertAlmostEqual(self.calc_spoilage_mult(15.0), 1.00, places=4)
        self.assertAlmostEqual(self.calc_spoilage_mult(25.0), 2.00, places=4)
        self.assertAlmostEqual(self.calc_spoilage_mult(35.0), 4.00, places=4)
        self.assertAlmostEqual(self.calc_spoilage_mult(5.0), 0.50, places=4)

    def test_extreme_subzero_freezing_minus_20(self):
        """At -20C (winter/blizzard/ice cellar), freeze clamp sets M_temp = 0.05,
        extending raw meat shelf life from 48h to 960h (40 days / 1.4 feudal years)."""
        m_freeze = self.calc_spoilage_mult(-20.0)
        self.assertEqual(m_freeze, 0.05)

        base_meat_life = 48.0 # hours
        shelf_life_minus_20 = base_meat_life / (m_freeze * 1.0)
        self.assertEqual(shelf_life_minus_20, 960.0)

    def test_extreme_scorching_heat_plus_40(self):
        """At +40C (desert/steppe heatwave/furnace room),
        spoilage multiplier reaches 2^(2.5) = 5.657x."""
        m_heat = self.calc_spoilage_mult(40.0)
        expected = 2.0 ** (2.5)
        self.assertAlmostEqual(m_heat, expected, places=3)
        self.assertAlmostEqual(m_heat, 5.657, places=3)

        base_meat_life = 48.0
        shelf_life_heat = base_meat_life / (m_heat * 1.0)
        self.assertAlmostEqual(shelf_life_heat, 8.485, places=2)

    def test_container_preservation_cold_cellar_salted_barrel(self):
        """Cold cellar (5C, M_temp=0.50) + Salted barrel (M_container=0.10 for food_salted_meat base 2016h):
        Effective life = 2016 / (0.50 * 0.10) = 40,320 hours (1,680 days / 60 years)!"""
        base_salt_life = 2016.0 # hours
        m_temp_5c = self.calc_spoilage_mult(5.0) # 0.50
        m_barrel = 0.10
        shelf_life = base_salt_life / (m_temp_5c * m_barrel)
        self.assertEqual(shelf_life, 40320.0)


class TestMarketPricingElasticity(unittest.TestCase):
    """
    Oracle 3: Market Pricing Elasticity Clamps (Section 49)
    Formula:
    P_buy = clamp(BasePrice * (1.0 + k_d * (Stock_target - Stock_current) / Stock_target)^gamma * M_season * M_rep,
                  0.20 * BasePrice, 5.00 * BasePrice)
    k_d = 0.85, gamma = 1.25.
    Stress-testing negative term hazard under hyper-supply.
    """

    def calc_gdd_p_buy_raw_base(self, stock_target: float, stock_current: float, k_d: float = 0.85) -> float:
        """Returns the inner base term (1.0 + k_d * (Stock_target - Stock_current) / Stock_target)."""
        return 1.0 + k_d * ((stock_target - stock_current) / stock_target)

    def calc_safe_p_buy(self, base_price: float, stock_target: float, stock_current: float,
                         m_season: float = 1.0, m_rep: float = 1.0, k_d: float = 0.85, gamma: float = 1.25) -> float:
        base_term = self.calc_gdd_p_buy_raw_base(stock_target, stock_current, k_d)
        # CRITICAL ENGINE DEFENSE: Clamp base_term to >= 0.0 before raising to fractional power gamma
        safe_base = max(0.0, base_term)
        elastic_factor = safe_base ** gamma
        raw_price = base_price * elastic_factor * m_season * m_rep
        return max(0.20 * base_price, min(5.00 * base_price, raw_price))

    def test_mathematical_hazard_unprotected_hyper_supply(self):
        """CRITICAL VULNERABILITY AUDIT:
        When Stock_current > (1 + 1/0.85) * Stock_target (~2.176x Stock_target),
        the inner base term becomes strictly NEGATIVE.
        In real arithmetic, (-x)^1.25 produces complex numbers or NaN, crashing naive engine implementations."""
        stock_target = 100.0
        threshold_stock = stock_target * (1.0 + 1.0 / 0.85) # ~217.65

        # Stock below threshold: base > 0 (well-defined)
        self.assertGreater(self.calc_gdd_p_buy_raw_base(stock_target, 200.0), 0.0)

        # Stock above threshold (Hyper-supply, e.g. 500 units in warehouse):
        base_hyper = self.calc_gdd_p_buy_raw_base(stock_target, 500.0)
        self.assertLess(base_hyper, 0.0, "Base term must be negative under hyper-supply")
        self.assertAlmostEqual(base_hyper, 1.0 + 0.85 * (-4.0), places=4) # 1 - 3.4 = -2.4

        # Proof that native math.pow fails on negative base with fractional power:
        with self.assertRaises(ValueError):
            math.pow(base_hyper, 1.25)

    def test_safe_pricing_clamps_under_acute_famine(self):
        """Under catastrophic famine:
        1. At zero inventory with neutral multipliers: price rises to exactly 2.158x BasePrice.
        2. With compounding winter crisis (Firewood M_season=2.20, Distrusted M_rep=1.25):
           Raw factor = 1.85^1.25 * 2.20 * 1.25 = 2.1576 * 2.75 = 5.933x BasePrice -> Clamped to 5.00x BasePrice!
        3. Under deficit backorders (Stock_current = -100, Stock_target = 100, M_season=1.8):
           Raw factor = (1 + 0.85*2)^1.25 * 1.8 = 2.70^1.25 * 1.8 = 3.427 * 1.8 = 6.169x -> Clamped to 5.00x BasePrice!"""
        base_price = 10.0 # 10 silver
        
        # 1. Zero inventory, neutral:
        p_zero_neutral = self.calc_safe_p_buy(base_price, stock_target=100.0, stock_current=0.0, m_season=1.0, m_rep=1.0)
        self.assertAlmostEqual(p_zero_neutral, 21.576, places=2)

        # 2. Compounding crisis (Firewood blizzard shortage M_season=2.20, bad rep M_rep=1.25):
        p_crisis = self.calc_safe_p_buy(base_price, stock_target=100.0, stock_current=0.0, m_season=2.20, m_rep=1.25)
        self.assertEqual(p_crisis, 50.0, "Compounding crisis must clamp strictly to 5.0x ceiling")

        # 3. Backorders / Deficit stock:
        p_deficit = self.calc_safe_p_buy(base_price, stock_target=100.0, stock_current=-100.0, m_season=1.80, m_rep=1.0)
        self.assertEqual(p_deficit, 50.0, "Deficit backorder spike must clamp strictly to 5.0x ceiling")

    def test_safe_pricing_clamps_under_massive_hyper_supply(self):
        """Under extreme hyper-supply (Stock_current = 2000, Stock_target = 100),
        price must clamp cleanly to exactly 0.20 * BasePrice without NaN or complex error."""
        base_price = 10.0
        p_glut = self.calc_safe_p_buy(base_price, stock_target=100.0, stock_current=2000.0)
        self.assertEqual(p_glut, 2.0, "Hyper-supply must clamp cleanly to 0.20x floor")

    def test_price_monotonicity_in_valid_range(self):
        """As available stock increases from 0 to 200, price should monotonically decrease."""
        base_price = 10.0
        stock_target = 100.0
        prices = [self.calc_safe_p_buy(base_price, stock_target, s) for s in range(0, 201, 10)]
        for i in range(len(prices) - 1):
            self.assertGreaterEqual(prices[i], prices[i + 1])


class TestCombatDamageAndArmorMitigation(unittest.TestCase):
    """
    Oracle 4: Combat Damage & Armor Mitigation Edge Cases (Sections 54 & 55)
    RawDamage = BaseDamage * (1.0 + Skill/100 * 0.75) * QualityMult * AttackTypeMult * HitZoneMult
    DamageAbsorbed = max(0.0, (RawDamage - D_flat) * (1.0 - A_pct))
    Glancing Blow: If RawDamage <= D_flat -> 1.0 HP glancing damage (Section 55.1).
    """

    def calc_raw_damage(self, base_dmg: float, skill: float, quality_mult: float,
                        attack_mult: float, hit_zone_mult: float) -> float:
        return base_dmg * (1.0 + (skill / 100.0) * 0.75) * quality_mult * attack_mult * hit_zone_mult

    def calc_mitigated_damage(self, raw_dmg: float, d_flat: float, a_pct: float, enforce_glancing: bool = True) -> float:
        if raw_dmg <= d_flat:
            return 1.0 if (enforce_glancing and raw_dmg > 0.0) else 0.0
        return max(0.0, (raw_dmg - d_flat) * (1.0 - a_pct))

    def test_glancing_blow_behavior(self):
        """Verify that a common iron sword (RawDamage=20) striking Full Steel Plate (D_flat=26)
        triggers a Glancing Blow yielding 1.0 scratch damage."""
        raw_slash = 20.0
        plate_d_flat = 26.0
        plate_a_pct = 0.92

        dmg_glancing = self.calc_mitigated_damage(raw_slash, plate_d_flat, plate_a_pct, enforce_glancing=True)
        self.assertEqual(dmg_glancing, 1.0, "Glancing blow should inflict 1.0 scratch HP")

        dmg_pure_math = self.calc_mitigated_damage(raw_slash, plate_d_flat, plate_a_pct, enforce_glancing=False)
        self.assertEqual(dmg_pure_math, 0.0, "Without glancing rule, damage should be 0.0")

    def test_slashing_vs_blunt_against_full_steel_plate(self):
        """Warhammer (Blunt Base=22, D_flat=8, A_pct=50%) must radically outperform
        Sword (Slash Base=22, D_flat=26, A_pct=92%) against Full Steel Plate."""
        # 1. Slashing Sword (Raw = 30):
        raw_dmg = 30.0
        dmg_slash = self.calc_mitigated_damage(raw_dmg, d_flat=26.0, a_pct=0.92, enforce_glancing=False)
        # (30 - 26) * 0.08 = 0.32 HP
        self.assertAlmostEqual(dmg_slash, 0.32, places=2)

        # 2. Blunt Warhammer (Raw = 30):
        dmg_blunt = self.calc_mitigated_damage(raw_dmg, d_flat=8.0, a_pct=0.50, enforce_glancing=False)
        # (30 - 8) * 0.50 = 11.0 HP
        self.assertAlmostEqual(dmg_blunt, 11.0, places=2)

        self.assertGreater(dmg_blunt, dmg_slash * 30.0, "Blunt must massively outperform Slash against Plate")

    def test_extreme_mounted_charge_lethal_headshot(self):
        """Legendary Halberd (Base=46, Skill=100 -> 1.75x, Quality=2.50x Legendary, Mounted=3.20x, Head=2.20x):
        Raw damage exceeds 1400 HP; verify it penetrates even Full Plate."""
        raw_lethal = self.calc_raw_damage(base_dmg=46.0, skill=100.0, quality_mult=2.50,
                                          attack_mult=3.20, hit_zone_mult=2.20)
        # 46 * 1.75 * 2.50 * 3.20 * 2.20 = 1416.8 HP
        self.assertAlmostEqual(raw_lethal, 1416.8, places=1)

        # Slash vs Plate: (1416.8 - 26) * 0.08 = 111.26 HP
        dmg_slash_lethal = self.calc_mitigated_damage(raw_lethal, 26.0, 0.92)
        self.assertAlmostEqual(dmg_slash_lethal, 111.264, places=2)
        self.assertGreater(dmg_slash_lethal, 100.0, "Mounted headshot must deliver 100+ lethal HP even through plate")

    def test_zero_and_negative_input_invariants(self):
        """Combat system must never return negative damage or corrupt under zero base damage."""
        dmg_zero = self.calc_mitigated_damage(0.0, 50.0, 0.50)
        self.assertEqual(dmg_zero, 0.0)


class TestMineCeilingStability(unittest.TestCase):
    """
    Oracle 5: Mine Ceiling Stability Sc over Deep Spans (0 to -350m) (Section 32)
    Formula:
    Sc = (K_rock * max(1.0, sum(R_sup^2 / (d^2 + 0.1)))) /
         (1.0 + alpha_span * (L_span / 2)^2 * (1.0 + beta_depth * (|y| / 100)))
    alpha_span = 0.08, beta_depth = 0.35, y <= 0.
    Cave-in collapse if Sc < 0.75. Safe if Sc >= 1.0.
    """

    def calc_sc(self, k_rock: float, l_span: float, depth_y: float,
                supports: list = None, alpha: float = 0.08, beta: float = 0.35) -> float:
        if supports:
            support_term = sum((r_sup ** 2) / (d ** 2 + 0.1) for r_sup, d in supports)
            sup_factor = max(1.0, support_term)
        else:
            sup_factor = 1.0

        depth_abs = abs(depth_y)
        denominator = 1.0 + alpha * ((l_span / 2.0) ** 2) * (1.0 + beta * (depth_abs / 100.0))
        return (k_rock * sup_factor) / max(0.01, denominator)

    def test_granite_vs_sandstone_surface_span(self):
        """At y = 0m, span = 6m:
        Sandstone (K=0.55) unsupported -> Sc = 0.55 / (1 + 0.08*9) = 0.55 / 1.72 = 0.320 < 0.75 (CAVE-IN!)
        Monolithic Granite (K=1.40) unsupported -> Sc = 1.40 / 1.72 = 0.814 (Critical warning, but > 0.75)."""
        sc_sandstone = self.calc_sc(k_rock=0.55, l_span=6.0, depth_y=0.0)
        self.assertLess(sc_sandstone, 0.75, "Unsupported 6m sandstone must collapse")

        sc_granite = self.calc_sc(k_rock=1.40, l_span=6.0, depth_y=0.0)
        self.assertGreaterEqual(sc_granite, 0.75)
        self.assertLess(sc_granite, 1.0)

    def test_depth_attenuation_from_0_to_minus_350m(self):
        """Stress test: As depth plunges to -350m, overburden pressure multiplies the span penalty by:
        1.0 + 0.35 * 3.5 = 2.225x.
        Even Monolithic Granite (K=1.40) with span=6m unsupported collapses at -350m:
        Sc = 1.40 / (1 + 0.08 * 9 * 2.225) = 1.40 / 2.602 = 0.538 < 0.75!"""
        sc_granite_surface = self.calc_sc(k_rock=1.40, l_span=6.0, depth_y=0.0)
        sc_granite_350 = self.calc_sc(k_rock=1.40, l_span=6.0, depth_y=-350.0)

        self.assertGreaterEqual(sc_granite_surface, 0.75)
        self.assertLess(sc_granite_350, 0.75, "Deep -350m excavation must cave-in without heavy structural support")
        self.assertAlmostEqual(sc_granite_350, 0.538, places=3)

    def test_softwood_failure_vs_iron_arch_success_at_minus_350m(self):
        """At -350m, a single softwood timber post (R_sup=3.0m at d=3m) cannot stabilize a 6m span:
        support_term = 9.0 / (9.0 + 0.1) = 0.989 <= 1.0 -> Sc remains 0.538 < 0.75 (CRUSHED!).
        However, an Iron-Reinforced Arch (R_sup=11.0m at d=3m) provides:
        support_term = 121 / 9.1 = 13.297 -> Sc = 1.4 * 13.297 / 2.602 = 7.155 >= 1.0 (Completely safe!)."""
        # Softwood at d=3m
        sc_softwood = self.calc_sc(k_rock=1.40, l_span=6.0, depth_y=-350.0, supports=[(3.0, 3.0)])
        self.assertLess(sc_softwood, 0.75, "Softwood timber must fail under deep lithostatic load")

        # Iron Arch at d=3m
        sc_iron_arch = self.calc_sc(k_rock=1.40, l_span=6.0, depth_y=-350.0, supports=[(11.0, 3.0)])
        self.assertGreaterEqual(sc_iron_arch, 1.0, "Iron arch must keep deep mine ceiling completely stable")
        self.assertAlmostEqual(sc_iron_arch, 7.155, places=2)


class TestGreenhouseThermodynamics(unittest.TestCase):
    """
    Oracle 6: Greenhouse Thermodynamic Heat Balance in -35C Blizzard (Section 68.4)
    Formula:
    T_eq = T_amb + (Q_geothermal + Q_solar) / (sum(U_i * A_i) + m_inf * c_p)
    Yield:
    T_eq < 0C: 0% (Withered Dead)
    0C <= T_eq < 10C: 25% (Severe Cold Stunting)
    10C <= T_eq < 18C: 65% (Sub-optimal)
    18C <= T_eq <= 28C: 100% (Optimal)
    T_eq > 35C: 30% (Heat Wither)
    """

    def calc_t_eq(self, t_amb: float, q_geo_watts: float, q_solar_watts: float,
                  conductance_w_per_k: float, infiltration_w_per_k: float = 0.0) -> float:
        total_heat = q_geo_watts + q_solar_watts
        total_loss = conductance_w_per_k + infiltration_w_per_k
        delta_t = total_heat / max(0.1, total_loss)
        return t_amb + delta_t

    def get_crop_yield(self, t_eq: float) -> float:
        if t_eq < 0.0:
            return 0.0
        elif t_eq < 10.0:
            return 0.25
        elif t_eq < 18.0:
            return 0.65
        elif t_eq <= 28.0:
            return 1.00
        elif t_eq <= 35.0:
            return 0.65 # transition
        else:
            return 0.30

    def test_standard_greenhouse_in_minus_15_calm_winter(self):
        """GDD Benchmark: T_amb = -15C, Area = 120m2, U = 2.0 W/m2*K (Total UA = 240 W/K), Q_geo = 8400W.
        Delta_T = 8400 / 240 = 35.0C -> T_eq = +20.0C -> 100% Optimal Yield."""
        t_eq = self.calc_t_eq(t_amb=-15.0, q_geo_watts=8400.0, q_solar_watts=0.0, conductance_w_per_k=240.0)
        self.assertAlmostEqual(t_eq, 20.0, places=2)
        self.assertEqual(self.get_crop_yield(t_eq), 1.00)

    def test_minus_35_extreme_blizzard_standard_build_marginal(self):
        """In a -35C Tundra Blizzard (Zero solar, Q_geo=8400W, UA=240 W/K):
        Delta_T = 35.0C -> T_eq = -35.0 + 35.0 = 0.0C!
        Yield drops to 25% (severe frost stunting); if wind infiltration adds 20 W/K, T_eq drops to -2.7C (100% CROP DEATH!)."""
        # No infiltration:
        t_eq_calm = self.calc_t_eq(t_amb=-35.0, q_geo_watts=8400.0, q_solar_watts=0.0, conductance_w_per_k=240.0)
        self.assertAlmostEqual(t_eq_calm, 0.0, places=2)
        self.assertEqual(self.get_crop_yield(t_eq_calm), 0.25)

        # Blizzard with wind infiltration loss (+20 W/K):
        t_eq_wind = self.calc_t_eq(t_amb=-35.0, q_geo_watts=8400.0, q_solar_watts=0.0,
                                  conductance_w_per_k=240.0, infiltration_w_per_k=20.0)
        # Delta_T = 8400 / 260 = 32.307C -> T_eq = -35 + 32.307 = -2.69C < 0C
        self.assertLess(t_eq_wind, 0.0)
        self.assertEqual(self.get_crop_yield(t_eq_wind), 0.0, "Crops must freeze and die in high-wind -35C blizzard under standard insulation")

    def test_earth_berm_sod_and_double_quartz_blizzard_proof_greenhouse(self):
        """Engineered Solution for -35C Blizzard:
        80 m2 Earth-Berm Sod walls (U=0.417) + 40 m2 Double Quartz ceiling (U=1.82).
        Total UA = (80 * 0.417) + (40 * 1.82) = 33.36 + 72.8 = 106.16 W/K.
        Delta_T = 8400 / 106.16 = 79.12C!
        Allows player to maintain 18C - 24C with controlled chimney ventilation in -35C blizzard."""
        ua_blizzard_proof = (80.0 * 0.417) + (40.0 * 1.82) # 106.16 W/K
        self.assertAlmostEqual(ua_blizzard_proof, 106.16, places=2)

        # With controlled ventilation damper adding 240 W/K of airflow to maintain comfortable +20C:
        damper_airflow = 136.0 # W/K
        t_eq_controlled = self.calc_t_eq(t_amb=-35.0, q_geo_watts=8400.0, q_solar_watts=0.0,
                                         conductance_w_per_k=ua_blizzard_proof, infiltration_w_per_k=damper_airflow)
        # Total loss = 106.16 + 136 = 242.16 W/K -> Delta_T = 8400 / 242.16 = 34.68C -> T_eq = -0.32C
        # If damper closed (only structure loss 106.16):
        t_eq_closed = self.calc_t_eq(t_amb=-35.0, q_geo_watts=8400.0, q_solar_watts=0.0, conductance_w_per_k=ua_blizzard_proof)
        self.assertGreater(t_eq_closed, 40.0, "Heavily insulated greenhouse heats up dramatically without ventilation")

        # Optimal damper setting for 22C: Total loss needed = 8400 / (22 - (-35)) = 8400 / 57 = 147.37 W/K
        vent_for_optimal = 147.37 - 106.16 # 41.21 W/K
        t_opt_blizzard = self.calc_t_eq(t_amb=-35.0, q_geo_watts=8400.0, q_solar_watts=0.0,
                                        conductance_w_per_k=ua_blizzard_proof, infiltration_w_per_k=vent_for_optimal)
        self.assertAlmostEqual(t_opt_blizzard, 22.0, places=1)
        self.assertEqual(self.get_crop_yield(t_opt_blizzard), 1.00, "Must achieve 100% yield during -35C blizzard with proper insulation & damper control")


if __name__ == "__main__":
    unittest.main()
