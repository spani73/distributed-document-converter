import pika, sys, os, time
from send import email_mailjet

def main():
    #rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        err = email_mailjet.notification(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(
        queue=os.environ.get('DOWNLOAD_QUEUE'), on_message_callback=callback
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