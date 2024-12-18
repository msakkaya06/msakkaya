from channels.middleware import BaseMiddleware
from django.core.exceptions import PermissionDenied

class WebSocketAllowedHostsMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        allowed_hosts = ['162.162.5.11', '127.0.0.1', 'localhost', '192.168.137.1']
        
        # Sadece WebSocket istekleri için kontrol
        if scope['type'] == 'websocket':
            client_ip = str(scope['client'][0])
            if client_ip not in allowed_hosts:
                raise PermissionDenied("You are not allowed to access this server.")
        
        # Normal akışa devam et
        return await super().__call__(scope, receive, send)
