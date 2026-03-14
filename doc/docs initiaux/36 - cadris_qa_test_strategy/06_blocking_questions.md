# 06_blocking_questions

## Statut general

Aucun bloquant strict n'empeche de transmettre la strategie de test.
Les questions ci-dessous bloquent surtout la transformation de cette strategie en gate de lancement totalement operationnel.

## Questions restantes

### Q-01 - Le lancement cible-t-il strictement la premiere tranche verticale, ou inclut-il deja une branche supplementaire ?

Pourquoi cela bloque :
- les criteres d'acceptation, la checklist et le plan manuel changent fortement si PDF, share links, File Search ou uploads entrent dans le scope.

Ce qu'il faut obtenir pour avancer :
- une phrase de scope explicite pour le lancement ;
- liste des surfaces officiellement hors scope.

Hypothese temporaire :
- lancement borne a `Demarrage` resserre uniquement.

### Q-02 - Quel provider d'auth et quel contrat de session font foi pour staging et production ?

Pourquoi cela bloque :
- le smoke auth et les scenarios d'autorisation ne peuvent pas etre completement figes sans callbacks et session reels.

Ce qu'il faut obtenir pour avancer :
- provider cible ;
- callbacks ;
- duree ou forme minimale de session ;
- compte(s) de test.

### Q-03 - Quel niveau de tests live OpenAI accepte-t-on avant lancement ?

Pourquoi cela bloque :
- sans limite explicite, l'equipe peut soit sous-tester la boucle coeur, soit exploser le cout de validation.

Ce qu'il faut obtenir pour avancer :
- nombre de scenarios live obligatoires ;
- environnement autorise ;
- budget ou plafond simple.

Hypothese temporaire :
- 1 a 2 scenarios live complets sur `staging`, hors PR standard.

### Q-04 - Quel niveau de finition visuelle est obligatoire pour declarer le lancement acceptable ?

Pourquoi cela bloque :
- le lockup logo final et la calibration des badges ne cassent pas la boucle coeur, mais peuvent brouiller le gate final si le niveau de finition n'est pas clarifie.

Ce qu'il faut obtenir pour avancer :
- arbitrage simple sur symbole temporaire vs lockup final ;
- exigence minimale de contraste des badges.

## Decision de travail

Ces questions ne bloquent pas la strategie QA.
Elles bloquent surtout :
- le gate final de lancement ;
- les smoke tests hyper concrets ;
- la decision GO / NO GO publique.
