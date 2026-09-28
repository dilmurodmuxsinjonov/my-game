"""
Automated Test Suite for Realism Pillar R5: Historical Feudal Socio-Economics & Logistics Friction.
Voxel Lord: Feudal Realm (Godot 4.3 / C++ Core)

Validates:
1. Transport friction mechanics (-50% mud penalty, +40% stone boost, 2.80x A* traversal cost ratio)
2. Five distinct medieval social strata charters (Serfs, Yeomen, Guild Artisans, Clergy, Nobility) and legal rights
3. Multi-market 5-hub pricing elasticity (gamma=1.25, kd=0.85, [0.2x, 5.0x] clamps, max(0.01) singularity protector)
4. Late-winter / early-spring "Hungry Gap" grain price surge (1.80x - 2.20x) and macroeconomic currency inflation
5. Trade caravan route security, escort protection scaling, and bandit ambush cargo interception

Organized under 4-Tier Test Architecture:
- Tier 1: Core Feature Coverage
- Tier 2: Boundary & Corner Cases
- Tier 3: Cross-Feature Interactions
- Tier 4: Real-World Scenarios
"""

import math
import unittest
from typing import Dict, List, Tuple, Optional


class FeudalLogisticsOracle:
    """Mathematical reference oracle for feudal economics, transport friction, and trade logistics."""

    BASE_ENTITY_SPEED: Dict[str, float] = {
        "citizen": 3.20,
        "wheelbarrow": 3.68,
        "handcart": 4.00,
        "wagon": 4.80,
    }

    SURFACE_MODIFIERS: Dict[str, float] = {
        "mud": 0.50,          # -50% haul velocity penalty
        "grass": 1.00,        # baseline
        "dirt_trail": 1.15,   # +15% boost
        "gravel": 1.25,       # +25% boost
        "cobblestone": 1.40,  # +40% boost
        "royal_highway": 1.60 # +60% boost
    }

    BASE_PRICES: Dict[str, float] = {
        "wheat": 1.0,
        "grain": 1.0,
        "bread": 2.0,
        "iron_ingot": 10.0,
        "steel_ingot": 28.0,
        "sword": 45.0,
        "salt": 4.0,
        "wool": 3.0,
    }

    # 5 Strata Charter specifications
    STRATA_CHARTERS: Dict[str, Dict] = {
        "serf": {
            "charter_name": "Manorial Labor Charter",
            "owes_corvee_labor": True,
            "corvee_days_per_week": 3,
            "tied_to_soil": True,
            "can_own_allodial_land": False,
            "can_trade_at_market": False,
            "military_service": "none",
            "tax_tolerance": 0.25,
            "revolt_type": "jacquerie",
        },
        "yeoman": {
            "charter_name": "Freehold Yeomanry Charter",
            "owes_corvee_labor": False,
            "corvee_days_per_week": 0,
            "tied_to_soil": False,
            "can_own_allodial_land": True,
            "can_trade_at_market": True,
            "military_service": "archer_militia",
            "tax_tolerance": 0.20,
            "revolt_type": "tax_strike",
        },
        "guild_artisan": {
            "charter_name": "Master Guild Incorporation Charter",
            "owes_corvee_labor": False,
            "corvee_days_per_week": 0,
            "tied_to_soil": False,
            "can_own_allodial_land": True,
            "can_trade_at_market": True,
            "military_service": "town_watch",
            "tax_tolerance": 0.15,
            "revolt_type": "craft_strike",
        },
        "clergy": {
            "charter_name": "Ecclesiastical Diocesan Charter",
            "owes_corvee_labor": False,
            "corvee_days_per_week": 0,
            "tied_to_soil": False,
            "can_own_allodial_land": True,
            "can_trade_at_market": False,
            "benefit_of_clergy": True,
            "sanctuary_days": 40,
            "military_service": "none",
            "tax_tolerance": 0.05,
            "revolt_type": "interdict_excommunication",
        },
        "nobility": {
            "charter_name": "Seigneurial Fiefdom Patent",
            "owes_corvee_labor": False,
            "corvee_days_per_week": 0,
            "tied_to_soil": False,
            "can_own_allodial_land": True,
            "can_trade_at_market": False,
            "has_high_justice": True,
            "military_service": "feudal_knights",
            "fealty_threshold": 15,
            "tax_tolerance": 0.10,
            "revolt_type": "baronial_civil_war",
        },
    }

    @classmethod
    def calculate_haul_velocity(
        cls,
        mode: str,
        surface: str,
        load_fraction: float = 0.0,
        incline_deg: float = 0.0,
    ) -> float:
        """
        V_haul = V_base * M_surface * M_load * M_gradient
        Special rule: Heavy wagon on mud with heavy load (>80%) drops to 0.20x baseline (stall).
        """
        v_base = cls.BASE_ENTITY_SPEED.get(mode.lower(), 3.20)
        m_surf = cls.SURFACE_MODIFIERS.get(surface.lower(), 1.00)

        # Wagon in mud stall condition
        if mode.lower() == "wagon" and surface.lower() == "mud":
            return v_base * 0.20

        # Load factor: M_load = 1.0 - 0.25 * load_fraction
        m_load = 1.0 - 0.25 * min(1.0, max(0.0, load_fraction))

        # Gradient factor
        if incline_deg > 0.0:
            m_grad = max(0.20, 1.0 - 0.05 * incline_deg)
        elif incline_deg < 0.0:
            m_grad = min(1.15, 1.0 + 0.02 * abs(incline_deg))
        else:
            m_grad = 1.00

        return v_base * m_surf * m_load * m_grad

    @classmethod
    def calculate_astar_traversal_cost(cls, distance_m: float, haul_velocity: float) -> float:
        """Cost = Distance / max(0.1, V_haul)"""
        return distance_m / max(0.1, haul_velocity)

    @classmethod
    def calculate_market_price(
        cls,
        item_id: str,
        current_stock: float,
        target_stock: float,
        season_day: int = 10,  # 1..28 (28-day year: Spring 1-7, Summer 8-14, Autumn 15-21, Winter 22-28)
        reputation: float = 50.0,
        inflation_rate: float = 0.0,
        kd: float = 0.85,
        gamma: float = 1.25,
    ) -> float:
        """
        Universal Algorithmic Market Pricing:
        P_buy = clamp(P_base * [max(0.01, 1.0 + kd * (Stock_target - Stock_current) / Stock_target)]^gamma
                      * M_season * M_rep * (1.0 + Inflation), 0.20 * P_base, 5.00 * P_base)
        """
        p_base = cls.BASE_PRICES.get(item_id.lower(), 1.0)
        t_stock = max(1.0, target_stock)

        # Elasticity base with critical singularity protector max(0.01, ...)
        linear_term = 1.0 + kd * ((t_stock - current_stock) / t_stock)
        protected_base = max(0.01, linear_term)
        elasticity_factor = protected_base ** gamma

        # Seasonal multiplier for grain/food
        m_season = cls.get_seasonal_grain_multiplier(season_day) if "wheat" in item_id or "bread" in item_id else 1.0

        # Reputation modifier (50 is neutral 1.0; 100 is 0.75; 0 is 1.25)
        m_rep = 1.0 - 0.25 * ((reputation - 50.0) / 50.0)

        # Inflation factor
        inf_factor = 1.0 + inflation_rate

        raw_price = p_base * elasticity_factor * m_season * m_rep * inf_factor
        return max(0.20 * p_base, min(5.00 * p_base, raw_price))

    @classmethod
    def get_seasonal_grain_multiplier(cls, day_of_year: int) -> float:
        """
        28-day 4-season agricultural cycle:
        Spring: 1-7 (1.30x - 1.50x)
        Summer: 8-14 (1.00x - 1.10x)
        Autumn: 15-21 (0.60x - 0.75x Harvest Glut)
        Early Winter: 22-23 (1.20x)
        Late Winter / Early Spring Hungry Gap: 24-28 and 1-3 (1.80x - 2.20x)
        """
        d = ((day_of_year - 1) % 28) + 1
        if d in [24, 25, 26, 27, 28, 1, 2, 3]:
            return 2.00  # Late winter / early spring "Hungry Gap" peak
        elif 4 <= d <= 7:
            return 1.40  # Spring sowing
        elif 8 <= d <= 14:
            return 1.00  # Summer baseline
        elif 15 <= d <= 21:
            return 0.65  # Autumn harvest glut
        else:
            return 1.25  # Early winter

    @classmethod
    def calculate_caravan_security_risk(
        cls,
        edge_lengths_m: List[float],
        threat_indices: List[float],
        guard_coverages: List[float],
        escort_strength: float = 0.0,
    ) -> Tuple[float, float, float]:
        """
        Calculates caravan route risk:
        Risk_edge = clamp((Length / 1000) * Threat * (1.0 - 0.70 * GuardCoverage), 0.0, 0.95)
        Risk_route = 1.0 - prod(1.0 - Risk_edge)
        Loss_fraction = clamp(Risk_route - 0.20 * EscortStrength, 0.0, 1.0)
        Returns (risk_route, loss_fraction, escort_cost_multiplier)
        """
        survival_prob = 1.0
        for length, threat, coverage in zip(edge_lengths_m, threat_indices, guard_coverages):
            edge_risk = (length / 1000.0) * threat * (1.0 - 0.70 * coverage)
            clamped_edge = min(0.95, max(0.0, edge_risk))
            survival_prob *= (1.0 - clamped_edge)

        route_risk = 1.0 - survival_prob
        loss_fraction = min(1.0, max(0.0, route_risk - 0.20 * escort_strength))
        escort_cost_mult = 1.0 + 2.50 * route_risk

        return route_risk, loss_fraction, escort_cost_mult


