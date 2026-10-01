import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(page_title="Assistente Inclusivo", page_icon="🧩")

st.title("🧩 Assistente de Apoio Inclusivo (TEA & TDAH)")
st.caption("Ferramenta de suporte pedagógico e organizacional.")

st.info("💡 **Nota:** Esta ferramenta oferece suporte pedagógico e organizacional. Não substitui diagnósticos ou tratamentos médicos.")

# Barra lateral para chaves
st.sidebar.header("Configuração de Acesso")
api_key_gemini = st.sidebar.text_input("Cole sua API Key do Gemini (Opcional):", type="password")
api_key_groq = st.sidebar.text_input("Cole sua API Key do Groq:", type="password", value="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")

if not api_key_gemini and not api_key_groq:
    st.warning("👈 Insira pelo menos uma chave de API na barra lateral para começar.")
    st.stop()

# Função de geração com contingência automática
def gerar_resposta(prompt):
    # 1. Tenta via Groq (Llama 3.3) - Ultrarrápido e sem erros de sobrecarga
    if api_key_groq:
        try:
            from groq import Groq
            client_groq = Groq(api_key=api_key_groq)
            chat_completion = client_groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            pass

    # 2. Contingência via Google Gemini
    if api_key_gemini:
        try:
            client = genai.Client(api_key=api_key_gemini)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if response and response.text:
                return response.text
        except Exception as e:
            pass

    raise Exception("Não foi possível gerar a resposta no momento. Tente novamente em alguns instantes.")

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
                    prompt = f"Crie uma História Social simples para uma criança de {idade} anos sobre a seguinte situação: {situacao}. Use linguagem clara, frases curtas e tom acolhedor."
                    texto = gerar_resposta(prompt)
                    st.success("História Pronta!")
                    st.write(texto)
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
                    prompt = f"Adapte esta tarefa para uma criança com TDAH, dividindo em passos curtos, destacando palavras-chave e eliminando distrações:\n\n{tarefa_original}"
                    texto = gerar_resposta(prompt)
                    st.success("Tarefa Adaptada!")
                    st.write(texto)
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
                    prompt = f"Forneça orientações imediatas para um responsável ou professor lidar com esta situação de crise sensorial/comportamental: {crise}. Responda em tópicos curtos e diretos."
                    texto = gerar_resposta(prompt)
                    st.markdown(texto)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.warning("Por favor, descreva o que está acontecendo.")
