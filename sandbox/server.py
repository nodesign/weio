import tornado.web
import tornado.ioloop
import tornado.httpserver

import logging

firstTime = True


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        global firstTime
        if (firstTime):
            self.clear_cookie("user")
            firstTime = False

        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)


class LoginHandler(BaseHandler):
    def get(self):
        htmlFile = './login.html'
        self.render(htmlFile)

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.checkPermission(password, username)

        if auth:
            self.set_secure_cookie("user", tornado.escape.json_encode(username))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/login" + error_msg)

        self.redirect("/")

    def checkPermission(self, password, username):
        if username == "admin" and password == "admin":
            return True
        return False


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")

# Make an application into HTTP server
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8081)

logging.getLogger().setLevel(logging.DEBUG)
logging.info(" [*] Listening on 0.0.0.0:8081")

tornado.ioloop.IOLoop.instance().start()
