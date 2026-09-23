# Voxel Lord — Unreal Engine implementation plan

Status: authorized by the user on 2026-09-23; execution started. This is a multi-milestone production plan, not a claim that the full GDD is implemented.

## Product and source of truth

Build the first-person medieval survival/colony game described in `MASTER_GDD.md`, retaining its progression from manual work to a sovereign realm. The user replaces Godot with Unreal Engine. Existing Godot files remain a reference prototype. New development lives in `unreal/`. Gameplay requirements retain their GDD section IDs; engine-specific examples are translated, not copied.

## Discovery and decisions

- Target Unreal Engine 5.8, Windows first; Linux and Steam distribution after a packaged vertical slice passes. Pin the exact installed patch after the first successful Unreal build.
- Native C++ for simulation, voxel data and gameplay rules; Unreal Actors/components for presentation and interaction; Blueprints/Data Assets for authored content once the editor is available.
- Build an engine-independent C++17 rules library compiled both by Unreal and a standalone test runner. This tests production logic rather than Python copies of formulas.
- Initial terrain: bounded 64x64x64 blocks, 1 block = 1 meter = 100 Unreal units. Horizontal axes X/Y, vertical Z. Chunk dimensions 16x16x64, flat uint16 block storage (32 KiB/chunk). Grow to GDD's 512x512 MVP through measured streaming work.
- Resolve GDD's 16x16x64, 32-cubed and prototype's 16x32x16 conflict in favor of section 127 for the first slice. GDD section 112's 12-bit local index cannot encode 16,384 cells: use uint16 local indices. Record all changes in the engine migration document.
- Canonical IDs are shared by inventory, recipes, world drops and saves. Transfers and crafting are atomic: insufficient capacity/materials must leave all state unchanged.
- No external database/server is needed for the single-player game. Data schema: world seed + generator version; chunk coordinate + local index + block ID deltas; player transform + stable item IDs and counts; calendar ticks; persistent entity IDs + role/job/state; realm policy/treasury. Versioned local archives support snapshots and future migrations. Unreal assets hold static content definitions. SQLite/network services add no value to the initial local simulation.
- No voxel-per-Actor model. Mesh one section per chunk; hide internal faces including neighboring chunks. Rebuild only edited and affected neighboring chunks. Initial finite terrain uses a simple synchronous reference mesher; async jobs/greedy meshing/collision budgets are a later measured optimization.
- Use Unreal's built-in ProceduralMeshComponent for the initial adapter. It is experimental and isolated behind a chunk actor; do not assume runtime meshes have Nanite or production Lumen support. Static architectural art can adopt Nanite later.

## Component architecture

`unreal/Source/VoxelLord/Core/`: portable voxel, inventory, calendar and snapshot code.
`unreal/Source/VoxelLord/Public/` and `Private/`: Unreal world/chunk adapters, first-person character, session, HUD, persistence and engine automation tests.
`unreal/Config/`: input, startup, rendering defaults.
`unreal/Content/Python/`: reproducible editor setup for the starting map/material, avoiding hand-authored binary assets before engine availability.
`unreal/Tests/`: standalone executable tests of the same C++ used by the game.
`unreal/Tools/`: environment detection, build and launch entry points.
`docs/`: GDD coverage, migration decisions and verification evidence.

## Sequential delivery milestones

