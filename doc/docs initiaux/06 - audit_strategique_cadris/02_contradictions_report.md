# Rapport de contradictions stratégiques

## Objet
Ce document liste les contradictions, tensions et fragilités stratégiques observées.
Il ne cherche pas à tout résoudre.
Il cherche à montrer :
- ce qui est contradictoire ;
- pourquoi cela compte ;
- l’impact potentiel ;
- la correction minimale recommandée.

## Contradiction 1 — Ancien modèle crédits vs modèle cible projet actif
### Description
Les premiers documents décrivent une logique de crédits visible.
Les documents business plus récents recommandent au contraire :
- projet actif ;
- logiciel récurrent ;
- logique hybride possible ;
- crédits relégués au rang d’hypothèse historique.

### Pourquoi c’est une contradiction
Le projet ne peut pas raconter en même temps :
- “je vends des crédits”
et
- “je vends la maîtrise continue d’un projet actif”

Ces deux logiques n’ancrent pas la valeur au même endroit.

### Impact potentiel
- confusion interne sur la monétisation ;
- confusion externe sur ce qui est acheté ;
- architecture de pricing incohérente ;
- risque de rebricoler plus tard la logique produit pour servir le pricing.

### Correction minimale recommandée
Acter explicitement :
- **modèle crédits = historique**
- **modèle cible = projet actif / continuité / logique hybride compatible**

## Contradiction 2 — Abonnement mensuel recommandé vs fréquence d’usage non encore prouvée
### Description
Les documents de revenue et pricing poussent vers le mensuel ancré sur le projet actif.
Mais les unit economics disent :
- usage par pics ;
- fréquence non uniforme ;
- support potentiellement élevé ;
- risque d’un flat trop généreux.

### Pourquoi c’est une contradiction
Un abonnement mensuel suppose une certaine régularité de valeur et une maîtrise minimale du coût moyen.
Or ces deux points ne sont pas encore suffisamment validés.

### Impact potentiel
- mauvaise marge ;
- churn si la valeur est perçue comme trop ponctuelle ;
- sous-pricing de gros utilisateurs ;
- sur-pricing de petits utilisateurs.

### Correction minimale recommandée
Ne pas verrouiller un “mensuel pur illimité”.
Garder explicitement ouverte une forme :
- projet actif borné ;
- ou hybride compatible ;
- avec mesure rapide de fréquence, revisites, coût IA et support.

## Contradiction 3 — Dossier exportable vendu à l’entrée vs continuité comme moteur économique
### Description
Les documents disent en même temps :
- le plus monétisable au départ est le dossier canonique exportable ;
- la profondeur économique vient ensuite de la continuité.

### Pourquoi c’est une tension
La valeur la plus vite comprise n’est pas forcément la valeur qui retient le mieux.
Le produit peut donc être bien acheté au départ mais mal retenu ensuite.

### Impact potentiel
- bon intérêt initial mais rétention faible ;
- confusion roadmap ;
- marketing tourné vers le one-shot alors que l’économie attend du récurrent.

### Correction minimale recommandée
Fixer une lecture simple :
- **façade d’entrée = artefact concret**
- **économie long terme = continuité**
et demander au GPT suivant de traiter cette dualité avec prudence.

## Contradiction 4 — Besoin profond de cohérence vs marché dominé par la vitesse
### Description
Le marché applaudit la vitesse de prototypage.
Cadris se différencie sur :
- cohérence ;
- mémoire ;
- contrôle ;
- transmission.

### Pourquoi c’est une tension
Le produit attaque un vrai besoin, mais pas forcément le besoin que le marché formule spontanément en premier.

### Impact potentiel
- difficulté de messaging ;
- comparaison défavorable avec les builders rapides ;
- objection “je peux déjà faire ça avec mes outils”.

### Correction minimale recommandée
Rattacher toujours la promesse à des coûts subis concrets :
- éviter le rebuild ;
- modifier sans casser ;
- reprendre sans se reperdre ;
- transmettre sans recontextualiser.

## Contradiction 5 — Cible déjà clarifiée, mais wedge exact encore trop large
### Description
La cible générale est devenue assez claire.
Mais “vrai SaaS” reste trop large sans cas inclus / exclus plus précis.

### Pourquoi c’est une contradiction
Le projet a un discours de focus, mais pas encore une frontière de wedge assez nette pour un lancement très clair.

### Impact potentiel
- onboarding trop ouvert ;
- objections de scope ;
- difficulté à produire un message très concret ;
- dérive produit.

