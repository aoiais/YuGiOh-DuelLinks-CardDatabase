#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
遊戯王デュエルリンクス カードデータ取得スクリプト
YGOPRODeck APIから最新のカード情報を取得します
"""

import json
import requests
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# API設定
YGOPRODECK_API = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
YUGIPEDIA_API = 'https://yugipedia.com/api.php'

# データベースディレクトリ
DB_DIR = Path(__file__).parent.parent / 'database'
DB_DIR.mkdir(exist_ok=True)

# ファイル名
CARDS_JSON = DB_DIR / 'cards.json'
CARDS_BACKUP = DB_DIR / f'cards_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'


def fetch_from_ygoprodeck() -> List[Dict[str, Any]]:
    """
    YGOPRODeck APIからDuel Linksのカード情報を取得
    
    Returns:
        カード情報のリスト
    """
    print("🎴 YGOPRODeck APIからカード情報を取得中...")
    
    try:
        params = {
            'format': 'Duel Links',
            'sort': 'name',
            'misc': 'yes'
        }
        
        response = requests.get(YGOPRODECK_API, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        cards = data.get('data', [])
        
        print(f"✅ {len(cards)} 件のカードを取得しました")
        return cards
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API接続エラー: {e}")
        return []


def fetch_from_yugipedia(card_name: str) -> Dict[str, Any]:
    """
    Yugipediaから追加情報を取得（オプション）
    
    Args:
        card_name: カード名
        
    Returns:
        追加情報
    """
    try:
        params = {
            'action': 'query',
            'titles': card_name,
            'format': 'json',
            'prop': 'info|images'
        }
        
        response = requests.get(YUGIPEDIA_API, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException:
        return {}


def normalize_card_data(card: Dict[str, Any]) -> Dict[str, Any]:
    """
    カードデータを正規化
    
    Args:
        card: 元のカードデータ
        
    Returns:
        正規化されたカードデータ
    """
    return {
        'id': card.get('id', ''),
        'name': card.get('name', ''),
        'type': card.get('type', 'Unknown'),
        'race': card.get('race', 'Unknown'),
        'attribute': card.get('attribute', 'Unknown'),
        'level': card.get('level', 0),
        'atk': card.get('atk', 0),
        'def': card.get('def', 0),
        'desc': card.get('desc', ''),
        'rarity': card.get('rarity', 'Unknown'),
        'sets': card.get('card_sets', []),
        'images': card.get('card_images', []),
        'prices': card.get('card_prices', []),
        'scale': card.get('scale', None),  # Pendulum スケール
        'linkval': card.get('linkval', None),  # Link マーカー数
        'linkmarkers': card.get('linkmarkers', []),  # Link マーカー位置
        'archetype': card.get('archetype', None),
        'banlist_info': card.get('banlist_info', None),
        'misc_info': card.get('misc_info', []),
        'fetched_at': datetime.now().isoformat()
    }


def enrich_card_data(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    カードデータを拡張・正規化
    
    Args:
        cards: カード情報のリスト
        
    Returns:
        拡張されたカード情報のリスト
    """
    enriched_cards = []
    
    for i, card in enumerate(cards, 1):
        normalized = normalize_card_data(card)
        
        # 追加の分類タグを付与
        tags = []
        
        # カードタイプ別タグ
        card_type = card.get('type', '').upper()
        if 'MONSTER' in card_type:
            tags.append('monster')
        if 'SPELL' in card_type:
            tags.append('spell')
        if 'TRAP' in card_type:
            tags.append('trap')
        if 'SYNCHRO' in card_type:
            tags.append('synchro')
        if 'XYZ' in card_type:
            tags.append('xyz')
        if 'FUSION' in card_type:
            tags.append('fusion')
        if 'LINK' in card_type:
            tags.append('link')
        if 'PENDULUM' in card_type:
            tags.append('pendulum')
        if 'TUNER' in card_type:
            tags.append('tuner')
        
        normalized['tags'] = tags
        enriched_cards.append(normalized)
        
        if i % 100 == 0:
            print(f"  処理中... {i}/{len(cards)}")
    
    return enriched_cards


