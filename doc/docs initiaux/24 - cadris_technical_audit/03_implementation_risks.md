# 03_implementation_risks

## Risques majeurs d’implémentation

| ID | Risque | Cause probable | Impact | Priorité |
|----|--------|----------------|--------|----------|
| IR-01 | Autorisation mal implementee | auth/tenancy encore ouverte | exposition d'un projet ou d'un export | Critique |
| IR-02 | Runs en cours casses par redeploiement | absence de doctrine explicite de compatibilite workflow/runtime | missions bloquees ou dupliquees | Critique |
| IR-03 | Migrations incompatibles | schema qui evolue plus vite que runtime et control plane | panne applicative, rollback difficile | Critique |
| IR-04 | Suppression/purge incoherente | retention non tranchee sur Postgres, S3, File Search, traces | dette de conformite et perte de confiance | Haute |
| IR-05 | Cout ops/LLM sous-estime | OpenAI, tracing, renderer PDF, staging E2E | facture ou throttling inattendus | Haute |
| IR-06 | Renderer PDF instable | Chromium, timeouts, ressources | valeur percue degradee, support accru | Haute |
| IR-07 | Mapping fichier -> index -> mission fragile | couplage S3 / File Search / metadata | citations cassees, purge difficile | Haute |
| IR-08 | Observabilite sensible mal calibree | trop ou pas assez de logs/traces | fuite de donnees ou pannes peu visibles | Haute |
| IR-09 | Choix de plateforme tardif | substrat de deploiement non fixe | delivery ralentie, IaC floue, ops retarde | Moyenne a Haute |
| IR-10 | Preview trop ambitieuse | envie de confort DX non arbitree | cout et complexite inutiles | Moyenne |

## Causes probables

- decisions transverses encore non fermees ;
- produit techniquement exigeant pour une V1 ;
- forte dependance a des integrations critiques ;
- besoin de compatibilite sur des missions durables, pas seulement sur du CRUD.

## Impacts principaux

- blocage des missions longues ;
- incoherence entre etat de run et etat metier ;
- exposition non voulue de donnees ;
- cout operatoire superieur a la valeur V1 ;
- perte de confiance utilisateur si reprise/export deviennent peu fiables.

## Priorités de traitement

### P1 - Avant implementation detaillee
- auth/tenancy + share links
- compatibilite des runs en cours
- migrations additives / backward-compatible
- retention transverse

### P2 - Tres tot dans la mise en oeuvre
- cout et quotas
- renderer PDF
- mapping S3 / File Search / purge
- hygiene des logs et traces

### P3 - Plus tard si besoin confirme
- preview plus riche
- abstraction provider plus large
- outillage ops plus avance