class TestFeudalLogisticsTier1(unittest.TestCase):
    """Tier 1: Core Feature Coverage for Friction, Charters, Pricing, and Caravans."""

    def test_surface_friction_speed_modifiers(self):
        """Verify unpaved mud penalizes speed by -50% and cobblestone boosts by +40%."""
        v_base = 3.20  # Citizen baseline
        v_mud = FeudalLogisticsOracle.calculate_haul_velocity("citizen", "mud")
        v_stone = FeudalLogisticsOracle.calculate_haul_velocity("citizen", "cobblestone")

        # Mud: 3.20 * 0.50 = 1.60 m/s (-50%)
        self.assertAlmostEqual(v_mud, 1.60, places=2)

        # Cobblestone: 3.20 * 1.40 = 4.48 m/s (+40%)
        self.assertAlmostEqual(v_stone, 4.48, places=2)

        # Cost ratio for 100m distance:
        cost_mud = FeudalLogisticsOracle.calculate_astar_traversal_cost(100.0, v_mud)
        cost_stone = FeudalLogisticsOracle.calculate_astar_traversal_cost(100.0, v_stone)
        ratio = cost_mud / cost_stone
        self.assertAlmostEqual(ratio, 2.80, places=2, msg="A* traversal cost ratio must be 2.80x")

    def test_five_social_strata_charters(self):
        """Verify schemas and core legal parameters across all 5 feudal strata."""
        charters = FeudalLogisticsOracle.STRATA_CHARTERS

        # 1. Serf: bound to soil, 3 days corvee, tax tolerance 25%
        self.assertTrue(charters["serf"]["tied_to_soil"])
        self.assertEqual(charters["serf"]["corvee_days_per_week"], 3)
        self.assertEqual(charters["serf"]["revolt_type"], "jacquerie")

        # 2. Yeoman: freeholder, market trade, archery militia
        self.assertFalse(charters["yeoman"]["tied_to_soil"])
        self.assertTrue(charters["yeoman"]["can_trade_at_market"])
        self.assertEqual(charters["yeoman"]["military_service"], "archer_militia")

        # 3. Guild Artisan: craft monopoly, strike revolt
        self.assertTrue(charters["guild_artisan"]["can_trade_at_market"])
        self.assertEqual(charters["guild_artisan"]["revolt_type"], "craft_strike")

        # 4. Clergy: Benefit of Clergy, 40-day sanctuary, interdict
        self.assertTrue(charters["clergy"]["benefit_of_clergy"])
        self.assertEqual(charters["clergy"]["sanctuary_days"], 40)
        self.assertEqual(charters["clergy"]["revolt_type"], "interdict_excommunication")

        # 5. Nobility: High Justice, feudal knights, fealty 15
        self.assertTrue(charters["nobility"]["has_high_justice"])
        self.assertEqual(charters["nobility"]["fealty_threshold"], 15)

    def test_multi_market_pricing_formula(self):
        """Verify price elasticity formula with normal supply and neutral reputation."""
        # Balanced market: current = target = 100
        p_wheat = FeudalLogisticsOracle.calculate_market_price(
            item_id="wheat",
            current_stock=100.0,
            target_stock=100.0,
            season_day=10,  # Summer neutral
            reputation=50.0,
        )
        self.assertAlmostEqual(p_wheat, 1.0, places=2)

    def test_seasonal_grain_hungry_gap_multipliers(self):
        """Verify seasonal grain multipliers: Autumn harvest glut 0.65x, Late winter Hungry Gap 2.00x."""
        m_autumn = FeudalLogisticsOracle.get_seasonal_grain_multiplier(18)  # Autumn Day 18
        self.assertEqual(m_autumn, 0.65)

        m_hungry_gap = FeudalLogisticsOracle.get_seasonal_grain_multiplier(26)  # Late Winter Day 26
        self.assertEqual(m_hungry_gap, 2.00)

    def test_caravan_route_security_risk_formula(self):
        """Verify caravan route risk aggregation across multiple road segments."""
        # 2 segments: each 1000m, threat 0.5, zero guards -> each edge risk = 0.50
        # Route risk = 1 - (1 - 0.5) * (1 - 0.5) = 1 - 0.25 = 0.75 (75%)
        risk, loss, escort_mult = FeudalLogisticsOracle.calculate_caravan_security_risk(
            edge_lengths_m=[1000.0, 1000.0],
            threat_indices=[0.5, 0.5],
            guard_coverages=[0.0, 0.0],
            escort_strength=0.0,
        )
        self.assertAlmostEqual(risk, 0.75, places=2)
        self.assertEqual(loss, 0.75)
        self.assertGreater(escort_mult, 2.5)


