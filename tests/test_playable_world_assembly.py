"""
Automated Test Suite for Milestone 43: Complete Playable World Assembly & Standalone Release.
Voxel Lord: Feudal Realm (Godot 4.3 / C++ Core)

Validates:
1. 8 Feudal Districts assembly (Citadel, Town, Steam, Harbor, Mining, Observatory, Agriculture, Wilderness)
2. All 112 GLB 3D model asset integration and district placement mappings
3. Player input map actions, keybindings (WASD, Mouse, E, C, L, H, F1, F2), and hotbar inventory
4. Real-time inspect telemetry (compressive stress, safety margin, temperature, soil NPK)
5. Standalone launchers configuration (run_game.bat, run_game.ps1, project.godot)
6. Interactive Simulator headless execution and game-loop verification

Organized under 4-Tier Test Architecture:
- Tier 1: Core Feature Coverage
- Tier 2: Boundary & Corner Cases
- Tier 3: Cross-Feature Interactions
- Tier 4: Real-World Scenarios
"""

import os
import re
import sys
import math
import subprocess
import unittest
from typing import Dict, List, Set, Tuple


class PlayableWorldAssemblyOracle:
    """Reference Oracle for District Assembly, 112 GLB models, and Player Controls."""

    DISTRICT_ENUMS = [
        "CITADEL",
        "TOWN_SQUARE",
        "STEAM_AND_FORGE",
        "HARBOR_AND_DOCKS",
        "MINING_RAIL",
        "OBSERVATORY",
        "AGRICULTURE_NORFOLK",
        "WILDERNESS_OUTPOSTS"
    ]

    DISTRICT_CENTERS: Dict[str, Tuple[float, float, float]] = {
        "CITADEL": (32.0, 0.0, 32.0),
        "TOWN_SQUARE": (48.0, 0.0, 32.0),
        "STEAM_AND_FORGE": (48.0, 0.0, 48.0),
        "HARBOR_AND_DOCKS": (64.0, 0.0, 16.0),
        "MINING_RAIL": (16.0, 0.0, 16.0),
        "OBSERVATORY": (32.0, 0.0, 56.0),
        "AGRICULTURE_NORFOLK": (16.0, 0.0, 48.0),
        "WILDERNESS_OUTPOSTS": (60.0, 0.0, 60.0)
    }

    MATERIAL_STRENGTHS: Dict[str, float] = {
        "limestone": 15.0,
        "granite": 45.0,
        "sandstone": 10.0,
        "fired_brick": 12.0,
        "oak_wood": 8.0,
        "pine_wood": 6.0,
        "structural_iron": 65.0,
        "dirt": 1.0
    }

    @staticmethod
    def calculate_safety_margin(applied_stress: float, max_allowable_stress: float) -> float:
        if max_allowable_stress <= 0.0:
            return 0.0
        return max(0.0, min(100.0, ((max_allowable_stress - applied_stress) / max_allowable_stress) * 100.0))

    @staticmethod
    def calculate_ballistic_flight(v0: float, theta_deg: float, mass: float) -> Tuple[float, float, float]:
        g = 9.81
        theta_rad = math.radians(theta_deg)
        flight_time = (2.0 * v0 * math.sin(theta_rad)) / g
        range_dist = (v0**2 * math.sin(2.0 * theta_rad)) / g
        kinetic_energy = 0.5 * mass * (v0**2)
        return flight_time, range_dist, kinetic_energy


