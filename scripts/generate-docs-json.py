#!/usr/bin/env python3
"""
One-shot generator for the restructured docs.json (Guides v3).

This script emits the new navigation for 5 languages from a single declarative
source of truth. Run once, diff the output, commit. After landing the refactor
this file is retained in scripts/ as a reference for future large reshuffles.
"""

import json
from pathlib import Path
from typing import Any

LANGS = ["en", "cn", "zh-Hant", "jp", "ko"]

# -------------------------------------------------------------------
# Localized group labels
# -------------------------------------------------------------------
LABELS = {
    # Docs tab top-level group labels
    "data_products":        {"en": "Data Products",        "cn": "数据产品",        "zh-Hant": "資料產品",        "jp": "データプロダクト",        "ko": "데이터 제품"},
    "access_methods":       {"en": "Access Methods",       "cn": "接入方式",        "zh-Hant": "接入方式",        "jp": "接続方法",               "ko": "접속 방법"},
    "kafka_streams":        {"en": "Kafka Streams",        "cn": "Kafka Streams",   "zh-Hant": "Kafka Streams",   "jp": "Kafka Streams",          "ko": "Kafka Streams"},
    "ai_agents":            {"en": "AI Agents",            "cn": "AI Agents",       "zh-Hant": "AI Agents",       "jp": "AI Agents",              "ko": "AI Agents"},
    "mcp_server":           {"en": "MCP Server",           "cn": "MCP Server",      "zh-Hant": "MCP Server",      "jp": "MCP Server",             "ko": "MCP Server"},
    "agent_skills":         {"en": "Agent Skills",         "cn": "Agent Skills",    "zh-Hant": "Agent Skills",    "jp": "Agent Skills",           "ko": "Agent Skills"},
    "compliance":           {"en": "Compliance (KYT/KYA)", "cn": "合规 (KYT/KYA)",   "zh-Hant": "合規 (KYT/KYA)",   "jp": "コンプライアンス (KYT/KYA)", "ko": "컴플라이언스 (KYT/KYA)"},
    "tutorials":            {"en": "Tutorials",            "cn": "教程",            "zh-Hant": "教學",            "jp": "チュートリアル",          "ko": "튜토리얼"},
    "recipes":              {"en": "Recipes",              "cn": "Recipes",         "zh-Hant": "Recipes",         "jp": "Recipes",                "ko": "Recipes"},
    "platform":             {"en": "Platform",             "cn": "平台",            "zh-Hant": "平台",            "jp": "プラットフォーム",       "ko": "플랫폼"},
    "auth":                 {"en": "Authentication",       "cn": "鉴权",            "zh-Hant": "鑑權",            "jp": "認証",                   "ko": "인증"},
    "billing_payments":     {"en": "Billing & Payments",   "cn": "计费与支付",       "zh-Hant": "計費與支付",       "jp": "課金と支払い",           "ko": "결제 및 요금"},
    "security":             {"en": "Security",             "cn": "安全",            "zh-Hant": "安全",            "jp": "セキュリティ",           "ko": "보안"},
    "ecosystem":            {"en": "Ecosystem",            "cn": "生态",            "zh-Hant": "生態",            "jp": "エコシステム",           "ko": "에코시스템"},
    "reference_group":      {"en": "Reference",            "cn": "参考",            "zh-Hant": "參考",            "jp": "リファレンス",           "ko": "레퍼런스"},

    # API Reference tab
    "api_authentication":   {"en": "Authentication",       "cn": "鉴权",            "zh-Hant": "鑑權",            "jp": "認証",                   "ko": "인증"},
    "rest_api":             {"en": "REST API",             "cn": "REST API",        "zh-Hant": "REST API",        "jp": "REST API",               "ko": "REST API"},
    "websocket_api":        {"en": "WebSocket",            "cn": "WebSocket",       "zh-Hant": "WebSocket",       "jp": "WebSocket",              "ko": "WebSocket"},
    "kafka_topics":         {"en": "Kafka Topics",         "cn": "Kafka Topics",    "zh-Hant": "Kafka Topics",    "jp": "Kafka Topics",           "ko": "Kafka Topics"},
    "cli_commands":         {"en": "CLI Commands",         "cn": "CLI 命令",         "zh-Hant": "CLI 命令",         "jp": "CLI コマンド",           "ko": "CLI 명령어"},
    "mcp_tools":            {"en": "MCP Tools",            "cn": "MCP 工具",         "zh-Hant": "MCP 工具",         "jp": "MCP ツール",             "ko": "MCP 도구"},

    # REST API sub-groups keep existing English labels; localizations are light
    "rest_token":           {"en": "Token",                "cn": "Token",           "zh-Hant": "Token",           "jp": "Token",                  "ko": "Token"},
    "rest_trade":           {"en": "Trade",                "cn": "Trade",           "zh-Hant": "Trade",           "jp": "Trade",                  "ko": "Trade"},
    "rest_wallet":          {"en": "Wallet",               "cn": "Wallet",          "zh-Hant": "Wallet",          "jp": "Wallet",                 "ko": "Wallet"},
    "rest_dex_pool":        {"en": "DEX Pool",             "cn": "DEX Pool",        "zh-Hant": "DEX Pool",        "jp": "DEX Pool",               "ko": "DEX Pool"},
    "rest_ranking":         {"en": "Ranking",              "cn": "Ranking",         "zh-Hant": "Ranking",         "jp": "Ranking",                "ko": "Ranking"},
    "rest_blockchain":      {"en": "Blockchain",           "cn": "Blockchain",      "zh-Hant": "Blockchain",      "jp": "Blockchain",             "ko": "Blockchain"},
    "rest_watchlist":       {"en": "Watchlist",            "cn": "Watchlist",       "zh-Hant": "Watchlist",       "jp": "Watchlist",              "ko": "Watchlist"},
    "rest_webhook":         {"en": "Webhook",              "cn": "Webhook",         "zh-Hant": "Webhook",         "jp": "Webhook",                "ko": "Webhook"},
    "rest_ipfs":            {"en": "IPFS",                 "cn": "IPFS",            "zh-Hant": "IPFS",            "jp": "IPFS",                   "ko": "IPFS"},
    "rest_redpacket":       {"en": "RedPacket",            "cn": "RedPacket",       "zh-Hant": "RedPacket",       "jp": "RedPacket",              "ko": "RedPacket"},
    "rest_kyt":             {"en": "KYT",                  "cn": "KYT",             "zh-Hant": "KYT",             "jp": "KYT",                    "ko": "KYT"},
    "rest_dex_swap":        {"en": "DEX Swap",             "cn": "DEX Swap",        "zh-Hant": "DEX Swap",        "jp": "DEX Swap",               "ko": "DEX Swap"},
    "rest_transaction":     {"en": "Transaction",          "cn": "Transaction",     "zh-Hant": "Transaction",     "jp": "Transaction",            "ko": "Transaction"},
    "rest_job":             {"en": "Job",                  "cn": "Job",             "zh-Hant": "Job",             "jp": "Job",                    "ko": "Job"},
    "rest_dex_registry":    {"en": "DEX Registry",         "cn": "DEX Registry",    "zh-Hant": "DEX Registry",    "jp": "DEX Registry",           "ko": "DEX Registry"},

    # GraphQL tab (preserve existing labels)
    "graphql_getting_started": {"en": "Getting Started",   "cn": "快速开始",         "zh-Hant": "快速開始",         "jp": "はじめに",               "ko": "시작하기"},
    "graphql_ide":          {"en": "GraphQL IDE",          "cn": "GraphQL IDE",     "zh-Hant": "GraphQL IDE",     "jp": "GraphQL IDE",            "ko": "GraphQL IDE"},
    "graphql_schema":       {"en": "Schema & Data Model",  "cn": "Schema 与数据模型", "zh-Hant": "Schema 與資料模型", "jp": "スキーマとデータモデル",   "ko": "스키마 & 데이터 모델"},
    "graphql_examples":     {"en": "Query Examples",       "cn": "查询示例",         "zh-Hant": "查詢範例",         "jp": "クエリ例",               "ko": "쿼리 예제"},
    "graphql_billing":      {"en": "Billing & Credits",    "cn": "计费与额度",       "zh-Hant": "計費與額度",       "jp": "課金とクレジット",       "ko": "빌링 & 크레딧"},

    # SDKs tab
    "sdks":                 {"en": "SDKs",                 "cn": "SDK",             "zh-Hant": "SDK",             "jp": "SDK",                    "ko": "SDK"},

    # Changelog tab
    "changelog":            {"en": "Changelog",            "cn": "更新日志",         "zh-Hant": "更新日誌",         "jp": "変更履歴",               "ko": "변경 이력"},
}


