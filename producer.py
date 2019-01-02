__author__ = 'Darr_en1'

# !/usr/bin/env python
import pika
credentials = pika.PlainCredentials('darren','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.214.140',5672,'/',credentials))
channel = connection.channel()

# 声明queue
channel.queue_declare(queue='balance')

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='balance',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
