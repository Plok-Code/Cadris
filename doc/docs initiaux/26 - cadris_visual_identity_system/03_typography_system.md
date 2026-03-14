# 03_typography_system

## Role du systeme typographique

La typographie de Cadris doit porter simultanement quatre messages :
- `CADRIS.AI donne un cadre` ;
- c'est un produit serieux, pas un theatre IA ;
- c'est accessible a des createurs de projet de niveaux heterogenes ;
- cela securise le projet au lieu d'intimider son auteur.

La typographie n'a donc pas seulement un role esthetique.
Elle porte une part centrale de :
- la lisibilite ;
- la confiance ;
- la densite d'information ;
- la perception de maitrise.

## Ce que dit la litterature utile

### 1. La question "serif vs sans serif" n'a pas de gagnant universel
Quand la taille, le x-height, l'espacement et la mise en page sont controles, la famille serif ou sans serif ne suffit pas a elle seule a predire la vitesse de lecture ou le taux d'erreur.

Consequence pour Cadris :
- ne pas choisir une sans serif en disant qu'elle est "scientifiquement plus lisible" par principe ;
- choisir plutot une famille dont le rythme, les ouvertures, la distinction des formes et le comportement ecran sont credibles.

### 2. L'espacement et le comportement du texte comptent fortement
La recherche et les standards d'accessibilite convergent sur un point :
- les utilisateurs doivent pouvoir augmenter interligne, espacement des mots et des lettres sans casser l'interface ;
- un texte trop serre penalise certaines lectures, en particulier pour les profils a basse vision ou en situation de fatigue.

Consequence pour Cadris :
- la famille choisie doit bien tenir avec un interligne genereux ;
- les composants ne doivent pas casser si le texte est agrandi ou espace ;
- le systeme ne doit pas dependre d'un crantage trop serre pour "avoir l'air premium".

### 3. La longueur de ligne et l'alignement influencent fortement le confort
Les recommandations W3C et les systemes publics robustes convergent vers :
- texte principal aligne a gauche ;
- pas de justification sur de longs blocs ;
- lignes idealement contenues autour de 70 a 80 caracteres max ;
- tailles et line-heights adaptes au support et au zoom.

Consequence pour Cadris :
- la typo doit etre jugee dans un systeme complet, pas isolee ;
- une excellente police peut mal performer si elle est posee dans des colonnes trop larges, trop serrees ou justifiees.

### 4. Pour l'ecran, le rythme et la regularite priment souvent sur la "personnalite"
Les retours de conception sur des polices de produit comme Inter montrent bien qu'un dessin trop optimise pour le pixel et les mots courts peut devenir fatigant en lecture longue si le rythme du texte est trop mecanique.

Consequence pour Cadris :
- la police principale doit etre capable de tenir a la fois :
  - des titres de landing ;
  - des blocs de produit denses ;
  - des exports et dossiers longs ;
- il faut eviter les dessins trop condenses, trop monospacises dans le ressenti, ou trop "display".

### 5. Une police hyperlegible peut aider, mais change aussi le ton de marque
Les approches comme Atkinson Hyperlegible renforcent la distinction des caracteres et l'accessibilite.
Mais elles apportent aussi une signature visuelle plus marquee, parfois plus "outil d'accessibilite" que "produit de cadrage expert".

Consequence pour Cadris :
- utile comme piste serieuse ;
- a manipuler avec prudence si l'on veut garder une autorite calme et non une identite "special needs first".

## Sources de travail utilisees

Sources scientifiques et normatives principales :
- W3C, Text Spacing (WCAG 2.2) : https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- W3C, Styling / Line length / Alignment : https://www.w3.org/WAI/tutorials/page-structure/styling/
- W3C, C20 line length : https://www.w3.org/TR/WCAG20-TECHS/C20.html
- GOV.UK Design System, Type scale : https://design-system.service.gov.uk/styles/type-scale/
- GOV.UK Design System, Font override classes : https://design-system.service.gov.uk/styles/font-override-classes/
- PMC, Times New Roman vs Helvetica : https://pmc.ncbi.nlm.nih.gov/articles/PMC9804255/
- PMC, Enhanced Text Spacing : https://pmc.ncbi.nlm.nih.gov/articles/PMC3823704/
- PMC, Systematic review on font size / readability on devices : https://pmc.ncbi.nlm.nih.gov/articles/PMC9376262/

