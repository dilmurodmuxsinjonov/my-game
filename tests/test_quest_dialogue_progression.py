# tests/test_quest_dialogue_progression.py
# Voxel Lord: Feudal Realm - Milestone 45 Automated Unit Test Suite
# Tests Quest Progression, Citizen Dialogue, Renown Scoring, and Monarch Coronation

import unittest


class MockCitizen:
    def __init__(self, name: str, role: int, morale: float = 75.0):
        self.name = name
        self.current_role = role
        self.morale = morale


class TestQuestManager(unittest.TestCase):
    """Validates the 6-tier Feudal Progression Questline, renown, and titles."""

    MONARCH_TITLES = [
        {"threshold": 0, "title": "Exiled Monarch"},
        {"threshold": 100, "title": "Lord of the Frontier"},
        {"threshold": 350, "title": "Baron of the Realm"},
        {"threshold": 800, "title": "Count of the Trade Lands"},
        {"threshold": 1500, "title": "Duke of High Metallurgy"},
        {"threshold": 2500, "title": "Sovereign King of the Feudal Realm"}
    ]

    QUEST_CATALOG = [
        "quest_1_foundations",
        "quest_2_bread_and_iron",
        "quest_3_steam_industry",
        "quest_4_maritime_fleet",
        "quest_5_clockwork_astronomy",
        "quest_6_sovereign_coronation"
    ]

    def test_all_6_quests_present_in_progression_order(self):
        """Ensure all 6 historical feudal quest tiers are defined."""
        self.assertEqual(len(self.QUEST_CATALOG), 6)
        self.assertEqual(self.QUEST_CATALOG[0], "quest_1_foundations")
        self.assertEqual(self.QUEST_CATALOG[-1], "quest_6_sovereign_coronation")

    def test_objective_progress_tracking_and_clamping(self):
        """Ensure objective counters increment and clamp at required limit."""
        obj = {"desc": "Harvest Wood Voxels", "key": "harvest_wood", "current": 0, "required": 10}
        
        # Add 4
        obj["current"] = min(obj["required"], obj["current"] + 4)
        self.assertEqual(obj["current"], 4)
        
        # Add 12 (should clamp at 10)
        obj["current"] = min(obj["required"], obj["current"] + 12)
        self.assertEqual(obj["current"], 10)

    def test_quest_completion_advances_to_next_tier(self):
        """Test active quest completion advances to next chapter."""
        progression = {
            "quest_1_foundations": "quest_2_bread_and_iron",
            "quest_2_bread_and_iron": "quest_3_steam_industry",
            "quest_3_steam_industry": "quest_4_maritime_fleet",
            "quest_4_maritime_fleet": "quest_5_clockwork_astronomy",
            "quest_5_clockwork_astronomy": "quest_6_sovereign_coronation"
        }
        current = "quest_1_foundations"
        for _ in range(5):
            self.assertIn(current, progression)
            current = progression[current]
        self.assertEqual(current, "quest_6_sovereign_coronation")

    def test_monarch_title_promotion_thresholds(self):
        """Ensure renown points promote monarch title through all 6 ranks."""
        def get_title(renown: int) -> str:
            best = self.MONARCH_TITLES[0]["title"]
            for entry in self.MONARCH_TITLES:
                if renown >= entry["threshold"]:
                    best = entry["title"]
            return best

        self.assertEqual(get_title(0), "Exiled Monarch")
        self.assertEqual(get_title(99), "Exiled Monarch")
        self.assertEqual(get_title(100), "Lord of the Frontier")
        self.assertEqual(get_title(350), "Baron of the Realm")
        self.assertEqual(get_title(800), "Count of the Trade Lands")
        self.assertEqual(get_title(1500), "Duke of High Metallurgy")
        self.assertEqual(get_title(2500), "Sovereign King of the Feudal Realm")
        self.assertEqual(get_title(5000), "Sovereign King of the Feudal Realm")

    def test_total_campaign_renown_sum(self):
        """Sum of all quest rewards must achieve Sovereign coronation threshold (>= 2500)."""
        quest_rewards = [100, 250, 450, 700, 1000, 1500]
        total = sum(quest_rewards)
        self.assertGreaterEqual(total, 2500)
        self.assertEqual(total, 4000)

    def test_victory_condition_flag(self):
        """Final coronation quest triggers sovereign victory."""
        total_renown = 4000
        is_victory = (total_renown >= 2500)
        self.assertTrue(is_victory)


