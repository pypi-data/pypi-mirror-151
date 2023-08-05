#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database connection and Base decleartion
Author: Prabal Pathak
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["get_db", "Base", "Session"]

URL = (
    "sqlite:///database.db"  # sqlite:///:memory: or sqlite:///relative/path/to/file.db
)
engine = create_engine(URL, echo=False, connect_args={"check_same_thread": False})
Session = sessionmaker(
    bind=engine
)  # bind=engine for sqlite optional: autocommit=False, autoflush=False
Base = declarative_base()  # Base class for all tables


def get_db():
    """
    Yield a session object
    """
    session = Session()
    try:
        yield session
    finally:
        session.close()