def L(key: str, lang: str) -> str:
    return LABELS[key][lang]


def prefix_pages(lang: str, pages: list[Any]) -> list[Any]:
    """Prefix every string page with the language prefix, recursing into nested groups."""
    out: list[Any] = []
    for p in pages:
        if isinstance(p, str):
            out.append(f"{lang}/{p}")
        elif isinstance(p, dict):
            new = dict(p)
            if "pages" in new:
                new["pages"] = prefix_pages(lang, new["pages"])
            out.append(new)
    return out


def group(lang: str, label_key: str, pages: list[Any], icon: str | None = None) -> dict:
    g: dict = {"group": L(label_key, lang), "pages": prefix_pages(lang, pages)}
    if icon:
        g["icon"] = icon
    return g


# -------------------------------------------------------------------
# Docs tab navigation (shared across languages, only labels differ)
# -------------------------------------------------------------------
def docs_groups(lang: str) -> list[dict]:
    return [
        # Top-level ungrouped pages
        {
            "group": " ",
            "pages": prefix_pages(lang, [
                "docs/home",
                "docs/quickstart",
                "docs/supported-chains",
            ]),
        },
        group(lang, "data_products", [
            "docs/data-products/overview",
            "docs/data-products/tokens",
            "docs/data-products/trades",
            "docs/data-products/wallets",
            "docs/data-products/dex-pools",
            "docs/data-products/rankings",
            "docs/data-products/candles-ohlc",
            "docs/data-products/holders",
            "docs/data-products/smart-money",
            "docs/data-products/blockchain-core",
            "docs/data-products/data-freshness",
        ], icon="database"),
        group(lang, "access_methods", [
            "docs/access-methods/overview",
            "docs/access-methods/rest-api",
            "docs/access-methods/graphql",
            "docs/access-methods/websocket",
            {
                "group": L("kafka_streams", lang),
                "icon": "bars-staggered",
                "pages": [
                    "docs/access-methods/kafka-streams/overview",
                    "docs/access-methods/kafka-streams/evm-streams",
                    "docs/access-methods/kafka-streams/solana-streams",
                    "docs/access-methods/kafka-streams/tron-streams",
                ],
            },
            "docs/access-methods/sdks",
            "docs/access-methods/cli",
        ], icon="plug"),
        group(lang, "ai_agents", [
            "docs/ai-agents/overview",
            {
                "group": L("mcp_server", lang),
                "pages": [
                    "docs/ai-agents/mcp-server/introduction",
                    "docs/ai-agents/mcp-server/setup",
                    "docs/ai-agents/mcp-server/tools",
                ],
            },
            {
                "group": L("agent_skills", lang),
                "pages": [
                    "docs/ai-agents/agent-skills/introduction",
                    "docs/ai-agents/agent-skills/installation",
                    "docs/ai-agents/agent-skills/chainstream-data",
                    "docs/ai-agents/agent-skills/chainstream-defi",
                ],
            },
        ], icon="robot"),
        group(lang, "compliance", [
            "docs/compliance/overview",
            "docs/compliance/kyt-concepts",
            "docs/compliance/kya-concepts",
            "docs/compliance/integration-guide",
        ], icon="shield-halved"),
        group(lang, "tutorials", [
            "docs/tutorials/build-price-alert-bot",
            "docs/tutorials/build-arbitrage-scanner",
            "docs/tutorials/smart-money-tracker",
            "docs/tutorials/integrate-deposit-check",
            "docs/tutorials/ai-agent-with-mcp",
        ], icon="graduation-cap"),
        group(lang, "recipes", [
            "docs/recipes/token-analysis-framework",
            "docs/recipes/defi-monitoring",
            "docs/recipes/webhook-fundamentals",
            "docs/recipes/pump-fun",
            "docs/recipes/raydium",
        ], icon="book"),
        group(lang, "platform", [
            {
                "group": L("auth", lang),
                "pages": [
                    "docs/platform/authentication/api-keys-oauth",
                    "docs/platform/authentication/wallet-auth-siwx",
                ],
            },
            {
                "group": L("billing_payments", lang),
                "pages": [
                    "docs/platform/billing-payments/plans-and-units",
                    "docs/platform/billing-payments/x402-payments",
                    "docs/platform/billing-payments/mpp-payments",
                ],
            },
            {
                "group": L("security", lang),
                "pages": [
                    "docs/platform/security/api-security",
                    "docs/platform/security/data-privacy",
                ],
            },
        ], icon="sliders"),
        group(lang, "ecosystem", [
            {
                "group": "OpenClaw",
                "pages": [
                    "docs/ecosystem/openclaw/overview",
                    "docs/ecosystem/openclaw/skills-install",
                    "docs/ecosystem/openclaw/cross-agent-compatibility",
                    "docs/ecosystem/openclaw/security",
                ],
            },
            {
                "group": "n8n",
                "pages": [
                    "docs/ecosystem/n8n/overview",
                    "docs/ecosystem/n8n/trigger-node",
                ],
            },
        ], icon="puzzle-piece"),
        group(lang, "reference_group", [
            "docs/reference/glossary",
            "docs/reference/error-codes",
            "docs/reference/faq",
        ], icon="book-bookmark"),
    ]


