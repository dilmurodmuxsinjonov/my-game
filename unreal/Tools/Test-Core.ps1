param([string]$Compiler = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$repoRoot = Split-Path $projectRoot -Parent
$outputDir = Join-Path $projectRoot 'Build\CoreTests'
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
if (-not $Compiler) { $Compiler = Join-Path $repoRoot '.tools\compiler\ziglang\zig.exe' }
if (-not (Test-Path -LiteralPath $Compiler)) {
    throw 'Portable compiler missing. Install ziglang==0.14.1 with pip --target .tools/compiler, or use CMake with MSVC/GCC/Clang.'
}
$env:ZIG_GLOBAL_CACHE_DIR = Join-Path $outputDir 'zig-cache'
$binary = Join-Path $outputDir 'RealmCoreTests.exe'
& $Compiler c++ -std=c++17 -Wall -Wextra -Werror -pedantic -O2 "-I$projectRoot\Source\VoxelLord\Core" (Join-Path $projectRoot 'Source\VoxelLord\Core\RealmCore.cpp') (Join-Path $projectRoot 'Tests\RealmCoreTests.cpp') -o $binary
if ($LASTEXITCODE -ne 0) { throw "Core compilation failed ($LASTEXITCODE)." }
& $binary
if ($LASTEXITCODE -ne 0) { throw "Core tests failed ($LASTEXITCODE)." }
