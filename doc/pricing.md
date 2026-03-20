# Cadris — Pricing

> Chaque cadrage produit 22 documents couvrant stratégie, business, produit, technique et design.

## Free — 0€
- 1 cadrage/mois
- Llama 3.3 (Together AI)
- Export PDF + Claude Code ready (Markdown)

## Starter — 9€/mois
- 5 cadrages/mois
- GPT-4.1
- Export PDF + Claude Code ready

## Pro — 29€/mois
- 10 cadrages/mois
- Claude Opus + GPT-4.1
- Analyse marché Perplexity
- Export PDF + Claude Code ready + PowerPoint

## Expert — 99€/mois
- 20 cadrages/mois
- Meilleurs modèles partout + DeepSearch
- Analyse marché approfondie
- Recherche d'antériorité
- Génération logo + identité visuelle
- Export PDF + Claude Code ready + PowerPoint

---

## Coûts API par mission

| Config | Coût/mission |
|--------|-------------|
| Llama 3.3 (Together AI) | ~$0.024 ≈ 0.02€ |
| GPT-4.1 (11 appels) | ~$0.19 ≈ 0.18€ |
| Opus mixé + Perplexity Sonar | ~$0.69 ≈ 0.64€ |
| Opus partout + DeepSearch + logo | ~$1.60 ≈ 1.48€ |

## Marges par plan

| Plan | Revenu | Coût max | Marge | % |
|------|--------|----------|-------|---|
| Free | 0€ | 0.03€ | -0.03€ | — |
| Starter (5 cadrages) | 9€ | 0.90€ | 8.10€ | 90% |
| Pro (10 cadrages) | 29€ | 6.40€ | 22.60€ | 78% |
| Expert (20 cadrages) | 99€ | 29.60€ | 69.40€ | 70% |

## Modèles IA par plan et par agent

### Free (Llama 3.3 via Together AI) — ✅ IMPLÉMENTÉ ET TESTÉ
- Tous les agents : Llama 3.3 70B via Together AI (OpenAIChatCompletionsModel)
- Pas de critic (skip pour économiser)
- max_tokens=8192 pour éviter troncature JSON
- Documents concis 150-500 mots (qualité instructions "300-500 mots")
- Context 800 chars par doc (vs 1200 pour paid)
- Retry intelligent sur erreurs JSON (prompt "sois plus concis")
- Fallback placeholder si échec total (jamais de doc manquant)
- Test: 3/3 projets, 66/66 documents, 0 erreur, 0 fallback

### Starter (GPT-4.1)
- Tous les agents : GPT-4.1
- Critic : GPT-4.1

### Pro (Opus mixé + Perplexity)
- Strategy : Claude Opus
- Business : Perplexity Sonar (données marché réelles)
- Product Core, Product Specs, Tech Arch, Tech Data, Design, Consolidation : GPT-4.1
- Critic : Claude Opus

### Expert (Meilleurs modèles partout)
- Strategy : Claude Opus
- Business : Perplexity DeepSearch
- Product Core, Product Specs, Tech Arch, Tech Data, Design, Consolidation : Claude Opus
- Critic : Claude Opus
- Logo : Ideogram / DALL-E 3
- Recherche d'antériorité : Perplexity DeepSearch

## Benchmarks marché (mars 2026)
- ChatPRD : 5-24€/mois (PRD generator)
- Gamma / Tome : 10-20€/mois (présentations IA)
- Notion AI : ~10€/add-on
- Lovable : 0 / 25€ / 50€ (app builder)
- Bolt : 0 / 25€ (app builder)
- v0 : 0 / 20€ (UI generator)
