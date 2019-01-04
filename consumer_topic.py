import sys

from connectPool import channel

__author__ = 'Darr_en1'

# topic    支持通配符的路由规则,routing_key指定匹配规则
# “#”表示0个或若干个关键字，“*”表示一个关键字。如“log.*”能与“log.warn”匹配，
# 无法与“log.warn.timeout”匹配；但是“log.#”能与上述两者匹配。

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write(f"Usage:{sys.argv[0]} [binding_key]... \n")
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange="topic_logs",
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
