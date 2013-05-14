# coding: utf-8


urls = (
    # 为静态文件添加后缀，使浏览器不读取缓存
    r'/assets/(.+?)', 'StaticFileHandler',

    # 主页
    r'/(由于安全原因，这里面的一个字符串，请自行写一个，用于你授权人人应用时用的)?', 'Home',
    # 授权页面
    r'/connect/renren', 'ConnectRenren',
    # 授权后返回code
    r'/oauth/renren', 'OauthOk',
    # 自动刷新accesstoken
    r'/cron/refresh/token', 'RefreshToken',
    # 发送
    r'/cron/post/renren', 'PostRenren',
    # 时间轴更新
    r'/latest/msg', 'LatestMsg',

    # 维持cookie
    r'/cron/keep/cookie', 'KeepCookie',
)
