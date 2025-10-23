import xmpp
import paho.mqtt.client as mqtt
import time
import sys
import ssl
import getpass

# Configurações MQTT
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/comando/checkbox"

mqtt_client = None

def message_handler(conn, msg):
    global mqtt_client_bridge
    
    try:
        body = msg.getBody()
        sender = msg.getFrom()
        
        if not body or msg.getType() == 'error':
            return
            
        print(f"\n[XMPP] Mensagem recebida de: {sender.getStripped()}")
        print(f"[XMPP] Conteúdo: {body}")
        
        body_lower = body.lower() 

        reply_text = f"Comando '{body_lower}' recebido e encaminhado para o MQTT."
        reply = xmpp.protocol.Message(to=sender, body=reply_text)
        conn.send(reply)
        print(f"[XMPP] Resposta enviada para: {sender.getStripped()}")

        if mqtt_client_bridge and mqtt_client_bridge.is_connected():
            mqtt_client_bridge.publish(MQTT_TOPIC, payload=body_lower)
            print(f"[MQTT] Publicado no tópico PÚBLICO '{MQTT_TOPIC}': {body_lower}")
        else:
            print("[MQTT] ERRO: Cliente MQTT não está conectado.")
            
    except Exception as e:
        print(f"[XMPP] ERRO no message_handler: {e}")

def setup_xmpp_bridge(server, port, resource):
    global mqtt_client_bridge
    # CONECTAR AO MQTT
    try:
        print("[MQTT] Conectando ao broker PÚBLICO (test.mosquitto.org)...")
        mqtt_client_bridge = mqtt.Client(client_id="xmpp_ponte_01_teste")

        mqtt_client_bridge.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client_bridge.loop_start() 
        print("[MQTT] Conectado e loop iniciado.")
    except Exception as e:
        print(f"[MQTT] ERRO: Falha ao conectar ao broker: {e}")
        return

    print("\n--- Autenticação XMPP ---")
    username = input("Digite o usuário XMPP (ex: ramon): ")
    try:
        password = getpass.getpass("Digite a senha XMPP: ")
    except Exception as e:
        print(f"Erro ao ler a senha: {e}")
        return

    # CONECTAR AO XMPP
    jid_string = f"{username}@{server}"
    jid = xmpp.protocol.JID(jid_string)
    client = xmpp.Client(jid.getDomain(), debug=[]) 

    print(f"[XMPP] Conectando como {jid}...")
    
    try:
        if not client.connect(server=(server, port)):
            raise IOError("Não foi possível conectar ao servidor XMPP.")
            
        print(f"[XMPP] Conectado. Autenticando...")
        
        if not client.auth(jid.getNode(), password, resource):
            raise IOError("Não foi possível autenticar (Verifique JID/Senha).")
            
        print(f"[XMPP] Autenticado com sucesso.")
        
        client.RegisterHandler('message', message_handler)
        client.sendInitPresence(requestRoster=0)
        print("[XMPP] Servidor pronto. Aguardando mensagens...")

        while client.Process(1):
            pass

    except KeyboardInterrupt:
        print("\n[XMPP] Desconectando...")
    except Exception as e:
        print(f"\n[XMPP] ERRO: {e}") 
    finally:
        if mqtt_client_bridge:
            mqtt_client_bridge.loop_stop()
            mqtt_client_bridge.disconnect()
        print("Script finalizado.")