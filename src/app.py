import paho.mqtt.client as mqtt
import os
import time
import datetime

def get_dt_iso():
    now = datetime.datetime.now()
    truncated_iso = now.isoformat(timespec='milliseconds')
    return truncated_iso

def header():
    return "["+get_dt_iso()+"]>>>"
print(get_dt_iso())
print(header())

##### VARIABLES START ######
# Define the MQTT broker and port
print("### remote-executor ###")
broker = os.getenv("V_BROKER")
topic_str = os.getenv("V_TOPICS")
version = "v1.0.17___2024-06-29"
if topic_str == None:
    print(header()+" [ERR] NO topic_str PARAM!")
    topic_str = "controller,datacollector,mobile,var,varfast,status" # example
    # topic_str = "controller,datacollector,mobile,var,varfast,logs,status" # example
    time.sleep(1)
if broker == None:
    print(header()+" [ERR] NO broker PARAM!")
    broker = "192.168.1.160" # example
    time.sleep(1)
##### VARIABLES END  ######

print(header()+f" build version & time: {version}")
print(header()+" === RUN remote-executor (app.py) ===")
print(header()+" app.py params: broker")
print(broker)
print(header()+f" subscribe topics raw: {topic_str}")

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    message_payload = message.payload.decode('utf-8',errors='replace')
    client.publish("remote-executor/mqttlogger", f"msg from {message.topic} len={len(message_payload)} logged")
    print(header()+f" msg from {message.topic} len={len(message_payload)} logged {get_dt_iso()}")
# Define the callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(header()+" Connected successfully")
        client.publish("remote-executor/mqttlogger", "Connected successfully")
        # Subscribe to the topic
        client.subscribe(topic_str)
    else:
        print(header()+f" Connect failed with code {rc}")

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,protocol=mqtt.MQTTv5)

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, 1883, 60)

# Start the MQTT client loop to process network traffic and dispatch callbacks
client.loop_forever()