// ============================================================
// GLOBAL
// ============================================================

GLOBAL.CHAIN.NAME='chain'
GLOBAL.CHAIN.DESCRIPTION='A chain name listed in supported networks'
GLOBAL.USERADDRESS.NAME='userAddress'
GLOBAL.USERADDRESS.DESCRIPTION='An address of a user'

// ============================================================
// CONTROLLERS - Legacy (v1)
// ============================================================

// DEX CONTROLLER
CONTROLLER.DEX.SWAP.SUMMARY='Dex - Swap'
CONTROLLER.DEX.SWAP.DESCRIPTION='Swap parameters including input token, output token, amount and slippage'
CONTROLLER.DEX.ROUTE.SUMMARY='Dex - Route'
CONTROLLER.DEX.ROUTE.DESCRIPTION='Calculate the best route for token swap considering price impact and fees. Returns the optimal path and a prepared transaction.'
CONTROLLER.DEX.QUOTE.SUMMARY='Dex - Get Quote'
CONTROLLER.DEX.QUOTE.DESCRIPTION='Get DEX trading quote information'
CONTROLLER.DEX.CREATE.SUMMARY='Dex - Create Token'
CONTROLLER.DEX.CREATE.DESCRIPTION='Create a new token on the specified DEX'

// TRANSACTION CONTROLLER
CONTROLLER.TRANSACTION.SEND.SUMMARY='Transaction - Send'
CONTROLLER.TRANSACTION.SEND.DESCRIPTION='Submit a signed transaction to the blockchain'
CONTROLLER.TRANSACTION.SEND.BODY='Transaction parameters'
CONTROLLER.TRANSACTION.GET_GAS_PRICE.SUMMARY='Transaction - Gas Price'
CONTROLLER.TRANSACTION.GET_GAS_PRICE.DESCRIPTION='Get the current gas price for an EVM chain'
CONTROLLER.TRANSACTION.ESTIMATE_GAS_LIMIT.SUMMARY='Transaction - Estimate Gas Limit'
CONTROLLER.TRANSACTION.ESTIMATE_GAS_LIMIT.DESCRIPTION='Estimate the gas limit for an EVM transaction'
CONTROLLER.TRANSACTION.ESTIMATE_GAS_LIMIT.BODY='Gas estimation parameters'

// JOB CONTROLLER
CONTROLLER.JOB.GET.SUMMARY='Job - Get'
CONTROLLER.JOB.GET.DESCRIPTION='Retrieve the current status and result of a job by its ID'
CONTROLLER.JOB.GET.ID='Job identifier'
CONTROLLER.JOB.GET.RESPONSE='Job status retrieved successfully'
CONTROLLER.JOB.STREAMING.SUMMARY='Job - Streaming'
CONTROLLER.JOB.STREAMING.DESCRIPTION='Subscribe to real-time job status updates via Server-Sent Events (SSE). The connection will remain open until the job completes or an error occurs'
CONTROLLER.JOB.STREAMING.RESPONSE='SSE stream established successfully'

// ============================================================
// CONTROLLERS - v2
// ============================================================

// SWAP AGGREGATOR CONTROLLER (defi/v2/swap-aggregator)
CONTROLLER.SWAP_AGGREGATOR.CHAINS.SUMMARY='Swap Aggregator - Supported Chains'
CONTROLLER.SWAP_AGGREGATOR.CHAINS.DESCRIPTION='Get list of supported chains for a swap aggregator provider'
CONTROLLER.SWAP_AGGREGATOR.TOKENS.SUMMARY='Swap Aggregator - Supported Tokens'
CONTROLLER.SWAP_AGGREGATOR.TOKENS.DESCRIPTION='Get list of supported tokens for a swap aggregator provider'
CONTROLLER.SWAP_AGGREGATOR.DEXES.SUMMARY='Swap Aggregator - Supported DEXes'
CONTROLLER.SWAP_AGGREGATOR.DEXES.DESCRIPTION='Get list of supported DEXes for a swap aggregator provider'
CONTROLLER.SWAP_AGGREGATOR.QUOTE.SUMMARY='Swap Aggregator - Quote'
CONTROLLER.SWAP_AGGREGATOR.QUOTE.DESCRIPTION='Get a quote for token swap through aggregator'
CONTROLLER.SWAP_AGGREGATOR.SWAP.SUMMARY='Swap Aggregator - Swap'
CONTROLLER.SWAP_AGGREGATOR.SWAP.DESCRIPTION='Execute a token swap through aggregator'

