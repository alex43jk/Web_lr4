class WsgiTopBottomMiddleware(object):
  def __init__(self, app):
    self.app = app
    self.assets = [
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
    self.styles = []
    self.scripts = []

def __call__(self, environ, start_response):
  response = self.app(environ, start_response).decode()

  if response.find('<head>' and '<body>') > -1:
    htmlstart, head = response.split('<head>')
    datahead, body = head.split('</head>')
    head1, bodytag = body.split('<body>')
    databody, end = bodytag.split('</body>')
    # Заполняю списки styles и scripts, и потом отдельно вывожу styles в <head>, а scripts в <body> 
    for item in self.assets:
      itemsplited = item.split('.')
      if itemsplited[1] == 'js':
        self.scripts.append(item)
      elif itemsplited[1] == 'css':
        self.styles.append(item)
    styles = "\n".join(
      [
        '<link rel="stylesheet" href="/_static/{}"/>'\
        .format(item)
        for item in self.styles
      ]
    )
    scripts = "\n".join(
      [
        '<script src="/_static/{}"></script>'\
        .format(item)
        for item in self.scripts
      ]
    )
    data = '<head>' + datahead + styles + '</head>' + '<body>' + databody + scripts + '</body>'
    yield (htmlstart + data + end).encode() 
  else:
    yield (response).encode()

def app(environ, start_response):
  response_code = '200 OK'
  response_type = ('Content-Type', 'text/HTML')
  start_response(response_code, [response_type])
  return '''
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>HTML Document</title>
</head>
<body>
<p>
<b>
This text is bold,
<i>a etot kursiv</i>
</b>
</p>
</body>
</html>
'''.encode()

app = WsgiTopBottomMiddleware(app)

from wsgiref.simple_server import make_server
make_server('0.0.0.0', 8000, app).serve_forever()
