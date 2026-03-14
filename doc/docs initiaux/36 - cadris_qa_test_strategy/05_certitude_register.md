# 05_certitude_register

# Registre de certitude

## Confirme
- la strategie de test doit rester centree sur la premiere tranche verticale `Demarrage` ;
- les flux critiques a proteger sont auth, mission, `waiting_user`, reprise, artefact canonique et dossier markdown ;
- `staging` est l'environnement E2E de reference ;
- les tests utiles sont prioritairement contrats, autorisation, reprise, export markdown et non-regression des statuts ;
- PDF, share links, File Search, uploads et flows secondaires ne font pas partie du gate de lancement retenu.

## Hypotheses de travail
- le lancement vise une mise en ligne limitee du coeur produit, pas un MVP complet etendu.
- Impact : la checklist et les criteres d'acceptation restent compacts et fermes.
- Pourquoi cette hypothese a ete retenue : le handoff final et la tranche verticale recommandee convergent clairement sur ce perimetre.

- le provider d'auth final sera assez simple pour permettre un smoke test complet sans RBAC complexe.
- Impact : les scenarios manuels restent realistes et peu nombreux.
- Pourquoi cette hypothese a ete retenue : les etapes securite et architecture convergent vers un modele owner-first simple en V1.

- un petit nombre de tests live OpenAI sur staging sera acceptable.
- Impact : la strategie combine confiance reelle et cout borne.
- Pourquoi cette hypothese a ete retenue : les attentes de test existantes excluent des tests live exhaustifs sur chaque PR.

## Inconnus
- le toolchain exact du repo et le runner CI final.
- Pourquoi ce point reste inconnu : l'etape engineering a fixe les principes sans fermer tous les outils.
- Quel impact potentiel : la mise en oeuvre precise de certains checks devra etre ajustee.

- le provider d'auth exact, ses callbacks et le contrat de session.
- Pourquoi ce point reste inconnu : ce sujet reste ouvert dans les etapes architecture, securite, infra et handoff final.
- Quel impact potentiel : les tests manuels auth et la checklist de lancement devront etre specialises.

- le niveau exact de live testing externe accepte en cadence normale.
- Pourquoi ce point reste inconnu : il depend du budget, du cout OpenAI et de la discipline de staging.
- Quel impact potentiel : la cadence des smoke tests live peut varier.

- le niveau final de fidelite visuelle impose pour logo et badges au lancement.
- Pourquoi ce point reste inconnu : la finition design reste partiellement ouverte.
- Quel impact potentiel : le gate launch UX peut demander des ajustements de forme sans changer la boucle coeur.

## Bloquants
- aucun bloquant strict n'empeche de transmettre la strategie de test a GPT 37.
- Pourquoi c'est bloquant : non applicable pour la transmission du cadrage QA.
- Ce qu'il faut obtenir pour debloquer : rien pour la transmission ; les inconnus devront etre fermes avant un lancement public plus large.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : la strategie QA est suffisamment fermee pour preparer le lancement du coeur produit, meme si certains choix d'auth, de tooling et de finition visuelle restent ouverts.
