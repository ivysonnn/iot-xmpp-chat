import sys

import mqtt_client_actuator as mca
import xmpp_mqtt_bridge as xmp
import bot

# Configurações XMPP
XMPP_JID = "admin@iot.imd"
XMPP_PASSWORD = "123" 
XMPP_SERVER = "iot.imd"
XMPP_PORT = 5222
RESOURCE = "PythonBridge"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'bot':
        print("--- INICIANDO CHATBOT ---")
        bot.xmpp_bot(XMPP_JID, XMPP_PASSWORD, XMPP_SERVER, XMPP_PORT)
    else:
        print("--- INICIANDO MODO PONTE XMPP-MQTT ---")
        xmp.setup_xmpp_bridge(XMPP_SERVER, XMPP_PORT, RESOURCE)