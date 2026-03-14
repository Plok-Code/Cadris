# 02_color_system

## Statut de palette

Palette retenue et validee :
**Mineral petrole**

Base validee :
- `#FBFAF7`
- `#E7E0D5`
- `#CDC3B3`
- `#2E3431`
- `#3F7277`

Lecture de marque :
- sobre ;
- structuree ;
- serieuse ;
- rassurante ;
- alignee avec Cadris.

## Logique generale

La couleur chez Cadris doit servir quatre choses :
- la lisibilite ;
- la structure ;
- la priorisation ;
- les statuts.

La palette est donc volontairement contenue :
- une base neutre minerale ;
- un accent principal maitrise ;
- un petit systeme de statuts ;
- un usage restreint des couleurs de soutien.

## Palette principale

### Neutres de base

| Nom | Hex | Role principal |
|-----|-----|----------------|
| Chalk 0 | `#FBFAF7` | fond principal, respiration |
| Chalk 1 | `#F4F1EB` | variante de fond legerement plus chaude |
| Limestone | `#E7E0D5` | surfaces secondaires, panneaux, cartes |
| Stone | `#CDC3B3` | bordures, trames, separateurs doux |
| Slate | `#6D716C` | texte secondaire, meta, annotations |
| Graphite | `#2E3431` | titres secondaires, UI forte, logo sombre |
| Ink | `#161918` | texte principal, contraste maximal |

### Accent principal de marque

| Nom | Hex | Role principal |
|-----|-----|----------------|
| Petrol 100 | `#DCE9E8` | fonds actifs legers, surlignage discret |
| Petrol 300 | `#7FA6A8` | traits de structure secondaires |
| Petrol 500 | `#3F7277` | accent principal valide, liens, etats actifs |
| Petrol 700 | `#234D52` | accents forts, CTA sobres, titres ponctuels |

## Palette de statuts

### Confirme / complet / valide
| Nom | Hex | Usage |
|-----|-----|-------|
| Sage 100 | `#DFE8E0` | fond de signal faible |
| Sage 600 | `#5E7767` | icone, label, statut confirme |

### Hypothese / attention moderee / sujet a confirmer
| Nom | Hex | Usage |
|-----|-----|-------|
| Ochre 100 | `#F1E8D1` | fond faible |
| Ochre 600 | `#8C6C2F` | label, puce, alerte moderee |

### Inconnu / non tranche / neutre
| Nom | Hex | Usage |
|-----|-----|-------|
| Mist 100 | `#E8ECE9` | fond de statut neutre |
| Mist 600 | `#66716B` | label, icone, repere neutre |

### Bloquant / reserve forte / erreur critique
| Nom | Hex | Usage |
|-----|-----|-------|
| Brick 100 | `#F2DAD6` | fond faible |
| Brick 600 | `#A14B43` | alerte forte, bloquant, reserve critique |

## Palette secondaire

Une palette secondaire tres reduite peut exister pour les illustrations ou les schemas, mais elle ne doit jamais concurrencer la palette retenue :
- `Sand` `#EFE7DB` pour plans de fond chaleureux ;
- `Steel` `#B7C2C3` pour liaisons ou couches secondaires ;
- `Forest Ink` `#31443C` pour profondeur ponctuelle.

Elle reste strictement de soutien.

## Roles des couleurs

### Fonds
- `Chalk 0` porte le fond principal de marque et de produit.
- `Chalk 1` sert de variation douce si une difference de plan est necessaire.
- `Limestone` sert a separer une zone, un panneau ou une famille de contenu.
- les fonds Petrol, Sage, Ochre et Brick restent legers et ponctuels.

### Texte
- `Ink` pour le texte principal ;
- `Graphite` pour les sous-titres et elements structurants ;
- `Slate` pour meta-informations, aides et annotations.

### Bordures et trames
- `Stone` pour les bordures ordinaires ;
- `Petrol 300` pour une structure mise en avant ;
- `Mist 600` pour les reperes neutres.

### Accent de marque
- `Petrol 500` est l'accent principal de l'identite ;
- `Petrol 700` sert aux moments de contraste plus fort ;
- elles servent les points de focus, liens, CTA sobres, activations et marqueurs de progression.

### Statuts
- `Sage` pour ce qui est confirme, suffisant, valide ;
- `Ochre` pour hypothese ou sujet a verifier ;
- `Mist` pour inconnu ou neutre non critique ;
- `Brick` pour bloquant ou alerte forte.

## Derives utiles a partir de la palette validee

Pour construire l'identite visuelle sans sortir de la palette retenue, les derives suivants sont recommandes :

| Token derive | Hex | Usage |
|-------------|-----|-------|
| Petrol Soft | `#DCE9E8` | fond d'accent tres leger |
| Petrol Deep | `#234D52` | accent fort, hover, focus |
| Graphite Soft | `#4B514D` | texte secondaire fort |
| Chalk Warm | `#F4F1EB` | alternance de surface |

## Contrastes et points de vigilance

### Regles minimales
- toujours privilegier `Ink` ou `Graphite` sur les fonds clairs ;
- ne pas utiliser `Petrol 500`, `Sage 600`, `Ochre 600` ou `Brick 600` comme couleur de long paragraphe ;
- les fonds de statut doivent rester pales, avec texte sombre ;
- les codes couleur doivent toujours etre doubles par un mot ou une icone.

### Ce qu'il faut eviter
- accent petrol sur toutes les sections ;
- multiplications de tints proches impossibles a distinguer ;
- usage du rouge brique comme couleur de marque ;
- usage de l'ocre comme "warning" permanent qui fatiguerait l'interface ;
- fond trop blanc clinique sans nuances minerales.

## Usage recommande par ratio

Sur une page ou un ecran type :
- 70 a 80 % de neutres ;
- 10 a 15 % de structure secondaire ;
- 5 a 10 % d'accent ou de statuts.

## Usage logo avec la palette validee

Le logo peut rester d'abord :
- en noir / graphite sur fond clair ;
- en blanc / chalk sur fond fonce ;
- en version petrole si la lecture reste nette.

Recommandation :
- garder un **master monochrome** ;
- utiliser la palette surtout pour l'environnement de marque ;
- n'utiliser la version couleur du logo que si elle ajoute une valeur claire.

## Decision de travail

La palette Cadris retenue est :
- claire d'abord ;
- minerale ;
- ancree dans les neutres ;
- structuree par un petrol maitrise ;
- completee par des statuts simples et lisibles.
