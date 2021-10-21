echo off & cls
@setlocal enableextensions
@cd /d "%~dp0"

::: Check installation path
if not exist C:\geckodriver\bin ( goto SETUP ) else ( goto RUN )

::: If geckodriver has not been installed yet, run the setup
:SETUP
color 0c
echo It seems like you have not installed geckodriver
echo on your system, run "setup.bat" to install it.
pause >nul
goto END


::: Run the python bot
:RUN
python __main__.py

::: Exit the script
:END
exit
