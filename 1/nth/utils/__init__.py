#!/usr/bin/env python
#coding:utf-8

# 一些通用的辅助函数

import datetime
import hashlib
import os

import web


md5 = lambda x: hashlib.md5(x).hexdigest()
now = datetime.datetime.now


def gzip_data(data):
    '''gzip压缩'''
    import gzip
    import cStringIO
    accepts = web.ctx.env.get('HTTP_ACCEPT_ENCODING', '')
    if accepts.find('gzip') != -1:
        zbuf = cStringIO.StringIO()
        zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9)
        # render产生的html内容是unicode的
        if isinstance(data, unicode):
            data = data.encode('u8')
        zfile.write(data)
        zfile.close()
        gzipped_data = zbuf.getvalue()
        # 原来的长度
        old_length = len(data)
        # 压缩的的长度[有可能压缩后变大]
        new_length = len(gzipped_data)
        if new_length < old_length:
            web.header('Content-Encoding', 'gzip')
            web.header('Content-Length', str(new_length))
            web.header('Vary', 'Accept-Encoding')
            data = gzipped_data
    return data


def static(static_dir, path):
    '''jinja2模板函数，添加后缀使浏览器决定静态文件是否读取缓存'''
    filename = os.path.join(static_dir, path)
    v = md5(file(filename).read())
    return '/assets/%s?v=%s' % (path, v)


def pathinfo():
    '''得到当前的网址，用于jinja2中高亮当前菜单'''
    return web.ctx.env.get('PATH_INFO', web.config.session.pages[0]['href'])


def static_file_handler(static_dir, path):
    '''静态文件改变了就重新加载，否则读取缓存'''
    import mimetypes
    import stat
    import hashlib
    abspath = os.path.join(static_dir, path)
    stat_result = os.stat(abspath)
    modified = datetime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])
    web.header(
        "Last-Modified", modified.strftime('%a, %d %b %Y %H:%M:%S GMT'))

    mime_type, encoding = mimetypes.guess_type(abspath)
    if mime_type:
        web.header("Content-Type", mime_type)

    # 缓存N年
    N = .5
    cache_time = 86400 * 365 * N
    web.header("Expires", datetime.datetime.now() +
               datetime.timedelta(seconds=cache_time))
    web.header("Cache-Control", "max-age=%s" % cache_time)

    ims_value = web.ctx.env.get("HTTP_IF_MODIFIED_SINCE")
    if ims_value is not None:
        # ie的ims值不标准，所以导致不能正常产生缓存，这里解决
        # IE的是Sat, 02 Feb 2013 14:44:34 GMT; length=4285
        # 标准的为Sat, 02 Feb 2013 14:44:34 GMT
        ims_value = ims_value.split(';')[0]

        since = datetime.datetime.strptime(
            ims_value, '%a, %d %b %Y %H:%M:%S %Z')
        if since >= modified:
            raise web.notmodified()

    with open(abspath, "rb") as f:
        data = f.read()
        hasher = hashlib.sha1()
        hasher.update(data)
        web.header("Etag", '"%s"' % hasher.hexdigest())
        return data


def json(*args, **kwargs):
    '''(dict like object) -> jsonstring

    设置Content-Type为json. 并返回相应的json串.
    >>> json(name='Mr. U', pwd='123')
    '{"pwd": "123", "name": "Mr. U"}'
    >>> json({'a': 1, 'b': 2}, c=3, d=4)
    '{"a": 1, "c": 3, "b": 2, "d": 4}'
    '''

    import json as jsonpy
    kwargs = dict(*args, **kwargs)
    web.header('Content-Type', 'application/json')
    return jsonpy.dumps(kwargs, ensure_ascii=False)
