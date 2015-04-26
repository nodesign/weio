import urllib2, urllib
from tornado import web, ioloop, iostream, gen, httpclient, httputil
import weioConfig
import socket,os,json, subprocess

pathToSave = "/tmp/weio_recovery.bin"

def isConnected(address):
    try:
      # see if we can resolve the host name -- tells us if there is
      # a DNS listening
      host = socket.gethostbyname(address)
      # connect to the host -- tells us if the host is actually
      # reachable
      s = socket.create_connection((host, 80), 2)
      return True
    except:
       pass
    return False

def checkForUpdates():
    data = {}
    if (isConnected("we-io.net") or isConnected("www.github.com")):
        config = weioConfig.getConfiguration()
        repository = ""
        print "REPO", config["weio_update_use_official_repository"]
        if (config["weio_update_use_official_repository"] == "YES") :
            repository = config["weio_update_official_repository"]
        else :
            repository = config["weio_update_alternate_repository"]

        h = httputil.HTTPHeaders({"Accept" : "application/vnd.github.v3+json","User-Agent" : "weio"})
        req = None
        if (config["weio_update_use_official_repository"] == "YES"):
            req = httpclient.HTTPRequest(repository, headers=h)
        else :
            req = httpclient.HTTPRequest(repository)

        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(req, callback=serverData)
    else :
        # not connected to the internet
        print "NO INTERNET CONNECTION"
        data['serverPush'] = "noInternetConnection"
        data['data'] = "Can't reach Internet servers"

def serverData(response):
    print response.body
    config = weioConfig.getConfiguration()

    data = json.loads(response.body)
    lastUpdate = data[0]
    found = False
    for file in lastUpdate["assets"]:
        if ("weio_recovery.bin" in file["name"]):
            print "found weio_recovery"
            fwDownloadLink = file["browser_download_url"]
            fwDownloadSize = file["size"]
            found = True
    if (found == True):
        startDownload(fwDownloadLink, pathToSave)
        sizeOnDisk = os.path.getsize(pathToSave)
        if (fwDownloadSize == sizeOnDisk):
            p = subprocess.Popen(["/etc/init.d/weio_run", "stop"])
            print p.communicate()
            p = subprocess.Popen(["sysupgrade", "-v", pathToSave])
            print p.communicate()
            exit()
        else :
            checkForUpdates()
def startDownload(fwUrl, targetFile):
    print "download init"
    try:
        req = urllib2.Request(fwUrl)
        handle = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print "Can't download firmware, error code - %s." % e.code
        return
    except urllib2.URLError:
        print "Bad URL for firmware file: %s" % fwUrl
        return
    else:
        print "download starts"
        urllib.urlretrieve(fwUrl, targetFile)
        print "download finished"

checkForUpdates()
ioloop.IOLoop.instance().start()