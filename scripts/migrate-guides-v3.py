#!/usr/bin/env python3
"""
Guides v3 migration: rename/move existing .mdx pages to new paths, delete merged
originals, and create stub files for net-new pages. Runs across all 5 languages.

Usage:
    python3 scripts/migrate-guides-v3.py [--dry-run]

Idempotent: reruns skip already-moved files.
"""

import os
import subprocess
import sys
from pathlib import Path

LANGS = ["en", "cn", "zh-Hant", "jp", "ko"]
ROOT = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Simple 1:1 path moves (relative to each {lang}/ directory)
# old_path -> new_path
# -------------------------------------------------------------------
MOVES: list[tuple[str, str]] = [
    # Top-level of Docs
    ("guides/getting-started/overview.mdx",          "docs/home.mdx"),
    ("guides/getting-started/quickstart.mdx",        "docs/quickstart.mdx"),
    ("guides/getting-started/supported-chains.mdx",  "docs/supported-chains.mdx"),

    # Data Products (only one existing page maps here; rest are new)
    ("guides/data-concepts/smart-money-methodology.mdx", "docs/data-products/smart-money.mdx"),

    # Access Methods
    ("guides/data-concepts/realtime-streaming.mdx", "docs/access-methods/websocket.mdx"),
    ("guides/data-concepts/kafka-streams/overview.mdx",       "docs/access-methods/kafka-streams/overview.mdx"),
    ("guides/data-concepts/kafka-streams/evm-streams.mdx",    "docs/access-methods/kafka-streams/evm-streams.mdx"),
    ("guides/data-concepts/kafka-streams/solana-streams.mdx", "docs/access-methods/kafka-streams/solana-streams.mdx"),
    ("guides/data-concepts/kafka-streams/tron-streams.mdx",   "docs/access-methods/kafka-streams/tron-streams.mdx"),

    # AI Agents
    ("guides/ai-infrastructure/overview.mdx",                        "docs/ai-agents/overview.mdx"),
    ("guides/ai-infrastructure/mcp-server/introduction.mdx",         "docs/ai-agents/mcp-server/introduction.mdx"),
    ("guides/ai-infrastructure/mcp-server/setup-guide.mdx",          "docs/ai-agents/mcp-server/setup.mdx"),
    ("guides/ai-infrastructure/mcp-server/tools-catalog.mdx",        "docs/ai-agents/mcp-server/tools.mdx"),
    ("guides/ai-infrastructure/agent-skills/introduction.mdx",       "docs/ai-agents/agent-skills/introduction.mdx"),
    ("guides/ai-infrastructure/agent-skills/installation.mdx",       "docs/ai-agents/agent-skills/installation.mdx"),
    ("guides/ai-infrastructure/agent-skills/chainstream-data.mdx",   "docs/ai-agents/agent-skills/chainstream-data.mdx"),
    ("guides/ai-infrastructure/agent-skills/chainstream-defi.mdx",   "docs/ai-agents/agent-skills/chainstream-defi.mdx"),

    # Compliance (KYT / KYA)
    ("guides/security-compliance/overview.mdx",        "docs/compliance/overview.mdx"),
    ("guides/data-concepts/kyt-concepts.mdx",          "docs/compliance/kyt-concepts.mdx"),
    ("guides/data-concepts/kya-concepts.mdx",          "docs/compliance/kya-concepts.mdx"),
    ("guides/data-concepts/compliance-integration.mdx","docs/compliance/integration-guide.mdx"),

    # Tutorials (from Playbooks/tutorials)
    ("playbooks/tutorials/build-price-alert-bot.mdx",   "docs/tutorials/build-price-alert-bot.mdx"),
    ("playbooks/tutorials/build-arbitrage-scanner.mdx", "docs/tutorials/build-arbitrage-scanner.mdx"),
    ("playbooks/tutorials/smart-money-tracker.mdx",     "docs/tutorials/smart-money-tracker.mdx"),
    ("playbooks/tutorials/integrate-deposit-check.mdx", "docs/tutorials/integrate-deposit-check.mdx"),
    ("playbooks/tutorials/ai-agent-with-mcp.mdx",       "docs/tutorials/ai-agent-with-mcp.mdx"),

    # Recipes (from Playbooks/frameworks and protocols)
    ("playbooks/frameworks/token-analysis-framework.mdx", "docs/recipes/token-analysis-framework.mdx"),
    ("playbooks/frameworks/defi-monitoring-overview.mdx", "docs/recipes/defi-monitoring.mdx"),
    ("playbooks/frameworks/webhook-fundamentals.mdx",     "docs/recipes/webhook-fundamentals.mdx"),
    ("playbooks/protocols/pump-fun.mdx",                  "docs/recipes/pump-fun.mdx"),
    ("playbooks/protocols/raydium.mdx",                   "docs/recipes/raydium.mdx"),

    # Platform / Authentication
    ("guides/getting-started/authentication.mdx",   "docs/platform/authentication/api-keys-oauth.mdx"),
    ("guides/getting-started/wallet-auth-siwx.mdx", "docs/platform/authentication/wallet-auth-siwx.mdx"),
    # Platform / Billing & Payments
    ("guides/getting-started/billing-and-units.mdx","docs/platform/billing-payments/plans-and-units.mdx"),
    ("guides/getting-started/x402-payments.mdx",    "docs/platform/billing-payments/x402-payments.mdx"),
    ("guides/getting-started/mpp-payments.mdx",     "docs/platform/billing-payments/mpp-payments.mdx"),
    # Platform / Security
    ("guides/data-concepts/api-security.mdx",  "docs/platform/security/api-security.mdx"),
    ("guides/data-concepts/data-privacy.mdx",  "docs/platform/security/data-privacy.mdx"),

    # Ecosystem (from Integrations)
    ("guides/integrations/openclaw/overview.mdx",                 "docs/ecosystem/openclaw/overview.mdx"),
    ("guides/integrations/openclaw/skills-install.mdx",           "docs/ecosystem/openclaw/skills-install.mdx"),
    ("guides/integrations/openclaw/cross-agent-compatibility.mdx","docs/ecosystem/openclaw/cross-agent-compatibility.mdx"),
    ("guides/integrations/openclaw/security.mdx",                 "docs/ecosystem/openclaw/security.mdx"),
    ("guides/integrations/n8n/overview.mdx",     "docs/ecosystem/n8n/overview.mdx"),
    ("guides/integrations/n8n/trigger-node.mdx", "docs/ecosystem/n8n/trigger-node.mdx"),

    # Reference
    ("guides/resources/glossary.mdx",    "docs/reference/glossary.mdx"),
    ("guides/resources/error-codes.mdx", "docs/reference/error-codes.mdx"),
    ("guides/getting-started/faq.mdx",   "docs/reference/faq.mdx"),

    # Changelog — promoted to top-level tab
    ("guides/resources/changelog.mdx", "changelog/index.mdx"),

    # Legal — out of sidebar, into footer; keep files reachable
    ("guides/legal-policies/terms-of-service.mdx", "legal/terms-of-service.mdx"),
    ("guides/legal-policies/privacy-policy.mdx",   "legal/privacy-policy.mdx"),
    ("guides/legal-policies/contact-support.mdx",  "legal/contact-support.mdx"),
]

