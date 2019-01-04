import sys
import uuid

import pika

__author__ = 'Darr_en1'

#rabbitmq 实现 rpc


class FibonacciRpcClient(object):
    def __init__(self,username,password,host):
        credentials = pika.PlainCredentials(username,password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,credentials = credentials
        ))
        self.channel = self.connection.channel()

        #支持消息持久化
        result = self.channel.queue_declare(exclusive=True)

        self.callback_queue = result.method.queue

        # 准备接收server结果
        self.channel.basic_consume(
            self.on_response,#收到server消息就调用on_response
            no_ack = True,
            queue = self.callback_queue
        )

    def on_response(self,ch,method,props,body):
        '''
        callback函数，server返回的id和client生成的id做校验
        '''
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self,n):
        self.response = None

        self.corr_id = str(uuid.uuid4())

        #发送
        self.channel.basic_publish(
            exchange='',
            routing_key = 'rpc_queue',
            properties = pika.BasicProperties( # 消息持久化
                reply_to=self.callback_queue,  # 让服务端命令结果返回到callback_queue
                correlation_id=self.corr_id

            ),
            body=str(n)
        )
        while self.response is None:  # 当没有数据，就一直循环
            # 非阻塞版的start_consuming(),会检查队列里面有没有新的信息
            self.connection.process_data_events()

        return int(self.response)


if __name__ == '__main__':
    fibonacci_rpc_client = FibonacciRpcClient('darren','123456','192.168.214.140')

    message = "".join(sys.argv[1:]) or 10

    print(f"-------->fib({message})")
    response = fibonacci_rpc_client.call(message)
    print(f"-------->{response}")