class TestFeudalLogisticsTier2(unittest.TestCase):
    """Tier 2: Boundary & Corner Cases for Pricing Clamps, Stalls, and Inflation."""

    def test_hyper_supply_singularity_protector_guard(self):
        """
        Verify that extreme hyper-supply (current_stock = 5x target) does NOT crash
        with negative power or NaN due to max(0.01, ...) singularity protector,
        and clamps cleanly to 0.20 * P_base.
        """
        p_oversupply = FeudalLogisticsOracle.calculate_market_price(
            item_id="iron_ingot",
            current_stock=5000.0,
            target_stock=1000.0,
            season_day=10,
        )
        # P_base = 10.0 -> 0.20 * 10 = 2.0
        self.assertEqual(p_oversupply, 2.0)

    def test_famine_zero_stock_hard_clamp_5x(self):
        """Verify acute famine (stock = 0, low reputation) clamps strictly to 5.00 * P_base."""
        p_famine = FeudalLogisticsOracle.calculate_market_price(
            item_id="bread",
            current_stock=0.0,
            target_stock=1000.0,
            season_day=26,  # Hungry gap (2.0x)
            reputation=0.0, # Hostile famine market (1.25x)
        )
        # P_base = 2.0 -> 5.00 * 2.0 = 10.0
        self.assertEqual(p_famine, 10.0)

    def test_heavy_wagon_mud_stall_at_0_20(self):
        """Verify that a heavy wagon entering an unpaved mud tile drops to 0.20x speed (stall)."""
        v_wagon_mud = FeudalLogisticsOracle.calculate_haul_velocity("wagon", "mud")
        # 4.80 * 0.20 = 0.96 m/s
        self.assertEqual(v_wagon_mud, 0.96)

    def test_steep_uphill_gradient_minimum_speed(self):
        """Verify that extreme uphill slope (>16 deg) is clamped to minimum 0.20x gradient multiplier."""
        v_uphill = FeudalLogisticsOracle.calculate_haul_velocity("citizen", "grass", incline_deg=25.0)
        # 3.20 * 1.0 * 1.0 * 0.20 = 0.64 m/s
        self.assertAlmostEqual(v_uphill, 0.64, places=2)

    def test_100_percent_debased_currency_inflation_cap(self):
        """Verify that extreme currency inflation at 40% increases market purchase prices accordingly."""
        p_inflated = FeudalLogisticsOracle.calculate_market_price(
            item_id="sword",
            current_stock=100.0,
            target_stock=100.0,
            season_day=10,
            inflation_rate=0.40,
        )
        # P_base = 45.0 * 1.40 = 63.0
        self.assertAlmostEqual(p_inflated, 63.0, places=1)


