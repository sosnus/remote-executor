import paho.mqtt.client as mqtt
import sqlitehelper as sqlitehelper
import os
import time

##### VARIABLES START ######
# Define the MQTT broker and port
broker = os.getenv("V_BROKER")
topic_str = os.getenv("V_TOPICS")
# topic_str = "controller,datacollector,mobile,var,varfast,logs,status" # example
db_path = "/tmp/mqttlogger/mqtt-logs/"
version = "v1.0.17___2024-06-29"
# if broker == None:
    # broker = "192.168.88.203"
if topic_str == None:
    print(">>> [ERR] NO topic_str PARAM!")
    topic_str = "controller,datacollector,mobile,var,varfast,status" # example
    # topic_str = "controller,datacollector,mobile,var,varfast,logs,status" # example
    time.sleep(1)
if broker == None:
    print(">>> [ERR] NO broker PARAM!")
    broker = "192.168.88.203" # example
    time.sleep(1)
##### VARIABLES END  ######

print(f">>> build version & time: {version}")
print(">>> === RUN MQTTLOGGER (app.py) ===")
print(">>> app.py params: broker, db_path")
print(broker)
print(db_path)
sqlitehelper.check_path(db_path)
with open(db_path+"init_log.txt", "w") as file:
    file.write(version)
topic_list = topic_str.split(',')
topics = list((str(item)+"/#", 0) for item in topic_list)

print(f">>> subscribe topics raw: {topic_str}")
print(f">>> subscribe topics list: {topics}")

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    message_payload = message.payload.decode('utf-8',errors='replace')
    sqlitehelper.insert_message(message_payload, message.topic)
    client.publish("mqttlogger/mqttlogger", f"msg from {message.topic} len={len(message_payload)} logged")
    print(f">>> msg from {message.topic} len={len(message_payload)} logged {datetime.now()}")
# Define the callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(">>> Connected successfully")
        client.publish("mqttlogger/mqttlogger", "Connected successfully")
        sqlitehelper.insert_message("Connected successfully", "mqttlogger/ok")
        sqlitehelper.insert_message(str(topics), "mqttlogger/subscribed_topics")
        # Subscribe to the topic
        client.subscribe(topics)
    else:
        print(f">>> Connect failed with code {rc}")
        sqlitehelper.insert_message("Connect failed with code {rc}", "mqttlogger/error")

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,protocol=mqtt.MQTTv5)

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

sqlitehelper.init_db(db_path)
message = "Init logger!"
topic = "mqttlogger/ok"
sqlitehelper.insert_message(message, topic)

# Connect to the MQTT broker
client.connect(broker, 1883, 60)

# Start the MQTT client loop to process network traffic and dispatch callbacks
client.loop_forever()