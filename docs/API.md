# REST API ドキュメント

遊戯王デュエルリンクス カードデータベースの REST API 仕様です。

## 基本情報

- **ベースURL**: `http://localhost:5000/api`
- **レスポンス形式**: JSON
- **文字コード**: UTF-8

## エンドポイント一覧

### ヘルスチェック

#### GET /health

APIサーバーの稼働状況を確認します。

**レスポンス:**

```json
{
  "status": "ok",
  "timestamp": "2026-08-30T12:34:56.789Z"
}
```

---

## カード検索

### GET /cards/search

カードを複数の条件で検索します。

**クエリパラメータ:**

| パラメータ | 型 | 説明 | 例 |
|-----------|-----|------|-----|
| name | string | カード名（部分一致） | `Blue-Eyes` |
| type | string | カードタイプ | `Synchro Monster` |
| race | string | 種族 | `Dragon` |
| attribute | string | 属性 | `Light` |
| rarity | string | レアリティ | `Ultra Rare` |
| archetype | string | アーキタイプ | `Blue-Eyes` |
| limit | integer | 取得件数（最大100） | `20` |
| offset | integer | オフセット | `0` |

**リクエスト例:**

```bash
curl "http://localhost:5000/api/cards/search?name=Blue-Eyes&limit=20&offset=0"
```

**レスポンス:**

