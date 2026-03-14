# 02_overengineering_flags

## Vue d'ensemble

Le projet n'est pas globalement sur-ingenieré par principe.
La plupart des couches supplementaires repondent a un besoin reel : missions longues, reprise, handoffs, retrieval, exports et audit trail.

Les drapeaux ci-dessous sont donc des **zones a surveiller**, pas des condamnations automatiques.

## Zones de complexité excessive possibles

### OF-01 - Trop d'agents trop tot
- Risque : la logique multi-agent devient une federation difficile a opérer avant d'avoir prouve la boucle V1.
- Statut : sous controle pour l'instant.
- Simplification recommandee : garder peu d'agents larges et nets au debut.

### OF-02 - Renderer PDF trop tot trop autonome
- Risque : un service PDF tres isole, trop industrialise, avant validation de l'usage reel du PDF.
- Statut : a surveiller.
- Simplification recommandee : conserver l'isolation logique, mais ne pas construire une plateforme de rendu complexe avant d'en avoir besoin.

### OF-03 - Preview full-stack
- Risque : dupliquer `Restate + Postgres + runtime + renderer` par PR pour une valeur faible.
- Statut : drapeau net.
- Simplification recommandee : `preview` leger ou pas de preview, `staging` restant l'environnement E2E.

### OF-04 - Observabilite trop ambitieuse trop tot
- Risque : accumulation de dashboards et d'alertes non actionnables.
- Statut : a surveiller.
- Simplification recommandee : 3 dashboards, peu d'alertes, identifiants de correlation partout.

### OF-05 - Durcissement security/enterprise hors scope
- Risque : RBAC fin, SSO, SIEM, certifications, data residency forte, SOC2-like controls avant preuve produit.
- Statut : bien contenu dans les documents.
- Simplification recommandee : maintenir ces sujets hors noyau V1.

## Couches non justifiées si ajoutées maintenant

- Kubernetes sans besoin d'exploitation clair
- bus evenementiel en plus de Restate
- CRDT / coedition temps reel riche
- RAG maison day 1
- environnement preview full-stack obligatoire
- programme conformite enterprise complet

## Services potentiellement inutiles si le scope deborde

- service PDF trop specialise si le volume reste faible
- preview full-stack dedie
- couche d'abstraction provider trop lourde avant un vrai besoin de multi-provider

## Simplifications recommandées

1. Garder `web`, `control-plane`, `runtime`, `renderer` comme plafond de complexite applicative V1.
2. Refuser tout service supplementaire qui ne sert ni la reprise, ni le dossier, ni la securite minimale.
3. Utiliser `staging` comme environnement E2E de reference, pas un maillage d'environnements equivalent a une V2.
4. Garder la governance technique centree sur la discipline de schema, de migrations et de reprise plutot que sur la multiplication d'outils.
