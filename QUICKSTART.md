# セットアップと実行ガイド

遊戯王デュエルリンクス カードデータベースをセットアップして実行するための完全ガイドです。

## 📋 クイックスタート

### Windows ユーザー

```bash
# セットアップを実行
setup.bat

# テストを実行
python test.py

# ユーザーテスト（サーバー起動＋ダッシュボード表示）
python run_tests.py
```

### macOS/Linux ユーザー

```bash
# セットアップを実行
chmod +x setup.sh
./setup.sh

# テストを実行
python test.py

# ユーザーテスト（サーバー起動＋ダッシュボード表示）
python run_tests.py
```

---

## 📖 詳細ガイド

### ステップ 1: ローカルテスト（セットアップ）

#### Windows

```bash
cd YuGiOh-DuelLinks-CardDatabase
setup.bat
```

**実行内容:**
1. ✅ Python 仮想環境を作成
2. ✅ Python 依存関係をインストール
3. ✅ YGOPRODeck API からカード情報を取得
4. ✅ SQLite データベースを作成
5. ✅ JSON、CSV、統計情報にエクスポート
6. ✅ Node.js 依存関係をインストール

#### macOS/Linux

```bash
cd YuGiOh-DuelLinks-CardDatabase
chmod +x setup.sh
./setup.sh
```

---

### ステップ 2: データベースとデータをテスト

```bash
# Python 仮想環境を有効化
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

# テストスクリプトを実行
python test.py
```

**テスト項目:**
- ✅ データベースファイルの存在確認
- ✅ JSON データの確認
- ✅ API サーバーの接続テスト
- ✅ カード検索機能テスト
- ✅ 統計情報取得テスト
- ✅ デッキ検証機能テスト

---

### ステップ 3: GitHub に接続とプッシュ

[docs/GITHUB_SETUP.md](./docs/GITHUB_SETUP.md) を参照してください。

**概要:**
```bash
# Git を初期化（まだの場合）
git init

# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "🎴 遊戯王デュエルリンクス カードデータベース - 初期設定"

# GitHub リモートリポジトリを設定
git remote add origin https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase.git

# main ブランチにプッシュ
git branch -M main
git push -u origin main
```

---

### ステップ 4: GitHub Actions を有効化

1. GitHub リポジトリを開く
2. **Actions** タブをクリック
3. **🔄 自動更新 - カードデータベース** を確認
4. **Enable workflow** をクリック
5. **Run workflow** で初回実行をテスト

---

### ステップ 5: ユーザーテスト（ダッシュボード + API）

すべてのサーバーを起動して実際にテスト：

```bash
# テストスクリプトを実行
python run_tests.py
```

**自動実行内容:**
1. 🔌 API サーバーを起動（ポート 5000）
2. 🎨 フロントエンド開発サーバーを起動（ポート 3000）
3. 🌐 ブラウザで http://localhost:3000 を自動オープン
4. 📋 テストガイドを表示
5. 🔌 API テスト例を表示

**テスト内容:**

#### ホームページ
- [ ] ホームページが表示される
- [ ] 統計情報が正しく表示される
- [ ] 各機能へのリンクが動作する

#### カード検索
- [ ] 「カード検索」ページが表示される
- [ ] カード名で検索できる
- [ ] フィルター（タイプ、属性など）が動作する
- [ ] 検索結果が表示される
- [ ] カードをクリックして詳細を確認できる

#### デッキ構築
- [ ] 「デッキ構築ツール」ページが表示される
- [ ] カード検索が動作する
- [ ] 「追加」でデッキにカードが追加される
- [ ] カード枚数が増加/削除できる
- [ ] デッキ統計が更新される
- [ ] デッキが 20-30 枚の場合に「有効」と表示される
- [ ] 「💾 デッキ保存」でローカルストレージに保存される
- [ ] 「📤 エクスポート」で JSON ファイルがダウンロードされる

#### API（ターミナルからテスト）
```bash
# ヘルスチェック
curl http://localhost:5000/api/health

# カード検索
curl "http://localhost:5000/api/cards/search?name=Blue&limit=5"

# 統計情報
curl http://localhost:5000/api/cards/stats

# デッキ検証
curl -X POST http://localhost:5000/api/decks/validate \
  -H "Content-Type: application/json" \
  -d '{"cards":[{"id":25955692,"quantity":3}]}'
```

---

### ステップ 6: カスタマイズと拡張

#### フロントエンドのカスタマイズ

```bash
cd frontend

# 開発モード
npm run dev

# 本番ビルド
npm run build

# 出力: frontend/dist
```

**カスタマイズ対象:**
- `src/App.vue` - メインレイアウト
- `src/pages/Home.vue` - ホームページ
- `src/pages/Search.vue` - 検索ページ
- `src/pages/DeckBuilder.vue` - デッキ構築ツール

#### バックエンド API のカスタマイズ

```bash
# API サーバーを実行
python api/app.py

# 編集対象: api/app.py
# 新しいエンドポイントを追加、既存エンドポイントを変更
```

#### スクリプトのカスタマイズ

```bash
# カード取得スクリプト
python scripts/fetch_cards.py

# DB 更新スクリプト
python scripts/update_database.py

# 形式変換スクリプト
python scripts/export_formats.py
```

---

## 🐛 トラブルシューティング

### "ModuleNotFoundError" が発生

```bash
# 仮想環境が有効化されていることを確認
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# 依存関係を再インストール
pip install -r requirements.txt
```

### "Port 5000 is already in use" エラー

```bash
# ポート5000を使用しているプロセスを確認
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# プロセスを終了
# Windows: taskkill /PID <PID> /F
# macOS/Linux: kill -9 <PID>
```

### npm install がエラー

```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### API がレスポンスしない

1. API サーバーが起動しているか確認
2. ファイアウォールがポート 5000 をブロックしていないか確認
3. `python api/app.py` の実行ログを確認

### ブラウザで localhost に接続できない

1. サーバーが起動しているか確認
2. ポート 3000（フロントエンド）、5000（API）が開いているか確認
3. ファイアウォール設定を確認

---

## 📊 成功指標

プロジェクトが正常に動作している場合、以下が確認できます：

- ✅ `database/cards.db` が 500MB 以上
- ✅ `database/cards.json` に 5000+ カード
- ✅ API が http://localhost:5000 で応答
- ✅ Webダッシュボードが http://localhost:3000 で表示
- ✅ カード検索が機能
- ✅ デッキ構築ツールが機能
- ✅ GitHub Actions で自動更新が実行
- ✅ database/ が毎日更新される

---

## 🚀 本番環境へのデプロイ

### Vercel へのデプロイ（フロントエンド）

```bash
# Vercel CLI をインストール
npm install -g vercel

# デプロイ
vercel frontend/
```

### Heroku へのデプロイ（API）

```bash
# Heroku CLI をインストール
# https://devcenter.heroku.com/articles/heroku-cli

# Heroku にログイン
heroku login

# アプリを作成
heroku create your-app-name

# デプロイ
git push heroku main
```

### Docker でのデプロイ

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN cd frontend && npm install && npm run build

EXPOSE 5000
CMD ["python", "api/app.py"]
```

```bash
docker build -t yugiohdl-carddb .
docker run -p 5000:5000 yugiohdl-carddb
```

---

## 📞 サポート

問題がある場合：

1. [GitHub Issues](https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase/issues) で報告
2. [docs/INSTALLATION.md](./INSTALLATION.md) のトラブルシューティングを参照
3. [CONTRIBUTING.md](../CONTRIBUTING.md) で貢献方法を確認

---

**最後更新**: 2026年8月30日
