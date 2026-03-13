# 06_blocking_questions

## Questions bloquantes restantes - Choix de stack

## Questions bloquantes

### Aucune question bloquante pour lancer l'architecture detaillee

La stack cible est maintenant suffisamment claire pour passer a la phase suivante.

---

## Points a arbitrer pendant la conception detaillee

Ces points ne remettent pas en cause la stack retenue.
Ils conditionnent la facon exacte de l'implementer.

### PT-01 - Grain exact des agents

Combien d'agents specialises cree-t-on vraiment en V1 ?

Options plausibles :
- `Supervisor + Strategy + Product + Requirements + BuildReview`
- ou une decomposition plus fine par document.

**Recommandation :**
commencer avec peu d'agents tres nets, pas une federation trop fine.

---

### PT-02 - Session model

Quelle session est persistante ?

Options :
- une session OpenAI principale par mission ;
- une session par agent specialise ;
- une session composee avec resume inter-agent en base.

**Recommandation :**
session de mission + resumes structures inter-agent, pas memoire brute infinie.

---

### PT-03 - File Search scope

Comment partitionner les fichiers dans File Search ?

Options :
- vector store par mission ;
- vector store par projet ;
- vector store mixte avec filtres metadata.

**Recommandation :**
par mission au depart, pour garder un contexte propre et effacable.

---

### PT-04 - Schema canonique des artefacts

Jusqu'ou structurer le dossier ?

Options :
- `artifact -> sections -> claims -> citations`
- ou schema plus simple `artifact -> sections`.

**Recommandation :**
au minimum `artifact`, `section`, `decision`, `citation`, `run_link`.

---

### PT-05 - Politique modele / cout

Quand autoriser `gpt-5.2 pro` ?

**Recommandation :**
jamais par defaut ; seulement sur :
- revue finale premium ;
- arbitrage dur ;
- synthese critique longue ;
- plans enterprise plus tard.

---

### PT-06 - Build review surface

L'agent d'aval lit-il seulement du texte ou aussi :
- diffs code ;
- screenshots ;
- logs ;
- sorties CI ;
- maquettes ?

**Recommandation :**
texte + screenshots d'abord.

---

### PT-07 - Auth et multi-tenant

Le produit reste-t-il mono-utilisateur par projet en V1, ou faut-il des organisations / membres ?

**Recommandation :**
preparer le schema pour `organization_id`, sans ouvrir toute la collaboration riche d'emblee.

---

### PT-08 - Plan B orchestration

Si Restate ne tient pas ses promesses sur le shape exact des runs, quel fallback ?

**Recommandation :**
Temporal est le plan B officiel.