Sources primaires de familles typographiques :
- Inter : https://rsms.me/work/inter/
- Public Sans : https://public-sans.digital.gov/
- IBM Plex : https://www.ibm.com/design/impact/plex/
- Atkinson Hyperlegible Next : https://www.brailleinstitute.org/freefont/

## Traduction pour Cadris

Au vu du message de marque, la typographie principale doit avoir ces proprietes :
- sans serif en base, pour la compatibilite produit et la neutralite de lecture ;
- ouvertures suffisantes ;
- rythme stable sans rigidite excessive ;
- bonne distinction des caracteres ;
- ton plus "structure claire" que "startup brillante" ;
- assez de personnalite pour faire exister `CADRIS.AI`, sans tomber dans le logo avant le logo.

La couche secondaire doit rester une mono fonctionnelle, reservee a :
- statuts ;
- annotations ;
- references ;
- IDs ;
- marqueurs systeme.

## Criteres d'evaluation pour le mot-symbole `CADRIS.AI`

La famille retenue doit bien tenir sur cette chaine :
`CADRIS.AI`

Ce que l'on doit verifier :
- solidite du `C` d'ouverture ;
- stabilite du `A` et du `R` ;
- absence de mollesse dans le `S` final ;
- point avant `AI` bien visible ;
- bonne separation entre `CADRIS` et `.AI` ;
- capitales nettes, sans faire corporate dur.

Ce qu'il faut eviter :
- dessin trop techno froid ;
- all-caps trop administration ;
- rythme trop generique SaaS ;
- formes trop originales qui casseraient la memorisation.

## Pistes typographiques comparees

### Piste A - Public Sans + IBM Plex Mono

#### Impression produite
- forte ;
- neutre ;
- rassurante ;
- civique ;
- structurelle.

#### Pourquoi elle colle au message
`CADRIS.AI donne un cadre` fonctionne tres bien avec Public Sans :
- le mot parait stable ;
- l'ensemble inspire du serieux sans preciosite ;
- la promesse de securisation du projet devient credible tres vite.

#### Avantages
- excellent ton `expert accessible` ;
- forte compatibilite interface / texte / heading ;
- ancrage "service fiable" utile pour Cadris ;
- bonne lecture a differents niveaux d'expertise.

#### Risques
- peut paraitre un peu institutionnelle si la composition est trop rigide ;
- necessite une direction visuelle assez editoriale pour ne pas glisser vers le registre public / admin.

#### Quand la retenir
- si on veut prioriser confiance, clarte, cadre et accessibilite large.

### Piste B - Inter + IBM Plex Mono

#### Impression produite
- produit ;
- numerique ;
- nette ;
- contemporaine ;
- tres ecran.

#### Pourquoi elle colle au message
Inter est tres forte pour la lecture d'interface et les systemes complexes.
Elle rend Cadris tres credible en produit logiciel et tient bien les ecrans denses.

#### Avantages
- tres bon comportement ecran ;
- enorme robustesse pour UI, documentation et dashboards ;
- variable font mature ;
- lecture familiere pour beaucoup d'utilisateurs du numerique.

#### Risques
- peut sembler trop generique dans l'ecosysteme SaaS ;
- moins de densite symbolique immediate pour "donner un cadre" ;
- moins memorisable comme signature de marque pure.

#### Quand la retenir
- si on veut prioriser l'ergonomie produit avant la singularite de marque.

### Piste C - IBM Plex Sans + IBM Plex Mono

#### Impression produite
- technique ;
- methodique ;
- humaine-machinique ;
- structuree ;
- un peu plus distinctive.

#### Pourquoi elle colle au message
Plex porte naturellement l'idee d'un systeme entre humain et machine.
Pour un service qui assume des agents IA sans theatrie, c'est une piste tres coherente.

#### Avantages
- tres forte coherence avec un produit agentique serieux ;
- excellente famille systeme complete ;
- plus de caractere que Inter ;
- plus de profondeur "outillage" que Public Sans.

