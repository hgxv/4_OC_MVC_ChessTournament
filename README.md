# Projet_4_OC

git clone https://github.com/hgxv/Projet_4_OC

cd chemin\du\projet

# Création de l'environnement virtuel

py -m venv env

# Lancement de l'environnement virtuel

env\scripts\activate (Windows)

source env/bin/activate (Linux)

# Installation des requirements

py -m pip install -r requirements.txt

# Lancement du projet

py main.py

# Naviguez selon les menus à l'écran !


# Pour générer un nouveau rapport Flake
Dans le répertoire principal: 

flake8 --format=html --htmldir=flake-report
