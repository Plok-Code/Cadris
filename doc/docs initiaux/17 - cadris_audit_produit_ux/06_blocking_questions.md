# 06_blocking_questions

## Questions bloquantes restantes — Audit Produit / UX

Aucune question bloquante restante.

L'audit a été conduit à partir des documents disponibles. Les 4 tensions identifiées ont été arbitrées dans 01_product_coherence_audit.md. Les 5 conditions du verdict GO ont été formulées de manière opérationnelle, sans nécessiter de décision externe.

---

## Points à surveiller par GPT 18 (non bloquants)

Ces points ne bloquent pas la transmission mais méritent attention lors de la conception technique :

### P-01 — Modèle de persistance du registre de certitude
Le registre est mis à jour par bloc (pas en temps réel). La question technique est : comment le registre est-il stocké, et comment les entrées sont-elles liées aux blocs sources ? Une décision d'architecture de données est nécessaire avant implémentation.

### P-02 — Moteur de détection des contradictions
Le service détecte les contradictions entre sous-éléments (ex : cible et proposition de valeur incompatibles). Au MVP, est-ce une détection automatique (logique métier ou IA) ou une détection guidée manuellement par le service ? Ce choix impacte significativement la complexité technique.

### P-03 — Format de sortie préféré par la majorité des utilisateurs
La question ouverte n°6 du PRD (pack markdown, doc structuré, espace partagé) est toujours ouverte. Pour le MVP, implémenter markdown + PDF est raisonnable. Mais si une intégration directe avec un outil externe (Notion, Linear, GitHub) est attendue dès le MVP, c'est un scope additionnel non trivial.

### P-04 — Mécanisme de dialogue guidé : IA ou logique conditionnelle ?
Le modèle "questions → reformulation → validation" implique soit une IA générative capable de reformuler librement, soit une logique conditionnelle plus rigide. Ce choix architectural conditionne l'infrastructure et le coût opérationnel du service.