#### Risques
- peut glisser vers un ton trop ingenierie ou enterprise ;
- demande plus de finesse de composition pour rester accessible aux createurs moins experts.

#### Quand la retenir
- si on veut assumer un peu plus le versant "systeme IA structure" sans perdre la credibilite.

### Piste D - Atkinson Hyperlegible Next + IBM Plex Mono

#### Impression produite
- tres lisible ;
- inclusive ;
- nette ;
- plus demonstrativement accessible.

#### Pourquoi elle colle au message
Elle pousse le plus loin l'idee :
"quel que soit ton niveau, tu dois pouvoir lire, comprendre et agir".

#### Avantages
- forte distinction des caracteres ;
- posture inclusive claire ;
- excellente piste pour des contextes de faible vision ou de lisibilite exigeante.

#### Risques
- tonalite de marque moins premium et moins "architecture editoriale calme" ;
- peut faire basculer Cadris vers une identite d'accessibilite plus que vers une identite de cadrage.

#### Quand la retenir
- plutot en variante accessibilite ou en piste secondaire que comme voix principale de marque.

## Recommandation actuelle

### Recommandation de fond
La litterature ne justifie pas de figer une typo uniquement sur la famille serif/sans.
Elle justifie surtout :
- un systeme flexible ;
- des tailles et interlignes robustes ;
- une bonne longueur de ligne ;
- une police sans effet parasite ;
- une interface qui tient au zoom et a l'espacement.

### Recommandation de marque pour Cadris
Pour le message :
`CADRIS.AI, donne un cadre, c'est fait pour les createurs de projets quel que soit leur niveau, c'est accessible et securisant pour le projet`

la piste principale retenue comme base de travail est :
1. **Public Sans + IBM Plex Mono**

Raison :
- `Public Sans` traduit le mieux l'idee de cadre clair, de fiabilite et d'accessibilite large ;
- elle tient bien un mot-symbole comme `CADRIS.AI` sans tomber dans le registre startup generique ;
- elle reste credible a la fois en landing, en produit et en dossier long ;
- sa licence et son hebergement sont simples a assumer.

Pistes secondaires a conserver comme back-up documente :
- `IBM Plex Sans + IBM Plex Mono` si l'on veut assumer plus tard une voix plus systeme ;
- `Inter + IBM Plex Mono` si la priorite absolue devient l'ergonomie produit pure.

### Choix de travail retenu

Pour construire l'identite visuelle maintenant, la combinaison de travail recommandee est :
- **Public Sans** pour la marque, les titres, le texte et l'interface ;
- **IBM Plex Mono** pour les statuts, metadonnees, references et marqueurs systeme.

Ce choix n'interdit pas un futur ajustement.
Il fixe simplement une base claire pour la suite.

## Regles d'usage stables quel que soit le choix final

### Tailles et hierarchie
- corps principal jamais sous `16px` ;
- base confortable recommandee `17-19px` en produit editorial ;
- interligne corps `1.5` a `1.65` ;
- hierarchie courte et lisible ;
- peu d'ecarts de graisse inutiles.

### Composition textuelle
- alignement a gauche pour le corps ;
- pas de justification sur textes longs ;
- longueur de ligne idealement entre `60` et `80` caracteres ;
- paragraphes aeres ;
- labels courts et explicites.

### Casse et rythme
- phrase case par defaut ;
- all caps reserve aux cas tres courts ou au mot-symbole ;
- mono reservee aux metadonnees ;
- jamais de mono pour le corps de texte.

## Decision de travail a ce stade

Le systeme typographique de Cadris est maintenant fixe, pour la suite du projet, sur :
- **Public Sans** en famille principale ;
- **IBM Plex Mono** en famille secondaire fonctionnelle.

Le dossier conserve :
- `IBM Plex Sans` comme alternative plus systeme ;
- `Inter` comme alternative plus produit ;
- `Atkinson Hyperlegible Next` comme piste accessibilite a utiliser avec prudence.

La validation future ne portera donc plus sur "quelle famille choisir a l'aveugle", mais sur :
- la qualite de composition ;
- la tenue dans le produit ;
- le comportement du wordmark ;
- la coherence globale avec le logo et la palette.
