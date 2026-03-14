# 06_blocking_questions

## Questions restantes

### Q-01 - Souhaite-t-on un dark mode en V1 ?
- Pourquoi cela reste ouvert : le systeme de couleur fonctionne deja en light-first, mais un dark mode impliquerait une seconde matrice de contrastes, surfaces et statuts.
- Ce qu'il faut obtenir pour avancer : une decision entre `non en V1`, `plus tard`, ou `oui des maintenant`.
- Hypothese temporaire : `plus tard`.

### Q-02 - Quel est le perimetre prioritaire du set d'icones ?
- Pourquoi cela reste ouvert : le style est defini, mais pas encore le volume ni la priorite de production.
- Ce qu'il faut obtenir pour avancer : une liste courte d'usages critiques : navigation, certitude, progression, export, partage, blocage, validation.
- Hypothese temporaire : set minimal centre produit.

### Q-03 - Le logo doit-il rester d'abord monochrome ou disposer aussi d'une version petrol par defaut ?
- Pourquoi cela reste ouvert : la palette est validee, mais le meilleur usage du logo entre noir/blanc master et variante accent n'est pas encore normalise.
- Ce qu'il faut obtenir pour avancer : une regle simple d'usage entre `master monochrome seulement` ou `master monochrome + variante petrol`.
- Hypothese temporaire : `master monochrome + usage couleur optionnel`.

## Pourquoi ces points restent importants

- Q-01 conditionne l'extension reelle de la palette.
- Q-02 conditionne la production concrete du langage iconographique.
- Q-03 conditionne la normalisation du pack logo.

## Priorite recommandee

1. arbitrage dark mode ;
2. inventaire prioritaire des icones ;
3. normalisation de la variante couleur du logo.

## Statut

- Bloquant pour definir le systeme visuel : non.
- Bloquant pour commencer une implementation : non.
- Bloquant seulement pour industrialisation haute fidelite complete : partiellement.
- Transmission autorisee vers GPT 27 : oui.