# -------------------------------------------------------------------
# API Reference tab navigation
# -------------------------------------------------------------------

REST_API_GROUPS = [
    ("rest_token", [
        "api-reference/endpoint/data/token/v2/token-search-get",
        "api-reference/endpoint/data/token/v2/token-chain-dev-devaddress-tokens-get",
        "api-reference/endpoint/data/token/v2/token-chain-list-get",
        "api-reference/endpoint/data/token/v2/token-chain-marketdata-multi-get",
        "api-reference/endpoint/data/token/v2/token-chain-metadata-multi-get",
        "api-reference/endpoint/data/token/v2/token-chain-multi-get",
        "api-reference/endpoint/data/token/v2/token-chain-pair-pair-candles-get",
        "api-reference/endpoint/data/token/v2/token-chain-pool-pooladdress-candles-get",
        "api-reference/endpoint/data/token/v2/token-chain-stats-multi-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-candles-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-creation-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-holders-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-holders-multi-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-liquiditysnapshots-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-marketdata-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-metadata-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-mintandburn-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-pools-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-price-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-prices-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-security-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-stats-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-topholders-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-traders-tag-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-transfer-total-get",
        "api-reference/endpoint/data/token/v2/token-chain-tokenaddress-transfers-get",
    ]),
    ("rest_trade", [
        "api-reference/endpoint/data/trade/v2/trade-chain-get",
        "api-reference/endpoint/data/trade/v2/trade-chain-activities-get",
        "api-reference/endpoint/data/trade/v2/trade-chain-top-traders-get",
        "api-reference/endpoint/data/trade/v2/trade-chain-trader-gainers-losers-get",
    ]),
    ("rest_wallet", [
        "api-reference/endpoint/data/wallet/v2/wallet-chain-first-tx-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-net-worth-summary-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-pnl-by-wallet-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-balance-updates-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-calculate-pnl-post",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-net-worth-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-net-worth-chart-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-net-worth-details-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-net-worth-tokens-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-pnl-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-pnl-by-token-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-pnl-details-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-tokens-balance-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-transfer-total-get",
        "api-reference/endpoint/data/wallet/v2/wallet-chain-walletaddress-transfers-get",
    ]),
    ("rest_dex_pool", [
        "api-reference/endpoint/data/dexpool/v2/dexpools-chain-pooladdress-get",
        "api-reference/endpoint/data/dexpool/v2/dexpools-chain-pooladdress-snapshots-get",
    ]),
    ("rest_ranking", [
        "api-reference/endpoint/data/ranking/v2/ranking-chain-finalstretch-get",
        "api-reference/endpoint/data/ranking/v2/ranking-chain-hottokens-duration-get",
        "api-reference/endpoint/data/ranking/v2/ranking-chain-migrated-get",
        "api-reference/endpoint/data/ranking/v2/ranking-chain-newtokens-get",
        "api-reference/endpoint/data/ranking/v2/ranking-chain-stocks-get",
    ]),
    ("rest_blockchain", [
        "api-reference/endpoint/data/blockchain/v2/blockchain-get",
        "api-reference/endpoint/data/blockchain/v2/blockchain-chain-latest_block-get",
    ]),
    ("rest_dex_registry", [
        "api-reference/endpoint/data/dex/v2/dex-get",
    ]),
    ("rest_kyt", [
        "api-reference/endpoint/data/kyt/v2/kyt-address-post",
        "api-reference/endpoint/data/kyt/v2/kyt-addresses-address-risk-get",
        "api-reference/endpoint/data/kyt/v2/kyt-transfer-post",
        "api-reference/endpoint/data/kyt/v2/kyt-transfers-transferid-alerts-get",
        "api-reference/endpoint/data/kyt/v2/kyt-transfers-transferid-exposures-direct-get",
        "api-reference/endpoint/data/kyt/v2/kyt-transfers-transferid-network-identifications-get",
        "api-reference/endpoint/data/kyt/v2/kyt-transfers-transferid-summary-get",
        "api-reference/endpoint/data/kyt/v2/kyt-withdrawal-post",
        "api-reference/endpoint/data/kyt/v2/kyt-withdrawal-withdrawalid-address-identifications-get",
        "api-reference/endpoint/data/kyt/v2/kyt-withdrawal-withdrawalid-alerts-get",
        "api-reference/endpoint/data/kyt/v2/kyt-withdrawal-withdrawalid-exposures-direct-get",
        "api-reference/endpoint/data/kyt/v2/kyt-withdrawal-withdrawalid-fraud-assessment-get",
        "api-reference/endpoint/data/kyt/v2/kyt-withdrawal-withdrawalid-network-identifications-get",
        "api-reference/endpoint/data/kyt/v2/kyt-withdrawal-withdrawalid-summary-get",
    ]),
    ("rest_dex_swap", [
        "api-reference/endpoint/defi/dex/v2/dex-chain-swap-post",
        "api-reference/endpoint/defi/dex/v2/dex-chain-route-post",
        "api-reference/endpoint/defi/dex/v2/dex-chain-quote-get",
        "api-reference/endpoint/defi/dex/v2/dex-chain-create-post",
    ]),
    ("rest_transaction", [
        "api-reference/endpoint/defi/transaction/v2/transaction-chain-send-post",
        "api-reference/endpoint/defi/transaction/v2/transaction-chain-gas-price-get",
        "api-reference/endpoint/defi/transaction/v2/transaction-chain-estimate-gas-limit-post",
    ]),
    ("rest_job", [
        "api-reference/endpoint/defi/job/v2/job-id-get",
        "api-reference/endpoint/defi/job/v2/job-id-streaming-get",
    ]),
    ("rest_watchlist", [
        "api-reference/endpoint/data/watchlist/v2/watchlist-chain-walletaddress-post",
    ]),
    ("rest_webhook", [
        "api-reference/endpoint/data/webhook/v2/webhook-endpoint-get",
        "api-reference/endpoint/data/webhook/v2/webhook-endpoint-post",
        "api-reference/endpoint/data/webhook/v2/webhook-endpoint-patch",
        "api-reference/endpoint/data/webhook/v2/webhook-endpoint-id-get",
        "api-reference/endpoint/data/webhook/v2/webhook-endpoint-id-delete",
        "api-reference/endpoint/data/webhook/v2/webhook-endpoint-id-secret-get",
        "api-reference/endpoint/data/webhook/v2/webhook-endpoint-id-secret-rotate-post",
    ]),
    ("rest_ipfs", [
        "api-reference/endpoint/data/ipfs/v2/ipfs-presign-post",
    ]),
    ("rest_redpacket", [
        "api-reference/endpoint/data/redpacket/v2/redpacket-get",
        "api-reference/endpoint/data/redpacket/v2/redpacket-wallet-address-claims-get",
        "api-reference/endpoint/data/redpacket/v2/redpacket-wallet-address-redpackets-get",
        "api-reference/endpoint/data/redpacket/v2/redpacket-chain-claim-post",
        "api-reference/endpoint/data/redpacket/v2/redpacket-chain-create-post",
        "api-reference/endpoint/data/redpacket/v2/redpacket-chain-send-post",
        "api-reference/endpoint/data/redpacket/v2/redpacket-id-get",
        "api-reference/endpoint/data/redpacket/v2/redpacket-id-claims-get",
    ]),
]


