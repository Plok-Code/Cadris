# 02_navigation_map

## Navigation principale

La navigation principale distingue cinq destinations, accessibles depuis n'importe quelle zone du produit :

```
[ Mes projets ]  [ Mission en cours ]  [ Dossier ]  [ Révision ]  [ Paramètres ]
```

### Règles de la navigation principale

- **Mes projets** : toujours accessible, toujours la destination de retour par défaut
- **Mission en cours** : n'apparaît que lorsqu'une mission est active — disparaît sinon
- **Dossier** : n'apparaît que lorsqu'un dossier a été généré — désactivé ou masqué avant
- **Révision** : n'apparaît que sur un projet avec un dossier livré
- **Paramètres** : toujours accessible, jamais mis en avant

**Point de vigilance :** la navigation ne doit pas afficher 5 entrées d'emblée si la mission n'a pas encore démarré. L'activation progressive réduit la charge cognitive au démarrage.

---

## Navigation secondaire — Zone Mission active

À l'intérieur d'une mission, la navigation secondaire guide l'utilisateur entre les blocs de contenu :

```
[ Contexte ]  [ Stratégie ]  [ Cadrage produit ]  [ Exigences ]  [ Registre ]  [ Questions ]
```

### Règles de la navigation secondaire

- **Contexte** : résumé du contexte d'entrée qualifié — toujours visible, non modifiable sans reprendre la qualification
- **Stratégie** : bloc vision / problème / cible / valeur / positionnement
- **Cadrage produit** : bloc périmètre / MVP / flows / JTBD
- **Exigences** : bloc FR / NFR / exclusions
- **Registre** : registre de certitude complet (confirmé / hypothèse / inconnu / bloquant)
- **Questions** : liste des questions ouvertes + questions bloquantes, clairement séparées

### Navigation flexible avec ordre suggéré par contexte

La navigation entre blocs est **flexible** (l'utilisateur peut accéder à n'importe quel bloc), mais chaque contexte d'entrée propose un ordre suggéré affiché visuellement :

| Contexte | Ordre suggéré |
|----------|---------------|
| Démarrage | Stratégie → Cadrage produit → Exigences → Registre |
| Projet flou | Collecte de l'existant → Stratégie (reformulation) → Cadrage produit → Exigences → Registre |
| Refonte / pivot | Identification de ce qui reste stable → Stratégie (révision) → Cadrage (révision) → Exigences → Registre |

Chaque bloc affiche un statut visible : **Non commencé / En cours / Suffisant pour décision / Complet**. L'utilisateur n'est pas forcé de suivre l'ordre, mais voit clairement où il en est.

**Point de vigilance :** les blocs Stratégie, Cadrage et Exigences ne doivent pas sembler indépendants — ils forment un dossier cohérent. Un fil de progression ou un indicateur visuel doit matérialiser leur interdépendance.

---

## Navigation secondaire — Zone Dossier

```
[ Vue complète ]  [ Complétude ]  [ Export ]  [ Clôture ]
```

- **Vue complète** : lecture du dossier consolidé
- **Complétude** : signaux de qualité par bloc (présent / suffisant / insuffisant)
- **Export** : choix du format de sortie (markdown, PDF, lien partageable)
- **Clôture** : validation finale de mission avec checklist

---

## Navigation secondaire — Zone Révision

```
[ Blocs impactés ]  [ Arbitrages ]  [ Historique ]
```

- **Blocs impactés** : liste des blocs à mettre à jour suite à un pivot ou changement
- **Arbitrages** : historique des décisions structurantes et leurs justifications
- **Historique** : chronologie des modifications

---

## Profondeur de navigation

| Zone | Profondeur maximale |
|------|---------------------|
| Mes projets → sélection projet | 2 clics |
| Mission active → bloc de contenu | 2 clics |
| Mission active → registre de certitude | 1 clic |
| Dossier → export | 2 clics |
| Dossier → clôture | 2 clics |
| Révision → bloc impacté | 2 clics |
| Paramètres | 1 clic |

**Règle générale :** aucune action critique ne doit nécessiter plus de 3 clics depuis la navigation principale.

---

## Points de vigilance

### V-01 — Ne pas cacher le registre de certitude
Le registre ne doit jamais être relégué à un sous-menu de sous-menu. C'est un élément de confiance central, pas un outil de reporting secondaire.

### V-02 — Distinguer visuellement les questions bloquantes des questions ouvertes
Ces deux catégories ont un poids très différent. Les confondre dans un même espace sans marqueur clair génère une friction de lecture et dilue l'urgence des bloquants.

### V-03 — La transition Mission → Dossier doit être explicite
Le passage de "on travaille" à "c'est terminé" ne doit pas être implicite. Il doit exister un moment de transition visible (écran de clôture, validation finale, signal de livraison).

### V-04 — Ne pas montrer toute la navigation dès l'onboarding
Un utilisateur qui démarre son premier projet ne doit pas voir "Dossier", "Révision" et "Mission en cours" simultanément dès l'arrivée. L'activation progressive de la navigation réduit la charge cognitive initiale.

### V-05 — Éviter les intitulés ambigus
Des labels comme "Gestion", "Outils", "Centre", "Ressources" sont à proscrire. Chaque entrée de navigation doit être nommée selon ce que l'utilisateur cherche à faire, pas selon la technique interne.
