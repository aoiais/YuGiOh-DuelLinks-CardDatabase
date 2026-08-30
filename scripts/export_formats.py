#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
カードデータを複数形式にエクスポート
JSON、CSV形式でのエクスポートを行います
"""

import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# ファイルパス
DB_DIR = Path(__file__).parent.parent / 'database'
CARDS_JSON = DB_DIR / 'cards.json'
CARDS_DB = DB_DIR / 'cards.db'
CARDS_CSV = DB_DIR / 'cards.csv'
CARDS_DETAILED_CSV = DB_DIR / 'cards_detailed.csv'


def export_to_csv_simple(db_path: Path, csv_path: Path) -> int:
    """
    SQLiteデータベースを簡易CSV形式にエクスポート
    
    Args:
        db_path: SQLiteデータベースのパス
        csv_path: 出力CSVファイルのパス
        
    Returns:
        エクスポートされたカードの件数
    """
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # カード情報を取得
        cursor.execute('''
            SELECT 
                id, name, type, race, attribute, level, atk, def, 
                rarity, archetype
            FROM cards
            ORDER BY name
        ''')
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        # CSVに書き込み
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        
        conn.close()
        print(f"✅ {len(rows)} 件のカードをCSVにエクスポート: {csv_path.name}")
        return len(rows)
    
    except Exception as e:
        print(f"❌ CSV出力エラー: {e}")
        return 0


def export_to_csv_detailed(db_path: Path, csv_path: Path) -> int:
    """
    SQLiteデータベースを詳細CSV形式にエクスポート（説明、タグなど含む）
    
    Args:
        db_path: SQLiteデータベースのパス
        csv_path: 出力CSVファイルのパス
        
    Returns:
        エクスポートされたカードの件数
    """
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # カード情報を取得
        cursor.execute('''
            SELECT 
                c.id, c.name, c.type, c.race, c.attribute, c.level, 
                c.atk, c.def, c.description, c.rarity, c.archetype,
                c.scale, c.linkval
            FROM cards c
            ORDER BY c.name
        ''')
        
        rows = cursor.fetchall()
        
        # CSVに書き込み
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            
            # ヘッダー
            headers = [
                'ID', 'カード名', 'タイプ', '種族', '属性', 'レベル',
                '攻撃力', '守備力', '説明', 'レアリティ', 'アーキタイプ',
                'スケール', 'リンク値'
            ]
            writer.writerow(headers)
            
            # データ
            for row in rows:
                # 説明を改行なしで統一
                description = row[8].replace('\n', ' ') if row[8] else ''
                
                new_row = list(row[:8]) + [description] + list(row[9:])
                writer.writerow(new_row)
        
        conn.close()
        print(f"✅ {len(rows)} 件のカードを詳細CSVにエクスポート: {csv_path.name}")
        return len(rows)
    
    except Exception as e:
        print(f"❌ 詳細CSV出力エラー: {e}")
        return 0


def export_to_json_by_type(db_path: Path, output_dir: Path) -> int:
    """
    カードタイプ別にJSONでエクスポート
    
    Args:
        db_path: SQLiteデータベースのパス
        output_dir: 出力ディレクトリ
        
    Returns:
        エクスポートされたカードの総件数
    """
    try:
        output_dir.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # カードタイプを取得
        cursor.execute('SELECT DISTINCT type FROM cards WHERE type IS NOT NULL ORDER BY type')
        types = [row[0] for row in cursor.fetchall()]
        
        total_cards = 0
        
        for card_type in types:
            # 安全なファイル名に変換
            safe_name = card_type.replace('/', '_').replace(' ', '_').lower()
            output_file = output_dir / f'cards_by_{safe_name}.json'
            
            # タイプ別カード情報を取得
            cursor.execute('''
                SELECT * FROM cards
                WHERE type = ?
                ORDER BY name
            ''', (card_type,))
            
            cards = []
            for row in cursor.fetchall():
                card_dict = dict(row)
                cards.append(card_dict)
            
            # JSONで保存
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'type': card_type,
                    'count': len(cards),
                    'cards': cards
                }, f, ensure_ascii=False, indent=2)
            
            print(f"  - {card_type}: {len(cards)} 件")
            total_cards += len(cards)
        
        conn.close()
        print(f"✅ タイプ別JSONをエクスポート: {total_cards} 件（{len(types)} ファイル）")
        return total_cards
    
    except Exception as e:
        print(f"❌ タイプ別JSON出力エラー: {e}")
        return 0


def export_to_json_by_archetype(db_path: Path, output_dir: Path) -> int:
    """
    アーキタイプ別にJSONでエクスポート
    
    Args:
        db_path: SQLiteデータベースのパス
        output_dir: 出力ディレクトリ
        
    Returns:
        エクスポートされたカードの総件数
    """
    try:
        output_dir.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # アーキタイプを取得
        cursor.execute('''
            SELECT DISTINCT archetype FROM cards 
            WHERE archetype IS NOT NULL 
            ORDER BY archetype
        ''')
        archetypes = [row[0] for row in cursor.fetchall()]
        
        total_cards = 0
        
        for archetype in archetypes:
            # 安全なファイル名に変換
            safe_name = archetype.replace('/', '_').replace(' ', '_').lower()
            output_file = output_dir / f'cards_arch_{safe_name}.json'
            
            # アーキタイプ別カード情報を取得
            cursor.execute('''
                SELECT * FROM cards
                WHERE archetype = ?
                ORDER BY name
            ''', (archetype,))
            
            cards = []
            for row in cursor.fetchall():
                card_dict = dict(row)
                cards.append(card_dict)
            
            # JSONで保存
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'archetype': archetype,
                    'count': len(cards),
                    'cards': cards
                }, f, ensure_ascii=False, indent=2)
            
            total_cards += len(cards)
        
        conn.close()
        print(f"✅ アーキタイプ別JSONをエクスポート: {total_cards} 件（{len(archetypes)} ファイル）")
        return total_cards
    
    except Exception as e:
        print(f"❌ アーキタイプ別JSON出力エラー: {e}")
        return 0


def create_statistics_json(db_path: Path, output_file: Path) -> bool:
    """
    統計情報をJSONで保存
    
    Args:
        db_path: SQLiteデータベースのパス
        output_file: 出力ファイルのパス
        
    Returns:
        成功したかどうか
    """
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 総カード数
        cursor.execute('SELECT COUNT(*) FROM cards')
        total_cards = cursor.fetchone()[0]
        
        # タイプ別
        cursor.execute('''
            SELECT type, COUNT(*) as count
            FROM cards
            GROUP BY type
            ORDER BY count DESC
        ''')
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        # レアリティ別
        cursor.execute('''
            SELECT rarity, COUNT(*) as count
            FROM cards
            GROUP BY rarity
            ORDER BY count DESC
        ''')
        by_rarity = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 属性別
        cursor.execute('''
            SELECT attribute, COUNT(*) as count
            FROM cards
            WHERE attribute IS NOT NULL AND attribute != 'Unknown'
            GROUP BY attribute
            ORDER BY count DESC
        ''')
        by_attribute = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 統計情報をJSON保存
        stats = {
            'updated_at': datetime.now().isoformat(),
            'total_cards': total_cards,
            'by_type': by_type,
            'by_rarity': by_rarity,
            'by_attribute': by_attribute
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        conn.close()
        print(f"✅ 統計情報をJSON保存: {output_file.name}")
        return True
    
    except Exception as e:
        print(f"❌ 統計情報の保存エラー: {e}")
        return False


def main():
    """メイン処理"""
    print("📤 カードデータをエクスポート中")
    print("="*50)
    
    if not CARDS_DB.exists():
        print(f"❌ SQLiteデータベースが見つかりません: {CARDS_DB}")
        print("   先に update_database.py を実行してください")
        return False
    
    # CSV形式にエクスポート
    print("\n📋 CSV形式にエクスポート中...")
    export_to_csv_simple(CARDS_DB, CARDS_CSV)
    export_to_csv_detailed(CARDS_DB, CARDS_DETAILED_CSV)
    
    # タイプ別JSONにエクスポート
    print("\n📁 タイプ別JSON形式にエクスポート中...")
    type_dir = DB_DIR / 'cards_by_type'
    export_to_json_by_type(CARDS_DB, type_dir)
    
    # アーキタイプ別JSONにエクスポート
    print("\n📁 アーキタイプ別JSON形式にエクスポート中...")
    archetype_dir = DB_DIR / 'cards_by_archetype'
    export_to_json_by_archetype(CARDS_DB, archetype_dir)
    
    # 統計情報をJSONで保存
    print("\n📊 統計情報をJSONで保存中...")
    stats_file = DB_DIR / 'statistics.json'
    create_statistics_json(CARDS_DB, stats_file)
    
    print("\n✅ 完了!")
    return True


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