// SWAP CONTROLLER (defi/v2/swap)
CONTROLLER.SWAP.CHAINS.SUMMARY='Swap - Supported Chains'
CONTROLLER.SWAP.CHAINS.DESCRIPTION='Get list of supported chains for a swap provider'
CONTROLLER.SWAP.TOKENS.SUMMARY='Swap - Supported Tokens'
CONTROLLER.SWAP.TOKENS.DESCRIPTION='Get list of supported tokens for a swap provider'
CONTROLLER.SWAP.QUOTE.SUMMARY='Swap - Quote'
CONTROLLER.SWAP.QUOTE.DESCRIPTION='Get a quote for direct DEX swap'
CONTROLLER.SWAP.SWAP.SUMMARY='Swap - Execute'
CONTROLLER.SWAP.SWAP.DESCRIPTION='Execute a direct DEX swap'

// BRIDGE CONTROLLER (defi/v2/bridge)
CONTROLLER.BRIDGE.CHAINS.SUMMARY='Bridge - Supported Chains'
CONTROLLER.BRIDGE.CHAINS.DESCRIPTION='Get list of supported chains for bridge'
CONTROLLER.BRIDGE.TOKENS.SUMMARY='Bridge - Supported Tokens'
CONTROLLER.BRIDGE.TOKENS.DESCRIPTION='Get list of supported tokens for bridge'
CONTROLLER.BRIDGE.QUOTE.SUMMARY='Bridge - Quote'
CONTROLLER.BRIDGE.QUOTE.DESCRIPTION='Get a quote for cross-chain bridge'
CONTROLLER.BRIDGE.SWAP_AND_BRIDGE.SUMMARY='Bridge - Swap and Bridge'
CONTROLLER.BRIDGE.SWAP_AND_BRIDGE.DESCRIPTION='Execute a swap and bridge operation'

// BRIDGE AGGREGATOR CONTROLLER (defi/v2/bridge-aggregator)
CONTROLLER.BRIDGE_AGGREGATOR.CHAINS.SUMMARY='Bridge Aggregator - Supported Chains'
CONTROLLER.BRIDGE_AGGREGATOR.CHAINS.DESCRIPTION='Get list of supported chains for bridge aggregator'
CONTROLLER.BRIDGE_AGGREGATOR.TOKENS.SUMMARY='Bridge Aggregator - Supported Tokens'
CONTROLLER.BRIDGE_AGGREGATOR.TOKENS.DESCRIPTION='Get list of supported tokens for bridge aggregator'
CONTROLLER.BRIDGE_AGGREGATOR.ROUTE.SUMMARY='Bridge Aggregator - Route'
CONTROLLER.BRIDGE_AGGREGATOR.ROUTE.DESCRIPTION='Get optimal route for cross-chain bridge'
CONTROLLER.BRIDGE_AGGREGATOR.QUOTE.SUMMARY='Bridge Aggregator - Quote'
CONTROLLER.BRIDGE_AGGREGATOR.QUOTE.DESCRIPTION='Get a quote for cross-chain bridge through aggregator'

// LAUNCHPAD CONTROLLER (defi/v2/launchpad)
CONTROLLER.LAUNCHPAD.QUOTE.SUMMARY='Launchpad - Quote'
CONTROLLER.LAUNCHPAD.QUOTE.DESCRIPTION='Get a quote for launchpad token swap'
CONTROLLER.LAUNCHPAD.SWAP.SUMMARY='Launchpad - Swap'
CONTROLLER.LAUNCHPAD.SWAP.DESCRIPTION='Execute a launchpad token swap'
CONTROLLER.LAUNCHPAD.CREATE_AND_BUY.SUMMARY='Launchpad - Create and Buy'
CONTROLLER.LAUNCHPAD.CREATE_AND_BUY.DESCRIPTION='Create a new token and execute initial buy on launchpad'

// TX RELAY CONTROLLER (defi/v2/tx-relay)
CONTROLLER.TX_RELAY.ESTIMATE.SUMMARY='Tx Relay - Estimate Gas'
CONTROLLER.TX_RELAY.ESTIMATE.DESCRIPTION='Estimate gas cost for a transaction'
CONTROLLER.TX_RELAY.SEND.SUMMARY='Tx Relay - Send Transaction'
CONTROLLER.TX_RELAY.SEND.DESCRIPTION='Send a signed transaction through relay'

// ============================================================
// DTOs - Legacy (v1)
// ============================================================

// DEX DTO
DTO.DEX.IDENTIFIER='DEX identifier for the trade'
DTO.DEX.WALLET='Public key of the wallet initiating the transaction'
DTO.DEX.PROGRAM_ADDRESS='DEX program address'
DTO.DEX.NAME='Dex name'
DTO.DEX.CHAIN='Blockchain'
DTO.DEX.IMAGE='DEX logo image URL'
DTO.DEX.PROTOCOL_FAMILY='DEX protocol family'

