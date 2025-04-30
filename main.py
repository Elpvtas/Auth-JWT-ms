from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# Fake DB
fake_users_db = {
    "prueba": {
        "username": "prueba",
        "full_name": "Usuario Prueba",
        "email": "usuario@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
    }
}

SECRET_KEY = "113e76771656fd6cbbe0fb52e60ba839f52882bfc9f699bae42b910df654ce6d"
ALGORITHM = "HS256"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer("/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

# Helpers
def get_username(db, username):
    if username in db:
        user_data = db[username]
        # Ajustar la clave full_name → fullname si es necesario
        return UserInDB(**user_data)
    return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username, password):
    user = get_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    expire = datetime.utcnow() + (time_expire or timedelta(minutes=15))
    data_copy.update({"exp": expire})
    return jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)

# Obtener usuario desde el token
def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_username(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Validar si el usuario está deshabilitado
def get_user_disable_user_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

# Rutas
@app.get("/")
def root():
    return "HI i am a fastapi"

@app.get("/andina/me")
def user(user: User = Depends(get_user_disable_user_current)):
    return user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token = create_token({"sub": user.username}, access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
