# Guides v3 Migration Notes

> Temporary working doc. Will be deleted before merging.

Branch: `docs/guides-v3`
Goal: Full docs restructure per Diátaxis framework; refocus narrative on "data service".

## Top-level Tabs

| Old | New |
|-----|-----|
| Guides | **Docs** (merged with Playbooks) |
| Playbooks | removed (contents → Docs/Tutorials + Docs/Recipes) |
| API Reference | API Reference (internal reorg) |
| GraphQL | GraphQL (unchanged) |
| SDKs | SDKs (unchanged) |
| — | **Changelog** (new top-level tab) |

## Docs Sidebar — Path Mapping

### Top (ungrouped)
- `{lang}/guides/getting-started/overview` → `{lang}/docs/home` (full rewrite)
- `{lang}/guides/getting-started/quickstart` → `{lang}/docs/quickstart`
- `{lang}/guides/getting-started/supported-chains` → `{lang}/docs/supported-chains`

### Data Products (NEW)
All new pages:
- `{lang}/docs/data-products/overview`
- `{lang}/docs/data-products/tokens`
- `{lang}/docs/data-products/trades`
- `{lang}/docs/data-products/wallets`
- `{lang}/docs/data-products/dex-pools`
- `{lang}/docs/data-products/rankings`
- `{lang}/docs/data-products/candles-ohlc`
- `{lang}/docs/data-products/holders`
- `{lang}/docs/data-products/smart-money` ← migrated from `{lang}/guides/data-concepts/smart-money-methodology`
- `{lang}/docs/data-products/blockchain-core`
- `{lang}/docs/data-products/data-freshness`

### Access Methods (NEW)
- `{lang}/docs/access-methods/overview` ← merged from `{lang}/guides/getting-started/api-comparison`
- `{lang}/docs/access-methods/rest-api` (new)
- `{lang}/docs/access-methods/graphql` (new)
- `{lang}/docs/access-methods/websocket` ← from `{lang}/guides/data-concepts/realtime-streaming`
- `{lang}/docs/access-methods/kafka-streams/overview` ← from `{lang}/guides/data-concepts/kafka-streams/overview`
- `{lang}/docs/access-methods/kafka-streams/evm-streams` ← from same path
- `{lang}/docs/access-methods/kafka-streams/solana-streams` ← from same path
- `{lang}/docs/access-methods/kafka-streams/tron-streams` ← from same path
- `{lang}/docs/access-methods/sdks` (new)
- `{lang}/docs/access-methods/cli` (new)

### AI Agents (renamed from AI Infrastructure)
- `{lang}/docs/ai-agents/overview` ← from `{lang}/guides/ai-infrastructure/overview`
- `{lang}/docs/ai-agents/mcp-server/introduction` ← from same path
- `{lang}/docs/ai-agents/mcp-server/setup` ← merged: setup-guide + self-hosted-installation + stdio-transport + prompts-and-resources
- `{lang}/docs/ai-agents/mcp-server/tools` ← merged: tools-catalog + tools-reference
- `{lang}/docs/ai-agents/agent-skills/introduction` ← from same path
- `{lang}/docs/ai-agents/agent-skills/installation` ← from same path
- `{lang}/docs/ai-agents/agent-skills/chainstream-data` ← from same path
- `{lang}/docs/ai-agents/agent-skills/chainstream-defi` ← from same path

### Compliance (promoted)
- `{lang}/docs/compliance/overview` ← merged: `{lang}/guides/security-compliance/overview` + `compliance-integration` (overview portion)
- `{lang}/docs/compliance/kyt-concepts` ← from `{lang}/guides/data-concepts/kyt-concepts`
- `{lang}/docs/compliance/kya-concepts` ← from `{lang}/guides/data-concepts/kya-concepts`
- `{lang}/docs/compliance/integration-guide` ← from `{lang}/guides/data-concepts/compliance-integration`

