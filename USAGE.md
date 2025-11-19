# Guide d'Utilisation - Smart Debugger

## Introduction

Smart Debugger est un outil intelligent qui utilise l'IA (via l'API GROQ) pour déboguer automatiquement votre code Python. Ce guide vous montre comment l'utiliser efficacement.

## Installation

### Installation depuis le dépôt

```bash
git clone https://github.com/NEZIRMahamat/smart_debugger.git
cd smart_debugger
pip install -r requirements.txt
```

### Installation en mode développement

```bash
pip install -e .
```

Après installation, vous pouvez utiliser la commande `smart-debugger` directement.

## Configuration

### Obtenir une clé API GROQ

1. Allez sur [console.groq.com](https://console.groq.com/)
2. Créez un compte gratuit
3. Générez une clé API
4. Conservez cette clé en sécurité

### Configurer la clé API

**Option 1: Variable d'environnement (recommandé)**
```bash
export GROQ_API_KEY="votre_clé_api_ici"
```

**Option 2: Fichier .env**
```bash
cp .env.example .env
# Éditez .env et ajoutez votre clé
```

**Option 3: Passer la clé en ligne de commande**
```bash
python -m smart_debugger.main --api-key "votre_clé" fichier.py
```

## Utilisation

### Utilisation en ligne de commande

#### Déboguer un fichier Python

```bash
python -m smart_debugger.main examples/buggy_example1.py
```

ou si installé:

```bash
smart-debugger examples/buggy_example1.py
```

#### Options avancées

```bash
# Utiliser un modèle spécifique
python -m smart_debugger.main --model llama-3.1-8b-instant fichier.py

# Limiter le nombre d'itérations
python -m smart_debugger.main --max-iterations 3 fichier.py

# Mode silencieux (moins de sortie)
python -m smart_debugger.main --quiet fichier.py

# Combiner plusieurs options
python -m smart_debugger.main \
  --api-key "votre_clé" \
  --model llama-3.1-70b-versatile \
  --max-iterations 5 \
  fichier.py
```

### Utilisation comme bibliothèque Python

#### Exemple basique

```python
from smart_debugger import SmartDebugger

# Initialiser le débogueur
debugger = SmartDebugger(api_key="votre_clé_api")

# Déboguer un fichier
success, fixed_code, history = debugger.debug_file("script_buggé.py")

if success:
    print("✓ Code corrigé avec succès!")
    print(fixed_code)
else:
    print("✗ Impossible de corriger le code")
```

#### Exemple avancé

```python
from smart_debugger import SmartDebugger

# Configuration personnalisée
debugger = SmartDebugger(
    api_key="votre_clé_api",
    model="llama-3.1-70b-versatile",  # Modèle plus puissant
    max_iterations=10  # Plus d'itérations
)

# Déboguer du code sous forme de chaîne
code_buggé = """
def calculer(x, y)
    return x + y

print(calculer(5, 3))
"""

success, code_corrigé, historique = debugger.debug_code(
    code_buggé,
    filepath="mon_script.py",  # Optionnel: pour de meilleurs messages d'erreur
    verbose=True  # Afficher les détails
)

# Examiner l'historique
print(f"\nNombre d'itérations: {len(historique)}")
for iteration in historique:
    print(f"Itération {iteration['iteration']}: {iteration['status']}")
```

#### Utilisation des composants individuels

```python
from smart_debugger import CodeExecutor, LLMAnalyzer, Patcher

# 1. Exécuter du code
executor = CodeExecutor()
success, stdout, error = executor.execute("print('Hello')")

# 2. Analyser une erreur
analyzer = LLMAnalyzer(api_key="votre_clé")
code_corrigé = analyzer.analyze_error(code_buggé, traceback)

# 3. Appliquer un patch
patcher = Patcher()
patcher.apply_patch(code_original, code_corrigé, "fichier.py")
```

## Exemples d'utilisation

### Exemple 1: Déboguer une erreur de syntaxe

```bash
# Fichier: erreur_syntaxe.py
def saluer(nom)  # Oups! Deux-points manquants
    print(f"Bonjour {nom}")

saluer("Alice")
```

```bash
python -m smart_debugger.main erreur_syntaxe.py
```

Smart Debugger détectera l'erreur de syntaxe et ajoutera automatiquement les deux-points manquants.

### Exemple 2: Déboguer une erreur d'exécution

```bash
# Fichier: division_zero.py
def diviser(a, b):
    return a / b

print(diviser(10, 0))  # Division par zéro!
```

```bash
python -m smart_debugger.main division_zero.py
```

Smart Debugger ajoutera une vérification pour éviter la division par zéro.

### Exemple 3: Déboguer une erreur de type

```bash
# Fichier: type_error.py
age = 25
message = "J'ai " + age + " ans"  # Impossible de concaténer str et int
print(message)
```

```bash
python -m smart_debugger.main type_error.py
```

Smart Debugger convertira `age` en chaîne avec `str()`.

## Fonctionnalités

### Sauvegardes automatiques

Smart Debugger crée automatiquement une sauvegarde avant de modifier votre fichier:
- Fichier original: `script.py`
- Sauvegarde: `script.py.backup`

Pour restaurer manuellement:
```python
from smart_debugger import Patcher
patcher = Patcher()
patcher.restore_backup("script.py")
```

### Protection contre les boucles infinies

Smart Debugger limite le nombre d'itérations (5 par défaut) pour éviter les boucles infinies si l'IA ne peut pas résoudre le problème.

### Historique des corrections

Chaque session de débogage conserve un historique:

```python
success, code, history = debugger.debug_file("fichier.py")

for iteration in history:
    print(f"Itération {iteration['iteration']}:")
    print(f"  Status: {iteration['status']}")
    if 'error' in iteration:
        print(f"  Erreur: {iteration['error'][:100]}...")
```

## Dépannage

### "GROQ API key not provided"

Assurez-vous d'avoir configuré votre clé API:
```bash
export GROQ_API_KEY="votre_clé"
```

### "ModuleNotFoundError: No module named 'groq'"

Installez les dépendances:
```bash
pip install -r requirements.txt
```

### Le code n'est pas corrigé après 5 itérations

Essayez d'augmenter le nombre d'itérations:
```bash
python -m smart_debugger.main --max-iterations 10 fichier.py
```

Ou utilisez un modèle plus puissant:
```bash
python -m smart_debugger.main --model llama-3.1-70b-versatile fichier.py
```

### Problèmes de quota API

GROQ offre un quota gratuit limité. Si vous dépassez le quota:
- Attendez la réinitialisation du quota
- Ou passez à un plan payant sur [console.groq.com](https://console.groq.com/)

## Bonnes Pratiques

1. **Commencez avec des fichiers simples**: Testez d'abord avec de petits scripts
2. **Vérifiez les corrections**: Examinez toujours le code corrigé avant de l'utiliser
3. **Conservez les sauvegardes**: Smart Debugger crée des sauvegardes, mais faites aussi vos propres backups
4. **Utilisez le verbose mode**: Pour comprendre ce que fait l'outil
5. **Limitez les itérations**: Évitez de consommer trop de quota API

## Modèles GROQ disponibles

- `llama-3.1-8b-instant` - Rapide et léger
- `llama-3.1-70b-versatile` - Plus puissant (recommandé)
- `mixtral-8x7b-32768` - Bon équilibre
- Consultez [console.groq.com](https://console.groq.com/) pour les modèles disponibles

## Support

- **Issues**: [github.com/NEZIRMahamat/smart_debugger/issues](https://github.com/NEZIRMahamat/smart_debugger/issues)
- **Documentation**: README.md et CONTRIBUTING.md
- **Exemples**: Dossier `examples/`
