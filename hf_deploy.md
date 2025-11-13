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

**Passo a passo rápido (checklist)**

- **1.** Crie um Space no Hugging Face → escolha `Streamlit`.
- **2.** No campo de importação escolha `Import from GitHub` e selecione o repositório `Robinhoalm/MetaClassificador` (ou clone o Space e copie os arquivos manualmente).
- **3.** Confirme que a raiz do Space contém `streamlit_app.py` (este arquivo importa `classificador_streamlit.py` que é o entrypoint do app).
- **4.** Em `Settings` → `Variables` do Space adicione a variável `OPENAI_API_KEY` com a chave **nova** da OpenAI (não use a chave que foi exposta anteriormente).
- **5.** Faça o push do código para o repositório do Space (ou use a importação automática). O build do Space vai rodar automaticamente.
- **6.** Acompanhe os logs de build e abra a URL do Space quando o status for `Running`.

**Rotacionar chave (recomendado)**

- A chave antiga foi removida do workspace local por segurança. Acesse https://platform.openai.com/account/api-keys e revogue/rotacione a chave exposta. Em seguida gere uma nova chave e use-a apenas como `OPENAI_API_KEY` no Secrets do Space.

Se quiser, eu posso abrir novamente a página de criação do Space para você.
