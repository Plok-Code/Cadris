# 01_user_flows

## Vue d'ensemble

Cadris ne suit plus un parcours lineaire "questionnaire puis document".

Le produit suit une boucle plus proche d'une vraie entreprise :
1. intake du projet ;
2. qualification du contexte ;
3. activation d'une equipe d'agents ;
4. questions ciblees a l'utilisateur ;
5. discussion inter-agents visible ;
6. production et relecture des documents ;
7. consolidation en dossier d'execution.

Les trois contextes d'entree restent les memes, mais ils passent tous par cette meme machine operatoire.

---

## Flow 1 - Demarrage de projet

**Declencheur :** l'utilisateur arrive avec une idee, quelques notes ou rien de structure.
**Intention :** faire emerger le projet, structurer les domaines utiles et produire les premiers documents serieux.
**Resultat attendu :** un premier corpus coherent et un dossier d'execution exploitable.

### Etapes

```text
[E-01] Tableau de bord
  -> Clic "Nouvelle mission"
       |
[E-02] Intake libre
  -> L'utilisateur raconte son projet, depose des notes ou des liens
  -> Le systeme accepte l'information brute, meme incomplete
       |
[E-03] Qualification du contexte
  -> Le systeme confirme : "Demarrage de projet"
  -> Premier objectif de mission propose
       |
[E-04] Proposition d'equipe
  -> Le superviseur active les premiers agents utiles
  -> Exemple : Strategie, Produit, Business, Technique
  -> Les agents non prioritaires restent observateurs
       |
[E-05] Mission room
  -> L'utilisateur voit :
     - le feed de mission ;
     - les agents actifs ;
     - les documents cibles ;
     - les questions en attente ;
     - les points ouverts
       |
[E-06] Premiere vague d'analyse
  -> Les agents lisent l'intake
  -> Ils commentent entre eux
  -> Ils signalent les angles morts et dependances
  -> Le superviseur regroupe les vraies questions a poser a l'utilisateur
       |
[E-07] Premiere vague de questions utilisateur
  -> Questions courtes, groupees par impact
  -> Chaque question affiche le ou les domaines concernes
  -> L'utilisateur repond dans son langage
       |
[E-08] Synthese inter-agents
  -> Les agents integrent les reponses
  -> Un agent peut intervenir sur le sujet d'un autre
  -> Les contradictions sont rendues visibles
  -> Une premiere structure documentaire se stabilise
  -> JALON : "L'equipe a compris votre projet"
       |
[E-09] Production des premiers artefacts
  -> Les agents redigent les documents prioritaires
  -> Exemple : vision produit, problem statement, ICP, scope, PRD initial
       |
[E-10] Relecture croisee
  -> Les agents challengent les documents des autres
  -> Les points fragiles deviennent questions, reserves ou decisions
       |
[E-11] Arbitrages utilisateur
  -> Le systeme remonte seulement les noeuds structurants
  -> L'utilisateur tranche ou accepte une hypothese temporaire
       |
[E-12] Consolidation
  -> Les documents passent a un statut lisible
  -> Le dossier d'execution est assemble avec ses reserves
       |
[E-13] Export / partage
  -> Export markdown, PDF ou lien
       |
[E-14] Cloture ou poursuite
  -> Mission closee si le dossier est juge exploitable
  -> Ou mission laissee active pour approfondissement
```

**Valeur percue :**
- premier signal fort a E-08, quand plusieurs agents convergent sur une lecture utile du projet ;
- second signal fort a E-09, quand les premiers vrais documents apparaissent ;
- valeur maximale a E-12, quand le dossier d'execution devient partageable.

---

## Flow 2 - Projet a recadrer

**Declencheur :** le projet existe deja, mais les decisions sont dispersees, contradictoires ou mal documentees.
**Intention :** remettre le projet en coherence sans repartir de zero.
**Resultat attendu :** un corpus nettoye qui fait foi et une memoire des arbitrages.

### Etapes

