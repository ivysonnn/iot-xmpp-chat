# Atividade Avaliativa - Unidade II: Sistema de Bate-Papo com XMPP

## Disciplina
Tecnologias de Comunicação para loT/IMD0907

**Professor:** Dr. Ramon Fontes

**Instituição:** UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE (UERN IME)

---

## Contexto

Há uma ampla variedade de plataformas de comunicação por chat no mercado, que transmitem milhões de mensagens diariamente por servidores ao redor do mundo, como WhatsApp e Telegram. O número de aplicativos de mensagens 1 para 1 está crescendo rapidamente devido ao aumento significativo do valor de mercado desses aplicativos.

Entre as várias tecnologias subjacentes a esses sistemas, o XMPP (Extensible Messaging and Presence Protocol) se destaca como um protocolo de comunicação aberto e padronizado, utilizado para mensagens instantâneas e presença em tempo real. O XMPP é conhecido por sua capacidade de interoperabilidade entre diferentes sistemas e plataformas, permitindo a comunicação entre usuários em redes distintas. Sua natureza extensível permite que novas funcionalidades sejam adicionadas através de extensões conhecidas como XEPS (XMPP Extension Protocols), adaptando-se às necessidades específicas dos desenvolvedores.

Uma implementação notável do protocolo XMPP é o Ejabberd. Este servidor de mensagens instantâneas e presença em tempo real, desenvolvido em Erlang, oferece uma infraestrutura robusta e escalável para a criação de aplicativos de bate-papo 1 para 1 e outras soluções de comunicação em tempo real. Ejabberd é compatível com diversos sistemas operacionais, incluindo Linux, Windows e macOS, e suporta várias técnicas de segurança, como criptografia TLS e autenticação SASL, garantindo a segurança das comunicações. Ele também se destaca pela sua capacidade de escalar para atender a um grande número de usuários simultâneos e oferece uma ampla gama de módulos para customização e extensibilidade.

## Objetivo da Atividade

Desenvolver e demonstrar um sistema de bate-papo funcional baseado em XMPP, integrando cliente, servidor e autenticação segura.

## Instruções

1.  **Cliente XMPP:** Use o **Pidgin** (`https://pidgin.im/`) ou semelhante como cliente gráfico.
2.  **Script Python:**
    * Desenvolva um cliente em Python, utilizando o módulo **xmpppy** (`https://github.com/xmpppy/xmpppy`) para interação com o servidor.
    * O cliente em Python pode, por exemplo, responder a alguma mensagem enviada através do Pidgin.
    * A mensagem enviada pelo cliente Python deve ser publicada em um **Broker MQTT**.
    * Este broker, por sua vez, deve executar uma ação em um cliente MQTT, como ativar ou desativar um checkbox.