def save_card_data(cards: List[Dict[str, Any]]) -> bool:
    """
    カードデータをJSONファイルに保存
    
    Args:
        cards: カード情報のリスト
        
    Returns:
        成功したかどうか
    """
    try:
        # バックアップを作成
        if CARDS_JSON.exists():
            import shutil
            shutil.copy(CARDS_JSON, CARDS_BACKUP)
            print(f"💾 バックアップを作成: {CARDS_BACKUP.name}")
        
        # 新しいデータを保存
        with open(CARDS_JSON, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_cards': len(cards),
                    'updated_at': datetime.now().isoformat(),
                    'format': 'Duel Links',
                    'source': 'YGOPRODeck'
                },
                'data': cards
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(cards)} 件のカードを保存しました: {CARDS_JSON}")
        return True
        
    except Exception as e:
        print(f"❌ 保存エラー: {e}")
        return False


def validate_card_data(cards: List[Dict[str, Any]]) -> bool:
    """
    カードデータを検証
    
    Args:
        cards: カード情報のリスト
        
    Returns:
        検証に成功したかどうか
    """
    if not cards:
        print("❌ エラー: カードデータが取得できませんでした")
        return False
    
    # 必須フィールドの確認
    required_fields = ['id', 'name', 'desc']
    missing_count = 0
    
    for card in cards:
        for field in required_fields:
            if not card.get(field):
                missing_count += 1
    
    if missing_count > 0:
        print(f"⚠️  警告: {missing_count} 個の必須フィールドが不足しています")
    
    print(f"✅ データ検証完了: {len(cards)} 件のカードが有効です")
    return True


def generate_summary(cards: List[Dict[str, Any]]) -> None:
    """
    カードデータの統計情報を表示
    
    Args:
        cards: カード情報のリスト
    """
    print("\n" + "="*50)
    print("📊 カードデータベース統計")
    print("="*50)
    
    # タイプ別集計
    types = {}
    rarities = {}
    attributes = {}
    races = {}
    
    for card in cards:
        # タイプ
        card_type = card.get('type', 'Unknown')
        types[card_type] = types.get(card_type, 0) + 1
        
        # レアリティ
        rarity = card.get('rarity', 'Unknown')
        rarities[rarity] = rarities.get(rarity, 0) + 1
        
        # 属性
        attribute = card.get('attribute', 'Unknown')
        if attribute != 'Unknown':
            attributes[attribute] = attributes.get(attribute, 0) + 1
        
        # 種族
        race = card.get('race', 'Unknown')
        if race != 'Unknown':
            races[race] = races.get(race, 0) + 1
    
    print(f"\n📈 総カード数: {len(cards)}")
    
    print("\n🎴 カードタイプ別:")
    for card_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {card_type}: {count}")
    
    print("\n⭐ レアリティ別:")
    for rarity, count in sorted(rarities.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {rarity}: {count}")
    
    if attributes:
        print("\n🔥 属性別 (TOP 5):")
        for attr, count in sorted(attributes.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {attr}: {count}")
    
    if races:
        print("\n👹 種族別 (TOP 5):")
        for race, count in sorted(races.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {race}: {count}")
    
    print("\n" + "="*50)


def main():
    """メイン処理"""
    print("🚀 遊戯王デュエルリンクス カードデータベース取得")
    print("="*50)
    
    # YGOPRODeckからカード情報を取得
    raw_cards = fetch_from_ygoprodeck()
    
    if not raw_cards:
        print("❌ カード情報の取得に失敗しました")
        return False
    
    # データを正規化・拡張
    print("\n📝 カードデータを処理中...")
    processed_cards = enrich_card_data(raw_cards)
    
    # データを検証
    print("\n🔍 カードデータを検証中...")
    if not validate_card_data(processed_cards):
        return False
    
    # データを保存
    print("\n💾 カードデータを保存中...")
    if not save_card_data(processed_cards):
        return False
    
    # 統計情報を表示
    generate_summary(processed_cards)
    
    print("\n✅ 完了!")
    return True


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
