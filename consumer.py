__author__ = 'Darr_en1'

# _*_coding:utf-8_*_
import pika

credentials = pika.PlainCredentials('darren','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.214.140',5672,'/',credentials))
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='balance')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

#消费
channel.basic_consume(callback,
                      queue='balance',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
