import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500
    
    message = {
        "upload_fid": str(fid),
        "download_fid": None,
        "username": access["username"]
    }
    
    try:
        channel.basic_publish(exchange="", routing_key="upload", body=json.dumps(message))