// DEX SWAP DTO
DTO.DEX.SWAP.INPUT_MINT='Input token mint address'
DTO.DEX.SWAP.OUTPUT_MINT='Output token mint address'
DTO.DEX.SWAP.AMOUNT='Amount to swap. Use "auto" for full balance or percentage like "50%"'
DTO.DEX.SWAP.MODE='Swap direction mode'
DTO.DEX.SWAP.SLIPPAGE='Slippage tolerance percentage'
DTO.DEX.SWAP.POOL_ADDRESS='DEX pool address'
DTO.DEX.SWAP.SERIALIZED_TX='Base64 encoded transaction'
DTO.DEX.SWAP.ELAPSED_TIME='Time taken to process the request in milliseconds'
DTO.DEX.SWAP.ARGS='Original swap request parameters'
DTO.DEX.SWAP.ROUTE_INFO='Detailed routing information'
DTO.DEX.SWAP.RECIPIENT_ADDRESS='Recipient wallet address for the swap'
DTO.DEX.SWAP.PERMIT='Permit data for the swap'
DTO.DEX.SWAP.DEADLINE='Swap deadline timestamp'

// DEX SWAP ROUTE INFO DTO
DTO.DEX.SWAP.ROUTE.CHAIN='Blockchain network for the swap'
DTO.DEX.SWAP.ROUTE.DEX='DEX identifier for the swap'
DTO.DEX.SWAP.ROUTE.SLIPPAGE='Slippage tolerance percentage'
DTO.DEX.SWAP.ROUTE.INPUT_MINT='Input token mint address'
DTO.DEX.SWAP.ROUTE.OUTPUT_MINT='Output token mint address'
DTO.DEX.SWAP.ROUTE.AMOUNT='Amount to swap'
DTO.DEX.SWAP.ROUTE.SWAP_MODE='Swap direction mode (ExactIn or ExactOut)'

// DEX MINT DTO
DTO.DEX.MINT.NAME='Name of the token to be created'
DTO.DEX.MINT.SYMBOL='Token symbol/ticker'
DTO.DEX.MINT.ADDRESS='Token mint address that requires signature for the transaction'
DTO.DEX.MINT.URI='URI for token metadata (usually points to image or JSON)'
DTO.DEX.MINT.IMAGE='Token image URL (Base64 or HTTPS)'
DTO.DEX.MINT.SERIALIZED_TX='Base64 encoded transaction'
DTO.DEX.MINT.ELAPSED_TIME='Time taken to process the request in milliseconds'
DTO.DEX.MINT.EXTRA='Additional metadata about the created token'
DTO.DEX.MINT.MINT_ADDRESS='Token mint address that requires signature for the transaction'

// DEX BASE DTO
DTO.DEX.BASE.PRIORITY_FEE='Priority fee in SOL to increase transaction processing speed'
DTO.DEX.BASE.IS_ANTI_MEV='Whether to enable anti-MEV protection'
DTO.DEX.BASE.IS_ANTE_MEV='true'
DTO.DEX.BASE.TIP_FEE='Tip fee in SOL to increase transaction processing speed'

// DEX QUOTE DTO
DTO.DEX.QUOTE.DEX='DEX protocol type'
DTO.DEX.QUOTE.AMOUNT='Trading amount'
DTO.DEX.QUOTE.INPUT_MINT='Input token address'
DTO.DEX.QUOTE.OUTPUT_MINT='Output token address'
DTO.DEX.QUOTE.EXACT_IN='Exact input mode'
DTO.DEX.QUOTE.SLIPPAGE='Slippage tolerance'
DTO.DEX.QUOTE.AMOUNT_OUT='Output amount'
DTO.DEX.QUOTE.MIN_AMOUNT_OUT='Minimum output amount'
DTO.DEX.QUOTE.CURRENT_PRICE='Current price'
DTO.DEX.QUOTE.EXECUTION_PRICE='Execution price'
DTO.DEX.QUOTE.PRICE_IMPACT='Price impact'
DTO.DEX.QUOTE.FEE='Trading fee'

// DEX CREATE TOKEN DTO
DTO.DEX.CREATE_TOKEN.SERIALIZED_TX='Base64 encoded transaction for token creation'
DTO.DEX.CREATE_TOKEN.MINT_ADDRESS='Token mint address that requires signature for the transaction'

// TRANSACTION DTO
DTO.TRANSACTION.SEND.SIGNED_TX='Base64 encoded signed transaction'
DTO.TRANSACTION.SEND.SUBMIT_TYPE='Transaction submission method'
DTO.TRANSACTION.SEND.SIGNATURE='Transaction signature/hash'
DTO.TRANSACTION.SEND.ELAPSED_TIME='Transaction processing time in milliseconds'
DTO.TRANSACTION.SEND.JOB_ID='job id'
DTO.TRANSACTION.SEND.OPTIONS='jito | direct'

// JOB DTO
DTO.JOB.STATE='Job state'
DTO.JOB.RESULT='Job result'
DTO.JOB.STREAMING.ID='Streaming job ID'
DTO.JOB.STREAMING.DATA='Streaming data'

