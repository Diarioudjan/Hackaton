# Signal Urbain

Signal Urbain est une plateforme de signalement et de navigation urbaine développée avec Django. Elle permet aux utilisateurs de signaler des problèmes urbains (routes endommagées, coupures électriques, gestion des déchets) et de consulter une cartographie interactive.

---

## **Prérequis**

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :
- Python 3.8 ou supérieur
- Pip (pip install -r requirements.txt)
- Virtualenv (optionnel mais recommandé)

---

## **Installation**

1. **Clonez le dépôt** :
   ```bash
   git clone <URL_DU_DEPOT>
   cd Signal_Urbain

## Fonctionnalités
Signalement des problèmes urbains : Les utilisateurs peuvent signaler des problèmes avec une description, une photo et une localisation GPS.
Cartographie interactive : Visualisation des signalements sur une carte en temps réel.
Authentification : Inscription, connexion, réinitialisation de mot de passe.
Tableau de bord pour les autorités : Suivi des signalements et gestion des interventions.
Structure du projet
signalements/ : Application pour gérer les signalements urbains.
utilisateurs/ : Application pour la gestion des utilisateurs (inscription, connexion, etc.).
templates/ : Dossier contenant les fichiers HTML pour les interfaces utilisateur.
static/ : Dossier contenant les fichiers CSS, JavaScript et images.
db.sqlite3 : Base de données SQLite utilisée pour stocker les données.

## Structure du projet
signalements/ : Application pour gérer les signalements urbains.
utilisateurs/ : Application pour la gestion des utilisateurs (inscription, connexion, etc.).
templates/ : Dossier contenant les fichiers HTML pour les interfaces utilisateur.
static/ : Dossier contenant les fichiers CSS, JavaScript et images.
db.sqlite3 : Base de données SQLite utilisée pour stocker les données.

## Technologies utilisées
Backend : Django 4.x
Base de données : SQLite (par défaut)
Frontend : HTML, CSS, JavaScript
Cartographie : Intégration avec une bibliothèque comme Leaflet.js ou Google Maps API (selon votre implémentation)