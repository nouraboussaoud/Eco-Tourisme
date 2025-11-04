# 🚀 QUICK LAUNCHER - EcoTravel Platform
# Usage: .\quick-start.ps1

Write-Host "`n" -ForegroundColor White
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "║              🚀 EcoTravel Platform - Quick Launcher 🚀            ║" -ForegroundColor Cyan
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Set locations
$projectPath = "c:\Users\abous\OneDrive\Bureau\webSemantique"
$backendPath = "$projectPath\backend"
$frontendPath = "$projectPath\frontend"
$fusekiPath = "C:\apache-jena-fuseki"

# Display menu
Write-Host "📌 SELECT AN OPTION:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [1] ⚡ Start Everything (Recommended)" -ForegroundColor Green
Write-Host "  [2] 🗄️  Start Fuseki Only" -ForegroundColor Cyan
Write-Host "  [3] 🔙 Start Backend Only" -ForegroundColor Cyan
Write-Host "  [4] 🎨 Start Frontend Only" -ForegroundColor Cyan
Write-Host "  [5] 🔧 Manual Setup (Show Instructions)" -ForegroundColor Cyan
Write-Host "  [6] ❌ Exit" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "Enter your choice (1-6)"

function Start-Fuseki {
    Write-Host "`n✨ Starting Fuseki (SPARQL Database)..." -ForegroundColor Yellow
    Write-Host "   ⏳ Please wait..." -ForegroundColor Gray
    
    if (-not (Test-Path $fusekiPath)) {
        Write-Host "   ❌ Fuseki not found at: $fusekiPath" -ForegroundColor Red
        Write-Host "   📥 Download: https://jena.apache.org/download/index.cgi" -ForegroundColor Yellow
        return $false
    }
    
    Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "cd '$fusekiPath'; .\fuseki-server.bat --update --mem /eco-tourism"
    
    Start-Sleep -Seconds 2
    return $true
}

function Start-Backend {
    Write-Host "`n✨ Starting Backend (FastAPI)..." -ForegroundColor Yellow
    Write-Host "   ⏳ Please wait..." -ForegroundColor Gray
    
    if (-not (Test-Path "$backendPath\venv")) {
        Write-Host "`n   📦 Creating Python venv..." -ForegroundColor Cyan
        cd $backendPath
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        
        Write-Host "   📦 Installing requirements..." -ForegroundColor Cyan
        pip install -q -r requirements.txt
    }
    
    Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "cd '$backendPath'; .\venv\Scripts\Activate.ps1; python main.py"
    
    Start-Sleep -Seconds 2
    return $true
}

function Start-Frontend {
    Write-Host "`n✨ Starting Frontend (React)..." -ForegroundColor Yellow
    Write-Host "   ⏳ Please wait..." -ForegroundColor Gray
    
    if (-not (Test-Path "$frontendPath\node_modules")) {
        Write-Host "   📦 Installing npm packages..." -ForegroundColor Cyan
        cd $frontendPath
        npm install --quiet
    }
    
    Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "cd '$frontendPath'; npm run dev"
    
    Start-Sleep -Seconds 2
    return $true
}

switch ($choice) {
    "1" {
        Write-Host "`n🚀 Starting all services..." -ForegroundColor Green
        Write-Host ""
        
        $fuseki_ok = Start-Fuseki
        $backend_ok = Start-Backend
        $frontend_ok = Start-Frontend
        
        if ($fuseki_ok -and $backend_ok -and $frontend_ok) {
            Write-Host "`n" + "═"*70 -ForegroundColor Green
            Write-Host "✅ ALL SERVICES STARTED!" -ForegroundColor Green
            Write-Host "═"*70 + "`n" -ForegroundColor Green
            
            Write-Host "📍 Access Points:" -ForegroundColor Cyan
            Write-Host "   🎨 Frontend:    http://localhost:3000" -ForegroundColor Yellow
            Write-Host "   🔧 API:         http://localhost:8000" -ForegroundColor Yellow
            Write-Host "   📚 API Docs:    http://localhost:8000/docs" -ForegroundColor Yellow
            Write-Host "   🗄️  Fuseki:     http://localhost:3030" -ForegroundColor Yellow
            Write-Host ""
            
            Write-Host "💡 Tips:" -ForegroundColor Cyan
            Write-Host "   • Don't close any terminal windows" -ForegroundColor Gray
            Write-Host "   • Services will keep running in the background" -ForegroundColor Gray
            Write-Host "   • Check terminal logs for errors" -ForegroundColor Gray
            Write-Host "   • Press Ctrl+C in any terminal to stop that service" -ForegroundColor Gray
            Write-Host ""
            
            # Open browser
            Write-Host "🌐 Opening application in browser..." -ForegroundColor Green
            Start-Process "http://localhost:3000"
            
            Write-Host "`n✨ Ready to go! Enjoy! 🎉" -ForegroundColor Green
            Write-Host ""
        } else {
            Write-Host "`n❌ Some services failed to start. Check the requirements." -ForegroundColor Red
        }
    }
    
    "2" {
        Write-Host "`n🗄️  Starting Fuseki..." -ForegroundColor Green
        Start-Fuseki | Out-Null
        Write-Host "✅ Fuseki started! Access: http://localhost:3030" -ForegroundColor Green
    }
    
    "3" {
        Write-Host "`n🔙 Starting Backend..." -ForegroundColor Green
        Start-Backend | Out-Null
        Write-Host "✅ Backend started! Access: http://localhost:8000" -ForegroundColor Green
    }
    
    "4" {
        Write-Host "`n🎨 Starting Frontend..." -ForegroundColor Green
        Start-Frontend | Out-Null
        Write-Host "✅ Frontend started! Access: http://localhost:3000" -ForegroundColor Green
    }
    
    "5" {
        Write-Host "`n📖 MANUAL STARTUP INSTRUCTIONS" -ForegroundColor Yellow
        Write-Host "═"*70 + "`n"
        
        Write-Host "TERMINAL 1 - Fuseki:" -ForegroundColor Cyan
        Write-Host "  cd C:\apache-jena-fuseki" -ForegroundColor Green
        Write-Host "  .\fuseki-server.bat --update --mem /eco-tourism" -ForegroundColor Green
        Write-Host "  → Access: http://localhost:3030" -ForegroundColor Gray
        Write-Host ""
        
        Write-Host "TERMINAL 2 - Backend:" -ForegroundColor Cyan
        Write-Host "  cd $backendPath" -ForegroundColor Green
        Write-Host "  python -m venv venv" -ForegroundColor Green
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Green
        Write-Host "  pip install -r requirements.txt" -ForegroundColor Green
        Write-Host "  python main.py" -ForegroundColor Green
        Write-Host "  → Access: http://localhost:8000" -ForegroundColor Gray
        Write-Host ""
        
        Write-Host "TERMINAL 3 - Frontend:" -ForegroundColor Cyan
        Write-Host "  cd $frontendPath" -ForegroundColor Green
        Write-Host "  npm install" -ForegroundColor Green
        Write-Host "  npm run dev" -ForegroundColor Green
        Write-Host "  → Access: http://localhost:3000" -ForegroundColor Gray
        Write-Host ""
        Write-Host "═"*70 + "`n"
    }
    
    "6" {
        Write-Host "`n👋 Goodbye!" -ForegroundColor Yellow
        exit 0
    }
    
    default {
        Write-Host "`n❌ Invalid choice. Please run again and select 1-6." -ForegroundColor Red
    }
}

Write-Host ""
Read-Host "Press Enter to continue"
