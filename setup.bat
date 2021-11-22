@echo off & cls
@setlocal enableextensions
@cd /d "%~dp0"

::: Check installation path
if not exist C:\geckodriver\bin ( goto SETUP ) else ( goto SETUPCOMPLETED )

::: If geckodriver is not installed, check if the script is running
::: with administrator privileges and then install geckodriver
:SETUP
net session >nul 2>&1
if %errorlevel% == 0 (
    echo In order to use this program you MUST have installed:
    echo - Python 3.10
    echo - Firefox
    echo This setup WILL NOT download / install them.
    echo Press enter to continue installation...
    pause >nul
    md "C:\geckodriver\bin"
    copy "%cd%\ext\geckodriver.exe" "C:\geckodriver\bin"
    setx PATH "%path%;C:\geckodriver\bin"
    pip install -r %cd%\requirements.txt
    cls
    color 0a
    echo Setup completed, to start the bot
    echo re-run the script.
    pause >nul
    goto END
) else ( goto NOTADMIN )

::: If the setup has alredy been performed, run the bot
:SETUPCOMPLETED
color 0e
echo Geckodriver has been installed
echo Skipping installation.
echo Press enter to continue...
pause >nul
goto RUN

::: If the script is not running as an administrator, close it
:NOTADMIN
color 0c
echo It seems like you haven't executed the setup yet
echo Run this script with administrator privileges to start it.
echo Press enter to continue...
pause >nul
goto END

::: If everything is installed, run the python bot
:RUN
run.bat
goto END

::: Close the script
:END
exit
