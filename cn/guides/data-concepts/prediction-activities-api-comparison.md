# Prediction Activities API 对比

本文记录 ChainStream prediction activities API 的调用方式、当前返回样本、futures.new 抓包样本，以及字段差异。

注意：产品上需要看的不是整个 `world-cup-winner` 专题的 activity feed，而是某一个 prediction / market 的 activity feed。`event_slug=world-cup-winner` 只是专题上下文，真正锁定单个预测应使用 `condition_id`。如果要进一步锁定 Yes / No 单个 outcome，再追加 `token_id`。

验证日期：2026-06-05  
ChainStream event：`world-cup-winner`  
ChainStream 目标 endpoint：`GET https://api.chainstream.io/v1/prediction/markets/{condition_id}/activities`
当前生产验证 endpoint：`GET https://api.chainstream.io/v1/prediction/events/{event_slug}/activities?condition_id={condition_id}`
服务端目标 endpoint PR：`https://github.com/chainstream-io/services/pull/30`

## ChainStream 调用方式

先通过 client credentials 获取 Bearer token，再调用 activities API。

```bash
export CHAINSTREAM_CLIENT_ID="..."
export CHAINSTREAM_CLIENT_SECRET="..."
export CHAINSTREAM_AUTH_URL="..."
export CHAINSTREAM_AUDIENCE="..."

TOKEN="$(
  curl -sS "$CHAINSTREAM_AUTH_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"grant_type\": \"client_credentials\",
      \"client_id\": \"$CHAINSTREAM_CLIENT_ID\",
      \"client_secret\": \"$CHAINSTREAM_CLIENT_SECRET\",
      \"audience\": \"$CHAINSTREAM_AUDIENCE\"
    }" | jq -r '.access_token'
)"

curl -sS \
  "https://api.chainstream.io/v1/prediction/markets/0x9b6fef249040fd17e9c107955b37ac2c3e923509b6b0ff01cc463a331ddeb894/activities?limit=1" \
  -H "Authorization: Bearer $TOKEN"
```

当前生产环境在 PR #30 merge、tag、部署前，可用 event endpoint 加 `condition_id` 作为兼容验证方式：

```bash
curl -sS \
  "https://api.chainstream.io/v1/prediction/events/world-cup-winner/activities?condition_id=0x9b6fef249040fd17e9c107955b37ac2c3e923509b6b0ff01cc463a331ddeb894&limit=1" \
  -H "Authorization: Bearer $TOKEN"
```

目标 market endpoint 支持的 query 参数：

| 参数 | 说明 |
|---|---|
| `cursor` | 上一页返回的 cursor，用于继续分页 |
| `limit` | 返回条数，当前接口支持 clamp 到服务端上限 |
| `token_id` | 按 outcome token id 过滤 |
| `wallet` | 按 taker wallet 过滤 |
| `activity_type` | `buy` / `sell` / `redeem` / `inventory_adjust` |
| `order` | `desc` 或 `asc` |

event endpoint 额外兼容 `market_id` / `condition_id` query 参数，用于从专题 feed 中过滤单个 prediction。

推荐调用口径：

| 使用场景 | 调用方式 |
|---|---|
| 某个 prediction / market 的全部 activity | `GET /v1/prediction/markets/{condition_id}/activities` |
| 某个 prediction / market 的某个 outcome activity | `GET /v1/prediction/markets/{condition_id}/activities?token_id={token_id}` |
| PR #30 部署前的生产兼容调用 | `GET /v1/prediction/events/{event_slug}/activities?condition_id={condition_id}` |
| 整个 event / topic feed | `GET /v1/prediction/events/{event_slug}/activities`，仅用于专题聚合，不建议作为单个预测页数据源 |

## ChainStream 返回样本

目标请求：

```http
GET /v1/prediction/markets/0x9b6fef249040fd17e9c107955b37ac2c3e923509b6b0ff01cc463a331ddeb894/activities?limit=1
```

当前生产验证请求：

```http
GET /v1/prediction/events/world-cup-winner/activities?condition_id=0x9b6fef249040fd17e9c107955b37ac2c3e923509b6b0ff01cc463a331ddeb894&limit=1
```

返回：

