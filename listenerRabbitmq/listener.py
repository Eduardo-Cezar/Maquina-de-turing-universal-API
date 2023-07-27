import pika as pk

exchange_name = 'mtu'
queue_name = "fila_mtu"
mtu_routing_key = 'chave_mtu'

ip_container = 'localhost'

conn = pk.BlockingConnection(pk.ConnectionParameters(host=ip_container))
channel = conn.channel()
print("Conectou ao rabbitmq")

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
print("Criou a exchange")

channel.queue_declare(queue=queue_name, exclusive=True)
print("Criou a fila '" + queue_name +"'")

channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=mtu_routing_key)

#Consumir a fila
def callback(ch, method, properties, body):
    print(body)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()