```text
[E-01] Tableau de bord
  -> Clic "Nouvelle mission"
       |
[E-02] Intake de l'existant
  -> L'utilisateur depose docs, backlog, maquettes, notes, code ou liens
       |
[E-03] Qualification du contexte
  -> Le systeme confirme : "Projet a recadrer"
       |
[E-04] Proposition d'equipe
  -> Activation plus large des agents de revue
  -> Exemple : Strategie, Produit, UX/UI, Technique, Business
       |
[E-05] Mission room
  -> La room affiche :
     - ce qui existe deja ;
     - ce qui manque ;
     - les premieres tensions detectees
       |
[E-06] Lecture distribuee de l'existant
  -> Chaque agent lit selon son domaine
  -> Tous voient aussi les remarques des autres
  -> Les agents pointent incoherences, zones vides et decisions obsoletes
       |
[E-07] Premiere synthese de remise en coherence
  -> Le superviseur resume :
     - ce qui semble faire foi ;
     - ce qui se contredit ;
     - ce qui manque vraiment
  -> JALON : "Les incoherences du projet sont explicites"
       |
[E-08] Questions ciblees a l'utilisateur
  -> Les questions portent sur les noeuds de confusion reels
  -> Pas de re-questionnaire complet si l'information existe deja
       |
[E-09] Re-ecriture des artefacts
  -> Les agents reecrivent ou restructurent les docs impactes
       |
[E-10] Relecture croisee
  -> Verification de coherence inter-domaines
       |
[E-11] Arbitrages de normalisation
  -> L'utilisateur tranche les vraies contradictions
       |
[E-12] Dossier d'execution consolide
       |
[E-13] Export / partage
       |
[E-14] Cloture ou poursuite
```

**Valeur percue :**
- des E-07, quand l'utilisateur voit enfin pourquoi le projet etait devenu confus ;
- puis a E-09, quand les documents cibles cessent d'etre des fragments epars.

---

## Flow 3 - Refonte / pivot

**Declencheur :** un projet cadre existe deja, mais un changement majeur le reconfigure.
**Intention :** reouvrir seulement ce qui est reellement impacte, puis republier un dossier credible.
**Resultat attendu :** une revision tracee, avec documents mis a jour et impacts explicites.

### Etapes

```text
[E-01] Ouverture d'une mission de revision
  -> L'utilisateur selectionne un projet existant
       |
[E-02] Declaration du changement
  -> Nouvelle cible, nouveau canal, nouvelle contrainte, nouveau modele economique, etc.
       |
[E-03] Qualification du contexte
  -> Le systeme confirme : "Refonte / pivot"
       |
[E-04] Reactivation de l'equipe
  -> Les agents deja concernes sont recharges
  -> De nouveaux agents peuvent etre actives si le changement l'exige
       |
[E-05] Analyse d'impact
  -> Chaque agent indique ce que le changement touche
  -> Les dependances entre documents sont listees
  -> JALON : "Les impacts du pivot sont cartographies"
       |
[E-06] Arbitrages de cadrage
  -> Le superviseur pose les questions manquantes a l'utilisateur
       |
[E-07] Reouverture des artefacts impactes
  -> Les sections touchees passent en statut "a reviser"
       |
[E-08] Re-redaction et relecture croisee
  -> Les agents reecrivent
  -> Les autres challengent les effets de bord
       |
[E-09] Nouvelle consolidation
  -> Le dossier indique clairement ce qui a change et pourquoi
       |
[E-10] Export / partage
       |
[E-11] Cloture de revision
```

**Valeur percue :**
- a E-05, quand l'utilisateur comprend immediatement l'impact reel du pivot ;
- puis a E-09, quand un nouveau dossier coherent existe sans devoir tout refaire.

---

## Synthese des flows

| Flow | Declencheur | Premier jalon | Resultat |
|------|-------------|----------------|----------|
| Flow 1 - Demarrage | Idee ou projet peu formalise | "L'equipe a compris votre projet" | Premier corpus + dossier d'execution |
| Flow 2 - Projet a recadrer | Projet existant incoherent | "Les incoherences du projet sont explicites" | Corpus nettoye qui fait foi |
| Flow 3 - Refonte / pivot | Changement majeur sur projet existant | "Les impacts du pivot sont cartographies" | Corpus revise et dossier republie |