### Tutorials (from Playbooks/tutorials)
- `{lang}/docs/tutorials/smart-money-tracker`
- `{lang}/docs/tutorials/build-price-alert-bot`
- `{lang}/docs/tutorials/build-arbitrage-scanner`
- `{lang}/docs/tutorials/integrate-deposit-check`
- `{lang}/docs/tutorials/ai-agent-with-mcp`

### Recipes (from Playbooks/frameworks + protocols)
- `{lang}/docs/recipes/token-analysis-framework`
- `{lang}/docs/recipes/defi-monitoring-overview`
- `{lang}/docs/recipes/webhook-fundamentals`
- `{lang}/docs/recipes/pump-fun`
- `{lang}/docs/recipes/raydium`

### Platform (NEW)
- `{lang}/docs/platform/authentication/api-keys-oauth` ← from `{lang}/guides/getting-started/authentication`
- `{lang}/docs/platform/authentication/wallet-auth-siwx` ← from `{lang}/guides/getting-started/wallet-auth-siwx`
- `{lang}/docs/platform/billing-payments/plans-and-units` ← from `{lang}/guides/getting-started/billing-and-units`
- `{lang}/docs/platform/billing-payments/x402-payments` ← from `{lang}/guides/getting-started/x402-payments` + `{lang}/guides/cli/x402-payment`
- `{lang}/docs/platform/billing-payments/mpp-payments` ← from `{lang}/guides/getting-started/mpp-payments`
- `{lang}/docs/platform/security/api-security` ← from `{lang}/guides/data-concepts/api-security`
- `{lang}/docs/platform/security/data-privacy` ← from `{lang}/guides/data-concepts/data-privacy`

### Ecosystem (renamed from Integrations)
- `{lang}/docs/ecosystem/openclaw/overview` ← from `{lang}/guides/integrations/openclaw/overview`
- `{lang}/docs/ecosystem/openclaw/skills-install` ← from same path
- `{lang}/docs/ecosystem/openclaw/cross-agent-compatibility` ← from same path
- `{lang}/docs/ecosystem/openclaw/security` ← from same path
- `{lang}/docs/ecosystem/n8n/overview` ← from `{lang}/guides/integrations/n8n/overview`
- `{lang}/docs/ecosystem/n8n/trigger-node` ← from same path

### Reference
- `{lang}/docs/reference/glossary` ← from `{lang}/guides/resources/glossary`
- `{lang}/docs/reference/error-codes` ← from `{lang}/guides/resources/error-codes`
- `{lang}/docs/reference/faq` ← from `{lang}/guides/getting-started/faq`

## Deletions

Pages to delete (content merged elsewhere):
- `{lang}/guides/getting-started/choosing-your-path` — redundant with Home/Quickstart next-steps
- `{lang}/guides/getting-started/api-comparison` — merged into Access Methods Overview
- `{lang}/guides/cli/overview` — content fed into new `{lang}/docs/access-methods/cli`
- `{lang}/guides/cli/authentication` — redirect to `{lang}/docs/platform/authentication/api-keys-oauth`
- `{lang}/guides/cli/commands` — promoted to API Reference CLI Commands Reference
- `{lang}/guides/cli/x402-payment` — merged into `{lang}/docs/platform/billing-payments/x402-payments`
- `{lang}/guides/ai-infrastructure/mcp-server/self-hosted-installation` — merged into setup
- `{lang}/guides/ai-infrastructure/mcp-server/stdio-transport` — merged into setup
- `{lang}/guides/ai-infrastructure/mcp-server/prompts-and-resources` — merged into setup
- `{lang}/guides/ai-infrastructure/mcp-server/tools-reference` — merged into tools
- `{lang}/guides/resources/changelog` — promoted to top-level Changelog tab

## Legal (moved to footer)
- `{lang}/guides/legal-policies/terms-of-service` → footer link only
- `{lang}/guides/legal-policies/privacy-policy` → footer link only
- `{lang}/guides/legal-policies/contact-support` → footer link only

## Changelog (new top-level tab)
- `{lang}/changelog/index` ← from `{lang}/guides/resources/changelog`

## Languages: en, cn, zh-Hant, jp, ko — all mirrored.