// ============================================================
// DTOs - v2
// ============================================================

// SWAP AGGREGATOR DTO
DTO.SWAP_AGGREGATOR.PROVIDER_ID='Swap aggregator provider identifier'
DTO.SWAP_AGGREGATOR.CHAIN_FAMILY='Chain family (evm or svm)'
DTO.SWAP_AGGREGATOR.CHAIN_ID='Chain ID for EVM chains'
DTO.SWAP_AGGREGATOR.IN_TOKEN='Input token address'
DTO.SWAP_AGGREGATOR.OUT_TOKEN='Output token address'
DTO.SWAP_AGGREGATOR.AMOUNT='Swap amount'
DTO.SWAP_AGGREGATOR.SLIPPAGE_BPS='Slippage tolerance in basis points'
DTO.SWAP_AGGREGATOR.SWAP_MODE='Swap direction mode'
DTO.SWAP_AGGREGATOR.ROUTE_INFO='Route information from quote'
DTO.SWAP_AGGREGATOR.USER_PUBLIC_KEY='User public key for SVM'
DTO.SWAP_AGGREGATOR.ACCOUNT='User account address'
DTO.SWAP_AGGREGATOR.GAS_PRICE='Gas price for EVM'
DTO.SWAP_AGGREGATOR.EXTRA='Additional parameters'

// SWAP DTO
DTO.SWAP.PROVIDER_ID='Swap provider identifier'
DTO.SWAP.CHAIN='Chain reference'
DTO.SWAP.IN_TOKEN='Input token address'
DTO.SWAP.OUT_TOKEN='Output token address'
DTO.SWAP.AMOUNT='Swap amount'
DTO.SWAP.SLIPPAGE_BPS='Slippage tolerance in basis points'
DTO.SWAP.ACCOUNT='User account address'

// BRIDGE DTO
DTO.BRIDGE.PROVIDER_ID='Bridge provider identifier'
DTO.BRIDGE.FROM_CHAIN='Source chain'
DTO.BRIDGE.TO_CHAIN='Destination chain'
DTO.BRIDGE.FROM_TOKEN='Source token address'
DTO.BRIDGE.TO_TOKEN='Destination token address'
DTO.BRIDGE.FROM_ADDRESS='Sender address'
DTO.BRIDGE.FROM_AMOUNT='Amount to bridge'
DTO.BRIDGE.TO_ADDRESS='Recipient address'
DTO.BRIDGE.SLIPPAGE_BPS='Slippage tolerance in basis points'

// BRIDGE AGGREGATOR DTO
DTO.BRIDGE_AGGREGATOR.PROVIDER_ID='Bridge aggregator provider identifier'
DTO.BRIDGE_AGGREGATOR.FROM_CHAIN_ID='Source chain ID'
DTO.BRIDGE_AGGREGATOR.TO_CHAIN_ID='Destination chain ID'
DTO.BRIDGE_AGGREGATOR.FROM_TOKEN='Source token address'
DTO.BRIDGE_AGGREGATOR.TO_TOKEN='Destination token address'
DTO.BRIDGE_AGGREGATOR.FROM_ADDRESS='Sender address'
DTO.BRIDGE_AGGREGATOR.FROM_AMOUNT='Amount to bridge'
DTO.BRIDGE_AGGREGATOR.TO_ADDRESS='Recipient address'
DTO.BRIDGE_AGGREGATOR.SLIPPAGE_BPS='Slippage tolerance in basis points'
DTO.BRIDGE_AGGREGATOR.INTEGRATOR='Integrator identifier'

// LAUNCHPAD DTO
DTO.LAUNCHPAD.PROVIDER_ID='Launchpad provider identifier'
DTO.LAUNCHPAD.IN_TOKEN='Input token address'
DTO.LAUNCHPAD.OUT_TOKEN='Output token address'
DTO.LAUNCHPAD.AMOUNT='Swap amount'
DTO.LAUNCHPAD.SLIPPAGE_BPS='Slippage tolerance in basis points'
DTO.LAUNCHPAD.SWAP_MODE='Swap direction mode'
DTO.LAUNCHPAD.ACCOUNT='User account address'
DTO.LAUNCHPAD.MINT_ADDRESS='Token mint address'
DTO.LAUNCHPAD.NAME='Token name'
DTO.LAUNCHPAD.SYMBOL='Token symbol'
DTO.LAUNCHPAD.URI='Token metadata URI'

// TX RELAY DTO
DTO.TX_RELAY.CHAIN='Chain reference'
DTO.TX_RELAY.EVM_TRANSACTION='EVM transaction data'
DTO.TX_RELAY.SVM_TRANSACTION='SVM transaction data'
DTO.TX_RELAY.SIGNED_TRANSACTION='Signed transaction data'
