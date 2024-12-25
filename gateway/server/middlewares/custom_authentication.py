# custom_authentication.py
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework import exceptions
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('myapp')


class JWTUser:
  def __init__(self, payload):
    self.payload = payload

  @property
  def is_authenticated(self):
    return True

  def __getitem__(self, key):
    return self.payload.get(key)

  def get(self, key, default=None):
    return self.payload.get(key, default)


class CustomJWTAuthentication(BaseAuthentication):
  def authenticate(self, request):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
      return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
      raise AuthenticationFailed('Authorization header must be Bearer token')

    token = parts[1]

    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Token is expired')
    except jwt.InvalidTokenError:
      raise AuthenticationFailed('Invalid token')

    if 'user_id' not in payload:
      raise AuthenticationFailed('Invalid token - missing user_id')

    payload["is_authenticated"] = True

    return (JWTUser(payload), token)
