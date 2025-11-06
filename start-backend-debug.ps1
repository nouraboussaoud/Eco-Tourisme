#!/usr/bin/env pwsh
# Script de démarrage du backend avec debug détaillé

Write-Host "================================" -ForegroundColor Cyan
Write-Host "🚀 DÉMARRAGE BACKEND - MODE DEBUG" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Aller dans le dossier backend
Set-Location -Path "$PSScriptRoot\backend"

# Vérifier que le venv existe
if (!(Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ ERREUR: venv non trouvé!" -ForegroundColor Red
    Write-Host "💡 Solution: Créez le venv avec:" -ForegroundColor Yellow
    Write-Host "   python -m venv venv" -ForegroundColor Yellow
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Activation du venv..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

Write-Host "✅ Vérification des dépendances..." -ForegroundColor Green
$fastapi = python -m pip show fastapi 2>$null
if (!$fastapi) {
    Write-Host "⚠️  FastAPI non installé, installation..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "📋 CONFIGURATION" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Lire la config
$env_content = Get-Content ".env" -ErrorAction SilentlyContinue
if ($env_content) {
    Write-Host "📄 Fichier .env trouvé:" -ForegroundColor Green
    $env_content | ForEach-Object {
        if ($_ -notmatch "^#" -and $_ -match "=") {
            Write-Host "   $_" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "⚠️  Fichier .env non trouvé" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🔧 TESTS PRÉ-DÉMARRAGE" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Test si Fuseki tourne
Write-Host "🔍 Test connexion Fuseki..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3030" -TimeoutSec 2 -ErrorAction SilentlyContinue
    Write-Host "✅ Fuseki accessible sur http://localhost:3030" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Fuseki non accessible" -ForegroundColor Yellow
    Write-Host "   → Le backend utilisera le Mock Client" -ForegroundColor Gray
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🚀 DÉMARRAGE DU SERVEUR" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📡 Backend sera accessible sur:" -ForegroundColor Green
Write-Host "   • API:     http://localhost:8000" -ForegroundColor Cyan
Write-Host "   • Docs:    http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   • Health:  http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Pour tester rapidement:" -ForegroundColor Yellow
Write-Host "   curl http://localhost:8000/health" -ForegroundColor Gray
Write-Host "   curl http://localhost:8000/destinations" -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 Pour arrêter: Ctrl+C" -ForegroundColor Red
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "📝 LOGS EN TEMPS RÉEL" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Démarrer le serveur
python main.py
