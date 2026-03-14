# 05_certitude_register

# Registre de certitude

## Confirme
- Cadris est un systeme multi-agent stateful, pas un simple chatbot ni un simple generateur de PDF.
- La stack retenue est `Next.js + FastAPI/Python + OpenAI Responses API / Agents SDK + Restate + PostgreSQL + S3`.
- Le frontend doit etre separe du runtime agentique.
- PostgreSQL est la source de verite canonique pour les missions, les decisions, les issues et les artefacts.
- Restate porte l'etat d'execution durable des missions longues.
- Les fichiers utilisateur vivent en stockage objet et sont lus en V1 via File Search.
- Les artefacts et leurs sections sont les unites documentaires de reference, pas le chat brut.
- Une mission peut etre mise en pause, attendre l'utilisateur puis reprendre sans perdre son contexte critique.
- Une seule mission de cadrage active par projet est autorisee au MVP.
- Les exports sont des snapshots immuables en markdown, PDF ou share link.
- SSE est le mode temps reel par defaut pour la V1.
- PostHog est la brique analytics retenue a ce stade pour la mesure produit.

## Hypotheses de travail
- H1 - La composition V1 de l'equipe active reste volontairement limitee : superviseur, strategie, produit, requirements, puis build review si utile.
- Impact : simplifie la coordination, reduit le cout et garde le runtime lisible ; si faux, il faudra redecouper les roles et les handoffs.
- Pourquoi cette hypothese a ete retenue : les documents amont insistent sur une V1 lisible et sur l'evitement d'une federation d'agents trop fine.

- H2 - Le frontend montre un feed inter-agents filtre avec syntheses du superviseur, pas un flux brut complet en permanence.
- Impact : diminue la surcharge cognitive ; si faux, l'architecture frontend devra gerer plus de bruit, plus de pagination et plus de filtrage.
- Pourquoi cette hypothese a ete retenue : les audits UX signalent le risque de cockpit surcharge et la mission room doit rester intelligible.

- H3 - Le modele V1 reste mono-utilisateur par projet, avec schema prepare a evoluer vers `organization_id`.
- Impact : simplifie auth, permissions et ownership ; si faux, la couche auth et partage devra etre durcie plus tot.
- Pourquoi cette hypothese a ete retenue : la cible MVP et les exclusions explicites repoussent la collaboration riche multi-parties.

- H4 - La matrice documentaire V1 peut etre geree par configuration simple par contexte de mission, sans moteur complexe.
- Impact : permet de calculer le statut dossier rapidement ; si faux, il faudra introduire une structure de couverture documentaire plus riche.
- Pourquoi cette hypothese a ete retenue : le modele de donnees signale ce point comme presque bloquant mais le MVP doit rester faisable.

- H5 - L'historique de section V1 reste limite a la version courante, aux statuts et aux snapshots/export, sans diff engine complet.
- Impact : revision plus simple mais moins fine ; si faux, il faudra ajouter un vrai mecanisme de versions et de comparaison.
- Pourquoi cette hypothese a ete retenue : les flows MVP et l'audit recommandent de limiter la complexite automatique sur les pivots et cascades.

## Inconnus
- I1 - Le provider exact d'authentification et le modele final de tenancy ne sont pas fixes.
- Pourquoi ce point reste inconnu : aucun document ne tranche entre auth purement applicative, auth externe, ni entre mono-user strict et organisation minimale.
- Quel impact potentiel : contrat API, gestion des droits, share links, analytics `user_id`, structure du schema.

- I2 - Le niveau exact de visibilite du feed inter-agents n'est pas tranche produit.
- Pourquoi ce point reste inconnu : les flows et l'IA l'identifient comme un point presque bloquant pour le detail des ecrans.
- Quel impact potentiel : volumetrie SSE, structure des read models, ergonomie de la mission room.

- I3 - Le mode de validation des documents sensibles ou transverses n'est pas decide.
- Pourquoi ce point reste inconnu : le PRD pose encore la question entre validation utilisateur, superviseur, ou double validation.
- Quel impact potentiel : workflow d'approvals, statuts d'artefacts, conditions de cloture.

- I4 - La surface exacte du build review V1 reste partiellement ouverte.
- Pourquoi ce point reste inconnu : la chaine confirme le besoin, mais pas encore si l'agent lit seulement du texte et des captures ou aussi des diffs et logs.
- Quel impact potentiel : outillage du runtime, stockage d'evidences, cout des runs.

- I5 - Les contraintes precises de retention, souverainete ou refus de retrieval gere ne sont pas connues.
- Pourquoi ce point reste inconnu : le MVP exclut l'enterprise lourd, mais ce point peut emerger plus tard avec certains clients.
- Quel impact potentiel : remise en cause partielle de File Search et d'une partie de la couche OpenAI.

## Bloquants
- B1 - La matrice minimale des documents requis par type de mission n'est pas formellement tranchee.
- Pourquoi c'est bloquant : sans cette matrice, le calcul exact de `quality_status`, de completude et de disponibilite du dossier reste partiellement implicite.
- Ce qu'il faut obtenir pour debloquer : une liste minimale de livrables obligatoires pour `Demarrage`, `ProjetFlou` et `Pivot`, avec labels produit associes `Nouveau projet`, `Projet a recadrer` et `Refonte / pivot`.

- B2 - Le mode de validation des documents sensibles n'est pas fixe.
- Pourquoi c'est bloquant : il conditionne les `approvals`, les transitions d'artefacts et la definition exacte d'un dossier "livrable".
- Ce qu'il faut obtenir pour debloquer : une regle claire par type de document critique.

- B3 - Le modele d'auth/tenancy V1 n'est pas formellement decide.
- Pourquoi c'est bloquant : il change les frontieres d'acces projet, le partage, le schema de proprietes et les contrats d'API.
- Ce qu'il faut obtenir pour debloquer : une decision simple entre mono-utilisateur strict, partage par lien seulement, ou organisation minimale.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : l'architecture logique est stable, mais les points B1 a B3 doivent etre arbitres avant une conception detaillee complete.
