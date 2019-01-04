import sys

from connectPool import channel, connection

__author__ = 'Darr_en1'

import pika

# 轮询消费模式


# 声明queue
channel.queue_declare(queue='balance')

message = "".join(sys.argv[1:]) or "Hello World!"

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',  # 使用默认ex，通过空字符串（“”）来识别。
                      routing_key='balance',  # 消息通过routing_key指定的路由到队列（如果存在）。
                      body=message)
print(f" [x] Sent '{message}'")
connection.close()
