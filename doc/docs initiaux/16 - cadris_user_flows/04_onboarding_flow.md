# 04_onboarding_flow

## Necessite d'un onboarding

**Verdict : Oui - onboarding necessaire, court, concret et centre sur le mode operatoire multi-agents.**

Le risque principal n'est plus seulement que l'utilisateur ne comprenne pas le mot "cadrage".
Le risque principal est qu'il ne comprenne pas comment fonctionne Cadris :
- plusieurs agents specialises ;
- tous branches sur la meme mission ;
- capables de se parler, se contester et se relire ;
- l'utilisateur n'intervient que pour les vraies decisions.

L'onboarding doit donc rendre evidente la mecanique du produit en moins de 2 minutes.

---

## Flow d'onboarding recommande

**Declencheur :** premier acces au produit.

```text
[Etape 1 - Promesse claire]
  Ecran unique, tres court :
  "Vous arrivez avec une idee ou un projet flou."
  "Cadris active une equipe d'agents specialises qui travaillent ensemble sur votre projet."
  "Ils vous posent seulement les questions qui comptent, puis produisent vos documents."
  Bouton : "Lancer ma mission"
       |
[Etape 2 - Comment ca marche]
  Mini schema ou 3 cartes :
  1. Vous donnez le contexte
  2. Les agents analysent, debattent et vous sollicitent si besoin
  3. Cadris assemble les docs et le dossier d'execution
  Bouton : "Voir un exemple" ou "Passer"
       |
[Etape 3 - Exemple de mission room]
  Apercu tres court d'une mission :
  - agents actifs ;
  - une question utile a l'utilisateur ;
  - une intervention croisee ;
  - un document en cours
  Message : "Vous ne faites pas les documents vous-meme. Vous arbitrez, l'equipe produit."
       |
[Etape 4 - Entree directe en mission]
  Redirection vers intake / qualification
```

**Duree totale cible :** 60 a 120 secondes.

---

## Premier succes utilisateur

**Definition :** premier moment ou l'utilisateur constate que son projet est pris en charge comme par une equipe competente, et pas seulement range dans un formulaire.

**Premier succes vise :**
le moment ou, apres l'intake initial, le systeme affiche :
- les agents actifs ;
- leur premiere lecture du projet ;
- une synthese du superviseur ;
- une premiere structure documentaire credible.

Ce succes arrive avant le dossier final.

**Signal a afficher a ce moment :**
> "Votre mission est maintenant prise en charge par l'equipe."
> "Les premiers domaines actifs et les premiers documents cibles sont en place."

---

## Onboarding pour utilisateurs de retour

Un utilisateur qui revient n'a pas besoin du meme onboarding.

Il faut lui montrer directement :
- ce qui a bouge pendant son absence ;
- quels agents attendent une decision ;
- quels documents ont avance ;
- quelle est la prochaine action utile.

La reprise doit ressembler a une equipe qui lui rend l'etat du dossier, pas a un nouveau tutorial.

---

## Risques de friction dans l'onboarding

### RF-01 - Onboarding trop conceptuel
Si l'onboarding explique l'idee des agents sans montrer une mission concrete, l'utilisateur n'ancre pas la valeur.

**Regle :** montrer un exemple de mission room, pas une theorie abstraite.

### RF-02 - Onboarding trop long
Si l'utilisateur doit parcourir 5 ecrans avant de raconter son projet, la promesse perd sa force.

**Regle :** maximum 3 ecrans courts avant l'action.

### RF-03 - Theatre multi-agents mal compris
Si l'utilisateur croit que les agents sont juste des noms decoratifs, la confiance chute.

**Regle :** montrer au moins une intervention croisee concrete entre agents.

### RF-04 - L'utilisateur pense qu'il doit lui-meme produire les docs
Si l'exemple ressemble a une checklist de travail pour lui, il peut se sentir ecrase.

**Regle :** dire explicitement que l'utilisateur arbitre et que l'equipe produit les artefacts.

### RF-05 - Premier succes trop tardif
Si le premier vrai effet visible n'arrive qu'au premier dossier complet, l'utilisateur peut decrocher.

**Regle :** faire apparaitre une premiere synthese multi-agents et un premier plan documentaire tres tot.

---

## Ce que l'onboarding ne doit pas faire

- presenter Cadris comme un simple chatbot ;
- faire croire que tous les agents parlent en meme temps sans coordination ;
- expliquer toute la taxonomie documentaire avant la premiere mission ;
- demander une configuration longue avant l'intake ;
- cacher le fait que certaines decisions devront etre arbitrees par l'utilisateur.
