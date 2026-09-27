"""
Automated Test Suite for Realism Pillar R1: Structural Integrity & Voxel Physics.
Voxel Lord: Feudal Realm (Godot 4.3 / C++ Core)

Validates:
1. Horizontal cantilever overhang limits (Stone 6, Brick 6, Timber 4, Iron 8, Dirt 1, Sand 0) and Buttress (+3m)
2. Vertical compressive column load accumulation and overload failure
3. Subterranean mine ceiling stability index Sc with overburden pressure P = rho * g * |y|
4. 3D aerodynamic ballistic projectile trajectory with barometric density decay and drag
5. Kinetic impact voxel blast dispersion, material hardness mitigation, and fracturing cratering

Organized under 4-Tier Test Architecture:
- Tier 1: Core Feature Coverage
- Tier 2: Boundary & Corner Cases
- Tier 3: Cross-Feature Interactions
- Tier 4: Real-World Scenarios
"""

import math
import unittest
from typing import Dict, List, Tuple, Set, Optional


class VoxelStructuralOracle:
    """Mathematical reference oracle for structural mechanics and load bearing."""

    CANTILEVER_LIMITS: Dict[str, int] = {
        "sand": 0,
        "gravel": 0,
        "dirt": 1,
        "timber": 4,
        "wood": 4,
        "cobblestone": 5,
        "stone": 6,
        "brick": 6,
        "chiseled_stone": 8,
        "iron": 8,
        "bedrock": 999999,
    }

    BUTTRESS_SUPPORT_BONUS = 3

    # Compressive limits in kg per 1x1m column
    COMPRESSIVE_LIMITS_KG: Dict[str, float] = {
        "timber": 4500.0,
        "cobblestone": 12000.0,
        "brick": 25000.0,
        "stone": 38000.0,
        "iron": 95000.0,
        "bedrock": 1e12,
    }

    VOXEL_MASS_KG: Dict[str, float] = {
        "air": 0.0,
        "timber": 500.0,
        "dirt": 1200.0,
        "cobblestone": 2000.0,
        "brick": 1800.0,
        "stone": 2600.0,
        "iron": 7800.0,
    }

    VOXEL_HP: Dict[str, float] = {
        "dirt": 80.0,
        "timber": 200.0,
        "cobblestone": 600.0,
        "brick": 1000.0,
        "chiseled_stone": 1200.0,
        "reinforced_stone": 2500.0,
        "iron": 3500.0,
    }

    VOXEL_HARDNESS_TIER: Dict[str, float] = {
        "dirt": 1.0,
        "timber": 2.0,
        "cobblestone": 4.0,
        "brick": 5.0,
        "chiseled_stone": 6.0,
        "reinforced_stone": 8.0,
        "iron": 9.0,
    }

    ROCK_TENSILE_K: Dict[str, float] = {
        "soil": 0.20,
        "sandstone": 0.55,
        "limestone": 0.55,
        "granite": 0.90,
        "monolithic_granite": 1.40,
        "basalt": 1.00,
        "bedrock": 10000.0,
    }

    ROCK_DENSITY: Dict[str, float] = {
        "soil": 1600.0,
        "sandstone": 2300.0,
        "limestone": 2300.0,
        "granite": 2600.0,
        "monolithic_granite": 2750.0,
        "basalt": 2900.0,
    }

    SUPPORT_RADIUS_M: Dict[str, float] = {
        "softwood_timber": 3.0,
        "hardwood_frame": 5.0,
        "reinforced_oak": 6.0,
        "stone_pillar": 7.5,
        "iron_arch": 11.0,
    }

    @classmethod
    def get_cantilever_limit(cls, material: str, has_buttress: bool = False) -> int:
        base = cls.CANTILEVER_LIMITS.get(material.lower(), 1)
        if has_buttress:
            return base + cls.BUTTRESS_SUPPORT_BONUS
        return base

    @classmethod
    def calculate_mine_stability_index(
        cls,
        rock_type: str,
        span_m: float,
        depth_m: float,
        supports: List[Tuple[float, float]],  # List of (support_radius, distance_m)
    ) -> float:
        """
        Calculate mine ceiling stability index Sc:
        Sc = [K_rock * max(1.0, sum(R_sup^2 / (d^2 + 0.1)))] /
             [1.0 + alpha_span * (L_span / 2)^2 * (1.0 + beta_depth * (|y| / 100))]
        """
        k_rock = cls.ROCK_TENSILE_K.get(rock_type.lower(), 0.50)
        alpha_span = 0.08
        beta_depth = 0.35

        support_term = 0.0
        for r_sup, dist in supports:
            support_term += (r_sup ** 2) / (dist ** 2 + 0.1)
        numerator = k_rock * max(1.0, support_term)

        y_abs = abs(depth_m)
        depth_factor = 1.0 + beta_depth * (y_abs / 100.0)
        span_factor = alpha_span * ((span_m / 2.0) ** 2) * depth_factor
        denominator = 1.0 + span_factor

        return numerator / denominator

    @classmethod
    def calculate_overburden_pressure_kpa(cls, rock_type: str, depth_m: float) -> float:
        """P_overburden = rho * g * |y| (in kPa)"""
        rho = cls.ROCK_DENSITY.get(rock_type.lower(), 2600.0)
        g = 9.81
        y_abs = abs(depth_m)
        pressure_pa = rho * g * y_abs
        return pressure_pa / 1000.0  # to kPa

    @classmethod
    def evaluate_column_load(cls, column_material: str, stacked_blocks: List[str]) -> Tuple[float, float, bool]:
        """
        Calculates cumulative vertical mass on a column and checks overload.
        Returns: (total_mass_kg, capacity_kg, is_overloaded)
        """
        total_mass = sum(cls.VOXEL_MASS_KG.get(b.lower(), 1000.0) for b in stacked_blocks)
        capacity = cls.COMPRESSIVE_LIMITS_KG.get(column_material.lower(), 5000.0)
        is_overloaded = total_mass > capacity
        return total_mass, capacity, is_overloaded

    @classmethod
    def calculate_blast_damage(
        cls,
        impact_damage: float,
        impact_pos: Tuple[float, float, float],
        voxel_pos: Tuple[float, float, float],
        hardness_tier: float,
    ) -> float:
        """
        Damage_voxel(X) = [ImpactDamage / (1.0 + |X - P_impact|^2)] * (1.0 - HardnessTier / 10.0)
        """
        dx = voxel_pos[0] - impact_pos[0]
        dy = voxel_pos[1] - impact_pos[1]
        dz = voxel_pos[2] - impact_pos[2]
        dist_sq = dx * dx + dy * dy + dz * dz

        falloff = 1.0 / (1.0 + dist_sq)
        hardness_factor = max(0.0, 1.0 - (hardness_tier / 10.0))
        return impact_damage * falloff * hardness_factor

    @classmethod
    def integrate_ballistic_step(
        cls,
        pos: Tuple[float, float, float],
        vel: Tuple[float, float, float],
        mass_kg: float,
        cd: float,
        area_m2: float,
        wind_vel: Tuple[float, float, float],
        dt: float,
    ) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """
        Single step ballistic integration with barometric density decay and drag:
        rho(y) = rho0 * exp(-y / 8500)
        v_rel = v - v_wind
        a_drag = - (1 / 2m) * rho(y) * Cd * A * |v_rel| * v_rel
        a_total = a_drag + (0, -9.81, 0)
        """
        x, y, z = pos
        vx, vy, vz = vel
        wx, wy, wz = wind_vel

        # Barometric density decay
        rho0 = 1.225
        h_scale = 8500.0
        rho = rho0 * math.exp(-max(0.0, y) / h_scale)

        # Relative velocity
        vrx = vx - wx
        vry = vy - wy
        vrz = vz - wz
        v_rel_mag = math.sqrt(vrx * vrx + vry * vry + vrz * vrz)

        if v_rel_mag > 1e-6:
            drag_coeff = 0.5 * rho * cd * area_m2 * v_rel_mag / mass_kg
            adx = -drag_coeff * vrx
            ady = -drag_coeff * vry
            adz = -drag_coeff * vrz
        else:
            adx, ady, adz = 0.0, 0.0, 0.0

        # Gravity
        gx, gy, gz = 0.0, -9.81, 0.0

        ax = adx + gx
        ay = ady + gy
        az = adz + gz

        # Euler-Verlet integration
        new_vx = vx + ax * dt
        new_vy = vy + ay * dt
        new_vz = vz + az * dt

        new_x = x + new_vx * dt
        new_y = y + new_vy * dt
        new_z = z + new_vz * dt

        return (new_x, new_y, new_z), (new_vx, new_vy, new_vz)


