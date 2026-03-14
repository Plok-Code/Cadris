# 04_architecture_go_no_go

## Verdict

**GO sous hypotheses**

## Justification

Le projet peut passer a la suite parce que :
- la stack est alignee avec le produit reel ;
- l'architecture est comprehensible et defendable ;
- la securite V1 est proportionnee ;
- l'exploitation proposee reste globalement sobre ;
- les exclusions MVP evitent deja plusieurs derives classiques.

Le projet ne merite pas un `GO` franc parce que :
- plusieurs decisions transverses restent ouvertes ;
- la discipline de compatibilite des runs longs n'est pas encore assez explicite ;
- une partie de la delivery et de l'ops reste theorique tant que la plateforme cible n'est pas tranchee.

## Conditions minimales pour passer à la suite

1. Trancher `auth/tenancy + contrat des share links`.
2. Fixer une matrice minimale de retention/suppression.
3. Choisir le substrat de deploiement V1.
4. Ecrire la regle de compatibilite des runs et migrations en cours.

## Ce qui n'impose pas un NO GO

- l'absence de preview full-stack ;
- l'absence de Kubernetes ;
- l'absence de RBAC fin ;
- l'absence de SLO chiffres au stade prototype.

## Ce qui ferait basculer en NO GO si non corrige

- laisser l'auth/tenancy floue jusqu'au code ;
- deployer sans strategie explicite pour les runs en cours ;
- garder la retention et la suppression implicites ;
- ajouter des couches ops ou infra supplementaires sans besoin V1 prouve.
