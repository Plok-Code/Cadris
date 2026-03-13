# 06_blocking_questions

## Questions bloquantes restantes - Modele de domaine & Donnees

### PT-01 - Faut-il une entite dediee pour la matrice de couverture documentaire ?
**Pourquoi c'est presque bloquant :**
Le produit parle d'un grand nombre de livrables potentiels. Si la mission doit savoir finement ce qui est obligatoire, recommande ou optionnel, un simple booleen `required_for_dossier` peut devenir trop pauvre.

**Ce qu'il faut obtenir :**
Une decision sur :
- booleen simple par artifact ;
- table `mission_document_requirements` ;
- ou configuration par type de mission.

### PT-02 - Quel niveau d'historique garde-t-on sur les sections ?
**Pourquoi c'est presque bloquant :**
Le pivot et la relecture croisee deviennent plus solides si l'on peut auditer l'evolution d'une section.

**Ce qu'il faut obtenir :**
Une decision sur :
- version courante seulement ;
- snapshots de section ;
- historique complet des diffs.

### PT-03 - Comment modeliser la liaison fine entre Issues et Artifacts impacts ?
**Pourquoi c'est presque bloquant :**
Le modele dit qu'un issue impacte des documents, mais il ne possede pas encore de table de jointure explicite.

**Ce qu'il faut obtenir :**
Une decision sur :
- lien derive en application ;
- table de relation dediee ;
- ou liaison au niveau `ArtifactSection`.

## Statut

Ce ne sont pas des blocages de doctrine, mais des choix de schema a trancher avant implementation detaillee.
