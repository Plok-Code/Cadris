# 01_design_tokens

## Logique generale

Le design system Cadris doit partir de tokens :
- semantiques avant tout ;
- compacts ;
- reutilisables entre site, produit et dossier ;
- compatibles avec une implementation future sans multiplication d'exceptions.

Regle centrale :
**pas de hardcode visuel dans les composants de V1 si un token existe deja pour l'exprimer**.

## Tokens couleur

### Palette source retenue

| Token source | Hex | Role |
|-------------|-----|------|
| `chalk-0` | `#FBFAF7` | fond principal |
| `chalk-1` | `#F4F1EB` | fond alternatif |
| `limestone` | `#E7E0D5` | surface secondaire |
| `stone` | `#CDC3B3` | bordure douce |
| `slate` | `#6D716C` | texte secondaire |
| `graphite` | `#2E3431` | structure forte |
| `ink` | `#161918` | texte principal |
| `petrol-100` | `#DCE9E8` | fond actif leger |
| `petrol-300` | `#7FA6A8` | trait d'accent secondaire |
| `petrol-500` | `#3F7277` | accent principal |
| `petrol-700` | `#234D52` | accent fort |
| `sage-100` | `#DFE8E0` | fond confirme |
| `sage-600` | `#5E7767` | texte confirme |
| `ochre-100` | `#F1E8D1` | fond hypothese |
| `ochre-600` | `#8C6C2F` | texte hypothese |
| `mist-100` | `#E8ECE9` | fond inconnu |
| `mist-600` | `#66716B` | texte inconnu |
| `brick-100` | `#F2DAD6` | fond bloquant |
| `brick-600` | `#A14B43` | texte bloquant |

### Tokens semantiques recommandes

```css
:root {
  --ds-bg-canvas: #FBFAF7;
  --ds-bg-canvas-alt: #F4F1EB;
  --ds-bg-surface: #E7E0D5;
  --ds-bg-overlay: rgba(22, 25, 24, 0.08);

  --ds-text-primary: #161918;
  --ds-text-strong: #2E3431;
  --ds-text-secondary: #6D716C;
  --ds-text-inverse: #FBFAF7;

  --ds-border-subtle: #CDC3B3;
  --ds-border-default: #B7C2C3;
  --ds-border-strong: #2E3431;

  --ds-accent-soft: #DCE9E8;
  --ds-accent-default: #3F7277;
  --ds-accent-strong: #234D52;

  --ds-status-confirmed-bg: #DFE8E0;
  --ds-status-confirmed-fg: #5E7767;
  --ds-status-hypothesis-bg: #F1E8D1;
  --ds-status-hypothesis-fg: #8C6C2F;
  --ds-status-unknown-bg: #E8ECE9;
  --ds-status-unknown-fg: #66716B;
  --ds-status-blocking-bg: #F2DAD6;
  --ds-status-blocking-fg: #A14B43;

  --ds-feedback-success-bg: #DFE8E0;
  --ds-feedback-success-fg: #5E7767;
  --ds-feedback-warning-bg: #F1E8D1;
  --ds-feedback-warning-fg: #8C6C2F;
  --ds-feedback-error-bg: #F2DAD6;
  --ds-feedback-error-fg: #A14B43;
  --ds-feedback-info-bg: #DCE9E8;
  --ds-feedback-info-fg: #234D52;
}
```

### Regles d'usage couleur

- le texte courant utilise `text-primary` ou `text-strong`, jamais une couleur de statut ;
- l'accent petrol sert aux focus, liens, CTA sobres, etats actifs et progression ;
- les couleurs de statut servent la lecture de l'etat, pas la marque ;
- les fonds de statut restent pale et toujours doubles par un label ;
- le rouge brique n'est jamais une couleur de marque.

## Echelle typographique

### Familles

| Token | Valeur | Usage |
|------|--------|-------|
| `font-family-sans` | `Public Sans, system-ui, sans-serif` | texte, titres, interface |
| `font-family-mono` | `IBM Plex Mono, ui-monospace, monospace` | metadonnees, IDs, statuts systeme |

