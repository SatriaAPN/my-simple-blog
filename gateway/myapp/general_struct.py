from collections import namedtuple

JwtDataStruct = namedtuple('JwtDataStruct', ['valid', 'error', 'userId', 'userRole'])