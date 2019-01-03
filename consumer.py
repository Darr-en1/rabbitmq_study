from connectPool import channel

__author__ = 'Darr_en1'


# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='balance')


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

#消费
channel.basic_consume(callback,
                      queue='balance',
                      no_ack=True)#消息不需要向生产者确认

print(' [*] Waiting for messages. To exit press CTRL+C')
#消费者轮询接收生产者的消息
channel.start_consuming()
