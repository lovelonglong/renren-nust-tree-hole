#coding:utf-8

import os

import web
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import sae.const

from nth.utils import template


# 调试是否开启
DEBUG = 'SERVER_SOFTWARE' not in os.environ
web.config.debug = DEBUG
#web.config.debug = True


# 数据库配置
if DEBUG:
    # 本地
    DB_NAME = 'your_db_name'
    DB_USER = 'ur name'
    DB_PASS = 'ur pwd'
    DB_HOST_M = '127.0.0.1'
    DB_PORT = 3306
else:
    # SAE
    DB_NAME = sae.const.MYSQL_DB
    DB_USER = sae.const.MYSQL_USER
    DB_PASS = sae.const.MYSQL_PASS
    DB_HOST_M = sae.const.MYSQL_HOST
    DB_PORT = int(sae.const.MYSQL_PORT)


# sqlalchemy 设置
engine = create_engine(
    'mysql://%s:%s@%s:%s/%s?charset=utf8' %
    (DB_USER, DB_PASS, DB_HOST_M, DB_PORT, DB_NAME),
    encoding='utf8',
    pool_recycle=10,
)
db = scoped_session(sessionmaker(bind=engine))


# 静态文件设置
APP_ROOT = os.path.dirname(__file__)
STATIC_DIR = os.path.join(APP_ROOT, 'static')
TEMPLATE_DIR = os.path.join(APP_ROOT, 'templates')


# jinja2模板设置
render = template.Render(
    TEMPLATE_DIR,
    trim_blocks=True,
    line_comment_prefix='##',
    line_statement_prefix='^',
)
