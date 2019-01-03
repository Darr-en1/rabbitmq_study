import sys

from connectPool import channel, connection

__author__ = 'Darr_en1'


#不声明队列，rabbitmq声明队列
channel.exchange_declare(exchange='Clogs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='Clogs',
                      routing_key='',
                      body=message)
print(f" [x] Sent '{message}'")
connection.close()
