import streamlit as st
import mysql.connector
from secrets import choice
import pandas as pd
import paho.mqtt.client as mqtt

cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='datakucing')

cursor = cnx.cursor()

 # MQTT
broker = "mqtt-dashboard.com"
port = 1883
topic = "petfeeder/ura$^cp22/beratt"
publishTopic = "petfeeder/ura$^cp22/servo/"
subscribeTopic = "petfeeder/ura$^cp22/jarak"

menu = ["Home", "Data", "Daftar", "Manual"]
choice = st.sidebar.selectbox("Menu", menu)

image = Image.open('doraemon.jpg')
st.image(image, caption='Automatic Cat Feeder')

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

client = get_mqtt_client()
client.on_publish = on_publish
client.connect(broker, int(port), 60)

if choice == "Data":
    st.header("Data Kucing")
    # Query untuk membaca data dari tabel
    query = "SELECT id, nama, umur, berat FROM data"

    # Baca data dari tabel ke dataframe
    df = pd.read_sql(query, cnx)

    # Memformat data sebelum menampilkan
    df['berat'] = df['berat'].apply(lambda x: '{:.1f}'.format(x))
    st.dataframe(df)

elif choice == "Daftar":    
    with st.form(key="my_form"):
        nama = st.text_input('Nama')
        berat = st.number_input('Berat (gram)', max_value=5000, min_value=500)
        umur = st.number_input('Umur (bulan)', max_value=50, min_value=0)
        daftar = st.form_submit_button (label="Daftar")
        if daftar:
            data = {"namakucing": nama, "berat": berat, "umur": umur}
            if nama and umur:
                insert_query = "INSERT INTO datakucing (nama, berat, umur) VALUES (%s, %s, %s)"
                insert_data = (nama, berat, umur)
                cursor.execute(insert_query, insert_data)
                cnx.commit()
                st.success(f"{nama} dengan Berat {berat} dan Umur {umur} Bulan Telah Terdaftar")
            else :
                st.error('Silahkan Isi Data')

elif choice == "Manual":
    if st.button("Beri Pakan"):
        client.publish(publishTopic, "open")

