from connectPool import channel

__author__ = 'Darr_en1'

# 为什么要再次声明队列——我们已经在前面的代码中声明了它?
# 如果我们确信队列已经存在，就可以避免这种情况
# 但是我们还不确定先运行哪个程序。在这种情况下，
# 练习在两个程序中重复声明队列,这是一件好事
channel.queue_declare(queue='durable', durable=True)


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback,
                      queue='durable',
                      # no_ack=True
                      )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
