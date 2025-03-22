from hyperliquid.info import Info

info = Info()
symbol = "BTC"

mids = info.all_mids()

if symbol in mids:
    print(f"📈 BTCのマーク価格: {mids[symbol]}")
else:
    print("❌ BTCのデータが見つからなかったよ〜😭")
