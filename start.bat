@echo off
echo Checking Python installation...
where python >nul 2>nul || (
    echo Python is not installed. Please install it before running the bot.
    pause
    exit /b
)

echo Installing dependencies...
pip install -r requirements.txt

echo Starting Discord bot...
python main.py

echo Bot has stopped. Press any key to restart...
pause
start start.bat
