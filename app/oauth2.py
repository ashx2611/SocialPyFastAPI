from datetime import datetime, timedelta

from jose import JWTError, jwt

from . import modelschema
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY="09efewjhdfrjwfejkw0e939"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id=payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data=modelschema.TokenData(id=id)

    except JWTError:

        raise credential_exception
        
    return token_data


def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    headers={"WWW=Authenticate":"Bearer"},detail=f"Could not validate credentials")
    return verify_access_token(token,credential_exception)


