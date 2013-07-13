from tornado import ioloop, httpclient


def get_file(url):
    http_client = httpclient.AsyncHTTPClient()
    http_client.fetch(url, callback=done)


def done(response):
    with open("./weioVersion.weio", "w") as f:
        f.write(response.body)
    print "DONE"


get_file("http://www.we-io.net/downloads/weioVersion.weio")
ioloop.IOLoop.instance().start()