@echo off
title Detener Delizzia POS
color 0C
echo.
echo  ========================================
echo   🛑 DELIZZIA POS - DETENIENDO SISTEMA
echo  ========================================
echo.

echo 🔍 Buscando procesos de Delizzia POS...

REM Terminar procesos de Python (Backend)
echo 🐍 Terminando Backend (FastAPI)...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul

REM Terminar procesos de Node (Frontend)
echo ⚛️ Terminando Frontend (React)...
taskkill /f /im node.exe 2>nul

REM Terminar procesos por puerto específico
echo 🔌 Liberando puertos 3000 y 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /f /pid %%a 2>nul

echo.
echo  ========================================
echo   ✅ DELIZZIA POS DETENIDO CORRECTAMENTE
echo   🔒 Todos los procesos terminados
echo   🔓 Puertos liberados
echo  ========================================
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul