import subprocess
import shutil
import os

def test_create_project():
    project_name = "teste_unitario"
    if os.path.exists(project_name):
        shutil.rmtree(project_name)

    result = subprocess.run(["oryum", "new", project_name], capture_output=True, text=True)

    assert result.returncode == 0
    assert os.path.exists(project_name)
    assert os.path.isfile(f"{project_name}/app.py")
    assert os.path.isfile(f"{project_name}/requirements.txt")
    assert os.path.isfile(f"{project_name}/init_db.py")
    assert os.path.isfile(f"{project_name}/oryum.json")

    # Limpeza após o teste
    shutil.rmtree(project_name)
