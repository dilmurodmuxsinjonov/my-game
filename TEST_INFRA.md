# Voxel Lord: Feudal Realm — Total Realism Test Infrastructure Specification

**Document Status:** Production / Active Quality Assurance Infrastructure  
**Author:** `teamwork_preview_test_writer_m6` (QA & Test Specialist)  
**Target Architecture:** Total Realism Architecture (M1–M6)  
**Governing Documents:** `ORIGINAL_REQUEST.md`, `PROJECT.md`, `MASTER_GDD.md`  
**Test Framework:** Python 3.12 Standard Library `unittest` (Zero-Dependency Execution)  

---

## 1. Quality Assurance Philosophy & Testing Methodology

"Voxel Lord: Feudal Realm" models an unforgiving medieval simulation combining 3D voxel structural mechanics, thermal and fluid dynamics, human metabolic survival, agronomy, and historically authentic feudal economics.

The test infrastructure adheres to four foundational engineering principles:

1. **Opaque-Box & Requirement-Driven Verification:**
   - Tests are derived strictly from physical laws, mathematical formulas, and interface contracts specified in `ORIGINAL_REQUEST.md` and `PROJECT.md`.
   - Never implement facade tests or tautological assertions. Every assertion tests real computation against analytical oracles.

2. **Zero-Dependency Universal Portability:**
   - Authored using standard Python 3.12 `unittest.TestCase` suites.
   - Runs natively on Windows, Linux, and macOS without requiring external pip packages (`python -m unittest discover tests`).

3. **4-Tier Test Hierarchical Structure:**
   Every realism test suite partitions verification across four rigor tiers:
   - **Tier 1 (Feature Coverage):** Primary happy path equations and state updates under canonical inputs.
   - **Tier 2 (Boundary & Corner Cases):** Extreme physical limits (depth -350m, 1400°C furnace stacks, 0% vs 100% soil depletion, hyper-supply pricing singularities).
   - **Tier 3 (Cross-Feature Interactions):** Multi-system couplings (e.g. fire conduction igniting structural timber; rain mud degrading road friction and rerouting A* pathfinding; bandit ambushes creating grain deficits during the winter Hungry Gap).
   - **Tier 4 (Real-World Scenarios):** Multi-agent and multi-seasonal end-to-end game world scenarios (e.g. 4-year 4-field crop rotation stability; castle wall siege breach under trebuchet bombardment; scurvy epidemic cure via cold cellar sauerkraut).

4. **Continuous Regression Prevention:**
   - All newly authored suites run seamlessly alongside the 205 baseline tests, ensuring 100% backward compatibility and zero regressions across the codebase and GDD.

---

## 2. Test Suite Architecture & Inventory

```
tests/
├── test_structural_integrity.py     # R1: Voxel Load, Cantilevers, Cave-ins, Ballistics, Blast (21 tests)
├── test_thermodynamics.py            # R2: Conduction, Stack Draft, Fire CA, Hydraulics, Ice (18 tests)
├── test_biological_metabolism.py     # R3: Caloric TEE/BMR, 3 Nutrients, Scurvy, Spoilage, NPK (18 tests)
├── test_feudal_logistics.py          # R5: Friction, 5 Strata Charters, 5-Hub Pricing, Hungry Gap (18 tests)
├── test_engine_vertical_slice.py     # Vertical slice engine, chunk math, and asset verification
├── test_gdd_e2e.py                   # Master GDD section integrity and formatting checks
├── test_challenger_empirical_oracles.py # Empirical mathematical stress testing oracles
├── test_challenger_final_empirical.py   # Final validation oracles
└── test_challenger2_completeness.py     # GDD depth and completeness audits
```

### 2.1. Suite 1: `test_structural_integrity.py` (Realism Pillar R1)
- **Cantilever Limits by Material:**
  - Sand: $0\text{m}$ (immediate collapse)
  - Dirt: $1\text{m}$
  - Timber: $4\text{m}$
  - Cobblestone: $5\text{m}$
  - Cut Stone / Brick: $6\text{m}$
  - Iron / Chiseled Arch: $8\text{m}$
  - Masonry Buttress Bonus: $+3\text{m}$ support expansion
- **Compressive Load Accumulation:**
  - Column vertical load summation: $\sum m_{above}$ vs material compressive limit.
  - Detects column crushing collapse when vertical weight exceeds threshold.
- **Subterranean Stability Index ($S_c$) & Overburden:**
  - Overburden pressure formula: $P_{overburden} = \rho \cdot g \cdot |y| \text{ (kPa)}$.
  - Stability formula:
    $$S_c = \frac{K_{rock} \cdot \max\left(1.0, \sum \frac{R_{sup, i}^2}{d_i^2 + 0.1}\right)}{1.0 + 0.08 \cdot (L_{span}/2)^2 \cdot (1.0 + 0.35 \cdot |y| / 100)}$$
  - Evaluates rock tensile factors ($K_{rock} = 0.20$ soil to $1.40$ monolithic granite) and support radii ($R_{sup} = 3.0\text{m}$ softwood to $11.0\text{m}$ iron arch).
