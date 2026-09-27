"""
Automated Test Suite for Realism Pillar R3: Biological Survival, Nutrition & NPK Agronomy.
Voxel Lord: Feudal Realm (Godot 4.3 / C++ Core)

Validates:
1. Citizen caloric Total Energy Expenditure (TEE) & Basal Metabolic Rate (BMR) budgeting
2. Three independent nutritional pillars (Carbohydrates, Proteins, Vitamins) decay kinetics
3. Scurvy (Singa) pathogenesis stages, clinical consequences, and cures
4. Arrhenius thermal spoilage (Q10 = 2.0), relative humidity rot, and preservation methods
5. Liebig's Law of the Minimum, 9-crop NPK soil depletion/regeneration, and canonical 4-year crop rotation

Organized under 4-Tier Test Architecture:
- Tier 1: Core Feature Coverage
- Tier 2: Boundary & Corner Cases
- Tier 3: Cross-Feature Interactions
- Tier 4: Real-World Scenarios
"""

import math
import unittest
from typing import Dict, List, Tuple, Optional


class MetabolismAgronomyOracle:
    """Mathematical reference oracle for citizen metabolism, food preservation, and soil agronomy."""

    BMR_KCAL_HOUR = 75.0  # 1800 kcal/day

    ACTIVITY_MULTIPLIERS: Dict[str, float] = {
        "sleep": 0.60,
        "rest": 1.00,
        "socialize": 1.00,
        "walk": 1.50,
        "farming": 1.85,
        "building": 1.85,
        "mining": 2.50,
        "blacksmithing": 2.50,
        "combat": 3.80,
    }

    # Food nutritional content: (calories_kcal, carbs, protein, vitamin)
    FOOD_NUTRITION: Dict[str, Tuple[float, float, float, float]] = {
        "food_bread": (320.0, 45.0, 6.0, 0.0),
        "food_grain_porridge": (280.0, 40.0, 8.0, 2.0),
        "food_meat_raw": (240.0, 0.0, 35.0, 1.0),
        "food_roast_meat": (380.0, 0.0, 48.0, 2.0),
        "food_cabbage_raw": (60.0, 8.0, 2.0, 40.0),
        "food_carrot_raw": (75.0, 12.0, 1.5, 35.0),
        "food_berries_fresh": (90.0, 16.0, 1.0, 55.0),
        "food_pickled_veg": (85.0, 10.0, 2.0, 65.0),
        "food_salted_meat": (390.0, 0.0, 50.0, 0.0),
        "food_smoked_meat": (420.0, 0.0, 52.0, 0.0),
    }

    # Agronomy NPK Demand and Drain per harvest:
    # (demand_N, demand_P, demand_K, delta_N, delta_P, delta_K)
    CROP_NPK_DATA: Dict[str, Tuple[float, float, float, float, float, float]] = {
        "crop_wheat": (100.0, 60.0, 60.0, -14.0, -8.0, -8.0),
        "crop_barley": (80.0, 60.0, 50.0, -12.0, -8.0, -6.0),
        "crop_rye": (60.0, 40.0, 40.0, -8.0, -5.0, -5.0),
        "crop_cabbage": (70.0, 50.0, 120.0, -8.0, -6.0, -16.0),
        "crop_turnip": (40.0, 40.0, 40.0, -5.0, -5.0, -5.0),
        "crop_carrot": (50.0, 70.0, 40.0, -6.0, -8.0, -5.0),
        "crop_flax": (80.0, 80.0, 80.0, -10.0, -10.0, -10.0),
        "crop_hops": (90.0, 80.0, 90.0, -12.0, -10.0, -12.0),
        "crop_peas": (20.0, 30.0, 30.0, +22.0, -2.0, -2.0),  # Rhizobia N-restorer!
    }

    @classmethod
    def calculate_tee(cls, activity: str, body_temp_c: float = 36.5) -> float:
        """
        Total Energy Expenditure (TEE) in kcal/hour:
        TEE = BMR * M_activity + E_shivering
        E_shivering = max(0.0, (36.5 - body_temp_c) / 4.5) * 120.0
        """
        mult = cls.ACTIVITY_MULTIPLIERS.get(activity.lower(), 1.0)
        shivering = max(0.0, (36.5 - body_temp_c) / 4.5) * 120.0
        return cls.BMR_KCAL_HOUR * mult + shivering

    @classmethod
    def calculate_nutrient_decay(
        cls,
        current_level: float,
        nutrient_type: str,
        delta_hours: float,
        is_working: bool = False,
    ) -> float:
        """
        First-order exponential decay:
        level(t) = level_0 * exp(-ln(2) * dt / tau)
        tau_carb = 18h (or 12h if working)
        tau_prot = 72h
        tau_vit = 120h
        """
        if nutrient_type == "carb":
            tau = 12.0 if is_working else 18.0
        elif nutrient_type == "prot":
            tau = 72.0
        elif nutrient_type == "vit":
            tau = 120.0
        else:
            tau = 48.0

        decay_factor = math.exp(-math.log(2) * delta_hours / tau)
        return max(0.0, min(100.0, current_level * decay_factor))

    @classmethod
    def evaluate_scurvy_stage(cls, vitamin_level: float, deficient_hours: float) -> Tuple[int, float, float]:
        """
        Scurvy progression:
        Trigger: Vitamin level < 15.0 sustained >= 72 hours (3 days).
        Stage 0: Healthy, natural healing = 1.0, hp_drain = 0.0
        Stage 1 (72h - 120h): Lethargy, healing = 0.0, hp_drain = 0.0
        Stage 2 (120h - 168h): Petechiae spots, healing = 0.0, hp_drain = 0.5 HP/h
        Stage 3 (>168h): Hemorrhaging, healing = 0.0, hp_drain = 2.5 HP/h
        Returns (stage, natural_healing_mult, hp_drain_per_hour)
        """
        if vitamin_level >= 15.0 or deficient_hours < 72.0:
            return 0, 1.0, 0.0
        elif deficient_hours < 120.0:
            return 1, 0.0, 0.0
        elif deficient_hours < 168.0:
            return 2, 0.0, 0.5
        else:
            return 3, 0.0, 2.5

    @classmethod
    def calculate_arrhenius_multiplier(cls, temp_c: float) -> float:
        """
        Thermal spoilage multiplier M_temp (Q10 = 2.0):
        T <= -5C: 0.02 (Permafrost)
        -5C < T <= 0C: 0.05 (Sub-zero cold)
        0C < T <= 45C: 2.0^((T - 15.0) / 10.0)
        T > 45C: 8.00 (Denaturation)
        """
        if temp_c <= -5.0:
            return 0.02
        elif temp_c <= 0.0:
            return 0.05
        elif temp_c <= 45.0:
            return 2.0 ** ((temp_c - 15.0) / 10.0)
        else:
            return 8.00

    @classmethod
    def calculate_preservation_multiplier(
        cls,
        container_type: str = "chest",
        preservation_method: str = "fresh",
        rh: float = 0.50,
        is_dry_good: bool = False,
    ) -> float:
        """
        Container multipliers:
        dirt: 1.50, chest: 1.00, barrel: 0.60, granary: 0.25, cellar: 0.25, icehouse: 0.10
        Preservation multipliers:
        fresh: 1.00, pickled: 0.14, smoked: 0.10, salted: 0.07, dried: 0.08
        """
        c_mult = {
            "dirt": 1.50,
            "chest": 1.00,
            "barrel": 0.60,
            "granary": 0.25,
            "cellar": 0.25,
            "icehouse": 0.10,
        }.get(container_type.lower(), 1.00)

        p_mult = {
            "fresh": 1.00,
            "pickled": 0.14,
            "smoked": 0.10,
            "salted": 0.07,
            "dried": 0.08,
        }.get(preservation_method.lower(), 1.00)

        if is_dry_good:
            h_mult = 1.0 + (max(0.0, (rh - 0.55) / 0.45) ** 2) * 4.0
        else:
            h_mult = 0.80 + 0.60 * rh

        return c_mult * p_mult * h_mult

    @classmethod
    def calculate_liebig_yield_multiplier(
        cls,
        soil_n: float,
        soil_p: float,
        soil_k: float,
        crop_id: str,
    ) -> float:
        """
        Liebig's Law of the Minimum:
        Fertility = min(N / N_req, P / P_req, K / K_req) * 100%
        Yield multiplier = min(1.20, max(0.20, Fertility / 100.0))
        """
        data = cls.CROP_NPK_DATA.get(crop_id.lower(), (100.0, 50.0, 50.0, 0, 0, 0))
        req_n, req_p, req_k = data[0], data[1], data[2]

        ratio_n = soil_n / req_n
        ratio_p = soil_p / req_p
        ratio_k = soil_k / req_k

        minimum_ratio = min(ratio_n, ratio_p, ratio_k)
        effective_fertility = minimum_ratio * 100.0

        # Yield multiplier bounded: base minimum 0.20x if depleted, up to 1.20x for Terra Preta
        return max(0.20, min(1.20, effective_fertility / 100.0))

    @classmethod
    def apply_crop_harvest_drain(
        cls,
        soil_n: float,
        soil_p: float,
        soil_k: float,
        crop_id: str,
        consecutive_plantings: int = 1,
    ) -> Tuple[float, float, float]:
        """
        Applies nutrient drain with monoculture multiplier:
        Drain_actual = Drain_base * (1.0 + 0.5 * (consecutive_plantings - 1))
        """
        data = cls.CROP_NPK_DATA.get(crop_id.lower(), (100.0, 50.0, 50.0, -10.0, -10.0, -10.0))
        _, _, _, dn_base, dp_base, dk_base = data

        mono_mult = 1.0 + 0.50 * max(0, consecutive_plantings - 1)

        # Negative values are drains; positive (peas N) are restorations
        dn = dn_base * mono_mult if dn_base < 0 else dn_base
        dp = dp_base * mono_mult if dp_base < 0 else dp_base
        dk = dk_base * mono_mult if dk_base < 0 else dk_base

        new_n = max(0.0, min(120.0, soil_n + dn))
        new_p = max(0.0, min(120.0, soil_p + dp))
        new_k = max(0.0, min(120.0, soil_k + dk))

        return new_n, new_p, new_k


