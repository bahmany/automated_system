import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', credentials=pika.PlainCredentials('guest', '****')))
channel = connection.channel()

channel.queue_declare(queue='args', durable=True)

channel.basic_publish(exchange='',
                      routing_key='args',
                      body='Hello World!',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      )
                      )
print(" [x] Sent 'Hello World!'")
connection.close()
