# 03_risk_register

## Echelle utilisee

- Probabilite : Faible / Moyenne / Haute
- Impact : Moyen / Haut / Critique
- Priorite : P1 = avant production, P2 = debut V1, P3 = plus tard

## Risques majeurs

| ID | Risque | Surface | Impact potentiel | Probabilite supposee | Priorite | Traitement recommande |
|----|--------|---------|------------------|----------------------|----------|-----------------------|
| R-01 | Auth/tenancy mal tranchee ou mal appliquee | acces produit | acces a un projet qui ne devrait pas etre visible | Moyenne | P1 | controles serveur par projet, modele owner-first, deny by default |
| R-02 | Fuite via share link | exports | diffusion externe d'un dossier sensible | Moyenne | P1 | token fort, revocation, snapshot seul, journalisation, eventuelle expiration |
| R-03 | Donnees sensibles dans logs, traces ou analytics | observabilite | fuite silencieuse de contenu projet hors surface principale | Moyenne | P1 | hygiene stricte des logs, minimisation analytics, retention traces documentee |
| R-04 | Suppression incoherente entre Postgres, S3, File Search et outils annexes | retention | donnees supprimees en apparence mais toujours presentes ailleurs | Moyenne | P1 | politique de suppression transverse et jobs de purge |
| R-05 | Attentes client incompatibles avec les traitements tiers OpenAI / File Search / PostHog | conformite / confiance | refus d'usage, litige contractuel, repositionnement force | Moyenne | P1 | transparence sous-traitants, verifier retention et perimetre des donnees |
| R-06 | Sur-permission des comptes techniques | integrations | lecture ou modification excessive par un service interne | Moyenne | P1 | identites techniques separees, droits minimaux par composant |
| R-07 | Fichier malveillant ou document prompt-injecte | ingestion / runtime | sorties trompeuses, contamination des runs, perte de confiance | Moyenne | P2 | validation upload, formats limites, cloisonnement des outils disponibles |
| R-08 | Echec de sauvegarde ou restauration | donnees canoniques | perte de mission, d'artefacts ou d'exports critiques | Faible a moyenne | P2 | sauvegardes automatiques + test de restauration |
| R-09 | Export partiel pris pour une version finale | transmission | mauvaise decision de build ou partage trompeur | Moyenne | P2 | marquage explicite, reserves visibles, UI claire |
| R-10 | Acces operateur interne non cadre | support / exploitation | consultation injustifiee de donnees client | Faible a moyenne | P2 | pas d'acces permanent, break-glass audite, justification obligatoire |

## Priorites de traitement

### P1 - A traiter avant mise en production
- R-01 Auth/tenancy et autorisation serveur
- R-02 Share links
- R-03 Logs / traces / analytics
- R-04 Retention et suppression
- R-05 Transparence sous-traitants et posture fournisseur
- R-06 Permissions des services techniques

### P2 - A traiter au lancement ou juste apres
- R-07 Hygiene d'ingestion et resistance minimale a la prompt injection
- R-08 Sauvegardes / restauration
- R-09 Qualite de marquage des exports partiels
- R-10 Acces operateur interne

## Risques acceptes

### RA-01 - Pas de RBAC fin multi-utilisateurs en V1
- Statut : Accepte
- Raison : hors scope MVP, permissions complexes explicitement exclues.
- Contrepartie : controle simple par proprietaire + share links restreints.

### RA-02 - Pas de programme de conformite enterprise complet en V1
- Statut : Accepte
- Raison : la cible MVP n'est pas enterprise lourde ni ultra-reglementee.
- Contrepartie : documenter les limites et ne pas sur-promettre.

### RA-03 - Dependance fournisseur forte sur OpenAI
- Statut : Accepte sous surveillance
- Raison : la qualite produit prime en V1 sur la souverainete totale.
- Contrepartie : transparence, verification de retention, plan B si exigence forte apparait.

## Points de vigilance

- un risque de securite n'est pas toujours une obligation legale ;
- un risque accepte doit rester explicite et revu plus tard ;
- les risques les plus graves ici sont ceux qui exposent un dossier ou rendent la suppression non credible.
