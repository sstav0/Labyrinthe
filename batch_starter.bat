@echo off
set /p aiNumber=Enter the player's index of the AI: 
set /p ans=Press O if you'd like to use your IP address or press N if you'd like to enter new IP address:
if %ans%==O python C:\Users\xavier\OneDrive\Bureau\LABYRINTHE\Labyrinthe\ai_starter.py --aiNumber %aiNumber%
if %ans%==N set /p IPaddress=Enter new IP address:
python C:\Users\xavier\OneDrive\Bureau\LABYRINTHE\Labyrinthe\ai_starter.py --IPaddress %IPaddress% --aiNumber %aiNumber%

pause