```json
{
  "eventSlug": "world-cup-winner",
  "cursor": "WyIxNzgwNjAwMzMwMDAwMDAwMTciLCIweDcwN2U1NmQ5NWMyODgwMTZhYmVjZDg5ZmY0OTFkNzQ0MDg3Mjc5ZDI4ZjljODI3Y2RjNDFiZWIwNDM2MDg5M2M6MTY6MzIyNzA0MTE2OTQ1MjM1Mzk0OTUyNjIzMDM4Njg2Mjk0Nzc4NjEwMTc4Mjk3MjIyODI1NzY0NTgwMzE4MTUzMzM0ODYzNjgyMzk1NDQ6aW52ZW50b3J5X2FkanVzdCJd",
  "limit": 1,
  "order": "desc",
  "retentionDays": 3,
  "activities": [
    {
      "activityId": "0x707e56d95c288016abecd89ff491d744087279d28f9c827cdc41beb04360893c:16:32270411694523539495262303868629477861017829722282576458031815333486368239544:inventory_adjust",
      "amount": "1061.432325",
      "assetIds": [
        "108233603819467706476318984012158651931658302669301887462181073562758483842092",
        "32270411694523539495262303868629477861017829722282576458031815333486368239544"
      ],
      "blockNumber": 87930230,
      "conditionId": "0x9b6fef249040fd17e9c107955b37ac2c3e923509b6b0ff01cc463a331ddeb894",
      "eventSlug": "world-cup-winner",
      "logIndex": 16,
      "marketIcon": "https://polymarket-upload.s3.us-east-2.amazonaws.com/world-cup-winner-france-flag-20260603-192743.png",
      "marketId": "558936",
      "marketQuestion": "Will France win the 2026 FIFA World Cup?",
      "outcome": "No",
      "outcomes": [
        "Yes",
        "No"
      ],
      "price": "0",
      "quantity": "1061.432325",
      "seqIndex": 178060033000000017,
      "source": "chainstream",
      "taker": "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296",
      "takerAge": 0,
      "takerImage": "",
      "takerName": "",
      "takerOrderHash": "",
      "takerPseudonym": "",
      "takerTags": [],
      "timestamp": 1780600330000,
      "tokenId": "32270411694523539495262303868629477861017829722282576458031815333486368239544",
      "txHash": "0x707e56d95c288016abecd89ff491d744087279d28f9c827cdc41beb04360893c",
      "type": "inventory_adjust"
    }
  ]
}
```

## futures.new 返回样本

样本来源：本地 Future.news 抓包样本，调用口径为 `event_slug=world-cup-winner`、`market_id=0x9b6fef249040fd17e9c107955b37ac2c3e923509b6b0ff01cc463a331ddeb894`、`token_id=108233603819467706476318984012158651931658302669301887462181073562758483842092`。

返回：

```json
{
  "code": 0,
  "reason": "",
  "message": "success",
  "data": {
    "activities": [
      {
        "taker": "0xc0066bf4d562183a49f4570f5b68ecd962d65d0b",
        "taker_name": "0xc0066BF4D562183A49f4570F5B68ecD962d65d0b-1780174254021",
        "taker_pseudonym": "Surprised-Bugle",
        "taker_image": "",
        "taker_age": 1780174594000,
        "type": "sell",
        "event_slug": "world-cup-winner",
        "asset_ids": null,
        "outcomes": null,
        "market_id": "0x9b6fef249040fd17e9c107955b37ac2c3e923509b6b0ff01cc463a331ddeb894",
        "market_question": "Will France win the 2026 FIFA World Cup?",
        "market_icon": "",
        "token_id": "108233603819467706476318984012158651931658302669301887462181073562758483842092",
        "outcome": "Yes",
        "quantity": "6",
        "amount": "1.02",
        "taker_order_hash": "0xc85b977249aa57b9da846937b90e2e7f9b7aaf724715b6cb7bee47655d1cf259",
        "seq_index": 87812400001579,
        "block_number": 0,
        "tx_hash": "0x9ab944b84e19d6d64cdf3f94f7c355ff2f77d6d64ed1ff363fcffd3a645c0f7a",
        "timestamp": 1780411421000,
        "price": "0.17",
        "taker_tags": [
          "fresh_wallet"
        ]
      }
    ],
    "cursor": "ODc4MTE4OTAwMDA2NjM="
  }
}
```

## 顶层结构差异

