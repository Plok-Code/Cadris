# 07_handoff_to_gpt_14

## Resume executif
Le PRD a ete recadre pour coller au vrai produit :
- Cadris n'est pas un simple service de reformulation ;
- Cadris est un systeme multi-agents specialise organise comme une petite entreprise autour du projet ;
- les agents partagent une memoire commune, voient les echanges utiles des autres et peuvent intervenir de maniere croisee ;
- l'utilisateur est sollicite au bon moment pour les arbitrages structurants ;
- la sortie attendue est un corpus documentaire coherent consolide en dossier d'execution.

## Perimetre produit detaille
Le produit doit aider un porteur de projet numerique a :
- faire travailler plusieurs domaines ensemble sur son projet ;
- transformer des infos partielles en documents utilisables ;
- rendre visibles les hypotheses, inconnus, contradictions, risques et decisions ;
- repartir avec un dossier d'execution exploitable par une equipe humaine ou agentique.

Le coeur du perimetre n'est plus "3 blocs guides", mais :
- une mission ;
- une equipe d'agents ;
- une memoire partagee ;
- des questions a l'utilisateur ;
- des artefacts documentaires ;
- une consolidation finale.

## Flux principaux
### Flux 1 - Demarrage
Intake utilisateur -> qualification -> activation des premiers agents -> questions de cadrage par domaines -> debats inter-agents -> arbitrages utilisateur -> production documentaire -> dossier consolide.

### Flux 2 - Projet deja flou
Collecte de l'existant -> lecture multi-domaines -> detection des tensions -> arbitrages cibles -> re-ecriture des artefacts -> dossier consolide.

### Flux 3 - Refonte / pivot
Changement declare -> analyse des impacts par agents -> reouverture des documents touches -> nouvelles questions utiles -> nouveau dossier d'execution.

## Exigences fonctionnelles
- qualifier le contexte et ouvrir une mission ;
- activer des agents par domaine ;
- maintenir une memoire partagee ;
- permettre les interventions croisees entre agents ;
- poser des questions utilisateur reliees aux bons domaines ;
- tracer arbitrages, hypotheses, inconnus et blocages ;
- produire des artefacts documentaires par domaine ;
- permettre la relecture croisee ;
- reprendre et reviser les missions ;
- consolider le dossier d'execution ;
- rendre les contributions tracables.

## Exigences non fonctionnelles
- lisibilite de la cooperation inter-agents ;
- coherence inter-domaines ;
- auditabilite des decisions ;
- reprise fiable d'une mission longue ;
- qualite documentaire exploitable ;
- separation nette entre traces de travail et source de verite canonique.

## Questions ouvertes
- matrice exacte des documents obligatoires par type de mission ;
- doctrine de visibilite des echanges inter-agents ;
- roster final des agents coeur du MVP ;
- seuil de qualite minimal par livrable ;
- modele economique le plus adapte a la valeur fournie.

## Points confirmes
- systeme multi-agents ;
- memoire partagee ;
- interventions croisees ;
- arbitrages utilisateur cibles ;
- corpus documentaire large ;
- dossier d'execution final.

## Hypotheses de travail
- un superviseur coordonne les sollicitations utilisateur ;
- la valeur percue nait tot quand l'utilisateur voit une vraie coordination multi-domaines ;
- le produit peut couvrir l'ensemble des familles de docs, avec profondeur ajustee au contexte.

## Inconnus
- profondeur minimale obligatoire par famille documentaire ;
- exposition optimale du feed inter-agents ;
- regles de validation finales des documents les plus sensibles.

## Bloquants
- aucun bloquant pour transmettre ;
- blocage futur si la matrice de couverture documentaire et la doctrine de visibilite ne sont pas tranchees.

## Niveau de fiabilite
**Bon sous hypotheses**

Le PRD est maintenant coherent avec la vision multi-agents et peut servir de base saine a l'UX et au modele de domaine.

## Ce que GPT 14 doit verifier en priorite
1. Comment rendre visible l'entreprise d'agents sans noyer l'utilisateur.
2. Quel est le premier moment de valeur le plus fort dans ce nouveau modele.
3. Comment doser les questions utilisateur pour qu'elles restent precises et peu redondantes.
4. Quelle representation de mission, d'agents et de documents rend le produit intelligible des la premiere session.
