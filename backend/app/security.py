"""
RoboPulse Fleet Command Center
Day 5 - password hashing and JWT helpers.

SECRET_KEY follows the same env-var-with-fallback pattern as Day 3's
DATABASE_URL - a known, deliberate shortcut. Week 3's bin/setup.sh
(from the problem statement) is where this project formally moves
secrets into a real .env file; don't commit a real secret key here.
"""

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

## Security constants and helper functions for password hashing and JWT token management.
SECRET_KEY = os.environ.get("SECRET_KEY", "<replace-with-a-real-secret-key>")
#algorithm used for signing the JWT tokens. There are other algorithms available, 
# but HS256 is a common choice for symmetric signing.
ALGORITHM = "HS256"
#the expiration time for access tokens, in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#We need to create two functions for password hashing and verification to
#make sure that we are never storing plain text passwords in the database. 
# Instead, we store a hashed version of the password, which is a one-way 
# transformation that cannot be easily reversed.

#this function takes a plain text password as input, hashes it using bcrypt, 
# and returns the hashed password as a string.
def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


#this function takes a plain text password and a hashed password as input,
# and checks if the plain text password matches the hashed password.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


#this function creates a JWT access token with the provided data and an optional expiration time.
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    #to_encode is a copy of the input data dictionary, which will be used 
    # to create the payload of the JWT token.
    to_encode = data.copy()
    #check if an expiration time was provided; if not, use the default expiration time defined 
    # by ACCESS_TOKEN_EXPIRE_MINUTES.
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#this function decodes a JWT access token and returns the payload as a dictionary.
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])