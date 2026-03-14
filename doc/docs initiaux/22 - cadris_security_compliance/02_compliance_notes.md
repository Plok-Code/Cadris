# 02_compliance_notes

## Vue d'ensemble

Ces notes servent a cadrer la conformite utile a la V1.
Elles ne valent pas programme de conformite complet ni avis juridique.

La ligne retenue est simple :
- couvrir les obligations probables liees aux donnees, aux exports et aux sous-traitants ;
- ne pas pretendre a une conformite lourde que le MVP n'a pas choisie ;
- rendre explicites les points a verifier avant lancement public.

## Obligations connues

### C-01 - Confidentialite des donnees projet
- les informations partagees par l'utilisateur sont explicitement considerees comme potentiellement sensibles dans le PRD ;
- elles ne doivent pas etre exposees au-dela des personnes et agents autorises ;
- cette obligation existe meme si le produit ne vise pas un secteur reglemente.

### C-02 - Privacy by design minimale
- le PRD demande un volet `privacy by design` si necessaire ;
- au MVP, cela implique au minimum :
  - minimisation des donnees analytiques ;
  - limitation des acces ;
  - suppression/revocation possibles ;
  - transparence sur les integrations tierces.

### C-03 - Encadrement des exports partageables
- les exports partageables doivent etre controles, tracables et revocables ;
- un share link doit etre traite comme une diffusion potentielle de contenu sensible ;
- un export partiel doit etre clairement marque pour eviter une mauvaise interpretation.

### C-04 - Transparence sur les sous-traitants et integrations
- la V1 repose sur des services tiers critiques : OpenAI, S3, PostHog, provider d'auth, eventuellement renderer ;
- leur role doit etre explique dans la documentation de confidentialite et dans les documents contractuels utiles ;
- la retention et le type de donnees envoyees a chaque service doivent etre documentes.

### C-05 - Analytics sans contenu utilisateur
- le tracking ne doit pas contenir le texte des reponses, arbitrages ou documents ;
- si un `user_id` est envoye, il doit rester pseudonymise quand le cadre RGPD s'applique ;
- les proprietes analytics doivent rester comportementales, pas documentaires.

## Hypotheses de conformite

### H-01 - Le RGPD est probablement pertinent
- Pourquoi : le projet manipule email, compte utilisateur, traces et documents, et la chaine mentionne explicitement le RGPD dans les exigences analytics.
- Impact : besoin probable de politique de confidentialite, base legale, information sur sous-traitants, gestion de droits et retention.

### H-02 - Les conformites lourdes ne sont pas requises en V1
- Pourquoi : le MVP exclut la gouvernance enterprise, la securite profonde, la conformite lourde et les contextes ultra-reglementes.
- Impact : pas de cible directe SOC 2, ISO 27001, HIPAA ou equivalent dans cette etape.

### H-03 - Le produit reste dans un perimetre B2B SaaS generaliste
- Pourquoi : la cible principale est early-stage, hors verticales tres reglementees.
- Impact : les obligations de base sur donnees, contrats et transparence priment sur les regimes sectoriels specifiques.

## Points a verifier plus tard

### V-01 - Juridictions cibles exactes
- UE uniquement ;
- France + UE ;
- UE + Etats-Unis ;
- autre combinaison.

Sans cette reponse, on ne peut pas figer completement le perimetre RGPD / ePrivacy / CCPA ou equivalents.

### V-02 - Role exact de chaque prestataire
- qui agit comme sous-traitant ;
- quelles donnees transitent ;
- quelles durees de retention s'appliquent ;
- quels accords contractuels ou DPA sont necessaires.

### V-03 - Politique de cookies / consentement analytics
- depend de l'implementation effective de PostHog, du mode self-hosted ou non, et des juridictions cibles ;
- a clarifier avant mise en production publique.

### V-04 - Procedure de suppression et de reponse aux demandes utilisateur
- suppression de compte ;
- suppression de projet ;
- purge des fichiers indexes ;
- purge des traces et evenements annexes.

### V-05 - Conditions de partage externe
- duree de vie des share links ;
- journalisation d'acces ;
- eventuelle protection complementaire pour les exports sensibles.

## Risques evidents de non-conformite

### NC-01 - Envoyer du contenu documentaire dans les analytics
Risque : fuite de donnees confidentielles + non-respect du principe de minimisation.

### NC-02 - Laisser des share links irreversibles ou trop larges
Risque : diffusion non maitrisee d'un dossier sensible sans capacite de retrait.

### NC-03 - Oublier de declarer les sous-traitants critiques
Risque : manque de transparence contractuelle et de politique de confidentialite.

### NC-04 - Ne pas definir la retention ou la suppression
Risque : conservation indefinie des projets, fichiers, traces et index externes.

### NC-05 - Journaliser trop de contenu dans les traces techniques
Risque : la confidentialite est affaiblie meme si l'application semble bien protegee.

## Documents utiles a prevoir pour la V1

- politique de confidentialite ;
- conditions d'utilisation ou CGU/CGV selon le modele retenu ;
- liste simple des sous-traitants critiques ;
- note interne de retention et suppression ;
- note interne sur les share links et les exports ;
- DPA ou equivalent si la cible B2B le demande.

## Ce qui n'est pas confirme a ce stade

- exigence de certification externe ;
- obligation sectorielle forte ;
- data residency stricte ;
- zero data retention fournisseur ;
- obligation de permissions complexes multi-utilisateurs.
