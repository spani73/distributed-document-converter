import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
import logging
import sys
from bson.objectid import ObjectId

# Configure logging to stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

server = Flask(__name__)

mongo_uploads = PyMongo(
    server,
    uri='mongodb://host.minikube.internal:27017/uploads'
)

mongo_download = PyMongo(
    server,
    uri='mongodb://host.minikube.internal:27017/downloads'
)

fs_uploads = gridfs.GridFS(mongo_uploads.db)
fs_downloads = gridfs.GridFS(mongo_download.db)

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
    
    if err:
        return err
    
    logging.info(access)
    access = json.loads(access)
    logging.info(access)
    
    if access["admin"]:
        if len(request.files) != 1:
            return "exactly 1 file is expected", 400
        for _, f in request.files.items():
            logging.info("uploading file")
            err = util.upload(f, fs_uploads, channel, access)
            logging.info("file uploaded")
            if err:
                return err
            
        return "success!", 200
    else:
        return "unauthorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)
    
    if err:
        return err
    
    access = json.loads(access)
    
    if access["admin"]:
        fid_string = request.args.get("fid")
        
        if not fid_string:
            return "valid fid is required", 400
        
        try:
            out = fs_downloads.get(ObjectId(fid_string))
            return send_file(out, download_name=f'{fid_string}.pdf')
        except Exception as err:
            logging.error(err)
            return "internal server error", 500
    
    return "unauthorized", 401

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)