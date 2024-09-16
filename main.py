import http.server
import socketserver
from py.iŋgliks import Translator
import json
from datetime import datetime

now = datetime.now()

PORT = 8000

translator = Translator()


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

  def do_GET(self):
    print("serve")
    if self.path == '/':
      self.path = '/static/index.html'
    elif self.path == '/info':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      text = open("./text/info.txt", "r",
                  encoding="utf8").read().strip() + "\n"
      data = {"info": text}
      self.wfile.write(json.dumps(data).encode())
      return
    elif self.path == '/pronunciation_guide':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      text = open("./text/pronunciation_guide.txt", "r",
                  encoding="utf8").read().strip() + "\n"
      data = {"pronunciation_guide": text}
      self.wfile.write(json.dumps(data).encode())
      return
    return http.server.SimpleHTTPRequestHandler.do_GET(self)

  def do_POST(self):
    if self.path == '/translate':
      # Extract and process the POST data
      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)

      data = json.loads(post_data.decode("utf-8"))
      print(data["text"])
      translated_data, not_in_dict = translator.translate(data["text"])

      # Send a 200 OK response
      self.send_response(200)

      # Send headers
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      data = {"translation": translated_data, "not_in_dict": not_in_dict}
      self.wfile.write(json.dumps(data).encode())
    elif self.path == '/feedback':
      # Extract and process the POST data
      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)

      data = json.loads(post_data.decode("utf-8"))
      print(data["feedback"])
      dt_string = now.strftime("%d-%b-%Y %H:%M:%S")
      open("feedback.txt", "a",
           encoding="utf8").write("[" + dt_string + "] " + data["feedback"] + "\n")

      # Send a 200 OK response
      self.send_response(200)

      # Send headers
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      data = {"feedback_success": True}
      self.wfile.write(json.dumps(data).encode())


Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
  print("Server started at http://localhost:" + str(PORT))
  httpd.serve_forever()
