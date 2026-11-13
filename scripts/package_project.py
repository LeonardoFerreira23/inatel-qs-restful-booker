
import os
import tarfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"

BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local")

FILES_TO_PACKAGE = [
    "conftest.py",
    "pytest.ini",
    "requirements.txt",
    "run_tests.py",
    "data",
    "tests",
    "utils",
    "scripts",
]


def create_package():
    DIST_DIR.mkdir(exist_ok=True)

    package_name = f"restful-booker-tests-{BUILD_NUMBER}.tar.gz"
    package_path = DIST_DIR / package_name

    with tarfile.open(package_path, "w:gz") as archive:
        for item in FILES_TO_PACKAGE:
            source = ROOT_DIR / item

            if not source.exists():
                raise FileNotFoundError(
                    f"Arquivo ou diretorio nao encontrado: {source}"
                )

            archive.add(
                source,
                arcname=item
            )

    print(f"Pacote criado com sucesso: {package_path}")


if __name__ == "__main__":
    create_package()
