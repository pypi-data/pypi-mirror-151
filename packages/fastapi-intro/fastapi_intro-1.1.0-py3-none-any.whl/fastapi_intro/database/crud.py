#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
descriptin: create, read, update, delete operations utils -> database
Author: Prabal Pathak
"""


from sqlalchemy.orm import Session
from authentication.auth_settings import pwd_context
from . import models, schema


def get_user(db: Session, username: str):
    """Retrive the user from database

    Args:
        db (Session): _description_
        username (str): _description_

    Returns:
        _type_: _description_
    """
    user = (
        db.query(models.UserSchema)
        .filter(models.UserSchema.username == username)
        .first()
    )
    return user


def create_user(db: Session, user: schema.UserCreate):
    """Create User

    Args:
        db (Session): database connection
        user (schema.UserCreate): user schema

    Returns:
        user(schema.UserCreate): if succesfully saved
    """
    hashed_password = pwd_context.hash(user.password)
    user = user.dict()
    user["password"] = hashed_password
    db_user = models.UserSchema(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user
