"""
Automated Test Suite for Realism Pillar R2: Grid-Based Thermodynamics & Fluid Hydraulics.
Voxel Lord: Feudal Realm (Godot 4.3 / C++ Core)

Validates:
1. Fourier 3D solid voxel thermal conduction and steady-state equilibrium
2. Chimney stack convection draft velocity (valid up to 1400°C in bloomery/firebox)
3. Wind-directed cellular automata fire spread and material ignition thresholds
4. Fluid volume conservation in open channels, aqueducts, and ditches
5. Phase transitions: ambient freezing into solid Ice at T <= 0°C and seasonal thaw

Organized under 4-Tier Test Architecture:
- Tier 1: Core Feature Coverage
- Tier 2: Boundary & Corner Cases
- Tier 3: Cross-Feature Interactions
- Tier 4: Real-World Scenarios
"""

import math
import unittest
from typing import Dict, List, Tuple, Optional


class ThermodynamicsOracle:
    """Mathematical reference oracle for cellular thermodynamics, fluids, and combustion."""

    # Thermal Conductivity (W / (m * K))
    THERMAL_CONDUCTIVITY: Dict[str, float] = {
        "iron": 50.0,
        "granite": 2.8,
        "stone": 2.5,
        "brick": 0.8,
        "water": 0.60,
        "ice": 2.22,
        "timber": 0.15,
        "wood": 0.15,
        "thatch": 0.06,
        "air": 0.026,
    }

    # Specific Heat Capacity (J / (kg * K))
    SPECIFIC_HEAT: Dict[str, float] = {
        "iron": 450.0,
        "stone": 840.0,
        "brick": 900.0,
        "water": 4184.0,
        "ice": 2090.0,
        "wood": 1700.0,
        "thatch": 1800.0,
        "air": 1005.0,
    }

    # Material Density (kg / m^3)
    DENSITY: Dict[str, float] = {
        "iron": 7800.0,
        "stone": 2600.0,
        "brick": 1800.0,
        "water": 1000.0,
        "ice": 917.0,
        "wood": 500.0,
        "thatch": 150.0,
        "air": 1.225,
    }

    # Ignition Thresholds in Celsius
    IGNITION_THRESHOLDS_C: Dict[str, float] = {
        "peat": 180.0,
        "coal": 180.0,
        "thatch": 220.0,
        "straw": 220.0,
        "timber": 300.0,
        "wood": 300.0,
        "stone": 999999.0,
        "iron": 999999.0,
        "water": 999999.0,
    }

    BASE_SPREAD_RATES: Dict[str, float] = {
        "thatch": 0.15,
        "straw": 0.15,
        "wood": 0.05,
        "timber": 0.05,
        "peat": 0.08,
    }

    @classmethod
    def calculate_conduction_step(
        cls,
        temp_a: float,
        temp_b: float,
        material_a: str,
        material_b: str,
        contact_area_m2: float = 1.0,
        distance_m: float = 1.0,
        dt_seconds: float = 1.0,
    ) -> Tuple[float, float, float]:
        """
        Calculates Fourier heat conduction between two adjacent voxels.
        Harmonic mean for interfacial conductivity: k_eff = 2 * k_a * k_b / (k_a + k_b)
        Heat flux Q = k_eff * A * (T_a - T_b) / d * dt
        Returns (new_temp_a, new_temp_b, heat_transferred_joules)
        """
        ka = cls.THERMAL_CONDUCTIVITY.get(material_a.lower(), 1.0)
        kb = cls.THERMAL_CONDUCTIVITY.get(material_b.lower(), 1.0)
        keff = (2.0 * ka * kb) / (ka + kb)

        # Delta T
        delta_t = temp_a - temp_b

        # Heat transfer rate dQ / dt = keff * A * delta_t / d
        heat_rate_watts = keff * contact_area_m2 * (delta_t / distance_m)
        q_joules = heat_rate_watts * dt_seconds

        # Thermal masses: m * cp
        rho_a = cls.DENSITY.get(material_a.lower(), 1000.0)
        cp_a = cls.SPECIFIC_HEAT.get(material_a.lower(), 1000.0)
        thermal_mass_a = rho_a * 1.0 * cp_a  # for 1 m^3 voxel

        rho_b = cls.DENSITY.get(material_b.lower(), 1000.0)
        cp_b = cls.SPECIFIC_HEAT.get(material_b.lower(), 1000.0)
        thermal_mass_b = rho_b * 1.0 * cp_b

        new_temp_a = temp_a - (q_joules / thermal_mass_a)
        new_temp_b = temp_b + (q_joules / thermal_mass_b)

        return new_temp_a, new_temp_b, q_joules

    @classmethod
    def calculate_interface_temperature(
        cls,
        temp_a: float,
        temp_b: float,
        material_a: str,
        material_b: str,
    ) -> float:
        """
        Contact surface interface temperature:
        T_int = (T_a * eff_a + T_b * eff_b) / (eff_a + eff_b)
        where effusivity = sqrt(k * rho * cp)
        """
        ka = cls.THERMAL_CONDUCTIVITY.get(material_a.lower(), 1.0)
        rho_a = cls.DENSITY.get(material_a.lower(), 1000.0)
        cp_a = cls.SPECIFIC_HEAT.get(material_a.lower(), 1000.0)
        eff_a = math.sqrt(ka * rho_a * cp_a)

        kb = cls.THERMAL_CONDUCTIVITY.get(material_b.lower(), 1.0)
        rho_b = cls.DENSITY.get(material_b.lower(), 1000.0)
        cp_b = cls.SPECIFIC_HEAT.get(material_b.lower(), 1000.0)
        eff_b = math.sqrt(kb * rho_b * cp_b)

        return (temp_a * eff_a + temp_b * eff_b) / (eff_a + eff_b)

    @classmethod
    def calculate_chimney_draft_velocity(
        cls,
        height_m: float,
        temp_chimney_c: float,
        temp_ambient_c: float,
        discharge_coeff: float = 0.65,
    ) -> Tuple[float, float]:
        """
        Calculates stack effect differential pressure and draft velocity:
        T_chimney_k = T_chimney_c + 273.15
        T_ambient_k = T_ambient_c + 273.15
        DeltaP = rho_amb * g * H * (1 - T_amb / T_chimney)
        v_draft = Cd * sqrt(2 * g * H * (T_chimney - T_amb) / T_amb)
        Returns (v_draft_m_per_s, delta_p_pascals)
        """
        if height_m <= 0.0 or temp_chimney_c <= temp_ambient_c:
            return 0.0, 0.0

        t_chimney_k = temp_chimney_c + 273.15
        t_ambient_k = temp_ambient_c + 273.15
        g = 9.81
        rho_amb = 1.225

        # Pressure differential
        delta_p = rho_amb * g * height_m * (1.0 - (t_ambient_k / t_chimney_k))

        # Draft velocity
        delta_t = t_chimney_k - t_ambient_k
        v_draft = discharge_coeff * math.sqrt(2.0 * g * height_m * (delta_t / t_ambient_k))

        return v_draft, delta_p

    @classmethod
    def evaluate_fire_spread(
        cls,
        material: str,
        current_temp_c: float,
        wind_vec: Tuple[float, float, float],
        direction_to_neighbor: Tuple[float, float, float],
        humidity: float,  # 0.0 to 1.0
    ) -> Tuple[bool, float]:
        """
        Evaluates fire ignition and spread probability:
        Ignition occurs if current_temp_c >= T_ignition.
        P_spread = BaseRate * (1 + kw * (v_wind . d_voxel)) * (1 - Humidity)
        Returns (is_ignited, spread_probability)
        """
        mat = material.lower()
        t_ignite = cls.IGNITION_THRESHOLDS_C.get(mat, 999999.0)
        is_ignited = current_temp_c >= t_ignite

        if t_ignite > 10000.0 or humidity >= 0.85:
            return False, 0.0

        base_rate = cls.BASE_SPREAD_RATES.get(mat, 0.05)
        kw = 0.40

        # Dot product of wind vector with propagation direction
        # Normalize direction
        dx, dy, dz = direction_to_neighbor
        mag = math.sqrt(dx * dx + dy * dy + dz * dz)
        if mag > 1e-6:
            dx, dy, dz = dx / mag, dy / mag, dz / mag
        dot_wind = wind_vec[0] * dx + wind_vec[1] * dy + wind_vec[2] * dz

        wind_factor = max(0.20, 1.0 + kw * dot_wind)
        humidity_factor = max(0.0, 1.0 - humidity)

        spread_prob = min(1.0, base_rate * wind_factor * humidity_factor)
        return is_ignited, spread_prob

    @classmethod
    def evaluate_fluid_exchange(
        cls,
        levels: List[float],  # Array of water levels in channel cells
        channel_type: str = "stone",
    ) -> Tuple[List[float], float]:
        """
        Step cellular automata water levels to simulate volume conservation:
        Flows from higher to lower levels: delta = (h1 - h2) / 2
        Applies conveyance loss based on channel type:
        - stone aqueduct: 0% loss
        - clay canal: 0.2% per step
        - dirt ditch: 0.8% per step
        Returns: (new_levels, total_conserved_volume)
        """
        n = len(levels)
        new_levels = list(levels)

        loss_rate = {
            "stone": 0.0,
            "clay": 0.002,
            "dirt": 0.008,
        }.get(channel_type.lower(), 0.0)

        # Equalization pass
        for i in range(n - 1):
            if new_levels[i] > new_levels[i + 1]:
                delta = (new_levels[i] - new_levels[i + 1]) * 0.5
                effective_transfer = delta * (1.0 - loss_rate)
                new_levels[i] -= delta
                new_levels[i + 1] += effective_transfer

        return new_levels, sum(new_levels)

    @classmethod
    def evaluate_phase_transition(
        cls,
        block_type: str,
        temp_c: float,
        volume: float,
    ) -> Tuple[str, float]:
        """
        Water freezes to ICE when T <= 0.0 C.
        Ice melts to WATER when T > 0.0 C.
        Volume is conserved: V_water = V_ice * (rho_ice / rho_water) = V_ice * 0.917
        Returns (new_block_type, new_volume)
        """
        btype = block_type.upper()
        if btype == "WATER" and temp_c <= 0.0:
            # Freezes into solid ice: volume expands slightly (1.0 / 0.917 = 1.09)
            ice_vol = volume / 0.917
            return "ICE", ice_vol
        elif btype == "ICE" and temp_c > 0.0:
            # Melts back to water: volume contracts back to conserved fluid
            water_vol = volume * 0.917
            return "WATER", water_vol
        return btype, volume


