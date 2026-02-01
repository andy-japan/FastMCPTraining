from fastmcp import FastMCP

mcp = FastMCP("Dify Integration Mock Server")

# 過去のQA集を取得するモックツール
@mcp.tool()
def get_qa_history() -> dict:
    """過去のQA集を取得します"""
    return {
        "qas": [
            {"question": "営業時間は？", "answer": "9:00〜18:00です。"},
            {"question": "定休日は?", "answer": "土日祝日です。"},
            {"question": "支払い方法は？", "answer": "現金、クレジットカードが利用可能です。"}
        ]
    }

# ユーザー名簿を取得するモックツール
@mcp.tool()
def get_users() -> dict:
    """ユーザー名簿を取得します"""
    return {
        "users": [
            {"id": 1, "name": "山田太郎", "email": "taro@example.com"},
            {"id": 2, "name": "鈴木花子", "email": "hanako@example.com"},
            {"id": 3, "name": "佐藤次郎", "email": "jiro@example.com"}
        ]
    }

if __name__ == "__main__":
    # SSEトランスポートで起動
    mcp.run(transport="sse")
