from fastapi import Depends, HTTPException, status
#from passlib.context import CryptContext
from models.request.tokens import TokenData
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.data.sqlalchemy_data import Usuario
from repository.users import UsersRepository
from db_config.sqlalchemy_connect import sess_db
from jose import jwt, JWTError
from datetime import datetime, timedelta

#crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
"""
def get_password_hash(password):
    return crypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

def authenticate(username, password, usuario:Usuario):
    try:
        #password_check = verify_password(password, account.passphrase)
        return password_check
    except Exception as e:
        print(e)
        return False    

"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login/token")

SECRET_KEY = "tbWivbkVxfsuTxCP8A+Xg67LcmjXXl/sszHXwH+TX9w="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(data: dict, expires_after: timedelta):
    print(data)
    plain_text = data.copy()
    print(plain_text)
    expire = datetime.utcnow() + expires_after
    plain_text.update({"exp": expire})
    print(plain_text)
    encoded_jwt = jwt.encode(plain_text, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), sess:Session = Depends(sess_db) ):
    print("Inicio get_current_user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    userrepo = UsersRepository(sess)
    user = userrepo.get_all_login_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def authenticate(username, password, usuario:Usuario):
    try:
        #password_check = verify_password(password, account.passphrase)
        if password==usuario.password:
            print("Autenticado")
            password_check=True
        else:
            print("NO Autenticado")
            password_check=False
        return password_check
    except Exception as e:
        print(e)
        return False 