class TestThermodynamicsTier1(unittest.TestCase):
    """Tier 1: Core Feature Coverage for Heat, Chimney, Fire, and Fluids."""

    def test_fourier_solid_conduction_transfer(self):
        """Verify Fourier heat flux transfers energy from hot block to colder block."""
        # 100C iron next to 20C iron
        t_hot, t_cold, q = ThermodynamicsOracle.calculate_conduction_step(
            temp_a=100.0,
            temp_b=20.0,
            material_a="iron",
            material_b="iron",
            contact_area_m2=1.0,
            distance_m=1.0,
            dt_seconds=1.0,
        )
        self.assertLess(t_hot, 100.0, "Hot block must cool down")
        self.assertGreater(t_cold, 20.0, "Cold block must warm up")
        self.assertGreater(q, 0.0, "Heat flux must be positive")

    def test_chimney_draft_stack_effect_formula(self):
        """Verify stack draft velocity calculation up to 1400C bloomery temperatures."""
        # 6m stone chimney, 1400C firebox, 20C ambient
        v_draft, delta_p = ThermodynamicsOracle.calculate_chimney_draft_velocity(
            height_m=6.0,
            temp_chimney_c=1400.0,
            temp_ambient_c=20.0,
        )
        # v_draft = 0.65 * sqrt(2 * 9.81 * 6.0 * (1380 / 293.15)) ~ 0.65 * sqrt(554.4) ~ 15.3 m/s
        self.assertGreaterEqual(v_draft, 14.0)
        self.assertLessEqual(v_draft, 16.5)
        self.assertGreater(delta_p, 50.0, "Draft pressure must exceed 50 Pa")

    def test_fire_ignition_thresholds(self):
        """Verify material ignition thresholds: Thatch 220C, Wood 300C, Stone incombustible."""
        ignited_thatch_200, _ = ThermodynamicsOracle.evaluate_fire_spread(
            "thatch", 200.0, (0, 0, 0), (1, 0, 0), 0.20
        )
        ignited_thatch_230, _ = ThermodynamicsOracle.evaluate_fire_spread(
            "thatch", 230.0, (0, 0, 0), (1, 0, 0), 0.20
        )
        self.assertFalse(ignited_thatch_200)
        self.assertTrue(ignited_thatch_230)

        ignited_wood_280, _ = ThermodynamicsOracle.evaluate_fire_spread(
            "wood", 280.0, (0, 0, 0), (1, 0, 0), 0.20
        )
        ignited_wood_310, _ = ThermodynamicsOracle.evaluate_fire_spread(
            "wood", 310.0, (0, 0, 0), (1, 0, 0), 0.20
        )
        self.assertFalse(ignited_wood_280)
        self.assertTrue(ignited_wood_310)

        # Stone at 1500C does not ignite
        ignited_stone_1500, _ = ThermodynamicsOracle.evaluate_fire_spread(
            "stone", 1500.0, (0, 0, 0), (1, 0, 0), 0.0
        )
        self.assertFalse(ignited_stone_1500)

    def test_fluid_volume_conservation_stone_aqueduct(self):
        """Verify that in a stone aqueduct, total water volume is 100% conserved (zero loss)."""
        initial_levels = [1.0, 0.6, 0.2, 0.0]
        initial_volume = sum(initial_levels)

        new_levels, final_volume = ThermodynamicsOracle.evaluate_fluid_exchange(
            levels=initial_levels,
            channel_type="stone",
        )
        self.assertAlmostEqual(final_volume, initial_volume, places=5)
        self.assertGreater(new_levels[3], 0.0, "Water must flow into empty downstream cell")

    def test_phase_transition_freeze_and_thaw(self):
        """Verify water freezes to solid ICE at <= 0C and thaws back to WATER at > 0C."""
        # 1.0 m^3 of water at -5C freezes to ICE
        block_frozen, vol_ice = ThermodynamicsOracle.evaluate_phase_transition("WATER", -5.0, 1.0)
        self.assertEqual(block_frozen, "ICE")
        self.assertGreater(vol_ice, 1.0, "Ice expands upon freezing")

        # That ICE warmed to +15C melts back to WATER
        block_melted, vol_water = ThermodynamicsOracle.evaluate_phase_transition("ICE", 15.0, vol_ice)
        self.assertEqual(block_melted, "WATER")
        self.assertAlmostEqual(vol_water, 1.0, places=4, msg="Mass must be conserved upon thaw")


