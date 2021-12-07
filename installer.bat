@echo off
REM checking the virtualenv library is present (and install it if not)
pip install virtualenv
REM create a new virtual environment for the application
virtualenv venv
REM activate the environment
call venv/bin/activate.bat
REM install needed libraries inside the environment
pip install -r requirements.txt
echo Application installation completed
REM writing the app launcher
>triplifier.bat (
  REM suppress commands output
  echo @echo off
  REM activating virtual environment
  echo call venv\scripts\activate.bat
  REM launch app
  echo start "" flask run
  REM launch default navigator at app url
  echo start "" http://localhost:5000
  REM deactivate virtual environment (only useful if launched from another terminal)
  echo deactivate
)
echo It can be launched with the 'triplifier.bat' executable
echo Press space to close the installation program, it will then destroy itself
pause
REM destroy installation file (this)
(goto) 2>nul & del "%~f0"
