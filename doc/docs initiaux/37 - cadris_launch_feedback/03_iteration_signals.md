# 03_iteration_signals

## Principe

Au lancement, Cadris ne doit pas lire trop de signaux.
Il doit suivre :
- quelques signaux de valeur ;
- quelques signaux de friction ;
- quelques signaux de faux positifs.

Avant `n = 10` utilisateurs qualifies, il faut lire surtout :
- des comptes absolus ;
- des motifs repetes ;
- des verbatims convergents.

Apres `n >= 10`, on peut commencer a lire aussi des pourcentages simples.

## Signaux utiles

### S1 - L'utilisateur atteint la premiere vraie question sans aide forte

Interpretation attendue :
- le demarrage, la mission et la synthese sont assez clairs ;
- le produit guide sans necessiter un operateur a chaque etape.

Alerte :
- si 3 utilisateurs qualifies sur les 5 premiers ont besoin d'etre relances ou guides manuellement avant `waiting_user`.

### S2 - La question utile est percue comme legitime

Interpretation attendue :
- la logique multi-agent produit une vraie valeur ;
- la question est comprise comme un accelerateur, pas comme une friction gratuite.

Alerte :
- si plusieurs utilisateurs disent que la question "n'apporte rien" ou "aurait pu etre posee des le debut" ;
- si le rejet de reformulation ou de question depasse durablement ~30%.

### S3 - La reprise apres reponse est fiable

Interpretation attendue :
- la promesse de mission durable tient ;
- le cycle `waiting_user -> resume` est credible.

Alerte :
- un seul bug net de duplication de run ou de perte de contexte est deja un signal grave ;
- deux cas en beta restreinte doivent geler l'ouverture.

### S4 - Le dossier est utilise comme base de travail

Interpretation attendue :
- le produit ne produit pas seulement un effet "waouh" ;
- il genere un actif percu comme utile pour le build.

Signaux positifs :
- l'utilisateur relit le dossier ;
- l'utilisateur l'exporte ou l'utilise pour la suite ;
- l'utilisateur parle de "base", "cadre", "point de depart", "source claire".

Alerte :
- si le dossier est lu mais jamais considere comme assez utile pour continuer ;
- si plusieurs utilisateurs disent "c'est interessant, mais je ne sais pas quoi en faire".

### S5 - Le produit tient sans assistance excessive

Interpretation attendue :
- le lancement peut passer de beta serree a beta elargie.

Alerte :
- si la majorite des sessions necessitent aide humaine active pour finir ;
- si chaque mission doit etre debloquee manuellement.

### S6 - Les demandes hors scope dominent le feedback

Interpretation attendue :
- soit le coeur est deja suffisamment bon et les utilisateurs poussent naturellement la suite ;
- soit le coeur n'est pas encore clair et ils se raccrochent a des extensions visibles.

Alerte :
- si PDF, share links, uploads ou flows secondaires reviennent avant meme que la boucle coeur soit jugee utile ;
- cela peut signaler un manque de valeur immediate sur le coeur.

## Seuils et alertes utiles

### Avant `n = 10`

Lire surtout :
- 3 cas similaires = motif credible ;
- 1 bug auth grave = alerte rouge ;
- 1 bug reprise grave = alerte rouge ;
- 3 utilisateurs sur 5 qui n'atteignent pas le dossier = lancement trop fragile.

### Apres `n >= 10`

Seuils simples reutilisables :
- activation utile : viser > 40%
- completion mission -> dossier : viser > 60%
- friction dialogue : viser < 30% de rejets
- reprise apres abandon : viser > 30% au minimum, > 50% tres sain

## Signaux trompeurs a relativiser

### T1 - Curiosite haute

Exemples :
- beaucoup de clics ;
- reactions positives ;
- essais tres courts.

Pourquoi c'est trompeur :
- ne prouve ni valeur, ni completion, ni retention.

### T2 - Beaucoup d'idees de features

Pourquoi c'est trompeur :
- un utilisateur peut demander plein de choses sans avoir valide le coeur.

### T3 - Un export ou une capture partagee

Pourquoi c'est trompeur :
- cela peut signaler de la curiosite ou de la demonstration, pas un usage durable.

### T4 - Satisfaction declarative seule

Pourquoi c'est trompeur :
- "c'est bien" vaut moins qu'un utilisateur qui revient, repond, finit et build a partir du dossier.

## Decision de travail

Les signaux d'iteration Cadris doivent donc servir a repondre a une seule question :
**est-ce que la boucle coeur est assez utile et assez fiable pour meriter une ouverture un peu plus large ?**