- **Aerodynamic Ballistics:**
  - Barometric density decay: $\rho(y) = \rho_0 \cdot \exp(-y / 8500)$.
  - Drag acceleration: $\vec{a}_d = -\frac{1}{2m} \rho(y) C_d A |\vec{v}_{rel}| \vec{v}_{rel}$.
  - Numerical integration with crosswind deflection and range reduction vs vacuum.
- **Voxel Blast Dispersion:**
  - Inverse-square falloff: $Damage_{voxel}(\vec{X}) = \frac{ImpactDamage}{1.0 + |\vec{X} - \vec{P}|^2} \cdot (1.0 - HardnessTier / 10.0)$.
  - Fractures blocks into debris when damage exceeds block HP.

### 2.2. Suite 2: `test_thermodynamics.py` (Realism Pillar R2)
- **Fourier Solid Thermal Conduction:**
  - Interfacial conductivity harmonic mean: $k_{eff} = 2 k_a k_b / (k_a + k_b)$.
  - Heat flux $\dot{Q} = k_{eff} A \Delta T / d$ and thermal mass temperature updates.
  - Contact surface interface temperature: $T_{int} = (T_1 b_1 + T_2 b_2) / (b_1 + b_2)$.
- **Vertical Stack Convection & Chimney Draft:**
  - Differential pressure: $\Delta P = \rho_{amb} \cdot g \cdot H \cdot (1 - T_{amb} / T_{chimney})$.
  - Draft velocity: $v_{draft} = C_d \cdot \sqrt{2 g H \frac{T_{chimney} - T_{amb}}{T_{amb}}}$.
  - Validated up to 1400°C for industrial bloomeries.
- **Cellular Fire Spread & Ignition Thresholds:**
  - Material ignition thresholds: Thatch $220^\circ\text{C}$, Wood $300^\circ\text{C}$, Stone $\infty$.
  - Wind-accelerated downwind propagation and humidity dampening ($RH \ge 0.85$ suppression).
  - Water bucket cooling suppression ($-250^\circ\text{C}$).
- **Fluid Volume Conservation & Freezing:**
  - Conserved volume in cellular automata open channels: $\sum V_{water}(t + \Delta t) = \sum V_{water}(t)$.
  - Zero loss in stone aqueducts, positive seepage in dirt ditches.
  - Phase transition at $T \le 0^\circ\text{C}$ to solid `BlockType.ICE` and seasonal thaw back to fluid.

### 2.3. Suite 3: `test_biological_metabolism.py` (Realism Pillar R3)
- **Caloric TEE & BMR Budgeting:**
  - Basal rate: $BMR = 75.0\text{ kcal/hr}$ ($1800\text{ kcal/day}$).
  - Multipliers: Sleep $0.60\times$, Rest $1.00\times$, Walk $1.50\times$, Farming $1.85\times$, Mining $2.50\times$, Combat $3.80\times$.
  - Thermoregulatory shivering expenditure: $\dot{E}_{shivering} = \max(0, \frac{36.5 - T_{body}}{4.5}) \times 120.0\text{ kcal/hr}$.
  - Starvation damage: $-2.5\text{ HP/hr}$ when caloric reserves reach zero.
- **Three Nutritional Pillars:**
  - Exponential decay: Carbs ($\tau = 18\text{h}$, or $12\text{h}$ working), Protein ($\tau = 72\text{h}$), Vitamins ($\tau = 120\text{h}$).
- **Scurvy Pathogenesis Stages:**
  - Trigger: Vitamin level $< 15.0$ sustained $\ge 72\text{h}$ (3 days).
  - Stage 1 (72–120h): Lethargy, natural healing frozen ($0.0$).
  - Stage 2 (120–168h): Petechiae skin spots, spontaneous tissue damage ($-0.5\text{ HP/hr}$).
  - Stage 3 (>168h): Severe hemorrhaging ($-2.5\text{ HP/hr}$).
  - Clinical cure: High-vitamin intake (e.g. pickled vegetables $+65$) halts bleeding and restores healing.
- **Arrhenius Spoilage & Preservation Kinetics:**
  - Temperature factor: $M_{temp} = 2.0^{\frac{T - 15.0}{10.0}}$ ($Q_{10} = 2.0$).
  - Sub-zero preservation: $0.05\times$ in icehouse, $0.02\times$ in permafrost.
  - Preservation multipliers: Halite salt ($0.07\times$), Smoking ($0.10\times$), Pickling ($0.14\times$), Cold cellar ($0.25\times$), Icehouse vault ($0.10\times$).
