# README — Installation rapide

Prérequis
- Python 3.8+ installé
- Accès au terminal (PowerShell, Cmd ou Bash)
- Fichier `requirements.txt` présent à la racine du projet

Étapes (depuis le dossier du projet, ex: C:\Users\nadji\...\api-fisherfans)
1. Créer l'environnement virtuel
```bash
python -m venv venv
```
2. Activer l'environnement
- PowerShell :
```powershell
.\venv\Scripts\Activate.ps1
```
- Cmd :
```cmd
venv\Scripts\activate.bat
```
- Bash (Linux/Mac) :
```bash
source venv/bin/activate
```
3. Mettre pip à jour et installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
4. Désactiver l'environnement (quand fini)
```bash
deactivate
```

Astuce
- Pour générer un `requirements.txt` à partir de l'environnement actif :
```bash
pip freeze > requirements.txt
```

Fin