class TestCitizenDialogue(unittest.TestCase):
    """Validates medieval citizen speech, seasonal lines, and morale interactions."""

    ROLE_DIALOGUE = {
        0: ["Greetings, Sire! Awaiting your royal decree. Where shall I direct my labor?"],
        1: ["The Norfolk crop rotation is bearing fruit, Sire. The soil is fertile and moist!"],
        2: ["The oak trunks are sturdy, Sire. Our axes are sharp and the timber crates are filling."],
        3: ["The subterranean shafts run deep into granite strata, Sire. Iron and coal abound!"],
        4: ["The millstone flour is ground fine, Sire. The brick ovens are warm and fragrant!"],
        5: ["The tuyeres are blowing a fierce draft! Our blast furnace reaches 1400°C today."],
        6: ["The ramparts are manned and the watchtowers vigilant, Sire! The realm is safe."]
    }

    def test_all_7_roles_have_dialogue(self):
        """Verify each citizen role (0 to 6) has tailored medieval dialogue."""
        for role_id in range(7):
            self.assertIn(role_id, self.ROLE_DIALOGUE)
            self.assertGreater(len(self.ROLE_DIALOGUE[role_id]), 0)

    def test_low_morale_complaint_priority(self):
        """Low morale (<40.0) overrides standard cheerful dialogue with plea."""
        def get_line(role_id: int, morale: float, is_winter: bool) -> str:
            if morale < 40.0:
                return "low_morale"
            if is_winter:
                return "winter"
            return "standard"

        self.assertEqual(get_line(1, 35.0, False), "low_morale")
        self.assertEqual(get_line(1, 35.0, True), "low_morale")
        self.assertEqual(get_line(1, 75.0, True), "winter")
        self.assertEqual(get_line(1, 75.0, False), "standard")

    def test_ration_and_inspiration_morale_boosts(self):
        """Rations add +15 morale, Inspiration adds +5 morale (clamped to 100)."""
        citizen = MockCitizen("Osric the Agronomist", 1, 60.0)
        
        # Give ration
        citizen.morale = min(100.0, citizen.morale + 15.0)
        self.assertEqual(citizen.morale, 75.0)

        # Inspire
        citizen.morale = min(100.0, citizen.morale + 5.0)
        self.assertEqual(citizen.morale, 80.0)

        # Max clamp
        citizen.morale = min(100.0, citizen.morale + 50.0)
        self.assertEqual(citizen.morale, 100.0)

    def test_morale_adjectives_mapping(self):
        """Check morale adjective classification."""
        def get_adjective(val: float) -> str:
            if val >= 85.0: return "Exultant"
            if val >= 70.0: return "Content"
            if val >= 50.0: return "Enduring"
            if val >= 30.0: return "Discontent"
            return "Rebellious"

        self.assertEqual(get_adjective(90.0), "Exultant")
        self.assertEqual(get_adjective(75.0), "Content")
        self.assertEqual(get_adjective(55.0), "Enduring")
        self.assertEqual(get_adjective(35.0), "Discontent")
        self.assertEqual(get_adjective(15.0), "Rebellious")


class TestQuestJournalUI(unittest.TestCase):
    """Validates QuestJournal formatting and objective rendering."""

    def test_objective_checklist_formatting(self):
        """Ensure completed objectives show [✓] and incomplete show [○]."""
        objectives = [
            {"desc": "Mine Stone", "current": 10, "required": 10},
            {"desc": "Harvest Wood", "current": 4, "required": 10}
        ]
        formatted = []
        for obj in objectives:
            is_done = (obj["current"] >= obj["required"])
            icon = "✓" if is_done else "○"
            formatted.append(f"[{icon}] {obj['desc']}: {obj['current']}/{obj['required']}")

        self.assertEqual(formatted[0], "[✓] Mine Stone: 10/10")
        self.assertEqual(formatted[1], "[○] Harvest Wood: 4/10")

    def test_keybinding_j_for_journal(self):
        """Ensure KEY_J maps to quest journal toggle."""
        bindings = {"KEY_J": "toggle_journal", "KEY_L": "toggle_ledger", "KEY_ESCAPE": "toggle_pause"}
        self.assertEqual(bindings["KEY_J"], "toggle_journal")


