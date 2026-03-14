# 07_handoff_to_gpt_23

## Resume executif

La posture securite / conformite / risque de Cadris V1 peut maintenant etre formulee de maniere exploitable.

Verdict :
- securite minimale V1 definie ;
- risques majeurs identifies ;
- strategie d'acces de haut niveau proposee ;
- transmission autorisee, mais sous hypotheses sur auth/tenancy, retention, share links et perimetre juridique.

La ligne directrice retenue est :
proteger serieusement les donnees projet, les exports et les integrations critiques, sans transformer la V1 en programme enterprise complet.

## Exigences de securite principales

- auth obligatoire pour tout acces non partage ;
- autorisation cote serveur par projet/mission ;
- share links limites a des snapshots exportes, revocables et tracables ;
- buckets et objets prives, acces signes ou via backend ;
- chiffrement en transit et au repos ;
- secrets hors repo et rotation possible ;
- identites techniques separees par composant ;
- hygiene stricte des logs, traces et analytics ;
- sauvegardes de la base canonique et reprise minimale ;
- politique de retention/suppression a definir et appliquer de facon transverse.

## Notes de conformite utiles

- les donnees projet sont traitees comme potentiellement sensibles ;
- le PRD demande un volet `privacy by design` si necessaire ;
- la transparence sur les sous-traitants critiques est requise ;
- les analytics ne doivent pas contenir de contenu utilisateur ;
- le RGPD est l'hypothese la plus plausible, mais la juridiction exacte n'est pas encore tranchee ;
- les conformites lourdes type SOC 2 / ISO / HIPAA ne sont pas des exigences confirmees de la V1.

## Risques majeurs

- mauvaise autorisation liee a un modele d'auth/tenancy encore flou ;
- fuite via share link ;
- fuite indirecte via logs, traces ou analytics ;
- suppression incomplete entre Postgres, S3, File Search et services annexes ;
- ecart entre les attentes de confidentialite client et les traitements tiers ;
- sur-permission des comptes techniques ;
- documents malveillants ou prompt-injectes ;
- absence de restauration credible.

## Strategie d'acces

- `owner-first` pour les humains ;
- `mission-scoped` pour les agents ;
- `least privilege` pour les services ;
- destinataire externe limite a un snapshot exporte ;
- aucun acces operateur permanent par defaut ;
- les permissions complexes restent hors scope V1, mais les controles doivent rester nets.

## Points confirmes

- documents et arbitrages consideres comme sensibles ;
- exports partageables a controler et revoquer ;
- base canonique + stockage objet + retrieval tiers ;
- permissions complexes exclues du MVP ;
- conformite lourde hors noyau V1 ;
- analytics sans contenu utilisateur.

## Hypotheses de travail

- auth V1 simple, centree proprietaire ;
- base RGPD-compatible ;
- share links consideres comme surface sensible ;
- traces techniques traitees comme surface de risque a part entiere.

## Inconnus

- provider exact d'auth et modele final de tenancy ;
- retention/suppression par systeme ;
- politique exacte des share links ;
- juridictions cibles de lancement ;
- surface finale du build review et des traces associees.

## Bloquants

- modele d'auth/tenancy V1 ;
- politique transverse de retention/suppression ;
- contrat exact des share links ;
- cadre juridique prioritaire du lancement.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : les exigences minimales sont bien alignees avec l'architecture, les NFR, les contraintes de donnees et les exclusions MVP deja definies.

## Ce que le GPT 23 doit traiter en priorite

1. Transformer les 4 bloquants restants en decisions explicites.
2. Fixer le modele d'acces final entre owner, share link, services techniques et eventuel support.
3. Formaliser la politique de retention/suppression par systeme.
4. Definir le contrat complet des share links : duree de vie, journalisation, revocation, contenu expose.
5. Verifier la documentation utilisateur et contractuelle minimale a preparer avant lancement.
6. Traduire ces exigences en decisions plus operationnelles sans surcharger la V1.

## Statut de transmission

- Transmission autorisee : Oui sous hypotheses
- Raison : la posture V1 est utilisable, mais les priorites 1 a 4 doivent etre arbitrees en premier a l'etape suivante.