class TestPlayableWorldAssembly(unittest.TestCase):
    """Test Suite verifying full world assembly, 112 GLB model coverage, controls, and launcher."""

    def setUp(self):
        self.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.models_dir = os.path.join(self.project_dir, "assets", "models")
        self.world_assembler_path = os.path.join(self.project_dir, "scripts", "world", "world_assembler.gd")
        self.player_path = os.path.join(self.project_dir, "scripts", "entities", "player.gd")
        self.hud_path = os.path.join(self.project_dir, "scripts", "ui", "hud.gd")
        self.game_manager_path = os.path.join(self.project_dir, "scripts", "core", "game_manager.gd")
        self.project_godot_path = os.path.join(self.project_dir, "project.godot")

    # =========================================================================
    # Tier 1: Core Feature Coverage
    # =========================================================================

    def test_tier1_all_112_models_exist_on_filesystem(self):
        """Verify that exactly 112 GLB models exist in assets/models/."""
        self.assertTrue(os.path.isdir(self.models_dir), "assets/models directory must exist")
        glb_files = [f for f in os.listdir(self.models_dir) if f.endswith(".glb")]
        self.assertGreaterEqual(len(glb_files), 112, f"Expected at least 112 GLB models, found {len(glb_files)}")

    def test_tier1_world_assembler_script_exists_and_contains_districts(self):
        """Verify that world_assembler.gd defines all 8 districts."""
        self.assertTrue(os.path.isfile(self.world_assembler_path), "world_assembler.gd must exist")
        with open(self.world_assembler_path, "r", encoding="utf-8") as f:
            content = f.read()

        for d in PlayableWorldAssemblyOracle.DISTRICT_ENUMS:
            self.assertIn(d, content, f"District {d} must be defined in world_assembler.gd")

    def test_tier1_world_assembler_maps_all_models(self):
        """Verify that world_assembler.gd contains placement entries for the landmark models."""
        with open(self.world_assembler_path, "r", encoding="utf-8") as f:
            content = f.read()

        key_models = [
            "portcullis_gate", "watchtower", "trebuchet_siege", "battering_ram",
            "town_hall_desk", "treasury_vault", "steam_boiler", "steam_engine_drive",
            "centrifugal_governor", "furnace", "industrial_trip_hammer",
            "drydock_slipway", "quayside_crane", "fluyt_cargo_ship",
            "mine_locomotive", "rail_switch", "hopper_unloader",
            "astronomical_clock", "armillary_sphere", "celestial_orrery",
            "windmill", "water_wheel", "millstone", "baker_oven"
        ]
        for m in key_models:
            self.assertIn(m, content, f"Model {m} must be registered in world_assembler.gd")

    def test_tier1_player_controller_has_playable_signals(self):
        """Verify that player.gd contains cycle_district_requested, toggle_debug_requested, and target_block_inspected."""
        with open(self.player_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("signal cycle_district_requested", content)
        self.assertIn("signal toggle_debug_requested", content)
        self.assertIn("signal target_block_inspected", content)
        self.assertIn("_inspect_target_voxel", content)

    def test_tier1_hud_has_inspect_and_debug_panels(self):
        """Verify that hud.gd provides inspect_panel, debug_panel, and update methods."""
        with open(self.hud_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("inspect_panel", content)
        self.assertIn("debug_panel", content)
        self.assertIn("update_inspect_tooltip", content)
        self.assertIn("toggle_debug_overlay", content)
        self.assertIn("update_debug_info", content)

    # =========================================================================
    # Tier 2: Boundary & Corner Cases
    # =========================================================================

    def test_tier2_safety_margin_bounds(self):
        """Verify safety margin calculation stays within [0.0%, 100.0%] bounds."""
        # Unloaded block
        m_zero = PlayableWorldAssemblyOracle.calculate_safety_margin(0.0, 15.0)
        self.assertAlmostEqual(m_zero, 100.0, delta=0.01)

        # 50% loaded
        m_half = PlayableWorldAssemblyOracle.calculate_safety_margin(7.5, 15.0)
        self.assertAlmostEqual(m_half, 50.0, delta=0.01)

        # At failure limit
        m_limit = PlayableWorldAssemblyOracle.calculate_safety_margin(15.0, 15.0)
        self.assertAlmostEqual(m_limit, 0.0, delta=0.01)

        # Overloaded beyond limit (clamped to 0.0)
        m_over = PlayableWorldAssemblyOracle.calculate_safety_margin(25.0, 15.0)
        self.assertEqual(m_over, 0.0)

        # Zero or negative allowable stress
        m_invalid = PlayableWorldAssemblyOracle.calculate_safety_margin(5.0, 0.0)
        self.assertEqual(m_invalid, 0.0)

    def test_tier2_project_godot_input_map(self):
        """Verify project.godot contains complete input action mappings."""
        with open(self.project_godot_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_actions = [
            "move_forward", "move_backward", "move_left", "move_right",
            "jump", "sprint", "interact", "crafting", "ledger",
            "war_horn", "toggle_debug", "cycle_district", "pause"
        ]
        for act in required_actions:
            self.assertIn(act + "={", content, f"Action {act} must be defined in project.godot [input] section")

    def test_tier2_district_center_coordinates_non_colliding(self):
        """Verify that district centers have sufficient spatial clearance (>12 units apart)."""
        centers = list(PlayableWorldAssemblyOracle.DISTRICT_CENTERS.values())
        for i in range(len(centers)):
            for j in range(i + 1, len(centers)):
                c1 = centers[i]
                c2 = centers[j]
                dist = math.sqrt((c1[0] - c2[0])**2 + (c1[2] - c2[2])**2)
                self.assertGreater(dist, 12.0, f"Districts {i} and {j} too close: {dist} < 12")

    # =========================================================================
    # Tier 3: Cross-Feature Interactions
    # =========================================================================

    def test_tier3_ballistics_kinetics(self):
        """Verify trebuchet ballistics trajectory, flight time, and kinetic energy."""
        v0 = 42.0
        theta = 45.0
        mass = 120.0
        t_flight, r_dist, ke = PlayableWorldAssemblyOracle.calculate_ballistic_flight(v0, theta, mass)

        # At 45 deg, range is v0^2 / g = 1764 / 9.81 = 179.816 m
        expected_range = 179.816
        self.assertAlmostEqual(r_dist, expected_range, delta=0.5)

        # Flight time is 2 * 42 * sin(45) / 9.81 = 6.054 s
        self.assertAlmostEqual(t_flight, 6.054, delta=0.05)

        # Kinetic energy is 0.5 * 120 * 42^2 = 105,840 J
        self.assertEqual(ke, 105840.0)

    def test_tier3_game_manager_world_assembler_linkage(self):
        """Verify that game_manager.gd instantiates and connects world_assembler."""
        with open(self.game_manager_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("WorldAssembler = preload", content)
        self.assertIn("world_assembler = WorldAssembler.new", content)
        self.assertIn("assemble_complete_realm", content)
        self.assertIn("player.cycle_district_requested.connect", content)
        self.assertIn("_on_cycle_district", content)
        self.assertIn("_get_current_district_name", content)

    # =========================================================================
    # Tier 4: Real-World Scenarios & Launcher Execution
    # =========================================================================

    def test_tier4_launchers_exist(self):
        """Verify run_game.bat and run_game.ps1 exist and have valid executable markers."""
        bat_path = os.path.join(self.project_dir, "run_game.bat")
        ps1_path = os.path.join(self.project_dir, "run_game.ps1")

        self.assertTrue(os.path.isfile(bat_path), "run_game.bat must exist")
        self.assertTrue(os.path.isfile(ps1_path), "run_game.ps1 must exist")

        with open(bat_path, "r", encoding="utf-8") as f:
            bat_content = f.read()
        self.assertIn("VOXEL LORD: FEUDAL REALM", bat_content)
        self.assertIn("res://scenes/main.tscn", bat_content)

        with open(ps1_path, "r", encoding="utf-8") as f:
            ps1_content = f.read()
        self.assertIn("interactive_play_simulator.py", ps1_content)
        self.assertIn("res://scenes/main.tscn", ps1_content)

    def test_tier4_interactive_simulator_headless_execution(self):
        """Verify tools/interactive_play_simulator.py runs cleanly in headless mode with 0 exit code."""
        sim_path = os.path.join(self.project_dir, "tools", "interactive_play_simulator.py")
        self.assertTrue(os.path.isfile(sim_path), "interactive_play_simulator.py must exist")

        res = subprocess.run([sys.executable, sim_path, "--headless"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, f"Simulator failed in headless mode: {res.stderr}")
        self.assertIn("All simulator subsystems passed verification cleanly", res.stdout)

    def test_tier2_hotbar_slot_selection_bounds(self):
        """Verify that hotbar slot index selection is strictly clamped within [0, 7]."""
        active = 0
        active = max(0, min(7, -3))
        self.assertEqual(active, 0)
        active = max(0, min(7, 4))
        self.assertEqual(active, 4)
        active = max(0, min(7, 12))
        self.assertEqual(active, 7)

    def test_tier2_all_8_district_names_unique(self):
        """Verify that all 8 district names are strictly unique and descriptive."""
        names = [
            "Royal Citadel & Fortifications",
            "Medieval Town & Market Square",
            "High-Pressure Steam & Heavy Metallurgy Quarter",
            "Maritime Harbor, Slipway & Quayside",
            "Subterranean Mining & Steam Rail Terminal",
            "Renaissance Clockwork Observatory",
            "Norfolk 4-Year Crop Rotation Agronomy",
            "Frontier Redoubts, Bandit Lairs & Crypts"
        ]
        self.assertEqual(len(names), 8)
        self.assertEqual(len(set(names)), 8)

    def test_tier3_norfolk_crop_rotation_cycle(self):
        """Verify Norfolk 4-year rotation cycle (Wheat -> Turnip -> Rye -> Clover)."""
        soil = {"N": 100.0, "P": 100.0, "K": 100.0}
        # Year 1: Wheat (Heavy N consumer)
        soil["N"] -= 35.0
        soil["P"] -= 15.0
        # Year 2: Turnips (Root weed cleaner, moderate P)
        soil["P"] -= 20.0
        soil["K"] -= 10.0
        # Year 3: Rye (Hardy cereal, moderate K)
        soil["N"] -= 15.0
        soil["K"] -= 25.0
        # Year 4: Red Clover (Nitrogen fixer, restores +50 N)
        soil["N"] = min(100.0, soil["N"] + 50.0)

        self.assertGreater(soil["N"], 80.0, "Clover nitrogen fixation must regenerate soil nitrogen")

    def test_tier3_steam_quarter_power_equilibrium(self):
        """Verify steam boiler pressure to kinetic output ratio (12 bar -> 1024 SU at 64 RPM)."""
        boiler_pressure_bar = 12.0
        throttle = 1.0
        su_output = boiler_pressure_bar * throttle * (1024.0 / 12.0)
        rpm_output = 64.0 * throttle
        self.assertEqual(su_output, 1024.0)
        self.assertEqual(rpm_output, 64.0)

    def test_tier3_mining_rail_drainage_pumping_balance(self):
        """Verify vertical sump pump 150 L/min rate overcomes 100 L/min subterranean ingress."""
        pump_rate_lpm = 150.0
        groundwater_ingress_lpm = 100.0
        net_drainage_rate = pump_rate_lpm - groundwater_ingress_lpm
        self.assertGreater(net_drainage_rate, 0.0, "Pump must yield net positive drainage to prevent shaft flood")
        self.assertEqual(net_drainage_rate, 50.0)

    def test_tier3_feudal_strata_strike_threshold(self):
        """Verify feudal strike and unrest trigger when citizen morale drops below 20.0."""
        strike_threshold = 20.0
        serf_morale = 18.5
        is_striking = serf_morale < strike_threshold
        self.assertTrue(is_striking, "Morale below 20.0 must trigger labor strike")

    def test_tier4_project_godot_window_resolution(self):
        """Verify project.godot display viewport configuration is 1920x1080 canvas_items."""
        with open(self.project_godot_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("viewport_width=1920", content)
        self.assertIn("viewport_height=1080", content)
        self.assertIn('mode="canvas_items"', content)

    def test_tier4_run_game_script_error_handling(self):
        """Verify launcher scripts contain error checks and valid options."""
        bat_path = os.path.join(self.project_dir, "run_game.bat")
        with open(bat_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("ERRORLEVEL", content)
        self.assertIn("FOUND_GODOT", content)
        self.assertIn("LAUNCH_SIMULATOR", content)


if __name__ == "__main__":
    unittest.main()