# -------------------------------------------------------------------
# Files to DELETE (content merged elsewhere; originals no longer needed).
# Relative to each {lang}/ directory.
# -------------------------------------------------------------------
DELETES: list[str] = [
    "guides/getting-started/choosing-your-path.mdx",  # redundant with home/quickstart
    "guides/getting-started/api-comparison.mdx",      # merged into docs/access-methods/overview
    "guides/ai-infrastructure/mcp-server/self-hosted-installation.mdx",  # → merged into setup
    "guides/ai-infrastructure/mcp-server/stdio-transport.mdx",           # → merged into setup
    "guides/ai-infrastructure/mcp-server/prompts-and-resources.mdx",     # → merged into setup
    "guides/ai-infrastructure/mcp-server/tools-reference.mdx",           # → merged into tools
    "guides/cli/overview.mdx",       # content moved to docs/access-methods/cli (new)
    "guides/cli/authentication.mdx", # already covered by platform/authentication
    "guides/cli/commands.mdx",       # promoted to api-reference/cli-commands
    "guides/cli/x402-payment.mdx",   # merged into platform/billing-payments/x402-payments
]

# -------------------------------------------------------------------
# Stub pages to CREATE if the path does not exist after moves
# Each entry: (relative_path_under_{lang}, title-map, description-map)
# -------------------------------------------------------------------

