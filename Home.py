import streamlit as st
import paho.mqtt.client as mqtt

st.title ("Automatic Pet Feeder")
st.subheader ("Sisa Pakan")

def on_connect(client, userdata, flags, rc):
    client.subscribe("petfeeder/ura$^cp22/jarak")
def on_disconnect(client, userdata, flags, rc):
    st.success("Disconect")
def get_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    return client
def on_publish(client, userdata, mid):
    print("mid: " + str(mid))
stok = st.empty()
def on_message(client, userdata, msg):
    stok.metric("Sisa pakan", msg.payload.decode("utf-8"))

broker = "mqtt-dashboard.com"
port = 1883
subscribeTopic = "petfeeder/ura$^cp22/jarak"
client = get_mqtt_client()
client.on_publish = on_publish
client.connect(broker, int(port), 60)

while True:
    client.loop()
