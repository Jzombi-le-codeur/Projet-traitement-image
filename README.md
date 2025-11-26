# Projet
Ce projet a été créé dans le cadre d'un projet de NSI, disponible [ici](https://raisintine.fr/chocolatine/document.php?id=399). \
Il s'agit d'un logiciel permettant d'appliquer des **filtres** sur des fichiers `.pbm`, `.pgm` et `.ppm` sur des images de type `P1`, `P2` et `P3`.

# Installation
## Requirements
- `Python 3` _(le projet est codé en `python3.13`)_
- `pip`

## Etapes
### 1. Téléchargement du repo
- Cloner le repo
```powershell
git clone https://github.com/Jzombi-le-codeur/Projet-traitement-image
```
- Extraire le repo
- Se placer dans le dossier du repo

### 2. Installation des dépendances
- Créer un environnement virtuel et l'activer
```powershell
python -m venv .venv; .venv\Scripts\activate.ps1
```
- Installer les dépendances
```
pip install -r requirements.txt
```

# Lancement
- Se placer à la racine du repo
- Lancer le programme :
```powershell
python main.py
```
