# MetaClassificador com API ChatGPT

## Objetivo

Criar um classificador baseado em definições pré-definidas para orientar a LLM na classificação de textos com a utilização da API do ChatGPT.

## Modelo

Para essa atividade utilizaremos OBRIGATORIAMENTE o modelo gpt-4.1-nano.

## Arquitetura

Nossa aplicação utilizará os seguintes componentes:

- API OPENAI / ChatGPT
- Linguagem Python
- Streamlit

## Passo-a-Passo

1. Testar o código deste repositório
  - clone o repositório
  - instale as dependências utilizando o comando "pip install -r requirements.txt"
  - crie o arquivo ".env" com a chave da OpenAI que for passada em sala de aula
  - execute o comando "python classificador_sentimento.py"
  - avalie o resultado
  - altere o texto na variável "texto" no código python e execute novamente para avaliar o resultado
    
2. Criar projeto no GitHUB (se preferir, faça um fork do projeto inicial)

3. Procurar no https://www.kaggle.com/ um problema real com uma base de dados de classificação de texto

4. Crie um novo classificador redefinindo o prompt para o problema escolhido

5. Teste e avalie resultado.

6. Crie uma interface em streamlit para uma vez que o usuário informe o texto, realize a classificação com retorno visual

7. Publique seu classificador no HuggingFace

  - Cuidado para não expor a chave OpenAI, ela nunca deve estar versionada!!!!

