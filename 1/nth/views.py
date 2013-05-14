#!/usr/bin/env python
#coding:utf-8

from functools import partial

import web

from nth import settings, utils, urls, ctrl, librenren


render = settings.render
static_file_handler = partial(utils.static_file_handler, settings.STATIC_DIR)
renren = librenren.renren


class Home:
    '''首页'''
    def GET(self, renren):
        latest = ctrl.get_latest_msg()
        return render('home.html', renren=renren, latest=latest)

    def POST(self, not_use):
        content = web.input().leaf.replace('\n', '').strip()[:120]
        if len(content) < 5:
            return
        pk = ctrl.save_msg(content)
        try:
            if renren.send_msg(u'#{0} {1}'.format(pk, content)):
                ctrl.save_msg_published(pk)
        except:
            pass


class PostRenren:
    def GET(self):
        msg = ctrl.get_next_msg()
        if msg is None:
            return 'no new msg'
        if renren.post_page('#%s %s' % (
                msg.pk, msg.content), ctrl.get_access_token()):
            ctrl.save_msg_published(msg.pk)
        return msg.pk


class LatestMsg:
    def GET(self):
        latest = ctrl.get_latest_msg()
        return render.get_module('utils.html').gen_msg(latest, False)


class ConnectRenren:
    '''进行人人授权'''
    def GET(self):
        raise web.seeother(librenren.OAUTH_URL)


class OauthOk:
    def GET(self):
        code = web.input().get('code')
        if code is not None:
            ctrl.save_token(renren.get_access_token(code))
            return 'oauth ok'
        # 用户点击了查看此应用
        raise web.seeother('/')


class KeepCookie:
    '''第隔15分钟登录一次'''
    def GET(self):
        return renren.login_by_cookie()


class RefreshToken:
    def GET(self):
        ctrl.save_token(renren.refresh(ctrl.get_refresh_token()))
        return 'refresh ok'


def notfound():
    stupid_ie = web.ctx.env['HTTP_USER_AGENT'].lower().find('msie') != -1
    return web.notfound(render('notfound.html', stupid_ie=stupid_ie))


def internalerror():
    return web.internalerror(render.internalerror())


class StaticFileHandler:
    '''静态文件改变了就重新加载，否则读取缓存'''
    def GET(self, path):
        return static_file_handler(path)


app = web.application(urls.urls, globals())
app.add_processor(ctrl.webpy_hook)
app.notfound = notfound
#if not settings.DEBUG:
#    app.internalerror = internalerror


# 添加自定义的模板变量与函数
render._lookup.globals.update({
    # 变量
    'DEBUG': settings.DEBUG,
    # 函数
    'static': partial(utils.static, settings.STATIC_DIR),
})
