import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
import json
import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

PIN = 26

class HandleRequests(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        '''Reads post request body'''
        self._set_headers()
        if "on" in self.path:
           GPIO.setmode(GPIO.BCM)
           GPIO.setup(PIN, GPIO.OUT)
           GPIO.output(PIN, 1)
        else:
           GPIO.output(PIN, 0)
           GPIO.cleanup()
        self.wfile.write(str.encode(json.dumps({ "result": "ok" })))
try:
  host = ''
  port = 7000
  http.server.HTTPServer((host, port), HandleRequests).serve_forever()
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program  

