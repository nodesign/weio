Tornado Programing Tutorial
===========================

Introduction
------------
This tutorial explains the basics of Tornado Python server programming
and IOLoop concept.


Installation
------------
Tornado can be installed automatically, via Pythin Installer, i.e. `pip` tool.

    # apt-get install python-setuptools
    # easy_install pip
    # pip install tornado
    # pip install sockjs-tornado


Quick Start
-----------

Tornado is a scalable, non-blocking web server and web application framework written in Python.
It uses IOLoop class, which implements an I/O event loop for non-blocking sockets.

Tornado is a server, so it listens on the port and opens sockets to the clients.

Clients send request to Tornado server via `routes`, and these are basically addresses in the browser.
For example, if Tornado serves and application on `http://example.com` and client goes to this page,
then this addres itself is the route `/` and `http:/example.com/test` is the route `/test`.

For each route Tornado installs handler that is called once a message comes via this route.

Code examples for Tornado always come on two sides : one is server side and another is client side.
One without another does not have a big meaning, and this must be always paired up for the application purposes.


### Server side

    import tornado.httpserver
    import tornado.websocket
    import tornado.ioloop
    import tornado.web
    

    # Define handler
    class MainHandler(tornado.web.RequestHandler):
        """Regular HTTP handler to serve the index page"""
        def get(self):
            self.render('index.html')

    class TestHandler(tornado.websocket.WebSocketHandler): 
        def open(self):
            print 'new connection'
            self.write_message("Hello World")
        
        def on_message(self, message):
            print 'message received %s' % message
    
        def on_close(self):
            print 'connection closed'
    
    # Create main application
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/test', TestHandler),
    ])
    
    if __name__ == "__main__":
        import logging
        logging.getLogger().setLevel(logging.DEBUG)

        # Make an application into HTTP server
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8888)

        logging.info(" [*] Listening on 0.0.0.0:8888")

        tornado.ioloop.IOLoop.instance().start()

### Client Side

    <!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <title>Tornado Test</title>

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

    </head>
    <body>
        <script>
            $(document).ready(function () {
                var ws;

                ws = new WebSocket("ws://" + "localhost" + ":" + "8888" + "/test");
            
                ws.onmessage = function(evt) {alert("message received: " + evt.data)};
            
                ws.onclose = function() { alert("Connection close"); };

                ws.onopen = function() {
                    console.log("ws open");

                };

            });
        </script>

        <p>Tornado test</b></i></p>

    </body>
    </html>


### Explanation

#### Server
##### Main Function
Main application is intantiated in `tornado.web.Application()`. Tuples `(route, handler)` are
provided as an argument.

Handlers are the callbacks that are called once the socket is open or recives a message
via given route from the client.

Tornados IOLoop is started in the end. Tornado turns in the loop and polls opens sockets,
receiving messages or sending them back. This way client side has impression that server
gives a data push only when something happens. In the reality, Tornado always loops,
polling for the new events.

Although this gives the impression of asynchroniosity, a care must be taket not to stop `IOLoop`
by executing some blocking call in Tornado. Better practice is to use `subprocess` and call
these functions in separate process from Tornado, talking to them via pipe or even better via
local (UNIX) socket. Sockets are better choice, as Tornado already implements a bunch of fuctions
to talk to the sockets, like read untill regexp and similar, which are missing for pipe reading.

##### Handlers
`MainHandler()` only renders `index.html`. As it lives on the route `/`, it is called immedialety when
we point the browser to : `localhost:8888`.

`TestHandler()` is called whenever WebSocket is opened on the route `/test`.
This is a JavaScript code example that opens `/test` route in the clients code :

    ws = new WebSocket("ws://localhost:8888/test");

When this happens, `open()` function of `TestHandler()` class is called and the word
`new connection` is printed on the console from which we started Tornado. Also, just after that
a message `Hello World` is sent to the client via the same WebSocket (the one that goes ove `/test` route).


#### Client
HTML code is self evident, apart from the embedded JavaScript. This is where all the magic happends.

The line in the HTML `<head>` :

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

fetches jQuery and is very important. Using standard `$(document).ready()` jQuery function, we can create (i.e. open) WebSocket
via `/test` route.

As explained in the capter before, when opening WebSocket from the client via `/test` route is done,
Tornado server will notice the message (in this case open message) coming via this route, and will
immediately call `TestHandler()` to handle this message. As it this message is WebSocket opening call,
`TestHandler.open()` function will be called.

Since this function also sends some text back to the client via same WebSocket (in our case called `ws`),
`ws.onmessage()` function will be called on the client side. 

N.B. To examine and debug JavaScript and `console.log()` calls in Chrome, use "Shift + Ctrl + J".



SockJS
------
General problem with WebSocket approach is that it is not supported by every browser yet.
So code that works in Chrome will not work in some other browser for example.

SockJS is a wrapper around WebSocket API (if it is supported by browser) or emulator for the browsers
that do not support it. This way it gives unified programming interface for asynchronious web application
with server push (i.e. WebSocket technology).

From the SockJS documentation :

