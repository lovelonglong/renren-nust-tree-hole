#!/usr/bin/env python
#coding:utf-8

import web


class Render:
    '''封装一个全局的模板变量'''
    def __init__(self, path, **kwargs):
        from jinja2 import Environment, FileSystemLoader
        self._lookup = Environment(loader=FileSystemLoader(path), **kwargs)

    def __call__(self, path, *args, **kwargs):
        '''提供简化的模板渲染方法，实现类实例的 ``()`` 功能.

        :param path: 模板路径，可以是相对路径，相对于__init__方法中的path.
        :type path: str.
        :param args: 传递到模板中的参数，字典形式，如 ``{'name': 'Mr. U'}`` .
        :type args: dict.
        :param kwargs: 传递到模板中的参数，以参数的形式传递.

        >>> render = Render(path)
        >>> render('home.html', {'pwd': '123'}, name='Mr. U', what='hello')
        '''

        kwargs = dict(*args, **kwargs)
        web.header('Content-Type', 'text/html')
        return self._lookup.get_template(path).render(**kwargs)

    def get_module(self, path):
        '''渲染某个模板中的某个macro.

        :param path: 要得到的模板的(相对)路径.
        :type path: str.

        >>> render = Render(path)
        >>> render.getModule('func.html').sayHello2Me('Hi!')

        其中func.html中可能会有如下形式的定义::

            {% macro sayHello2Me(what) %}
                <p>Hello {{ what }} </p>
            {% endmacro %}
        '''

        web.header('Content-Type', 'text/html')
        return self._lookup.get_template(path).module
