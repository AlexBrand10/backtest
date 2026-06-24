from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings


def create_access_token(account):
    now = datetime.now(timezone.utc)
    claims = {
        'sub': str(account.id),
        'email': account.email,
        'iat': now,
        'exp': now + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
    }
    return jwt.encode(claims, settings.JWT_SECRET, algorithm='HS256')
