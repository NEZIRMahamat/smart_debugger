# Smart Debugger 🐛🤖

Un agent IA intelligent pour déboguer automatiquement du code Python buggué en utilisant l'API GROQ.

## Description

Smart Debugger est un outil qui utilise l'intelligence artificielle pour analyser et corriger automatiquement les erreurs dans du code Python. Il est structuré en trois composants principaux :

1. **Exécuteur de Code** (`executor.py`) - Exécute le code buggué et capture le code source ainsi que la trace d'erreur (traceback)
2. **Analyseur LLM** (`analyzer.py`) - Analyse le code source et la trace d'erreur en utilisant l'API GROQ
3. **Patcheur** (`patcher.py`) - Applique les corrections suggérées par le LLM

Le système principal (`main.py`) articule ces trois parties dans une boucle qui continue tant qu'il y a des erreurs, avec des garde-fous pour éviter les boucles infinies.

## Installation

### Prérequis

- Python 3.7 ou supérieur
- Une clé API GROQ (obtenir gratuitement sur [console.groq.com](https://console.groq.com/))

### Étapes d'installation

1. Cloner le dépôt :
```bash
git clone https://github.com/NEZIRMahamat/smart_debugger.git
cd smart_debugger
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer la clé API GROQ :
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API GROQ
```

Ou définir la variable d'environnement directement :
```bash
export GROQ_API_KEY="votre_clé_api_ici"
```

## Utilisation

### Utilisation en ligne de commande

Pour déboguer un fichier Python :

```bash
python -m smart_debugger.main examples/buggy_example1.py
```

Avec options :
```bash
python -m smart_debugger.main examples/buggy_example1.py \
  --api-key YOUR_API_KEY \
  --model llama-3.1-70b-versatile \
  --max-iterations 5
```

### Utilisation comme bibliothèque Python

```python
from smart_debugger import SmartDebugger

# Initialiser le débogueur
debugger = SmartDebugger(
    api_key="votre_clé_api",
    model="llama-3.1-70b-versatile",
    max_iterations=5
)

# Déboguer du code sous forme de chaîne
code = """
def calculate_sum(a, b)
    return a + b

print(calculate_sum(5, 10))
"""

success, fixed_code, history = debugger.debug_code(code, verbose=True)

if success:
    print("Code corrigé :")
    print(fixed_code)
else:
    print("Échec du débogage")

# Ou déboguer un fichier directement
success, fixed_code, history = debugger.debug_file("buggy_script.py", verbose=True)
```

## Exemples

Le dossier `examples/` contient plusieurs exemples de code buggué :

1. **buggy_example1.py** - Erreur de syntaxe (deux-points manquant)
2. **buggy_example2.py** - Erreur d'exécution (division par zéro)
3. **buggy_example3.py** - Erreur de type (concaténation string/int)

Testez-les avec :
```bash
python -m smart_debugger.main examples/buggy_example1.py
```

## Architecture

### Composants principaux

```
smart_debugger/
├── executor.py    # Exécute le code et capture les erreurs
├── analyzer.py    # Analyse les erreurs avec l'API GROQ
├── patcher.py     # Applique les corrections
├── main.py        # Orchestrateur principal
└── __init__.py    # Initialisation du package
```

### Flux de travail

```
1. Exécution → 2. Analyse LLM → 3. Application du patch → 4. Ré-exécution
                        ↑                                        ↓
                        └────────── Boucle si erreur ────────────┘
                        (max 5 itérations par défaut)
```

## Options de configuration

- `--api-key` : Clé API GROQ (ou variable d'environnement `GROQ_API_KEY`)
- `--model` : Modèle GROQ à utiliser (défaut: `llama-3.1-70b-versatile`)
- `--max-iterations` : Nombre maximum d'itérations de débogage (défaut: 5)
- `--quiet` : Supprime la sortie de progression

## Prévention des boucles infinies

Le système inclut plusieurs mécanismes de sécurité :
- Limite du nombre d'itérations (`max_iterations`)
- Historique des tentatives de correction
- Détection automatique de succès d'exécution

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Ce projet est sous licence MIT.

## Auteur

NEZIR Mahamat