*SockJS is a browser JavaScript library that provides a WebSocket-like object.
SockJS gives you a coherent, cross-browser, Javascript API which creates a low latency, full duplex,
cross-domain communication channel between the browser and the web server.

Under the hood SockJS tries to use native WebSockets first.
If that fails it can use a variety of browser-specific transport protocols and presents
them through WebSocket-like abstractions.

SockJS is intended to work for all modern browsers and in environments which
don't support WebSocket protcol, for example behind restrictive corporate proxies.*


Here is the example of using SockJS API with Tornado :

### Server

    from tornado import web, ioloop
    from sockjs.tornado import SockJSRouter, SockJSConnection

    class TestConnection(SockJSConnection):
        def on_message(self, msg):
            logging.info("Handshake successful")

        def on_open(self, info):
            logging.info("ON_OPEN")

    if __name__ == '__main__':
        import logging
        logging.getLogger().setLevel(logging.DEBUG)

        TestRouter = SockJSRouter(TestConnection, '/test')

        app = web.Application(TestRouter.urls)
        app.listen(8081)

        logging.info(" [*] Listening on 0.0.0.0:8081/test")

        ioloop.IOLoop.instance().start()

    
### Client

    <!doctype html>
    <html><head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        <script src="http://cdn.sockjs.org/sockjs-0.3.min.js"></script>

        </head>

        <body lang="en">
        <h1>SockJS Echo example</h1>

        <script>
            var sockjs_url = 'http://localhost:8081/test';		 
            var sockjs = new SockJS(sockjs_url);

            sockjs.onopen    = function()  {console.log('[*] open', sockjs.protocol);};
            sockjs.onclose   = function()  {console.log('[*] close');};
        </script>

    </body></html>


### Explanation

SockJS mimics WebSockets API but instead of WebSocket there is a SockJS Javascript object.

First, you need to load SockJS JavaScript library, for example you can put that in your http head:

    <script src="http://cdn.sockjs.org/sockjs-0.3.min.js"></script>

After the script is loaded you can establish a connection with the SockJS server. Here's a simple example:

    <script>
    var sock = new SockJS('http://mydomain.com/my_prefix');
    sock.onopen = function() {
        console.log('open');
    };
    sock.onmessage = function(e) {
        console.log('message', e.data);
    };
    sock.onclose = function() {
        console.log('close');
    };
    </script>

**N.B** *You can observe `console.log()` messages in browser by pressing Ctrl+Shift+J in Chrome*


JSON VS. XML
------------

In different languages data is held in structures of different data types.
To exchange these data objects between server and client, they have to be serialized and sent over
TCP/IP (Internet) Socket, which can only transfer raw bytes - i.e. serialized data - and has
no notion of structure.

When data are fetched on the server side of the socket, they can be casted into appropriate structure.

But what if the data are fetched on the client side? While JavaScript can cast this data into some
internal structure, most often server sends HTML presentable strings themselfs.

This is where XML came into the play, because it became possible to describe a data structure
in the string format, and then send this string "as is", i.e. as a an array of character bytes to the client.

JavaScript running on the client would then parse XML and pick up the structure members and present them
in right places.

### XML
The XMLHttpRequest object is used to exchange data with a server behind the scenes.

The XMLHttpRequest object is a developer's dream, because you can:

* Update a web page without reloading the page
* Request data from a server after the page has loaded
* Receive data from a server after the page has loaded
* Send data to a server in the background

All modern browsers have a built-in XML parser.

An XML parser converts an XML document into an XML DOM object - which can then be manipulated with JavaScript.


### JSON
JSON,  or JavaScript Object Notation, is a text-based open standard designed
for human-readable data interchange. It is derived from the JavaScript scripting
language for representing simple data structures and associative arrays, called objects.
Despite its relationship to JavaScript, it is language-independent, with parsers available for many languages.

The JSON format is often used for serializing and transmitting structured data over a network connection.
It is used primarily to transmit data between a server and web application, serving as an alternative to XML.

### Server

    from tornado import web, ioloop.
    from sockjs.tornado import SockJSRouter, SockJSConnection

    class EchoConnection(SockJSConnection):
        def on_message(self, msg):
        logging.info("Handshake successful")
        self.send(msg)

        def on_open(self, info):
            logging.info("ON_OPEN")

    if __name__ == '__main__':
        import logging
        logging.getLogger().setLevel(logging.DEBUG)

        EchoRouter = SockJSRouter(EchoConnection, '/echo')

        app = web.Application(EchoRouter.urls)
        app.listen(8081)

        logging.info(" [*] Listening on 0.0.0.0:8081/echo")

        ioloop.IOLoop.instance().start()

