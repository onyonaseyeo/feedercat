import streamlit as st
from paho.mqtt import client as mqtt

st.title ("Pakan Kucing")
    # MQTT
def on_connect(client, userdata, flags, rc):
    client.subscribe("petfeeder/ura$^cp22/jarak")
def on_disconnect(client, userdata, flags, rc):
    st.write("Disconect")
def get_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    return client
def on_publish(client, userdata, mid):
    print("mid: " + str(mid))
def on_message(client, userdata, msg):
    st.write(msg.topic+ "::" + str(msg.payload))

broker = "mqtt-dashboard.com"
port = 1883
topic = "petfeeder/ura$^cp22/servo"
publishTopic = "petfeeder/ura$^cp22/servo"
subscribeTopic = "petfeeder/ura$^cp22/jarak"

client = get_mqtt_client()
client.on_publish = on_publish
client.connect(broker, int(port), 60)

if st.button("Beri Pakan"):
    client.publish(publishTopic, "open")



st.subheader ("Sisa Pakan")
if st.button("Stok Pakan"):
    def on_connect(client, userdata, flags, rc):
        client.subscribe("petfeeder/ura$^cp22/jarak")
    def convert_to_percentage(distance):
        # Lakukan perhitungan konversi sesuai dengan skala jarak Anda
        #min_distance = 1  # Jarak minimum
        max_distance = 11  # Jarak maksimum
        percentage = (max_distance - distance) * 10
        return round(percentage, 2)
    def on_message(client, userdata, msg):
        distance = int(msg.payload.decode("utf-8"))
        percentage = convert_to_percentage(distance)
        st.write("Stok: ", percentage, "%")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mqtt-dashboard.com", 1883, 60)

    while True:
        client.loop()


