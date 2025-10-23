import paho.mqtt.client as mqtt
import time

# Configurações MQTT
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/comando/checkbox"

def setup_mqtt_actuator():
    # O estado do checkbox precisa ser mutável dentro do callback on_message
    class Checkbox:
        isOn = False

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[Atuador] Conectado ao Broker: {MQTT_BROKER}")
            client.subscribe(MQTT_TOPIC)
            print(f"[Atuador] Inscrito no tópico: {MQTT_TOPIC}")
        else:
            print(f"[Atuador] Falha ao conectar, código: {rc}")

    def on_message(client, userdata, msg):
        # Acessa o estado mutável do checkbox
        nonlocal Checkbox
        
        payload = msg.payload.decode('utf-8').lower()
        print(f"\n[Atuador] Ação recebida: '{payload}'")

        if payload == "ligar" or payload == "on":
            Checkbox.isOn = True
            print("[Atuador] Status: [X] Checkbox Ativado!")
        elif payload == "desligar" or payload == "off":
            Checkbox.isOn = False
            print("[Atuador] Status: [ ] Checkbox Desativado.")
        else:
            print(f"[Atuador] Status: Comando '{payload}' não reconhecido.")

    client = mqtt.Client(client_id="atuador_checkbox_01")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("[Atuador] Iniciando... (Pressione Ctrl+C para sair)")
        client.loop_forever()
    except Exception as e:
        print(f"[Atuador] ERRO: Não foi possível conectar ao broker: {e}")
    except KeyboardInterrupt:
        print("\n[Atuador] Desconectando...")
        client.disconnect()

if __name__ == "__main__":
    setup_mqtt_actuator()