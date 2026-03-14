# 03_forbidden_deviations

## Ecarts interdits

- transformer Cadris en monolithe Next.js qui orchestre les runs ;
- faire parler le web directement a Postgres, S3, Restate ou OpenAI ;
- traiter le markdown comme source de verite canonique ;
- construire PDF, share links ou File Search avant la premiere tranche verticale ;
- multiplier les agents avant d'avoir un supervisor et un cycle `waiting_user` stables ;
- coder une mission room cockpit a plusieurs panneaux dominants ;
- inventer un second systeme d'etats hors mapping central ;
- disperser les prompts critiques inline dans le code ;
- construire des surfaces riches de revision avant d'avoir mission et dossier initiaux ;
- ouvrir le post-MVP pendant que le MVP n'est pas stabilise.

## Outils exclus ou non autorises par defaut

- second orchestrateur en plus de Restate ;
- pipeline RAG maison V1 ;
- WebSockets partout ;
- `react-pdf` comme chemin PDF principal ;
- bibliotheque UI qui impose un autre langage visuel ;
- SDK critique duplique dans plusieurs couches sans adapter local ;
- abstractions multi-provider speculatives au debut.

## Patterns interdits

- verite metier dans l'etat client ;
- duplication manuelle des schemas en TS et Python ;
- retry automatique sur operation non idempotente ;
- badges ou statuts compris uniquement par couleur ;
- ombres fortes et effets premium dans l'app de travail ;
- mono utilisee comme police de lecture principale ;
- feed agentique expose comme surface dominante par defaut ;
- configuration prod bricolee hors systeme documente.

## Libertes non autorisees

- changer l'ordre de build sans raison structurelle forte ;
- choisir un flow secondaire comme premiere preuve de valeur ;
- enrichir la marque au detriment de la lisibilite ;
- remplacer `Demarrage` resserre par un plan plus large mais plus flou ;
- ignorer les hypotheses encore ouvertes comme si elles etaient confirmees ;
- introduire des dependances non justifiees "au cas ou".

## Decision de travail

Les deviations interdites Cadris sont celles qui :
**cassent les frontieres, retardent la preuve de valeur, diluent le canonique, ou font deriver le build vers un produit plus complexe que le MVP confirme**.
