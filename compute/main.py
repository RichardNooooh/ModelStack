# import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process

from .jobs import JobQueue
from time import sleep

HOST, PORT = "localhost", 42069

class JobControlHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def do_POST(self):
        pass
    

def run_http_server():
    with HTTPServer((HOST, PORT), JobControlHandler) as server:
        server.serve_forever(poll_interval=1.0)


if __name__ == "__main__":
    p = Process(target=run_http_server, daemon=True)
    p.start()

    # we run the job q system indefinitely..
    while True:
        JobQueue.lock.acquire()
        try:
            print(len(JobQueue.queue))
        finally:
            JobQueue.lock.release()

        sleep(5.0)