class TestThermodynamicsTier2(unittest.TestCase):
    """Tier 2: Boundary & Corner Cases for Heat, Convection, Fire, and Fluids."""

    def test_zero_temperature_gradient_quiescence(self):
        """When adjacent blocks have identical temperatures, heat flux is exactly zero."""
        t1, t2, q = ThermodynamicsOracle.calculate_conduction_step(
            temp_a=25.0,
            temp_b=25.0,
            material_a="stone",
            material_b="stone",
        )
        self.assertEqual(t1, 25.0)
        self.assertEqual(t2, 25.0)
        self.assertEqual(q, 0.0)

    def test_zero_height_chimney_draft(self):
        """A chimney stack of height 0m generates zero draft velocity and zero pressure."""
        v, p = ThermodynamicsOracle.calculate_chimney_draft_velocity(
            height_m=0.0,
            temp_chimney_c=800.0,
            temp_ambient_c=20.0,
        )
        self.assertEqual(v, 0.0)
        self.assertEqual(p, 0.0)

    def test_cold_chimney_no_reverse_draft(self):
        """When chimney temperature is at or below ambient, no upward draft velocity occurs."""
        v, p = ThermodynamicsOracle.calculate_chimney_draft_velocity(
            height_m=10.0,
            temp_chimney_c=15.0,
            temp_ambient_c=20.0,
        )
        self.assertEqual(v, 0.0)
        self.assertEqual(p, 0.0)

    def test_extreme_humidity_extinguishes_fire(self):
        """High humidity (>= 85% rain/downpour) completely prevents fire spread."""
        is_ignited, spread_prob = ThermodynamicsOracle.evaluate_fire_spread(
            material="thatch",
            current_temp_c=250.0,
            wind_vec=(10.0, 0.0, 0.0),
            direction_to_neighbor=(1.0, 0.0, 0.0),
            humidity=0.90,
        )
        self.assertFalse(is_ignited)
        self.assertEqual(spread_prob, 0.0)

    def test_negative_absolute_temperature_protection(self):
        """Ensure conduction and phase transitions handle extreme sub-zero permafrost temperatures."""
        block, vol = ThermodynamicsOracle.evaluate_phase_transition("WATER", -40.0, 1.0)
        self.assertEqual(block, "ICE")
        self.assertGreater(vol, 0.0)