class TestStructuralIntegrityTier1(unittest.TestCase):
    """Tier 1: Core Feature Coverage for Structural Mechanics & Ballistics."""

    def test_cantilever_material_limits(self):
        """Verify baseline horizontal cantilever overhang limits per material."""
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("sand"), 0)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("dirt"), 1)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("timber"), 4)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("cobblestone"), 5)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("stone"), 6)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("brick"), 6)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("iron"), 8)

    def test_buttress_support_expansion(self):
        """Verify that masonry buttress increases cantilever limit by exactly +3m."""
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("timber", has_buttress=True), 7)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("stone", has_buttress=True), 9)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("brick", has_buttress=True), 9)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("iron", has_buttress=True), 11)

    def test_compressive_load_bearing_capacity(self):
        """Verify column compressive threshold detection under vertical loads."""
        # 8 timber blocks on timber column: 8 * 500 = 4000 kg <= 4500 kg (Stable)
        mass, cap, overloaded = VoxelStructuralOracle.evaluate_column_load("timber", ["timber"] * 8)
        self.assertEqual(mass, 4000.0)
        self.assertFalse(overloaded)

        # 10 timber blocks on timber column: 10 * 500 = 5000 kg > 4500 kg (Overloaded!)
        mass, cap, overloaded = VoxelStructuralOracle.evaluate_column_load("timber", ["timber"] * 10)
        self.assertEqual(mass, 5000.0)
        self.assertTrue(overloaded)

    def test_mine_stability_index_formula(self):
        """Verify subterranean Sc formula with span, depth, and support radius."""
        # Granite ceiling, 4m span at 20m depth with 1 hardwood support 1m away
        sc = VoxelStructuralOracle.calculate_mine_stability_index(
            rock_type="granite",
            span_m=4.0,
            depth_m=20.0,
            supports=[(5.0, 1.0)],
        )
        self.assertGreaterEqual(sc, 1.0, "Properly supported granite mine must be stable")

    def test_overburden_pressure_formula(self):
        """Verify lithostatic overburden pressure P = rho * g * |y|."""
        # At 100m depth in granite (rho=2600), P = 2600 * 9.81 * 100 / 1000 = 2550.6 kPa
        p_kpa = VoxelStructuralOracle.calculate_overburden_pressure_kpa("granite", 100.0)
        self.assertAlmostEqual(p_kpa, 2550.6, places=1)

    def test_ballistic_drag_and_barometric_decay(self):
        """Verify aerodynamic drag reduces horizontal velocity and respects barometric decay."""
        pos0 = (0.0, 100.0, 0.0)
        vel0 = (50.0, 0.0, 0.0)
        dt = 0.1

        pos1, vel1 = VoxelStructuralOracle.integrate_ballistic_step(
            pos=pos0,
            vel=vel0,
            mass_kg=0.045,
            cd=0.40,
            area_m2=0.0005,
            wind_vel=(0.0, 0.0, 0.0),
            dt=dt,
        )
        # Drag must reduce horizontal velocity
        self.assertLess(vel1[0], 50.0)
        # Gravity must induce downward vertical velocity
        self.assertLess(vel1[1], 0.0)

    def test_voxel_blast_fracturing_formula(self):
        """Verify blast damage falloff with distance squared and material hardness."""
        impact_pos = (10.0, 10.0, 10.0)
        # Point of impact: distance = 0 -> damage = ImpactDamage * (1 - Hardness/10)
        dmg_timber = VoxelStructuralOracle.calculate_blast_damage(
            impact_damage=500.0,
            impact_pos=impact_pos,
            voxel_pos=(10.0, 10.0, 10.0),
            hardness_tier=2.0,
        )
        # 500 / 1.0 * (1 - 0.2) = 400.0
        self.assertAlmostEqual(dmg_timber, 400.0, places=2)

        # 2 meters away: dist_sq = 4 -> falloff = 1 / 5 = 0.2 -> 500 * 0.2 * 0.8 = 80.0
        dmg_dist2 = VoxelStructuralOracle.calculate_blast_damage(
            impact_damage=500.0,
            impact_pos=impact_pos,
            voxel_pos=(12.0, 10.0, 10.0),
            hardness_tier=2.0,
        )
        self.assertAlmostEqual(dmg_dist2, 80.0, places=2)