def api_ref_groups(lang: str) -> list[dict]:
    return [
        {
            "group": " ",
            "pages": prefix_pages(lang, [
                "api-reference/overview",
            ]),
        },
        group(lang, "api_authentication", [
            "api-reference/authentication/authenticate",
        ]),
        {
            "group": L("rest_api", lang),
            "icon": "bolt",
            "pages": [
                group(lang, label_key, pages)
                for label_key, pages in REST_API_GROUPS
            ],
        },
        group(lang, "websocket_api", [
            "api-reference/endpoint/websocket/introduction",
            "api-reference/endpoint/websocket/api",
            "api-reference/endpoint/websocket/timeouts-and-heartbeats",
        ], icon="tower-broadcast"),
        group(lang, "kafka_topics", [
            "api-reference/kafka-topics/evm",
            "api-reference/kafka-topics/solana",
            "api-reference/kafka-topics/tron",
        ], icon="bars-staggered"),
        group(lang, "cli_commands", [
            "api-reference/cli-commands/overview",
        ], icon="terminal"),
        group(lang, "mcp_tools", [
            "api-reference/mcp-tools/overview",
        ], icon="robot"),
    ]


# -------------------------------------------------------------------
# GraphQL tab
# -------------------------------------------------------------------

def graphql_groups(lang: str) -> list[dict]:
    return [
        group(lang, "graphql_getting_started", [
            "graphql/getting-started/overview",
            "graphql/getting-started/endpoints",
            "graphql/getting-started/first-query",
        ]),
        group(lang, "graphql_ide", [
            "graphql/ide/introduction",
            "graphql/ide/query-editor",
            "graphql/ide/query-templates",
            "graphql/ide/saved-queries",
            "graphql/ide/code-export",
        ], icon="code"),
        group(lang, "graphql_schema", [
            "graphql/schema/schema-overview",
            "graphql/schema/chain-groups",
            "graphql/schema/cubes",
            "graphql/schema/dataset-aggregates",
            "graphql/schema/filtering",
            "graphql/schema/ordering-pagination",
            "graphql/schema/metrics-aggregation",
        ], icon="diagram-project"),
        group(lang, "graphql_examples", [
            "graphql/examples/dex-trades",
            "graphql/examples/transfers",
            "graphql/examples/balance-holders",
            "graphql/examples/pools-liquidity",
            "graphql/examples/ohlc-stats",
            "graphql/examples/blocks-transactions",
            "graphql/examples/prediction-markets",
        ], icon="flask"),
        group(lang, "graphql_billing", [
            "graphql/billing/graphql-billing",
        ], icon="credit-card"),
    ]


