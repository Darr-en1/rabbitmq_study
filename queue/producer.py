import sys

from pika.adapters.blocking_connection import BlockingChannel

__author__ = 'Darr_en1'

# 轮询消费模式

import pika

credentials = pika.PlainCredentials('darren', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.98.128', 5672, '/', credentials))
channel: BlockingChannel = connection.channel()

# 声明queue
channel.queue_declare(queue='balance', durable=True)

message = "".join(sys.argv[1:]) or "Hello World!"
for i in range(10):
    channel.basic_publish(exchange='',  # 使用默认ex，通过空字符串（''）来识别。
                          routing_key='balance',  # 消息通过routing_key指定的路由到队列（如果存在）。
                          properties=pika.BasicProperties(delivery_mode=2),  # 使消息持久
                          body=f"{message}_{i}")
    print(f" [x] Sent '{message}'")
connection.close()
