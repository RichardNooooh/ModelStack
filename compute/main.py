# import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import json

import uuid

from jobs import JobQueue, JobEncoder, Job
from time import sleep

from threading import Thread

HOST, PORT = "localhost", 42069

class JobControlHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        JobQueue.lock.acquire()
        # try:
        q = [json.dumps(job, cls=JobEncoder) for job in JobQueue.queue]
        # finally:
        JobQueue.lock.release()

        self.wfile.write(json.dumps({"queue": q}).encode('utf-8'))

    def do_POST(self):
        print("> Entered POST")
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        print("> About to acquire lock")
        JobQueue.lock.acquire()
        print("> Acquired lock")
        try:
            JobQueue.queue.append(Job(uuid.uuid4()))
        finally:
            JobQueue.lock.release()
        print("> Released lock")
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message).encode('utf-8'))
    

def run_http_server():
    server = HTTPServer((HOST, PORT), JobControlHandler)
    server.serve_forever()

if __name__ == "__main__":
    Thread(target=run_http_server, daemon=True).start()

    # we run the job q system indefinitely..
    while True:
        JobQueue.lock.acquire()
        try:
            print(len(JobQueue.queue))
        finally:
            JobQueue.lock.release()

        sleep(3.0)
