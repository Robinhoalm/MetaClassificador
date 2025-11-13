import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI
client = OpenAI(api_key=api_key)

# Configuração da página
st.set_page_config(page_title="Classificador de Texto", page_icon="🤖")

st.title("🤖 Classificador de Texto com GPT-4.1-nano")

# Entrada de texto multilinha
texto = st.text_area(
    "Digite o texto que deseja classificar:",
    placeholder="Exemplo: O atendimento foi ótimo, mas o preço é alto.",
    height=150
)

# Botão de ação
if st.button("Classificar"):
    if not texto.strip():
        st.warning("Por favor, digite um texto antes de classificar.")
    else:
        with st.spinner("Analisando o texto..."):
            # Instrução para retornar JSON com label, confidence e justificativa curta
            prompt = (
                "Classifique o sentimento deste texto em uma das três opções: Positive, Negative, Neutral.\n"
                f"Texto: \"{texto}\"\n"
                "Responda única e exclusivamente em JSON com as chaves: \"label\" (uma das opções), \"confidence\" (valor float entre 0 e 1) e \"justification\" (1-2 frases justificando a escolha)."
            )

            resposta = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "Você é um classificador de sentimento que responde estritamente em JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            raw = resposta.choices[0].message.content.strip()
            # Tenta parsear JSON com justificativa
            try:
                import json

                parsed = json.loads(raw)
                classificacao = parsed.get('label', '').lower()
                confidence = float(parsed.get('confidence', 0))
                justification = parsed.get('justification', '')
            except Exception:
                # fallback simples: extrair label e deixar justificativa vazia
                classification_text = raw.lower()
                if 'positive' in classification_text or 'positivo' in classification_text:
                    classificacao = 'positive'
                elif 'negative' in classification_text or 'negativo' in classification_text:
                    classificacao = 'negative'
                else:
                    classificacao = 'neutral'
                confidence = 0.0
                justification = ''

        # Define cor e ícone conforme classificação
        if "positive" in classificacao or "positivo" in classificacao:
            cor = "#00C853"  # verde
            icone = "😊"
            texto_label = "Positivo"
        elif "negative" in classificacao or "negativo" in classificacao:
            cor = "#D50000"  # vermelho
            icone = "😠"
            texto_label = "Negativo"
        else:
            cor = "#FFD600"  # amarelo
            icone = "😐"
            texto_label = "Neutro"

        # Exibe resultado com cor e ícone
        st.markdown(
            f"""
            <div style='background-color:{cor}; padding:15px; border-radius:10px; text-align:center;'>
                <h3 style='color:white;'>{icone} Classificação: {texto_label} — Confiança: {confidence:.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Barra de confiança
        st.progress(min(max(confidence, 0.0), 1.0))
        # Mostra justificativa e JSON bruto em expanders
        if justification:
            with st.expander('Justificativa da classificação'):
                st.write(justification)

        with st.expander('Resposta JSON bruta'):
            st.code(raw)
