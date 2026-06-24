import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import Account


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = b'bearer'

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).split()
        if not header or header[0].lower() != self.keyword:
            return None
        if len(header) != 2:
            raise exceptions.AuthenticationFailed('Encabezado de autorización inválido')

        try:
            claims = jwt.decode(header[1].decode(), settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('El token ha expirado')
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Token inválido')

        account = Account.objects.filter(pk=claims.get('sub')).first()
        if account is None:
            raise exceptions.AuthenticationFailed('Cuenta no encontrada')
        return account, header[1].decode()
