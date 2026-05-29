# OSS Trend Radar

GitHubのトレンドOSS・スター獲得数をリサーチし、Markdownレポートを生成するツール。

## Usage

```bash
pip install -e .
python -m ossradar report --top 10
# -> reports/<YYYY-MM-DD>.md を生成
```

オプション:

- `--query` GitHub Search クエリ (既定: `stars:>10000`)
- `--top` 取得件数 (既定: 10)
- `--out-dir` 出力ディレクトリ (既定: `reports`)

認証レート上限を上げるには環境変数 `GITHUB_TOKEN` を設定してください。

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Scope (T-0002)

最初の縦切り: Search API を1回呼び出し、人気OSS上位N件を取得して `reports/<日付>.md` を生成するCLI。
定期実行 (GitHub Actions cron) は次の縦切りで対応予定。
