# coding: utf-8


import json

from netbase import Net


# 开发者中心回去的API Key 和 Secret Key
APIKEY = '这里是API KEY'
SECRET = '这里是SECRET KEY'
CALLBACK_URL = '这里是你的授权后回调地址'
#CALLBACK_URL = 'http://localhost:8080/调试时候用的回调地址，注意修改人人应用里面的相应地方'

# 获取Authorization Code 的URI
AUTHORIZATION_URI = 'https://graph.renren.com/oauth/authorize'
# 获取Access Token 的URI
ACCESS_TOKEN_URI = 'https://graph.renren.com/oauth/token'
# 人人API Session Key 资源URI
SESSION_KEY_URI = 'https://graph.renren.com/renren_api/session_key'
# 人人API Server URI
API_SERVER = 'https://api.renren.com/restserver.do'
# 授权地址
OAUTH_URL = '{0}?client_id={1}&redirect_uri={2}&response_type=code&scope=read_user_message+admin_page+publish_feed+status_update'.format(AUTHORIZATION_URI, APIKEY, CALLBACK_URL)
# 主页id
PAGE_ID = 601730243

n = Net()


class RenRen(object):
    def __init__(self):
        self.params = dict(
            v='1.0',
            format='json',
            call_id=0,
            page_id=PAGE_ID
        )
        self.login_by_cookie()

    def get_access_token(self, code):
        params = dict(
            grant_type='authorization_code',
            client_id=APIKEY,
            redirect_uri=CALLBACK_URL,
            client_secret=SECRET,
            code=code
        )
        return json.loads(n.post(ACCESS_TOKEN_URI, params))

    def refresh(self, refresh_token):
        params = dict(
            grant_type='refresh_token',
            client_id=APIKEY,
            refresh_token=refresh_token,
            client_secret=SECRET
        )
        return json.loads(n.post(ACCESS_TOKEN_URI, params))

    def post_page(self, content, access_token):
        if isinstance(content, unicode):
            content = content.encode('u8')
        params = {}
        params.update(self.params)
        params.update(dict(
            access_token=access_token,
            status=content,
            method='status.set'
        ))
        ret = json.loads(n.post(API_SERVER, params))
        return ret.get('result', 0) == 1

    # 以下代码为非oauth授权用户的操作
    _net = Net()

    def login_by_cookie(self, cookie=None):
        '''刷新cookie用的'''
        import re
        if cookie is None:
            cookie = '在chrome的js控制台，输入document.cookie出来的那个字符串，写在这里，注意前后无双引号'
        try:
            c = 'Cookie', cookie
            if c not in self._net.opener.addheaders:
                self._net.opener.addheaders.append(c)
            self._net.get('http://page.renren.com/601730243/admin')
            p = re.compile("get_check:'(.*)',get_check_x:'(.*)',env")
            h = self._net.get('http://page.renren.com/%s/fdoing' % PAGE_ID)
            result = p.search(h)
            self._token = {
                'requestToken': result.group(1),
                '_rtk': result.group(2)
            }
            return self._token
        except:
            pass

    def send_msg(self, content):
        if isinstance(content, unicode):
            content = content.encode('u8')
        params = {
            'pid': PAGE_ID,
            'c': content
        }
        params.update(self._token)
        r = json.loads(self._net.post(
            'http://page.renren.com/doing/update', params))
        return r['code'] == 0


renren = RenRen()
#print renren.login_by_cookie()
