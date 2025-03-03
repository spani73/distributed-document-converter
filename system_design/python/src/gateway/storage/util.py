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
        channel.basic_publish(exchange="", routing_key="upload", body=json.dumps(message),
            properties= pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)) # We need to make sure the message is not lost if kubernetes pod is restarted.
    except Exception as err:
        fs.delete(fid)
        return "internal server error", 500