# -------------------------------------------------------------------
# SDKs tab
# -------------------------------------------------------------------

def sdks_groups(lang: str) -> list[dict]:
    return [
        group(lang, "sdks", [
            "sdks/overview",
            "sdks/typescript",
            "sdks/python",
            "sdks/go",
            "sdks/rust",
        ]),
    ]


# -------------------------------------------------------------------
# Changelog tab
# -------------------------------------------------------------------

def changelog_groups(lang: str) -> list[dict]:
    return [
        group(lang, "changelog", [
            "changelog/index",
        ]),
    ]


# -------------------------------------------------------------------
# Assemble full docs.json
# -------------------------------------------------------------------

def build_docs_json() -> dict:
    def tab(name: str, groups_fn) -> dict:
        return {
            "tab": name,
            "languages": [
                {"language": lang, "groups": groups_fn(lang)}
                for lang in LANGS
            ],
        }

    return {
        "$schema": "https://mintlify.com/docs.json",
        "theme": "maple",
        "name": "ChainStream",
        "colors": {
            "primary": "#7438e5",
            "light": "#7438e5",
            "dark": "#7438e5",
        },
        "favicon": "./favicon.ico",
        "navigation": {
            "tabs": [
                tab("Docs", docs_groups),
                tab("API Reference", api_ref_groups),
                tab("GraphQL", graphql_groups),
                tab("SDKs", sdks_groups),
                tab("Changelog", changelog_groups),
            ],
            "global": {
                "anchors": [
                    {"anchor": "X",        "href": "https://x.com/chainstreamio",      "icon": "x-twitter"},
                    {"anchor": "Discord",  "href": "https://discord.gg/quhPXEkJ",       "icon": "discord"},
                    {"anchor": "Telegram", "href": "https://t.me/+lAhiZIa0zP40ZGU0",    "icon": "telegram"},
                    {"anchor": "Github",   "href": "https://github.com/chainstream-io", "icon": "github"},
                ]
            },
        },
        "logo": {
            "light": "/logo/light.png",
            "dark": "/logo/dark.png",
        },
        "navbar": {
            "primary": {
                "type": "button",
                "label": "Dashboard",
                "href": "https://www.chainstream.io/dashboard/statistics",
            },
            "links": [
                {"label": "Support", "href": "mailto:support@chainstream.io"},
                {"label": "Terms",   "href": "/en/legal/terms-of-service"},
                {"label": "Privacy", "href": "/en/legal/privacy-policy"},
            ],
        },
        "footer": {
            "socials": {
                "x-twitter": "https://x.com/chainstreamio",
                "discord":   "https://discord.gg/quhPXEkJ",
                "telegram":  "https://t.me/+lAhiZIa0zP40ZGU0",
                "linkedin":  "https://www.linkedin.com/company/chainstream-io",
            },
            "links": [
                {
                    "header": "Legal",
                    "items": [
                        {"label": "Terms of Service", "href": "/en/legal/terms-of-service"},
                        {"label": "Privacy Policy",   "href": "/en/legal/privacy-policy"},
                        {"label": "Contact Support",  "href": "/en/legal/contact-support"},
                    ],
                },
            ],
        },
        "redirects": build_redirects(),
        "contextual": {
            "options": ["claude", "chatgpt", "cursor", "vscode", "mcp", "copy", "view", "perplexity"],
        },
        "errors": {
            "404": {
                "redirect": True,
                "title": "Page Not Found",
                "description": "The page you're looking for doesn't exist. Visit our [Home](/en/docs/home) to get started.",
            }
        },
    }


