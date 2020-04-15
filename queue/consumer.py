import time

from pika.adapters.blocking_connection import BlockingChannel

__author__ = 'Darr_en1'

import pika

credentials = pika.PlainCredentials('darren', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.98.128', 5672, '/', credentials))
channel: BlockingChannel = connection.channel()

# 为什么要再次声明队列——我们已经在前面的代码中声明了它?
# 如果我们确信队列已经存在，就可以避免这种情况
# 但是我们还不确定先运行哪个程序。在这种情况下，
# 在两个程序中重复声明队列,这是一件好事
channel.queue_declare(queue='balance', durable=True)


def callback(ch: BlockingChannel, method, properties, body):
    time.sleep(2)
    print(f" [x] Received {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 通过消息确认保证消息不丢失


# prefetch_count=1 表明consumer在运行过程中不接受新的msg推送，如果处理能力过慢可能会导致msg 在queue堆积过多
channel.basic_qos(prefetch_count=1)

# 消费
channel.basic_consume(
    queue='balance',
    on_message_callback=callback,
    auto_ack=False)  # auto_ack :消息是否自动向生产者确认，手动发送消息确认auto_ack为False

print(' [*] Waiting for messages. To exit press CTRL+C')
# 消费者轮询接收生产者的消息
channel.start_consuming()
