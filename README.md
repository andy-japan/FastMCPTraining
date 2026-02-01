# Dify連携用MCPサーバー（モック）

FastMCPを使用したMCP（Model Context Protocol）サーバーのモック実装です。
Difyや他のAIクライアントから外部システム連携を試すために使用できます。

## 機能

このMCPサーバーは以下のツールを提供します：

- **get_qa_history**: 過去のQA集を取得（モックデータ）
- **get_users**: ユーザー名簿を取得（モックデータ）

## 起動方法

```bash
docker compose up -d
```

## 接続情報

### エンドポイント
```
http://localhost:8000/sse
```

MCPサーバーは**SSE（Server-Sent Events）トランスポート**で起動しています。

### Difyからの接続方法

Difyの設定で以下のように指定します：

1. **MCP Server URL**: `http://localhost:8000/sse`
2. **Transport Type**: `SSE`

### Pythonクライアントからの接続例

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/sse") as client:
        # QA履歴を取得
        result = await client.call_tool(
            name="get_qa_history", 
            arguments={}
        )
        print(result)
        
        # ユーザー一覧を取得
        result = await client.call_tool(
            name="get_users", 
            arguments={}
        )
        print(result)

asyncio.run(main())
```

## ログの確認

```bash
docker compose logs -f mcp-server
```

## 停止方法

```bash
docker compose down
```

## ファイル構成

```
.
├── docker-compose.yml
├── mcp_server/
│   ├── main.py           # MCPサーバー本体
│   ├── requirements.txt  # Python依存パッケージ
│   └── Dockerfile        # Dockerイメージ定義
└── README.md
```

## カスタマイズ

`mcp_server/main.py`を編集して、新しいツールを追加したり、既存のモックデータを変更できます。

```python
@mcp.tool()
def your_custom_tool(param: str) -> dict:
    """あなたのカスタムツール"""
    return {"result": "カスタム結果"}
```

変更後は再ビルドが必要です：

```bash
docker compose down
docker compose build
docker compose up -d
```
