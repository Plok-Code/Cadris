# 02_critical_paths

## Parcours critiques

Les parcours critiques sont ceux qui conditionnent la promesse centrale de Cadris :
faire sentir a l'utilisateur qu'une vraie equipe competente travaille sur son projet, sans perdre la lisibilite ni la rigueur documentaire.

---

## CP-01 - Qualification correcte du contexte et de l'equipe initiale

**Pourquoi c'est critique :**
Une mauvaise qualification active les mauvais agents trop tot, pose les mauvaises questions et deforme tout le reste de la mission.

**Chemin nominal :**
```text
Intake utilisateur
  -> Qualification du contexte
  -> Proposition de mission
  -> Proposition d'equipe initiale
  -> Validation implicite ou explicite par l'utilisateur
```

**Points de decision :**
- le contexte est correctement qualifie -> l'equipe initiale est pertinente ;
- le contexte est conteste -> le superviseur ajuste la mission et l'equipe.

**Risques d'abandon :**
- trop de questions de qualification avant de voir les agents agir ;
- une equipe proposee absurde ou trop large ;
- une qualification opaque que l'utilisateur ne comprend pas.

**Regle :** la qualification doit etre courte et produire un effet concret immediat : quels agents entrent en scene et pourquoi.

---

## CP-02 - Premiere demonstration de cooperation inter-agents

**Pourquoi c'est critique :**
Le produit vend une organisation d'agents, pas un formulaire de plus. Si l'utilisateur ne voit pas rapidement une cooperation credible entre specialites, la promesse s'effondre.

**Chemin nominal :**
```text
Agents actives
  -> Lecture de l'intake
  -> Premiers commentaires croises
  -> Regroupement des angles morts
  -> Premiere synthese du superviseur
  -> Jalon visible
```

**Points de decision :**
- les agents convergent utilement -> confiance qui monte ;
- les agents paraissent repetitifs ou decoratifs -> perte de confiance immediate.

**Risques d'abandon :**
- feed trop bavard ;
- interventions trop generiques ;
- aucun lien visible entre ce que disent les agents et les documents qui vont etre produits.

**Regle :** avant meme le premier dossier complet, l'utilisateur doit voir une intelligence collective credible et orientee resultat.

---

## CP-03 - Escalade utilisateur au bon moment

**Pourquoi c'est critique :**
Si les agents posent trop de questions, l'experience ressemble a un interrogatoire. S'ils n'en posent pas assez, les documents deviennent speculatifs.

**Chemin nominal :**
```text
Agents detectent un manque de certitude
  -> Le superviseur fusionne les besoins
  -> Une question claire est envoyee a l'utilisateur
  -> L'utilisateur repond
  -> La reponse est distribuee aux domaines impactes
```

**Points de decision :**
- l'utilisateur peut arbitrer -> la mission avance ;
- l'utilisateur ne sait pas -> une hypothese temporaire est creee et visible.

**Risques d'abandon :**
- plusieurs agents posent des variantes de la meme question ;
- question sans contexte ni impact visible ;
- l'utilisateur repond mais ne voit pas l'effet de sa reponse.

**Regle :** chaque escalade doit expliquer pourquoi elle existe et quels artefacts elle debloque.

---

## CP-04 - Resolution d'un conflit inter-domaines

**Pourquoi c'est critique :**
La valeur du produit est dans la coherence entre domaines. Si les conflits restent implicites ou mal geres, le systeme ne vaut pas mieux que des documents produits en silo.

**Chemin nominal :**
```text
Un agent detecte un conflit
  -> Le conflit devient un issue explicite
  -> Les agents concernes debattent
  -> Le superviseur resume l'impact
  -> Arbitrage utilisateur ou hypothese documentee
  -> Documents touches mis a jour
```

**Risques d'abandon :**
- conflit remonte trop tard ;
- arbitrage demande sans contexte ;
- conflit "resolu" sans trace dans les documents.

**Regle :** un conflit ne peut pas disparaitre sans laisser soit une decision, soit une reserve, soit un blocage visible.

---

## CP-05 - Convergence des artefacts vers un dossier

**Pourquoi c'est critique :**
Si le produit reste au stade du flux de conversation, il ne livre pas la valeur finale. Il faut convertir le travail agentique en artefacts puis en dossier d'execution.

**Chemin nominal :**
```text
Documents prioritaires produits
  -> Relecture croisee
  -> Statut des artefacts stabilise
  -> Dossier assemble
  -> Export / partage
```

**Points de decision :**
- les artefacts requis sont suffisants -> dossier exploitable ;
- certains artefacts restent fragiles -> dossier exportable avec reserves ;
- des blocages majeurs restent ouverts -> pas de cloture serieuse.

**Risques d'abandon :**
- pas de frontiere claire entre brouillon, document solide et dossier final ;
- export qui ressemble a un simple transcript ;
- impossibilite de savoir quoi partager ou non.

**Regle :** le dossier doit etre une vue consolidee des artefacts, decisions et reserves, pas un dump de messages.

---

## CP-06 - Reprise asynchrone d'une mission longue

**Pourquoi c'est critique :**
Le produit repose sur des missions potentiellement longues, avec attente utilisateur, lectures de documents et revisions. Si la reprise est confuse, tout le systeme perd son interet.

**Chemin nominal :**
```text
Mission en pause
  -> Reprise plus tard
  -> La room affiche :
     - dernier etat utile ;
     - questions encore ouvertes ;
     - documents en attente ;
     - prochains pas recommandes
```

**Risques d'abandon :**
- l'utilisateur ne comprend pas ce qui s'est passe pendant son absence ;
- les agents perdent le contexte ;
- les questions deja traitees reapparaissent.

**Regle :** une mission reprise doit se comporter comme une equipe qui reprend un dossier vivant, pas comme une session effacee.

---

## Dependances critiques entre les chemins

```text
CP-01 (qualification)
  -> conditionne CP-02 (cooperation credible)
  -> conditionne CP-03 (bonnes questions a l'utilisateur)

CP-02 (cooperation visible)
  -> conditionne CP-04 (gestion des conflits)
  -> conditionne CP-05 (confiance dans les artefacts produits)

CP-03 (escalades)
  -> conditionne CP-04 (resolution des tensions)
  -> conditionne CP-05 (qualite finale des documents)

CP-06 (reprise)
  -> soutient tous les autres chemins sur mission longue
```

**Regle generale :** aucun critical path ne doit laisser l'utilisateur face a une activite agentique opaque, ni face a une charge de questions non priorisee.
