import bcrypt
import logging
from myapp.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from myapp.general_struct import UserStruct

logger = logging.getLogger('myapp')

def getUserByEmail(email: str) -> User:
  user = User.objects.filter(email=email).first()

  return user

def createUser(userData: UserStruct) -> User:
  raw_password = userData.password 
  hashed_password = str(bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()))

  user = User.objects.create(
      name=userData.name,
      email=userData.email,
      hashed_password=hashed_password.decode('utf-8'),
      role="writer"
  )

  return user