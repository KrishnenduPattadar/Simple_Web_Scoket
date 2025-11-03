import os
import threading
import asyncio
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chatapp.routing
import market.routing
from market.tasks import start_market_feed

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_socketchat.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatapp.routing.websocket_urlpatterns + market.routing.websocket_urlpatterns
        )
    ),
})

# ✅ Background task runner for simulated Nifty updates
def run_background_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_market_feed())

# ✅ Start background task in a separate thread
threading.Thread(target=run_background_task, daemon=True).start()