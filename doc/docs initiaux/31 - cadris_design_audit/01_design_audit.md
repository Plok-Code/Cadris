# 01_design_audit

## Coherences observees

### 1. La marque et le produit racontent bien la meme chose

La chaine 25 -> 30 reste coherent sur un point central :
- Cadris doit paraitre structurel ;
- calme ;
- expert accessible ;
- anti-hype ;
- tourne vers la mise au net du projet.

Cette ligne est tenue dans :
- la direction `Architecture editoriale calme` ;
- la palette `Mineral petrole` ;
- le choix typo `Public Sans + IBM Plex Mono` ;
- la UI `mission-first` ;
- l'UX orientee synthese, arbitrage et progression visible ;
- le design system compact et semantique.

### 2. L'identite visuelle reste compatible avec l'usage reel

Le systeme visuel ne pousse pas Cadris vers :
- un imaginaire IA spectaculaire ;
- un outil cyber ;
- un cabinet ;
- un SaaS ludique.

Il reste compatible avec :
- une landing ;
- une mission room ;
- un dossier exporte ;
- une interface dense mais lisible.

### 3. Le design system suit bien les besoins UX

Les composants prioritaires definis en etape 30 couvrent correctement les flows retenus :
- question ;
- certitude ;
- progression ;
- revision ;
- export ;
- synthese.

Le systeme n'est ni trop abstrait, ni trop large pour la V1.

### 4. Le logo va dans la bonne direction

Les assets presents dans `27 - cadris_logo_direction` confirment une famille de signe :
- structurelle ;
- reductible ;
- proche du monogramme / assemblage ;
- coherente avec l'idee de cadre, de couche et de mise en ordre.

Le signe observe n'entre pas en contradiction avec la direction de marque.

## Tensions observees

### T1 - Vocabulaire d'etat maintenant canonise, mais a centraliser

Le corpus recent retient des labels primaires uniques :
- `Solide`
- `A confirmer`
- `Inconnu`
- `Bloquant`
- `Pret a decider` pour la progression

Les termes `Confirme`, `Hypothese` et `Suffisant pour decision` restent seulement des alias secondaires ou des traces historiques.

La tension restante n'est donc plus le choix des mots, mais leur centralisation technique pour eviter :
- des badges differents ;
- des microcopies divergentes ;
- des specs de composants ambigues.

### T2 - Les contrastes de statuts sont encore un peu fragiles

Le systeme couleur principal est bon, mais plusieurs couples texte/fond de statut sont limites pour du petit texte :
- solide : environ `3.89:1`
- a confirmer : environ `4.00:1`
- inconnu : environ `4.25:1`
- bloquant : environ `4.38:1`

Conclusion :
- acceptable pour des tags robustes et labels visibles ;
- plus fragile pour du texte petit, fin ou secondaire.

### T3 - Le systeme logo est coherent en intention, pas encore complet en production

La direction logo demande :
- symbole ;
- logotype ;
- combination mark ;
- favicon.

Mais le pack actuel montre surtout :
- des symboles ;
- des variantes de contraste ;
- un naming encore instable ;
- pas de lockup canonique clairement fige pour le web.

Il y a donc un decalage entre :
- direction logo bien posee ;
- production finale du pack logo.

### T4 - Le symbole peut devenir trop present si mal utilise

Le signe actuel a une geometrie forte et un cadre marque.
C'est un atout pour :
- la memorisation ;
- le favicon ;
- l'entree produit ;
- la signature documentaire.

Mais si on le repete trop dans l'app, il peut pousser l'interface vers :
- l'effet tampon ;
- le sur-cadrage ;
- une sensation plus institutionnelle que `expert accessible`.

## Robustesse design globale

Le design Cadris est globalement :
- coherent ;
- lisible ;
- maintenable en V1 ;
- plausible a implementer sans rework massif.

Je ne vois pas de contradiction structurelle entre :
- marque ;
- identite ;
- logo ;
- UI ;
- UX ;
- design system.

Le projet n'est pas dans un cas de `NO GO`.
Il est plutot dans un cas :
**bon socle, quelques verrouillages de discipline encore necessaires**.

## Ajustements minimaux recommandes

### 1. Centraliser la table officielle de mapping des etats

Document a produire ou ajouter :
- cle interne ;
- label affiche ;
- ton ;
- couleur ;
- usages autorises.

Objectif :
- appliquer partout `Solide`, `A confirmer`, `Inconnu`, `Bloquant` et `Pret a decider` comme labels primaires ;
- garder `Confirme`, `Hypothese` et `Suffisant pour decision` en alias secondaires seulement.

### 2. Renforcer la doctrine accessibilite des statuts

Il faut choisir une regle simple :
- soit des foregrounds plus fonces ;
- soit des tags plus gras et plus grands ;
- soit les deux.

Objectif :
- ne pas faire reposer les statuts critiques sur une teinte trop douce.

### 3. Geler un pack logo canonique

Minimum a figer :
- symbole light
- symbole dark
- wordmark light
- wordmark dark
- lockup horizontal light
- lockup horizontal dark
- favicon `16`, `32`, `ico`

Objectif :
- passer d'une exploration reussie a un systeme integrable proprement.

### 4. Poser une source de verite design unique

Il faut dire ce qui fait foi en premier entre :
- markdown ;
- maquette ;
- code.

Objectif :
- eviter les derives entre docs, assets et future implementation.

## Decision d'audit

Le design Cadris est :
**coherent et defendable pour la suite, mais il doit encore verrouiller ses etats, son pack logo canonique et sa discipline d'accessibilite avant handoff final propre**.
