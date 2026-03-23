"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header
from langsmith import Client 

load_dotenv()

def pull_prompts_from_langsmith():
    client = Client()
    prompt = client.pull_prompt("leonanluppi/bug_to_user_story_v1")
    
    try:
        serialized = prompt.to_json()
    except AttributeError:
        try:
            serialized = prompt.to_dict()
        except AttributeError:
            serialized = prompt.model_dump()

    data = {
            "name": "leonanluppi/bug_to_user_story_v1",
            "prompt": serialized,
        }

    out_path = Path("prompts/raw_prompts.yml")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    save_yaml(data, out_path)

    print(f"Prompt salvo em {out_path.resolve()}")


def main():
    """Função principal"""
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
