# FisherFans API

Bienvenue sur le dépôt du backend de **FisherFans**, la plateforme collaborative de mise en relation entre passionnés de pêche. Ce projet fournit une API RESTful robuste permettant la gestion des utilisateurs, des bateaux, des sorties en rivière/mer, des réservations et des carnets de pêche numériques.

## 📋 Contexte du Projet

L'objectif de cette API est de servir de socle technique fiable pour l'application cliente (Web/Mobile) de FisherFans. Elle respecte les contraintes du cahier des charges, notamment la recherche géographique de bateaux et la sécurisation des données utilisateurs.

### Technologies Principales
*   **Langage :** Python 3.9+
*   **Framework :** FastAPI (Performance, Asynchrone)
*   **ORM :** SQLModel (Abstraction SQL & Validation des données)
*   **Base de Données :** SQLite (fichiers locaux pour le prototype)
*   **Conteneurisation :** Docker & Docker Compose
*   **Tests :** Pytest

---

## 🚀 Installation et Démarrage

Vous pouvez lancer le projet de deux manières : via **Docker** (recommandé) ou manuellement en **Python local**.

### Option 1 : Via Docker (Recommandé)

Assurez-vous d'avoir Docker et Docker Compose installés sur votre machine.

1.  **Construire et lancer les conteneurs :**
    ```bash
    docker-compose up -d --build
    ```
2.  L'API sera accessible sur : `http://localhost:8000`
3.  Le serveur Nginx (Reverse Proxy) sera accessible sur : `http://localhost:80`

### Option 2 : Installation Manuelle (Python)

1.  **Créer un environnement virtuel :**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\Activate.ps1

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3.  **Lancer le serveur de développement :**
    ```bash
    uvicorn main:app --reload
    ```

---

## 📚 Documentation de l'API

Une documentation interactive est générée automatiquement à partir du code (conforme OpenAPI).

### 1. Swagger UI (Interface Interactive)
C'est l'interface privilégiée pour explorer et tester les points de terminaison (endpoints) directement depuis votre navigateur.
*   **URL :** [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Spécification OpenAPI (YAML)
Le fichier de spécification complet au format **OpenAPI 3.1 (AOS 3.1)** se trouve à la racine du projet. Ce fichier peut être importé dans des outils tiers comme Postman.
*   **Chemin du fichier :** `./fishersfan-api.yaml`

### 3. ReDoc
Une documentation alternative, plus axée sur la lecture.
*   **URL :** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Tests

Des tests fonctionnels sont inclus pour valider le comportement de l'API (scénarios nominaux et gestion des erreurs).

Pour lancer la suite de tests avec `pytest` :

```bash
# Assurez-vous d'être dans votre environnement virtuel
pytest -v
```

---

## 📂 Structure du Projet

```
api-fisherfans/
├── app/
│   ├── models/       # Modèles de données (SQLModel)
│   ├── routers/      # Routes de l'API (Endpoints)
│   ├── auth.py       # Gestion de l'authentification (JWT)
│   ├── database.py   # Configuration de la BDD
│   └── ...
├── nginx/            # Configuration du serveur web Nginx
├── tests/            # Tests fonctionnels (Pytest)
├── docker-compose.yml
├── Dockerfile
├── fishersfan-api.yaml  <-- Spécification API (OpenAPI 3.1)
├── main.py           # Point d'entrée de l'application
├── requirements.txt  # Dépendances Python
└── README.md         # Ce fichier
```

---

## 👥 Équipe Projet

*   Nadjide OMAR
*   Nawfel HILAL
