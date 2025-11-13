# Deploy rápido para Hugging Face Space (Streamlit)

Este arquivo contém os passos mínimos para publicar este projeto como um Space do Hugging Face usando Streamlit.

Pré-requisitos
- Conta no Hugging Face e estar logado no navegador
- `git` instalado
- (opcional) `huggingface-cli` configurado se preferir usar CLI

Opções de deploy

1) Importar do GitHub (recomendado)

- No Hugging Face: New Space → escolha `Streamlit` → clique em `Import from GitHub` e selecione `Robinhoalm/MetaClassificador`.
- Em `Settings` → `Variables` do Space adicione `OPENAI_API_KEY` com a chave nova (não use a chave antiga exposta).

2) Usando o repositório do Space (via git)

```bash
# clona o repo do Space (substitua pelos seus valores)
git clone https://huggingface.co/spaces/<seu-usuario>/<seu-space>
cd <seu-space>

# copie os arquivos do projeto para a raiz do Space
cp -r /caminho/para/MetaClassificador/* .

git add .
git commit -m "Add Streamlit app for sentiment classifier"
git push
```

O Space por padrão irá buildar. A entrypoint pode ser `streamlit_app.py` (já incluído neste repo), que importa `classificador_streamlit.py`.

Segurança
- NÃO versionar `.env` nem chaves de API. Use as `Variables`/`Secrets` do Space.
- Se a chave foi exposta acidentalmente (como ocorreu localmente), revogue/rotacione imediatamente em https://platform.openai.com/account/api-keys .

Dicas
- Se o build falhar, verifique os logs no painel do Space (aba `Logs`).
- Se usar pacotes extras, confirme `requirements.txt` está atualizado.

Boa sorte! Se quiser, eu posso abrir a página de criação do Space para você agora.
