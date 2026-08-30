@echo off
REM セットアップと初期テストスクリプト (Windows)

echo 🚀 遊戯王デュエルリンクス カードデータベース セットアップ
echo ============================================================

REM ステップ 1: Python 環境のセットアップ
echo.
echo 📦 ステップ 1: Python 環境をセットアップ中...
python -m venv venv
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Python 環境のセットアップが完了しました

REM ステップ 2: カードデータを取得
echo.
echo 🎴 ステップ 2: カードデータを取得中...
python scripts/fetch_cards.py

if not exist "database/cards.json" (
    echo ❌ エラー: cards.json が作成されませんでした
    exit /b 1
)

echo ✅ カードデータの取得が完了しました

REM ステップ 3: データベースを作成
echo.
echo 🗄️  ステップ 3: SQLite データベースを作成中...
python scripts/update_database.py

if not exist "database/cards.db" (
    echo ❌ エラー: cards.db が作成されませんでした
    exit /b 1
)

echo ✅ データベースの作成が完了しました

REM ステップ 4: 複数形式にエクスポート
echo.
echo 📤 ステップ 4: 複数形式にエクスポート中...
python scripts/export_formats.py

echo ✅ エクスポートが完了しました

REM ステップ 5: API テスト
echo.
echo 🔌 ステップ 5: API テストを準備中...
echo 以下のコマンドで API サーバーを起動してください:
echo.
echo   python api/app.py
echo.
echo 別のターミナルで以下をテストしてください:
echo   curl "http://localhost:5000/api/health"
echo   curl "http://localhost:5000/api/cards/stats"
echo.

REM ステップ 6: フロントエンド設定
echo.
echo 🎨 ステップ 6: フロントエンドをセットアップ中...
cd frontend
call npm install

echo.
echo ✅ フロントエンドのセットアップが完了しました
echo.
echo 以下のコマンドで Webダッシュボードを起動してください:
echo   cd frontend
echo   npm run dev
echo.

cd ..

echo.
echo ============================================================
echo ✅ セットアップが完了しました!
echo.
echo 📚 次のステップ:
echo   1. API サーバーを起動: python api/app.py
echo   2. Webダッシュボードを起動: cd frontend 然后 npm run dev
echo   3. ブラウザで http://localhost:3000 を開く
echo.
echo 📖 ドキュメント:
echo   - インストールガイド: docs/INSTALLATION.md
echo   - API 仕様書: docs/API.md
echo   - デッキ構築ツール: docs/DECK_BUILDER.md
echo.
pause