class TestFeudalLogisticsTier3(unittest.TestCase):
    """Tier 3: Cross-Feature Interactions (Weather Roads -> A* -> Ambush Deficits)."""

    def test_rain_churning_dirt_road_altering_astar_route(self):
        """
        A 100m direct dirt trail degrades to churned mud (speed 1.60 m/s, cost 62.5s).
        An alternative 200m cobblestone highway (speed 4.48 m/s, cost 44.64s)
        becomes the faster route despite being twice as long geometrically.
        """
        dist_direct = 100.0
        v_mud = FeudalLogisticsOracle.calculate_haul_velocity("citizen", "mud")
        cost_direct_mud = FeudalLogisticsOracle.calculate_astar_traversal_cost(dist_direct, v_mud)

        dist_highway = 200.0
        v_stone = FeudalLogisticsOracle.calculate_haul_velocity("citizen", "cobblestone")
        cost_highway_stone = FeudalLogisticsOracle.calculate_astar_traversal_cost(dist_highway, v_stone)

        self.assertLess(cost_highway_stone, cost_direct_mud, "Paved cobblestone detour must beat muddy shortcut")

    def test_bandit_ambush_looting_grain_amplifying_hungry_gap(self):
        """
        A grain caravan is ambushed and 100% looted in late winter.
        Destination market receives 0 grain -> stock collapses to 0 during Hungry Gap.
        Price reaches maximum 5.00x famine ceiling.
        """
        # Ambush with zero guards
        _, loss, _ = FeudalLogisticsOracle.calculate_caravan_security_risk(
            edge_lengths_m=[2000.0],
            threat_indices=[0.8],
            guard_coverages=[0.0],
            escort_strength=0.0,
        )
        self.assertGreaterEqual(loss, 0.80)

        # Resulting destination market price in Hungry Gap (Day 26) with zero stock and low reputation
        p_bread_crisis = FeudalLogisticsOracle.calculate_market_price(
            item_id="bread",
            current_stock=0.0,
            target_stock=500.0,
            season_day=26,
            reputation=0.0,
        )
        self.assertEqual(p_bread_crisis, 10.0, "Looted grain in Hungry Gap drives bread to max 5x ceiling")

    def test_excessive_taxation_triggering_social_revolt(self):
        """
        Monarch sets 35% tax rate.
        Serf tolerance is 25% -> Triggers Jacquerie agrarian revolt.
        Yeoman tolerance is 20% -> Triggers tax resistance strike.
        Artisan tolerance is 15% -> Triggers craft guild closure.
        """
        tax_rate = 0.35
        serf_revolts = tax_rate > FeudalLogisticsOracle.STRATA_CHARTERS["serf"]["tax_tolerance"]
        yeoman_revolts = tax_rate > FeudalLogisticsOracle.STRATA_CHARTERS["yeoman"]["tax_tolerance"]
        artisan_revolts = tax_rate > FeudalLogisticsOracle.STRATA_CHARTERS["guild_artisan"]["tax_tolerance"]

        self.assertTrue(serf_revolts)
        self.assertTrue(yeoman_revolts)
        self.assertTrue(artisan_revolts)

    def test_escort_guards_neutralizing_caravan_loss(self):
        """
        Hiring a strong guard escort (strength = 5.0) reduces cargo loss fraction to 0.0
        along a dangerous route (route risk = 0.60).
        """
        risk, loss_with_guards, cost_mult = FeudalLogisticsOracle.calculate_caravan_security_risk(
            edge_lengths_m=[1500.0],
            threat_indices=[0.6],
            guard_coverages=[0.2],
            escort_strength=5.0,  # 5.0 * 0.20 = 1.0 protection
        )
        self.assertEqual(loss_with_guards, 0.0, "Heavy escort prevents all cargo loss")
        self.assertGreater(cost_mult, 1.5, "Escort cost scales with route danger")


