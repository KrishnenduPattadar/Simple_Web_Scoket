import asyncio
from channels.layers import get_channel_layer
from nsepython import nsefetch

async def start_market_feed():
    layer = get_channel_layer()

    while True:
        try:
            # --- 1️⃣ Fetch main NIFTY 50 index data ---
            all_indices = nsefetch("https://www.nseindia.com/api/allIndices")

            nifty_50 = None
            for index in all_indices["data"]:
                if index["index"] == "NIFTY 50":
                    nifty_50 = {
                        "price": index["last"],
                        "change": index["variation"],
                        "change_percent": index["percentChange"],
                    }
                    break

            # --- 2️⃣ Fetch all 50 stocks under NIFTY 50 ---
            stock_data = nsefetch("https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050")

            stocks = []
            for stock in stock_data["data"]:
                stocks.append({
                    "symbol": stock["symbol"],
                    "price": stock["lastPrice"],
                    "change": stock["change"],
                    "change_percent": stock["pChange"],
                })

            # --- 3️⃣ Send both to WebSocket group ---
            await layer.group_send(
                "market_updates",
                {
                    "type": "market_update",
                    "data": {
                        "nifty_50": nifty_50,
                        "stocks": stocks,
                    },
                },
            )

            print(f"📡 Sent NIFTY 50: {nifty_50['price']} ({nifty_50['change']:+.2f}, {nifty_50['change_percent']:+.2f}%)")
            print(f"📊 Sent {len(stocks)} stock updates")

        except Exception as e:
            print("⚠️ Error fetching NIFTY data:", e)

        await asyncio.sleep(5)  # refresh every 5 seconds