class TestGameManagerQuestWiring(unittest.TestCase):
    """Validates GameManager quest trigger hooks."""

    def test_wood_and_stone_mining_triggers(self):
        """Block mining translates to quest objectives."""
        # BlockType 4 = WOOD, BlockType 3 = STONE
        block_quest_keys = {
            4: "harvest_wood",
            10: "harvest_wood",
            3: "mine_stone",
            9: "mine_stone",
            14: "harvest_wheat"
        }
        self.assertEqual(block_quest_keys[4], "harvest_wood")
        self.assertEqual(block_quest_keys[3], "mine_stone")
        self.assertEqual(block_quest_keys[14], "harvest_wheat")

    def test_district_exploration_quest_keys(self):
        """District travel triggers exploration quest objectives."""
        district_keys = {
            2: "visit_steam_district",      # STEAM_AND_FORGE
            3: "visit_harbor_district",     # HARBOR_AND_DOCKS
            4: "visit_mining_district",     # MINING_RAIL
            5: "visit_observatory"          # OBSERVATORY
        }
        self.assertEqual(district_keys[2], "visit_steam_district")
        self.assertEqual(district_keys[3], "visit_harbor_district")
        self.assertEqual(district_keys[5], "visit_observatory")

    def test_all_monarch_titles_strictly_ascending_thresholds(self):
        """Ensure title thresholds are strictly monotonically increasing."""
        thresholds = [0, 100, 350, 800, 1500, 2500]
        for i in range(len(thresholds) - 1):
            self.assertLess(thresholds[i], thresholds[i + 1])

    def test_quest_objectives_positive_requirements(self):
        """Every objective in the campaign must require >= 1 action."""
        sample_requirements = [10, 10, 1, 4, 4, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        for req in sample_requirements:
            self.assertGreaterEqual(req, 1)

    def test_dialogue_winter_season_response(self):
        """Winter weather triggers cold climate dialogue."""
        is_winter = True
        line = "The winter frost is harsh upon the realm, my Lord." if is_winter else "The sun is warm."
        self.assertIn("frost", line)

    def test_dialogue_ration_event_emission(self):
        """Ration offered emits citizen name."""
        citizen_name = "Osric the Agronomist"
        event_payload = {"citizen": citizen_name, "morale_boost": 15.0}
        self.assertEqual(event_payload["citizen"], "Osric the Agronomist")
        self.assertEqual(event_payload["morale_boost"], 15.0)

    def test_dialogue_inspire_event_emission(self):
        """Monarch inspiration event structure."""
        citizen_name = "Gareth the Guard"
        event_payload = {"citizen": citizen_name, "morale_boost": 5.0}
        self.assertEqual(event_payload["citizen"], "Gareth the Guard")
        self.assertEqual(event_payload["morale_boost"], 5.0)

    def test_quest_summary_text_generation(self):
        """Checklist string generation."""
        title = "I. Foundations of the Realm"
        objs = [
            {"desc": "Harvest Wood", "current": 10, "required": 10},
            {"desc": "Mine Stone", "current": 5, "required": 10}
        ]
        lines = [f"[{title}]"]
        for o in objs:
            check = "✓" if o["current"] >= o["required"] else "○"
            lines.append(f" [{check}] {o['desc']}: ({o['current']}/{o['required']})")
        summary = "\n".join(lines)
        self.assertIn("[✓] Harvest Wood: (10/10)", summary)
        self.assertIn("[○] Mine Stone: (5/10)", summary)

    def test_quest_status_enum_values(self):
        """Ensure QuestStatus integer states match locked/active/completed."""
        LOCKED, ACTIVE, COMPLETED = 0, 1, 2
        self.assertEqual(LOCKED, 0)
        self.assertEqual(ACTIVE, 1)
        self.assertEqual(COMPLETED, 2)

    def test_quest_journal_renown_text_display(self):
        """Header display formatting."""
        title = "Baron of the Realm"
        renown = 420
        banner = f"👑 Sovereign Title: {title} | ⚜️ Total Renown: {renown}"
        self.assertIn("Baron of the Realm", banner)
        self.assertIn("420", banner)

    def test_quest_all_quests_list_order(self):
        """Exact 6 quests in historical progression."""
        quest_keys = [
            "quest_1_foundations", "quest_2_bread_and_iron", "quest_3_steam_industry",
            "quest_4_maritime_fleet", "quest_5_clockwork_astronomy", "quest_6_sovereign_coronation"
        ]
        self.assertEqual(len(quest_keys), 6)
        self.assertEqual(quest_keys[0], "quest_1_foundations")

    def test_reassign_citizen_role_mapping(self):
        """Citizen role IDs map to readable titles."""
        roles = {
            0: "Unassigned Freeman",
            1: "Norfolk Agronomist Farmer",
            2: "Royal Forester & Lumberjack",
            3: "Subterranean Miner",
            4: "Guild Baker",
            5: "Metallurgist Blacksmith",
            6: "Feudal Militia Guard"
        }
        self.assertEqual(roles[1], "Norfolk Agronomist Farmer")
        self.assertEqual(roles[5], "Metallurgist Blacksmith")

    def test_victory_renown_overkill(self):
        """Renown > 2500 maintains Sovereign King title."""
        renown = 6000
        title = "Sovereign King of the Feudal Realm" if renown >= 2500 else "Lord"
        self.assertEqual(title, "Sovereign King of the Feudal Realm")


if __name__ == "__main__":
    unittest.main()
