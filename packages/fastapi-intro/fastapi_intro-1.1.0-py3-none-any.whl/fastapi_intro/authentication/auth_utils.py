"""
Description : All Authentication utils
Author: Prabal Pathak
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud, schema
from .schema import TokenData, Token
from .auth_settings import (
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme,
    pwd_context,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


# to get a string like this run:
# openssl rand -hex 32

router = APIRouter()


def verify_password(plain_password: str, password: str) -> str:
    """verify password

    Args:
        plain_password (str): plain password
        password (db password): hashed password

    Returns:
        bool : return constraints
    """
    return pwd_context.verify(plain_password, password)


def get_password_hash(password: str) -> str:
    """get hashed password from plain password

    Args:
        password (str): plain password

    Returns:
        hash password: return password hash
    """
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> dict:
    """get user from database

    Args:
        db (Session): database connection
        username (str): username

    Returns:
        user : detail dictorynary
    """
    db_user = crud.get_user(db, username=username)
    if not db_user:
        return None
    user = schema.UserInDB(**db_user.__dict__)
    return user


def authenticate_user(db: Session, username: str, password: str) -> dict:
    """authenticate the user

    Args:
        db (Session): database connection
        username (str): username
        password (str): password str

    Returns:
        user : if verified
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """create access token

    Args:
        data (dict): user data
        expires_delta (Optional[timedelta], optional): timedelta . Defaults to None.

    Returns:
        string : encoded jwt
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> dict:
    """get current user

    Args:
        token (str, optional): jwt token Defaults to Depends(oauth2_scheme).
        db (Session, optional): database connection  Defaults to Depends(get_db).

    Raises:
        credentials_exception: exception
        credentials_exception: exception
        credentials_exception: exception

    Returns:
        dict: user details
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schema.UserInDB = Depends(get_current_user),
) -> dict:
    """current active user

    Args:
        current_user (schema.UserInDB, optional):
            user in the database . Defaults to Depends(get_current_user).

    Raises:
        HTTPException: exception

    Returns:
        dict: user details
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    """
    login the user
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create", response_model=schema.UserCreate)
async def create_user(
    user: schema.UserCreate,
    db: Session = Depends(get_db),
    current_user: schema.UserInDB = Depends(get_current_active_user),
) -> dict:
    """
    create new user if
    current user is admin
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="Not admin")
    db_user = crud.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/me/", response_model=schema.User)
async def read_users_me(
    current_user: schema.UserInDB = Depends(get_current_active_user),
) -> dict:
    """
    user details
    """
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: schema.UserInDB = Depends(get_current_active_user),
) -> dict:
    """
    items details
    """
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/create_admin")
async def create_admin(db: Session = Depends(get_db)) -> dict:
    """
    create admin
    """
    admin = schema.UserCreate(
        username="admin",
        password="admin",
        email="prabal@gmail.com",
        is_active=True,
        is_admin=True,
    )
    return crud.create_user(db=db, user=admin)
