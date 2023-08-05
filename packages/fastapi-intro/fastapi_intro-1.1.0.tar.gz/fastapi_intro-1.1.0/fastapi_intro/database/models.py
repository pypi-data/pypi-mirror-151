#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
description: Models for the user app.
AUTHOR: prabal pathak
"""

__all__ = ["UserSchema"]

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base


class UserSchema(Base):
    """
    class= UserSchema
    Functions= __init__, __repr__
    description= constructor, return string representation of the object
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    updated_by = Column(String)
    additional_info = Column(String)

    def __init__(
        self,
        username,
        password,
        email,
        is_admin,
        is_active,
        updated_by,
        additional_info,
    ):
        """
        Function= __init__
        Args= (username, password, email,
        is_admin, is_active, created_at, updated_at, updated_by, additional_info)
        description= constructor
        """
        self.username = username
        self.password = password
        self.email = email
        self.is_active = is_active
        self.is_admin = is_admin
        self.updated_by = updated_by
        self.additional_info = additional_info

    def __repr__(self) -> str:
        """
        Function= __repr__
        Args= self
        description= return string representation of the object
        """
        return "<User('%s','%s','%s')>" % (self.username, self.password, self.email)
