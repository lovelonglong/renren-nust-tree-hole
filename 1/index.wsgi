#!/usr/bin/env python
#coding:utf-8

import sae
import nth.views


application = sae.create_wsgi_app(nth.views.app.wsgifunc())
