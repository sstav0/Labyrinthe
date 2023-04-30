@echo off
set /p aiNumber=Enter the player's index of the AI: 
set /p response1=Change AI level ? o/n
if %response1%  == "o" (
	set /p aiLevel=Enter AI level:
	python "C:\Users\xavier\OneDrive\Bureau\LABYRINTHE\Labyrinthe\ai_starter.py" --aiNumber %aiNumber% --aiLevel %aiLevel%
)else (
	python "C:\Users\xavier\OneDrive\Bureau\LABYRINTHE\Labyrinthe\ai_starter.py" --aiNumber %aiNumber% 
)
pause