T = dict[str, str]  # language -> localized string

def t(en: str, cn: str = None, zh: str = None, jp: str = None, ko: str = None) -> T:
    """Localized label helper. Defaults to English if translation missing."""
    return {
        "en": en,
        "cn": cn or en,
        "zh-Hant": zh or (cn or en),
        "jp": jp or en,
        "ko": ko or en,
    }


STUBS: list[tuple[str, T, T]] = [
    # Data Products entity pages (10 new + overview)
    ("docs/data-products/overview.mdx",
     t("Data Products Overview",
       cn="数据产品概览", zh="資料產品概覽", jp="データプロダクト概要", ko="데이터 제품 개요"),
     t("The full catalog of datasets ChainStream publishes across supported chains.",
       cn="ChainStream 在所有支持链上提供的数据集目录。",
       zh="ChainStream 在所有支援鏈上提供的資料集目錄。",
       jp="ChainStream がサポートする全チェーンで公開しているデータセットの全カタログ。",
       ko="ChainStream이 지원하는 모든 체인에서 제공하는 데이터셋 전체 카탈로그.")),
    ("docs/data-products/tokens.mdx",
     t("Tokens", cn="代币", zh="代幣", jp="トークン", ko="토큰"),
     t("Token metadata, market data, prices, and stats across all supported chains.",
       cn="所有支持链上的代币元数据、市场数据、价格与统计指标。",
       zh="所有支援鏈上的代幣元資料、市場資料、價格與統計指標。")),
    ("docs/data-products/trades.mdx",
     t("Trades", cn="交易", zh="交易", jp="トレード", ko="거래"),
     t("DEX trade stream — every swap normalized across Solana, Ethereum, BSC and more.",
       cn="DEX 交易流——在 Solana、Ethereum、BSC 等链上标准化的每一笔 swap。",
       zh="DEX 交易流——在 Solana、Ethereum、BSC 等鏈上標準化的每一筆 swap。")),
    ("docs/data-products/wallets.mdx",
     t("Wallets", cn="钱包", zh="錢包", jp="ウォレット", ko="지갑"),
     t("Wallet balances, PnL, holdings, transfers, and net-worth evolution.",
       cn="钱包余额、PnL、持仓、转账与净值演变。",
       zh="錢包餘額、PnL、持倉、轉帳與淨值演變。")),
    ("docs/data-products/dex-pools.mdx",
     t("DEX Pools", cn="DEX 池子", zh="DEX 池子", jp="DEX プール", ko="DEX 풀"),
     t("Liquidity pool state, reserves, swap fees and snapshots.",
       cn="流动性池状态、储备、手续费与快照。",
       zh="流動性池狀態、儲備、手續費與快照。")),
    ("docs/data-products/rankings.mdx",
     t("Rankings", cn="榜单", zh="榜單", jp="ランキング", ko="랭킹"),
     t("Curated lists of hot / new / migrated / final-stretch tokens per chain.",
       cn="每条链上热门、新发、迁移、冲线代币的精选榜单。",
       zh="每條鏈上熱門、新發、遷移、衝線代幣的精選榜單。")),
    ("docs/data-products/candles-ohlc.mdx",
     t("Candles (OHLC)", cn="K线 (OHLC)", zh="K線 (OHLC)", jp="ローソク足 (OHLC)", ko="캔들 (OHLC)"),
     t("OHLC candlestick data at multiple intervals for token or pair or pool.",
       cn="代币 / 交易对 / 池子的多周期 OHLC K 线数据。",
       zh="代幣 / 交易對 / 池子的多週期 OHLC K 線資料。")),
    ("docs/data-products/holders.mdx",
     t("Holders", cn="持币人", zh="持幣人", jp="ホルダー", ko="홀더"),
     t("Token holder distribution, top holders, holder changes over time.",
       cn="代币持仓分布、顶级持币人、持币变化。",
       zh="代幣持倉分布、頂級持幣人、持幣變化。")),
    ("docs/data-products/blockchain-core.mdx",
     t("Blockchain Core", cn="区块链底层数据", zh="區塊鏈底層資料", jp="ブロックチェーン基盤データ", ko="블록체인 코어"),
     t("Raw blocks, transactions and chain-level metrics.",
       cn="原始区块、交易与链级指标。",
       zh="原始區塊、交易與鏈級指標。")),
    ("docs/data-products/data-freshness.mdx",
     t("Data Freshness & SLA", cn="数据新鲜度与 SLA", zh="資料新鮮度與 SLA", jp="データ鮮度と SLA", ko="데이터 신선도 및 SLA"),
     t("Latency guarantees, refresh intervals and backfill behaviour per dataset.",
       cn="每个数据集的延迟保障、刷新间隔与回填行为。",
       zh="每個資料集的延遲保障、刷新間隔與回填行為。")),

    # Access Methods overview + new pages
    ("docs/access-methods/overview.mdx",
     t("Access Methods", cn="接入方式", zh="接入方式", jp="接続方法", ko="접속 방법"),
     t("Pick the right interface for your workload — REST, GraphQL, WebSocket, Kafka, SDK, or CLI.",
       cn="为你的场景选对接口——REST、GraphQL、WebSocket、Kafka、SDK 或 CLI。",
       zh="為你的場景選對介面——REST、GraphQL、WebSocket、Kafka、SDK 或 CLI。")),
    ("docs/access-methods/rest-api.mdx",
     t("REST API", cn="REST API", zh="REST API", jp="REST API", ko="REST API"),
     t("HTTPS endpoints for on-demand lookups of tokens, wallets, trades and more.",
       cn="用于按需查询代币、钱包、交易等数据的 HTTPS 接口。",
       zh="用於按需查詢代幣、錢包、交易等資料的 HTTPS 介面。")),
    ("docs/access-methods/graphql.mdx",
     t("GraphQL", cn="GraphQL", zh="GraphQL", jp="GraphQL", ko="GraphQL"),
     t("Flexible analytical queries across blocks, transactions, trades and balances.",
       cn="跨区块、交易、交易记录与余额的灵活分析查询。",
       zh="跨區塊、交易、交易記錄與餘額的彈性分析查詢。")),
    ("docs/access-methods/sdks.mdx",
     t("SDKs", cn="SDK", zh="SDK", jp="SDK", ko="SDK"),
     t("Typed client libraries in TypeScript, Python, Go and Rust.",
       cn="TypeScript、Python、Go 与 Rust 的类型化客户端库。",
       zh="TypeScript、Python、Go 與 Rust 的型別化用戶端函式庫。")),
    ("docs/access-methods/cli.mdx",
     t("CLI", cn="CLI", zh="CLI", jp="CLI", ko="CLI"),
     t("The chainstream command-line interface for data queries and DeFi execution.",
       cn="用于数据查询与 DeFi 执行的 chainstream 命令行工具。",
       zh="用於資料查詢與 DeFi 執行的 chainstream 命令列工具。")),

    # Tutorials & Recipes: already moved from playbooks; no stubs needed
    # Ecosystem already moved; no stubs needed

    # API Reference new pages
    ("api-reference/overview.mdx",
     t("API Reference", cn="API 参考", zh="API 參考", jp="API リファレンス", ko="API 레퍼런스"),
     t("All programmatic surfaces — REST, WebSocket, Kafka topics, CLI and MCP tools.",
       cn="所有程序接口——REST、WebSocket、Kafka topic、CLI 与 MCP 工具。",
       zh="所有程式介面——REST、WebSocket、Kafka topic、CLI 與 MCP 工具。")),
    ("api-reference/kafka-topics/evm.mdx",
     t("EVM Kafka Topics", cn="EVM Kafka Topics", zh="EVM Kafka Topics", jp="EVM Kafka Topics", ko="EVM Kafka Topics"),
     t("Reference list of EVM-chain Kafka topic names, keys and payload schemas.",
       cn="EVM 链 Kafka topic 名称、key 与 payload schema 参考。",
       zh="EVM 鏈 Kafka topic 名稱、key 與 payload schema 參考。")),
    ("api-reference/kafka-topics/solana.mdx",
     t("Solana Kafka Topics", cn="Solana Kafka Topics", zh="Solana Kafka Topics", jp="Solana Kafka Topics", ko="Solana Kafka Topics"),
     t("Reference list of Solana Kafka topic names, keys and payload schemas.",
       cn="Solana 链 Kafka topic 名称、key 与 payload schema 参考。",
       zh="Solana 鏈 Kafka topic 名稱、key 與 payload schema 參考。")),
    ("api-reference/kafka-topics/tron.mdx",
     t("Tron Kafka Topics", cn="Tron Kafka Topics", zh="Tron Kafka Topics", jp="Tron Kafka Topics", ko="Tron Kafka Topics"),
     t("Reference list of Tron Kafka topic names, keys and payload schemas.",
       cn="Tron 链 Kafka topic 名称、key 与 payload schema 参考。",
       zh="Tron 鏈 Kafka topic 名稱、key 與 payload schema 參考。")),
    ("api-reference/cli-commands/overview.mdx",
     t("CLI Commands Reference", cn="CLI 命令参考", zh="CLI 命令參考", jp="CLI コマンドリファレンス", ko="CLI 명령어 레퍼런스"),
     t("Full list of chainstream CLI commands, flags and output formats.",
       cn="chainstream CLI 全部命令、参数与输出格式。",
       zh="chainstream CLI 全部命令、參數與輸出格式。")),
    ("api-reference/mcp-tools/overview.mdx",
     t("MCP Tools Reference", cn="MCP 工具参考", zh="MCP 工具參考", jp="MCP ツールリファレンス", ko="MCP 도구 레퍼런스"),
     t("Complete tool catalog exposed by the ChainStream MCP Server.",
       cn="ChainStream MCP Server 暴露的完整工具目录。",
       zh="ChainStream MCP Server 暴露的完整工具目錄。")),
]