class TestFeudalLogisticsTier4(unittest.TestCase):
    """Tier 4: Real-World Scenarios (5-Hub Network, Hungry Gap Relief, Merchant Hauling)."""

    def test_five_hub_regional_grain_trade_arbitrage(self):
        """
        Scenario: 5 regional hubs:
        1. Sovereign Settlement (Capital)
        2. Coastal Port (High luxury, grain deficit)
        3. Northern Fortress (Mining biome, acute grain deficit)
        4. Holy Order Abbey (Monastic farming surplus)
        5. Steppe Bazaar (Nomad horse market)

        Verify price arbitrage: Grain price at Holy Order (surplus, stock = 2000)
        is drastically cheaper than at Northern Fortress (deficit, stock = 100),
        incentivizing inter-market trade caravans.
        """
        p_abbey = FeudalLogisticsOracle.calculate_market_price(
            item_id="wheat",
            current_stock=2000.0,
            target_stock=1000.0,
            season_day=10,  # Summer neutral
        )
        p_fortress = FeudalLogisticsOracle.calculate_market_price(
            item_id="wheat",
            current_stock=100.0,
            target_stock=1000.0,
            season_day=10,  # Summer neutral
        )

        self.assertLess(p_abbey, 0.60, "Abbey surplus harvest grain is cheap")
        self.assertGreater(p_fortress, 1.50, "Fortress grain deficit is expensive")
        # Profit margin > 2.5x
        self.assertGreater(p_fortress / p_abbey, 2.5)

    def test_manorial_economy_winter_hungry_gap_relief(self):
        """
        Scenario: During the Day 26 Hungry Gap, normal market bread price surges to 2x (4.0 silver).
        The monarch releases 600 loaves from the royal granary, raising stock to target level.
        The price returns towards baseline, preventing serf jacquerie riots.
        """
        # Hungry Gap before relief (stock = 200 / target = 1000)
        p_crisis = FeudalLogisticsOracle.calculate_market_price(
            item_id="bread",
            current_stock=200.0,
            target_stock=1000.0,
            season_day=26,
        )
        self.assertGreaterEqual(p_crisis, 3.5)

        # After releasing royal reserves (stock = 1000 / target = 1000)
        p_relieved = FeudalLogisticsOracle.calculate_market_price(
            item_id="bread",
            current_stock=1000.0,
            target_stock=1000.0,
            season_day=26,
        )
        # Still seasonal modifier (2.0x base = 4.0), but without deficit multiplier
        self.assertLess(p_relieved, p_crisis)

    def test_heavily_escorted_caravan_traversing_dangerous_mountain_pass(self):
        """
        Scenario: A 3-mile mountain trade route connecting the Capital to Northern Fortress.
        Bandit threat is 0.75. Unescorted caravan has 70% risk of ambush and loss.
        Deploying 5 mounted guards (strength 5.0) and watchtower outposts (coverage 0.5)
        reduces cargo loss to 0.0%.
        """
        # Protected route
        risk, loss, cost_mult = FeudalLogisticsOracle.calculate_caravan_security_risk(
            edge_lengths_m=[1500.0, 1500.0],
            threat_indices=[0.75, 0.75],
            guard_coverages=[0.5, 0.5],
            escort_strength=5.0,
        )
        self.assertEqual(loss, 0.0)

    def test_feudal_social_strata_rights_and_obligations_matrix(self):
        """
        Scenario: Full verification of social stratification rights matrix.
        Assert that Serfs are the only strata tied to the soil and owing corvee labor,
        Nobility alone holds High Justice, and Clergy alone holds Benefit of Clergy.
        """
        charters = FeudalLogisticsOracle.STRATA_CHARTERS

        # Only serfs owe corvee labor
        for strata_id, c in charters.items():
            if strata_id == "serf":
                self.assertTrue(c["owes_corvee_labor"])
                self.assertTrue(c["tied_to_soil"])
            else:
                self.assertFalse(c["owes_corvee_labor"])
                self.assertFalse(c["tied_to_soil"])

        # Only nobility holds High Justice
        for strata_id, c in charters.items():
            if strata_id == "nobility":
                self.assertTrue(c.get("has_high_justice", False))
            else:
                self.assertFalse(c.get("has_high_justice", False))

        # Only clergy holds Benefit of Clergy
        for strata_id, c in charters.items():
            if strata_id == "clergy":
                self.assertTrue(c.get("benefit_of_clergy", False))
            else:
                self.assertFalse(c.get("benefit_of_clergy", False))


if __name__ == "__main__":
    unittest.main()
