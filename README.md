Jurisconsult (Django)

Application web pour la gestion des consultations juridiques entre avocats et clients (UI en français).

Prérequis
- Python 3.11+
- Windows PowerShell (ou bash)

Installation
```bash
python -m venv .venv
.venv\Scripts\pip install --upgrade pip
.venv\Scripts\pip install "Django>=5.0,<6.0" django-crispy-forms crispy-bootstrap5 Pillow psycopg[binary]
```

Configuration
- Paramètres clés dans `jurisconsult/settings.py`:
  - `LANGUAGE_CODE = 'fr'`
  - `TIME_ZONE = 'Africa/Douala'`
  - `AUTH_USER_MODEL = 'accounts.User'`
  - `STATICFILES_DIRS`, `MEDIA_ROOT`

Initialisation de la base
```bash
.venv\Scripts\python manage.py makemigrations
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py createsuperuser
```

Données de démo
```bash
.venv\Scripts\python manage.py seed_demo
```

Lancer le serveur
```bash
.venv\Scripts\python manage.py runserver
```
- Accueil: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Comptes de démo
- Superuser: `admin` (mdp défini lors de la création)
- Avocat: `avocat1` / `password123`
- Client: `client1` / `password123`

Fonctionnalités (MVP)
- Utilisateur personnalisé (client/avocat/admin)
- Profils avocat/client, spécialités
- Recherche avocats (nom, ville, spécialité)
- Réservation d’une consultation
- Modèles messagerie et paiements
- UI Bootstrap en français

Évolutions prévues
- Notifications email et internes
- Paiement mobile money/carte
- Agenda/Disponibilités
- Avis et notes

