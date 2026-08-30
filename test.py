#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
テストスクリプト - API と機能の検証
"""

import subprocess
import time
import requests
import json
import sys
from pathlib import Path

# ファイルパス
DB_DIR = Path(__file__).parent / 'database'
CARDS_DB = DB_DIR / 'cards.db'


def check_database():
    """データベースが存在するか確認"""
    print("\n" + "="*60)
    print("🗄️  データベース確認")
    print("="*60)
    
    if CARDS_DB.exists():
        print(f"✅ データベースが見つかりました: {CARDS_DB}")
        print(f"   ファイルサイズ: {CARDS_DB.stat().st_size / (1024*1024):.2f} MB")
        return True
    else:
        print(f"❌ データベースが見つかりません: {CARDS_DB}")
        return False


def check_json_data():
    """JSONデータが存在するか確認"""
    print("\n" + "="*60)
    print("📄 JSON データ確認")
    print("="*60)
    
    cards_json = DB_DIR / 'cards.json'
    if cards_json.exists():
        with open(cards_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            total = data.get('metadata', {}).get('total_cards', 0)
            print(f"✅ JSON ファイルが見つかりました")
            print(f"   総カード数: {total}")
            return True
    else:
        print(f"❌ JSON ファイルが見つかりません")
        return False


def check_api_server():
    """API サーバーの接続テスト"""
    print("\n" + "="*60)
    print("🔌 API サーバー確認")
    print("="*60)
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ API サーバーが稼働しています")
            print(f"   レスポンス: {response.json()}")
            return True
        else:
            print(f"❌ API サーバーが応答しません (ステータス: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API サーバーに接続できません")
        print("   以下を確認してください:")
        print("   1. 別のターミナルで 'python api/app.py' を実行してください")
        print("   2. サーバーがポート 5000 で起動するまで待機してください")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def test_card_search():
    """カード検索機能のテスト"""
    print("\n" + "="*60)
    print("🔍 カード検索テスト")
    print("="*60)
    
    try:
        # カード検索テスト
        response = requests.get(
            'http://localhost:5000/api/cards/search',
            params={'name': 'Blue', 'limit': 5},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                cards = data.get('data', [])
                total = data.get('pagination', {}).get('total', 0)
                print(f"✅ カード検索が成功しました")
                print(f"   検索結果: {len(cards)} 件 (全体: {total} 件)")
                
                if cards:
                    print(f"\n   最初のカード:")
                    card = cards[0]
                    print(f"   - 名前: {card.get('name')}")
                    print(f"   - タイプ: {card.get('type')}")
                    print(f"   - レアリティ: {card.get('rarity')}")
                return True
            else:
                print("❌ 検索に失敗しました")
                return False
        else:
            print(f"❌ API がエラーを返しました (ステータス: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def test_statistics():
    """統計情報取得テスト"""
    print("\n" + "="*60)
    print("📊 統計情報テスト")
    print("="*60)
    
    try:
        response = requests.get(
            'http://localhost:5000/api/cards/stats',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                stats = data.get('data', {})
                total = stats.get('total_cards', 0)
                print(f"✅ 統計情報が取得できました")
                print(f"   総カード数: {total}")
                
                by_type = stats.get('by_type', {})
                if by_type:
                    print(f"\n   カードタイプ別 (TOP 5):")
                    for i, (card_type, count) in enumerate(list(by_type.items())[:5], 1):
                        print(f"   {i}. {card_type}: {count}")
                return True
            else:
                print("❌ 統計情報取得に失敗しました")
                return False
        else:
            print(f"❌ API がエラーを返しました (ステータス: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def test_deck_validation():
    """デッキ検証テスト"""
    print("\n" + "="*60)
    print("🎯 デッキ検証テスト")
    print("="*60)
    
    try:
        # テストデッキ
        test_deck = {
            "cards": [
                {"id": 25955692, "quantity": 3},  # Blue-Eyes White Dragon
                {"id": 12345678, "quantity": 2}
            ]
        }
        
        response = requests.post(
            'http://localhost:5000/api/decks/validate',
            json=test_deck,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            deck_data = data.get('data', {})
            total_cards = deck_data.get('total_cards', 0)
            errors = deck_data.get('errors', [])
            
            print(f"✅ デッキ検証が完了しました")
            print(f"   総カード数: {total_cards}/20-30")
            
            if errors:
                print(f"   エラー/警告:")
                for error in errors:
                    print(f"   - {error}")
            else:
                print(f"   エラー: なし")
            return True
        else:
            print(f"❌ API がエラーを返しました (ステータス: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def main():
    """メインテスト実行"""
    print("\n" + "="*60)
    print("🧪 遊戯王デュエルリンクス カードデータベース テスト")
    print("="*60)
    
    results = {}
    
    # ローカルテスト
    results['データベース'] = check_database()
    results['JSON データ'] = check_json_data()
    
    # API テスト
    print("\n" + "="*60)
    print("⏳ API サーバー確認中...")
    print("="*60)
    print("注: API サーバーが起動していない場合、別のターミナルで実行してください:")
    print("   python api/app.py")
    print("")
    
    api_available = check_api_server()
    
    if api_available:
        results['カード検索'] = test_card_search()
        results['統計情報'] = test_statistics()
        results['デッキ検証'] = test_deck_validation()
    else:
        print("\n⚠️  API サーバーが起動していないため、API テストをスキップしました")
    
    # テスト結果サマリー
    print("\n" + "="*60)
    print("📋 テスト結果サマリー")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n合計: {passed}/{total} 成功")
    
    if passed == total:
        print("\n🎉 すべてのテストが成功しました!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} つのテストが失敗しました")
        print("\n🔧 トラブルシューティング:")
        print("  1. API サーバーが起動していることを確認")
        print("  2. データベースが正しく作成されているか確認")
        print("  3. docs/INSTALLATION.md のトラブルシューティングを参照")
        return 1


if __name__ == '__main__':
    sys.exit(main())
