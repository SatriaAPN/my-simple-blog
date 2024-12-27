import bcrypt
import logging
from myapp.models import User
from myapp.general_struct import UserStruct
from myapp.utils import hashPassword

logger = logging.getLogger('myapp')

def getUserByEmail(email: str) -> User:
  user = User.objects.filter(email=email).first()

  return user

def getUserById(userId: int) -> User:
  user = User.objects.filter(id=userId).first()

  return user

def createUser(userData: UserStruct) -> User:
  raw_password = userData.password
  hashed_password = hashPassword(raw_password)

  user = User.objects.create(
      name=userData.name,
      email=userData.email,
      hashed_password=hashed_password,
      role="writer"
  )

  return user