### Correction minimale recommandée
Fixer explicitement :
- 3 cas inclus ;
- 3 cas exclus ;
- un niveau de complexité acceptable ;
- une frontière avant-code fort / pendant-build léger.

## Contradiction 6 — Profondeur documentaire comme force vs profondeur documentaire comme friction
### Description
La profondeur documentaire est traitée comme un levier de valeur.
Mais plusieurs documents reconnaissent le risque :
- “plus de doc” sans gain clair ;
- surcharge ;
- besoin d’éducation support.

### Pourquoi c’est une tension
Ce qui différencie le produit peut aussi ralentir l’achat et l’usage.

### Impact potentiel
- onboarding trop lourd ;
- support trop élevé ;
- rejet par les builders qui veulent garder de la vitesse.

### Correction minimale recommandée
Définir :
- le minimum crédible ;
- le niveau premium ;
- la sortie la plus actionnable ;
- ce que la V1 ne produit pas encore.

## Contradiction 7 — Segment post-Lovable séduisant vs preuve acheteur insuffisante
### Description
Le post-Lovable / post-builder bloqué revient comme sous-segment prometteur.
Mais il est explicitement noté comme encore à valider.

### Pourquoi c’est une contradiction
Le projet risque de commencer à se raconter autour d’un segment qui n’est pas encore prouvé comme acheteur.

### Impact potentiel
- wording trop dépendant d’un angle fragile ;
- ciblage marketing biaisé ;
- mauvaises priorités de recherche.

### Correction minimale recommandée
Garder ce segment comme hypothèse de travail, pas comme certitude.
Le GPT suivant doit le traiter avec prudence tant que la preuve terrain manque.

## Contradiction 8 — Ambition de forte couverture documentaire vs discipline MVP
### Description
Les premiers documents parlaient de couverture SaaS très profonde.
Les documents plus récents disciplinent davantage :
- cas simples à moyens ;
- avant-code fort ;
- continuité légère ;
- pas d’enterprise ;
- pas de build autonome fort.

### Pourquoi c’est une tension
Le projet a encore des traces d’ambition large alors que la V1 utile exige un scope plus étroit.

### Impact potentiel
- surcharge produit ;
- attentes trop élevées ;
- incohérence entre landing, expérience et valeur réelle.

### Correction minimale recommandée
Faire primer les documents de scope, MVP, business rules et PRD récents sur les formulations plus totalisantes des documents amont.

## Contradiction 9 — Pricing souhaité lisible vs prix encore non prouvés
### Description
Les documents imposent un pricing lisible, concret et rassurant.
Mais le corridor de prix acceptable est explicitement encore inconnu.

### Pourquoi c’est une tension
La structure du pricing est plus claire que les montants eux-mêmes.

### Impact potentiel
- affichage trop tôt d’un prix arbitraire ;
- ancrage faux ;
- perception de sur-prix ou de sous-prix.

### Correction minimale recommandée
Ne pas figer de montant définitif dans la doctrine stratégique.
Garder la décision prix comme validation terrain à court terme.

## Contradiction 10 — Produit logiciel vs risque de glisser vers service caché
### Description
Le projet refuse l’étiquette de service ou de conseil déguisé.
Mais l’aide au cadrage, à la profondeur et à la compréhension peut pousser vers beaucoup de support.

### Pourquoi c’est une tension
Plus le produit doit expliquer et accompagner, plus il peut ressembler à un service dans son coût réel.

### Impact potentiel
- marge dégradée ;
- charge support imprévue ;
- difficulté à tenir un modèle software léger.

### Correction minimale recommandée
Définir strictement :
- ce qui est inclus produit ;
- ce qui n’est pas promis ;
- ce qui doit rester borné dans la V1.

## Synthèse des contradictions principales
### Contradictions les plus critiques
1. crédits historique vs projet actif cible ;
2. abonnement mensuel vs fréquence/coût encore non prouvés ;
3. livrable ponctuel vs continuité récurrente ;
4. wedge encore trop large ;
5. profondeur documentaire comme force et comme friction.

## Lecture finale
Ces contradictions ne rendent pas le projet incohérent au point de bloquer toute transmission.
Elles indiquent surtout que :
- le noyau stratégique tient ;
- mais l’histoire d’offre et d’économie doit encore être clarifiée.

## Statut
**Contradictions réelles mais traitables.**
Elles justifient un verdict :
**GO sous hypothèses** et non **GO net**.
