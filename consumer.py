from connectPool import channel

__author__ = 'Darr_en1'

# 为什么要再次声明队列——我们已经在前面的代码中声明了它?
# 如果我们确信队列已经存在，就可以避免这种情况
# 但是我们还不确定先运行哪个程序。在这种情况下，
# 练习在两个程序中重复声明队列,这是一件好事
channel.queue_declare(queue='balance')


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


# 消费
channel.basic_consume(callback,
                      queue='balance',
                      no_ack=True)  # 消息不需要向生产者确认

print(' [*] Waiting for messages. To exit press CTRL+C')
# 消费者轮询接收生产者的消息
channel.start_consuming()
