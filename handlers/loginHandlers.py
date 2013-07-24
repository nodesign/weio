import base64
import uuid

import tornado

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_login_url(self):
        return u"/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None


class WeioLoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", next=self.get_argument("next","/"))

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.checkPermission(password, username)

        if auth:
            self.set_secure_cookie("user", tornado.escape.json_encode(username))
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/login" + error_msg)

    def checkPermission(self, password, username):
        if username == "admin" and password == "admin":
            return True
        return False


class WeioLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

def generateCookieSecret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
