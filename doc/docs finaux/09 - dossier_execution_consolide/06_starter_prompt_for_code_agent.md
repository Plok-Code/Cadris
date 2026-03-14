# Starter prompt for code agent

Tu travailles sur Cadris.

Lis d'abord, dans cet ordre :
1. `doc/docs finaux/00 - dossier_canonique/01_authority_order.md`
2. `doc/docs finaux/00 - dossier_canonique/02_default_build_decisions.md`
3. `doc/docs finaux/09 - dossier_execution_consolide/02_build_brief_for_codex.md`
4. `doc/docs finaux/02 - cadrage_produit/02_prd_global.md`
5. `doc/docs finaux/04 - technique/01_architecture.md`
6. `doc/docs finaux/04 - technique/03_data_model.md`
7. `doc/docs finaux/04 - technique/04_api_specification.md`
8. `doc/docs finaux/07 - execution/01_implementation_plan.md`
9. `doc/docs finaux/07 - execution/02_testing_and_acceptance.md`

Regles a respecter :
- construire du canonique vers le rendu
- ne jamais faire parler le web directement a Postgres, OpenAI, S3 ou Restate
- ne jamais traiter le markdown comme source de verite
- ne jamais etendre le scope avant stabilite de `Demarrage`
- garder une seule zone dominante par ecran
- utiliser les statuts canoniques

Ordre de travail :
1. verifier l'existant
2. prendre le plus petit lot utile suivant l'ordre canonique
3. implementer
4. verifier
5. documenter les ecarts si necessaire

Si un point est encore ouvert :
- applique les defaults du dossier canonique
- n'arrete pas le build pour un detail non critique
- n'invente pas un nouveau produit

Premier objectif :
garantir une tranche verticale complete `projet -> mission Demarrage -> question -> reponse -> dossier markdown`.

