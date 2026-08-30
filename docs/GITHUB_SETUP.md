# GitHub 連携ガイド

遊戯王デュエルリンクス カードデータベースをGitHubにプッシュし、自動更新を有効化するガイドです。

## 前提条件

- Git がインストール済み
- GitHub アカウント
- SSH キー または パーソナルアクセストークン（PAT）を設定済み

## ステップ 1: GitHub でリポジトリを設定

### オプション A: 既存リポジトリにプッシュ

```bash
cd YuGiOh-DuelLinks-CardDatabase

# 既存のリモートリポジトリを確認
git remote -v

# リモートリポジトリを設定（既にある場合は変更）
git remote set-url origin https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase.git

# または SSH で設定
git remote set-url origin git@github.com:aoiais/YuGiOh-DuelLinks-CardDatabase.git
```

### オプション B: 新規リポジトリを初期化

```bash
cd YuGiOh-DuelLinks-CardDatabase

# Git を初期化
git init

# 最初のコミット
git add .
git commit -m "🎴 初回コミット: 遊戯王デュエルリンクス カードデータベース"

# GitHub でリポジトリを作成後、リモート追加
git remote add origin https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase.git

# メインブランチにリネーム
git branch -M main

# プッシュ
git push -u origin main
```

## ステップ 2: 認証設定

### SSH キー認証（推奨）

```bash
# SSH キーペアを生成（既にない場合）
ssh-keygen -t ed25519 -C "your_email@example.com"

# SSH キーを追加
ssh-add ~/.ssh/id_ed25519

# ~/.ssh/id_ed25519.pub の内容を GitHub の SSH Keys に登録
# Settings > SSH and GPG keys > New SSH key
```

### HTTPS + PAT 認証

```bash
# GitHub でパーソナルアクセストークンを生成
# Settings > Developer settings > Personal access tokens > Tokens (classic) > Generate new token

# .git/config にクレデンシャルを設定
git config --global credential.helper store

# 初回のプッシュ時に PAT を入力
git push
```

## ステップ 3: リポジトリをプッシュ

```bash
cd YuGiOh-DuelLinks-CardDatabase

# 状態確認
git status

# すべての変更をステージング
git add .

# コミット
git commit -m "🎴 遊戯王デュエルリンクス カードデータベース - 初期設定"

# プッシュ
git push -u origin main
```

**出力例:**
```
Enumerating objects: 150, done.
Counting objects: 100% (150/150), done.
Delta compression using up to 8 threads
Compressing objects: 100% (120/120), done.
Writing objects: 100% (150/150), 2.5 MiB | 1.2 MiB/s, done.
Total 150 (delta 45), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (45/45), done.
remote: 
remote: Create a pull request for 'main' on GitHub by visiting:
remote:      https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase/pull/new/main
remote:
To github.com:aoiais/YuGiOh-DuelLinks-CardDatabase.git
 * [new branch]      main -> main
```

## ステップ 4: GitHub Actions を有効化

### 自動更新ワークフローの有効化

1. GitHub リポジトリを開く
   ```
   https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase
   ```

2. **Actions** タブをクリック

3. ワークフローが表示されます：
   ```
   🔄 自動更新 - カードデータベース
   ```

4. **Enable workflow** をクリック（有効化）

### ワークフロー実行設定

`.github/workflows/update-cards.yml` のスケジュール設定を確認：

```yaml
schedule:
  # 毎日 00:00 UTC にカードデータを更新
  - cron: '0 0 * * *'
```

**タイムゾーン変更例:**

日本時間（JST = UTC+9）に毎日 09:00 に実行する場合：

```yaml
schedule:
  # 毎日 09:00 JST（00:00 UTC）に実行
  - cron: '0 0 * * *'
  
  # または毎日 18:00 JST（09:00 UTC）に実行
  - cron: '0 9 * * *'
```

**注:** GitHub Actions は UTC タイムゾーンを使用します。

## ステップ 5: 初回の自動実行を確認

### 手動でワークフローを実行

1. GitHub リポジトリの **Actions** タブを開く

2. 左側で **🔄 自動更新 - カードデータベース** を選択

3. **Run workflow** をクリック

4. ブランチを選択し、**Run workflow** をクリック

### 実行状況を監視

1. ワークフロー実行を選択

2. ジョブログを確認：
   ```
   ✅ カードデータを取得
   ✅ データベースを更新
   ✅ 複数形式にエクスポート
   ✅ 変更をコミット
   ```