### Graisses

| Token | Valeur |
|------|--------|
| `font-weight-regular` | `400` |
| `font-weight-medium` | `500` |
| `font-weight-semibold` | `600` |
| `font-weight-bold` | `700` |

### Tailles et interlignes

| Token | Taille | Interligne | Usage |
|------|--------|------------|-------|
| `text-xs` | `12px` | `16px` | meta compacte, labels secondaires |
| `text-sm` | `14px` | `20px` | aides, descriptions courtes |
| `text-md` | `16px` | `24px` | corps interface par defaut |
| `text-lg` | `18px` | `28px` | corps editorial confortable |
| `text-xl` | `20px` | `30px` | sous-titres et cartes majeures |
| `text-2xl` | `24px` | `34px` | titres de section |
| `text-3xl` | `32px` | `40px` | titres d'ecran |
| `text-4xl` | `40px` | `48px` | hero ou page d'entree |

### Regles typo

- corps interface par defaut : `text-md` ;
- lecture longue preferee : `text-lg` ;
- mono reservee a des fragments courts ;
- pas de justification ;
- peu de variations de graisse ;
- label simple d'abord, terme expert en second niveau si utile.

## Espacements

### Echelle de base

| Token | Valeur | Usage |
|------|--------|-------|
| `space-1` | `4px` | micro-separation |
| `space-2` | `8px` | gap compact |
| `space-3` | `12px` | liste dense |
| `space-4` | `16px` | padding standard |
| `space-5` | `24px` | separation de blocs courts |
| `space-6` | `32px` | separation de sections |
| `space-7` | `40px` | respiration forte |
| `space-8` | `48px` | marge ecran principale |
| `space-9` | `64px` | hero, grandes transitions |

### Regles d'usage

- un panneau standard utilise `16-24px` de padding ;
- une grande section separee utilise `32px` minimum ;
- une vue dense ne descend pas sous `12px` de separation d'items.

## Rayons et bordures

### Rayons

| Token | Valeur | Usage |
|------|--------|-------|
| `radius-sm` | `8px` | inputs, badges rectangulaires |
| `radius-md` | `12px` | cartes, panneaux, blocs |
| `radius-lg` | `16px` | grandes surfaces de contenu |
| `radius-pill` | `999px` | pills, chips, tags |

### Bordures

| Token | Valeur | Usage |
|------|--------|-------|
| `border-width-thin` | `1px` | bordure standard |
| `border-width-strong` | `2px` | etat de focus, panneau actif |

## Ombres

La logique Cadris privilegie les bordures et la structure avant l'ombre.

| Token | Valeur | Usage |
|------|--------|-------|
| `shadow-none` | `none` | etat par defaut |
| `shadow-sm` | `0 2px 8px rgba(22, 25, 24, 0.06)` | overlay legere, dropdown |
| `shadow-md` | `0 8px 24px rgba(22, 25, 24, 0.10)` | modal, drawer, couche elevee |

Regle :
- pas d'ombre forte sur les cartes ordinaires ;
- l'ombre sert les elevations rares.

## Tokens de layout utiles

| Token | Valeur | Usage |
|------|--------|-------|
| `layout-max-reading` | `72ch` | lecture de dossier |
| `layout-rail-width` | `320px` | rail contextuel desktop |
| `layout-shell-max` | `1280px` | largeur de travail confortable |
| `layout-touch-target-min` | `44px` | cible interactive mobile |

## Points de vigilance

- ne pas multiplier les tokens de couleur proches pour des cas isoles ;
- ne pas creer une deuxieme palette parallele pour les statuts ;
- ne pas confondre tokens source et tokens semantiques dans les composants ;
- ne pas inventer des ombres plus fortes pour "faire premium" ;
- ne pas casser l'echelle typo avec des tailles arbitraires hors systeme.

## Decision de travail

Le socle de tokens Cadris V1 est :
**semantique, light-first, compact, editorial, et suffisamment strict pour alimenter site, produit et dossier sans catalogue excessif**.