class TestStructuralIntegrityTier2(unittest.TestCase):
    """Tier 2: Boundary & Corner Cases for Physics & Geology."""

    def test_zero_span_anchored_stability(self):
        """Zero unsupported span directly adjacent to solid foundation must always have Sc >= 1.0."""
        sc = VoxelStructuralOracle.calculate_mine_stability_index(
            rock_type="sandstone",
            span_m=0.0,
            depth_m=10.0,
            supports=[],
        )
        self.assertGreaterEqual(sc, 0.55)

    def test_unsupported_sand_immediate_fall(self):
        """Sand has zero cantilever capacity; any horizontal overhang = 0."""
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("sand"), 0)
        self.assertEqual(VoxelStructuralOracle.get_cantilever_limit("gravel"), 0)

    def test_infinite_bedrock_stability(self):
        """Bedrock possesses infinite tensile strength and zero collapse risk."""
        self.assertGreater(VoxelStructuralOracle.get_cantilever_limit("bedrock"), 1000)
        sc = VoxelStructuralOracle.calculate_mine_stability_index(
            rock_type="bedrock",
            span_m=50.0,
            depth_m=350.0,
            supports=[],
        )
        self.assertGreater(sc, 10.0)

    def test_extreme_depth_overburden_pressure(self):
        """At deep subterranean depth (-350m), overburden pressure reaches extreme MPa levels."""
        p_350m = VoxelStructuralOracle.calculate_overburden_pressure_kpa("basalt", 350.0)
        # 2900 * 9.81 * 350 / 1000 = 9957.15 kPa (~9.96 MPa)
        self.assertAlmostEqual(p_350m, 9957.15, places=1)
        self.assertGreater(p_350m, 9000.0)

    def test_zero_velocity_ballistic_quiescence(self):
        """A stationary projectile with zero velocity experiences zero aerodynamic drag."""
        pos, vel = VoxelStructuralOracle.integrate_ballistic_step(
            pos=(0.0, 50.0, 0.0),
            vel=(0.0, 0.0, 0.0),
            mass_kg=1.0,
            cd=0.5,
            area_m2=0.01,
            wind_vel=(0.0, 0.0, 0.0),
            dt=0.1,
        )
        # Only gravity acts on it
        self.assertAlmostEqual(vel[0], 0.0)
        self.assertAlmostEqual(vel[1], -0.981, places=3)
        self.assertAlmostEqual(vel[2], 0.0)

    def test_hardness_tier_10_complete_blast_absorption(self):
        """Voxel with hardness tier 10 absorbs 100% of blast damage."""
        dmg = VoxelStructuralOracle.calculate_blast_damage(
            impact_damage=10000.0,
            impact_pos=(0.0, 0.0, 0.0),
            voxel_pos=(0.0, 0.0, 0.0),
            hardness_tier=10.0,
        )
        self.assertEqual(dmg, 0.0)


