import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.google import Gemini

from ingest import build_knowledge

load_dotenv()

MODEL_ID = "gemini-2.5-flash"

INSTRUCTIONS = [
    "Você é um assistente que responde perguntas sobre a carreira, discografia, "
    "turnês e prêmios de Taylor Swift, usando EXCLUSIVAMENTE as informações "
    "encontradas na base de conhecimento.",
    "Sempre use a ferramenta de busca na base de conhecimento antes de responder, "
    "mesmo que ache que já sabe a resposta.",
    "Se a informação não estiver claramente nos documentos recuperados, diga "
    "explicitamente que não sabe ou que a pergunta está fora do escopo da base "
    "de conhecimento. Nunca invente ou complete a resposta com conhecimento geral.",
    "Ao final da resposta, indique de qual documento (nome do arquivo) a "
    "informação foi extraída, em uma linha no formato: 'Fonte: <nome_do_arquivo>' e"
    "copie literalmente o trecho do documento utilizado para responder a pergunta.",
    "Seja direto e objetivo. Não adicione informações que não estejam nos trechos "
    "recuperados da base.",
]


def build_agent() -> Agent:
    knowledge = build_knowledge()
    return Agent(
        model=Gemini(id=MODEL_ID),
        knowledge=knowledge,
        search_knowledge=True,
        instructions=INSTRUCTIONS,
        markdown=True,
    )


if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit(
            "GOOGLE_API_KEY não encontrada. Copie .env.example para .env e "
            "preencha sua chave da Gemini API."
        )

    agent = build_agent()

    print("=== Agente de Conhecimento Axisor (RAG com Agno) ===")
    print("Digite sua pergunta (ou 'sair' para encerrar).\n")

    while True:
        question = input("Você: ").strip()
        if question.lower() in {"sair", "exit", "quit"}:
            print("Até mais!")
            break
        if not question:
            continue
        try:
            agent.print_response(question, stream=True)
        except Exception as exc:
            print(
                "\n[Erro] Não foi possível obter resposta do modelo agora. "
                f"Detalhe: {exc}\n"
                "Dica: se for erro 429, você atingiu o limite gratuito da API "
                "Gemini, aguarde alguns instantes e tente novamente.\n"
            )
        print()
