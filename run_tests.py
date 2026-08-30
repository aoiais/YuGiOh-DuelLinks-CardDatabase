#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ユーザーテスト実行スクリプト
Webダッシュボード、API、デッキ構築ツールのテスト
"""

import subprocess
import time
import sys
import webbrowser
from pathlib import Path

def start_api_server():
    """API サーバーを起動"""
    print("\n" + "="*60)
    print("🔌 API サーバーを起動中...")
    print("="*60)
    
    try:
        # API サーバーをバックグラウンドで起動
        api_process = subprocess.Popen(
            [sys.executable, 'api/app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent
        )
        
        print("⏳ サーバーの起動を待機中... (5秒)")
        time.sleep(5)
        
        # プロセスが起動しているか確認
        if api_process.poll() is None:
            print("✅ API サーバーが起動しました")
            print("   URL: http://localhost:5000")
            return api_process
        else:
            print("❌ API サーバーの起動に失敗しました")
            return None
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None


def start_frontend_server():
    """フロントエンド開発サーバーを起動"""
    print("\n" + "="*60)
    print("🎨 フロントエンド開発サーバーを起動中...")
    print("="*60)
    
    try:
        # フロントエンドをビルドして起動
        frontend_dir = Path(__file__).parent / 'frontend'
        
        # npm サーバーをバックグラウンドで起動
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=frontend_dir
        )
        
        print("⏳ サーバーの起動を待機中... (10秒)")
        time.sleep(10)
        
        # プロセスが起動しているか確認
        if frontend_process.poll() is None:
            print("✅ フロントエンド開発サーバーが起動しました")
            print("   URL: http://localhost:3000")
            return frontend_process
        else:
            print("❌ フロントエンドサーバーの起動に失敗しました")
            return None
    except FileNotFoundError:
        print("❌ npm が見つかりません")
        print("   Node.js と npm がインストールされていることを確認してください")
        return None
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None


def open_dashboard():
    """Webダッシュボードをブラウザで開く"""
    print("\n" + "="*60)
    print("🌐 Webダッシュボードを開中...")
    print("="*60)
    
    try:
        webbrowser.open('http://localhost:3000')
        print("✅ ブラウザでダッシュボードを開きました")
        return True
    except Exception as e:
        print(f"⚠️  ブラウザを自動で開けませんでした: {e}")
        print("   手動で以下にアクセスしてください: http://localhost:3000")
        return False


def print_test_guide():
    """テストガイドを表示"""
    print("\n" + "="*60)
    print("📋 テストガイド")
    print("="*60)
    
    guide = """
✅ ホームページのテスト
  1. http://localhost:3000 を開く
  2. 統計情報が表示されているか確認
  3. カード総数が表示されているか確認
  4. 各機能へのリンクが動作するか確認

✅ カード検索ページのテスト
  1. 「🔍 カード検索」リンクをクリック
  2. 検索ボックスに「Blue」と入力
  3. 「検索」ボタンをクリック
  4. 検索結果が表示されるか確認
  5. カードをクリックして詳細を確認
  6. レアリティなどでフィルターテスト

✅ デッキ構築ツールのテスト
  1. 「🎯 デッキ構築ツール」リンクをクリック
  2. 検索ボックスに「Blue」と入力
  3. 「検索」ボタンをクリック
  4. 検索結果の「追加」ボタンをクリック
  5. カードがデッキに追加されるか確認
  6. カード枚数が更新されるか確認
  7. 「➕」ボタンで枚数を増加（最大3枚）
  8. デッキ統計が正しく表示されるか確認
  9. デッキが有効（20-30枚）か確認
  10. 「💾 デッキ保存」ボタンをテスト
  11. 「📤 エクスポート」ボタンで JSON ダウンロード

✅ API のテスト（ターミナルから実行）
  curl http://localhost:5000/api/health
  curl "http://localhost:5000/api/cards/search?name=Blue&limit=5"
  curl http://localhost:5000/api/cards/stats

✅ レスポンシブデザインのテスト
  1. F12 でデベロッパーツールを開く
  2. 「デバイスモード」を開く
  3. iPhone などモバイルデバイスで表示確認
  4. タッチ操作でテスト

✅ ローカルストレージのテスト
  1. デッキを構築して保存
  2. ブラウザのデベロッパーツール > Application > Storage
  3. decks キーが保存されているか確認
"""
    print(guide)


def print_api_examples():
    """API 使用例を表示"""
    print("\n" + "="*60)
    print("🔌 API テスト例")
    print("="*60)
    
    examples = """
# 基本的なテスト
curl http://localhost:5000/api/health

# カード検索（Blue-Eyes で検索）
curl "http://localhost:5000/api/cards/search?name=Blue&limit=10"

# 統計情報取得
curl http://localhost:5000/api/cards/stats

# カード詳細取得（ID: 25955692）
curl http://localhost:5000/api/cards/25955692

# 属性でフィルター
curl -X POST http://localhost:5000/api/cards/filter \\
  -H "Content-Type: application/json" \\
  -d '{
    "filters": {"attribute": ["Light"]},
    "limit": 20
  }'

# デッキ検証
curl -X POST http://localhost:5000/api/decks/validate \\
  -H "Content-Type: application/json" \\
  -d '{
    "cards": [
      {"id": 25955692, "quantity": 3},
      {"id": 12345678, "quantity": 2}
    ]
  }'
"""
    print(examples)


def main():
    """メイン実行"""
    print("\n" + "="*60)
    print("🧪 遊戯王デュエルリンクス カードデータベース")
    print("ユーザーテストスクリプト")
    print("="*60)
    
    # API サーバーを起動
    api_process = start_api_server()
    if not api_process:
        print("\n❌ API サーバーの起動に失敗しました")
        return 1
    
    # フロントエンド開発サーバーを起動
    frontend_process = start_frontend_server()
    if not frontend_process:
        print("\n❌ フロントエンドサーバーの起動に失敗しました")
        if api_process:
            api_process.terminate()
        return 1
    
    # Webダッシュボードを開く
    open_dashboard()
    
    # テストガイドを表示
    print_test_guide()
    
    # API テスト例を表示
    print_api_examples()
    
    # 実行中の状態
    print("\n" + "="*60)
    print("✅ サーバーが起動しています")
    print("="*60)
    print("\n🔗 アクセスURL:")
    print("  - Webダッシュボード: http://localhost:3000")
    print("  - API Server: http://localhost:5000")
    print("\n📚 ドキュメント:")
    print("  - API 仕様: docs/API.md")
    print("  - インストール: docs/INSTALLATION.md")
    print("\n🛑 停止するには: Ctrl+C を押してください")
    print("="*60 + "\n")
    
    try:
        # サーバーの実行を継続
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("🛑 テストを終了しています...")
        print("="*60)
        
        # プロセスを終了
        if api_process and api_process.poll() is None:
            print("API サーバーを停止中...")
            api_process.terminate()
            api_process.wait(timeout=5)
        
        if frontend_process and frontend_process.poll() is None:
            print("フロントエンドサーバーを停止中...")
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
        
        print("✅ 終了しました\n")
        return 0


if __name__ == '__main__':
    sys.exit(main())
