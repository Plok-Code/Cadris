# 04_manual_test_plan

## Principe

Le plan manuel doit valider la boucle coeur avant toute extension.
Ordre recommande :
- happy path ;
- reprise ;
- robustesse ;
- autorisation ;
- lisibilite ;
- hors-scope explicite.

## Scenarios

### M-01 - Happy path `Demarrage` bout en bout

Etapes :
- se connecter ;
- creer un projet ;
- ouvrir une mission `Demarrage` ;
- saisir un intake libre texte ;
- lancer la mission ;
- attendre une synthese et une question ;
- repondre ;
- verifier la reprise ;
- ouvrir `Dossier`.

Resultat attendu :
- la mission passe par `waiting_user` puis reprend ;
- un premier artefact existe ;
- le dossier est lisible apres refresh.

Anomalies a noter :
- absence de question utile ;
- duplication ;
- dossier vide ;
- statut incoherent.

### M-02 - Refresh et reprise en `waiting_user`

Etapes :
- lancer une mission jusqu'a `waiting_user` ;
- recharger la page ;
- revenir sur la mission ;
- repondre apres le refresh.

Resultat attendu :
- la mission reste dans le bon etat ;
- aucune perte de contexte ;
- une seule reprise est creee.

Anomalies a noter :
- reset de mission ;
- question disparue ;
- double reprise.

### M-03 - Double soumission / idempotence

Etapes :
- soumettre rapidement deux fois la meme reponse utilisateur ;
- verifier l'etat de mission et les artefacts.

Resultat attendu :
- une seule reprise effective ;
- pas de doublon d'artefact critique ;
- message ou comportement coherent en cas de double clic.

Anomalies a noter :
- deux runs paralleles ;
- deux artefacts concurrents ;
- etat bloque sans message.

### M-04 - Acces non autorise

Etapes :
- tenter d'ouvrir un projet ou une mission via un identifiant externe ou un second compte ;
- tester un acces direct a une route metier si possible en staging.

Resultat attendu :
- refus explicite ;
- aucune fuite de contenu ;
- journalisation securite exploitable si prevue.

Anomalies a noter :
- ressource visible ;
- metadonnees exposees ;
- erreur 500 au lieu de 401/403.

### M-05 - Erreur de validation utilisateur

Etapes :
- tenter un intake vide ou trop pauvre selon les regles retenues ;
- tenter une reponse vide ou invalide.

Resultat attendu :
- erreur comprenable ;
- pas de run lance si l'entree est invalide ;
- pas de casse de l'ecran.

Anomalies a noter :
- erreur generique ;
- validation seulement cote client ;
- ecran bloque.

### M-06 - Dossier rendu depuis canonique

Etapes :
- produire un premier artefact ;
- ouvrir `Dossier` ;
- recharger ;
- rouvrir plus tard depuis `Mes projets`.

Resultat attendu :
- meme contenu rendu sans derive ;
- aucun indice que le markdown serait la source canonique ;
- structure stable.

Anomalies a noter :
- contenu different sans raison ;
- texte perdu ;
- dossier non retrouvable.

### M-07 - Etats, labels et lisibilite

Etapes :
- observer `Mes projets`, `Mission`, `Dossier` ;
- verifier les labels et badges principaux ;
- verifier un contexte dense ou petite largeur si disponible.

Resultat attendu :
- labels principaux coherents ;
- statuts lisibles sans couleur seule ;
- aucune reintroduction de labels principaux legacy.

Anomalies a noter :
- `Confirme` ou `Hypothese` en label principal ;
- badge trop pale ;
- label different pour un meme etat.

### M-08 - Redeploiement simple puis reprise

Etapes :
- mettre une mission en `waiting_user` ;
- redeployer ou simuler la reprise d'un service sur staging ;
- repondre ensuite.

Resultat attendu :
- la mission reprend ;
- pas de duplication ni de perte d'etat ;
- le dossier final reste lisible.

Anomalies a noter :
- mission orpheline ;
- reprise impossible ;
- etat incoherent apres restart.

### M-09 - Hors-scope visible et propre

Etapes :
- inspecter l'app et verifier l'absence ou la neutralisation propre de PDF, share links, File Search et uploads si hors scope.

Resultat attendu :
- aucune promesse active d'une surface non livree ;
- pas de bouton mort critique ;
- pas d'appel backend partiel vers une fonctionnalite non lancee.

Anomalies a noter :
- CTA visible mais non branche ;
- fonctionnalite semi-active ;
- confusion produit sur ce qui est lance.

## Ordre recommande d'execution

1. M-01
2. M-02
3. M-03
4. M-04
5. M-05
6. M-06
7. M-07
8. M-08
9. M-09

## Decision de travail

Si M-01 a M-04 echouent, le lancement doit etre bloque.
M-05 a M-09 servent a qualifier la robustesse minimale et la qualite percue avant mise en ligne.
