# 07_handoff_to_gpt_37

## Resume executif

La strategie QA retenue pour Cadris est volontairement compacte et priorisee.
Elle valide d'abord la premiere tranche verticale `Demarrage`, pas un MVP large.

Le coeur a prouver avant lancement est :
- auth minimale ;
- projet ;
- mission ;
- `waiting_user` ;
- reprise ;
- artefact canonique ;
- dossier markdown lisible.

## Criteres d'acceptation

Les gates critiques sont :
- creation de projet et ouverture de mission `Demarrage` ;
- question utile et passage en `waiting_user` ;
- reprise sans duplication ;
- premier artefact persiste dans le canonique ;
- dossier rendu depuis snapshot ;
- autorisation serveur correcte ;
- statuts primaires coherents et lisibles.

## Strategie de test

Priorites :
- P0 : auth, reprise, canonique, dossier, autorisation, statuts ;
- P1 : redeploiement + reprise, contrats, migrations, fallback ;
- P2 : PDF, share links, File Search, uploads, flows secondaires quand ils entrent en scope.

Types de verification utiles :
- checks statiques ;
- unitaires cibles ;
- contractuels ;
- integrations sur les frontieres ;
- smoke E2E sur `staging` ;
- quelques tests live limites.

## Checklist de lancement

Le lancement doit verifier au minimum :
- scope borne au coeur `Demarrage` ;
- staging E2E disponible ;
- run `start -> waiting_user -> resume -> complete` valide ;
- dossier markdown stable ;
- auth et autorisation server-side ;
- interdits du handoff respectes ;
- anomalies critiques closes ou arbitrees.

## Plan de test manuel

Ordre recommande :
1. happy path `Demarrage`
2. refresh / reprise
3. double soumission et idempotence
4. acces non autorise
5. validation utilisateur invalide
6. dossier rendu depuis canonique
7. lisibilite et coherence des statuts
8. redeploiement puis reprise
9. verification du hors-scope

## Points confirmes

- le lancement cible la boucle coeur, pas le produit complet ;
- `staging` est la reference E2E ;
- les regressions les plus graves concernent auth, autorisation, reprise, canonique et dossier ;
- les interdits techniques doivent devenir des non-regressions QA ;
- les surfaces hors scope ne doivent pas polluer la gate de lancement.

## Hypotheses de travail

- lancement borne a `Demarrage` resserre ;
- auth V1 simple ;
- tests live limites sur staging ;
- finition visuelle suffisante sans exiger tout le packaging final.

## Inconnus

- toolchain exact et runner CI final ;
- provider d'auth et contrat de session ;
- niveau exact de live testing OpenAI ;
- niveau de finition visuelle obligatoire au launch.

## Bloquants

- aucun bloquant strict pour la transmission ;
- ces inconnus deviennent surtout bloquants au moment du GO / NO GO final.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : la strategie s'appuie sur le handoff final, les attentes de test existantes, la tranche verticale retenue et les contraintes de securite / ops deja converges.

## Ce que le GPT 37 doit utiliser pour preparer le lancement

1. Transformer la checklist en gate GO / NO GO concret.
2. Reprendre les scenarios manuels dans un ordre d'execution realiste.
3. Rendre explicites les prerequis `staging`, comptes de test et donnees de demo.
4. Garder PDF, share links, File Search et flows secondaires hors gate tant qu'ils ne sont pas officiellement dans le scope.
5. Traiter auth, autorisation, reprise et dossier comme surfaces de validation prioritaires absolues.
