from openai import OpenAI
import os
import xmpp

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "phi3:mini"

openai_client = None


# Uso da API da OpenAI
def bot_talk(prompt, client):
    # CORREÇÃO: Usar client.chat.completions.create, que é compatível com Ollama.
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            # 'instructions' no Responses API é mapeado para 'system' na Chat API
            {"role": "system", "content": "You're the user friend. Talk to him like he really is. And dont make your text too big."},
            # 'input' no Responses API é mapeado para 'user' na Chat API
            {"role": "user", "content": prompt}
        ],
        # Adicionar temperature opcional para controle de criatividade
        temperature=0.3
    )
    
    # CORREÇÃO: O retorno é extraído do objeto messages (response.choices[0].message.content)
    return response.choices[0].message.content

def message_handler(conn, msg):
    global openai_client
    try:
        body = msg.getBody()
        if not body or msg.getType() == 'error':
            return

        response_text = bot_talk(body, openai_client)
        
        reply = xmpp.Message(msg.getFrom(), response_text)
        reply.setType(msg.getType())
        conn.send(reply)
    except Exception as e:
        print(f"Erro: {e}")


def xmpp_bot(jid, psw, server, port, resource="bot"):
    # Conexão com a API do OpenAI
    global openai_client
    openai_client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",
    )

    bot_jid = xmpp.protocol.JID(jid)
    bot_client = xmpp.Client(bot_jid.getDomain(), debug=[])
    print(f"Conectando como {jid} Bot...")

    try:
        if not bot_client.connect(server=(server, port)):
            raise IOError("Não foi possível conectar ao servidor XMPP.")
            
        print(f"Conectado. Autenticando...")
        
        if not bot_client.auth(bot_jid.getNode(), psw, resource):
            raise IOError("Não foi possível autenticar (Verifique JID/Senha).")
            
        print(f"Autenticado com sucesso.")
        
        bot_client.RegisterHandler('message', message_handler)
        bot_client.sendInitPresence(requestRoster=0)
        print("[XMPP] Servidor pronto. Aguardando mensagens...")

        while bot_client.Process(1):
            pass

    except KeyboardInterrupt:
        print("\n[XMPP] Desconectando...")
    except Exception as e:
        print(f"\n[XMPP] ERRO: {e}") 