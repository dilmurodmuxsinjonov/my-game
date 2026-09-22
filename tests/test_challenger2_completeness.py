"""
Challenger 2: Deep Completeness, Placeholder, Table, and Entity Consistency Audit
"""

import os
import re
import sys

# Ensure UTF-8 output even on Windows cp1252 consoles
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

GDD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "MASTER_GDD.md"))

def run_audit():
    print(f"Loading GDD from: {GDD_PATH}")
    with open(GDD_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()

    print(f"Total Lines: {len(lines)}")
    print(f"Total Characters: {len(content)}")
    print(f"Total Words: {len(content.split())}")

    # ==========================================
    # 1. SECTION COMPLETENESS AUDIT (0 to 132)
    # ==========================================
    print("\n" + "=" * 60)
    print("1. SECTION AUDIT (0 to 132)")
    print("=" * 60)

    section_pattern = re.compile(r"^#\s+([0-9]+)\.\s*(.*)")
    section_headers = []
    for idx, line in enumerate(lines, 1):
        m = section_pattern.match(line.strip())
        if m:
            sec_num = int(m.group(1))
            sec_title = m.group(2).strip()
            section_headers.append((sec_num, sec_title, idx))

    print(f"Found {len(section_headers)} top-level numbered sections.")

    found_numbers = {sec[0]: sec for sec in section_headers}
    missing_sections = [i for i in range(133) if i not in found_numbers]
    duplicate_sections = []
    seen = set()
    for sec_num, sec_title, idx in section_headers:
        if sec_num in seen:
            duplicate_sections.append((sec_num, sec_title, idx))
        seen.add(sec_num)

    print(f"Missing sections (0-132): {missing_sections}")
    print(f"Duplicate section headers: {duplicate_sections}")

    # Section body length analysis
    section_chunks = re.split(r"\n(?=#\s+[0-9]+\.)", content)
    section_stats = []
    for chunk in section_chunks:
        c_lines = chunk.strip().splitlines()
        if not c_lines:
            continue
        first_line = c_lines[0].strip()
        m = section_pattern.match(first_line)
        if m:
            sec_num = int(m.group(1))
            sec_title = m.group(2).strip()
            body_text = "\n".join(c_lines[1:]).strip()
            words = len(body_text.split())
            tables = len(re.findall(r"(\|.+?\|\n\|[-:\s|]+\|\n(?:\|.+?\|\n)+)", chunk))
            code_blocks = len(re.findall(r"```", chunk)) // 2
            section_stats.append({
                "num": sec_num,
                "title": sec_title,
                "lines": len(c_lines),
                "words": words,
                "tables": tables,
                "code_blocks": code_blocks,
                "body_preview": body_text[:200]
            })

    print(f"Total parsed section bodies: {len(section_stats)}")
    low_word_sections = [s for s in section_stats if s["words"] < 50]
    print(f"Sections with < 50 words: {len(low_word_sections)}")
    if low_word_sections:
        for s in low_word_sections:
            print(f"  - Section {s['num']}: {s['title']} ({s['words']} words)")
            print(f"    Preview: {s['body_preview']}")

    # ==========================================
    # 2. PLACEHOLDER SCAN
    # ==========================================
    print("\n" + "=" * 60)
    print("2. PLACEHOLDER & FORBIDDEN STRINGS SCAN")
    print("=" * 60)

    forbidden_patterns = [
        ("TBD", r"\bTBD\b", re.IGNORECASE),
        ("TODO", r"\bTODO\b", re.IGNORECASE),
        ("FIXME", r"\bFIXME\b", re.IGNORECASE),
        ("Ellipsis (...)", r"\.\.\.", 0),
        ("va boshqalar", r"va\s+boshqalar", re.IGNORECASE),
        ("namuna", r"\bnamuna\b", re.IGNORECASE),
        ("masalan:", r"masalan:", re.IGNORECASE),
        ("XXX", r"\bXXX\b", 0),
        ("WIP", r"\bWIP\b", 0),
        ("PLACEHOLDER", r"\bPLACEHOLDER\b", re.IGNORECASE),
        ("Hali yozilmadi", r"hali\s+yozilmadi", re.IGNORECASE),
        ("davomi bor", r"davomi\s+bor", re.IGNORECASE),
    ]

    placeholder_findings = {}
    for name, pat, flags in forbidden_patterns:
        regex = re.compile(pat, flags)
        matches = []
        for idx, line in enumerate(lines, 1):
            if regex.search(line):
                matches.append((idx, line.strip()))
        placeholder_findings[name] = matches
        print(f"Pattern '{name}': {len(matches)} occurrences")
        if matches:
            for l_idx, text in matches:
                print(f"   Line {l_idx}: {text[:120]}")

    # ==========================================
    # 3. MARKDOWN TABLE AUDIT
    # ==========================================
    print("\n" + "=" * 60)
    print("3. MARKDOWN TABLE AUDIT")
    print("=" * 60)

    raw_tables = re.findall(r"(\|.+?\|\n\|[-:\s|]+\|\n(?:\|.+?\|\n)+)", content)
    print(f"Found {len(raw_tables)} standard multi-row markdown tables.")

    table_separator_pattern = re.compile(r"^\|[-:\s|]+\|$")
    sep_lines = [idx for idx, line in enumerate(lines, 1) if table_separator_pattern.match(line.strip())]
    print(f"Total table separator rows (|---|) found in document: {len(sep_lines)}")

    table_errors = []
    total_table_cells = 0
    empty_table_cells = []

    for t_idx, raw_t in enumerate(raw_tables, 1):
        t_lines = [l.strip() for l in raw_t.strip().splitlines() if l.strip()]
        header = [c.strip() for c in t_lines[0].split("|")[1:-1]]
        separator = [c.strip() for c in t_lines[1].split("|")[1:-1]]
        num_cols = len(header)

        if len(separator) != num_cols:
            table_errors.append(f"Table {t_idx}: Separator columns ({len(separator)}) != Header columns ({num_cols})")

        for r_idx, row_line in enumerate(t_lines[2:], 1):
            cols = [c.strip() for c in row_line.split("|")[1:-1]]
            if len(cols) != num_cols:
                table_errors.append(f"Table {t_idx} Row {r_idx}: Col count {len(cols)} != Header {num_cols}: {row_line[:60]}")
            for c_idx, cell in enumerate(cols, 1):
                total_table_cells += 1
                if cell == "":
                    empty_table_cells.append(f"Table {t_idx} Row {r_idx} Col {c_idx}")

    print(f"Total Table Cells checked: {total_table_cells}")
    print(f"Table Structural Errors: {len(table_errors)}")
    if table_errors:
        for err in table_errors[:10]:
            print(f"  [ERROR] {err}")
    print(f"Empty Table Cells: {len(empty_table_cells)}")
    if empty_table_cells:
        for err in empty_table_cells[:10]:
            print(f"  [EMPTY] {err}")

    # ==========================================
    # 4. ENTITY NAMING CONSISTENCY AUDIT
    # ==========================================
    print("\n" + "=" * 60)
    print("4. ENTITY NAMING CONSISTENCY AUDIT")
    print("=" * 60)

    crops = [
        "crop_wheat", "crop_barley", "crop_rye", "crop_cabbage", 
        "crop_carrot", "crop_flax", "crop_onion", "crop_hemp", "crop_turnip"
    ]
    print("Canonical Crop IDs occurrences:")
    for c in crops:
        cnt = len(re.findall(re.escape(c), content))
        print(f"  {c}: {cnt}")

    factions = [
        "League of Coastal Merchants", "Northern Iron Warlords", 
        "Holy Sun Order", "Steppe Horse Clans"
    ]
    print("\nCanonical Factions occurrences:")
    for f in factions:
        cnt = len(re.findall(re.escape(f), content))
        print(f"  {f}: {cnt}")

    fsm_states = ["Walk", "Work", "Eat", "Sleep", "Fight", "Flee", "Socialize", "Heal", "Transport", "Rest"]
    print("\nCanonical Citizen FSM states occurrences:")
    for s in fsm_states:
        cnt = len(re.findall(r"\b" + re.escape(s) + r"\b", content))
        print(f"  State '{s}': {cnt}")

    biomes = ["Mulgazar", "Sahro", "Tundra", "O'rmon", "Tog'", "Botiqlik"]
    print("\nBiome mentions:")
    for b in biomes:
        cnt = len(re.findall(re.escape(b), content, re.IGNORECASE))
        print(f"  {b}: {cnt}")

    print("\n" + "=" * 60)
    print("AUDIT SUMMARY:")
    print(f"Total Sections: {len(section_headers)} (0..132 present: {len(missing_sections) == 0})")
    print(f"Total Tables: {len(raw_tables)}")
    print(f"Table Errors: {len(table_errors)}")
    print(f"Empty Cells: {len(empty_table_cells)}")
    print(f"Zero Placeholders Verified: {all(len(m) == 0 for k, m in placeholder_findings.items() if k not in ['namuna', 'masalan:'])}")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
