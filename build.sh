#!/bin/bash

# Attiva l'ambiente virtuale
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt

# Esegui le migrazioni del database
python manage.py makemigrations
python manage.py migrate

# Avvia il server Django
python manage.py runserver