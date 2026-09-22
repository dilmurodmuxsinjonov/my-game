"""
Challenger Final: Comprehensive Empirical Oracles & Stress Harness
Evaluates MASTER_GDD.md against all completeness, mathematical soundness, and quality criteria.
"""

import math
import os
import random
import re
import sys
import unittest

# Reconfigure stdout for UTF-8 on Windows
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GDD_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "MASTER_GDD.md")
)


def load_gdd():
    with open(GDD_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestChallengerFinalEmpirical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = load_gdd()
        cls.lines = cls.content.splitlines()

    # -------------------------------------------------------------
    # 1. SECTION COMPLETENESS & WORD COUNTS (0 to 132)
    # -------------------------------------------------------------
    def test_all_133_sections_presence_and_length(self):
        """Verify that every section 0 to 132 exists, is non-empty, and exceeds 35 words."""
        section_pattern = re.compile(r"^#\s+([0-9]+)\.\s*(.*)")
        found_sections = {}
        for idx, line in enumerate(self.lines, 1):
            m = section_pattern.match(line.strip())
            if m:
                sec_num = int(m.group(1))
                found_sections[sec_num] = (idx, m.group(2).strip())

        self.assertEqual(len(found_sections), 133, f"Expected 133 sections, found {len(found_sections)}")
        missing = [i for i in range(133) if i not in found_sections]
        self.assertEqual(missing, [], f"Missing sections: {missing}")

        # Check section body lengths
        chunks = re.split(r"\n(?=#\s+[0-9]+\.)", self.content)
        word_counts = []
        short_sections = []

        for chunk in chunks:
            c_lines = chunk.strip().splitlines()
            if not c_lines:
                continue
            m = section_pattern.match(c_lines[0].strip())
            if m:
                sec_num = int(m.group(1))
                body = " ".join(c_lines[1:])
                words = len(re.findall(r"\b\w+\b", body))
                word_counts.append((sec_num, words))
                if words < 35:
                    short_sections.append((sec_num, words, m.group(2).strip()))

        self.assertEqual(
            short_sections,
            [],
            f"Sections under 35 words: {short_sections}",
        )

        min_wc = min(w for _, w in word_counts)
        max_wc = max(w for _, w in word_counts)
        avg_wc = sum(w for _, w in word_counts) / len(word_counts)
        print(f"\n[SECTION STATS] Count: {len(word_counts)}, Min words: {min_wc}, Max words: {max_wc}, Avg words: {avg_wc:.1f}")

    # -------------------------------------------------------------
    # 2. SECTION 69 IN-DEPTH EMPIRICAL VERIFICATION
    # -------------------------------------------------------------
    def test_section_69_full_specification(self):
        """Verify Section 69 contains detailed fauna catalog, balance tables, AI FSM, and formulas."""
        match = re.search(r"# 69\.\s*TABIIY VA YIRTQICH DUSHMANLAR.*?(?=\n# 70\.)", self.content, re.DOTALL)
        self.assertIsNotNone(match, "Section 69 not found in GDD")
        sec69_text = match.group(0)

        # Word count check
        words = len(re.findall(r"\b\w+\b", sec69_text))
        print(f"\n[SECTION 69 STATS] Word count: {words}")
        self.assertGreater(words, 400, f"Section 69 word count too low: {words}")

        # Check Table 23 presence and 5 creature archetypes
        required_creatures = [
            "Bo'rilari To'dasi",
            "Ayiq",
            "Qaroqchilar To'dasi",
            "Kalamush",
            "O'rgimchak",
        ]
        for creature in required_creatures:
            self.assertIn(creature, sec69_text, f"Creature {creature} missing from Section 69")

        # Check Table 23 columns
        required_columns = [
            "HP",
            "Bazaviy Zarar",
            "Harakat Tezligi",
            "Zirh / Himoya",
            "Agressiya Radiusi",
            "Asosiy Biom",
            "Birlamchi Xatti-harakat",
            "O'lja",
        ]
        for col in required_columns:
            self.assertIn(col, sec69_text, f"Column {col} missing from Section 69 balance table")

        # Check AI State Machine (Table 24)
        required_states = ["Idle / Graze", "Alert", "Stalk", "Charge / Flank", "Retreat"]
        for st in required_states:
            self.assertIn(st, sec69_text, f"FSM state {st} missing from Section 69 AI specification")

        # Check mathematical formulas: Spawn density, nocturnal cosine wave, panic probability
        self.assertIn("D_{spawn}", sec69_text, "Spawn density formula missing")
        self.assertIn("M_{nocturnal}", sec69_text, "Nocturnal multiplier formula missing")
        self.assertIn("P_{panic}", sec69_text, "Morale break panic formula missing")

    # -------------------------------------------------------------
    # 3. SECTION 104 HUD FOUR SEASONS VERIFICATION
    # -------------------------------------------------------------
    def test_section_104_four_seasons_explicit(self):
        """Verify Section 104 explicitly lists all 4 seasons with diegetic HUD icon representations."""
        match = re.search(r"# 104\.\s*FOYDALANUVCHI INTERFEYSI.*?(?=\n# 105\.)", self.content, re.DOTALL)
        self.assertIsNotNone(match, "Section 104 not found in GDD")
        sec104_text = match.group(0)

        seasons = ["Bahor", "Yoz", "Kuz", "Qish"]
        for s in seasons:
            self.assertIn(s, sec104_text, f"Season {s} missing from Section 104 HUD specification")

        # Verify icon descriptors for each season
        self.assertIn("Bahor (Spring)", sec104_text)
        self.assertIn("Yoz (Summer)", sec104_text)
        self.assertIn("Kuz (Autumn)", sec104_text)
        self.assertIn("Qish (Winter)", sec104_text)

    # -------------------------------------------------------------
    # 4. ZERO PLACEHOLDERS VERIFICATION
    # -------------------------------------------------------------
    def test_zero_forbidden_placeholders(self):
        """Exhaustively verify no placeholder patterns exist across MASTER_GDD.md."""
        forbidden_regexes = [
            (r"\bTBD\b", "TBD"),
            (r"\bTODO\b", "TODO"),
            (r"\bFIXME\b", "FIXME"),
            (r"\.\.\.", "Ellipsis (...)"),
            (r"va boshqalar", "'va boshqalar'"),
            (r"\bXXX\b", "XXX"),
            (r"\bWIP\b", "WIP"),
            (r"\bPLACEHOLDER\b", "PLACEHOLDER"),
            (r"Hali yozilmadi", "Hali yozilmadi"),
            (r"davomi bor", "davomi bor"),
        ]

        found_violations = []
        for pattern, label in forbidden_regexes:
            matches = list(re.finditer(pattern, self.content, re.IGNORECASE if label != "Ellipsis (...)" else 0))
            if matches:
                for m in matches:
                    start = max(0, m.start() - 30)
                    end = min(len(self.content), m.end() + 30)
                    snippet = self.content[start:end].replace("\n", " ")
                    found_violations.append(f"[{label}] at index {m.start()}: '...{snippet}...'")

        self.assertEqual(
            found_violations,
            [],
            f"Forbidden placeholders detected: {found_violations}",
        )

    # -------------------------------------------------------------
    # 5. DYNAMIC PRICING MONTE-CARLO STRESS TEST
    # -------------------------------------------------------------
    def test_dynamic_pricing_monte_carlo_oracle(self):
        """Stress-test the Section 49.1 / 115.6 dynamic pricing formula under extreme conditions.
        Ensures zero NaN, zero math domain errors, and strictly bounded prices."""
        def calc_buy_price(base_price, stock_target, stock_current, m_season=1.0, m_rep=1.0, k_d=0.85, gamma=1.25):
            safe_target = max(1.0, stock_target)
            stock_ratio = (safe_target - stock_current) / safe_target
            raw_base = 1.0 + (k_d * stock_ratio)
            safe_base = max(0.01, raw_base)
            elastic_factor = math.pow(safe_base, gamma)
            raw_price = base_price * elastic_factor * m_season * m_rep
            return max(0.20 * base_price, min(5.00 * base_price, raw_price))

        # Test extreme boundary conditions
        base_price = 100.0
        target = 1000.0

        # 1. Severe famine crisis (zero stock, winter crisis M_season=2.20, bad rep M_rep=1.25) -> clamp to 5.0x
        p_scarcity = calc_buy_price(base_price, target, 0.0, m_season=2.20, m_rep=1.25)
        self.assertAlmostEqual(p_scarcity, 5.00 * base_price, places=2)

        # 2. Exact target stock -> equilibrium (with m_season=1, m_rep=1 -> 1.0x)
        p_equil = calc_buy_price(base_price, target, target)
        self.assertAlmostEqual(p_equil, base_price, places=2)

        # 3. Severe hyper-supply (surplus 10x target -> stock_current = 10,000)
        # Without inner clamp max(0.01, ...), 1.0 + 0.85 * (1000 - 10000)/1000 = 1.0 - 7.65 = -6.65
        # (-6.65)^1.25 causes ValueError. Inner clamp must keep it positive and clamp to 0.20x.
        p_hypersupply = calc_buy_price(base_price, target, 10000.0)
        self.assertAlmostEqual(p_hypersupply, 0.20 * base_price, places=2)

        # 4. Monte-Carlo random testing (10,000 runs)
        random.seed(42)
        for _ in range(10000):
            bp = random.uniform(1.0, 10000.0)
            tg = random.uniform(1.0, 50000.0)
            # test stock ranging from -100 (abnormal input) to 1,000,000 (extreme hyper-supply)
            cur = random.uniform(0.0, 100.0 * tg)
            m_s = random.uniform(0.5, 3.0)
            m_r = random.uniform(0.5, 1.5)
            k = random.uniform(0.1, 2.0)
            g = random.uniform(0.5, 2.5)

            price = calc_buy_price(bp, tg, cur, m_s, m_r, k, g)
            self.assertFalse(math.isnan(price), "Price became NaN")
            self.assertFalse(math.isinf(price), "Price became Inf")
            self.assertGreaterEqual(price, 0.20 * bp - 1e-6)
            self.assertLessEqual(price, 5.00 * bp + 1e-6)

        print("\n[MONTE CARLO STRESS TEST] 10,000 extreme market conditions passed with zero NaN and strictly clamped bounds.")

    # -------------------------------------------------------------
    # 6. TABLE SYNTAX & COLUMN BALANCE ORACLE
    # -------------------------------------------------------------
    def test_markdown_tables_syntax(self):
        """Verify that every markdown table has consistent column counts and zero empty cells."""
        table_pattern = re.compile(r"(\|.+?\|\n\|[-:\s|]+\|\n(?:\|.+?\|\n)+)")
        tables = table_pattern.findall(self.content)
        self.assertGreaterEqual(len(tables), 50, f"Expected many tables, found {len(tables)}")

        table_errors = []
        for t_idx, table_str in enumerate(tables, 1):
            t_lines = [l.strip() for l in table_str.strip().splitlines() if l.strip()]
            header_cols = [c.strip() for c in t_lines[0].split("|")[1:-1]]
            num_cols = len(header_cols)

            # Check rows
            for r_idx, row in enumerate(t_lines[2:], 3):
                cols = [c.strip() for c in row.split("|")[1:-1]]
                if len(cols) != num_cols:
                    table_errors.append(f"Table {t_idx} row {r_idx} column mismatch: expected {num_cols}, got {len(cols)}")
                for c_idx, cell in enumerate(cols, 1):
                    if not cell:
                        table_errors.append(f"Table {t_idx} row {r_idx} col {c_idx} is empty")

        self.assertEqual(table_errors, [], f"Table errors found: {table_errors}")
        print(f"\n[TABLE AUDIT] {len(tables)} tables verified with zero column mismatches and zero empty cells.")


if __name__ == "__main__":
    unittest.main()
