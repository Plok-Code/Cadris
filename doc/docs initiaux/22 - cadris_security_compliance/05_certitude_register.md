# 05_certitude_register

# Registre de certitude

## Confirmé
- Cadris manipule des informations de projet, des documents utilisateur, des arbitrages, des exports et des traces de runs.
- Ces informations doivent etre traitees comme potentiellement sensibles.
- Les exports partageables doivent etre controles, tracables et revocables.
- Le MVP reste hors contextes ultra-reglementes et hors conformite lourde.
- Les permissions complexes et les roles avances sont explicitement exclus du MVP.
- Le modele V1 est oriente mono-utilisateur par projet, avec partage externe par lien comme hypothese de travail forte.
- La base canonique est PostgreSQL, les binaires vivent en S3, et File Search sert le retrieval V1.
- PostHog ne doit pas recevoir de contenu utilisateur.
- La suppression et la retention deviennent des sujets critiques a cause du couple `Postgres + S3 + File Search + traces + analytics`.
- L'auth/tenancy, le mode de validation des documents sensibles et la politique de partage restent ouverts.

## Hypothèses de travail
- H1 - La V1 fonctionnera avec un controle d'acces simple : proprietaire de projet, destinataire de share link, comptes techniques, acces operateur exceptionnel.
- Impact : permet une securite nette sans introduire un RBAC lourd ; si faux, toute la couche permissions devra etre redecoupee.
- Pourquoi cette hypothese a ete retenue : les documents amont excluent les permissions complexes et la collaboration riche.

- H2 - Le RGPD est probablement la base de conformite la plus plausible a court terme.
- Impact : impose transparence, minimisation analytics, retention, suppression et documentation des sous-traitants ; si faux, le cadrage devra etre ajuste a d'autres juridictions.
- Pourquoi cette hypothese a ete retenue : les exigences analytics mentionnent explicitement le RGPD et le projet manipule des donnees personnelles et documentaires.

- H3 - Les share links doivent etre consideres comme un mecanisme de diffusion sensible, pas comme une commodite produit secondaire.
- Impact : pousse a imposer revocation, tracabilite et restriction au snapshot ; si faux, le principal risque de fuite V1 serait sous-estime.
- Pourquoi cette hypothese a ete retenue : le PRD et les contraintes de donnees insistent deja sur le caractere controle et immuable des exports.

- H4 - Les traces et journaux sont un risque aussi important que la base principale.
- Impact : exige hygiene des logs et retention documentee ; si faux, des fuites pourraient survenir hors des surfaces produit visibles.
- Pourquoi cette hypothese a ete retenue : le runtime agentique, OpenAI tracing et PostHog multiplient les points de sortie possibles de la donnee.

## Inconnus
- I1 - Le provider exact d'authentification et le modele final de tenancy ne sont pas fixes.
- Pourquoi ce point reste inconnu : l'etape 21 l'a laisse ouvert.
- Quel impact potentiel : controles d'acces, structure du schema, partage, journaux de connexion, experience utilisateur.

- I2 - La politique exacte de retention et de suppression par systeme n'est pas definie.
- Pourquoi ce point reste inconnu : la chaine mentionne le risque, mais ne fixe ni duree ni mecanisme de purge.
- Quel impact potentiel : risque de non-conformite, suppression incomplète, perte de confiance client.

- I3 - Le regime juridique exact cible au lancement n'est pas formellement tranche.
- Pourquoi ce point reste inconnu : le projet ne fixe pas encore ses juridictions prioritaires.
- Quel impact potentiel : cookies/analytics, documents juridiques, DPA, pseudonymisation, droits utilisateurs.

- I4 - La politique exacte des share links n'est pas detaillee.
- Pourquoi ce point reste inconnu : on sait qu'ils doivent etre revocables, mais pas encore s'ils expirent par defaut ni quel niveau de journalisation est impose.
- Quel impact potentiel : risque de fuite externe, mauvaise interpretation du produit, exposition durable d'un dossier.

- I5 - La surface finale du build review et des traces associees n'est pas complete.
- Pourquoi ce point reste inconnu : texte + captures sont recommandes, mais l'ouverture a des logs, diffs ou sorties CI reste possible plus tard.
- Quel impact potentiel : sensibilite des donnees traitees, retention, besoins de cloisonnement supplementaires.

## Bloquants
- B1 - Le modele exact d'auth/tenancy V1 n'est pas tranche.
- Pourquoi c'est bloquant : il conditionne toute la strategie d'acces et la solidite de l'autorisation serveur.
- Ce qu'il faut obtenir pour debloquer : une decision explicite entre mono-utilisateur strict, partage par lien seulement, ou organisation minimale.

- B2 - La politique de retention/suppression transverse n'est pas definie.
- Pourquoi c'est bloquant : sans elle, la posture de confidentialite et la conformite restent inachevees.
- Ce qu'il faut obtenir pour debloquer : une table simple par systeme `Postgres / S3 / File Search / traces / analytics`.

- B3 - La politique exacte des share links n'est pas fixee.
- Pourquoi c'est bloquant : le lien partageable est la principale surface d'exposition externe du MVP.
- Ce qu'il faut obtenir pour debloquer : regles de revocation, duree de vie, journalisation et contenu expose.

- B4 - Le cadre juridique prioritaire du lancement n'est pas explicite.
- Pourquoi c'est bloquant : il change le niveau d'exigence sur consentement analytics, documents contractuels et traitement des demandes.
- Ce qu'il faut obtenir pour debloquer : au minimum la liste des juridictions cibles du lancement.

## Statut de transmission
- Transmission autorisée : Oui sous hypothèses
- Raison : la securite minimale V1 et les risques majeurs sont identifiables, mais les points B1 a B4 doivent etre fixes pour finaliser la posture d'acces et de conformite.
