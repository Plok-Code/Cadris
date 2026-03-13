# 03_ux_complexity_flags

## Signaux de complexité UX

---

## UCF-01 — Dialogue guidé : risque de fatigue cognitive si les boucles sont trop longues

**Description :** le modèle d'interaction (question → réponse → reformulation → validation) est répété 5 fois pour le Bloc Stratégie, puis à nouveau pour Cadrage et Exigences. Si chaque boucle prend 3 à 5 minutes, une mission complète peut durer 45 minutes à 1h30 selon la complexité du projet.

**Signal d'alerte :** sans indication de durée estimée et sans micro-signaux d'avancement, l'utilisateur ne sait pas s'il est à mi-chemin ou à 10% du parcours. La fatigue cognitive peut provoquer un abandon.

**Recommandation :**
- Afficher une durée estimée par étape au démarrage de chaque bloc ("Cette étape prend environ 10 minutes")
- Afficher le numéro de la question dans le bloc ("Question 2 sur 5")
- Déclencher un micro-signal positif à chaque sous-élément validé, pas seulement à la fin du bloc

---

## UCF-02 — E-06 : ordre problème/vision encore non arbitré dans l'interface

**Description :** la tension T-01 identifiée dans l'audit de cohérence (hiérarchie de contenu dit "vision en premier", flow dit "problème en premier") doit être résolue avant implémentation. Si les deux couches divergent, le développeur et le designer travailleront sur des bases contradictoires.

**Signal d'alerte :** c'est le premier dialogue de fond que voit l'utilisateur. La première question posée conditionne sa perception du service pour toute la mission.

**Recommandation :**
- Ordre retenu : problème → cible → proposition de valeur → vision → positionnement
- Justification : le problème est le point d'entrée le plus naturel pour un builder ("Quel problème mon produit résout-il ?" est plus concret que "Quelle est ma vision ?")
- La vision est reformulée en fin de bloc à partir des réponses précédentes, pas posée à froid

---

## UCF-03 — Registre de certitude : risque de surcharge perçue si toujours visible

**Description :** E-09 (registre de certitude) est conçu comme "accessible en permanence". Si le registre est visible comme panneau latéral pendant tout le dialogue de bloc, l'utilisateur est exposé en permanence à ses incertitudes et bloquants — ce qui peut créer un sentiment d'anxiété ou de "travail non terminé" plutôt que de confiance.

**Signal d'alerte :** l'hypothèse UX HYP-4 dit que la transparence des incertitudes est un signal de confiance. Mais ce n'est vrai que si l'affichage est bien dosé et bien encadré. Un registre qui affiche 5 "inconnus" et 2 "bloquants" en permanence peut décourager.

**Recommandation :**
- Au MVP : le registre est accessible depuis le Hub (E-05) sur action explicite, pas affiché en permanence pendant le dialogue
- Seul le compteur de bloquants actifs (ex : "2 points à résoudre") reste visible en tête de page
- Le registre complet est affiché en avant au moment du dossier consolidé (E-12), pas pendant la production

---

## UCF-04 — Transition vers le dossier : risque de déception si le dossier "fait document"

**Description :** le livrable principal est un dossier textuel. Pour un vibroder habitué à des outils visuels (Lovable, Figma, Linear), recevoir un dossier markdown ou PDF peut être perçu comme insuffisant ou austère.

**Signal d'alerte :** si l'export est présenté brut (un fichier texte), sans mise en forme ni signal de valeur, l'utilisateur peut sous-estimer ce qu'il a reçu.

**Recommandation :**
- Le dossier consolidé (E-12) doit avoir une présentation soignée dans l'interface : sections nommées, statuts de certitude visibles, résumé exécutif en tête
- L'export markdown doit être proprement structuré avec des titres clairs, pas un flux de texte brut
- L'écran E-15 (clôture) doit célébrer la livraison : "Votre dossier est prêt. Voici ce que vous pouvez faire maintenant."

---

## UCF-05 — Onboarding : risque d'exemple de résultat trop dense

**Description :** l'étape 2 de l'onboarding propose un extrait de dossier exemple (Bloc Stratégie complété). Si cet exemple est trop long ou trop formel, il peut intimider l'utilisateur plutôt que le rassurer.

**Recommandation :**
- L'exemple doit être partiel : 3 lignes maximum par sous-élément, pas un dossier complet
- Accompagné du message : "C'est Cadris qui produit ça. Vous répondez à des questions."
- Format visuel : encadré, non scrollable, visuellement distinct d'une "page à remplir"

---

## UCF-06 — E-02 (qualification) : risque de questions trop binaires

**Description :** les exemples de questions proposées dans les flows sont binaires (oui/non) ou fermées. Des questions trop fermées ne capturent pas la réalité des projets hybrides et forcent un choix artificiel.

**Exemples problématiques :**
- "Le projet est-il clair pour toute l'équipe ?" → trop binaire
- "Est-ce un changement de direction majeur ?" → "majeur" est subjectif

**Recommandation :** les questions de qualification doivent être formulées avec des choix concrets illustrés par des exemples :
- "Où en est votre projet ?" avec des options : "C'est une idée, j'ai peu formalisé" / "J'ai déjà du code ou des specs" / "J'ai un produit qui tourne mais je cherche à le recadrer"
- Ces formulations sont plus proches du mental model de l'utilisateur que des questions oui/non abstraites

---

## UCF-07 — Clôture (E-15) : checklist manuelle vs validation automatique

**Description :** la checklist de clôture (4 critères : cohérence, couverture, bloquants identifiés, décision possible pour l'équipe suivante) peut être source de friction si l'utilisateur doit la valider manuellement sans savoir comment évaluer chaque critère.

**Recommandation :**
- La checklist est pré-remplie automatiquement à partir des données de la mission (blocs complétés → couverture ✓, aucun bloquant non traité → bloquants identifiés ✓, etc.)
- L'utilisateur ne valide que les éléments non automatisables (ex : "l'équipe suivante peut prendre la suite ?")
- Un résumé lisible remplace un formulaire : "Votre dossier couvre [X sur Y blocs], contient [Z bloquants documentés], [W contradictions résolues]."

---

## Zones de confusion probables en usage réel

| Zone | Confusion probable | Gravité |
|------|-------------------|---------|
| E-02 | Mauvaise compréhension des catégories de contexte | Haute |
| E-06 | Première question trop abstraite → réponse vague | Haute |
| E-09/E-10 | Différence entre registre et questions bloquantes non comprise | Moyenne |
| E-13 | "Dossier exploitable avec réserves" non compris comme verdict positif | Moyenne |
| E-15 | Utilisateur ne sait pas ce qu'il doit "faire" après la clôture | Moyenne |
| E-12 | Dossier perçu comme trop dense ou trop austère | Moyenne |
