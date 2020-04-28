from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import urllib
import sys
try:
    from os import scandir
except ImportError:
    from scandir import scandir  # use scandir PyPI module on Python < 3.5

# This is a web file browser for folders which may contain millions of images
# default behaviour - show only first MAX_FILES from each folder (unordered, as in file system table)
MAX_FILES = 50

class MyHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def end_headers (self):
        # This will allow use images from this server in other web scripts, google "CORS"
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        #if '.jpg' in self.path or '.jpeg' in self.path or '.png' in self.path:
        qget = self.path.split('?')
        nolim=0
        allsort=0
        if len(qget)>1:
            if qget[1].startswith('nolim'):
                nolim=1
            if qget[1].startswith('nolimsort'):
                allsort=1
            self.path = qget[0]
        self.path = urllib.parse.unquote(self.path)
        if self.path != '/' and self.path != '' and self.path[-1] != '/':
            return SimpleHTTPRequestHandler.do_GET(self)

        self._set_headers()

        self.put("""<html>
        <head>
          <meta charset="UTF-8">
          <style>
            ul {
              display: inline-flex;
              margin: 0px;
            }
            li {
              list-style-type: none;
              padding: 0px;
              margin: 0px;
              position: relative;
              z-index: auto;
            }
            .large {
              position: absolute;
              left: -9999px;
            }
            li:hover .large {
                left: 80px;
                top: 0px;
                z-index: 99999;
                box-shadow: 0px 0px 3px 3px rgba(127, 127, 127, 0.25); 
            }

          a.button {
             /* -webkit-appearance: button;
              -moz-appearance: button;
              appearance: button;
*/

              text-decoration: none;
              color: initial;
              margin-left: 3px;
              margin-top: 8px;
              padding: 0px 8px 0 8px;
          }
            a.dir {
                color: #00f;

            }
          </style>
        </head>
        <body>"""+ "<h2>"+self.path+"</h2><hr/>");
        self.put('<a href="'+self.path+'?nolim">view all</a>|' )
        self.put('<a href="'+self.path+'?nolimsort">view all sorted</a><br/>' )
        n = 0
        print("self.path=", self.path)
        folder_iter = sorted(scandir('.'+self.path), key=lambda e: e.path) if allsort==1 else scandir('.'+self.path)
        for entry in folder_iter:
            suf=''
            dir_class = ''
            if entry.is_dir():
                suf='/'
                dir_class='dir'
            p='<a class=button href="/"><b>./&nbsp;</b></a>'
            pref=''
            fp = entry.path
            parts = fp.split('/')
            for i in range(1,len(parts)):
                s = "/".join(parts[0:i+1])
                pref += pref + s + '/'
                sep='/'
                if i >= (len(parts)-1):
                    sep = suf
                    p += '<a class="'+dir_class+' button" href="/' + s + sep + '">' + parts[i] + sep + '</a>'
                else:
                    p += '<a class=button href="/' + s + sep + '">' + parts[i] + sep + '</a>'

            self.put(p)
            if  entry.name[-4:] in ('.jpg', '.png', '.bmp', '.JPG', '.PNG', '.BMP'):
                self.put('<ul><li>')
                self.put('<img height=64 src="' + entry.name + '">')
                self.put('<span class="large"> <img height=300 class=large-image src="' + entry.name + '"></span>')
                self.put('</li></ul>')

            self.put('<br/>')
            n+=1
            if n > MAX_FILES and nolim == 0:
                self.put('<b>this folder has MORE files</b>'+'<a href="'+self.path+'?nolim">view all</a>' )
                self.put('<a href="'+self.path+'?nolimsort">view all sorted</a>' )
                break

        self.put('<hr/></body></html>');

    def put(self, line):
         self.wfile.write(line.encode())

    def do_HEAD(self):
        self._set_headers()




class ThreadingSimpleServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8080

print("Using port ", port)
server = ThreadingSimpleServer(('', port), MyHandler)
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print("Done")


