import asyncio
from channels.layers import get_channel_layer
from nsepython import nsefetch

async def start_market_feed():
    layer = get_channel_layer()

    while True:
        try:
            data = nsefetch("https://www.nseindia.com/api/allIndices")

            price = None
            change = None
            change_percent = None

            for index in data["data"]:
                if index["index"] == "NIFTY 50":
                    price = index["last"]
                    change = index["variation"]
                    change_percent = index["percentChange"]
                    break

            if price:
                await layer.group_send(
                    "market_updates",
                    {
                        "type": "market_update",
                        "data": {
                            "nifty_50": price,
                            "change": change,
                            "change_percent": change_percent,
                        },
                    }
                )
                print(f"Sent live NIFTY 50: {price} ({change:+.2f}, {change_percent:+.2f}%)")

            else:
                print("Nifty 50 not found in response")

        except Exception as e:
            print("Error fetching Nifty data:", e)

        await asyncio.sleep(1)
