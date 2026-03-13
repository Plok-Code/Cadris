# Questions bloquantes

Ce document ne signifie pas que le projet est arrêté.  
Il liste les questions que le GPT 02 devra traiter en priorité pour éviter un brief trop ambitieux mais inexploitable.

## 1. Comment mesurer objectivement la qualité d'un dossier ?
**Pourquoi c'est bloquant :**  
La réussite actuelle est formulée en termes de qualité perçue très élevée, mais sans critères précis il sera difficile de juger si le système produit réellement des documents professionnels.

**Ce qu'il faut obtenir :**
- une grille de qualité ;
- des dimensions d'évaluation ;
- un mode de revue ;
- un seuil minimal d'acceptation.

## 2. Que signifie exactement "stack pertinente" ?
**Pourquoi c'est bloquant :**  
Le projet veut empêcher les mauvais choix techniques, mais il faut une règle d'évaluation claire pour différencier une recommandation crédible d'une recommandation arbitraire.

**Ce qu'il faut obtenir :**
- des critères de pertinence ;
- des règles de justification ;
- des cas où le système doit insister fortement contre un mauvais choix.

## 3. Jusqu'où va réellement le périmètre "SaaS à 100%" ?
**Pourquoi c'est bloquant :**  
Le périmètre exprimé est très large. Sans cadre, le prototype risque de devenir trop vaste, trop lent ou trop hétérogène.

**Ce qu'il faut obtenir :**
- une segmentation du périmètre SaaS ;
- une définition de ce qui est couvert par défaut ;
- des modules conditionnels par cas.

## 4. Quelle est la structure normée du dossier final exportable ?
**Pourquoi c'est bloquant :**  
L'ambition documentaire est très large, mais l'utilisateur final et les LLM ont besoin d'un format de sortie clair, stable et hiérarchisé.

**Ce qu'il faut obtenir :**
- une structure de dossier canonique ;
- une hiérarchie de documents ;
- une logique de consolidation ;
- une séparation entre documents obligatoires et documents contextuels.

## 5. Comment le chatbot d'aval arbitre-t-il entre suggestion et contrôle ?
**Pourquoi c'est bloquant :**  
Le chatbot doit à la fois suggérer le prochain prompt et contrôler la qualité des sorties. Sans doctrine claire, il risque d'être soit trop passif, soit trop intrusif.

**Ce qu'il faut obtenir :**
- des règles de comportement ;
- des types de vérifications ;
- des seuils d'alerte ;
- des cas où il doit simplement recommander, et des cas où il doit insister fortement.

## 6. Quel modèle de crédits est économiquement viable sans dégrader la confiance ?
**Pourquoi c'est bloquant :**  
Le principe du crédit est posé, mais pas son équilibre réel. Un mauvais réglage peut casser l'expérience ou la monétisation.

**Ce qu'il faut obtenir :**
- nombre moyen de crédits consommés ;
- structure de packs ;
- logique de pause ou brouillon à 0 crédit ;
- moment optimal du paywall ;
- expérience utilisateur perçue.
