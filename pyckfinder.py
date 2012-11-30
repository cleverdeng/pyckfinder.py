#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Author:cleverdeng
#   E-mail:cleverdeng@gmail.com
#   Description: ckedit+ckfinder+tornado

#说明:鉴于国外作者ckedit+ckfinder+django改造而来，主要使用该作者的前端逻辑。http://code.google.com/p/django-ckeditor-filemanager


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import settings
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

from logic import *

class DirListHandler(tornado.web.RequestHandler):
    def post(self):
        ckfinder = CkFinder()
        self.write(ckfinder.dirlist(self.request))

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class GetInfoHandler(tornado.web.RequestHandler):
    def post(self):
        ckfinder = CkFinder()
        upload_path = self.get_argument("currentpath", "")
        file = self.request.files["newfile"]
        self.write(ckfinder.upload(upload_path, file))

    def get(self):
        ckfinder = CkFinder()
        action = self.get_argument("mode", "")
        if "getinfo" == action:
            info = ckfinder.get_info(self.get_argument("path", ""))
            self.write(info)

        elif "getfolder" == action:
            self.write(ckfinder.get_dir_file(self.get_argument("path", "")))

        elif "rename" == action:
            old_name = self.get_argument("old", "")
            new_name = self.get_argument("new", "")
            self.write(ckfinder.rename(old_name, new_name))

        elif "delete" == action:
            path = self.get_argument("path", "")
            self.write(ckfinder.delete(path))
        
        elif "addfolder" == action:
            path = self.get_argument("path", "")
            name = self.get_argument("name", "")
            self.write(ckfinder.addfolder(path, name))

        else:
            self.write("fail")


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/filemanager/dirlist/?", DirListHandler),
        (r"/", DefaultHandler),
        (r"/filemanager/?", GetInfoHandler),
        (settings.TEMPLATE_URL, tornado.web.StaticFileHandler, dict(path = settings.TEMPLATE_PATH))
    ], static_path=settings.STATIC_PATH, template_path=settings.TEMPLATE_PATH)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(options.port, "0.0.0.0")
    http_server.start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
