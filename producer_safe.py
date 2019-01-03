import sys

import pika

from connectPool import channel, connection

__author__ = 'Darr_en1'


#队列持久化

#通过设置保证rabbitmq在重启之后消息队列能被保存，并且消息队列中的消息也能被持久化


# 声明queue  设置durable=True保证消息队列的持久化，
# 注：消息队列一旦被声明为durable=True就不可更改
channel.queue_declare(queue='durable',durable=True)

message = "".join(sys.argv[1:]) or "Hello World!"

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='durable',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # 消息持久化
                      )
                      )
print(f" [x] Sent '{message}'")
connection.close()
