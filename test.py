from chat import build_agent

TEST_CASES = [
    {
        "question": "Em que ano foi lançado o álbum 1989?",
        "expected": "2014 (27 de outubro de 2014). "
        "Fonte: discografia_albuns.txt",
    },
    {
        "question": "Qual é a cor favorita da Taylor Swift?",
        "expected": "O agente deve informar que essa informação não está presente na base e não inventar uma resposta."
    },
    {
        "question": "Quantas vezes a Taylor Swift venceu o Grammy de Álbum do Ano?",
        "expected": "4 vezes: Fearless (2010), 1989 (2016), Folklore (2021) "
        "e Midnights (2024). Fonte: turnes_premios.txt",
    },
    {
        "question": "Qual é o prato de comida favorito da Taylor Swift?",
        "expected": "NÃO deve responder com dados inventados — a base não "
        "cobre esse assunto. O agente deve dizer que não sabe / está fora "
        "do escopo dos documentos.",
    },
    {
        "question": "Por que a Taylor Swift regravou seus álbuns antigos?",
        "expected": "Porque a Big Machine Records foi vendida em 2019 e os "
        "masters dos 6 primeiros álbuns passaram para terceiros sem o "
        "consentimento dela; ela regravou como 'Taylor's Version'. "
        "Fonte: biografia_carreira.txt",
    },
]


if __name__ == "__main__":
    agent = build_agent()

    print("=== Teste do agente (4 perguntas) ===\n")

    for i, case in enumerate(TEST_CASES, start=1):
        print(f"--- Pergunta {i}/{len(TEST_CASES)} ---")
        print(f"Pergunta: {case['question']}")
        print(f"Esperado: {case['expected']}")
        print("Resposta do agente:")
        try:
            agent.print_response(case["question"], stream=False)
        except Exception as exc:
            print(f"[Erro ao consultar o agente: {exc}]")
        print()
