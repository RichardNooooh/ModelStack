# import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import json

import uuid

from jobs import JobQueue, JobEncoder, Job
from time import sleep

from threading import Thread

from training import begin_training

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
        q = [json.dumps(job, cls=JobEncoder) for job in JobQueue.queue]
        JobQueue.lock.release()

        self.wfile.write(json.dumps({"queue": q}).encode('utf-8'))

    def do_POST(self):
        print("> Entered POST")
        length = int(self.headers.get('content-length'))
        body_data = self.rfile.read(length).decode('utf-8')
        message = json.loads(body_data)
        
        # add a property to the object, just to mess with data
        new_job = Job(message["job_id"],
                        message["model_path"],
                        message["parameters"]["learning_rate"],
                        message["parameters"]["num_epochs"])
        JobQueue.lock.acquire()
        JobQueue.queue.append(new_job)
        JobQueue.lock.release()

        print(f"New job!: {new_job.id}")

        # send the message back
        self._set_headers()
        message['received'] = 'ok'
        return_message = json.dumps(message).encode('utf-8')
        # print(return_message)
        self.wfile.write(return_message)
    

def run_http_server():
    server = HTTPServer((HOST, PORT), JobControlHandler)
    server.serve_forever()

if __name__ == "__main__":
    Thread(target=run_http_server, daemon=True).start()

    # we run the job q system indefinitely..
    while True:
        current_job = None

        JobQueue.lock.acquire()
        if len(JobQueue.queue) > 0 and not current_job:
            current_job = JobQueue.queue.popleft()
        else:
            print("No job yet.")
        JobQueue.lock.release()

        if current_job:
            begin_training(current_job)
            current_job = None

        sleep(3.0)
        
