from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import users.routing as users_routing


application = ProtocolTypeRouter(
	{
		'websocket': AuthMiddlewareStack(
			URLRouter(
				users_routing.websocket_urlpatterns
			)
		)
	}
)

