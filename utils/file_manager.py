import os


def read_file(path: str) -> str | None:
    """Lê um arquivo e retorna o conteúdo"""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def write_file(path: str, content: str) -> None:
    """Escreve conteúdo em um arquivo"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
