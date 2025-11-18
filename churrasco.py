import streamlit as st
from urllib.parse import quote
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DO AÇOUGUE ---
# AQUI VOCÊ COLOCA O NÚMERO DO CLIENTE QUE VAI RECEBER O PEDIDO
WHATSAPP_ACOUGUE = "5511999999999" 

# Configura a página para parecer um App
st.set_page_config(page_title="Churrasco Express", page_icon="🥩")

# --- TÍTULO E CABEÇALHO ---
st.title("🥩 Churrasco Express")
st.write("Faça seu orçamento automático e envie direto para nosso WhatsApp!")
st.divider()

# --- 1. DADOS DO CLIENTE ---
st.header("1. Seus Dados")
nome = st.text_input("Seu Nome Completo:")
telefone = st.text_input("Seu WhatsApp (com DDD):")

# --- 2. LOGÍSTICA ---
st.header("2. Entrega ou Retirada?")
opcao = st.radio("Como prefere?", ["Vou buscar no Balcão", "Quero Entrega (Delivery)"])

endereco = ""
if opcao == "Quero Entrega (Delivery)":
    endereco = st.text_input("Digite o Endereço de Entrega:")

# --- 3. DADOS DA FESTA ---
st.header("3. O Churrasco")
col1, col2, col3 = st.columns(3)
with col1:
    homens = st.number_input("Homens", min_value=0, value=0)
with col2:
    mulheres = st.number_input("Mulheres", min_value=0, value=0)
with col3:
    criancas = st.number_input("Crianças", min_value=0, value=0)

# --- 4. CÁLCULO E BOTÃO ---
st.divider()

if st.button("CALCULAR E PEDIR AGORA ➤", type="primary"):
    if not nome or not telefone:
        st.error("⚠️ Ops! Preencha seu Nome e Telefone antes de continuar.")
    else:
        # MATEMÁTICA DO CHURRASCO
        carne_total = ((homens * 500) + (mulheres * 350) + (criancas * 200)) / 1000
        picanha = carne_total * 0.50
        linguica = carne_total * 0.25
        frango = carne_total * 0.25
        carvao = carne_total * 1.2
        cerveja = (homens + mulheres) * 4
        
        # CÁLCULO DE PRAZO (+1 HORA)
        agora = datetime.now()
        prazo = agora + timedelta(hours=1)
        hora_limite = prazo.strftime("%H:%M")
        
        local_entrega = endereco if endereco else "Retirada no Balcão"

        # MENSAGEM DO WHATSAPP
        mensagem = f"""🔔 *NOVO PEDIDO VIA LINK* 🔔

👤 *Cliente:* {nome}
📱 *Tel:* {telefone}
🚚 *Tipo:* {opcao}
📍 *Local:* {local_entrega}

----------------------------------
🥩 *SUGESTÃO DE PEDIDO:*
- Picanha/Alcatra: {picanha:.2f} kg
- Linguiça: {linguica:.2f} kg
- Frango: {frango:.2f} kg
- Carvão: {carvao:.1f} kg
- Cerveja (est.): {cerveja} latas
----------------------------------
TOTAL CARNE: {carne_total:.2f} kg

⏰ *URGÊNCIA:*
Cliente aguarda confirmação até: *{hora_limite}*.

Aguardo valor total e Pix!"""

        # GERAR LINK
        link_zap = f"https://wa.me/{WHATSAPP_ACOUGUE}?text={quote(mensagem)}"

        # MOSTRAR RESULTADO NA TELA
        st.success("✅ Orçamento Gerado com Sucesso!")
        st.info(f"Seu pedido foi calculado. Clique abaixo para enviar ao Açougueiro.")
        
        # BOTÃO DO ZAP
        st.link_button("📲 ENVIAR PEDIDO NO WHATSAPP", link_zap)