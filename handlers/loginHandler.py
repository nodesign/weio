import base64
import uuid

import tornado

from weioLib import weioConfig

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
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("../www/login.html", errormessage = errormessage)

    def post(self):
        #username = self.get_argument("username", "")
        username = "weio"
        password = self.get_argument("password", "")
        auth = self.checkPermission(password, username)

        if auth:
            self.set_secure_cookie("user", tornado.escape.json_encode(username))
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/login" + error_msg)

    def checkPermission(self, password, username):
        confFile = weioConfig.getConfiguration()
        validPass = confFile['password']
        #if username == "admin" and password == "admin":
        #    return True
        if password == validPass:
            return True
        return False


class WeioLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

def generateCookieSecret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
