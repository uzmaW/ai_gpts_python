import logging
import os
import json
import random
from re import S
from tokenize import String
import uuid
import requests
from kafka import KafkaProducer, KafkaConsumer
from google.protobuf.json_format import Parse, MessageToDict
from app.customer_order_pb2 import CustomerOrder
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer,ProtobufSerializer

from confluent_kafka.schema_registry import SchemaRegistryClient
from dotenv import load_dotenv
from app import customer_order_pb2

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
SCHEMA_REGISTRY_URL = os.environ.get('SCHEMA_REGISTRY_URL', 'http://localhost:8081')
pr = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, 
                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))  

from fastapi import FastAPI
from confluent_kafka import Consumer, Producer

app = FastAPI()

def delivery_report(entity):
    def callback(err, msg):
        """
        Reports the failure or success of a message delivery.

        Args:
            err (KafkaError): The error that occurred on None on success.
            msg (Message): The message that was produced or failed.
        """

        if err is not None:
            print("Delivery failed for {} record {}: {}".format(entity,msg.key(), err))
            return
        print('{} record {} successfully produced to {} [{}] at offset {}'.format(
            entity, msg.key(), msg.topic(), msg.partition(), msg.offset()))
    return callback

def register_schema(schema_registry_url, schema_str):
    url = f"{schema_registry_url}/subjects/customer-orders-value/versions"
    headers = {"Content-Type": "application/vnd.schemaregistry.v1+json"}
    data = json.dumps({"schema": schema_str})
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_protobuf_serializer(schema_registry_client, schema_str):
    return ProtobufSerializer(CustomerOrder, schema_registry_client, {'use.deprecated.format': False})

def produce_order(producer, serializer, order_data):
    order = CustomerOrder()
    Parse(json.dumps(order_data), order)
    serialized_data = serializer(order, SerializationContext('customer-orders', MessageField.VALUE))
    producer.produce('customer-orders', value=serialized_data)
    producer.flush()
    print(f"Produced order: {order_data}")

def consume_orders(consumer):
    for message in consumer:
        order = CustomerOrder()
        order.ParseFromString(message.value)
        print(f"Consumed order: {MessageToDict(order)}")
@app.get("/")
def main():    
    # # Register schema
    # with open('app/customer_order.proto', 'r') as f:
    #     schema_str = f.read()
    # print(f"Schema: {schema_str}") 
    topic = 'customer-orders'  
    # schema_id = register_schema(SCHEMA_REGISTRY_URL, schema_str)
    # print(f"Registered schema with id: {schema_id}")

    # Set up schema registry client and serializer
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    string_serializer = StringSerializer('utf8')

    protobuf_serializer = ProtobufSerializer(customer_order_pb2.CustomerOrder, 
                                             schema_registry_client, 
                                             {'use.deprecated.format': False})

    producer_conf = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}

    producer = Producer(producer_conf)

    print("Producing  records to topic {}. ^C to exit.".format(topic))
    try:
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        
        # Produce a sample order
        order_id = str(uuid.uuid4())
        customer_id = f"C{random.randint(1, 1000):03d}"
        items = [
            {"product_id": f"P{random.randint(1, 100):02d}", "quantity": random.randint(1, 5), "price": round(random.uniform(5.0, 100.0), 2)}
            for _ in range(random.randint(1, 5))
        ]
        total_amount = sum(item["price"] * item["quantity"] for item in items)
        sample_order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "items": items,
            "total_amount": round(total_amount, 2)
        }
        co = customer_order_pb2.CustomerOrder(
            order_id=order_id,
            customer_id=customer_id,
            items=[customer_order_pb2.OrderItem(product_id=item["product_id"], quantity=item["quantity"], price=item["price"]) for item in items],
            total_amount=total_amount
        )
        print(f"Producing order: {sample_order}")
        
        producer.produce(topic=topic, 
                            partition=0,
                            #offset=-1,
                            key=string_serializer(#'order_'+str(uuid.uuid4())
                                order_id
                                ),
                            value=protobuf_serializer(co, SerializationContext(topic, MessageField.VALUE)),
                            on_delivery=delivery_report(entity=co)
                            )
    except ValueError:
        print("Invalid data, discarding record...")
    except Exception as e:
        print(f"Exception while producing record value - {sample_order} to topic {topic}: {e}")           
    print("\nFlushing records...")
    producer.flush()
    
    print("Records flushed.")
    
    # Set up Consumer and Deserializer
    protobuf_deserializer = ProtobufDeserializer(customer_order_pb2.CustomerOrder,
                                                 {'use.deprecated.format': False})
    
    consumer_conf = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 
                         'group.id': 'mart-group', 
                         'auto.offset.reset': 'earliest' }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            md = protobuf_deserializer(msg.value(),SerializationContext(topic, MessageField.VALUE))

            if md is not None:
                print("model record {}:\n"
                      "\tdata: {}\n"
                      .format(msg.key(), md))
        except KeyboardInterrupt:
            break

    consumer.close()
                      

# if __name__ == "__main__":
#     main()