def sh(*args: str, dry: bool = False) -> None:
    if dry:
        print("(dry)", *args)
        return
    subprocess.run(list(args), cwd=ROOT, check=True)


def git_mv(old: Path, new: Path, dry: bool) -> None:
    if not old.exists():
        return
    if new.exists():
        print(f"skip (dest exists): {new}")
        return
    new.parent.mkdir(parents=True, exist_ok=True)
    if dry:
        print(f"(dry) git mv {old} {new}")
        return
    # Use git mv to preserve history
    subprocess.run(["git", "mv", str(old), str(new)], cwd=ROOT, check=True)


def git_rm(p: Path, dry: bool) -> None:
    if not p.exists():
        return
    if dry:
        print(f"(dry) git rm {p}")
        return
    subprocess.run(["git", "rm", str(p)], cwd=ROOT, check=True)


STUB_TEMPLATE = """---
title: "{title}"
description: "{description}"
---

<Note>
  This page is part of the **Guides v3** restructure. Content is being migrated
  — check back soon or open an issue if you need this sooner.
</Note>
"""


def write_stub(p: Path, title: str, description: str, dry: bool) -> None:
    if p.exists():
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    if dry:
        print(f"(dry) stub {p}")
        return
    p.write_text(STUB_TEMPLATE.format(title=title, description=description))


def main() -> None:
    dry = "--dry-run" in sys.argv

    # 1) MOVES
    for old_rel, new_rel in MOVES:
        for lang in LANGS:
            old = ROOT / lang / old_rel
            new = ROOT / lang / new_rel
            git_mv(old, new, dry)

    # 2) DELETES
    for rel in DELETES:
        for lang in LANGS:
            git_rm(ROOT / lang / rel, dry)

    # 3) STUBS for new pages
    for rel, titles, descs in STUBS:
        for lang in LANGS:
            p = ROOT / lang / rel
            write_stub(p, titles[lang], descs[lang], dry)

    print("done." + (" (dry-run)" if dry else ""))


if __name__ == "__main__":
    main()
