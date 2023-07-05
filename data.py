import streamlit as st
import mysql.connector
import pandas as pd
import paho.mqtt.client as mqtt

# Buat koneksi ke database
cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='datakucing')

cursor = cnx.cursor()

 # MQTT
broker = "mqtt-dashboard.com"
port = 1883
topic = "petfeeder/ura$^cp22/beratt"
publishTopic = "petfeeder/ura$^cp22/servo/"
subscribeTopic = "petfeeder/ura$^cp22/berat"

def on_connect(client, userdata, flags, rc):
    client.subscribe("petfeeder/ura$^cp22/berat")
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
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
def publish_mqtt(berat):
    client = mqtt.Client()
    client.connect = (broker, port)
    client.on_publish = (topic, berat)

client = get_mqtt_client()
client.on_publish = on_publish
client.connect(broker, int(port), 60)

st.header("Data Kucing")
# Query untuk membaca data dari tabel
query = "SELECT id, nama, umur, berat FROM datakucing"

# Baca data dari tabel ke dataframe
df = pd.read_sql(query, cnx)

# Memformat data sebelum menampilkan
df['berat'] = df['berat'].apply(lambda x: '{:.1f}'.format(x))
st.dataframe(df)
 
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

# Membuat form input untuk mengisi data yang akan dihapus
delete_id = st.number_input("Masukkan ID data yang akan dihapus:", max_value=100, min_value=0)

# hapus data dari tabel
hapus = st.button("Hapus Data")
    # Perintah SQL untuk menghapus data dari tabel
if hapus:
    if delete_id:
        delete_query = "DELETE FROM datakucing WHERE id = %s"
        data = (delete_id,)
        cursor.execute(delete_query, data)
        cnx.commit()
        st.success("Data berhasil dihapus!")
    else:
        st.error("Masukkan ID data yang akan dihapus dan tekan tombol 'Hapus Data'.")

cnx.close()

if st.button("Beri Pakan"):
   client.publish(publishTopic, "open")
   st.success(f"{nama} dengan Berat {berat} Gram Telah Makan")