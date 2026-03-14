# 01_codex_handoff

## Contexte projet compact

Cadris est un produit de missions documentaires multi-agents.
Le coeur n'est ni un simple chat, ni un simple wizard, ni un simple generateur de PDF.

Le produit doit permettre :
- de creer une mission ;
- d'analyser un projet ;
- de poser une vraie question utile a l'utilisateur ;
- de reprendre la mission apres reponse ;
- de produire des artefacts documentaires canoniques ;
- de rendre un premier dossier lisible.

## Stack imposee

- `apps/web` : Next.js 15 + React 19 + TypeScript
- `apps/control-plane` : FastAPI + Pydantic v2
- `apps/runtime` : Python 3.13 + OpenAI Agents SDK + Restate
- `apps/renderer` : rendu markdown / HTML / PDF
- `PostgreSQL` : verite metier canonique
- `S3` : stockage binaire
- `OpenAI File Search` : retrieval V1, mais pas dans la premiere tranche verticale
- `SSE` : temps reel par defaut

Regles centrales :
- `PostgreSQL = verite metier`
- `Restate = execution`
- `Frontend = presentation et collecte`
- `Markdown/PDF = vues rendues, jamais source canonique`

## MVP a construire

Le MVP commence par une premiere tranche verticale resserree :
- utilisateur authentifie ;
- creation d'un projet ;
- ouverture d'une mission `Demarrage` ;
- intake libre texte ;
- supervisor + 2 agents coeur ;
- premiere synthese ;
- une question utile ;
- reponse utilisateur ;
- reprise ;
- premier artefact ;
- premier dossier markdown.

Ce qui vient ensuite seulement :
- uploads ;
- File Search ;
- PDF ;
- share links ;
- flow `Projet a recadrer` ;
- flow `Refonte / pivot` simplifie ;
- certitude detaillee ;
- export / partage complets.

## Ordre de build a respecter

1. Figer le bootstrap repo et les choix outillage minimaux.
2. Creer la structure `apps / packages / infra / scripts`.
3. Poser config, schemas partages et client SDK.
4. Poser primitives transverses : IDs, erreurs, statuts, mapping labels.
5. Poser schema canonique et migrations initiales.
6. Poser auth context et autorisation serveur minimale.
7. Poser control-plane minimal.
8. Poser runtime minimal et lifecycle `start -> waiting_user -> resume -> complete`.
9. Poser renderer markdown minimal depuis snapshot.
10. Poser web minimal : `Mes projets`, `Mission`, `Dossier`.
11. Construire la premiere tranche verticale.
12. Etendre au reste du MVP.
13. Stabiliser.

## Points encore hypothetiques

- toolchain exact du repo ;
- provider d'auth exact ;
- pile persistence exacte du control-plane ;
- lockup logo final ;
- calibration finale des badges de statut ;
- matrice documentaire MVP exacte.

## Decision de travail

L'agent de code doit partir d'un dossier compact mais ferme :
**stack imposee, MVP resserre, build en ordre strict, frontieres non negociables, et hypothese visibles la ou il reste du flou**.
