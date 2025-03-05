import pika, json
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        logging.info("mongodb" , err)
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
        logging.info("queueu" , err)
        fs.delete(fid)
        return "internal server error", 500