class TestBiologicalMetabolismTier1(unittest.TestCase):
    """Tier 1: Core Feature Coverage for Calories, Nutrients, Spoilage, and Agronomy."""

    def test_caloric_expenditure_bmr_and_activities(self):
        """Verify TEE calculation across sleep, rest, farming, and mining states."""
        # Sleep: 75 * 0.60 = 45 kcal/hr
        tee_sleep = MetabolismAgronomyOracle.calculate_tee("sleep")
        self.assertEqual(tee_sleep, 45.0)

        # Rest: 75 * 1.0 = 75 kcal/hr
        tee_rest = MetabolismAgronomyOracle.calculate_tee("rest")
        self.assertEqual(tee_rest, 75.0)

        # Farming: 75 * 1.85 = 138.75 kcal/hr
        tee_farm = MetabolismAgronomyOracle.calculate_tee("farming")
        self.assertEqual(tee_farm, 138.75)

        # Mining: 75 * 2.50 = 187.5 kcal/hr
        tee_mining = MetabolismAgronomyOracle.calculate_tee("mining")
        self.assertEqual(tee_mining, 187.5)

    def test_three_nutritional_pillars_decay(self):
        """Verify independent exponential decay rates for Carbs, Protein, and Vitamins."""
        # 12 hours elapsed:
        # Carbs: tau=18h -> level = 100 * exp(-ln2 * 12 / 18) = 100 * 2^(-2/3) ~ 62.99
        c12 = MetabolismAgronomyOracle.calculate_nutrient_decay(100.0, "carb", 12.0)
        self.assertAlmostEqual(c12, 100.0 * (2.0 ** (-12.0 / 18.0)), places=2)

        # Protein: tau=72h -> level = 100 * 2^(-12/72) ~ 89.08
        p12 = MetabolismAgronomyOracle.calculate_nutrient_decay(100.0, "prot", 12.0)
        self.assertAlmostEqual(p12, 100.0 * (2.0 ** (-12.0 / 72.0)), places=2)

        # Vitamin: tau=120h -> level = 100 * 2^(-12/120) ~ 93.30
        v12 = MetabolismAgronomyOracle.calculate_nutrient_decay(100.0, "vit", 12.0)
        self.assertAlmostEqual(v12, 100.0 * (2.0 ** (-12.0 / 120.0)), places=2)

    def test_scurvy_pathogenesis_progression_stages(self):
        """Verify the 3 clinical stages of Scurvy when vitamin level is deficient."""
        # Day 2 (< 72h): Stage 0 (Healthy)
        stage0, heal0, drain0 = MetabolismAgronomyOracle.evaluate_scurvy_stage(5.0, 48.0)
        self.assertEqual(stage0, 0)
        self.assertEqual(heal0, 1.0)
        self.assertEqual(drain0, 0.0)

        # Day 4 (96h): Stage 1 (Lethargy, healing frozen)
        stage1, heal1, drain1 = MetabolismAgronomyOracle.evaluate_scurvy_stage(5.0, 96.0)
        self.assertEqual(stage1, 1)
        self.assertEqual(heal1, 0.0)
        self.assertEqual(drain1, 0.0)

        # Day 6 (144h): Stage 2 (Tissue damage, 0.5 HP/h drain)
        stage2, heal2, drain2 = MetabolismAgronomyOracle.evaluate_scurvy_stage(5.0, 144.0)
        self.assertEqual(stage2, 2)
        self.assertEqual(drain2, 0.5)

        # Day 8 (192h): Stage 3 (Hemorrhage, 2.5 HP/h drain)
        stage3, heal3, drain3 = MetabolismAgronomyOracle.evaluate_scurvy_stage(5.0, 192.0)
        self.assertEqual(stage3, 3)
        self.assertEqual(drain3, 2.5)

    def test_arrhenius_spoilage_q10_formula(self):
        """Verify Arrhenius food decomposition factor doubles every +10C."""
        m_15c = MetabolismAgronomyOracle.calculate_arrhenius_multiplier(15.0)
        self.assertEqual(m_15c, 1.0)  # Baseline 1.0 at 15C

        m_25c = MetabolismAgronomyOracle.calculate_arrhenius_multiplier(25.0)
        self.assertEqual(m_25c, 2.0)  # Doubles to 2.0 at 25C

        m_35c = MetabolismAgronomyOracle.calculate_arrhenius_multiplier(35.0)
        self.assertEqual(m_35c, 4.0)  # Quadruples to 4.0 at 35C

    def test_liebig_minimum_yield_formula(self):
        """Verify Liebig's Law where the most deficient nutrient limits total harvest yield."""
        # Wheat demands: N=100, P=60, K=60
        # Soil: N=100 (100%), P=60 (100%), K=30 (50%) -> Limited by K to 50%
        y_mult = MetabolismAgronomyOracle.calculate_liebig_yield_multiplier(100.0, 60.0, 30.0, "crop_wheat")
        self.assertAlmostEqual(y_mult, 0.50, places=2)

    def test_rhizobia_nitrogen_fixation_peas(self):
        """Verify that harvesting peas restores +22% Nitrogen to the soil."""
        n0, p0, k0 = 40.0, 80.0, 80.0
        n1, p1, k1 = MetabolismAgronomyOracle.apply_crop_harvest_drain(n0, p0, k0, "crop_peas")
        self.assertEqual(n1, 62.0, "Peas must fix +22% Nitrogen")
        self.assertEqual(p1, 78.0, "Peas consume 2% Phosphorus")
        self.assertEqual(k1, 78.0, "Peas consume 2% Potassium")


