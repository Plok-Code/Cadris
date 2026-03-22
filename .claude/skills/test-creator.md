---
name: test-creator
description: Creer des tests pour le code modifie. Tests unitaires + integration. Pas de flaky tests.
---

# Test Creator

## Regles anti-flaky
- JAMAIS de `time.sleep()` dans les tests.
- JAMAIS de dependance a l'ordre d'execution.
- JAMAIS de test qui depend d'un etat global mutable.
- Chaque test cree ses propres fixtures et nettoie apres.
- Utiliser des mocks pour les appels externes (runtime, renderer, Stripe, Resend).

## Backend (pytest)
1. Identifier les fonctions/endpoints modifies
2. Pour chaque endpoint : test happy path + test erreur + test auth
3. Fichier de test : `tests/test_{module}.py`
4. Utiliser les fixtures de `conftest.py` (client, auth_headers, mock_runtime)
5. Assertions precises : status code + body content

## Frontend (vitest/jest si configure)
1. Tests de composants : render + interactions
2. Tests de hooks : mock des API calls
3. Tests d'integration : flow complet

## Process
1. `git diff --name-only HEAD~1` pour lister les fichiers modifies
2. Identifier les fonctions publiques sans test
3. Generer les tests
4. Lancer : `python -m pytest apps/control-plane/tests/ apps/runtime/tests/ -q`
5. Verifier 100% pass

## Output
Fichiers de test crees, nombre de tests ajoutes, resultat d'execution.
