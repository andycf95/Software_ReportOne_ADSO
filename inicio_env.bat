@echo off
REM Ir a la carpeta donde está este .bat
cd /d "%~dp0"

REM Activar entorno virtual ubicado en la carpeta env
call env\Scripts\activate.bat

REM Mantener la terminal abierta
cmd /k