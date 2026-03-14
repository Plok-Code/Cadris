# 04_starter_prompt

## Prompt de depart complet

Tu travailles sur Cadris.

Contexte minimal :
- Cadris est un produit de missions documentaires multi-agents.
- La stack imposee est : Next.js 15 + React 19 + TypeScript pour `web`, FastAPI + Pydantic v2 pour `control-plane`, Python 3.13 + OpenAI Agents SDK + Restate pour `runtime`, et un `renderer` separe pour markdown / HTML / PDF.
- `PostgreSQL` est la verite metier canonique.
- `Restate` porte l'etat d'execution.
- `S3` porte le binaire.
- Le frontend ne parle jamais directement a Postgres, OpenAI, S3 ou Restate.
- Le markdown et le PDF sont des vues rendues, pas la source canonique.

Objectif initial :
construire la premiere tranche verticale utile du flow `Demarrage` en suivant l'ordre de build impose.

Premiere tranche verticale a viser :
- utilisateur authentifie
- creation d'un projet
- ouverture d'une mission `Demarrage`
- intake libre texte
- supervisor + 2 agents coeur
- premiere synthese
- une question utile
- reponse utilisateur
- reprise du run
- premier artefact canonique
- premier dossier markdown lisible

Ordre recommande :
1. verifier ou creer la structure `apps / packages / infra / scripts`
2. poser `packages/schemas` et la config partagee
3. poser le schema Postgres minimal et les migrations initiales
4. poser auth minimale et autorisation serveur
5. poser le `control-plane` minimal
6. poser le `runtime` minimal avec lifecycle `start -> waiting_user -> resume -> complete`
7. poser le `renderer` markdown minimal
8. poser le `web` minimal : `Mes projets`, `Mission`, `Dossier`
9. brancher la tranche verticale bout en bout

Regles a respecter explicitement :
- construire du canonique vers le rendu ;
- valider a chaque frontiere ;
- aucune sortie LLM canonique sans validation structuree ;
- toute commande relancable doit etre idempotente ;
- UI `mission-first`, sobre, lisible ;
- une seule zone dominante par ecran ;
- statuts verbaux et visibles ;
- palette semantique avec accent petrol rare ;
- `Public Sans + IBM Plex Mono` ;
- bordures avant ombres.

Interdits a repeter :
- pas de monolithe Next.js pour l'orchestration ;
- pas d'appel direct du web a Postgres, S3, Restate ou OpenAI ;
- pas de markdown comme verite canonique ;
- pas de PDF, share links ou File Search avant la premiere tranche verticale ;
- pas de mission room cockpit ;
- pas de second systeme d'etats ;
- pas de dependance speculative ;
- pas de build post-MVP avant stabilisation du MVP.

Compromis acceptables en V1 :
- symbole logo seul temporairement dans l'app ;
- mission room resserree sans feed dominant ;
- dossier markdown avant PDF ;
- `CertaintyPanel` compact plus tard ;
- roster d'agents simplifie.

Premier livrable attendu :
- un squelette de repo propre et bootstrappable ;
- les contrats partages initiaux ;
- le schema canonique minimal ;
- les services minimaux `web`, `control-plane`, `runtime`, `renderer` ;
- puis une premiere execution demonstrable du flow `Demarrage` resserre.

Format de travail attendu :
- commence par lire le repo et confirmer ce qui existe deja ;
- propose ensuite le plus petit prochain lot utile ;
- implemente ce lot ;
- verifie ce qui peut l'etre ;
- resume ce qui a ete fait, ce qui reste, et les hypotheses encore ouvertes.

## Decision de travail

Ce starter prompt doit lancer l'agent de code sur :
**la premiere tranche verticale utile, avec un ordre strict, peu d'ambiguite et des interdits explicites**.
