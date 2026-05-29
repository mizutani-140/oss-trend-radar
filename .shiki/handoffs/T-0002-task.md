# Codex Task Handoff: T-0002

Goal: G-0002
Task: T-0002
Branch: shiki/t-0002-search-api-oss-n-markdown-1-cli

## Scope
Python CLI 1本でGitHub Search APIを1回呼び出し、人気OSS上位N件(リポジトリ名/スター数/言語/説明/URL)を取得して reports/<日付>.md を生成する最小エンドツーエンド実装。httpx + pytest を使用。

## Required Skills
- tdd

## Engineering Skills Directory
/Users/kio.mizutani/Documents/lead-os/skills/engineering

## Acceptance Checks
- `python -m ossradar report` 実行で reports/<日付>.md が生成される
- レポートに上位N件のリポジトリ名・スター数・URLが含まれる
- APIレスポンスをモックして整形ロジックを検証するpytestがgreen
