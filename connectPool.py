import pika
credentials = pika.PlainCredentials('darren','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.214.140',5672,'/',credentials))
channel = connection.channel()
