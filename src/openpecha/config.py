from pathlib import Path


def _mkdir(path):
    path.mkdir(exist_ok=True, parents=True)
    return path


BASE_PATH = _mkdir(Path.home() / ".pechadata")
PECHAS_PATH = _mkdir(BASE_PATH / "pechas")
