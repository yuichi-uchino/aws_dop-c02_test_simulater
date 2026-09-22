## Codespaces + Codex CLI 開発環境セットアップ

このリポジトリでは、GitHub Codespaces 上に開発環境を構築し、Codex CLI を利用する。

Codespaces を利用することで、Mac / Windows / Android Termux など、接続元の端末に依存せず同一のLinux開発環境を利用できる。

### 構成

```text
Mac / Android Termux
        |
        | SSH
        v
GitHub Codespaces
  ├─ Repository
  ├─ Node.js / npm
  ├─ Codex CLI
  └─ Agent Skills / 問題JSON
        |
        v
OpenAI
```

AI推論はOpenAI側で実行され、Codespacesはソースコード、ファイル操作、Git、Node.js、Codex CLIなどの実行環境として利用する。

---

## 1. GitHub CLI のインストール

Macの場合:

```bash
brew install gh
```

バージョン確認:

```bash
gh --version
```

---

## 2. GitHub CLI にログイン

```bash
gh auth login
```

以下を選択する。

```text
Where do you use GitHub?
→ GitHub.com

What is your preferred protocol for Git operations on this host?
→ HTTPS

Authenticate Git with your GitHub credentials?
→ Yes
```

認証状態を確認する。

```bash
gh auth status
```

---

## 3. Codespaces 権限を追加

CodespacesをCLIから操作するため、GitHub CLIの認証トークンに `codespace` scopeを追加する。

```bash
gh auth refresh -h github.com -s codespace
```

再度確認する。

```bash
gh auth status
```

以下のように `codespace` が含まれていればOK。

```text
Token scopes: 'codespace', 'gist', 'read:org', 'repo', 'workflow'
```

---

## 4. Codespace を作成

現在のデフォルトブランチは `main`。

```bash
gh codespace create \
  -R yuichi-uchino/aws_dop-c02_test_simulater \
  -b main
```

Machine Type は通常以下で十分。

```text
2 cores
8 GB RAM
32 GB storage
```

CodexのAI推論自体はOpenAI側で実行されるため、通常の開発・Agent利用では2 coresから開始する。

---

## 5. Codespace を確認

```bash
gh codespace list
```

作成されたCodespace名を確認する。

例:

```text
humble-couscous-xxxxxxxxxxxxxxxxx
```

---

## 6. Codespace にSSH接続

```bash
gh codespace ssh -c <CODESPACE_NAME>
```

例:

```bash
gh codespace ssh -c humble-couscous-xxxxxxxxxxxxxxxxx
```

接続後、リポジトリは通常以下に配置されている。

```bash
cd /workspaces/aws_dop-c02_test_simulater
```

確認:

```bash
pwd
git branch --show-current
git status
```

---

## 7. Node.js / npm の確認

```bash
node -v
npm -v
```

Codespacesの標準環境にNode.jsが含まれている場合は、そのまま利用できる。

---

## 8. Codex CLI のインストール

Codespace内で実行する。

```bash
npm install -g @openai/codex
```

確認:

```bash
codex --version
```

---

## 9. Codex CLI にログイン

CodespacesはリモートLinux環境のため、Device Authenticationを利用する。

```bash
codex login --device-auth
```

表示されたURLをブラウザで開き、表示されたコードを入力してOpenAIアカウントで認証する。

認証後はCodespace内に認証情報が保持される。

---

## 10. Codex を起動

リポジトリのルートディレクトリで実行する。

```bash
cd /workspaces/aws_dop-c02_test_simulater
codex
```

Codexから、このリポジトリ内の以下のリソースを利用できる。

```text
ソースコード
問題JSON
Agent Skills
Git履歴
各種設定ファイル
```

---

## 11. Codespace の停止

利用していないCodespaceは停止する。

```bash
gh codespace stop -c <CODESPACE_NAME>
```

停止中はCompute利用時間を消費しない。

Codespace自体を削除しない限り、インストール済みのCodex CLIや各種設定、ファイルは保持される。

---

## Android / Termux から利用する場合

TermuxにGitHub CLIをインストールする。

```bash
pkg update
pkg install gh git
```

GitHubにログインする。

```bash
gh auth login
```

Codespaces権限を追加する。

```bash
gh auth refresh -h github.com -s codespace
```

Codespace一覧を確認する。

```bash
gh codespace list
```

Macで作成したCodespaceと同じ環境にSSH接続できる。

### スマホ / Termux で Codespace 名が省略される場合

`gh codespace list` は端末幅が狭いと Codespace 名が省略表示されることがある。

Codespace 名だけをフル表示する場合:

```bash
gh codespace list --json name --jq '.[].name'
```

```bash
gh codespace ssh -c <CODESPACE_NAME>
```

接続後:

```bash
cd /workspaces/aws_dop-c02_test_simulater
codex
```

これにより、MacとAndroidのどちらから接続しても同一のCodespaces環境、ソースコード、Codex CLIを利用できる。

---

## 運用イメージ

```text
GitHub Repository
      |
      v
GitHub Codespaces
      |
      +-- Codex CLI
      +-- Agent Skills
      +-- 問題JSON
      +-- Node.js
      |
      +------ MacからSSH
      |
      +------ TermuxからSSH
```

接続元の端末は操作用クライアントとして利用し、開発処理はCodespaces、AI推論はOpenAI側で実行する。