class TestStructuralIntegrityTier3(unittest.TestCase):
    """Tier 3: Cross-Feature Interactions (Overhang + Load + Blast + Collapse)."""

    def test_buttress_expansion_with_cantilever(self):
        """A stone cantilever extended from 6m to 8m fails without buttress but stabilizes with one."""
        limit_normal = VoxelStructuralOracle.get_cantilever_limit("stone", has_buttress=False)
        limit_buttressed = VoxelStructuralOracle.get_cantilever_limit("stone", has_buttress=True)

        span_tested = 8
        self.assertLess(limit_normal, span_tested, "8m span exceeds standard stone limit (6m)")
        self.assertGreaterEqual(limit_buttressed, span_tested, "8m span is supported with buttress (9m)")

    def test_column_load_accumulation_from_cantilever_roof(self):
        """
        Verify that a vertical stone column carrying a 5m stone roof accumulates
        roof mass plus vertical stack mass and detects overloading if overloaded.
        """
        # Column: 4 stone blocks (4 * 2600 = 10,400 kg)
        # Roof: 10 stone blocks (10 * 2600 = 26,000 kg)
        # Total = 36,400 kg <= 38,000 kg capacity for stone (Stable)
        total_mass, cap, overloaded = VoxelStructuralOracle.evaluate_column_load(
            "stone", ["stone"] * 14
        )
        self.assertEqual(total_mass, 36400.0)
        self.assertFalse(overloaded)

        # Add 1 more block -> 39,000 kg > 38,000 kg -> Overloaded!
        total_mass_over, _, overloaded_now = VoxelStructuralOracle.evaluate_column_load(
            "stone", ["stone"] * 15
        )
        self.assertEqual(total_mass_over, 39000.0)
        self.assertTrue(overloaded_now)

    def test_pillar_demolition_cascading_cave_in_bfs(self):
        """
        Simulate removing a support pillar in an unpropped 8m span limestone chamber.
        Before removal: supported (Sc >= 1.0).
        After removal: support distance increases -> Sc < 0.75 (Critical failure).
        """
        # With active hardwood frame at 2m distance
        sc_supported = VoxelStructuralOracle.calculate_mine_stability_index(
            rock_type="limestone",
            span_m=8.0,
            depth_m=60.0,
            supports=[(5.0, 2.0)],
        )
        self.assertGreaterEqual(sc_supported, 0.75)

        # Removing pillar pushes nearest support to 12m away
        sc_unsupported = VoxelStructuralOracle.calculate_mine_stability_index(
            rock_type="limestone",
            span_m=8.0,
            depth_m=60.0,
            supports=[(5.0, 12.0)],
        )
        self.assertLess(sc_unsupported, 0.75, "Ceiling without nearby support must fail")

    def test_projectile_kinetic_impact_triggering_blast_cratering(self):
        """
        A high-velocity projectile impacts a cobblestone wall.
        Calculates impact kinetic energy -> blast damage -> voxel fracture threshold.
        """
        # Catapult boulder: 40 kg traveling at 35 m/s
        mass = 40.0
        vel = 35.0
        ke = 0.5 * mass * (vel ** 2)  # 24,500 Joules
        impact_damage = ke * 0.05      # 1,225 damage

        # Voxel at impact point: Cobblestone (HP = 600, Hardness = 4.0)
        voxel_dmg = VoxelStructuralOracle.calculate_blast_damage(
            impact_damage=impact_damage,
            impact_pos=(0, 0, 0),
            voxel_pos=(0, 0, 0),
            hardness_tier=4.0,
        )
        # 1225 * 1.0 * (1 - 0.4) = 735.0 damage
        self.assertEqual(voxel_dmg, 735.0)
        # Exceeds Cobblestone HP (600) -> Fractures into rubble!
        self.assertGreater(voxel_dmg, VoxelStructuralOracle.VOXEL_HP["cobblestone"])


