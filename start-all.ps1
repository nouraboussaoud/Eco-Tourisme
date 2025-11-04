# Script de démarrage pour EcoWaste Manager (PowerShell)
# Usage: .\start-all.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         EcoWaste Manager - Startup Script                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Paths
$fusekiPath = "C:\apache-jena-fuseki-4.10.0"
$projectRoot = Get-Location

# Vérifier Fuseki
if (-not (Test-Path $fusekiPath)) {
    Write-Host "❌ ERROR: Apache Jena Fuseki non trouvé!" -ForegroundColor Red
    Write-Host "Télécharger depuis: https://jena.apache.org/download/index.cgi" -ForegroundColor Yellow
    Write-Host "Extraire dans: C:\apache-jena-fuseki-x.x.x" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Configuration validée" -ForegroundColor Green
Write-Host ""

# Menu
Write-Host "Sélectionnez une action:" -ForegroundColor Cyan
Write-Host "[1] Démarrer tous les services" -ForegroundColor White
Write-Host "[2] Démarrer seulement Fuseki" -ForegroundColor White
Write-Host "[3] Démarrer seulement Backend" -ForegroundColor White
Write-Host "[4] Démarrer seulement Frontend" -ForegroundColor White
Write-Host "[5] Quitter" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Entrez votre choix (1-5)"

function Start-Fuseki {
    Write-Host ""
    Write-Host "[1/3] 🚀 Démarrage de Fuseki..." -ForegroundColor Yellow
    Start-Process -FilePath "powershell" -ArgumentList `
        "-NoExit", "-Command", `
        "cd '$fusekiPath'; .\fuseki-server.bat --update --mem /waste_management"
    Start-Sleep -Seconds 3
}

function Start-Backend {
    Write-Host "[2/3] 🚀 Démarrage du Backend (FastAPI)..." -ForegroundColor Yellow
    Start-Process -FilePath "powershell" -ArgumentList `
        "-NoExit", "-Command", `
        "cd '$projectRoot\backend'; .\venv\Scripts\Activate.ps1; python main.py"
    Start-Sleep -Seconds 3
}

function Start-Frontend {
    Write-Host "[3/3] 🚀 Démarrage du Frontend (React)..." -ForegroundColor Yellow
    Start-Process -FilePath "powershell" -ArgumentList `
        "-NoExit", "-Command", `
        "cd '$projectRoot\frontend'; npm run dev"
    Start-Sleep -Seconds 3
}

switch ($choice) {
    "1" {
        Start-Fuseki
        Start-Backend
        Start-Frontend
        
        Write-Host ""
        Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
        Write-Host "║     ✓ Tous les services sont en démarrage!                ║" -ForegroundColor Green
        Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 Accéder à:" -ForegroundColor Cyan
        Write-Host "   Frontend:   http://localhost:3000" -ForegroundColor Green
        Write-Host "   Backend:    http://localhost:8000" -ForegroundColor Green
        Write-Host "   Fuseki:     http://localhost:3030" -ForegroundColor Green
        Write-Host "   API Docs:   http://localhost:8000/docs" -ForegroundColor Green
        Write-Host ""
    }
    "2" { Start-Fuseki }
    "3" { Start-Backend }
    "4" { Start-Frontend }
    "5" { exit 0 }
    default { Write-Host "Choix invalide" -ForegroundColor Red }
}