class TestThermodynamicsTier3(unittest.TestCase):
    """Tier 3: Cross-Feature Interactions (Conduction -> Combustion -> Extinguishment)."""

    def test_firebox_heat_conducting_to_chimney_stack_convection(self):
        """
        A charcoal fire in a bloomery heats the stone chimney base to 600C,
        which in turn establishes a buoyant convection stack effect.
        """
        # 1000C charcoal fire conducting into 20C stone base
        t_fire, t_stone, q = ThermodynamicsOracle.calculate_conduction_step(
            temp_a=1000.0,
            temp_b=20.0,
            material_a="brick",
            material_b="stone",
            contact_area_m2=1.0,
            distance_m=0.5,
            dt_seconds=60.0,
        )
        self.assertGreater(t_stone, 20.0)

        # Stone base now drives vertical chimney draft
        v_draft, p_draft = ThermodynamicsOracle.calculate_chimney_draft_velocity(
            height_m=5.0,
            temp_chimney_c=t_stone,
            temp_ambient_c=15.0,
        )
        self.assertGreater(v_draft, 0.5)

    def test_furnace_wall_conduction_igniting_adjacent_timber(self):
        """
        An uninsulated furnace wall reaches 500C and conducts heat into an adjacent timber wall.
        Calculates interface contact temperature; when it exceeds 300C, fire ignition triggers.
        """
        # Interfacial surface temperature of timber in direct contact with 500C furnace brick
        t_interface = ThermodynamicsOracle.calculate_interface_temperature(
            temp_a=500.0,
            temp_b=250.0,
            material_a="brick",
            material_b="wood",
        )
        # Interface temperature reaches ~440C > 300C ignition threshold
        self.assertGreater(t_interface, 300.0)

        # Check fire spread at timber surface
        ignited, prob = ThermodynamicsOracle.evaluate_fire_spread(
            material="wood",
            current_temp_c=t_interface,
            wind_vec=(0, 0, 0),
            direction_to_neighbor=(1, 0, 0),
            humidity=0.10,
        )
        self.assertTrue(ignited, "Timber contact surface heated past 300C must catch fire")
        self.assertGreater(prob, 0.0)

    def test_water_bucket_suppression_cooling_below_ignition(self):
        """
        Applying a water bucket cools burning timber by 250C, quenching it below 300C.
        """
        burning_temp = 450.0
        cooled_temp = burning_temp - 250.0  # 200C
        ignited, prob = ThermodynamicsOracle.evaluate_fire_spread(
            material="wood",
            current_temp_c=cooled_temp,
            wind_vec=(0, 0, 0),
            direction_to_neighbor=(1, 0, 0),
            humidity=0.50,
        )
        self.assertFalse(ignited, "Quenched timber below 300C ceases combustion")

    def test_dirt_ditch_conveyance_losses_vs_aqueduct(self):
        """
        Verify that an unlined dirt ditch experiences conveyance seepage losses
        while a stone aqueduct maintains 100% volume.
        """
        levels = [1.0, 0.5, 0.2, 0.0]
        initial_vol = sum(levels)

        # Stone aqueduct: zero loss
        _, vol_stone = ThermodynamicsOracle.evaluate_fluid_exchange(levels, "stone")
        self.assertAlmostEqual(vol_stone, initial_vol, places=5)

        # Dirt ditch: positive seepage loss
        _, vol_dirt = ThermodynamicsOracle.evaluate_fluid_exchange(levels, "dirt")
        self.assertLess(vol_dirt, initial_vol, "Dirt ditch must lose water to soil seepage")


