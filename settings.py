#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

import os.path
BASE_PATH = os.path.dirname(__file__)
FILE_MANAGER_PATH = os.path.join(BASE_PATH, "static/upload/")
TEMPLATE_PATH = os.path.join(BASE_PATH, "template")
TEMPLATE_URL = r"/template/(.*)"
STATIC_PATH = os.path.join(BASE_PATH, "static")
