# Boas Práticas de Versionamento e Deploy para ORYUM STACK CLI

## Versionamento Semântico

Para garantir uma evolução consistente e previsível da ORYUM STACK CLI, recomendamos a adoção do **Versionamento Semântico** (SemVer), seguindo o formato `MAJOR.MINOR.PATCH`:

1. **MAJOR**: Incrementado quando há mudanças incompatíveis com versões anteriores
2. **MINOR**: Incrementado quando há adição de funcionalidades mantendo compatibilidade
3. **PATCH**: Incrementado quando há correções de bugs mantendo compatibilidade

### Exemplos práticos:

- `1.0.0`: Versão inicial estável
- `1.1.0`: Adição de novo comando (ex: `oryum make:api`)
- `1.1.1`: Correção de bug no comando existente
- `2.0.0`: Mudança na estrutura de comandos que quebra compatibilidade

### Implementação no código:

```python
# oryum_stack/__init__.py
__version__ = "1.0.0"
```

```python
# oryum_stack/cli.py
from oryum_stack import __version__

app = typer.Typer(
    name="oryum",
    help="Ferramenta para criação de projetos Flask com autenticação e painel admin",
)

@app.callback()
def main(version: bool = typer.Option(False, "--version", "-v", help="Mostrar versão")):
    """
    ORYUM STACK CLI: Gerador de projetos Flask com autenticação e painel admin.
    """
    if version:
        typer.echo(f"ORYUM STACK CLI versão: {__version__}")
        raise typer.Exit()
```

## Controle de Versão com Git

### Estrutura de Branches

Recomendamos o modelo **GitFlow** adaptado para as necessidades do projeto:

- **main**: Branch principal que contém código de produção estável
- **develop**: Branch de desenvolvimento para próxima versão
- **feature/xxx**: Branches para novas funcionalidades
- **bugfix/xxx**: Branches para correções de bugs
- **release/x.y.z**: Branches para preparação de releases

### Commits Semânticos

Adotar commits semânticos para facilitar a geração automática de changelogs:

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

Tipos comuns:
- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Alterações na documentação
- **style**: Formatação, ponto-e-vírgula, etc; sem alteração de código
- **refactor**: Refatoração de código
- **test**: Adição ou correção de testes
- **chore**: Atualizações de tarefas de build, configurações, etc

Exemplo:
```
feat(make:model): adiciona suporte para relacionamentos

Implementa a geração automática de relacionamentos entre modelos
através da flag --relationships no comando make:model.

Closes #123
```

### Arquivo CHANGELOG.md

Manter um arquivo CHANGELOG.md atualizado com todas as alterações relevantes:

```markdown
# Changelog

## [1.1.0] - 2025-05-20
### Adicionado
- Comando `make:api` para gerar endpoints RESTful
- Suporte para relacionamentos em modelos

### Corrigido
- Bug na geração de rotas com caracteres especiais

## [1.0.0] - 2025-05-01
### Adicionado
- Versão inicial estável
- Comandos `new`, `make:model` e `make:route`
- Suporte para SQLite e PostgreSQL
```

## Publicação no PyPI

### Preparação do Pacote

1. **Configuração do pyproject.toml**:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "oryum-stack"
version = "1.0.0"
description = "CLI para criação de projetos Flask com autenticação e painel admin"
readme = "README.md"
authors = [
    {name = "Oryum Tech", email = "contato@oryum.com.br"}
]
license = {text = "MIT"}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
requires-python = ">=3.8"
dependencies = [
    "typer>=0.9.0",
    "cookiecutter>=2.1.1",
    "pyyaml>=6.0",
    "colorama>=0.4.4",
]

[project.urls]
"Homepage" = "https://github.com/oryumtech/oryum-stack"
"Bug Tracker" = "https://github.com/oryumtech/oryum-stack/issues"

[project.scripts]
oryum = "oryum_stack.cli:app"
```

2. **Criação de arquivos de distribuição**:

```bash
python -m pip install --upgrade build
python -m build
```

3. **Publicação no PyPI**:

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
```

### Automação com GitHub Actions

Criar um workflow para publicação automática no PyPI quando uma nova tag é criada:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

## Integração Contínua

### Testes Automatizados

Configurar testes automatizados com pytest:

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        pip install -e .
    - name: Test with pytest
      run: |
        pytest --cov=oryum_stack tests/
```

### Verificação de Qualidade de Código

Adicionar verificação de qualidade com flake8, black e isort:

```yaml
# .github/workflows/lint.yml
name: Lint

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 black isort
    - name: Lint with flake8
      run: |
        flake8 oryum_stack tests
    - name: Check formatting with black
      run: |
        black --check oryum_stack tests
    - name: Check imports with isort
      run: |
        isort --check-only --profile black oryum_stack tests
