from connectPool import channel

__author__ = 'Darr_en1'
#发布/订阅模式


# RabbitMQ中消息传递模型的核心思想是生产者永远不会将任何消息直接发送到队列。
# 实际上，生产者通常甚至不知道消息是否会被传递到任何队列。
#
# 相反，生产者只能向exchange发送消息。exchange需要做的事。一方面，它接收来自
# 生产者的消息，另一方面将它们推送到队列。exchang必须确切知道如何处理收到的消息。
# 它应该附加到特定队列吗？它应该附加到许多队列吗？或者它应该被丢弃。其规则由交换类型定义。
#
# 类型：
#   direct   C绑定的队列名称须和P发布指定的路由名称一致
#   topic    支持通配符的路由规则
#   fanout   将信息分发到exchange上绑定的所有队列上
#   header   消息发送时可以在header中定义一些键值对，
#            接收消息队列与headers转发器绑定时可以指定键值对(all、any)



channel.exchange_declare(exchange='Clogs',
                         exchange_type='fanout')
# 不指定queue名字,rabbit会随机分配一个名字,
# exclusive=True会在使用此queue的消费者断开后,自动将queue删除
result = channel.queue_declare(exclusive=True)

#获取到当前生成的队列名称
queue_name = result.method.queue

channel.queue_bind(exchange='Clogs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
