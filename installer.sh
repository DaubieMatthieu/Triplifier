#!/bin/bash -x
# checking the virtualenv library is present (and install it if not)
pip install virtualenv
# create a new environment for the application
virtualenv venv
# activate the environment
source venv/bin/activate
# install needed libraries inside the environment
pip install -r requirements.txt
{ echo "Application installation completed"; } 2>/dev/null
# writing the app launcher
touch triplifier.sh
cat >triplifier.sh <<EOT
#!/bin/bash -x
# activating virtual environment
source venv/bin/activate
# launch app
flask run
# launch default navigator at app url
xdg-open http://127.0.0.0:5000 || true
open http://127.0.0.0:5000 || true
# deactivate virtual environment (only useful if launched from another terminal)
deactivate
EOT
# make the script executable
chmod +x triplifier.sh
{
  echo 'It can be launched with the "triplifier.sh" executable'
  echo "Press any key to close the installation program, it will then destroy itself"
} 2>/dev/null
read _
# destroy installation file (this)
rm -- "$0"
