"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.loading import load_prompt
from utils import load_yaml, check_env_vars, print_section_header
from langsmith import Client

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    
    try:
        system_prompt = prompt_data.get('system_prompt', '')
        user_prompt = prompt_data.get('user_prompt', '{bug_report}')

        prompt_template = ChatPromptTemplate.from_messages(
                [("system", system_prompt), ("human", user_prompt)]
            )

        url = hub.push(prompt_name, prompt_template)
        print(url)
        return True
    except Exception as e:
        print(f"❌ Erro ao fazer o push: {e}")
        return False




def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    required_fields = ['description', 'system_prompt', 'version']
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    username = os.getenv('USERNAME_LANGSMITH_HUB')

    prompt_template = load_yaml("prompts/bug_to_user_story_v2.yml").get("bug_to_user_story_v2")
    
    is_valid, errors = validate_prompt(prompt_template)

    if is_valid:
        push_prompt_to_langsmith(f"{username}/bug_to_user_story_v2", prompt_template)
    else: 
        for err in errors:
            print(f"Erro: {err}")


if __name__ == "__main__":
    sys.exit(main())