| Milestone | Delivery | Acceptance gate |
|---|---|---|
| M0 — production foundation | Environment inventory, migration decisions, all 133 GDD sections mapped, source layout and build commands | Traceability contains every section exactly once; prerequisites and blocked checks reported honestly |
| M1 — first-person voxel slice | Seeded finite terrain, boundary-correct meshing, walking/jumping, mining/placing, atomic stockpile/crafting, clock, basic HUD and versioned quicksave | Core tests pass; Unreal builds; a player can mine, craft, place and reload an edited world in a packaged build |
| M2 — survival day | Hunger/thirst/stamina/temperature, tool durability, hearth/shelter, injury/recovery and tutorial | A full 24-minute game day can be played, saved and resumed without duplication, starvation exploits or lost inventory |
| M3 — living settlement | 10-state citizen behavior, jobs, pathfinding, housing, hauling, food and needs, actual ledger assignments | 30 citizens autonomously maintain a bread chain for 10 days; blocked paths and resource contention recover |
| M4 — economy and land | Nine crops, seasons/irrigation/fertility, animal husbandry, metallurgy, storage/spoilage, trade and dynamic prices | Resource-conservation scenarios and season transitions pass; economy remains stable over 100 simulated days |
| M5 — construction and conflict | Blueprints, structural stability, fire/gas, melee/archery/armor, raids, training, formations and siege | Saveable building and combat damage, defensible settlement, consistent navigation after destruction |
| M6 — civic realm | Families/aging, health/epidemics/sanitation, crime/courts/laws, education/culture/religion/death | Causal citizen stories and recoverable epidemics/crime; no stalled entities or dangling references |
| M7 — sovereign realm | Factions/diplomacy/borders, ranks/technology, exploration/quests, bosses and three victories | Every progression path is reachable and completes under automated rule scenarios and human playtests |
| M8 — presentation and release | Art/animation/audio, accessibility/localization, 2–4 player host-authoritative co-op, Steam integration, Linux, optimization | Packaged build QA, multiplayer consistency, save migration, crash-free soak and measured performance on declared hardware |

Milestones are dependencies, not calendar promises. No milestone is complete merely because source files exist. Each feature needs implementation, automated checks where meaningful, an Unreal integration check, and player-facing validation.

## First execution batch

1. Create project knowledge folders, this plan and task ledger.
2. Generate a GDD section-to-milestone matrix and resolve engine-specific conflicts.
3. Implement and execute portable core tests: negative coordinate division, seeded generation, boundary meshing, item transactions, edit restoration, corrupt-save rejection, clock progression.
4. Add Unreal project/targets/module, playable adapters, editor bootstrap and environment-aware build scripts.
5. Compile Unreal if installed; otherwise preserve this gate as blocked and provide exact setup steps. Never represent standalone core tests as an Unreal build.

## Quality and performance gates

- Correctness before art: no free items, partial craft consumption, overwritten slots, stale mesh boundaries, incompatible silent save loads or duplicate citizen assignments.
- Initial target: 1080p, 60 FPS on the user's RTX 4060 Laptop after profiling. This is a target, not a measured result. Tune Lumen/shadow/scalability to actual laptop thermals and VRAM.
- Dense chunk access is O(1); generation and reference meshing are O(chunk volume), memory O(volume + emitted faces). Edited-boundary rebuilding touches at most four horizontal neighbor chunks. Later async work uses immutable snapshots, generation IDs and bounded main-thread uploads.
- Do not carry the GDD's unmeasured 1 ms/no-hitch, RAM, AI-count or save-size claims forward as facts. Capture Unreal Insights, GPU timings and reproducible seeds before signing performance gates.
- Preserve the previous valid save on write failure. Validate lengths, IDs, coordinates and versions before applying a loaded snapshot. Production saves add SHA-256, compression, rolling backups and migrations before M1 is signed off.
- Continuous integration: standalone core tests on Windows/Linux; Unreal Automation Tool build/test/package on a machine with licensed engine prerequisites. Docker is unnecessary for the desktop runtime.

## Environment and references

Observed 2026-09-23: 31.7 GiB RAM, NVIDIA RTX 4060 Laptop GPU; about 17 GiB free on C and 198 GiB on D. Unreal/Visual Studio installations were not found in standard folders/registry. Engine binaries, build caches and future DDC should use D after setup. No large downloads or license acceptance have been performed.

- Epic toolchain compatibility: https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine
- Epic hardware guidance: https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine
- ProceduralMeshComponent API: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/ProceduralMeshComponent/UProceduralMeshComponent

Epic currently documents UE 5.8 with Visual Studio 2026 for general development; the compatibility table also lists VS 2022 17.14+. Confirm exact installed engine requirements before compiling.
