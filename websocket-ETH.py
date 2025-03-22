import asyncio
import websockets
import json
from datetime import datetime

# トレード方向に応じた色分け
def get_side_color(side):
    if side == "A":
        return "🟢 買い (A)"
    elif side == "B":
        return "🔴 売り (B)"
    return "❓ 未確認"

async def listen():
    uri = "wss://api.hyperliquid.xyz/ws"
    async with websockets.connect(uri) as ws:
        # ETHのトレードデータを購読
        subscribe_message = {
            "method": "subscribe",
            "subscription": {
                "type": "trades",
                "coin": "ETH"
            }
        }
        await ws.send(json.dumps(subscribe_message))
        print("📡 サブスク送信完了！ETHのトレードデータを待機中...")

        while True:
            try:
                response = await ws.recv()

                # 受け取ったレスポンスを表示して内容を確認
                print(f"📩 受け取ったレスポンス: {response}")

                # 文字列の場合は、JSONに変換
                try:
                    if isinstance(response, str):
                        data = json.loads(response)
                    else:
                        data = response
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSONデコードエラー: {e}")
                    continue

                # サブスクリプション応答が届いたときは処理を進めない
                if "subscriptionResponse" in data.get("channel", ""):
                    print("📡 サブスクリプション応答受信: トレードデータが流れてくるのを待機中...")
                    continue  # トレードデータが届くのを待つ

                # トレードデータが届くか確認
                if "data" in data:  # データがある場合
                    trades = data["data"]
                    for trade in trades:
                        price = trade.get("px", "N/A")
                        size = trade.get("sz", "N/A")
                        side = trade.get("side", "N/A")
                        timestamp = trade.get("time", None)

                        # タイムスタンプが存在する場合のみ変換
                        if timestamp:
                            timestamp = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            timestamp = "N/A"

                        # 色分け表示
                        side_display = get_side_color(side)

                        # 見やすい形で出力
                        print(f"📊 [時刻: {timestamp}] ETHトレード → 価格: 💰{price} | サイズ: 📏{size} | {side_display}")

            except websockets.ConnectionClosed:
                print("🔌 接続が閉じられました。再接続を試みます...")
                break
            except Exception as e:
                print(f"⚠️ エラーが発生しました: {e}")
                break

if __name__ == "__main__":
    asyncio.run(listen())
