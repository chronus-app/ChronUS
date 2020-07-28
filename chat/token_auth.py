from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed 

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
        token = query['token']
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token!")
        scope['student'] = token.user.student
        return self.inner(scope)