### Client

    <!doctype html>
    <html><head>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        <script src="http://cdn.sockjs.org/sockjs-0.3.min.js"></script>
        <style>
        .box {
            width: 300px;
            float: left;
            margin: 0 20px 0 20px;
        }
        .box div, .box input {
            border: 1px solid;
            -moz-border-radius: 4px;
            border-radius: 4px;
            width: 100%;
            padding: 0px;
            margin: 5px;
        }
        .box div {
            border-color: grey;
            height: 300px;
            overflow: auto;
        }
        .box input {
            height: 30px;
        }
        h1 {
            margin-left: 30px;
        }
        body {
            background-color: #F0F0F0;
            font-family: "Arial";
        }
        </style>

    </head><body lang="en">
        <h1>SockJS Echo example</h1>
        <div id="first" class="box">
            <div></div>
            <form><input autocomplete="off" value="Type here..."></input></form>
        </div>
        <script>
            //var sockjs_url = '/echo';
            var sockjs_url = 'http://localhost:8081/echo';		 
            var sockjs = new SockJS(sockjs_url);
            $('#first input').focus();

            var div  = $('#first div');
            var inp  = $('#first input');
            var form = $('#first form');

            var print = function(m, p) {
                p = (p === undefined) ? '' : JSON.stringify(p);
                div.append($("<code>").text(m + ' ' + p));
                div.append($("<br>"));
                div.scrollTop(div.scrollTop()+10000);
            };

            sockjs.onopen    = function()  {print('[*] open', sockjs.protocol);};
            sockjs.onmessage = function(e) {print('[.] message', e.data);};
            sockjs.onclose   = function()  {print('[*] close');};

            form.submit(function() {
                print('[ ] sending', inp.val());
                sockjs.send(inp.val());
                inp.val('');
                return false;
            });
        </script>
        </body></html>



### Explanation
#### JavaScript
A JSON parser will recognize only JSON text, rejecting all scripts.
In browsers that provide native JSON support, JSON parsers are also much faster than eval.
It is expected that native JSON support will be included in the next ECMAScript standard.

    var myJSONText = JSON.stringify(myObject, replacer);

A JSON stringifier goes in the opposite direction, converting JavaScript data structures into JSON text.
JSON does not support cyclic data structures, so be careful to not give cyclical
structures to the JSON stringifier.

    var myObject = JSON.parse(myJSONtext, reviver);

#### Python
The json module provides an API similar to pickle for converting in-memory Python objects to a
serialized representation known as JavaScript Object Notation (JSON).
Unlike pickle, JSON has the benefit of having implementations in many languages
(especially JavaScript), making it suitable for inter-application communication. 

Python makes a difference between "dump()" and "dumps()" mehods :
The pickle.dumps() function (note the 's' at the end of the function name) performs the same
serialization as the pickle.dump() function. Instead of taking a stream object and writing
the serialized data to a file on disk, it simply returns the serialized data.

The encoder understands Python’s native types by default (string, unicode, int, float, list, tuple, dict).

    import json

    data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
    print 'DATA:', repr(data)

    data_string = json.dumps(data)
    print 'JSON:', data_string
    
Values are encoded in a manner very similar to Python’s repr() output.

    $ python json_simple_types.py

    DATA: [{'a': 'A', 'c': 3.0, 'b': (2, 4)}]
    JSON: [{"a": "A", "c": 3.0, "b": [2, 4]}]


Encoding, then re-decoding may not give exactly the same type of object.

    import json

    data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
    data_string = json.dumps(data)
    print 'ENCODED:', data_string

    decoded = json.loads(data_string)
    print 'DECODED:', decoded

    print 'ORIGINAL:', type(data[0]['b'])
    print 'DECODED :', type(decoded[0]['b'])

In particular, strings are converted to unicode and tuples become lists.

    $ python json_simple_types_decode.py

    ENCODED: [{"a": "A", "c": 3.0, "b": [2, 4]}]
    DECODED: [{u'a': u'A', u'c': 3.0, u'b': [2, 4]}]
    ORIGINAL: <type 'tuple'>
    DECODED : <type 'list'>


Bootstrap
---------
Twitter Bootstrap is a free collection of tools for creating websites and web applications.
It contains HTML and CSS-based design templates for typography, forms, buttons,
charts, navigation and other interface components, as well as optional JavaScript extensions.

Basically, it is HTML framework, used for crating static HTML sites with JavaScript.

Weio project uses it as the presentation layer, i.e. for creating the static content that will be presented
in the browser on the client side.

It also uses jQuery JavaScript library that seamlessly integrates into the Bootstrap to do browser side scripting
and communication to the Tornado server via SockJS Client JavaScript library.

Here is the example of the script that gets the Bootstrap and does Hello World :

    #!/bin/bash

    wget http://twitter.github.io/bootstrap/assets/bootstrap.zip
    unzip bootstrap.zip
    cd bootstrap/

    cat << END > index.html
    <!DOCTYPE html>
    <head>
        <title>Twitter Bootstrap</title>
        <style type='text/css'></style>

        <link href="css/bootstrap.min.css" rel="stylesheet">
        <script src="js/bootstrap.min.js"></script>

    </head>
    <body>
        Hello World!
        <button type="button" class="btn">Button</button>
    </body>
    </html>
    END





References
----------
 * https://github.com/sihirliparmakcan/simple_websocket_example
 * http://srchea.com/blog/2011/12/build-a-real-time-application-using-html5-websockets/
 * http://www.rabbitmq.com/blog/2011/09/13/sockjs-websocket-emulation/
 * http://getpython3.com/diveintopython3/serializing.html
