Guia rápido: preparar e publicar no Hugging Face Space

1) Crie um Space do tipo `Streamlit` no Hugging Face.
2) No repositório do Space, adicione os arquivos do projeto: `classificador_streamlit.py`, `streamlit_app.py`, `requirements.txt`, `kaggle_prepare_and_evaluate.py`.
3) Configure Secrets no Space (Settings -> Variables):
   - `OPENAI_API_KEY` com sua chave OpenAI
   - NÃO envie `.env` ao repositório
4) Push do código para o Space via Git (use `huggingface-cli` ou o link do Space):

```bash
git clone https://huggingface.co/spaces/<seu-usuario>/<seu-space>
cd <seu-space>
cp -r /caminho/para/MetaClassificador/* .
git add .
git commit -m "Adiciona Streamlit app usando GPT-4.1-nano"
git push
```

5) No painel do Space, configure `Hardware` conforme necessidade (CPU é suficiente, mas otimize para custo).
6) Teste o app no Space e monitore uso de tokens.

Observações de segurança:
- Nunca versionar `OPENAI_API_KEY` em repositórios públicos.
- Para produção, considere limites e caching de previsões para reduzir custos.
