@echo off
REM Script de démarrage rapide pour EcoWaste Manager
REM Ce script ouvre 3 terminaux pour fuseki, backend et frontend

echo.
echo ========================================
echo  EcoWaste Manager - Startup Script
echo ========================================
echo.

REM Vérifier si fuseki existe
if not exist "C:\apache-jena-fuseki-4.10.0" (
    echo ERROR: Apache Jena Fuseki non trouvé!
    echo Télécharger depuis: https://jena.apache.org/download/index.cgi
    echo Extraire dans: C:\apache-jena-fuseki-4.x.x
    pause
    exit /b 1
)

echo [1/3] Démarrage de Fuseki...
start "Fuseki Server" cmd /k "cd C:\apache-jena-fuseki-4.10.0 && fuseki-server.bat --update --mem /waste_management"

timeout /t 3 /nobreak

echo [2/3] Démarrage du Backend (FastAPI)...
start "Backend API" cmd /k "cd backend && venv\Scripts\Activate.ps1 && python main.py"

timeout /t 3 /nobreak

echo [3/3] Démarrage du Frontend (React)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo  ✓ Tous les services sont en démarrage!
echo ========================================
echo.
echo Accéder à:
echo - Frontend:  http://localhost:3000
echo - Backend:   http://localhost:8000
echo - Fuseki:    http://localhost:3030
echo - API Docs:  http://localhost:8000/docs
echo.
echo Fermez cette fenêtre pour arrêter le script.
echo (Chaque service s'arrêtera quand vous fermerez son terminal)
echo.

pause
