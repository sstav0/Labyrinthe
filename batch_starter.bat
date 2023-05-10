@echo off

set /p aiNumber=Enter the player's index of the AI: 
python "C:\Users\xavier\Desktop\LABYRINTHE\Labyrinthe\ai_starter.py" --aiNumber %aiNumber% 

pause