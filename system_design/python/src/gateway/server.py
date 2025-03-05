import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
import logging
import sys

# Configure logging to stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

server = Flask(__name__)
server.config['MONGO_URI'] = 'mongodb://host.minikube.internal:27017/uploads'

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods = ["POST"])
def login():
    token, err = access.login(request)  
    
    if not err:
        return token
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    logging.info(access)
    access = json.loads(access)
    logging.info(access)
    
    if access["admin"]:
        if len(request.files) != 1:
            return "exactly 1 file is expected", 400
        for _, f in request.files.items():
            logging.info("uploading file")
            err = util.upload(f, fs, channel, access)
            logging.info("file uploaded")
            if err:
                return err
            
        return "success!", 200
    else:
        return "unauthorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)