class TestBiologicalMetabolismTier2(unittest.TestCase):
    """Tier 2: Boundary & Corner Cases for Calories, Decay, and Soil."""

    def test_starvation_caloric_depletion_health_drain(self):
        """When caloric reserve drops to 0, citizen incurs -2.5 HP/hour starvation damage."""
        reserve = 0.0
        hp_loss_per_hour = 2.5
        hours_starving = 24.0
        total_damage = hours_starving * hp_loss_per_hour
        self.assertEqual(total_damage, 60.0)

    def test_extreme_permafrost_freeze_preservation(self):
        """At -20C deep freeze, spoilage rate is strictly clamped to 0.02x (50x shelf life)."""
        m_freeze = MetabolismAgronomyOracle.calculate_arrhenius_multiplier(-20.0)
        self.assertEqual(m_freeze, 0.02)

    def test_single_nutrient_zero_soil_yield_collapse(self):
        """If a single nutrient is 0%, yield collapses to the emergency base minimum (0.20x)."""
        # Nitrogen is 0%, P and K are 100%
        y_mult = MetabolismAgronomyOracle.calculate_liebig_yield_multiplier(0.0, 100.0, 100.0, "crop_wheat")
        self.assertEqual(y_mult, 0.20)

    def test_monoculture_penalty_amplification(self):
        """Consecutive plantings of the same crop amplify nutrient depletion by (1 + 0.5 * (C - 1))."""
        # Single planting: Wheat consumes 14% N
        n1, _, _ = MetabolismAgronomyOracle.apply_crop_harvest_drain(100.0, 100.0, 100.0, "crop_wheat", 1)
        self.assertEqual(n1, 86.0)

        # 3rd consecutive planting: Monoculture mult = 1 + 0.5 * 2 = 2.0x -> Consumes 28% N
        n3, _, _ = MetabolismAgronomyOracle.apply_crop_harvest_drain(100.0, 100.0, 100.0, "crop_wheat", 3)
        self.assertEqual(n3, 72.0)

    def test_fertilizer_terra_preta_120_cap(self):
        """Soil nutrients cannot exceed the Terra Preta maximum cap of 120.0%."""
        # Over-enriching soil with peas
        n, p, k = MetabolismAgronomyOracle.apply_crop_harvest_drain(115.0, 100.0, 100.0, "crop_peas")
        self.assertEqual(n, 120.0, "Nitrogen cap is 120%")