| 对比项 | ChainStream | futures.new |
|---|---|---|
| HTTP envelope | 直接返回业务对象 | 外层为 `code` / `reason` / `message` / `data` |
| activities 路径 | `activities` | `data.activities` |
| cursor 路径 | `cursor` | `data.cursor` |
| event slug | `eventSlug` | activity 内的 `event_slug` |
| prediction / market id | path `{condition_id}`，响应 `conditionId` / `marketId`；生产兼容调用也支持 query `condition_id` | query `market_id`，响应 `market_id` |
| limit | `limit` | 未在样本顶层返回 |
| order | `order` | 未在样本顶层返回 |
| 数据保留说明 | `retentionDays` | 未在样本顶层返回 |
| 字段命名风格 | `camelCase` | `snake_case` |

## Activity 字段对比

| futures.new 字段 | ChainStream 字段 | 状态 | 说明 |
|---|---|---|---|
| `taker` | `taker` | 对齐 | taker wallet |
| `taker_name` | `takerName` | 对齐 | 缺失时返回 `""` |
| `taker_pseudonym` | `takerPseudonym` | 对齐 | 缺失时返回 `""` |
| `taker_image` | `takerImage` | 对齐 | 缺失时返回 `""` |
| `taker_age` | `takerAge` | 对齐 | 数字 |
| `type` | `type` | 对齐 | `buy` / `sell` / `redeem` / `inventory_adjust` |
| `event_slug` | `eventSlug` | 对齐 | 当前 Day2 支持 `world-cup-winner` |
| `asset_ids` | `assetIds` | 对齐 | futures 样本为 `null`，ChainStream 可返回数组 |
| `outcomes` | `outcomes` | 对齐 | futures 样本为 `null`，ChainStream 可返回数组 |
| `market_id` | `marketId` / `conditionId` | 语义拆分 | futures 样本里的 `market_id` 是 condition id 风格；ChainStream 同时返回 numeric `marketId` 和 hex `conditionId` |
| `market_question` | `marketQuestion` | 对齐 | 市场问题 |
| `market_icon` | `marketIcon` | 对齐 | 缺失时返回 `""` |
| `token_id` | `tokenId` | 对齐 | outcome token id |
| `outcome` | `outcome` | 对齐 | 如 `Yes` / `No` |
| `quantity` | `quantity` | 对齐 | 字符串 |
| `amount` | `amount` | 对齐 | 字符串 |
| `taker_order_hash` | `takerOrderHash` | 对齐 | settlement 或 inventory 类 activity 可能返回 `""` |
| `seq_index` | `seqIndex` | 对齐 | 排序和 cursor 使用 |
| `block_number` | `blockNumber` | 对齐 | ChainStream 返回链上 block number；futures 样本为 `0` |
| `tx_hash` | `txHash` | 对齐 | 交易 hash |
| `timestamp` | `timestamp` | 对齐 | 毫秒时间戳 |
| `price` | `price` | 对齐 | 字符串 |
| `taker_tags` | `takerTags` | 对齐 | 缺失时返回 `[]` |

## ChainStream 额外字段

| ChainStream 字段 | futures.new 是否存在 | 说明 |
|---|---|---|
| `activityId` | 否 | activity 唯一 ID，用于去重和幂等 |
| `conditionId` | 否 | Polymarket condition id |
| `logIndex` | 否 | 链上 log index |
| `source` | 否 | 数据来源，当前为 `chainstream` |

## 数量对比

| 对比项 | ChainStream | futures.new |
|---|---:|---:|
| activity item 字段数 | 27 | 23 |
| futures.new 字段映射缺失 | 0 | - |
| ChainStream 额外字段数 | 4 | - |

## 差异结论

1. ChainStream activity 字段集合覆盖 futures.new activity 字段集合，按命名映射后缺失字段为 `[]`。
2. ChainStream 使用 `camelCase`，futures.new 使用 `snake_case`。
3. ChainStream 顶层不返回 `code/reason/message/data` wrapper，而是直接返回业务对象。
4. ChainStream 多返回 `activityId`、`conditionId`、`logIndex`、`source`，便于去重、链上追溯和数据来源标识。
5. `market_id` 语义需要注意：futures.new 样本里是 condition id 风格；ChainStream 拆成 `marketId` 和 `conditionId`，语义更明确。
6. 单个预测页目标接口为 `/v1/prediction/markets/{condition_id}/activities`；如果要和 futures.new 的 outcome tab 完全一致，再追加 `token_id`。
7. 当前生产最新两页普通 cursor 分页无重复；深分页重复 `activityId` 已定位，services 修复 PR 为 `https://github.com/chainstream-io/services/pull/29`，market-level endpoint PR 为 `https://github.com/chainstream-io/services/pull/30`，均待 review 后再 merge、tag、部署和复测。
