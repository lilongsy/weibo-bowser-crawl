# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.engine.url import URL
from setting import DATABASE
from contextlib import contextmanager

engine = create_engine(URL(**DATABASE))
Base = declarative_base()


@contextmanager
def session_scope(s):
    session = s()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class WeiboUser(Base):
    __tablename__ = 'iqilu_weibo_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    user_url = Column(String(255))

class WeiboContent(Base):
    __tablename__ = 'iqilu_weibo_content'
    id = Column(Integer, primary_key=True)
    cid1 = Column(Integer)
    username = Column(String(255))
    url = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime)
    publish_at = Column(DateTime)
    isPublish = Column(Integer)
