# RAG Project

Este é um projeto simples utilizando Retrieval-Augmented Generation (RAG) com
FastAPI e LangChain. esse projeto utiliza um pdf com parte de infração de
trânsito.

## Tecnologias Utilizadas

- **FastAPI** - Framework web para APIs em Python
- **Uvicorn** - Servidor ASGI para rodar o FastAPI
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Pydantic** - Validação de dados
- **LangChain** - Framework para conectar LLMs a fontes externas de conhecimento
- **langchain-openai** - Integração do LangChain com a API da OpenAI
- **ChromaDB** - Banco de dados vetorial para armazenamento e recuperação de
  informações

## Como Rodar o Projeto

1. Clone o repositório e entre na pasta do projeto:
   ```bash
   git clone https://github.com/hesfra/pocRAG.git
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente (crie um arquivo `.env` com suas
   credenciais com o seguinte modelo: OPENAI_API_KEY = {key} ).

5. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Como Fazer Perguntas

Envie uma requisição POST para `http://localhost:{porta}/ai` com um JSON no
seguinte formato:

```json
{
    "text": "dirigir sem CNH"
}
```

O servidor responderá com a resposta gerada pelo modelo de IA baseado no
contexto recuperado.

## Contribuição

Sinta-se à vontade para contribuir com melhorias! Para isso, faça um fork do
repositório, crie uma branch com suas alterações e envie um pull request.

---

Caso tenha alguma dúvida, abra uma issue no repositório!

o link para a referencia utilizada no material é:
https://github.com/Piyush150398/RAG_Application/tree/main

não utilizei o streamlit, fiz direto pelo fastapi. alguns problemas que já foram
vistos acontecerem são:

- eu utilizo uma collection específica, portanto isso está dando problema na
  hora de reinicializar o aplicativo, pra resolver precisa apagar a pasta que é
  criada dentro do collections
