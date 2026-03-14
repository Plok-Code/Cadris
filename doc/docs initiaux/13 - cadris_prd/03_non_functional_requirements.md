# 03_non_functional_requirements

## Performance attendue si connue
- Aucun SLO chiffre n'est encore fige au niveau MVP.
- En revanche, le produit doit donner des signaux utiles rapidement :
  - qualification de mission lisible ;
  - equipe initiale proposee sans latence excessive ;
  - premiere synthese inter-agents visible tot ;
  - reprise de mission sans recontextualisation longue.

## Securite attendue si connue
- Les informations de projet partagees par l'utilisateur doivent etre traitees comme potentiellement sensibles.
- Les documents, decisions et arbitrages ne doivent pas etre exposes au-dela des personnes et agents autorises.
- Les exports partageables doivent etre controles, tracables et revocables.
- La gestion des secrets, fichiers et traces de mission doit rester compatible avec un produit SaaS serieux.

## Contraintes d'usage
- La mission room doit rester lisible meme si plusieurs agents interviennent.
- Les questions adressees a l'utilisateur doivent etre peu nombreuses, bien groupees et justifiees.
- Les documents doivent etre comprehensibles par plusieurs profils : fondateur, produit, design, technique, business.
- L'utilisateur doit pouvoir reprendre une mission sans devoir relire tout le feed brut.

## Contraintes de qualite et de fiabilite

### NFR-1 - Coherence inter-domaines
Les artefacts produits par differents agents ne doivent pas se contredire sur les points structurants sans reserve explicite.

### NFR-2 - Lisibilite de la cooperation
La collaboration inter-agents doit etre visible de facon intelligible, sans se transformer en bruit conversationnel permanent.

### NFR-3 - Tracabilite
Les hypotheses, issues, escalades, decisions, reviews et exports doivent laisser une trace exploitable.

### NFR-4 - Auditabilite documentaire
Un lecteur doit pouvoir comprendre d'ou vient une affirmation importante : input, decision, message, ou relecture.

### NFR-5 - Maintenabilite
Un pivot ou changement majeur doit permettre de reviser les artefacts impactes sans reconstruire toute la mission.

### NFR-6 - Separation des couches
Le produit doit distinguer clairement :
- la conversation ;
- la memoire partagee ;
- les issues et decisions ;
- les artefacts documentaires ;
- le dossier d'execution exporte.

### NFR-7 - Robustesse des missions longues
Une mission doit pouvoir etre mise en pause, attendre une reponse utilisateur, puis reprendre sans perte de contexte critique.

### NFR-8 - Qualite exploitable
Les livrables ne doivent pas seulement etre bien rediges ; ils doivent etre utilisables pour guider un build humain ou agentique.

### NFR-9 - Transmission
Le dossier doit permettre a une autre equipe de comprendre :
- ce qui est decide ;
- ce qui reste hypothetique ;
- ce qui est bloque ;
- ce qui doit etre verifie ensuite.

## Autres contraintes non fonctionnelles
- Le MVP doit rester compatible avec des projets simples a moyens.
- Les contextes ultra-reglementes ou multi-equipes riches peuvent rester hors noyau MVP.
- Les agents ne doivent pas inventer une certitude absente pour donner une impression de fluidite.
