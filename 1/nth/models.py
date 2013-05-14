#coding:utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.mysql import INTEGER

import sys
sys.path.insert(0, '../')

from nth import settings, utils

db = settings.db

Base = declarative_base()


class Msg(Base):
    __tablename__ = 'msg'

    pk = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    content = Column(String(120), nullable=False)
    date = Column(DateTime, default=utils.now, index=True)
    published = Column(Boolean, default=False, index=True)


class Oauth(Base):
    __tablename__ = 'oauth'

    pk = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    access_token = Column(String(200))
    refresh_token = Column(String(200))


# 初始化数据库
def initDb():
    metadata = Base.metadata
    metadata.create_all(settings.engine)


if __name__ == '__main__':
    initDb()
