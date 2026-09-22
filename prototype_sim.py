"""
Voxel Lord: Feudal Realm - Kingdom Simulation & Economics Prototype
Run this script with: python prototype_sim.py
Simulates the game's production chains, food distribution, tool wear, and citizen morale.
"""

import time
import random

class KingdomSimulator:
    def __init__(self, name="Oltin Vodiy"):
        self.name = name
        self.day = 1
        self.hour = 8
        self.morale = 80.0  # 0 to 100%
        self.treasury = 50  # Gold coins
        self.tax_rate = 0.10 # 10%
        
        # Stockpile Inventory
        self.inventory = {
            "bug'doy (wheat)": 20,
            "non (bread)": 40,
            "yog'och (logs)": 30,
            "taxta (planks)": 15,
            "tosh (stone)": 20,
            "temir rudasi (iron ore)": 5,
            "asboblar (tools)": 10,
            "qurollar (weapons)": 4
        }
        
        # Citizens
        self.citizens = {
            "dehqon (farmer)": 3,
            "novvoy (baker)": 1,
            "o'rmonchi (lumberjack)": 2,
            "konchi (miner)": 2,
            "temirchi (blacksmith)": 1,
            "qorovul (guard)": 2,
            "bo'sh (unassigned)": 2
        }

    def total_population(self):
        return sum(self.citizens.values())

    def simulate_day(self):
        print(f"\n==================== [ {self.name} - KUN {self.day} ] ====================")
        total_pop = self.total_population()
        
        # 1. Production
        wheat_gen = self.citizens["dehqon (farmer)"] * 4
        self.inventory["bug'doy (wheat)"] += wheat_gen
        
        # Baker converts wheat to bread
        bakers = self.citizens["novvoy (baker)"]
        wheat_needed = bakers * 3
        wheat_used = min(self.inventory["bug'doy (wheat)"], wheat_needed)
        self.inventory["bug'doy (wheat)"] -= wheat_used
        bread_gen = wheat_used * 2
        self.inventory["non (bread)"] += bread_gen
        
        # Lumberjacks
        logs_gen = self.citizens["o'rmonchi (lumberjack)"] * 3
        self.inventory["yog'och (logs)"] += logs_gen
        
        # Miners
        stone_gen = self.citizens["konchi (miner)"] * 3
        ore_gen = self.citizens["konchi (miner)"] * 1
        self.inventory["tosh (stone)"] += stone_gen
        self.inventory["temir rudasi (iron ore)"] += ore_gen
        
        # Blacksmiths (Requires 2 iron ore + 1 log -> 1 tool)
        smiths = self.citizens["temirchi (blacksmith)"]
        tools_crafted = 0
        for _ in range(smiths):
            if self.inventory["temir rudasi (iron ore)"] >= 2 and self.inventory["yog'och (logs)"] >= 1:
                self.inventory["temir rudasi (iron ore)"] -= 2
                self.inventory["yog'och (logs)"] -= 1
                self.inventory["asboblar (tools)"] += 1
                tools_crafted += 1

        # 2. Consumption (1 bread per citizen per day)
        bread_available = self.inventory["non (bread)"]
        fed = min(bread_available, total_pop)
        self.inventory["non (bread)"] -= fed
        unfed = total_pop - fed
        
        # 3. Tool wear (0.2 tool per worker per day)
        active_workers = total_pop - self.citizens["bo'sh (unassigned)"]
        tool_loss = round(active_workers * 0.15)
        self.inventory["asboblar (tools)"] = max(0, self.inventory["asboblar (tools)"] - tool_loss)
        
        # 4. Morale calculation
        food_satisfaction = (fed / total_pop) * 100 if total_pop > 0 else 100
        guard_ratio = (self.citizens["qorovul (guard)"] / total_pop) * 100
        target_morale = (food_satisfaction * 0.6) + min(30, guard_ratio * 2.0) + (10 - self.tax_rate * 50)
        self.morale = round(0.7 * self.morale + 0.3 * target_morale, 1)
        
        # 5. Taxes (Gold collected)
        tax_income = int(fed * self.tax_rate * 2)
        self.treasury += tax_income
        
        # Summary report
        print(f"Aholi: {total_pop} kishi (To'ygan: {fed}, Och: {unfed}) | Xursandlik: {self.morale}%")
        print(f"Xazina: {self.treasury} oltin (+{tax_income}) | Ishlab chiqarish: +{wheat_gen} bug'doy, +{bread_gen} non, +{logs_gen} yog'och, +{ore_gen} temir")
        print(f"Omborxona holati:")
        for k, v in self.inventory.items():
            print(f"  * {k.capitalize()}: {v}")
            
        # Population growth or leaving
        if self.morale >= 85 and self.inventory["non (bread)"] >= 20:
            print("[Xushxabar!] Farovonlik yuqori! Qishloqqa yangi 1 ta muhojir oila ko'chib keldi.")
            self.citizens["bo'sh (unassigned)"] += 1
        elif self.morale < 35:
            if self.citizens["bo'sh (unassigned)"] > 0:
                print("[OGOHLANTIRISH!] Ochlik va norozilik tufayli 1 ta fuqaro boshqa qirollikka qochib ketdi!")
                self.citizens["bo'sh (unassigned)"] -= 1

        self.day += 1

if __name__ == "__main__":
    sim = KingdomSimulator()
    print("Voxel Lord: Feudal Realm - Simulyatsiyasi ishga tushirildi.")
    print("5 kunlik o'yin jarayoni hisoblanmoqda...\n")
    for _ in range(5):
        sim.simulate_day()