3. 完了後、リポジトリの `database/` ディレクトリが更新されます

## ステップ 6: GitHub Pages で Webダッシュボードをホスト（オプション）

### ビルドと公開

```bash
# フロントエンドをビルド
cd frontend
npm run build

# 出力は frontend/dist に生成される
```

### GitHub Pages の設定

1. **Settings** > **Pages** を開く

2. **Source** で以下を設定：
   - Branch: `main`
   - Folder: `/(root)` または `frontend/dist`

3. **Save** をクリック

4. 数分後、以下で公開されます：
   ```
   https://aoiais.github.io/YuGiOh-DuelLinks-CardDatabase
   ```

## ステップ 7: README バッジを追加（オプション）

GitHub Actions の実行状況を README に表示：

```markdown
# 🎴 遊戯王デュエルリンクス カードデータベース

[![Update Cards](https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase/actions/workflows/update-cards.yml/badge.svg)](https://github.com/aoiais/YuGiOh-DuelLinks-CardDatabase/actions/workflows/update-cards.yml)

自動更新型の遊戯王デュエルリンクス全カード網羅データベースです。
```

## ステップ 8: コラボレーターの追加（オプション）

1. **Settings** > **Collaborators** を開く

2. **Add people** をクリック

3. コラボレーターのユーザー名を入力

4. 権限を選択してアクセス許可

## トラブルシューティング

### "Permission denied (publickey)" エラー

```bash
# SSH キーが正しく設定されているか確認
ssh -T git@github.com

# 正しい出力:
# Hi aoiais! You've successfully authenticated, but GitHub does not provide shell access.
```

**解決方法:**
- SSH キーを GitHub に登録
- `ssh-add ~/.ssh/id_ed25519` を実行
- `git remote set-url origin git@github.com:...` で SSH URL に変更

### "fatal: Authentication failed"

```bash
# HTTPS 認証の場合、PAT を確認
git credential-osxkeychain erase
# or
git credential-manager-core erase
```

その後、再度プッシュを試みると、認証入力が表示されます。

### ワークフローが実行されない

1. **Actions** タブで有効化されているか確認
2. `.github/workflows/update-cards.yml` が存在するか確認
3. YAML 構文が正しいか確認（[YAML バリデーター](https://www.yamllint.com/) で検証）

### プッシュが "pre-commit hook" で失敗

```bash
# pre-commit フックをスキップ
git push --no-verify
```

## 自動更新の検証

### ログを確認

GitHub リポジトリ > **Actions** > ワークフロー実行 > ジョブを選択

### 更新内容を確認

```
GitHub リポジトリ > **Commits** > 最新のコミット
例: "🔄 自動更新: 2026年08月30日 のカードデータベース更新"
```

### ローカルで確認

```bash
# リモートから最新を取得
git fetch origin

# 最新のコミットログを確認
git log origin/main --oneline -10

# ローカルに反映
git pull origin main

# database/ ディレクトリの更新日時を確認
ls -la database/
```

## 日常的な運用

### 定期的なチェック

```bash
# 毎日、以下を確認
1. GitHub Actions が実行されたか
2. エラーがないか
3. database/ が更新されたか
```

### マニュアル更新が必要な場合

```bash
# GitHub Actions で更新を待たずに、ローカルで実行
python scripts/fetch_cards.py
python scripts/update_database.py
python scripts/export_formats.py

# 変更をコミット・プッシュ
git add database/
git commit -m "🔄 手動更新: カードデータベース"
git push origin main
```

## より高度な設定

### 複数ブランチの管理

```bash
# 開発ブランチを作成
git checkout -b develop
git push -u origin develop

# main は本番用、develop は開発用として使用
```

### リリースタグの作成

```bash
# リリースタグを作成
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Protected Branches の設定

1. **Settings** > **Branches** を開く
2. **Add rule** をクリック
3. Branch name pattern: `main`
4. 以下を有効化：
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging

## 次のステップ

1. ✅ GitHub リポジトリにプッシュ
2. ✅ GitHub Actions を有効化
3. ⏳ 初回自動実行を確認
4. ⏳ Webダッシュボードをテスト
5. ⏳ ドキュメントを公開

---

**最後更新**: 2026年8月30日

**参考:**
- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [Git 基本](https://git-scm.com/doc)
- [GitHub Pages](https://pages.github.com/)
