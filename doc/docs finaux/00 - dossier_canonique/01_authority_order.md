# Ordre d'autorite

## Regle generale

Quand deux documents semblent diverger, l'ordre d'autorite est :

1. `doc/docs finaux/09 - dossier_execution_consolide/02_build_brief_for_codex.md`
2. `doc/docs finaux/00 - dossier_canonique/02_default_build_decisions.md`
3. `doc/docs finaux/02 - cadrage_produit/*.md`
4. `doc/docs finaux/04 - technique/*.md`
5. `doc/docs finaux/03 - ux_ui/*.md`
6. `doc/docs finaux/07 - execution/*.md`
7. `doc/docs initiaux/35 - cadris_codex_handoff/*.md`
8. le reste des `doc/docs initiaux`

## Regles de precedence

- Le dossier final prime sur les docs amont si une formulation est plus ancienne.
- Les codes machine priment sur les labels marketing.
- Les contraintes de securite et d'autorisation priment sur une commodite UI.
- Le canonique `PostgreSQL = verite metier` prime sur tout shortcut local.
- La premiere tranche verticale `Demarrage` prime sur les flows secondaires.

## Regle en cas de silence

Si aucune doc ne tranche explicitement un point :
- appliquer les decisions par defaut ;
- choisir l'option la plus simple compatible avec l'architecture retenue ;
- ne pas etendre le scope ;
- conserver un point d'extension visible.

