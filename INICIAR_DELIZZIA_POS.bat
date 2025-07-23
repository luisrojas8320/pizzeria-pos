@echo off
title Delizzia POS - Sistema de Punto de Venta
color 0A
echo.
echo  ========================================
echo   🍕 DELIZZIA POS - INICIANDO SISTEMA
echo  ========================================
echo.

cd /d "%~dp0"

echo ⏳ Preparando entorno...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no encontrado. Instala Python desde python.org
    pause
    exit /b 1
)

REM Preparar entorno Python - MÉTODO SIMPLE Y ROBUSTO
echo 📦 Preparando entorno Python...
cd backend

REM Siempre recrear entorno para garantizar dependencias correctas
if exist "venv" (
    echo 🔄 Limpiando entorno virtual anterior...
    rmdir /s /q venv 2>nul
)

echo 🆕 Creando nuevo entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)

echo 📦 Instalando dependencias Python...
call venv\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias Python
    pause
    exit /b 1
)

echo ✅ Entorno Python listo
cd ..

REM Configurar base de datos SQLite
if not exist "backend\.env" (
    echo 🔐 Configurando entorno inicial...
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env" >nul
        echo ✅ Configuración copiada desde .env.example
    ) else (
        echo DATABASE_URL=sqlite:///./delizzia_pos.db > backend\.env
        echo SECRET_KEY=CHANGE_THIS_SECRET_KEY_FOR_PRODUCTION >> backend\.env
        echo ENVIRONMENT=development >> backend\.env
        echo SQL_ECHO=false >> backend\.env
    )
)

echo 🚀 Iniciando Backend (FastAPI)...
cd backend
start "Delizzia Backend" cmd /k "venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"
cd ..

echo ⏳ Esperando backend (3 segundos)...
timeout /t 3 /nobreak >nul

REM Verificar Node.js
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Node.js no encontrado. Instala Node.js desde nodejs.org
    pause
    exit /b 1
)

echo 🎨 Verificando dependencias del frontend...
if not exist "node_modules" (
    echo 📦 Instalando dependencias del frontend...
    npm install --legacy-peer-deps
    if errorlevel 1 (
        echo ❌ Error instalando dependencias del frontend
        pause
        exit /b 1
    )
)

echo 🌐 Iniciando Frontend (React)...
cd /d "%~dp0"
start "Delizzia Frontend" /B npm run dev

echo ⏳ Esperando frontend (20 segundos)...
timeout /t 20 /nobreak >nul

echo 🌍 Abriendo navegador...
start http://localhost:3000

echo.
echo  ========================================
echo   ✅ DELIZZIA POS INICIADO CORRECTAMENTE
echo   🌐 Frontend: http://localhost:3000
echo   📡 Backend: http://localhost:8000/docs
echo  ========================================
echo.
echo 💡 Para crear usuario administrador ejecuta:
echo    cd backend
echo    python scripts/create_admin.py
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul