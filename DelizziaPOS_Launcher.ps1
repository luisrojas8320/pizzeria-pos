# Delizzia POS PowerShell Launcher
# Versión avanzada con manejo de errores

param(
    [switch]$Stop
)

$Host.UI.RawUI.WindowTitle = "Delizzia POS Launcher"

function Write-ColoredOutput {
    param($Text, $Color = "Green")
    Write-Host $Text -ForegroundColor $Color
}

function Write-Header {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   🍕 DELIZZIA POS - LAUNCHER" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Test-Port {
    param($Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

function Stop-DelizziaPOS {
    Write-Header
    Write-ColoredOutput "🛑 Deteniendo Delizzia POS..." "Red"
    
    # Terminar procesos específicos
    Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
    
    # Liberar puertos
    $processes = Get-NetTCPConnection -LocalPort 3000,8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    foreach ($proc in $processes) {
        Stop-Process -Id $proc -Force -ErrorAction SilentlyContinue
    }
    
    Write-ColoredOutput "✅ Sistema detenido correctamente" "Green"
    Read-Host "Presiona Enter para salir"
    exit
}

function Start-DelizziaPOS {
    Write-Header
    
    # Verificar si Python está instalado
    try {
        $pythonVersion = python --version
        Write-ColoredOutput "✅ Python encontrado: $pythonVersion" "Green"
    }
    catch {
        Write-ColoredOutput "❌ Error: Python no encontrado. Instala Python desde python.org" "Red"
        Read-Host "Presiona Enter para salir"
        exit
    }
    
    # Verificar si Node.js está instalado
    try {
        $nodeVersion = node --version
        Write-ColoredOutput "✅ Node.js encontrado: $nodeVersion" "Green"
    }
    catch {
        Write-ColoredOutput "❌ Error: Node.js no encontrado. Instala Node.js desde nodejs.org" "Red"
        Read-Host "Presiona Enter para salir"
        exit
    }
    
    Write-Host ""
    Write-ColoredOutput "📦 Preparando entorno de desarrollo..." "Yellow"
    
    # Configurar entorno virtual
    if (!(Test-Path "backend\venv")) {
        Write-ColoredOutput "🔧 Creando entorno virtual por primera vez..." "Yellow"
        Set-Location backend
        python -m venv venv
        Set-Location ..
    }
    
    # Siempre actualizar dependencias
    Write-ColoredOutput "🔄 Verificando y actualizando dependencias de Python..." "Yellow"
    Set-Location backend
    & "venv\Scripts\Activate.ps1"
    pip install -r requirements.txt --quiet
    Set-Location ..
    
    # Configurar variables de entorno - MÉTODO SEGURO
    if (!(Test-Path "backend\.env")) {
        Write-ColoredOutput "🔐 Configurando entorno seguro inicial..." "Yellow"
        if (Test-Path "backend\.env.example") {
            Copy-Item "backend\.env.example" "backend\.env"
            Write-ColoredOutput "✅ Configuración copiada desde .env.example" "Green"
            Write-ColoredOutput "⚠️ IMPORTANTE: Revisa backend\.env para producción" "Yellow"
        } else {
            Write-ColoredOutput "🗄️ Creando configuración básica..." "Yellow"
            Set-Content "backend\.env" "DATABASE_URL=sqlite:///./delizzia_pos.db"
            Add-Content "backend\.env" "SECRET_KEY=CHANGE_THIS_SECRET_KEY_FOR_PRODUCTION"
            Add-Content "backend\.env" "ENVIRONMENT=development"
            Add-Content "backend\.env" "SQL_ECHO=false"
            Write-ColoredOutput "⚠️ ADVERTENCIA: Usa .env.example como referencia" "Red"
        }
    }
    
    # Verificar puertos disponibles
    if (Test-Port 8000) {
        Write-ColoredOutput "⚠️ Puerto 8000 ocupado. Deteniendo procesos..." "Yellow"
        Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    }
    
    if (Test-Port 3000) {
        Write-ColoredOutput "⚠️ Puerto 3000 ocupado. Deteniendo procesos..." "Yellow"
        Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    }
    
    # Iniciar Backend
    Write-ColoredOutput "🚀 Iniciando Backend (FastAPI)..." "Green"
    $backendJob = Start-Job -ScriptBlock {
        Set-Location $args[0]
        Set-Location backend
        & "venv\Scripts\Activate.ps1"
        uvicorn app.main:app --reload --port 8000
    } -ArgumentList (Get-Location)
    
    # Esperar backend
    Write-ColoredOutput "⏳ Esperando backend..." "Yellow"
    Start-Sleep -Seconds 8
    
    # Verificar si backend está corriendo
    if (Test-Port 8000) {
        Write-ColoredOutput "✅ Backend iniciado correctamente en puerto 8000" "Green"
    } else {
        Write-ColoredOutput "❌ Error iniciando backend" "Red"
        return
    }
    
    # Instalar dependencias frontend si es necesario
    if (!(Test-Path "node_modules")) {
        Write-ColoredOutput "📦 Instalando dependencias del frontend..." "Yellow"
        npm install --legacy-peer-deps
    }
    
    # Iniciar Frontend
    Write-ColoredOutput "🌐 Iniciando Frontend (React)..." "Green"
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location $args[0]
        npm run dev
    } -ArgumentList (Get-Location)
    
    # Esperar frontend
    Write-ColoredOutput "⏳ Esperando frontend..." "Yellow"
    Start-Sleep -Seconds 10
    
    # Verificar si frontend está corriendo
    if (Test-Port 3000) {
        Write-ColoredOutput "✅ Frontend iniciado correctamente en puerto 3000" "Green"
    } else {
        Write-ColoredOutput "❌ Error iniciando frontend" "Red"
        return
    }
    
    # Abrir navegador
    Write-ColoredOutput "🌍 Abriendo navegador..." "Cyan"
    Start-Process "http://localhost:3000"
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   ✅ DELIZZIA POS INICIADO" -ForegroundColor Green
    Write-Host "   🌐 Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "   📡 Backend:  http://localhost:8000/docs" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-ColoredOutput "💡 Para detener el sistema, ejecuta: .\DelizziaPOS_Launcher.ps1 -Stop" "Yellow"
    Write-Host ""
    
    # Mantener ventana abierta y monitorear
    Write-ColoredOutput "🔍 Monitoreando sistema (Presiona Ctrl+C para salir)..." "Yellow"
    try {
        while ($true) {
            Start-Sleep -Seconds 30
            if (!(Test-Port 8000) -or !(Test-Port 3000)) {
                Write-ColoredOutput "⚠️ Se detectó que un servicio se detuvo" "Red"
                break
            }
        }
    }
    catch {
        Write-ColoredOutput "🛑 Deteniendo sistema..." "Yellow"
    }
}

# Ejecutar función principal
if ($Stop) {
    Stop-DelizziaPOS
} else {
    Start-DelizziaPOS
}