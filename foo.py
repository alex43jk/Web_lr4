from webob import Request, Response

from jinja2 import Environment, FileSystemLoader

req = Request.blank('/index.html')
req.host = 'localhost'
req.accept = 'text/html'
req.http_version = 'HTTP/1.1'

assets = [
  'app.js',
  'react.js',
  'leaflet.js',
  'D3.js',
  'moment.js',
  'math.js',
  'main.css',
  'bootstrap.css',
  'normalize.css',
]

STYLES = []
SCRIPTS = []

for item in assets:
    itemsplited = item.split('.')
    if itemsplited[1] == 'js':
        SCRIPTS.append(item)
    elif itemsplited[1] == 'css':
        STYLES.append(item)

class WsgiTopBottomMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
      response = self.app(environ, start_response).decode()

      if response.find('<head>' and '<body>') > -1:
        htmlstart, head = response.split('<head>')
        datahead, body = head.split('</head>')
        head1, bodytag = body.split('<body>')
        databody, end = bodytag.split('</body>')
        
        yield (htmlstart + data + end).encode() 
      else:
        yield (response).encode()

def app(environ, start_response):
  response_code = '200 OK'
  response_type = ('Content-Type', 'text/HTML')
  start_response(response_code, [response_type])
  return ''''''

app = WsgiTopBottomMiddleware(app)

req2 = Request.blank('/index.html')

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('index.html')
print(template.render(javascripts=SCRIPTS, styles=STYLES))

print(req2.get_response(app))