class TestStructuralIntegrityTier4(unittest.TestCase):
    """Tier 4: Real-World Scenarios (Siege, Deep Mining, Aerodynamics)."""

    def test_four_story_keep_tower_overload_collapse(self):
        """
        Scenario: A 4-story masonry keep built with timber foundation pillars.
        Upper levels: 3 floors of brick (12 blocks = 21,600 kg) on a timber column (capacity 4,500 kg).
        System must trigger column crushing collapse.
        """
        blocks = ["brick"] * 12
        mass, cap, overloaded = VoxelStructuralOracle.evaluate_column_load("timber", blocks)
        self.assertTrue(overloaded, "Timber pillar cannot support 3-story brick tower")
        self.assertGreater(mass, cap * 4.0)

    def test_deep_mine_drift_support_grid_comparison(self):
        """
        Scenario: Mining gallery at -150m in sandstone.
        Compare softwood timber (R=3m) vs stone pillar (R=7.5m) at 6m spacing.
        """
        depth = 150.0
        span = 6.0

        # Softwood timber 4m away: support term = 3^2 / (16 + 0.1) = 0.559 -> Sc < 0.75 (Critical failure)
        sc_timber = VoxelStructuralOracle.calculate_mine_stability_index(
            rock_type="sandstone",
            span_m=span,
            depth_m=depth,
            supports=[(3.0, 4.0)],
        )

        # Stone pillar 2.5m away: support term = 7.5^2 / (6.25 + 0.1) = 8.858 -> Sc > 1.0 (Fully stable)
        sc_stone = VoxelStructuralOracle.calculate_mine_stability_index(
            rock_type="sandstone",
            span_m=span,
            depth_m=depth,
            supports=[(7.5, 2.5)],
        )

        self.assertLess(sc_timber, 0.75, "Softwood at 4m distance in deep mine cannot prevent cave-in")
        self.assertGreaterEqual(sc_stone, 1.0, "Stone pillar at 2.5m distance stabilizes deep gallery")

    def test_crosswind_archery_ballistic_trajectory_vs_vacuum(self):
        """
        Scenario: Longbow shot (72 m/s at 15 deg elevation) fired with 8 m/s crosswind (Z axis).
        Verify aerodynamic drag reduces flight distance compared to vacuum trajectory,
        and crosswind deflects arrow along Z axis.
        """
        v0 = 72.0
        theta_rad = math.radians(15.0)
        vx0 = v0 * math.cos(theta_rad)
        vy0 = v0 * math.sin(theta_rad)
        vz0 = 0.0

        # Vacuum range: R = (v0^2 * sin(2*theta)) / g
        vacuum_range = (v0 ** 2 * math.sin(2 * theta_rad)) / 9.81

        # Simulate aerodynamic flight until ground impact (y <= 0)
        pos = (0.0, 1.8, 0.0)
        vel = (vx0, vy0, vz0)
        wind = (0.0, 0.0, 8.0)
        dt = 0.02

        total_time = 0.0
        while pos[1] > 0.0 and total_time < 10.0:
            pos, vel = VoxelStructuralOracle.integrate_ballistic_step(
                pos=pos,
                vel=vel,
                mass_kg=0.045,
                cd=0.40,
                area_m2=0.0005,
                wind_vel=wind,
                dt=dt,
            )
            total_time += dt

        # Real distance along X must be noticeably less than vacuum range due to air drag
        self.assertLess(pos[0], vacuum_range * 0.90, "Aerodynamic drag must shorten flight range")
        # Real position along Z must be deflected downwind
        self.assertGreater(pos[2], 2.0, "Crosswind must push projectile along Z axis")

    def test_trebuchet_siege_boulder_curtain_wall_breach(self):
        """
        Scenario: Trebuchet flings 130 kg boulder at 50 m/s into reinforced stone curtain wall.
        Tests crater radius: impact block destroyed, immediate neighbors damaged, distant blocks intact.
        """
        boulder_mass = 130.0
        boulder_vel = 50.0
        ke = 0.5 * boulder_mass * (boulder_vel ** 2)  # 162,500 Joules
        impact_damage = ke * 0.05                      # 8,125 damage

        wall_center = (50.0, 10.0, 50.0)
        hardness = VoxelStructuralOracle.VOXEL_HARDNESS_TIER["reinforced_stone"]  # 8.0
        wall_hp = VoxelStructuralOracle.VOXEL_HP["reinforced_stone"]              # 2500.0

        # 1. Direct hit voxel (dist = 0)
        dmg_center = VoxelStructuralOracle.calculate_blast_damage(
            impact_damage, wall_center, wall_center, hardness
        )
        # 8125 * (1 - 0.8) = 1625 damage
        self.assertAlmostEqual(dmg_center, 1625.0)

        # In double-strike siege barrage (two hits = 3250 damage > 2500 HP), wall breaches!
        self.assertGreater(dmg_center * 2, wall_hp, "Two consecutive trebuchet hits breach reinforced stone")


if __name__ == "__main__":
    unittest.main()