- **NPK Agronomy & 4-Year Crop Rotation:**
  - Liebig's Law of the Minimum: Effective fertility $= \min(N/N_{req}, P/P_{req}, K/K_{req}) \times 100\%$.
  - 9-crop NPK drain/restoration matrix; Peas Rhizobia fix $+22\%$ Nitrogen.
  - Monoculture penalty: Drain $\times (1.0 + 0.5 \cdot C_{plantings})$.
  - Canonical 4-year cycle (Wheat $\to$ Peas $\to$ Roots $\to$ Fallow) maintains fertility $>80\%$ indefinitely.

### 2.4. Suite 4: `test_feudal_logistics.py` (Realism Pillar R5)
- **Transport Surface Friction:**
  - Mud penalty: $-50\%$ haul speed ($0.50\times$).
  - Cobblestone boost: $+40\%$ haul speed ($1.40\times$).
  - A* traversal edge cost ratio: $\frac{1.40}{0.50} = 2.80\times$ (paved detour preference).
  - Heavy wagon mud stall at $0.20\times$ baseline velocity.
- **5 Social Strata Charters & Rights:**
  - Serfs: Tied to soil, 3 days corvée labor, customary strips, jacquerie revolt trigger.
  - Yeomen: Freeholders, quit-rent, market sales, longbow militia, tax strike trigger.
  - Guild Artisans: Craft monopolies, apprentice indentures, production quotas, craft strike trigger.
  - Clergy: Canon law, Benefit of Clergy, 10% Church Tithe, 40-day sanctuary, interdict trigger.
  - Nobility: Seigneurial Fiefdom Patent, High and Low Justice, 40-day knight service, civil war trigger.
- **Multi-Market Elasticity Pricing:**
  - Elasticity formula:
    $$P_{buy} = \text{clamp}\left(P_{base} \cdot \left[\max\left(0.01, \; 1.0 + k_d \cdot \frac{Stock_{target} - Stock_{current}}{Stock_{target}}\right)\right]^\gamma \cdot M_{season} \cdot M_{rep} \cdot (1 + Inf), \; 0.20 \cdot P_{base}, \; 5.00 \cdot P_{base}\right)$$
  - Parameters: $\gamma = 1.25$, $k_d = 0.85$, singularity protector $\max(0.01, \dots)$ preventing complex/NaN errors.
  - Hard clamps: $[0.20 \cdot P_{base}, 5.00 \cdot P_{base}]$.
- **Seasonal Grain Surges ("Hungry Gap"):**
  - Autumn harvest glut: $0.65\times$ price crash.
  - Late winter / early spring "Hungry Gap" (Day 24–28, 1–3): $1.80\times - 2.20\times$ staple price surge.
- **Caravan Route Security & Ambush:**
  - Route risk aggregation: $Risk_{route} = 1.0 - \prod (1.0 - Risk_{edge})$.
  - Loss fraction: $\max(0.0, Risk_{route} - 0.20 \cdot EscortStrength)$.
  - Cargo looting triggers destination supply shocks and local price spikes.

---

## 3. Requirements Traceability Matrix

| Requirement | Module Name | Primary Test Suite | Test Count | Coverage Status |
|---|---|---|---|---|
| **R1** | Structural Integrity & Voxel Physics | `tests/test_structural_integrity.py` | 21 tests | **100% Green** |
| **R2** | Thermodynamics & Fluid Hydraulics | `tests/test_thermodynamics.py` | 18 tests | **100% Green** |
| **R3** | Biological Survival & NPK Agronomy | `tests/test_biological_metabolism.py` | 18 tests | **100% Green** |
| **R4** | PBR Surfaces & Dynamic Atmosphere | `tests/test_engine_vertical_slice.py` | 12 tests | **100% Green** |
| **R5** | Feudal Socio-Economics & Logistics | `tests/test_feudal_logistics.py` | 18 tests | **100% Green** |
| **E2E / GDD** | GDD Completeness & Balance Tables | `tests/test_gdd_e2e.py` & Challenger Suites | 193 tests | **100% Green** |
| **Total** | **Full Simulation Engine** | **All 9 Test Modules** | **280 tests** | **100% Green** |

---

## 4. Execution Commands

```powershell
# Run the entire test suite across all 280 tests:
python -m unittest discover tests

# Run with verbose reporting:
python -m unittest discover tests -v

# Run individual realism test suites:
python -m unittest tests/test_structural_integrity.py -v
python -m unittest tests/test_thermodynamics.py -v
python -m unittest tests/test_biological_metabolism.py -v
python -m unittest tests/test_feudal_logistics.py -v
```
