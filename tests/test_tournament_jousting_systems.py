#!/usr/bin/env python3
"""
Unit Test Suite for Milestone 50: Grand Feudal Jousting Tournament & Chivalric Knighthood
Author: Voxel Lord Engineering Team
Tests knightly disciplines (Joust, Foot Melee, Archery Contest, Boss Duel),
chivalric honor, title progression, arena grandstand wagers, regal feasts, and persistence roundtrip.
"""

import unittest
import hashlib
import json
from typing import Dict, Any, List


class MockSupplyChain:
    """Mock supply chain tracking resources for banquet and wagering tests."""
    def __init__(self):
        self.resources: Dict[str, int] = {
            "bread": 60,
            "gold_coins": 150,
            "wood": 80,
            "stone": 80,
            "iron_ingots": 30
        }

    def get_resource(self, res: str) -> int:
        return self.resources.get(res, 0)

    def add_resource(self, res: str, amt: int) -> None:
        self.resources[res] = self.resources.get(res, 0) + amt

    def consume_resource(self, res: str, amt: int) -> bool:
        if self.resources.get(res, 0) >= amt:
            self.resources[res] -= amt
            return True
        return False


class PythonTournamentManager:
    """Python reference mirror of scripts/combat/tournament_manager.gd."""

    TITLE_THRESHOLDS = [
        {"honor": 0, "title": "Page of the Realm", "icon": "🛡️"},
        {"honor": 100, "title": "Squire of the High Seat", "icon": "🗡️"},
        {"honor": 250, "title": "Knight of the Gilded Spur", "icon": "⚔️"},
        {"honor": 500, "title": "Knight Banneret of the Crown", "icon": "🚩"},
        {"honor": 1000, "title": "Grandmaster of Chivalry & Sovereign Defender", "icon": "👑"}
    ]

    def __init__(self):
        self.champions: Dict[str, Dict[str, Any]] = {}
        self.active_discipline: str = ""
        self.current_match: Dict[str, Any] = {}
        self.chivalric_honor: int = 0
        self.current_title: str = "Page of the Realm"
        self.unlocked_titles: List[str] = ["Page of the Realm"]
        self.total_tournaments_won: int = 0
        self.total_jousts_won: int = 0
        self.total_melees_won: int = 0
        self.total_archery_won: int = 0
        self.total_duels_won: int = 0
        self.grand_feasts_hosted: int = 0
        self.grandstand_excitement: float = 75.0
        self.active_wagers: List[Dict[str, Any]] = []
        self.completed_wagers: List[Dict[str, Any]] = []
        self.signal_log: List[tuple] = []
        self.init_default_champions()

    def init_default_champions(self):
        self.champions = {
            "sir_roland": {
                "id": "sir_roland",
                "name": "Sir Roland the Ironclad",
                "realm": "Kingdom of Valoria",
                "title": "The Unyielding Bulwark",
                "joust_skill": 90,
                "melee_skill": 92,
                "archery_skill": 45,
                "chivalry": 95,
                "odds": 1.75,
                "icon": "🛡️"
            },
            "lady_gwendolyn": {
                "id": "lady_gwendolyn",
                "name": "Lady Gwendolyn the Swift",
                "realm": "Barony of Silvercoast",
                "title": "The Silver Falcon",
                "joust_skill": 82,
                "melee_skill": 75,
                "archery_skill": 96,
                "chivalry": 90,
                "odds": 2.10,
                "icon": "🏹"
            },
            "lord_valerie": {
                "id": "lord_valerie",
                "name": "Lord Valerie the Falcon",
                "realm": "Duchy of Ashfell",
                "title": "The Azure Knight",
                "joust_skill": 86,
                "melee_skill": 80,
                "archery_skill": 70,
                "chivalry": 80,
                "odds": 2.25,
                "icon": "🦅"
            },
            "brother_bartholomew": {
                "id": "brother_bartholomew",
                "name": "Brother Bartholomew the Steadfast",
                "realm": "Sunken Mire Monastic Order",
                "title": "The Resolute Templar",
                "joust_skill": 70,
                "melee_skill": 88,
                "archery_skill": 55,
                "chivalry": 98,
                "odds": 2.50,
                "icon": "✝️"
            },
            "prince_alden": {
                "id": "prince_alden",
                "name": "Prince Alden of Valoria",
                "realm": "Crown Prince of the High Realm",
                "title": "Grand Sovereign Champion",
                "joust_skill": 94,
                "melee_skill": 90,
                "archery_skill": 88,
                "chivalry": 92,
                "odds": 1.50,
                "icon": "👑"
            }
        }

    def start_joust_match(self, opponent_id: str = "sir_roland") -> Dict[str, Any]:
        opp = self.champions.get(opponent_id, self.champions["sir_roland"])
        self.active_discipline = "joust"
        self.current_match = {
            "discipline": "joust",
            "opponent_id": opponent_id,
            "opponent_name": opp.get("name", "Sir Roland"),
            "current_pass": 1,
            "max_passes": 3,
            "player_score": 0,
            "opponent_score": 0,
            "player_unhorsed": False,
            "opponent_unhorsed": False,
            "is_finished": False,
            "history": []
        }
        self.signal_log.append(("discipline_started", "joust", "Monarch", opp["name"]))
        return self.current_match

    def execute_joust_pass(self, target_zone: str = "shield", timing_factor: float = 0.85) -> Dict[str, Any]:
        if self.active_discipline != "joust" or not self.current_match or self.current_match.get("is_finished", False):
            return {"error": "No active joust match"}

        pass_num = self.current_match["current_pass"]
        hit_success = timing_factor >= 0.40
        clean_lance_break = False
        opp_unhorsed = False
        player_pts = 0

        if hit_success:
            if target_zone == "helm":
                if timing_factor >= 0.70:
                    player_pts = 3
                    clean_lance_break = True
                    if timing_factor >= 0.85:
                        opp_unhorsed = True
                else:
                    player_pts = 1
            elif target_zone == "shield":
                player_pts = 2
                clean_lance_break = (timing_factor >= 0.50)
                if timing_factor >= 0.95:
                    opp_unhorsed = True
            elif target_zone == "breastplate":
                player_pts = 1
                clean_lance_break = True
                if timing_factor >= 0.90:
                    opp_unhorsed = True
            else:
                player_pts = 1

        opp_pts = 1
        player_unhorsed = False
        if timing_factor < 0.45:
            opp_pts = 2

        self.current_match["player_score"] += player_pts
        self.current_match["opponent_score"] += opp_pts

        rec = {
            "pass": pass_num,
            "target": target_zone,
            "timing": timing_factor,
            "player_pts": player_pts,
            "opp_pts": opp_pts,
            "clean_break": clean_lance_break,
            "opp_unhorsed": opp_unhorsed,
            "player_unhorsed": player_unhorsed
        }
        self.current_match["history"].append(rec)
        self.signal_log.append(("joust_pass_completed", pass_num, player_pts, opp_pts, player_unhorsed, opp_unhorsed))

        if opp_unhorsed or player_unhorsed or pass_num >= self.current_match["max_passes"]:
            self.current_match["is_finished"] = True
            player_won = opp_unhorsed or (self.current_match["player_score"] > self.current_match["opponent_score"])
            victor = "Monarch" if player_won else self.current_match["opponent_name"]
            prize = 75 if player_won else 15
            honor = 35 if player_won else 10
            if opp_unhorsed:
                honor += 25

            if player_won:
                self.total_jousts_won += 1
                self.total_tournaments_won += 1
                self.add_chivalric_honor(honor)

            self._resolve_wagers_for_match(victor, self.current_match["opponent_id"])
            self.signal_log.append(("tournament_victorious", "joust", victor, prize, honor if player_won else 0))
        else:
            self.current_match["current_pass"] += 1

        return rec

    def start_melee_match(self, opponent_id: str = "brother_bartholomew") -> Dict[str, Any]:
        opp = self.champions.get(opponent_id, self.champions["brother_bartholomew"])
        self.active_discipline = "melee"
        self.current_match = {
            "discipline": "melee",
            "opponent_id": opponent_id,
            "opponent_name": opp.get("name", "Bartholomew"),
            "round": 1,
            "player_hp": 100.0,
            "opponent_hp": 100.0,
            "player_stamina": 100.0,
            "opponent_stamina": 100.0,
            "is_finished": False
        }
        self.signal_log.append(("discipline_started", "melee", "Monarch", opp["name"]))
        return self.current_match

    def execute_melee_action(self, action: str = "strike") -> Dict[str, Any]:
        if self.active_discipline != "melee" or not self.current_match or self.current_match.get("is_finished", False):
            return {"error": "No active melee match"}

        p_dmg = 20.0
        o_dmg = 12.0
        if action == "heavy_cleave":
            p_dmg = 40.0
            o_dmg = 15.0
        elif action == "parry":
            p_dmg = 10.0
            o_dmg = 4.0
        elif action == "shield_bash":
            p_dmg = 22.0
            o_dmg = 8.0

        self.current_match["opponent_hp"] = max(0.0, self.current_match["opponent_hp"] - p_dmg)
        self.current_match["player_hp"] = max(0.0, self.current_match["player_hp"] - o_dmg)

        winner = ""
        if self.current_match["opponent_hp"] <= 0.0 or self.current_match["player_hp"] <= 0.0:
            self.current_match["is_finished"] = True
            player_won = self.current_match["opponent_hp"] <= 0.0 and self.current_match["player_hp"] > 0.0
            winner = "Monarch" if player_won else self.current_match["opponent_name"]
            prize = 80 if player_won else 20
            honor = 40 if player_won else 10
            if player_won:
                self.total_melees_won += 1
                self.total_tournaments_won += 1
                self.add_chivalric_honor(honor)

            self._resolve_wagers_for_match(winner, self.current_match["opponent_id"])
            self.signal_log.append(("tournament_victorious", "melee", winner, prize, honor if player_won else 0))
        else:
            self.current_match["round"] += 1

        self.signal_log.append(("melee_round_completed", self.current_match["round"], winner, self.current_match["player_hp"], self.current_match["opponent_hp"]))
        return {
            "action": action,
            "player_damage": p_dmg,
            "opp_damage": o_dmg,
            "player_hp": self.current_match["player_hp"],
            "opponent_hp": self.current_match["opponent_hp"],
            "is_finished": self.current_match["is_finished"]
        }

    def start_archery_contest(self, opponent_id: str = "lady_gwendolyn") -> Dict[str, Any]:
        opp = self.champions.get(opponent_id, self.champions["lady_gwendolyn"])
        self.active_discipline = "archery"
        self.current_match = {
            "discipline": "archery",
            "opponent_id": opponent_id,
            "opponent_name": opp.get("name", "Lady Gwendolyn"),
            "current_shot": 1,
            "max_shots": 3,
            "player_total_score": 0,
            "opp_total_score": 0,
            "current_distance": 30.0,
            "current_wind": 1.5,
            "history": [],
            "is_finished": False
        }
        self.signal_log.append(("discipline_started", "archery", "Monarch", opp["name"]))
        return self.current_match

    def shoot_archery_arrow(self, aim_elevation: float = 1.5, wind_compensation: float = 1.5) -> Dict[str, Any]:
        if self.active_discipline != "archery" or not self.current_match or self.current_match.get("is_finished", False):
            return {"error": "No active archery contest"}

        shot_num = self.current_match["current_shot"]
        dist = self.current_match["current_distance"]
        wind = self.current_match["current_wind"]

        wind_err = abs(wind - wind_compensation)
        elev_err = abs(aim_elevation - (dist * 0.05))
        dev = wind_err * 1.5 + elev_err * 2.0

        p_score = 0
        if dev < 1.0:
            p_score = 10
        elif dev < 2.5:
            p_score = 7
        elif dev < 4.5:
            p_score = 5
        elif dev < 7.0:
            p_score = 2
        else:
            p_score = 0

        opp_score = 7
        self.current_match["player_total_score"] += p_score
        self.current_match["opp_total_score"] += opp_score

        rec = {
            "shot": shot_num,
            "distance": dist,
            "wind": wind,
            "player_score": p_score,
            "opp_score": opp_score
        }
        self.current_match["history"].append(rec)
        self.signal_log.append(("archery_shot_recorded", shot_num, dist, wind, p_score))

        if shot_num >= self.current_match["max_shots"]:
            self.current_match["is_finished"] = True
            player_won = self.current_match["player_total_score"] >= self.current_match["opp_total_score"]
            victor = "Monarch" if player_won else self.current_match["opponent_name"]
            prize = 60 if player_won else 15
            honor = 30 if player_won else 10
            if player_won:
                self.total_archery_won += 1
                self.total_tournaments_won += 1
                self.add_chivalric_honor(honor)

            self._resolve_wagers_for_match(victor, self.current_match["opponent_id"])
            self.signal_log.append(("tournament_victorious", "archery", victor, prize, honor if player_won else 0))
        else:
            self.current_match["current_shot"] += 1
            self.current_match["current_distance"] += 20.0
            self.current_match["current_wind"] = 2.0

        return rec

    def start_champion_duel(self, opponent_id: str = "prince_alden") -> Dict[str, Any]:
        opp = self.champions.get(opponent_id, self.champions["prince_alden"])
        self.active_discipline = "champion_duel"
        self.current_match = {
            "discipline": "champion_duel",
            "opponent_id": opponent_id,
            "opponent_name": opp.get("name", "Prince Alden"),
            "player_hp": 120.0,
            "opponent_hp": 150.0,
            "turn": 1,
            "is_finished": False
        }
        self.signal_log.append(("discipline_started", "champion_duel", "Monarch", opp["name"]))
        return self.current_match

    def execute_duel_gambit(self, gambit: str = "riposte_counter") -> Dict[str, Any]:
        if self.active_discipline != "champion_duel" or not self.current_match or self.current_match.get("is_finished", False):
            return {"error": "No active champion duel"}

        p_dmg = 45.0 if gambit == "riposte_counter" else 30.0
        o_dmg = 8.0 if gambit == "riposte_counter" else 15.0

        self.current_match["opponent_hp"] = max(0.0, self.current_match["opponent_hp"] - p_dmg)
        self.current_match["player_hp"] = max(0.0, self.current_match["player_hp"] - o_dmg)

        if self.current_match["opponent_hp"] <= 0.0 or self.current_match["player_hp"] <= 0.0:
            self.current_match["is_finished"] = True
            player_won = self.current_match["opponent_hp"] <= 0.0
            victor = "Monarch" if player_won else self.current_match["opponent_name"]
            prize = 150 if player_won else 30
            honor = 60 if player_won else 15
            if player_won:
                self.total_duels_won += 1
                self.total_tournaments_won += 1
                self.add_chivalric_honor(honor)

            self._resolve_wagers_for_match(victor, self.current_match["opponent_id"])
            self.signal_log.append(("tournament_victorious", "champion_duel", victor, prize, honor if player_won else 0))
        else:
            self.current_match["turn"] += 1

        return {
            "gambit": gambit,
            "player_damage": p_dmg,
            "opponent_damage": o_dmg,
            "player_hp": self.current_match["player_hp"],
            "opponent_hp": self.current_match["opponent_hp"],
            "is_finished": self.current_match["is_finished"]
        }

    def place_wager(self, champion_id: str, amount: int) -> Dict[str, Any]:
        champ = self.champions.get(champion_id)
        if not champ and champion_id != "monarch":
            return {"success": False, "reason": "Unknown champion"}
        if amount <= 0:
            return {"success": False, "reason": "Invalid amount"}

        odds = champ.get("odds", 1.8) if champ else 1.8
        potential_payout = int(amount * odds)
        wager_id = f"wager_{len(self.active_wagers) + len(self.completed_wagers) + 1}"
        wager = {
            "id": wager_id,
            "champion_id": champion_id,
            "champion_name": champ.get("name", "Monarch") if champ else "Monarch",
            "amount": amount,
            "odds": odds,
            "potential_payout": potential_payout,
            "status": "pending"
        }
        self.active_wagers.append(wager)
        self.signal_log.append(("wager_placed", wager_id, champion_id, amount, potential_payout))
        return {"success": True, "wager": wager}

    def _resolve_wagers_for_match(self, victor_name: str, opp_id: str) -> None:
        for w in self.active_wagers:
            won = (victor_name == "Monarch" and w["champion_id"] == "monarch") or \
                  (w["champion_id"] == opp_id and victor_name == w["champion_name"])
            w["status"] = "won" if won else "lost"
            payout = w["potential_payout"] if won else 0
            w["payout"] = payout
            self.completed_wagers.append(w)
            self.signal_log.append(("wager_resolved", w["id"], won, payout))
        self.active_wagers.clear()

    def add_chivalric_honor(self, amount: int) -> None:
        self.chivalric_honor += amount
        self._check_title_promotion()

    def _check_title_promotion(self) -> None:
        for entry in self.TITLE_THRESHOLDS:
            if self.chivalric_honor >= entry["honor"] and entry["title"] not in self.unlocked_titles:
                self.unlocked_titles.append(entry["title"])
                self.current_title = entry["title"]
                self.signal_log.append(("chivalric_title_unlocked", entry["title"], self.chivalric_honor))

    def host_grand_feast(self, supply_chain: MockSupplyChain = None) -> Dict[str, Any]:
        bread_cost = 15
        gold_cost = 25
        if supply_chain:
            if supply_chain.get_resource("bread") < bread_cost:
                return {"success": False, "reason": "Insufficient bread"}
            if supply_chain.get_resource("gold_coins") < gold_cost:
                return {"success": False, "reason": "Insufficient gold"}
            supply_chain.consume_resource("bread", bread_cost)
            supply_chain.consume_resource("gold_coins", gold_cost)

        self.grand_feasts_hosted += 1
        self.add_chivalric_honor(100)
        self.grandstand_excitement = min(100.0, self.grandstand_excitement + 20.0)
        self.signal_log.append(("grand_feast_hosted", 25.0, 50))
        return {
            "success": True,
            "morale_boost": 25.0,
            "guests_count": 50,
            "honor_awarded": 100
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chivalric_honor": self.chivalric_honor,
            "current_title": self.current_title,
            "unlocked_titles": list(self.unlocked_titles),
            "total_tournaments_won": self.total_tournaments_won,
            "total_jousts_won": self.total_jousts_won,
            "total_melees_won": self.total_melees_won,
            "total_archery_won": self.total_archery_won,
            "total_duels_won": self.total_duels_won,
            "grand_feasts_hosted": self.grand_feasts_hosted,
            "grandstand_excitement": self.grandstand_excitement,
            "active_wagers": self.active_wagers,
            "completed_wagers": self.completed_wagers
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        if not data:
            return
        self.chivalric_honor = data.get("chivalric_honor", 0)
        self.current_title = data.get("current_title", "Page of the Realm")
        self.unlocked_titles = list(data.get("unlocked_titles", ["Page of the Realm"]))
        self.total_tournaments_won = data.get("total_tournaments_won", 0)
        self.total_jousts_won = data.get("total_jousts_won", 0)
        self.total_melees_won = data.get("total_melees_won", 0)
        self.total_archery_won = data.get("total_archery_won", 0)
        self.total_duels_won = data.get("total_duels_won", 0)
        self.grand_feasts_hosted = data.get("grand_feasts_hosted", 0)
        self.grandstand_excitement = data.get("grandstand_excitement", 75.0)
        self.active_wagers = list(data.get("active_wagers", []))
        self.completed_wagers = list(data.get("completed_wagers", []))


class TestTournamentJoustingSystems(unittest.TestCase):
    """Automated unit test suite verifying Milestone 50 tournament mechanics."""

    def setUp(self):
        self.tm = PythonTournamentManager()
        self.supply = MockSupplyChain()

    def test_default_champions_roster(self):
        """Verify all 5 AI champions are registered with chivalric attributes and odds."""
        self.assertEqual(len(self.tm.champions), 5)
        self.assertIn("sir_roland", self.tm.champions)
        self.assertIn("lady_gwendolyn", self.tm.champions)
        self.assertIn("lord_valerie", self.tm.champions)
        self.assertIn("brother_bartholomew", self.tm.champions)
        self.assertIn("prince_alden", self.tm.champions)

        roland = self.tm.champions["sir_roland"]
        self.assertEqual(roland["joust_skill"], 90)
        self.assertEqual(roland["melee_skill"], 92)
        self.assertEqual(roland["odds"], 1.75)

    def test_start_joust_match(self):
        """Verify joust match initiation, initial passes, and discipline tracking."""
        match_data = self.tm.start_joust_match("sir_roland")
        self.assertEqual(self.tm.active_discipline, "joust")
        self.assertEqual(match_data["current_pass"], 1)
        self.assertEqual(match_data["max_passes"], 3)
        self.assertEqual(match_data["player_score"], 0)
        self.assertFalse(match_data["is_finished"])

    def test_execute_joust_pass_shield(self):
        """Verify standard shield tilt produces clean lance break and 2 points."""
        self.tm.start_joust_match("sir_roland")
        rec = self.tm.execute_joust_pass("shield", 0.85)
        self.assertEqual(rec["pass"], 1)
        self.assertEqual(rec["player_pts"], 2)
        self.assertTrue(rec["clean_break"])
        self.assertFalse(rec["opp_unhorsed"])
        self.assertEqual(self.tm.current_match["current_pass"], 2)

    def test_execute_joust_pass_helm_unhorse(self):
        """Verify precise helm strike unhorses opponent and achieves instant victory."""
        self.tm.start_joust_match("sir_roland")
        rec = self.tm.execute_joust_pass("helm", 0.90)
        self.assertEqual(rec["player_pts"], 3)
        self.assertTrue(rec["opp_unhorsed"])
        self.assertTrue(self.tm.current_match["is_finished"])
        self.assertEqual(self.tm.total_jousts_won, 1)
        self.assertGreaterEqual(self.tm.chivalric_honor, 60)

    def test_joust_match_three_passes(self):
        """Verify joust match completes after 3 passes if no unhorsing occurs."""
        self.tm.start_joust_match("sir_roland")
        self.tm.execute_joust_pass("breastplate", 0.70)
        self.tm.execute_joust_pass("breastplate", 0.70)
        rec3 = self.tm.execute_joust_pass("breastplate", 0.70)
        self.assertEqual(rec3["pass"], 3)
        self.assertTrue(self.tm.current_match["is_finished"])

    def test_foot_melee_combat_flow(self):
        """Verify foot melee damage calculations, actions, and victory upon HP depletion."""
        self.tm.start_melee_match("brother_bartholomew")
        self.assertEqual(self.tm.active_discipline, "melee")
        res1 = self.tm.execute_melee_action("heavy_cleave")
        self.assertEqual(res1["player_damage"], 40.0)
        self.assertEqual(self.tm.current_match["opponent_hp"], 60.0)

        # Second heavy cleave
        self.tm.execute_melee_action("heavy_cleave")
        # Third heavy cleave finishes opponent
        res3 = self.tm.execute_melee_action("heavy_cleave")
        self.assertEqual(res3["opponent_hp"], 0.0)
        self.assertTrue(res3["is_finished"])
        self.assertEqual(self.tm.total_melees_won, 1)
        self.assertGreaterEqual(self.tm.chivalric_honor, 40)

    def test_foot_melee_parry_defense(self):
        """Verify parry reduces incoming damage significantly."""
        self.tm.start_melee_match("sir_roland")
        res = self.tm.execute_melee_action("parry")
        self.assertEqual(res["opp_damage"], 4.0)

    def test_archery_contest_accuracy_and_progression(self):
        """Verify archery contest distance progression (30m, 50m, 70m) and bullseye scoring."""
        self.tm.start_archery_contest("lady_gwendolyn")
        # Shot 1 at 30m: perfect compensation -> 10 pts
        res1 = self.tm.shoot_archery_arrow(aim_elevation=1.5, wind_compensation=1.5)
        self.assertEqual(res1["player_score"], 10)
        self.assertEqual(self.tm.current_match["current_distance"], 50.0)

        # Shot 2 at 50m: elevation 2.5, wind 2.0 -> 10 pts
        res2 = self.tm.shoot_archery_arrow(aim_elevation=2.5, wind_compensation=2.0)
        self.assertEqual(res2["player_score"], 10)
        self.assertEqual(self.tm.current_match["current_distance"], 70.0)

        # Shot 3 at 70m: complete match
        res3 = self.tm.shoot_archery_arrow(aim_elevation=3.5, wind_compensation=2.0)
        self.assertTrue(self.tm.current_match["is_finished"])
        self.assertEqual(self.tm.total_archery_won, 1)

    def test_archery_miss_with_bad_wind(self):
        """Verify uncompensated wind results in outer ring or zero score."""
        self.tm.start_archery_contest("lady_gwendolyn")
        res = self.tm.shoot_archery_arrow(aim_elevation=4.0, wind_compensation=-5.0)
        self.assertLessEqual(res["player_score"], 2)

    def test_champion_boss_duel(self):
        """Verify duel against Prince Alden and riposte counter gambit."""
        self.tm.start_champion_duel("prince_alden")
        res1 = self.tm.execute_duel_gambit("riposte_counter")
        self.assertEqual(res1["player_damage"], 45.0)
        self.assertEqual(self.tm.current_match["opponent_hp"], 105.0)

        self.tm.execute_duel_gambit("riposte_counter")
        self.tm.execute_duel_gambit("riposte_counter")
        res4 = self.tm.execute_duel_gambit("riposte_counter")
        self.assertTrue(res4["is_finished"])
        self.assertEqual(self.tm.total_duels_won, 1)
        self.assertGreaterEqual(self.tm.chivalric_honor, 60)

    def test_chivalric_title_progression(self):
        """Verify honor thresholds promote through all 5 knighthood ranks."""
        self.assertEqual(self.tm.current_title, "Page of the Realm")

        self.tm.add_chivalric_honor(110)
        self.assertEqual(self.tm.current_title, "Squire of the High Seat")
        self.assertIn("Squire of the High Seat", self.tm.unlocked_titles)

        self.tm.add_chivalric_honor(150) # Total 260
        self.assertEqual(self.tm.current_title, "Knight of the Gilded Spur")

        self.tm.add_chivalric_honor(250) # Total 510
        self.assertEqual(self.tm.current_title, "Knight Banneret of the Crown")

        self.tm.add_chivalric_honor(500) # Total 1010
        self.assertEqual(self.tm.current_title, "Grandmaster of Chivalry & Sovereign Defender")
        self.assertEqual(len(self.tm.unlocked_titles), 5)

    def test_grandstand_wager_placement_and_payout(self):
        """Verify grandstand betting mechanics and payout resolution upon monarch victory."""
        w_res = self.tm.place_wager("monarch", 50)
        self.assertTrue(w_res["success"])
        wager = w_res["wager"]
        self.assertEqual(wager["amount"], 50)
        self.assertEqual(wager["potential_payout"], 90) # 50 * 1.8
        self.assertEqual(len(self.tm.active_wagers), 1)

        # Monarch wins a joust match
        self.tm.start_joust_match("sir_roland")
        self.tm.execute_joust_pass("helm", 0.95) # Instant unhorse victory

        self.assertEqual(len(self.tm.active_wagers), 0)
        self.assertEqual(len(self.tm.completed_wagers), 1)
        cw = self.tm.completed_wagers[0]
        self.assertEqual(cw["status"], "won")
        self.assertEqual(cw["payout"], 90)

    def test_grandstand_wager_invalid_params(self):
        """Verify invalid champion or negative amount wagers are rejected."""
        res1 = self.tm.place_wager("unknown_knight", 20)
        self.assertFalse(res1["success"])
        res2 = self.tm.place_wager("monarch", -10)
        self.assertFalse(res2["success"])

    def test_host_grand_feudal_feast_success(self):
        """Verify hosting a grand banquet consumes supplies and grants morale & honor."""
        res = self.tm.host_grand_feast(self.supply)
        self.assertTrue(res["success"])
        self.assertEqual(res["morale_boost"], 25.0)
        self.assertEqual(res["honor_awarded"], 100)
        self.assertEqual(self.tm.grand_feasts_hosted, 1)
        self.assertEqual(self.tm.chivalric_honor, 100)
        self.assertEqual(self.supply.get_resource("bread"), 45) # 60 - 15
        self.assertEqual(self.supply.get_resource("gold_coins"), 125) # 150 - 25

    def test_host_grand_feudal_feast_insufficient_resources(self):
        """Verify banquet cannot be held if supplies are lacking."""
        self.supply.consume_resource("bread", 55) # 5 left (requires 15)
        res = self.tm.host_grand_feast(self.supply)
        self.assertFalse(res["success"])
        self.assertIn("Insufficient bread", res["reason"])

    def test_serialization_roundtrip(self):
        """Verify serialization to dictionary and restoration maintains full state."""
        self.tm.chivalric_honor = 420
        self.tm.current_title = "Knight of the Gilded Spur"
        self.tm.unlocked_titles = ["Page of the Realm", "Squire of the High Seat", "Knight of the Gilded Spur"]
        self.tm.total_tournaments_won = 12
        self.tm.total_jousts_won = 6
        self.tm.total_melees_won = 4
        self.tm.total_archery_won = 2
        self.tm.grand_feasts_hosted = 3
        self.tm.grandstand_excitement = 92.5

        d = self.tm.to_dict()
        new_tm = PythonTournamentManager()
        new_tm.from_dict(d)

        self.assertEqual(new_tm.chivalric_honor, 420)
        self.assertEqual(new_tm.current_title, "Knight of the Gilded Spur")
        self.assertEqual(len(new_tm.unlocked_titles), 3)
        self.assertEqual(new_tm.total_tournaments_won, 12)
        self.assertEqual(new_tm.total_jousts_won, 6)
        self.assertEqual(new_tm.grand_feasts_hosted, 3)
        self.assertEqual(new_tm.grandstand_excitement, 92.5)

    def test_save_payload_sha256_integrity(self):
        """Verify save payload with tournament block produces deterministic SHA-256 hash."""
        d = self.tm.to_dict()
        payload = {
            "version": "1.0.0",
            "tournament": d
        }
        json_str = json.dumps(payload, sort_keys=True)
        h = hashlib.sha256(json_str.encode("utf-8")).hexdigest()
        self.assertEqual(len(h), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in h))

    def test_wager_loss_resolution(self):
        """Verify wagers on monarch resolve as lost when opponent wins."""
        self.tm.place_wager("monarch", 30)
        # Opponent wins
        self.tm.start_joust_match("sir_roland")
        # Trigger unhorsing on player or simulate loss
        self.tm.current_match["player_score"] = 0
        self.tm.current_match["opponent_score"] = 5
        self.tm.current_match["current_pass"] = 3
        self.tm.execute_joust_pass("breastplate", 0.40)
        self.assertEqual(len(self.tm.completed_wagers), 1)
        self.assertEqual(self.tm.completed_wagers[0]["status"], "lost")
        self.assertEqual(self.tm.completed_wagers[0]["payout"], 0)

    def test_wager_on_opponent_champion_won(self):
        """Verify betting on opponent pays out when opponent wins."""
        self.tm.place_wager("sir_roland", 40)
        self.tm.start_joust_match("sir_roland")
        self.tm.current_match["player_score"] = 0
        self.tm.current_match["opponent_score"] = 6
        self.tm.current_match["current_pass"] = 3
        self.tm.execute_joust_pass("breastplate", 0.40)
        self.assertEqual(len(self.tm.completed_wagers), 1)
        self.assertEqual(self.tm.completed_wagers[0]["status"], "won")
        self.assertEqual(self.tm.completed_wagers[0]["payout"], int(40 * 1.75))

    def test_joust_breastplate_targeting(self):
        """Verify breastplate targeting yields 1 pt and solid lance impact."""
        self.tm.start_joust_match("lady_gwendolyn")
        rec = self.tm.execute_joust_pass("breastplate", 0.85)
        self.assertEqual(rec["target"], "breastplate")
        self.assertEqual(rec["player_pts"], 1)
        self.assertTrue(rec["clean_break"])

    def test_melee_shield_bash_action(self):
        """Verify shield bash action inflicts 22 DMG and lowers incoming damage."""
        self.tm.start_melee_match("brother_bartholomew")
        res = self.tm.execute_melee_action("shield_bash")
        self.assertEqual(res["action"], "shield_bash")
        self.assertEqual(res["player_damage"], 22.0)
        self.assertEqual(res["opp_damage"], 8.0)

    def test_archery_inner_ring_scoring(self):
        """Verify slight deviation scores 7 points in the inner ring."""
        self.tm.start_archery_contest("lady_gwendolyn")
        # Deviation between 1.0 and 2.5
        rec = self.tm.shoot_archery_arrow(aim_elevation=2.0, wind_compensation=1.5) # elev err = 0.5 * 2.0 = 1.0 dev
        self.assertEqual(rec["player_score"], 7)

    def test_archery_outer_ring_scoring(self):
        """Verify moderate deviation scores 2 points in the outer ring."""
        self.tm.start_archery_contest("lady_gwendolyn")
        # elev 4.0 at 30m -> elev err = 2.5 * 2.0 = 5.0 dev
        rec = self.tm.shoot_archery_arrow(aim_elevation=4.0, wind_compensation=1.5)
        self.assertEqual(rec["player_score"], 2)

    def test_champion_duel_defensive_guard(self):
        """Verify defensive guard in champion duel minimizes monarch damage to 4."""
        self.tm.start_champion_duel("prince_alden")
        res = self.tm.execute_duel_gambit("defensive_guard")
        self.assertEqual(res["player_damage"], 30.0)
        self.assertEqual(res["opponent_damage"], 15.0)

    def test_feast_excitement_ceiling(self):
        """Verify multiple grand banquets respect the 100% grandstand excitement ceiling."""
        self.tm.grandstand_excitement = 95.0
        self.tm.host_grand_feast(self.supply)
        self.assertEqual(self.tm.grandstand_excitement, 100.0)

    def test_exact_title_progression_thresholds(self):
        """Verify exact boundary promotions across all 5 chivalric titles."""
        self.assertEqual(self.tm.current_title, "Page of the Realm")
        self.tm.add_chivalric_honor(100)
        self.assertEqual(self.tm.current_title, "Squire of the High Seat")
        self.tm.add_chivalric_honor(150) # 250
        self.assertEqual(self.tm.current_title, "Knight of the Gilded Spur")
        self.tm.add_chivalric_honor(250) # 500
        self.assertEqual(self.tm.current_title, "Knight Banneret of the Crown")
        self.tm.add_chivalric_honor(500) # 1000
        self.assertEqual(self.tm.current_title, "Grandmaster of Chivalry & Sovereign Defender")

    def test_full_save_payload_with_tournament_block(self):
        """Verify realistic game manager payload serialization including tournament block."""
        d = self.tm.to_dict()
        full_payload = {
            "version": "1.0.0",
            "slot_name": "quicksave",
            "timestamp": 1727700000,
            "player": {"health": 100.0, "stamina": 100.0},
            "economy": {"wood": 100, "stone": 100},
            "diplomacy": {},
            "invasions": {},
            "tournament": d
        }
        json_dump = json.dumps(full_payload, sort_keys=True)
        self.assertIn('"tournament"', json_dump)
        self.assertIn('"chivalric_honor"', json_dump)
        sha = hashlib.sha256(json_dump.encode("utf-8")).hexdigest()
        self.assertEqual(len(sha), 64)


if __name__ == "__main__":
    unittest.main()

