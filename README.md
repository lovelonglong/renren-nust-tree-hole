renren-nust-tree-hole
=====================

人人公共主页树洞(搭建于SAE)

开发环境:

    Python v2.7
    Jinja2 v2.6
    Sqlalchemy v0.8
    Web.py v0.37
    MySql

说明：

在浏览器常规窗口中进入人人，登录 **你自己的** 人人账号，先放在一旁备用。

新建一个隐身窗口，进入人人，申请一个马甲，在这个马甲上添加一个公共主页，把这个马甲设置为超级管理员
，进入人人开放平台申请一个web应用，填写相关信息，然后把你自己的人人账号添加为超级管理员。

进入浏览器常规窗口，接受成为管理员的邀请，此时在隐身窗口中将你自己的账号升级为超级管理员。

隐身窗口中进入公共主页管理页面/admin结尾的，打开chrome的console，输入代码`document.cookie`，复制得到的这个字符串(不要复制前后的双引号)，打开1/nth/librenren.py大概在80行左右的cookie这里粘贴。

config.yaml中设置了cron的规则

运行时需要设置的地方包括:

* settings.py中数据库本地的地方(即DB\_NAME, DB\_USER, DB\_PASS)

* url.py中一个url，随便写一个网址，确保这个网址只能你一个人知道(这个网址用于对对公共主页管理员授权的)

比如你设置的是:

    r'/(shuji)?', 'Home',

那么你可以通过访问/shuji这个url来对你的管理员账号授权。

librenren.py中有3个地方根据申请到的api数据设置下(APIKEY, SECRET, CALLBACK\_URL, PAGE\_ID)。


此时应该可以启动调试用服务器了(在1目录下面执行dev\_server.py命令或者双击dev\_server.bat启动服务器)

隐身窗口中进入上面你在url.py中设置的网址，点击页面的人人连接按钮，对马甲账号授权。[关闭隐身窗口，注意，从此不要再登录那个马甲账号]
