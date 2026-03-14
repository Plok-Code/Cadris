# 03_launch_checklist

## Regle de decision

- si un item `Critique` echoue : pas de lancement ;
- si un item `Important` echoue : lancement seulement avec arbitrage explicite ;
- si un item `Differable` echoue : consigner la dette et lancer si le coeur reste sain.

## 1. Scope et release gate

- [ ] Critique - le scope de lancement est explicitement borne a la premiere tranche verticale `Demarrage`
- [ ] Critique - PDF, share links, File Search, uploads et flows secondaires sont soit hors scope, soit caches proprement
- [ ] Critique - aucun interdit du handoff final n'a ete viole en implementation
- [ ] Important - les hypotheses encore ouvertes sont visibles dans la doc de release

## 2. Verifications techniques

- [ ] Critique - lint, typecheck, validation Python et build passent
- [ ] Critique - schemas partages et clients associes sont coherents
- [ ] Critique - migrations initiales ont ete verifiees sur staging
- [ ] Critique - `staging` est l'environnement E2E de reference et est deploye
- [ ] Critique - le run `start -> waiting_user -> resume -> complete` fonctionne sur staging
- [ ] Critique - aucun doublon critique de run ou d'artefact n'apparait sur double soumission
- [ ] Critique - le dossier markdown est rendu depuis snapshot canonique
- [ ] Important - un scenario de rollback simple a ete repete ou documente
- [ ] Important - les logs d'erreur critiques sont retrouvables avec correlation utile

## 3. Verifications produit

- [ ] Critique - un utilisateur peut creer un projet puis une mission `Demarrage`
- [ ] Critique - une premiere synthese et une vraie question utile sont visibles
- [ ] Critique - une reponse utilisateur relance correctement la mission
- [ ] Critique - un premier artefact persiste est visible apres refresh
- [ ] Critique - la vue `Dossier` est lisible, stable et exploitable
- [ ] Important - les ecrans `Mes projets`, `Mission`, `Dossier` sont suffisants pour demontrer la valeur
- [ ] Differable - l'habillage visuel final logo / badges est acceptable meme s'il n'est pas totalement fige

## 4. Verifications securite et acces

- [ ] Critique - auth requise pour tout acces non partage
- [ ] Critique - autorisation serveur verifiee par projet / mission
- [ ] Critique - aucune route metier ne depend du seul etat client
- [ ] Critique - aucun secret n'est dans le repo ou dans les `.env.example`
- [ ] Important - les logs et traces n'embarquent pas le texte integral sensible par defaut
- [ ] Differable - la politique exacte des share links est documentee si cette surface reste hors scope

## 5. Verifications design et UX

- [ ] Critique - labels primaires d'etat coherents : `Solide`, `A confirmer`, `Inconnu`, `Bloquant`, `Pret a decider`
- [ ] Critique - statuts comprenables sans la couleur seule
- [ ] Important - une seule zone dominante par ecran est respectee
- [ ] Important - la mission room reste resserree, sans cockpit ni feed dominant
- [ ] Differable - lockup logo final non bloque pas le lancement si le symbole temporaire est assume

## 6. Verifications QA et staging

- [ ] Critique - smoke tests manuels P0 executes sur staging
- [ ] Critique - aucune anomalie bloquante ouverte sur auth, reprise, canonique, dossier
- [ ] Important - anomalies connues priorisees et documentees
- [ ] Important - un mini lot de tests live externes a ete execute si le budget le permet

## 7. Preconditions de lancement

- [ ] Critique - compte de test disponible
- [ ] Critique - jeu de donnees de demonstration minimum disponible
- [ ] Important - procedure de support de premiere ligne documentee
- [ ] Important - responsable de decision GO / NO GO identifie
- [ ] Important - canal de remontee d'anomalies ouvert

## Decision de travail

Cette checklist vaut pour un lancement limite de la premiere tranche verticale.
Si le lancement inclut PDF, share links, File Search ou flows secondaires, une checklist complementaire devient necessaire.
