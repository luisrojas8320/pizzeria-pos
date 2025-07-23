@echo off
title Crear Acceso Directo - Delizzia POS
color 0B
echo.
echo  ========================================
echo   🔗 CREANDO ACCESO DIRECTO EN ESCRITORIO
echo  ========================================
echo.

set "scriptPath=%~dp0INICIAR_DELIZZIA_POS.bat"
set "desktopPath=%USERPROFILE%\Desktop"
set "shortcutPath=%desktopPath%\Delizzia POS.lnk"

echo 📋 Creando acceso directo...

REM Crear script VBS temporal para crear el shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\shortcut.vbs"
echo sLinkFile = "%shortcutPath%" >> "%temp%\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\shortcut.vbs"
echo oLink.TargetPath = "%scriptPath%" >> "%temp%\shortcut.vbs"
echo oLink.WorkingDirectory = "%~dp0" >> "%temp%\shortcut.vbs"
echo oLink.Description = "Delizzia POS - Sistema de Punto de Venta" >> "%temp%\shortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,21" >> "%temp%\shortcut.vbs"
echo oLink.Save >> "%temp%\shortcut.vbs"

REM Ejecutar script VBS
cscript //nologo "%temp%\shortcut.vbs"

REM Limpiar archivo temporal
del "%temp%\shortcut.vbs"

if exist "%shortcutPath%" (
    echo.
    echo  ========================================
    echo   ✅ ACCESO DIRECTO CREADO EXITOSAMENTE
    echo   📍 Ubicación: %desktopPath%
    echo   🍕 Nombre: Delizzia POS
    echo  ========================================
    echo.
    echo 💡 Ahora puedes hacer doble clic en el ícono
    echo    del escritorio para iniciar el sistema
) else (
    echo ❌ Error creando el acceso directo
)

echo.
echo Presiona cualquier tecla para continuar...
pause >nul