# mqtt_server.py
import paho.mqtt.client as mqtt
from db_session import get_db
from database.commands_database import get_product_by_barcode, add_shopping_cart, remove_shopping_cart, get_shopping_cart_item_by_uid, get_shopping_cart_items
from ai_services import add_product_use_ai
import json
import threading
from fastapi import HTTPException
from websocket_manager import notify_client
import asyncio


MQTT_BROKER = "127.0.0.1"  # O broker corre localmente no teu PC
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
    try:
        raw = message.payload.decode()         # <- transforma bytes em string
        print(f"📩 Mensagem recebida: {raw}")

        msg = json.loads(raw)                  # <- transforma string JSON em dicionário

        uid = msg["uid"]
        barcode = msg["barcode"]

        product = get_product_by_barcode(db, barcode)
        try:
            check = get_shopping_cart_item_by_uid(db, uid)
        except HTTPException:
            check = None

        if check:
            remove_shopping_cart(db, 1, product.id, check[0].uid)  # TODO: usar client real
            print(f"🛒 Produto '{product.name}' removido (uid={uid})")
            asyncio.run(notify_client("1", "ADD"))
        else:
            threading.Thread(target=add_product_use_ai, args=(product, uid)).start()
            print(f"🛒 Produto '{product.name}' adicionado (uid={uid})")
        
        notify_client("1", "ADD")

    except Exception as e:
        print(f"❌ Erro ao processar mensagem MQTT: {e}")
    finally:
        db.close()

        
def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("🔄 A iniciar loop MQTT...")
    client.loop_forever()
