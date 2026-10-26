# test_process_runner.py
from unittest.mock import MagicMock, patch
from process_runner import executar_comando


@patch("subprocess.run")
def test_executar_comando_com_sucesso(mock_run):
    """Testa o comportamento quando o processo externo é concluído com sucesso."""
    # Configuração da resposta simulada do subprocess.run
    mock_processo = MagicMock()
    mock_processo.returncode = 0
    mock_processo.stdout = "Operação concluída com sucesso\n"
    mock_processo.stderr = ""
    mock_run.return_value = mock_processo

    # Execução da função
    resposta = executar_comando(["echo", "hello"])

    # Validações (Asserts)
    assert resposta == {
        "status": "sucesso",
        "saida": "Operação concluída com sucesso",
    }
    mock_run.assert_called_once_with(
        ["echo", "hello"], capture_output=True, text=True, check=False
    )


@patch("subprocess.run")
def test_executar_comando_com_falha(mock_run):
    """Testa o comportamento quando o processo externo falha."""
    # Configuração do erro simulado
    mock_processo = MagicMock()
    mock_processo.returncode = 1
    mock_processo.stdout = ""
    mock_processo.stderr = "Erro: Comando não encontrado\n"
    mock_run.return_value = mock_processo

    # Execução
    resposta = executar_comando(["invalid_command"])

    # Validações
    assert resposta == {
        "status": "erro",
        "mensagem": "Erro: Comando não encontrado",
    }
    mock_run.assert_called_once()
