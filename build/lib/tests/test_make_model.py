import subprocess
import shutil
import os
import pytest

@pytest.fixture(autouse=True)
def cleanup():
    # Antes e depois de cada teste, remove a pasta
    yield
    for d in ("teste_unitario_model",):
        if os.path.exists(d):
            shutil.rmtree(d)

def test_make_model(tmp_path):
    project_name = tmp_path / "teste_unitario_model"

    # 1) Gera projeto
    subprocess.run(
        ["oryum", "new", str(project_name)],
        check=True,
        capture_output=True,
        text=True
    )

    # 2) Executa make:model dentro da pasta recém-criada
    result = subprocess.run(
        ["oryum", "make:model", "Produto", "--fields", "nome:string,preco:float"],
        cwd=str(project_name),
        check=True,
        capture_output=True,
        text=True
    )

    # 3) Verifica código, mensagem e arquivo
    assert "Modelo criado com sucesso" in result.stdout
    model_file = project_name / "models" / "produto.py"
    assert model_file.exists()