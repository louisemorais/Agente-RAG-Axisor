# Agente de Conhecimento RAG — Axisor Technologies (Desafio Técnico)

Agente de **Agentic RAG** construído com o framework [Agno](https://github.com/agno-agi/agno), que ingere um conjunto de documentos sobre a carreira, discografia, turnês e prêmios da Taylor Swift em uma vector DB e responde perguntas **exclusivamente** com base nesse conteúdo, indicando sempre de qual documento a resposta foi extraída.

## Requisitos do desafio atendidos

- **Ingestão de corpus** (mínimo 3 documentos) em uma vector DB — `LanceDB`.
- **Agente Agno** configurado com `knowledge` e `search_knowledge=True`.
- **Anti-alucinação**: o agente é instruído a responder apenas com base nos documentos recuperados e a dizer explicitamente quando não sabe ou quando a pergunta está fora do escopo.
- **Rastreabilidade**: cada resposta indica o documento de origem e o trecho literal utilizado.
- **README** (este arquivo) com instruções de uso e decisões técnicas.

## Arquitetura e decisões técnicas

| Item | Escolha | Motivo |
|---|---|---|
| Framework | **Agno** | Exigência do desafio |
| Vector DB | **LanceDB** | Roda em arquivo local, sem precisar subir um serviço externo como Postgres, zero-config, adequado para o escopo do desafio |
| Busca | **Hybrid Search** (`SearchType.hybrid`) | Combina busca vetorial (similaridade semântica) com busca full-text (BM25/keyword), reduzindo falsos negativos quando a pergunta usa termos exatos que aparecem no texto (ex.: nomes de álbuns, datas) |
| Embeddings | **GeminiEmbedder** (`gemini-embedding-001`) | Free tier do Google, consistente com o LLM escolhido |
| LLM | **Gemini 2.5 Flash** (`gemini-2.5-flash`) | Free tier, baixa latência, suficiente para QA sobre um corpus pequeno |
| Formato do corpus | **`.txt`** | Documentos de texto simples, sem necessidade de formatação para o conteúdo (biografia, discografia, prêmios). Evita complexidade extra de parsing que PDF ou DOCX exigiriam, mantendo a ingestão simples e direta |
| Chunking | Padrão do Agno (`Knowledge.add_content`) | Os documentos são curtos e cada um cobre um único tema (um arquivo por assunto: biografia, discografia, turnês/prêmios). Como o conteúdo já é naturalmente coeso e pequeno, o chunker default do Agno preserva o contexto sem cortar informação no meio, dispensando ajuste manual de `chunk_size`/`overlap` para o escopo deste desafio |

## Estrutura do projeto

```
.
├── chat.py            # CLI interativa para conversar com o agente
├── ingest.py          # Script de ingestão do corpus na vector DB (LanceDB)
├── test.py            # Testes com perguntas e respostas esperadas
├── requirements.txt   # Dependências do projeto
├── .env.example        # Modelo de variáveis de ambiente
├── data/               # Corpus de documentos (.txt) a ser ingerido
└── tmp/lancedb/         # Base vetorial gerada localmente pela ingestão
```

## Como rodar

### 1. Pré-requisitos

- Python 3.12
- Uma chave de API do Google AI Studio (Gemini) — gratuita: https://aistudio.google.com/app/apikey

### 2. Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configuração

```bash
cp .env.example .env
```

Edite o `.env` e preencha:

```
GOOGLE_API_KEY=sua_chave_aqui
```

### 4. Corpus de documentos

Os documentos utilizados ficam na pasta `data/`:

- `data/biografia_carreira.txt`
- `data/discografia_albuns.txt`
- `data/turnes_premios.txt`

### 5. Ingestão dos documentos

```bash
python ingest.py
```

Isso cria a base vetorial em `tmp/lancedb`.

### 6. Conversar com o agente

```bash
python chat.py
```

Digite suas perguntas no terminal. Digite `sair`, `exit` ou `quit` para encerrar.

### 7. Rodar os testes

```bash
python test.py
```

Executa um conjunto de perguntas com resposta esperada conhecida, incluindo um caso deliberadamente **fora do escopo** da base, para validar o comportamento anti-alucinação.

## Tratamento de alucinação

O agente é instruído (via `INSTRUCTIONS` em `chat.py`) a:

1. Sempre consultar a base de conhecimento antes de responder (`search_knowledge=True`), mesmo quando "acha" que sabe a resposta.
2. Responder **apenas** com base no conteúdo recuperado — nunca complementar com conhecimento geral do modelo.
3. Dizer explicitamente que não sabe / que a pergunta está fora do escopo quando a informação não estiver nos documentos recuperados.

Esse comportamento é validado em `test.py`, com a pergunta sobre o "prato de comida favorito da Taylor Swift" e na pergunta "Qual é a cor favorita da Taylor Swift?", dados que não existe na base, no qual o agente deve se recusar a inventar uma resposta.

## Rastreabilidade das respostas

Ao final de cada resposta, o agente indica:

```
Fonte: <nome_do_arquivo>
"<trecho literal utilizado>"
```

Isso permite auditar de qual documento a informação foi extraída.
