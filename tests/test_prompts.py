"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
from pathlib import Path

FILE_PATH = "prompts/bug_to_user_story_v2.yml"

def load_prompt(file_path: str):
    """Carrega o conteúdo do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    prompt_key = list(data.keys())[0] if data else None
    return data.get(prompt_key, {})

class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup_prompt(self):
        self.prompt = load_prompt(FILE_PATH)
        assert self.prompt, "Falha ao carregar YAML"

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo system_prompt existe e não está vazio."""
        system_prompt = self.prompt.get('system_prompt')
        assert system_prompt is not None, "Campo 'system_prompt' ausente"
        assert system_prompt.strip(), "Campo 'system_prompt' vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt.get('system_prompt', '')
        assert any(phrase in system_prompt.lower() for phrase in [
            'você é um', 'você é uma', 'você atua como', 'como um'
        ]), "Persona/role não definida no system_prompt"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt.get('system_prompt', '')
        assert any(phrase in system_prompt.lower() for phrase in [
            'user story', 'como', 'eu quero', 'markdown', 'gherkin', 'given-when-then'
        ]), "Não menciona formato User Story ou Markdown/Gherkin"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt.get('system_prompt', '')
        has_examples = (
            'exemplo' in system_prompt.lower() or
            'output' in system_prompt.lower() or
            'input' in system_prompt.lower() 
        )
        assert has_examples, "Exemplos few-shot não encontrados"

    def test_prompt_no_todos(self):
        """Garante que não há [TODO] no texto do prompt."""
        system_prompt = self.prompt.get('system_prompt', '')
        user_prompt = self.prompt.get('user_prompt', '')
        full_text = system_prompt + ' ' + user_prompt
        assert '[todo]' not in full_text.lower(), "Encontrado [TODO] no prompt"

    def test_minimum_techniques(self):
        """Verifica que pelo menos 2 técnicas estão listadas em techniques_applied."""
        techniques = self.prompt.get('techniques_applied', [])
        assert isinstance(techniques, list), "'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, f"Encontradas apenas {len(techniques)} técnicas: {techniques}"
        # Exemplos esperados (case-insensitive)
        expected_patterns = ['role prompting', 'few-shot', 'chain of thought', 'tree of thought', 
                           'skeleton of thought', 'react']
        found_matching = sum(1 for tech in techniques if any(pattern in str(tech).lower() for pattern in expected_patterns))
        assert found_matching >= 2, f"Menos de 2 técnicas reconhecidas em {techniques}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