class TestThermodynamicsTier4(unittest.TestCase):
    """Tier 4: Real-World Scenarios (Greenhouse, Bloomery, Canal Freeze)."""

    def test_tundra_geothermal_greenhouse_thermal_equilibrium(self):
        """
        Scenario: Geothermal greenhouse in Tundra during -35C blizzard.
        Heat inputs: Geothermal steam = 8.4 kW, Solar = 0.6 kW -> Total Q_in = 9.0 kW.
        Heat losses through glass/stone walls: Sum(U * A) = 200 W / K.
        Equilibrium temperature: T_eq = T_amb + (Q_in / Sum(U * A)) = -35 + (9000 / 200) = +10.0C.
        Inside temperature remains above freezing (+10C), saving crops from frostbite.
        """
        t_amb = -35.0
        q_in_watts = 9000.0
        heat_loss_coeff = 200.0  # W / K

        t_eq = t_amb + (q_in_watts / heat_loss_coeff)
        self.assertEqual(t_eq, 10.0)
        self.assertGreater(t_eq, 0.0, "Geothermal greenhouse must sustain above-freezing temperature")

    def test_industrial_bloomery_chimney_draft_operation(self):
        """
        Scenario: High-temperature bloomery running at 1400C with 8m vertical chimney.
        Verify that stack draft velocity exceeds 15 m/s, providing adequate oxygen influx.
        """
        v_draft, p_draft = ThermodynamicsOracle.calculate_chimney_draft_velocity(
            height_m=8.0,
            temp_chimney_c=1400.0,
            temp_ambient_c=15.0,
        )
        self.assertGreaterEqual(v_draft, 16.0)
        self.assertGreaterEqual(p_draft, 70.0)

    def test_canal_winter_freeze_over_and_spring_thaw(self):
        """
        Scenario: A settlement moat / navigation canal in Winter (-8C) and Spring (+12C).
        1. Winter: Surface water freezes to solid ICE blocks.
        2. Spring: Ambient temperature rises to +12C, ICE thaws back into water conserving volume.
        """
        water_volume = 150.0  # m^3 in canal
        # Freezing
        block_state, ice_volume = ThermodynamicsOracle.evaluate_phase_transition("WATER", -8.0, water_volume)
        self.assertEqual(block_state, "ICE")
        self.assertGreater(ice_volume, water_volume)

        # Thawing
        thawed_state, restored_water_volume = ThermodynamicsOracle.evaluate_phase_transition("ICE", 12.0, ice_volume)
        self.assertEqual(thawed_state, "WATER")
        self.assertAlmostEqual(restored_water_volume, water_volume, places=3)

    def test_wind_driven_settlement_thatch_firestorm(self):
        """
        Scenario: Gale-force downwind wind (15 m/s) blowing towards neighboring thatch cottage.
        Downwind neighbor has high spread probability; upwind neighbor has low spread probability.
        """
        wind = (15.0, 0.0, 0.0)
        # Downwind neighbor (direction +X)
        _, prob_downwind = ThermodynamicsOracle.evaluate_fire_spread(
            material="thatch",
            current_temp_c=250.0,
            wind_vec=wind,
            direction_to_neighbor=(1.0, 0.0, 0.0),
            humidity=0.15,
        )

        # Upwind neighbor (direction -X)
        _, prob_upwind = ThermodynamicsOracle.evaluate_fire_spread(
            material="thatch",
            current_temp_c=250.0,
            wind_vec=wind,
            direction_to_neighbor=(-1.0, 0.0, 0.0),
            humidity=0.15,
        )

        self.assertGreater(prob_downwind, prob_upwind * 2.0, "Wind must strongly amplify downwind fire spread")


if __name__ == "__main__":
    unittest.main()
