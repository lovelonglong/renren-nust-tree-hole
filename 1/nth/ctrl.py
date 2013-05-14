#!/usr/bin/env python
#coding:utf-8


import web

import nth.utils as utils
from nth import models, settings


db = settings.db


def webpy_hook(handler):
    '''webpy钩子'''
    try:
        data = handler()
        if data is not None:
            data = utils.gzip_data(data)
        headers = dict(web.ctx.headers)
        web.ctx.headers = list(headers.viewitems())
        return data
    except web.HTTPError:
        raise
    finally:
        db.close()


def save_token(jsn):
    '''保存授权后的access_token和refresh_token'''
    db.merge(models.Oauth(
        pk=1,
        access_token=jsn['access_token'],
        refresh_token=jsn['refresh_token']))
    db.commit()


def get_refresh_token():
    return db.query(models.Oauth.refresh_token).first().refresh_token


def get_access_token():
    return db.query(models.Oauth.access_token).first().access_token


def save_msg(content):
    msg = models.Msg(content=content)
    db.add(msg)
    db.commit()
    return msg.pk


def get_next_msg():
    M = models.Msg
    return db.query(M.pk, M.content).filter_by(
        published=False).order_by(M.date.asc()).first()


def save_msg_published(pk):
    db.query(models.Msg).filter_by(pk=pk).update({'published': True})
    db.commit()


def get_latest_msg():
    '''时间轴'''
    M = models.Msg
    return db.query(M.pk, M.content, M.date).order_by(M.date.desc()).limit(10)