# -------------------------------------------------------------------
# 301 redirects (old path -> new path)
# -------------------------------------------------------------------

# Each entry is (old_suffix, new_suffix) relative to /{lang}/.
# Generated for all 5 languages.
OLD_TO_NEW_SUFFIXES: list[tuple[str, str]] = [
    # Getting Started top-level
    ("guides/getting-started/overview",          "docs/home"),
    ("guides/getting-started/quickstart",        "docs/quickstart"),
    ("guides/getting-started/supported-chains",  "docs/supported-chains"),
    ("guides/getting-started/choosing-your-path", "docs/home"),
    ("guides/getting-started/api-comparison",    "docs/access-methods/overview"),
    ("guides/getting-started/authentication",    "docs/platform/authentication/api-keys-oauth"),
    ("guides/getting-started/billing-and-units", "docs/platform/billing-payments/plans-and-units"),
    ("guides/getting-started/x402-payments",     "docs/platform/billing-payments/x402-payments"),
    ("guides/getting-started/mpp-payments",      "docs/platform/billing-payments/mpp-payments"),
    ("guides/getting-started/wallet-auth-siwx",  "docs/platform/authentication/wallet-auth-siwx"),
    ("guides/getting-started/faq",               "docs/reference/faq"),

    # Data Concepts
    ("guides/data-concepts/realtime-streaming",       "docs/access-methods/websocket"),
    ("guides/data-concepts/smart-money-methodology",  "docs/data-products/smart-money"),
    ("guides/data-concepts/data-privacy",             "docs/platform/security/data-privacy"),
    ("guides/data-concepts/api-security",             "docs/platform/security/api-security"),
    ("guides/data-concepts/kyt-concepts",             "docs/compliance/kyt-concepts"),
    ("guides/data-concepts/kya-concepts",             "docs/compliance/kya-concepts"),
    ("guides/data-concepts/compliance-integration",   "docs/compliance/integration-guide"),
    ("guides/data-concepts/kafka-streams/overview",       "docs/access-methods/kafka-streams/overview"),
    ("guides/data-concepts/kafka-streams/evm-streams",    "docs/access-methods/kafka-streams/evm-streams"),
    ("guides/data-concepts/kafka-streams/solana-streams", "docs/access-methods/kafka-streams/solana-streams"),
    ("guides/data-concepts/kafka-streams/tron-streams",   "docs/access-methods/kafka-streams/tron-streams"),

    # AI Infrastructure -> AI Agents
    ("guides/ai-infrastructure/overview", "docs/ai-agents/overview"),
    ("guides/ai-infrastructure/mcp-server/introduction",          "docs/ai-agents/mcp-server/introduction"),
    ("guides/ai-infrastructure/mcp-server/setup-guide",           "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/self-hosted-installation", "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/stdio-transport",       "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/prompts-and-resources", "docs/ai-agents/mcp-server/setup"),
    ("guides/ai-infrastructure/mcp-server/tools-catalog",         "docs/ai-agents/mcp-server/tools"),
    ("guides/ai-infrastructure/mcp-server/tools-reference",       "docs/ai-agents/mcp-server/tools"),
    ("guides/ai-infrastructure/agent-skills/introduction",    "docs/ai-agents/agent-skills/introduction"),
    ("guides/ai-infrastructure/agent-skills/installation",    "docs/ai-agents/agent-skills/installation"),
    ("guides/ai-infrastructure/agent-skills/chainstream-data", "docs/ai-agents/agent-skills/chainstream-data"),
    ("guides/ai-infrastructure/agent-skills/chainstream-defi", "docs/ai-agents/agent-skills/chainstream-defi"),

    # CLI
    ("guides/cli/overview",       "docs/access-methods/cli"),
    ("guides/cli/authentication", "docs/platform/authentication/api-keys-oauth"),
    ("guides/cli/commands",       "api-reference/cli-commands/overview"),
    ("guides/cli/x402-payment",   "docs/platform/billing-payments/x402-payments"),

    # Security & Compliance
    ("guides/security-compliance/overview", "docs/compliance/overview"),

    # Integrations -> Ecosystem
    ("guides/integrations/openclaw/overview",                 "docs/ecosystem/openclaw/overview"),
    ("guides/integrations/openclaw/skills-install",           "docs/ecosystem/openclaw/skills-install"),
    ("guides/integrations/openclaw/cross-agent-compatibility", "docs/ecosystem/openclaw/cross-agent-compatibility"),
    ("guides/integrations/openclaw/security",                 "docs/ecosystem/openclaw/security"),
    ("guides/integrations/n8n/overview",     "docs/ecosystem/n8n/overview"),
    ("guides/integrations/n8n/trigger-node", "docs/ecosystem/n8n/trigger-node"),

    # Resources
    ("guides/resources/glossary",     "docs/reference/glossary"),
    ("guides/resources/error-codes",  "docs/reference/error-codes"),
    ("guides/resources/changelog",    "changelog/index"),

    # Legal (moved out of sidebar but kept reachable)
    ("guides/legal-policies/terms-of-service", "legal/terms-of-service"),
    ("guides/legal-policies/privacy-policy",   "legal/privacy-policy"),
    ("guides/legal-policies/contact-support",  "legal/contact-support"),

    # Playbooks -> Tutorials / Recipes
    ("playbooks/tutorials/smart-money-tracker",       "docs/tutorials/smart-money-tracker"),
    ("playbooks/tutorials/build-price-alert-bot",     "docs/tutorials/build-price-alert-bot"),
    ("playbooks/tutorials/build-arbitrage-scanner",   "docs/tutorials/build-arbitrage-scanner"),
    ("playbooks/tutorials/integrate-deposit-check",   "docs/tutorials/integrate-deposit-check"),
    ("playbooks/tutorials/ai-agent-with-mcp",         "docs/tutorials/ai-agent-with-mcp"),
    ("playbooks/frameworks/token-analysis-framework", "docs/recipes/token-analysis-framework"),
    ("playbooks/frameworks/defi-monitoring-overview", "docs/recipes/defi-monitoring"),
    ("playbooks/frameworks/webhook-fundamentals",     "docs/recipes/webhook-fundamentals"),
    ("playbooks/protocols/pump-fun",                  "docs/recipes/pump-fun"),
    ("playbooks/protocols/raydium",                   "docs/recipes/raydium"),
]


def build_redirects() -> list[dict]:
    out: list[dict] = []
    for lang in LANGS:
        for old, new in OLD_TO_NEW_SUFFIXES:
            out.append({
                "source": f"/{lang}/{old}",
                "destination": f"/{lang}/{new}",
                "permanent": True,
            })
    return out


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():
    out_path = Path(__file__).resolve().parent.parent / "docs.json"
    payload = build_docs_json()
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
