# 07_handoff_to_gpt_17

## Resume executif

Les user flows ont ete recadres pour le vrai produit.

Cadris n'est plus modele comme un dialogue guide lineaire.
Le produit est maintenant decrit comme :
- une mission ;
- une mission room partagee ;
- une equipe d'agents specialises ;
- un superviseur qui orchestre ;
- des questions utilisateur ciblees ;
- des artefacts documentaires produits, relus puis consolides.

**Transmission autorisee : Oui.**

---

## Flows principaux

### Flow 1 - Demarrage de projet
Intake libre -> qualification -> proposition d'equipe -> premiere analyse inter-agents -> questions ciblees -> synthese -> production des premiers artefacts -> relecture -> arbitrages -> dossier -> export.

### Flow 2 - Projet a recadrer
Collecte de l'existant -> qualification -> lecture distribuee -> synthese des incoherences -> questions utiles -> re-ecriture des artefacts -> dossier consolide.

### Flow 3 - Refonte / pivot
Declaration du changement -> cartographie d'impact -> reouverture des artefacts touches -> nouvelles questions -> re-redaction -> nouveau dossier.

---

## Critical paths

| # | Chemin | Risque principal |
|---|--------|-----------------|
| CP-01 | Qualification + equipe initiale | Mauvais agents = mauvaise mission |
| CP-02 | Premiere cooperation visible | Promesse multi-agent non credible |
| CP-03 | Escalade utilisateur | Trop de questions ou mauvaises questions |
| CP-04 | Resolution des conflits inter-domaines | Faux alignement documentaire |
| CP-05 | Convergence vers dossier | Restitution trop proche d'un transcript |
| CP-06 | Reprise de mission longue | Perte de contexte et d'elan |

---

## Edge cases couverts

| # | Cas | Type |
|---|-----|------|
| EC-01 | Aucun materiau au depart | Utilisabilite |
| EC-02 | Questions redondantes | Experience |
| EC-03 | Intervention tardive d'un observateur | Coherence |
| EC-04 | Impossible d'arbitrer | Qualite |
| EC-05 | Desaccord fort entre agents | Coherence |
| EC-06 | Feed trop dense | Lisibilite |
| EC-07 | Hypothese cachee | Fiabilite |
| EC-08 | Pivot en cours de mission | Perimetre |
| EC-09 | Export partiel | Transmission |
| EC-10 | Decision corrigee apres propagation | Tracabilite |

---

## Onboarding retenu

**Oui - onboarding minimal obligatoire.**

Structure :
1. promesse claire ;
2. explication courte du mode multi-agents ;
3. apercu de mission room ;
4. entree immediate en mission.

**Premier succes cible :**
la premiere convergence multi-agents visible et utile, avant meme le dossier complet.

---

## Points confirmes

- La mission room est l'ecran central, pas un wizard classique.
- Les agents doivent voir la meme mission et pouvoir intervenir de facon croisee.
- L'utilisateur doit recevoir des vagues de questions ciblees, pas des questions dispersees.
- Les conflits et reserves doivent etre visibles avant le dossier final.
- La sortie finale est un dossier consolide a partir d'artefacts documentaires.

---

## Hypotheses de travail

- Le feed inter-agents visible augmente la confiance s'il reste bien filtre.
- Le superviseur doit jouer un role d'orchestrateur fort dans les sollicitations utilisateur.
- Le premier moment de valeur peut arriver avant le premier document complet.

---

## Inconnus

- niveau de detail exact du feed visible ;
- forme ideale de l'inbox d'arbitrages ;
- wording final du premier jalon.

---

## Niveau de fiabilite

**Bon**

Les parcours sont maintenant coherents avec le PRD recadre et avec la vision d'une entreprise d'agents produisant des documents, pas juste un chat guide.

---

## Ce que GPT 17 doit auditer en priorite

1. Comment rendre le feed inter-agents comprehensible sans perdre sa richesse.
2. Comment regrouper intelligemment les arbitrages utilisateur.
3. Quel est le meilleur premier jalon visible.
4. Comment representer l'etat des artefacts, reserves et blocages dans la mission room.
