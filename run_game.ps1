# run_game.ps1 - Voxel Lord: Feudal Realm Master PowerShell Launcher
param(
    [switch]$Test,
    [switch]$Sim,
    [string]$GodotPath = ""
)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "           VOXEL LORD: FEUDAL REALM - POWERSHELL LAUNCHER" -ForegroundColor Yellow
Write-Host "     First-Person Medieval Voxel Colony Simulator (Godot 4.3 / C++ Core)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

if ($Test) {
    Write-Host "[*] Executing Automated Test Suite..." -ForegroundColor Green
    python -m unittest discover -s "$ScriptDir\tests" -p "test_*.py"
    exit $LASTEXITCODE
}

if ($Sim) {
    Write-Host "[*] Launching Standalone Interactive Playable Simulator..." -ForegroundColor Green
    python "$ScriptDir\tools\interactive_play_simulator.py"
    exit $LASTEXITCODE
}

# Locate Godot
$GodotExe = $null

if ($GodotPath -ne "" -and (Test-Path $GodotPath)) {
    $GodotExe = $GodotPath
} elseif (Get-Command godot -ErrorAction SilentlyContinue) {
    $GodotExe = "godot"
} elseif (Test-Path "$ScriptDir\godot.exe") {
    $GodotExe = "$ScriptDir\godot.exe"
} elseif (Test-Path "C:\Godot\godot.exe") {
    $GodotExe = "C:\Godot\godot.exe"
} elseif (Test-Path "C:\Program Files\Godot\godot.exe") {
    $GodotExe = "C:\Program Files\Godot\godot.exe"
} else {
    $dl = Get-ChildItem "$env:USERPROFILE\Downloads" -Filter "Godot_v4*.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($dl) {
        $GodotExe = $dl.FullName
    }
}

if ($GodotExe) {
    Write-Host "[+] Found Godot Engine: $GodotExe" -ForegroundColor Green
    Write-Host "[+] Launching Voxel Lord project at $ScriptDir..." -ForegroundColor Cyan
    & $GodotExe --path $ScriptDir res://scenes/main.tscn
} else {
    Write-Host "[-] Godot 4.3 binary not found in standard system locations." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Select an action:" -ForegroundColor White
    Write-Host "  [1] Launch Instant Interactive Playable Simulator (Python Engine)" -ForegroundColor Cyan
    Write-Host "  [2] Run Automated Realism Test Suite (300+ Tests)" -ForegroundColor Green
    Write-Host "  [3] Attempt automatic Godot installation via winget" -ForegroundColor Yellow
    Write-Host "  [4] Exit" -ForegroundColor Red
    Write-Host ""
    $choice = Read-Host "Enter option [1-4]"

    switch ($choice) {
        "1" {
            python "$ScriptDir\tools\interactive_play_simulator.py"
        }
        "2" {
            python -m unittest discover -s "$ScriptDir\tests" -p "test_*.py"
        }
        "3" {
            winget install GodotEngine.GodotEngine
        }
        Default {
            Write-Host "Exiting launcher." -ForegroundColor White
        }
    }
}
