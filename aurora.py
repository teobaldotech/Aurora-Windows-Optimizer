from unittest.mock import Mock


def test_processo_simulado_com_sucesso():
    """Exemplo de resposta simulada de um processo externo."""
    process = Mock()
    process.returncode = 0
    process.stdout = "Operação concluída"
    process.stderr = ""

    assert process.returncode == 0
    assert "concluída" in process.stdout
    assert process.stderr == ""


def test_processo_simulado_com_falha():
    """O código deve conseguir representar uma falha simulada."""
    process = Mock()
    process.returncode = 1
    process.stdout = ""
    process.stderr = "Falha simulada"

    assert process.returncode != 0
    assert process.stderr != ""
