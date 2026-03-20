# Cadris — Specs UI / UX

## 1. Cohérence des docs après correction
- Quand l'utilisateur corrige 1 doc d'un bloc (ex: "Vision produit" dans les 4 docs de Stratégie), les 3 autres docs du même bloc doivent être re-vérifiés pour cohérence avec la correction
- Même logique pour tous les blocs (Business & Produit, Tech & Design, Consolidation)
- Concrètement : si correction → re-run l'agent avec le feedback → re-présenter TOUS les docs du bloc pour validation

## 2. Rendu Markdown optimisé
- Les tableaux Markdown s'affichent mal dans la fenêtre de review
- Intégrer un vrai renderer Markdown (react-markdown ou similar) avec support :
  - Tableaux HTML formatés
  - Code blocks
  - Listes imbriquées
  - Blockquotes
  - Gras, italique, code inline
- Le rendu doit ressembler à un lecteur .md professionnel (style GitHub)

## 3. Navigation dans le bloc de docs
- On peut naviguer entre les docs **du bloc en cours uniquement** (pas les blocs précédents)
- Cliquer sur les dots de navigation pour revenir à n'importe quel doc du bloc
- Bouton "Précédent" pour revenir au doc précédent dans le bloc
- Avant de passer au bloc suivant : message de confirmation "Validez-vous tous les documents de ce bloc ? Vous ne pourrez plus revenir dessus."
- Une fois le bloc validé, on ne peut plus y revenir (les docs sont lockés)

## 4. Skip docs déjà validés
- Quand une nouvelle wave se termine, ne montrer que les NOUVEAUX docs (ceux de la wave qui vient de finir)
- Ne PAS re-montrer les docs des waves précédentes déjà validés

## 5. Sommaire fixe (page dossier final)
- Le sommaire des docs à gauche doit être sticky (position: sticky)
- Seul le contenu du doc sélectionné à droite scroll
- Le sommaire ne bouge jamais de l'écran

## 6. Export / Téléchargement
- 3 boutons d'export :
  - "Télécharger MD" → ZIP contenant tous les .md organisés par dossier
  - "Télécharger PDF" → ZIP contenant tous les .pdf
  - "Tout télécharger" → ZIP avec .md ET .pdf ensemble
- Les endpoints doivent fonctionner (actuellement cassés)

## 7. Historique des projets / Compte
- Page "Mes projets" accessible depuis le menu compte
- Liste des cadrages passés avec date, nom du projet, plan utilisé
- Chaque projet est re-consultable (page dossier final)
- Les docs restent accessibles tant que le compte existe

## 8. Flow d'accueil / Auth
- Page d'accueil → bouton "Commencer" → page connexion (Google/GitHub)
- Après connexion → page des offres (Free/Starter/Pro/Expert)
- Bouton "Continuer avec Free" → lance le cadrage
- Compte OBLIGATOIRE avant de lancer un cadrage (pas de cadrage anonyme)
- Pas de cadrage sans compte pour éviter l'abus du free plan

## 9. Guide utilisateur — Mise en avant
- Le user_guide doit être mis en avant sur la page dossier final (pas enterré dans la liste)
- Affiché en premier ou avec un badge "À lire en premier"
- Doit indiquer clairement les étapes de démarrage dans cet ordre :
  1. Créer un repo GitHub (public ou privé) — avec un prompt prêt pour Claude Code
  2. Dézipper les docs dans l'IDE à la racine du projet
  3. Installer la stack technique — en précisant que Claude Code/Codex peut le faire avec un prompt fourni
  4. Lancer les phases de développement

## 10. Guide d'implémentation — Chemins fichiers
- Le plan d'implémentation référence les chemins du ZIP
- Problème : l'utilisateur dézip avant de mettre dans l'IDE, les chemins restent relatifs
- Solution : le guide doit dire clairement "Dézippez ce dossier à la RACINE de votre projet" dès le début
- Les chemins dans le guide doivent correspondre à la structure post-dézip
- Ne PAS dire "se référer aux chemins du zip" mais "les fichiers sont organisés comme suit dans votre projet :"

## 11. Prompts Claude Code dans le guide
- Chaque phase du guide doit inclure un prompt prêt à copier-coller dans Claude Code/Codex
- Le guide doit indiquer que Claude Code peut automatiser :
  - Création du repo GitHub
  - Installation de la stack
  - Exécution de chaque phase
- Format : blocs de code avec le prompt exact à donner

---

## Priorités d'implémentation suggérées

### P0 — Bloquant
- [ ] Fix export ZIP/MD/PDF (actuellement cassé)
- [ ] Fix re-review des docs déjà validés (skip les anciens)
- [ ] Rendu Markdown propre (tableaux, listes)

### P1 — UX critique
- [ ] Navigation dans le bloc (précédent, dots cliquables)
- [ ] Confirmation avant passage au bloc suivant
- [ ] Sommaire sticky sur page dossier
- [ ] Scroll to top sur changement de doc

### P2 — Flow utilisateur
- [ ] Auth obligatoire avant cadrage
- [ ] Page offres avec "Continuer Free"
- [ ] Page "Mes projets" dans le compte
- [ ] Projets consultables dans l'historique

### P3 — Qualité des livrables
- [ ] Guide utilisateur mis en avant
- [ ] Ordre des étapes dans le guide (repo → dézip → stack → dev)
- [ ] Prompts Claude Code prêts à copier dans le guide
- [ ] Correction chemins fichiers dans le plan d'implémentation
- [ ] Re-vérification cohérence des docs après correction dans un bloc
