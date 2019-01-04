import pika

__author__ = 'Darr_en1'


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch,method,props,body):
    '''
    rollback函数，接收client数据处理后将结果发布返回给client
    '''
    n = int(body)
    print(f" [.] fib({n})")
    response = fib(n)
    print(" [.] finish  \n")

    ch.basic_publish(
        exchange='',  # 把执行结果发回给客户端
        routing_key=props.reply_to,  # 客户端要求返回想用的queue
        # 返回客户端发过来的correction_id 为了让客户端验证消息一致性
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 任务完成，告诉客户端



if __name__ == '__main__':
    credentials = pika.PlainCredentials('darren', '123456')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        '192.168.214.140', 5672, '/', credentials))
    channel = connection.channel()
    # 声明一个rpc_queue,client并未声明直接调用，因此server得先启动
    channel.queue_declare(queue='rpc_queue')



    #每次server只处理一个消息，再处理过程中不去rabbitmq中获取消息
    channel.basic_qos(prefetch_count=1)
    # 在rpc_queue里收消息,收到消息就调用on_request
    channel.basic_consume(on_request, queue='rpc_queue')
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
