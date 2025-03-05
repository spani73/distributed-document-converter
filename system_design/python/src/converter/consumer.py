import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import converter


def main():
    client = MongoClient("host.minikube.internal", 27017)
    db_uploads = client.uploads
    db_downloads = client.downloads
    # gridfs
    fs_uploads = gridfs.GridFS(db_uploads)
    fs_downloads = gridfs.GridFS(db_downloads)
    
    #rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        err = converter.start(body, fs_uploads, fs_downloads, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(
        queue=os.environ.get('UPLOAD_QUEUE'), on_message_callback=callback
    )
    
    print("waiting for messages...")
    
    channel.start_consuming()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)