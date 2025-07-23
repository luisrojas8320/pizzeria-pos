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

REM Crear/recrear entorno virtual y dependencias
echo 📦 Preparando entorno Python...
cd backend

REM Si existe venv pero falta jose, recrear entorno
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python -c "import jose" 2>nul
    if errorlevel 1 (
        echo 🔄 Recreando entorno virtual (dependencias faltantes)...
        rmdir /s /q venv 2>nul
    )
    deactivate 2>nul
)

REM Crear entorno virtual si no existe
if not exist "venv\Scripts\activate.bat" (
    echo 🆕 Creando nuevo entorno virtual...
    python -m venv venv
)

REM Instalar dependencias
echo 📦 Instalando dependencias Python...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

REM Verificar instalación crítica
python -c "import jose; print('✅ python-jose instalado correctamente')" || (
    echo ❌ Error: python-jose no se pudo instalar
    pause
    exit /b 1
)

cd ..

REM Configurar base de datos SQLite - MÉTODO SEGURO
if not exist "backend\.env" (
    echo 🔐 Configurando entorno seguro inicial...
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env" >nul
        echo ✅ Configuración copiada desde .env.example
        echo ⚠️  IMPORTANTE: Revisa backend\.env para producción
    ) else (
        echo 🗄️ Creando configuración básica...
        echo DATABASE_URL=sqlite:///./delizzia_pos.db > backend\.env
        echo SECRET_KEY=CHANGE_THIS_SECRET_KEY_FOR_PRODUCTION >> backend\.env
        echo ENVIRONMENT=development >> backend\.env
        echo SQL_ECHO=false >> backend\.env
        echo ⚠️  ADVERTENCIA: Usa .env.example como referencia
    )
)

echo 🚀 Iniciando Backend (FastAPI)...
cd backend
start "Delizzia Backend" cmd /k "venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"
cd ..

echo ⏳ Esperando backend (5 segundos)...
timeout /t 5 /nobreak >nul

echo 🎨 Verificando dependencias del frontend...
if not exist "node_modules" (
    echo 📦 Instalando dependencias del frontend...
    npm install --legacy-peer-deps
)

echo 🌐 Iniciando Frontend (React)...
start "Delizzia Frontend" cmd /k "npm run dev"

echo ⏳ Esperando frontend (8 segundos)...
timeout /t 8 /nobreak >nul

echo 🌍 Abriendo navegador...
start http://localhost:3000

echo.
echo  ========================================
echo   ✅ DELIZZIA POS INICIADO CORRECTAMENTE
echo   🌐 Frontend: http://localhost:3000
echo   📡 Backend: http://localhost:8000/docs
echo  ========================================
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul