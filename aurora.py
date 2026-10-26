# process_runner.py
import subprocess


def executar_comando(comando: list[str]) -> dict:
    """Executa um comando no sistema e retorna o resultado formatado."""
    resultado = subprocess.run(
        comando, capture_output=True, text=True, check=False
    )

    if resultado.returncode == 0:
        return {"status": "sucesso", "saida": resultado.stdout.strip()}

    return {"status": "erro", "mensagem": resultado.stderr.strip()}