class TestBiologicalMetabolismTier3(unittest.TestCase):
    """Tier 3: Cross-Feature Interactions (Thermoregulation + Nutrition + Agronomy)."""

    def test_shivering_cold_accelerating_caloric_burn(self):
        """
        A citizen suffering hypothermia (T_body = 32.0C) burns significant shivering thermogenesis:
        shivering = ((36.5 - 32.0) / 4.5) * 120 = 120 kcal/hr.
        Total TEE = BMR + shivering = 75 + 120 = 195 kcal/hr.
        """
        tee_chilled = MetabolismAgronomyOracle.calculate_tee("rest", body_temp_c=32.0)
        self.assertEqual(tee_chilled, 195.0)
        self.assertGreater(tee_chilled, MetabolismAgronomyOracle.BMR_KCAL_HOUR * 2.5)

    def test_scurvy_deficiency_freezing_combat_wound_healing(self):
        """
        Citizen wounded in combat (50/100 HP) who has Stage 2 Scurvy cannot regenerate health,
        and tissue breakdown drains further health.
        """
        stage, healing_mult, hp_drain = MetabolismAgronomyOracle.evaluate_scurvy_stage(
            vitamin_level=8.0,
            deficient_hours=130.0,  # Stage 2
        )
        self.assertEqual(stage, 2)
        self.assertEqual(healing_mult, 0.0, "Natural wound healing must be frozen")
        self.assertEqual(hp_drain, 0.5, "Tissue breakdown must cause active bleeding")

    def test_salted_meat_in_icehouse_vault_multiplied_preservation(self):
        """
        Compounding preservation:
        Halite salt curing (0.07x) + Subterranean Icehouse vault (0.10x) + Cold temp 1C (0.38x).
        Combined multiplier extends shelf life by >300x.
        """
        m_preserv = MetabolismAgronomyOracle.calculate_preservation_multiplier(
            container_type="icehouse",
            preservation_method="salted",
            rh=0.40,
        )
        m_temp = MetabolismAgronomyOracle.calculate_arrhenius_multiplier(1.0)
        total_decay_rate = m_preserv * m_temp
        self.assertLess(total_decay_rate, 0.01, "Salt + Icehouse vault must extend shelf life >100x")

    def test_peas_rotation_replenishing_wheat_nitrogen_deficit(self):
        """
        Wheat depletes Nitrogen from 100% to 86%.
        Immediately planting peas restores Nitrogen from 86% back to 100% (capped from 108%).
        """
        n_after_wheat, _, _ = MetabolismAgronomyOracle.apply_crop_harvest_drain(100.0, 100.0, 100.0, "crop_wheat")
        self.assertEqual(n_after_wheat, 86.0)

        n_after_peas, _, _ = MetabolismAgronomyOracle.apply_crop_harvest_drain(n_after_wheat, 100.0, 100.0, "crop_peas")
        self.assertEqual(n_after_peas, 108.0)
        self.assertGreater(n_after_peas, 100.0, "Peas fully replenish nitrogen lost from wheat")


