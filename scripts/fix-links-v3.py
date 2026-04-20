#!/usr/bin/env python3
"""Bulk-fix internal links after the v3 restructure.

Walks every .mdx (and a few .md / .txt) under en/ cn/ zh-Hant/ jp/ ko/ and
rewrites old `/{lang}/guides/...` and `/{lang}/playbooks/...` links to their
new v3 locations, per MIGRATION_NOTES.md.

Safe to run multiple times; idempotent.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["en", "cn", "zh-Hant", "jp", "ko"]

GUIDES_MAP: list[tuple[str, str]] = [
    ("guides/getting-started/overview", "docs/home"),
    ("guides/getting-started/quickstart", "docs/quickstart"),
    ("guides/getting-started/supported-chains", "docs/supported-chains"),
    ("guides/getting-started/authentication", "docs/platform/authentication/api-keys-oauth"),
    ("guides/getting-started/wallet-auth-siwx", "docs/platform/authentication/wallet-auth-siwx"),
    ("guides/getting-started/billing-and-units", "docs/platform/billing-payments/plans-and-units"),
    ("guides/getting-started/x402-payments", "docs/platform/billing-payments/x402-payments"),
    ("guides/getting-started/mpp-payments", "docs/platform/billing-payments/mpp-payments"),
    ("guides/getting-started/faq", "docs/reference/faq"),
    ("guides/getting-started/api-comparison", "docs/access-methods/overview"),
    ("guides/getting-started/choosing-your-path", "docs/home"),
    ("guides/data-concepts/smart-money-methodology", "docs/data-products/smart-money"),
    ("guides/data-concepts/realtime-streaming", "docs/access-methods/websocket"),
    ("guides/data-concepts/kafka-streams/overview", "docs/access-methods/kafka-streams/overview"),
    ("guides/data-concepts/kafka-streams/evm-streams", "docs/access-methods/kafka-streams/evm-streams"),
    ("guides/data-concepts/kafka-streams/solana-streams", "docs/access-methods/kafka-streams/solana-streams"),
    ("guides/data-concepts/kafka-streams/tron-streams", "docs/access-methods/kafka-streams/tron-streams"),
    ("guides/data-concepts/kyt-concepts", "docs/compliance/kyt-concepts"),
    ("guides/data-concepts/kya-concepts", "docs/compliance/kya-concepts"),
    ("guides/data-concepts/compliance-integration", "docs/compliance/integration-guide"),
    ("guides/data-concepts/api-security", "docs/platform/security/api-security"),
    ("guides/data-concepts/data-privacy", "docs/platform/security/data-privacy"),
    ("guides/security-compliance/overview", "docs/compliance/overview"),
    ("guides/ai-infrastructure/overview", "docs/ai-agents/overview"),
    ("guides/ai-infrastructure/mcp-server/introduction", "docs/ai-agents/mcp-server/introduction"),
    ("guides/ai-infrastructure/mcp-server/setup-guide", "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/self-hosted-installation", "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/stdio-transport", "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/prompts-and-resources", "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/tools-catalog", "docs/ai-agents/mcp-server/tools"),
    ("guides/ai-infrastructure/mcp-server/tools-reference", "docs/ai-agents/mcp-server/tools"),
    ("guides/ai-infrastructure/agent-skills/introduction", "docs/ai-agents/agent-skills/introduction"),
    ("guides/ai-infrastructure/agent-skills/installation", "docs/ai-agents/agent-skills/installation"),
    ("guides/ai-infrastructure/agent-skills/chainstream-data", "docs/ai-agents/agent-skills/chainstream-data"),
    ("guides/ai-infrastructure/agent-skills/chainstream-defi", "docs/ai-agents/agent-skills/chainstream-defi"),
    ("guides/integrations/openclaw/overview", "docs/ecosystem/openclaw/overview"),
    ("guides/integrations/openclaw/skills-install", "docs/ecosystem/openclaw/skills-install"),
    ("guides/integrations/openclaw/cross-agent-compatibility", "docs/ecosystem/openclaw/cross-agent-compatibility"),
    ("guides/integrations/openclaw/security", "docs/ecosystem/openclaw/security"),
    ("guides/integrations/n8n/overview", "docs/ecosystem/n8n/overview"),
    ("guides/integrations/n8n/trigger-node", "docs/ecosystem/n8n/trigger-node"),
    ("guides/resources/glossary", "docs/reference/glossary"),
    ("guides/resources/error-codes", "docs/reference/error-codes"),
    ("guides/resources/changelog", "changelog/overview"),
    ("guides/legal-policies/terms-of-service", "docs/reference/terms-of-service"),
    ("guides/legal-policies/privacy-policy", "docs/reference/privacy-policy"),
    ("guides/legal-policies/contact-support", "docs/reference/contact-support"),
    ("guides/cli/overview", "docs/access-methods/cli"),
    ("guides/cli/authentication", "docs/platform/authentication/api-keys-oauth"),
    ("guides/cli/commands", "api-reference/cli-commands/overview"),
    ("guides/cli/x402-payment", "docs/platform/billing-payments/x402-payments"),
    ("guides/ai-infrastructure/mcp-server/overview", "docs/ai-agents/mcp-server/introduction"),
    ("guides/ai-infrastructure/mcp-server/installation", "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server", "docs/ai-agents/mcp-server/introduction"),
    ("guides/ai-infrastructure/agent-skills", "docs/ai-agents/agent-skills/introduction"),
    ("guides/ai-infrastructure", "docs/ai-agents/overview"),
    ("guides/getting-started", "docs/home"),
    ("guides/data-concepts", "docs/data-products/overview"),
    ("guides/resources", "docs/reference/glossary"),
    ("guides/cli", "docs/access-methods/cli"),
    ("guides/security-compliance", "docs/compliance/overview"),
    ("guides/integrations", "docs/ecosystem/openclaw/overview"),
]

PLAYBOOKS_MAP: list[tuple[str, str]] = [
    ("playbooks/tutorials/smart-money-tracker", "docs/tutorials/smart-money-tracker"),
    ("playbooks/tutorials/build-price-alert-bot", "docs/tutorials/build-price-alert-bot"),
    ("playbooks/tutorials/build-arbitrage-scanner", "docs/tutorials/build-arbitrage-scanner"),
    ("playbooks/tutorials/integrate-deposit-check", "docs/tutorials/integrate-deposit-check"),
    ("playbooks/tutorials/ai-agent-with-mcp", "docs/tutorials/ai-agent-with-mcp"),
    ("playbooks/frameworks/token-analysis-framework", "docs/recipes/token-analysis-framework"),
    ("playbooks/frameworks/defi-monitoring-overview", "docs/recipes/defi-monitoring"),
    ("playbooks/frameworks/webhook-fundamentals", "docs/recipes/webhook-fundamentals"),
    ("playbooks/frameworks/defi-monitoring", "docs/recipes/defi-monitoring"),
    ("playbooks/protocols/pump-fun", "docs/recipes/pump-fun"),
    ("playbooks/protocols/raydium", "docs/recipes/raydium"),
    ("playbooks/overview", "docs/recipes/overview"),
]

GUIDES_AND_TUTORIALS_MAP: list[tuple[str, str]] = [
    ("guides-and-tutorials/overview", "docs/home"),
]

ALL_MAPS = GUIDES_MAP + PLAYBOOKS_MAP + GUIDES_AND_TUTORIALS_MAP


def build_patterns() -> list[tuple[re.Pattern[str], str]]:
    pats: list[tuple[re.Pattern[str], str]] = []
    for lang in LANGS:
        for old, new in ALL_MAPS:
            # Match inside href/URL contexts OR after docs.chainstream.io for llms.txt
            pat = re.compile(
                rf"(?<=[\"\'\(\s\>]){re.escape(f'/{lang}/{old}')}(?=[\"\'\)\s\#\<\)]|$)",
                re.MULTILINE,
            )
            pats.append((pat, f"/{lang}/{new}"))
    return pats


def fix_file(path: Path, patterns: list[tuple[re.Pattern[str], str]]) -> int:
    text = path.read_text(encoding="utf-8")
    new = text
    for pat, repl in patterns:
        new = pat.sub(repl, new)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return 1
    return 0


def main() -> None:
    filter_arg = sys.argv[1] if len(sys.argv) > 1 else None
    patterns = build_patterns()

    files: list[Path] = []
    for lang in LANGS:
        base = ROOT / lang
        if not base.is_dir():
            continue
        for ext in ("*.mdx", "*.md", "*.txt"):
            files.extend(base.rglob(ext))

    if filter_arg:
        files = [f for f in files if filter_arg in str(f.relative_to(ROOT))]

    changed = 0
    for f in files:
        if fix_file(f, patterns):
            rel = f.relative_to(ROOT)
            print(f"  OK: {rel}")
            changed += 1

    print(f"\nDone — {changed} files updated out of {len(files)} scanned.")


if __name__ == "__main__":
    main()
