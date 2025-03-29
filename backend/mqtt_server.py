# mqtt_server.py
import paho.mqtt.client as mqtt
from db_session import get_db
from database.commands_database import get_product_by_barcode, add_shopping_cart

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "test/tecstorm"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao broker MQTT com sucesso")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ Falha na conexão. Código de retorno: {rc}")

def on_message(client, userdata, message):
    db = next(get_db())
    print(f"Receber mensagem: {message.payload.decode()}")
    #TODO

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("🔄 A iniciar loop MQTT...")
    client.loop_forever()
