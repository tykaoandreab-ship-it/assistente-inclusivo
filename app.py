import streamlit as st
from google import genai

st.set_page_config(page_title="Assistente Inclusivo", page_icon="🧩", layout="centered")
st.title("🧩 Assistente de Apoio Inclusivo (TEA & TDAH)")
st.caption("Ferramenta de suporte pedagógico e organizacional.")

st.info("💡 Nota: Esta ferramenta oferece suporte pedagógico e organizacional. Não substitui diagnósticos ou tratamentos médicos.")

api_key_input = st.sidebar.text_input("Cole sua API Key do Google AI Studio:", type="password")
api_key = api_key_input.strip() if api_key_input else ""

if api_key:
    client = genai.Client(api_key=api_key)
    
    opcao = st.selectbox("Selecione o tipo de ajuda:", [
        "1. Gerar História Social / Rotina (TEA)",
        "2. Adaptar Tarefa Escolar (TDAH)",
        "3. Orientação para Manejo de Crise"
    ])
    st.divider()

    if opcao == "1. Gerar História Social / Rotina (TEA)":
        st.subheader("📖 Criador de História Social")
        idade = st.number_input("Idade da criança:", min_value=1, max_value=18, value=6)
        situacao = st.text_input("Qual situação vai acontecer?")
        if st.button("Gerar História Social"):
            if situacao:
                with st.spinner("Criando a história..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=f"Crie uma História Social simples para uma criança autista de {idade} anos. Situação: {situacao}."
                        )
                        st.success("História Pronta!")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Erro na geração: {e}")

    elif opcao == "2. Adaptar Tarefa Escolar (TDAH)":
        st.subheader("✏️ Adaptador de Tarefas para TDAH")
        tarefa = st.text_area("Cole aqui a tarefa original:")
        if st.button("Adaptar Tarefa"):
            if tarefa:
                with st.spinner("Adaptando..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=f"Adapte esta tarefa para uma criança com TDAH, dividindo em passos curtos e claros: {tarefa}"
                        )
                        st.success("Tarefa Adaptada!")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Erro na geração: {e}")

    elif opcao == "3. Orientação para Manejo de Crise":
        st.subheader("🛡️ Guia Rápido de Suporte em Crises")
        comportamento = st.text_input("O que está acontecendo agora?")
        if st.button("Obter Orientações Práticas"):
            if comportamento:
                with st.spinner("Buscando orientações..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=f"Forneça orientações imediatas para um responsável lidando com a seguinte crise: {comportamento}"
                        )
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Erro na geração: {e}")
else:
    st.warning("👈 Insira sua chave de API na barra lateral para começar.")
