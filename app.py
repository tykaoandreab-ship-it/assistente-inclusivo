import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Assistente Inclusivo", page_icon="🧩")

# ==========================================
# 1. SISTEMA DE CONTROLE DE ACESSO E SENHAS
# ==========================================
SENHAS_VALIDAS = {
    "demo2026": "Acesso Demonstração",
    "piratininga2026": "Prefeitura de Piratininga",
    "escola123": "Escola Municipal"
}

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

def verificar_senha():
    senha_digitada = st.session_state.get("campo_senha", "")
    if senha_digitada in SENHAS_VALIDAS:
        st.session_state["autenticado"] = True
        st.session_state["cliente_nome"] = SENHAS_VALIDAS[senha_digitada]
    else:
        st.error("🔒 Senha incorreta ou acesso não autorizado.")

if not st.session_state["autenticado"]:
    st.title("🔒 Acesso Restrito - Assistente Inclusivo")
    st.caption("Plataforma licenciada para redes de ensino e instituições autorizadas.")
    st.info("Insira a sua senha de acesso corporativa para entrar no sistema.")
    
    st.text_input(
        "Senha de Acesso:", 
        type="password", 
        key="campo_senha", 
        on_change=verificar_senha
    )
    st.button("Entrar no Sistema", on_click=verificar_senha)
    st.stop()

# ==========================================
# 2. APLICAÇÃO PRINCIPAL (APÓS LOGIN)
# ==========================================

col1, col2 = st.columns([3, 1])
with col1:
    st.title("🧩 Assistente de Apoio Inclusivo (TEA & TDAH)")
with col2:
    st.caption(f"🔑 **Licenciado para:**\n{st.session_state.get('cliente_nome')}")
    if st.button("Sair / Bloquear"):
        st.session_state["autenticado"] = False
        st.rerun()

st.caption("Ferramenta de suporte pedagógico e organizacional.")
st.info("💡 **Nota:** Esta ferramenta oferece suporte pedagógico e organizacional. Não substitui diagnósticos ou tratamentos médicos.")

st.sidebar.header("Configuração do Sistema")

CHAVE_PADRAO = "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"

api_key_groq = st.sidebar.text_input(
    "API Key do Groq:", 
    type="password", 
    value=CHAVE_PADRAO
)

if not api_key_groq:
    st.warning("👈 Insira a chave da API na barra lateral para começar.")
    st.stop()

client = Groq(api_key=api_key_groq)

def gerar_resposta(prompt):
    # Busca dinamicamente os modelos disponíveis na conta
    lista_modelos = client.models.list()
    
    # Filtra modelos de texto da família Llama, ignorando Whisper/Áudio/Visão
    modelo_escolhido = None
    for m in lista_modelos.data:
        m_id = m.id.lower()
        if ("llama" in m_id) and ("whisper" not in m_id) and ("vision" not in m_id):
            modelo_escolhido = m.id
            break
            
    # Se não encontrar Llama, seleciona o primeiro modelo de texto disponível
    if not modelo_escolhido and len(lista_modelos.data) > 0:
        for m in lista_modelos.data:
            if "whisper" not in m.id.lower():
                modelo_escolhido = m.id
                break

    if not modelo_escolhido:
        raise Exception("Nenhum modelo de texto disponível foi encontrado na conta Groq.")

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=modelo_escolhido,
    )
    return chat_completion.choices[0].message.content

opcao = st.selectbox(
    "Selecione o tipo de ajuda:",
    [
        "1. Gerar História Social / Rotina (TEA)",
        "2. Adaptar Tarefa Escolar (TDAH)",
        "3. Orientação para Manejo de Crise"
    ]
)

if opcao == "1. Gerar História Social / Rotina (TEA)":
    st.subheader("📖 Criador de História Social")
    idade = st.number_input("Idade da criança:", min_value=2, max_value=18, value=6)
    situacao = st.text_input("Qual situação vai acontecer?", placeholder="Ex: Ir ao dentista fazer limpeza")
    
    if st.button("Gerar História Social"):
        if situacao:
            with st.spinner("Criando a história..."):
                try:
                    prompt = f"Responda obrigatoriamente em português do Brasil. Crie uma História Social simples para uma criança de {idade} anos sobre a seguinte situação: {situacao}. Use linguagem clara, frases curtas e tom acolhedor."
                    texto = gerar_resposta(prompt)
                    st.success("História Pronta!")
                    st.write(texto)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.warning("Por favor, informe a situação.")

elif opcao == "2. Adaptar Tarefa Escolar (TDAH)":
    st.subheader("📝 Adaptador de Tarefas para TDAH")
    tarefa_original = st.text_area("Cole aqui a tarefa original:")
    
    if st.button("Adaptar Tarefa"):
        if tarefa_original:
            with st.spinner("Adaptando..."):
                try:
                    prompt = f"Responda obrigatoriamente em português do Brasil. Adapte esta tarefa para uma criança com TDAH, dividindo em passos curtos, destacando palavras-chave e eliminando distrações:\n\n{tarefa_original}"
                    texto = gerar_resposta(prompt)
                    st.success("Tarefa Adaptada!")
                    st.write(texto)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.warning("Por favor, cole a tarefa original.")

elif opcao == "3. Orientação para Manejo de Crise":
    st.subheader("🆘 Guia Rápido de Suporte em Crises")
    crise = st.text_input("O que está acontecendo agora?", placeholder="Ex: Criança chorando e cobrindo os ouvidos devido a barulho alto")
    
    if st.button("Obter Orientações Práticas"):
        if crise:
            with st.spinner("Buscando orientações..."):
                try:
                    prompt = f"Responda obrigatoriamente em português do Brasil. Forneça orientações imediatas para um responsável ou professor lidar com esta situação de crise sensorial/comportamental: {crise}. Responda em tópicos curtos e diretos."
                    texto = gerar_resposta(prompt)
                    st.markdown(texto)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.warning("Por favor, descreva o que está acontecendo.")
            