```

## Deploy de Projetos Gerados

### Configuração para Render

Incluir arquivos de configuração para deploy no Render nos projetos gerados:

```python
# {{cookiecutter.project_name}}/render.yaml
services:
  - type: web
    name: {{cookiecutter.project_name}}
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: {{cookiecutter.project_name}}-db
          property: connectionString

databases:
  - name: {{cookiecutter.project_name}}-db
    {% if cookiecutter.db_type == 'postgresql' %}
    databaseName: {{cookiecutter.project_name}}
    user: {{cookiecutter.project_name}}
    {% endif %}
```

### Configuração para Railway

Incluir arquivos de configuração para deploy no Railway nos projetos gerados:

```python
# {{cookiecutter.project_name}}/railway.json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "gunicorn run:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Documentação de Deploy

Incluir instruções detalhadas de deploy em ambas as plataformas na documentação gerada:

```markdown
# Deploy no Render

1. Crie uma conta no [Render](https://render.com)
2. Conecte seu repositório GitHub
3. Clique em "New Web Service"
4. Selecione seu repositório
5. O Render detectará automaticamente as configurações do arquivo render.yaml
6. Clique em "Create Web Service"

# Deploy no Railway

1. Crie uma conta no [Railway](https://railway.app)
2. Instale a CLI do Railway: `npm i -g @railway/cli`
3. Faça login: `railway login`
4. Inicialize o projeto: `railway init`
5. Faça deploy: `railway up`
```

## Atualizações e Migrações

### Estratégia de Atualização da CLI

1. **Verificação de Versão**:
   Implementar comando para verificar se há versões mais recentes disponíveis:

```python
@app.command()
def check_update():
    """Verifica se há atualizações disponíveis para a CLI."""
    import requests
    from oryum_stack import __version__
    
    try:
        response = requests.get("https://pypi.org/pypi/oryum-stack/json")
        latest_version = response.json()["info"]["version"]
        
        if latest_version != __version__:
            typer.echo(f"Nova versão disponível: {latest_version} (atual: {__version__})")
            typer.echo("Para atualizar, execute: pip install --upgrade oryum-stack")
        else:
            typer.echo(f"Você está usando a versão mais recente ({__version__}).")
    except Exception as e:
        typer.echo(f"Erro ao verificar atualizações: {e}")
```

2. **Migrações de Projetos**:
   Implementar comando para atualizar projetos existentes:

```python
@app.command()
def upgrade_project():
    """Atualiza um projeto existente para a versão atual da CLI."""
    # Lógica para atualizar estrutura e dependências
    pass
```

## Documentação Bilíngue

### Estrutura de Documentação

Manter documentação em português e inglês:

```
docs/
├── en/
│   ├── index.md
│   ├── installation.md
│   ├── commands.md
│   └── deployment.md
└── pt/
    ├── index.md
    ├── instalacao.md
    ├── comandos.md
    └── implantacao.md
```

### Geração de Documentação

Usar MkDocs para gerar site de documentação:

```yaml
# mkdocs.yml
site_name: ORYUM STACK CLI
theme: material

nav:
  - Home: 
      - English: en/index.md
      - Português: pt/index.md
  - Installation/Instalação:
      - English: en/installation.md
      - Português: pt/instalacao.md
  - Commands/Comandos:
      - English: en/commands.md
      - Português: pt/comandos.md
  - Deployment/Implantação:
      - English: en/deployment.md
      - Português: pt/implantacao.md

plugins:
  - search
  - i18n:
      default_language: pt
      languages:
        en: English
        pt: Português
```

## Resumo das Recomendações

1. **Versionamento**:
   - Adotar Versionamento Semântico (MAJOR.MINOR.PATCH)
   - Usar GitFlow adaptado para gerenciamento de branches
   - Implementar commits semânticos
   - Manter CHANGELOG.md atualizado

2. **Publicação**:
   - Configurar pyproject.toml adequadamente
   - Publicar no PyPI com twine
   - Automatizar publicação com GitHub Actions

3. **Integração Contínua**:
   - Implementar testes automatizados com pytest
   - Verificar qualidade de código com flake8, black e isort
   - Executar CI em pull requests e branches principais

4. **Deploy de Projetos**:
   - Incluir configurações para Render e Railway
   - Fornecer documentação detalhada de deploy
   - Implementar comandos de verificação e atualização

5. **Documentação**:
   - Manter documentação bilíngue (português e inglês)
   - Usar MkDocs para gerar site de documentação
   - Incluir exemplos práticos e tutoriais

Seguindo estas práticas, a ORYUM STACK CLI terá um ciclo de desenvolvimento robusto, facilitando a manutenção, evolução e adoção por desenvolvedores.