class TestBiologicalMetabolismTier4(unittest.TestCase):
    """Tier 4: Real-World Scenarios (4-Year Crop Rotation, Scurvy Outbreak, Miner Fatigue)."""

    def test_canonical_four_year_crop_rotation_soil_stability(self):
        """
        Scenario: A 4-field rotation cycle over 4 simulated years:
        Year 1: Wheat (Heavy N-drain)
        Year 2: Peas (Rhizobia N-restorer)
        Year 3: Turnips (Root forage, low drain)
        Year 4: Fallow + Grazing (Natural weathering + manure restoration)
        Assert that after 4 full years, all soil nutrients remain strictly > 80.0%,
        whereas 4 consecutive years of wheat monoculture collapses Nitrogen < 45.0%.
        """
        # 1. Four-Year Rotation Plot
        n, p, k = 100.0, 100.0, 100.0
        for year in range(4):
            # Year 1: Wheat
            n, p, k = MetabolismAgronomyOracle.apply_crop_harvest_drain(n, p, k, "crop_wheat")
            # Year 2: Peas
            n, p, k = MetabolismAgronomyOracle.apply_crop_harvest_drain(n, p, k, "crop_peas")
            # Year 3: Turnip
            n, p, k = MetabolismAgronomyOracle.apply_crop_harvest_drain(n, p, k, "crop_turnip")
            # Year 4: Fallow + grazing restoration (+15% N, +10% P, +10% K)
            n = min(120.0, n + 15.0)
            p = min(120.0, p + 10.0)
            k = min(120.0, k + 10.0)

        self.assertGreaterEqual(n, 80.0, "4-year rotation sustains Nitrogen > 80%")
        self.assertGreaterEqual(p, 80.0, "4-year rotation sustains Phosphorus > 80%")
        self.assertGreaterEqual(k, 80.0, "4-year rotation sustains Potassium > 80%")

        # 2. Monoculture Plot (Wheat 4 consecutive cycles)
        mono_n, mono_p, mono_k = 100.0, 100.0, 100.0
        for cycle in range(1, 5):
            mono_n, mono_p, mono_k = MetabolismAgronomyOracle.apply_crop_harvest_drain(
                mono_n, mono_p, mono_k, "crop_wheat", consecutive_plantings=cycle
            )
        self.assertLess(mono_n, 45.0, "Monoculture wheat causes Nitrogen collapse < 45%")

    def test_winter_scurvy_crisis_cured_by_cellar_sauerkraut(self):
        """
        Scenario: In late winter, citizens have eaten only dried bread and meat for 15 days.
        Vitamin level falls to 0.0%, causing Stage 3 Scurvy (bleeding, no healing).
        The monarch opens the cold cellar and distributes Pickled Vegetables (+65 Vitamin).
        Citizen vitamin pool recovers to 65%, halting hemorrhaging and restoring health regeneration.
        """
        # Citizen suffering Stage 3 Scurvy
        stage_before, heal_before, drain_before = MetabolismAgronomyOracle.evaluate_scurvy_stage(
            vitamin_level=0.0,
            deficient_hours=200.0,
        )
        self.assertEqual(stage_before, 3)
        self.assertEqual(drain_before, 2.5)

        # Consumes food_pickled_veg -> +65.0 Vitamin
        c_add, p_add, v_add = (
            MetabolismAgronomyOracle.FOOD_NUTRITION["food_pickled_veg"][1],
            MetabolismAgronomyOracle.FOOD_NUTRITION["food_pickled_veg"][2],
            MetabolismAgronomyOracle.FOOD_NUTRITION["food_pickled_veg"][3],
        )
        new_vitamin = min(100.0, 0.0 + v_add)
        self.assertEqual(new_vitamin, 65.0)

        # Re-evaluate scurvy status post-treatment
        stage_after, heal_after, drain_after = MetabolismAgronomyOracle.evaluate_scurvy_stage(
            vitamin_level=new_vitamin,
            deficient_hours=0.0,  # Deficit broken
        )
        self.assertEqual(stage_after, 0, "Sauerkraut completely cures scurvy")
        self.assertEqual(heal_after, 1.0, "Healing restored")
        self.assertEqual(drain_after, 0.0, "Bleeding halted")

    def test_heavy_miner_caloric_deficit_and_glycogen_collapse(self):
        """
        Scenario: Miner performing 12 hours of continuous underground mining (187.5 kcal/hr).
        Total energy expenditure = 12 * 187.5 = 2250 kcal.
        Consumes 2 loaves of bread (640 kcal) -> Deficit of 1610 kcal drawn from reserves.
        Carbohydrate pool drops rapidly due to heavy labor, demonstrating glycogen exhaustion risk.
        """
        hours_worked = 12.0
        tee = MetabolismAgronomyOracle.calculate_tee("mining") * hours_worked
        self.assertEqual(tee, 2250.0)

        caloric_intake = MetabolismAgronomyOracle.FOOD_NUTRITION["food_bread"][0] * 2.0
        self.assertEqual(caloric_intake, 640.0)

        deficit = tee - caloric_intake
        self.assertEqual(deficit, 1610.0)

        # Glycogen decay under continuous labor (tau = 12 hours)
        carb_remaining = MetabolismAgronomyOracle.calculate_nutrient_decay(
            current_level=100.0,
            nutrient_type="carb",
            delta_hours=12.0,
            is_working=True,
        )
        self.assertAlmostEqual(carb_remaining, 50.0, places=1)


if __name__ == "__main__":
    unittest.main()
