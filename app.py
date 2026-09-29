import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(page_title="Assistente Inclusivo", page_icon="🧩")

st.title("🧩 Assistente de Apoio Inclusivo (TEA & TDAH)")
st.caption("Ferramenta de suporte pedagógico e organizacional.")

st.info("💡 **Nota:** Esta ferramenta oferece suporte pedagógico e organizacional. Não substitui diagnósticos ou tratamentos médicos.")

# Barra lateral para inserir a API Key
api_key = st.sidebar.text_input("Cole sua API Key do Google AI Studio:", type="password")

if not api_key:
    st.warning("👈 Insira sua chave de API na barra lateral para começar.")
    st.stop()

# Inicialização do cliente Gemini
client = genai.Client(api_key=api_key)

# Seleção da funcionalidade
opcao = st.selectbox(
    "Selecione o tipo de ajuda:",
    [
        "1. Gerar História Social / Rotina (TEA)",
        "2. Adaptar Tarefa Escolar (TDAH)",
        "3. Orientação para Manejo de Crise"
    ]
)

# Funcionalidade 1: História Social
if opcao == "1. Gerar História Social / Rotina (TEA)":
    st.subheader("📖 Criador de História Social")
    idade = st.number_input("Idade da criança:", min_value=2, max_value=18, value=6)
    situacao = st.text_input("Qual situação vai acontecer?", placeholder="Ex: Ir ao dentista fazer limpeza")
    
    if st.button("Gerar História Social"):
        if situacao:
            with st.spinner("Criando a história..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=f"Crie uma História Social simples para uma criança de {idade} anos sobre a seguinte situação: {situacao}. Use linguagem clara, frases curtas e tom acolhedor."
                    )
                    st.success("História Pronta!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.warning("Por favor, informe a situação.")

# Funcionalidade 2: Adaptar Tarefa
elif opcao == "2. Adaptar Tarefa Escolar (TDAH)":
    st.subheader("📝 Adaptador de Tarefas para TDAH")
    tarefa_original = st.text_area("Cole aqui a tarefa original:")
    
    if st.button("Adaptar Tarefa"):
        if tarefa_original:
            with st.spinner("Adaptando..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=f"Adapte esta tarefa para uma criança com TDAH, dividindo em passos curtos, destacando palavras-chave e eliminando distrações:\n\n{tarefa_original}"
                    )
                    st.success("Tarefa Adaptada!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.warning("Por favor, cole a tarefa original.")

# Funcionalidade 3: Manejo de Crise
elif opcao == "3. Orientação para Manejo de Crise":
    st.subheader("🆘 Guia Rápido de Suporte em Crises")
    crise = st.text_input("O que está acontecendo agora?", placeholder="Ex: Criança chorando e cobrindo os ouvidos devido a barulho alto")
    
    if st.button("Obter Orientações Práticas"):
        if crise:
            with st.spinner("Buscando orientações..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=f"Forneça orientações imediatas para um responsável ou professor lidar com esta situação de crise sensorial/comportamental: {crise}. Responda em tópicos curtos e diretos."
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.warning("Por favor, descreva o que está acontecendo.")
