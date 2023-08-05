#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Description: pydantic schema for models
Author: Prabal Pathak
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Save user details in the database

    Args:
        BaseModel (class): pydantic basemodel
    """

    username: str
    email: EmailStr
    password: str
    is_admin: bool
    is_active: bool
    updated_by: Optional[str] = None
    additional_info: Optional[str] = None

    class Config:
        """configuration class"""

        orm_mode = True


class User(BaseModel):
    """get user without password

    Args:
        BaseModel (class) : _description_
    """

    id: Optional[int]
    username: str
    is_active: bool
    is_admin: bool
    updated_by: Optional[str] = None
    additional_info: Optional[str] = None

    class Config:
        """configuration class"""

        orm_mode = True


class UserInDB(User):
    """return the password with other user details

    Args:
        User (class): user details
    """

    password: str

    class Config:
        """configuration class"""

        orm_mode = True


if __name__ == "__main__":
    user = {
        "id": 1,
        "username": "John Doe",
        "email": "prabal@gmail.com",
        "password": "232",
        "is_admin": True,
        "is_active": True,
        "additional_info": "age: 23",
    }
    user_model = UserCreate(**user)
    print(user_model.dict())
    print(user_model)
