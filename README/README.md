# Finance API

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)](https://fastapi.tiangolo.com/)  
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/<VOTRE_USER>/<VOTRE_REPO>/actions)  
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/<VOTRE_USER>/<VOTRE_REPO>/actions)  

API **FastAPI** pour récupérer et analyser des données financières, calculer des indicateurs et générer des visualisations.

---

## Description

Cette API permet de :  
- Récupérer les données financières d’actions via **Yahoo Finance**.  
- Calculer des indicateurs financiers simples : rendement, volatilité, ratios financiers (ex. Sharpe ratio).  
- Générer des graphiques avec **Matplotlib**, exportés en images.  
- Fournir les résultats via un endpoint API JSON.  
- Tester l’application avec des tests unitaires et d’intégration.

---

## Fonctionnalités principales

1. **Récupération de données** : Yahoo Finance, période configurable (`1mo`, `6mo`, `1y`, etc.).  
2. **Calculs financiers** :  
   - Rendement moyen  
   - Volatilité  
   - Sharpe ratio 
3. **Visualisation** : Graphiques exportés en PNG avec Matplotlib.  
4. **API FastAPI** : Input → liste de symboles, output → JSON avec résultats.  
5. **Tests** :  
   - Vérification des calculs sur des datasets fictifs.  
   - Vérification de la structure JSON retournée.  
   - Gestion des erreurs (ex. symbole inconnu ou données vides).

---

## Installation

1. Cloner le projet :
```bash
git clone <URL_DU_DEPOT>
cd nom_du_projet
```
2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. Installer les dépendances :
```bash
pip install -r requirements.txt
```
## Lancer l'API
```bash
uvicorn app.main:app --reload
```
Accès : `http://127.0.0.1:8000`
## Endpoints principaux
### GET /calculate
Endpoint pour calculer le rendement, la volatilité et le ratio de Sharpe des actions demandées.

---
#### Paramètres

- **symbols** : liste d’actions séparées par des virgules. **Ex**: `AAPL,MSFT`  
- **period**  : période pour les données.**Ex**: `6mo`  

---

#### Exemple d’appel cURL

```bash
curl -X GET "http://127.0.0.1:8000/calculate?symbols=AAPL,MSFT&period=6mo" -H "accept: application/json"
```
#### Exemple de réponse 
````
{
  "query_symbols": ["AAPL", "MSFT"],
  "sharpe_ratios": {"AAPL": 1.2, "MSFT": 1.1},
  "volatility": {"AAPL": 0.25, "MSFT": 0.22}
}
````
### GET /metrics_image

Endpoint pour générer un graphique représentant l’évolution cumulée du rendement et de la volatilité des actions demandées.  
Le graphique est renvoyé encodé en **base64**.

---

#### Paramètres

- **symbols** : liste d’actions séparées par des virgules. **Ex**: `AAPL,MSFT`  
- **period**  : période pour les données. **Ex**: `6mo`  

---

#### Exemple d’appel cURL

```bash
curl -X GET "http://127.0.0.1:8000/metrics_image?symbols=AAPL,MSFT&period=6mo" -H "accept: application/json"
```
#### Graphique généré
Exemple d’image Matplotlib montrant l’évolution des actions :
![Visualisation](https://github.com/Yu9763/finance-api/raw/495696ecdda6b13a9c325ae319b608401d6c50dc/Visualisation.PNG)

## Tests
### Lancer des tests :
````
pytest
````
* Vérifie les calculs financiers sur un dataset fictif.
* Vérifie le format JSON renvoyé par l’API.
* Vérifie la gestion des erreurs (ex. symbole inconnu ou données vides).
  
## Structure du projet:
````
Mini-portfolio-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints.py      # endpoints FastAPI
│   ├── core/
│   │   ├── config.py            
│   │   └── __init__.py
│   ├── services/
│   │   ├── data_fetcher.py       # Récupération de données financieres 
│   │   ├── financial_calc.py     # Fonctions de calcul (rendement, volatilité, ratios)
│   │   └── visualization.py      # Fonctions de création des images
│   └── main.py              		  # Point d'entrée FastAPI
│                    
├── tests/
│   ├── unit/
│   │   └── test_calculations.py  # Tests des fonctions de financial_calc.py 
│   ├── integration/
│       └── test_api_endpoints.py # Tests des routes FastAPI 
│   
├── README.md  
├──.env.txt                 
├── requirements.txt             
└── .gitignore 
````
## Contribution
1. Fork le projet 
2. Crée une branche : `git checkout -b ma-branche`
3. Commit tes modifications : `git commit -m "Description"`
4. Push la branche : `git push origin ma-branche`
5. Ouvre une Pull Request

## Licence

Ce projet est sous licence **MIT**.  

Vous êtes libre de :  
- Utiliser, copier et modifier le code.  
- Distribuer votre version du projet.  
- Publier votre projet dérivé.  

Sous réserve que :  
- Vous incluiez le **copyright** et la **notice de licence** dans toutes les copies ou portions substantielles du projet.  

Pour plus d’informations, voir le fichier [LICENSE](LICENSE).