```json
{
  "success": true,
  "data": [
    {
      "id": 25955692,
      "name": "Blue-Eyes White Dragon",
      "type": "Normal Monster",
      "race": "Dragon",
      "attribute": "Light",
      "level": 8,
      "atk": 3000,
      "def": 2500,
      "description": "This legendary dragon is white...",
      "rarity": "Ultra Rare",
      "archetype": "Blue-Eyes",
      "scale": null,
      "linkval": null,
      "created_at": "2026-08-30T12:00:00Z",
      "updated_at": "2026-08-30T12:00:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

### GET /cards/{id}

特定のカードの詳細情報を取得します。

**パスパラメータ:**

| パラメータ | 型 | 説明 |
|-----------|-----|------|
| id | integer | カードID |

**リクエスト例:**

```bash
curl "http://localhost:5000/api/cards/25955692"
```

**レスポンス:**

```json
{
  "success": true,
  "data": {
    "id": 25955692,
    "name": "Blue-Eyes White Dragon",
    "type": "Normal Monster",
    "race": "Dragon",
    "attribute": "Light",
    "level": 8,
    "atk": 3000,
    "def": 2500,
    "description": "This legendary dragon is white...",
    "rarity": "Ultra Rare",
    "archetype": "Blue-Eyes",
    "scale": null,
    "linkval": null,
    "created_at": "2026-08-30T12:00:00Z",
    "updated_at": "2026-08-30T12:00:00Z",
    "images": [
      {
        "id": 1,
        "card_id": 25955692,
        "image_url": "https://example.com/images/25955692.jpg",
        "image_url_small": "https://example.com/images/25955692_small.jpg"
      }
    ],
    "sets": [
      {
        "id": 1,
        "card_id": 25955692,
        "set_name": "Starter Deck",
        "set_code": "SDY-006",
        "set_rarity": "Super Rare",
        "set_price": 25.99
      }
    ],
    "tags": ["monster", "dragon", "synchro"],
    "link_markers": []
  }
}
```

---

## フィルター検索

### POST /cards/filter

複数の条件でカードをフィルター検索します。

**リクエストボディ:**

```json
{
  "filters": {
    "type": ["Synchro Monster", "XYZ Monster"],
    "attribute": ["Light", "Water"],
    "level": {
      "min": 4,
      "max": 8
    },
    "atk": {
      "min": 2000,
      "max": 3000
    },
    "def": {
      "min": 1500,
      "max": 2500
    }
  },
  "limit": 50,
  "offset": 0
}
```

**レスポンス:**

```json
{
  "success": true,
  "data": [
    {
      "id": 12345678,
      "name": "Sample Card",
      ...
    }
  ],
  "pagination": {
    "total": 125,
    "limit": 50,
    "offset": 0,
    "hasMore": true
  }
}
```

---

## 統計情報

### GET /cards/stats

カード統計情報を取得します。

**レスポンス:**

```json
{
  "success": true,
  "data": {
    "total_cards": 5000,
    "by_type": {
      "Normal Monster": 800,
      "Effect Monster": 1200,
      "Synchro Monster": 600,
      "Spell Card": 1200,
      "Trap Card": 1200
    },
    "by_rarity": {
      "Ultra Rare": 1500,
      "Super Rare": 2000,
      "Rare": 1500
    },
    "by_attribute": {
      "Light": 800,
      "Dark": 900,
      "Water": 700,
      "Fire": 600,
      "Wind": 650
    }
  }
}
```

### GET /cards/types

すべてのカードタイプを取得します。

**レスポンス:**

```json
{
  "success": true,
  "data": [
    "Normal Monster",
    "Effect Monster",
    "Synchro Monster",
    "XYZ Monster",
    "Fusion Monster",
    "Link Monster",
    "Pendulum Monster",
    "Spell Card",
    "Trap Card"
  ]
}
```

### GET /cards/attributes

すべてのカード属性を取得します。

**レスポンス:**

```json
{
  "success": true,
  "data": [
    "Light",
    "Dark",
    "Water",
    "Fire",
    "Wind",
    "Earth",
    "Divine"
  ]
}
```

### GET /cards/rarities

すべてのレアリティを取得します。

**レスポンス:**

```json
{
  "success": true,
  "data": [
    "Ultra Rare",
    "Super Rare",
    "Rare",
    "Common"
  ]
}
```

---

## デッキ検証

### POST /decks/validate

デッキの有効性を検証します。

**リクエストボディ:**

```json
{
  "cards": [
    {"id": 25955692, "quantity": 3},
    {"id": 12345678, "quantity": 2},
    {"id": 87654321, "quantity": 1}
  ]
}
```

**レスポンス（有効）:**

```json
{
  "success": true,
  "data": {
    "valid": true,
    "cards": [
      {
        "id": 25955692,
        "name": "Blue-Eyes White Dragon",
        "quantity": 3
      },
      {
        "id": 12345678,
        "name": "Sample Card",
        "quantity": 2
      },
      {
        "id": 87654321,
        "name": "Another Card",
        "quantity": 1
      }
    ],
    "total_cards": 6,
    "errors": []
  }
}
```

**レスポンス（無効）:**

```json
{
  "success": false,
  "data": {
    "valid": false,
    "cards": [...],
    "total_cards": 35,
    "errors": [
      "Deck size too large: 35/20-30",
      "Card ID 99999999: 3枚までしか使用できません（指定: 4枚）"
    ]
  }
}
```

---

## エラーレスポンス

### 404 Not Found

```json
{
  "success": false,
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error

```json
{
  "success": false,
  "error": "Internal server error"
}
```

### 400 Bad Request

```json
{
  "success": false,
  "error": "Invalid limit or offset"
}
```

---

## レート制限

現在、レート制限は設定されていません。
ただし、サーバーへの負荷軽減のため、大量のリクエストは避けてください。

---

## 認証

認証は不要です。すべてのエンドポイントは公開されています。

---

## サンプルコード

### Python

```python
import requests

# カード検索
response = requests.get(
    'http://localhost:5000/api/cards/search',
    params={
        'name': 'Blue-Eyes',
        'limit': 20
    }
)
cards = response.json()['data']
for card in cards:
    print(f"{card['name']}: {card['type']}")
```

### JavaScript

```javascript
// カード検索
const response = await fetch(
  '/api/cards/search?name=Blue-Eyes&limit=20'
);
const data = await response.json();
data.data.forEach(card => {
  console.log(`${card.name}: ${card.type}`);
});
```

### cURL

```bash
# カード検索
curl -X GET "http://localhost:5000/api/cards/search?name=Blue-Eyes&limit=20"

# 統計情報取得
curl -X GET "http://localhost:5000/api/cards/stats"

# デッキ検証
curl -X POST "http://localhost:5000/api/decks/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "cards": [
      {"id": 25955692, "quantity": 3}
    ]
  }'
```

---

## 更新履歴

- **2026-08-30** - API ドキュメント v1.0 リリース
