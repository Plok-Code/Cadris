# 05_certitude_register

# Registre de certitude

## Confirmé
- Cadris est encore au stade prototype.
- L'architecture retenue se compose au minimum d'une web app, d'un control plane, d'un runtime agentique, de Restate, de PostgreSQL, de S3 et d'un renderer PDF.
- Les missions sont longues, stateful et doivent survivre aux crashes, redeploiements et reprises.
- OpenAI tracing + OpenTelemetry sont les briques d'observabilite choisies pour les runs.
- PostHog est la brique analytics produit retenue.
- Le produit a besoin d'exports markdown, PDF et share links.
- Le renderer PDF est plus fragile et plus lourd qu'un simple rendu web.
- La securite V1 impose deja secrets geres proprement, buckets prives, hygiene logs/traces et sauvegardes.
- Aucun SLO chiffre n'est encore fixe dans les documents.
- Les permissions complexes et la collaboration riche ne font pas partie de la V1.

## Hypothèses de travail
- H1 - Une plateforme de deploiement geree avec conteneurs sera suffisante pour la V1.
- Impact : permet une exploitation simple et rapide ; si faux, il faudra concevoir une couche infra plus lourde.
- Pourquoi cette hypothèse a été retenue : les documents demandent une V1 operable, pas une plateforme DevOps ideale.

- H2 - Trois environnements suffisent : `local`, `staging`, `production`.
- Impact : limite les couts et la complexite ; si faux, le besoin de preview full-stack devra etre industrialise.
- Pourquoi cette hypothèse a été retenue : le pack infra demande peu d'environnements, mais bien definis.

- H3 - Les unites de deploiement V1 restent nettes : web, control plane, runtime, renderer.
- Impact : facilite le rollback et l'isolation des pannes ; si faux, les incidents seront plus diffus et les redeploiements plus risqués.
- Pourquoi cette hypothèse a été retenue : l'architecture logique et les tradeoffs insistent sur la separation web / runs longs / rendu PDF.

- H4 - Une delivery `CI -> staging -> validation humaine -> prod` est suffisante au MVP.
- Impact : garde une mise en production sure sans CD sur-sophistique ; si faux, il faudra renforcer l'automatisation et les gardes-fous.
- Pourquoi cette hypothèse a été retenue : l'equipe est technique, mais le produit n'est pas encore a un niveau de trafic imposant une usine de release.

- H5 - Les migrations doivent rester additives ou backward-compatible pendant la V1.
- Impact : rend le rollback et la reprise des runs realistes ; si faux, chaque release deviendra un risque majeur sur la base canonique et Restate.
- Pourquoi cette hypothèse a été retenue : la persistence et la reprise sont centrales dans tout le projet.

## Inconnus
- I1 - Le fournisseur ou substrat exact de deploiement n'est pas fixe.
- Pourquoi ce point reste inconnu : aucun document ne tranche entre cloud cible, PaaS ou IaaS precise.
- Quel impact potentiel : IaC, reseau, secret manager, deploy, cout, observabilite native.

- I2 - Le niveau exact de trafic et de parallelisme reel n'est pas connu.
- Pourquoi ce point reste inconnu : la V1 n'a pas encore de donnees terrain sur le nombre de missions simultanees.
- Quel impact potentiel : taille des workers, quotas, alertes et budget infra.

- I3 - Le besoin exact d'environnement preview n'est pas tranche.
- Pourquoi ce point reste inconnu : utile pour la revue, mais peut etre trop couteux si on tente de dupliquer la stack complete.
- Quel impact potentiel : forme du pipeline CI/CD et cout operatoire.

- I4 - Les seuils d'alerte et niveaux d'astreinte ne sont pas definis.
- Pourquoi ce point reste inconnu : les documents listent des signaux utiles, mais pas de seuils ops stables.
- Quel impact potentiel : alert fatigue ou incidents non vus.

- I5 - Le provider exact d'auth et certaines politiques de retention viennent encore de l'etape securite.
- Pourquoi ce point reste inconnu : ils restent bloquants a l'etape 22.
- Quel impact potentiel : configuration d'environnements, callbacks, retention logs/traces/backups.

## Bloquants
- B1 - Le substrat de deploiement cible n'est pas decide.
- Pourquoi c'est bloquant : il conditionne la forme exacte du deploiement, de l'IaC, du reseau et de l'outillage ops.
- Ce qu'il faut obtenir pour débloquer : une decision simple sur la plateforme ou le cloud de reference V1.

- B2 - La politique de retention applicable aux logs, traces, backups et donnees de staging n'est pas fixee.
- Pourquoi c'est bloquant : sans elle, l'observabilite et la sauvegarde restent inachevees operationnellement.
- Ce qu'il faut obtenir pour débloquer : une matrice de retention par type de donnee et par environnement.

- B3 - Le provider d'auth et le contrat de callback ne sont pas tranches.
- Pourquoi c'est bloquant : cela change la configuration des environnements, des previews et des releases.
- Ce qu'il faut obtenir pour débloquer : le choix du provider et la liste des URLs/callbacks a supporter.

- B4 - La politique exacte de preview n'est pas arbitree.
- Pourquoi c'est bloquant : elle change directement le cout et la forme du pipeline de delivery.
- Ce qu'il faut obtenir pour débloquer : une decision entre absence de preview, preview leger, ou preview full-stack.

## Statut de transmission
- Transmission autorisée : Oui sous hypothèses
- Raison : la strategie ops V1 est suffisamment claire pour avancer, mais les points B1 a B4 doivent etre tranches avant une mise en oeuvre detaillee.
