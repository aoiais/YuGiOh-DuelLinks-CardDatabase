#!/bin/bash
# 遊戯王デュエルリンクス カードデータベース セットアップスクリプト (macOS/Linux)

set -e

echo "=================================================="
echo "🚀 セットアップを開始します"
echo "=================================================="

# ステップ 1: 仮想環境の作成
echo ""
echo "📦 ステップ 1: 仮想環境を作成中..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 仮想環境を作成しました"
else
    echo "✅ 仮想環境はすでに存在します"
fi

# ステップ 2: 仮想環境を有効化
echo ""
echo "🔗 ステップ 2: 仮想環境を有効化中..."
source venv/bin/activate
echo "✅ 仮想環境を有効化しました"

# ステップ 3: 依存関係をインストール
echo ""
echo "📚 ステップ 3: Python 依存関係をインストール中..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python 依存関係をインストールしました"

# ステップ 4: カードデータを取得
echo ""
echo "🎴 ステップ 4: YGOPRODeck API からカード情報を取得中..."
if python scripts/fetch_cards.py; then
    echo "✅ カード情報を取得しました"
else
    echo "⚠️  警告: カード情報の取得に失敗しました"
    echo "   後で以下のコマンドで手動実行してください:"
    echo "   python scripts/fetch_cards.py"
fi

# ステップ 5: データベースを作成
echo ""
echo "🗄️  ステップ 5: SQLiteデータベースを作成中..."
if [ -f "database/cards.json" ]; then
    if python scripts/update_database.py; then
        echo "✅ データベースを作成しました"
    else
        echo "❌ データベース作成に失敗しました"
        exit 1
    fi
else
    echo "⚠️  警告: cards.json が見つかりません"
fi

# ステップ 6: データをエクスポート
echo ""
echo "📤 ステップ 6: データを複数形式にエクスポート中..."
if python scripts/export_formats.py; then
    echo "✅ データをエクスポートしました"
else
    echo "⚠️  警告: エクスポートに失敗しました"
fi

# ステップ 7: フロントエンドのセットアップ
echo ""
echo "🎨 ステップ 7: フロントエンドの依存関係をインストール中..."
cd frontend
if npm install; then
    echo "✅ フロントエンドの依存関係をインストールしました"
else
    echo "⚠️  警告: npm インストールに失敗しました"
fi
cd ..

# 完了
echo ""
echo "=================================================="
echo "✅ セットアップが完了しました！"
echo "=================================================="
echo ""
echo "📚 次のステップ:"
echo ""
echo "1. API サーバーを起動（ターミナル 1）:"
echo "   source venv/bin/activate && python api/app.py"
echo ""
echo "2. フロントエンドを起動（ターミナル 2）:"
echo "   cd frontend && npm run dev"
echo ""
echo "3. ブラウザでアクセス:"
echo "   http://localhost:3000"
echo ""
echo "=================================================="
