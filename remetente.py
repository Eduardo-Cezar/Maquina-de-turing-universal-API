import pika as pk

exchange_name = 'mtu'
queue_name = "fila_mtu"
mtu_routing_key = 'chave_mtu'

ip_container = 'localhost'
conn = pk.BlockingConnection(pk.ConnectionParameters(host=ip_container))
channel = conn.channel()
print("Conectou ao rabbitmq")

my_tag= mtu_routing_key #routing_key
message= 'exemplo kj RabbitMQ'
'''
channel.basic_publish(exchange=exchange_name, routing_key=my_tag, body=message)
conn.close()
'''

def enviaMSG(msg):
    channel.basic_publish(exchange=exchange_name, routing_key=my_tag, body=msg)



