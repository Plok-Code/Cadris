# 08_brand_tokens

## Objectif

Traduire la palette retenue `Mineral petrole` en tokens simples, reutilisables et coherents pour :
- site ;
- produit ;
- documents ;
- usage logo.

## Tokens principaux

```css
:root {
  --cadris-canvas: #FBFAF7;
  --cadris-surface: #E7E0D5;
  --cadris-border: #CDC3B3;
  --cadris-ink: #2E3431;
  --cadris-accent: #3F7277;

  --cadris-canvas-alt: #F4F1EB;
  --cadris-ink-strong: #161918;
  --cadris-ink-soft: #6D716C;
  --cadris-accent-soft: #DCE9E8;
  --cadris-accent-strong: #234D52;

  --cadris-status-ok-bg: #DFE8E0;
  --cadris-status-ok-fg: #5E7767;
  --cadris-status-warn-bg: #F1E8D1;
  --cadris-status-warn-fg: #8C6C2F;
  --cadris-status-neutral-bg: #E8ECE9;
  --cadris-status-neutral-fg: #66716B;
  --cadris-status-danger-bg: #F2DAD6;
  --cadris-status-danger-fg: #A14B43;
}
```

## Usage recommande

### Fonds
- `--cadris-canvas` : fond principal
- `--cadris-canvas-alt` : alternance legere
- `--cadris-surface` : cartes, panneaux, blocs secondaires

### Texte
- `--cadris-ink-strong` : texte principal
- `--cadris-ink` : titres et marque
- `--cadris-ink-soft` : meta, annotations, aides

### Accent
- `--cadris-accent` : liens, focus, CTA sobres
- `--cadris-accent-soft` : fonds actifs doux
- `--cadris-accent-strong` : accent fort, hover, selected

### Statuts
- utiliser les tokens de statut seulement pour :
  - certitude ;
  - progression ;
  - blocage ;
  - validation

Ne pas transformer toute l'identite en systeme multicolore.

## Tokens logo recommandes

```css
:root {
  --cadris-logo-light-bg: #FBFAF7;
  --cadris-logo-light-fg: #2E3431;
  --cadris-logo-dark-bg: #2E3431;
  --cadris-logo-dark-fg: #FBFAF7;
  --cadris-logo-accent: #3F7277;
}
```

## Regles simples

- logo principal sur fond clair : `--cadris-logo-light-fg`
- logo principal sur fond fonce : `--cadris-logo-dark-fg`
- accent petrol reserve au symbole ou a des usages choisis, pas obligatoire partout
- ne pas poser le logo petrole sur `Limestone` si le contraste semble mou

## Decision de travail

La palette `Mineral petrole` est maintenant traduite en tokens simples, directement reutilisables pour un site ou un systeme produit.
