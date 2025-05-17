# Plano Técnico de Implementação da ORYUM STACK CLI

## Sumário Executivo

Este documento apresenta um plano técnico completo para o desenvolvimento da ORYUM STACK CLI, uma ferramenta de linha de comando para geração automática de projetos Flask com autenticação, painel administrativo e estrutura modular. A análise abrange escolha de tecnologias, arquitetura, organização de código, práticas de desenvolvimento e estratégias de distribuição.

## Índice

1. [Visão Geral](#visão-geral)
2. [Frameworks e Bibliotecas](#frameworks-e-bibliotecas)
3. [Arquitetura e Organização Modular](#arquitetura-e-organização-modular)
4. [Fluxo de Geração de Projetos](#fluxo-de-geração-de-projetos)
5. [Versionamento e Deploy](#versionamento-e-deploy)
6. [Estratégia de Distribuição](#estratégia-de-distribuição)
7. [Exemplos de Código](#exemplos-de-código)
8. [Próximos Passos](#próximos-passos)

## Visão Geral

A ORYUM STACK CLI será uma ferramenta instalável via pip que permitirá aos desenvolvedores criar rapidamente projetos Flask completos com:

- Sistema de autenticação (cadastro, login, logout)
- Diferenciação de perfis de usuário
- Painel administrativo com dashboard e CRUD
- Upload e edição de imagens de perfil
- Estrutura modular e organizada
- Suporte a múltiplos bancos de dados
- Comandos para geração de código

A ferramenta seguirá princípios de design que priorizam:
- Produtividade do desenvolvedor
- Código de alta qualidade e manutenível
- Flexibilidade e personalização
- Documentação bilíngue (português e inglês)

## Frameworks e Bibliotecas

### Framework CLI Principal

Após análise comparativa detalhada, recomendamos o uso de **Typer** como framework principal para a CLI, pelos seguintes motivos:

- Sintaxe moderna e intuitiva com suporte a type hints
- Código mais conciso e limpo que alternativas
- Excelente suporte para subcomandos (essencial para `oryum new`, `oryum make:model`, etc.)
- Autocompleção de shell integrada
- Desenvolvido pelo criador do FastAPI, com documentação de qualidade

### Motor de Templates

Para a geração de estrutura de projetos, recomendamos **Cookiecutter**:

- Especializado em scaffolding de projetos
- Sistema robusto de templates com Jinja2
- Grande ecossistema e comunidade ativa
- Suporte a prompts interativos e personalização

### Bibliotecas para Projetos Gerados

Os projetos gerados pela CLI utilizarão:

1. **Framework Web**:
   - Flask (core)
   - Flask-Blueprints (organização modular)

2. **Autenticação**:
   - Flask-Login (autenticação básica)
   - Flask-Dance (OAuth com Google)
   - Flask-Security (opcional, para recursos avançados)

3. **ORM e Banco de Dados**:
   - SQLAlchemy (ORM)
   - Flask-SQLAlchemy (integração)
   - Flask-Migrate (migrações)
   - Suporte a SQLite e PostgreSQL

4. **Frontend**:
   - Bootstrap 5 (framework CSS responsivo)
   - Cropper.js (edição de imagens)
   - Flask-WTF (formulários)

5. **Configuração e Ambiente**:
   - python-dotenv (variáveis de ambiente)
   - Flask-Env (configurações por ambiente)

6. **Utilitários**:
   - Pillow (manipulação de imagens)
   - Flask-Admin (painel administrativo)

## Arquitetura e Organização Modular

### Estrutura da CLI

```
oryum-stack/
├── pyproject.toml                # Configuração do pacote Python
├── README.md                     # Documentação principal (bilíngue)
├── CHANGELOG.md                  # Registro de alterações
├── LICENSE                       # Licença do projeto
├── oryum_stack/                  # Pacote principal
│   ├── __init__.py               # Inicialização do pacote
│   ├── __main__.py               # Ponto de entrada para execução direta
│   ├── cli.py                    # Definição principal da CLI com Typer
│   ├── commands/                 # Módulos de comandos
│   │   ├── __init__.py
│   │   ├── new.py                # Comando 'oryum new'
│   │   ├── make_model.py         # Comando 'oryum make:model'
│   │   ├── make_route.py         # Comando 'oryum make:route'
│   │   └── utils.py              # Funções utilitárias para comandos
│   ├── config/                   # Gerenciamento de configuração
│   │   ├── __init__.py
│   │   ├── yaml_parser.py        # Parser para arquivos YAML
│   │   └── defaults.py           # Configurações padrão
│   ├── templates/                # Templates Cookiecutter
│   │   ├── project/              # Template para projeto completo
│   │   ├── model/                # Template para geração de models
│   │   └── route/                # Template para geração de rotas
│   └── utils/                    # Utilitários gerais
│       ├── __init__.py
│       ├── file_operations.py    # Operações de arquivo
│       ├── validators.py         # Validadores de entrada
│       └── i18n.py               # Internacionalização
├── tests/                        # Testes automatizados
└── docs/                         # Documentação detalhada
    ├── en/                       # Documentação em inglês
    └── pt/                       # Documentação em português
```

### Estrutura do Projeto Gerado

```
meu_projeto/
├── .env                      # Variáveis de ambiente
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore                # Configuração do Git
├── config.py                 # Configurações do aplicativo
├── settings.py               # Configurações específicas de ambiente
├── run.py                    # Script para executar o aplicativo
├── init_db.py                # Script para inicializar o banco de dados
├── requirements.txt          # Dependências do projeto
├── models/                   # Modelos de dados
│   ├── __init__.py
│   ├── base.py               # Classe base para modelos
│   └── user.py               # Modelo de usuário com autenticação
├── routes/                   # Rotas e controllers
│   ├── __init__.py           # Registro de blueprints
│   ├── auth.py               # Rotas de autenticação
│   ├── admin.py              # Rotas do painel administrativo
│   └── main.py               # Rotas principais do site
├── static/                   # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
└── templates/                # Templates HTML
    ├── base.html             # Template base
    ├── auth/
    ├── admin/
    └── main/
```

## Fluxo de Geração de Projetos

### Processo de Geração

1. **Invocação do Comando**: 
   ```bash
   pip install oryum-stack
   oryum new meu_projeto
   cd meu_projeto
   flask run
   ```

2. **Fluxo Interno**:
   - Processamento de argumentos e opções
   - Validação de nome e diretório
   - Preparação do contexto para Cookiecutter
   - Geração da estrutura base
   - Personalização com base nas opções
   - Instalação de dependências
   - Inicialização do banco de dados
   - Exibição de instruções finais

### Comandos Principais

1. **Criação de Projeto**:
   ```bash
   oryum new meu_projeto [opções]
   ```
   Opções:
   - `--db-type`: sqlite ou postgresql (padrão: sqlite)
   - `--with-oauth`: incluir autenticação Google (padrão: false)
   - `--with-premium`: incluir sistema de assinatura (padrão: false)

2. **Geração de Modelo**:
   ```bash
   oryum make:model Usuario
   ```
   Opções:
   - `--fields`: campos do modelo (ex: "nome:string,email:string,idade:integer")
   - `--timestamps`: incluir created_at e updated_at (padrão: true)

3. **Geração de Rotas**:
   ```bash
   oryum make:route produto
   ```
   Opções:
   - `--crud`: gerar operações CRUD completas (padrão: true)
   - `--api`: gerar endpoints API RESTful (padrão: false)

### Sistema de Configuração YAML

A CLI suportará personalização via arquivo YAML:

```yaml
# oryum.yaml
project:
  default_db: postgresql
  default_port: 5000
  
user_model:
  table_name: users
  fields:
    - name: name
      type: String
      nullable: false
    - name: email
      type: String
      unique: true
    - name: password
      type: String
    - name: role
      type: String
      default: "user"
    - name: profile_image
      type: String
      nullable: true
```

## Versionamento e Deploy

### Versionamento Semântico

A ORYUM STACK CLI seguirá o Versionamento Semântico (SemVer):

- **MAJOR**: Mudanças incompatíveis com versões anteriores
- **MINOR**: Novas funcionalidades com compatibilidade mantida
- **PATCH**: Correções de bugs com compatibilidade mantida

### Controle de Versão

- **Modelo de Branches**: GitFlow adaptado
  - `main`: Código estável de produção
  - `develop`: Desenvolvimento da próxima versão
  - `feature/xxx`: Novas funcionalidades
  - `bugfix/xxx`: Correções de bugs
  - `release/x.y.z`: Preparação de releases

- **Commits Semânticos**:
  ```
  <tipo>(<escopo>): <descrição>
  ```
  Exemplos:
  - `feat(make:model): adiciona suporte para relacionamentos`
  - `fix(auth): corrige validação de senha`

### Publicação no PyPI

1. **Configuração do pyproject.toml**:
   ```toml
   [build-system]
   requires = ["setuptools>=42", "wheel"]
   build-backend = "setuptools.build_meta"

   [project]
   name = "oryum-stack"
   version = "1.0.0"
   description = "CLI para criação de projetos Flask com autenticação e painel admin"
   # ...
   ```

2. **Automação com GitHub Actions**:
   - Testes automatizados em pull requests
   - Publicação automática no PyPI em novas tags
   - Verificação de qualidade de código

### Deploy de Projetos Gerados

Os projetos gerados incluirão configurações para deploy em:

1. **Render**:
   - Arquivo `render.yaml` com configurações
   - Suporte a PostgreSQL gerenciado

2. **Railway**:
   - Arquivo `railway.json` com configurações
   - Integração com CLI do Railway

## Estratégia de Distribuição

Após análise comparativa entre modelos público e privado, recomendamos a **Abordagem Open Core**:

- **Core CLI e templates básicos**: Open Source (GitHub público)
- **Templates premium e plugins avançados**: Pagos

### Justificativa

1. **Alinhamento com necessidades atuais**: Resolve o problema imediato de repetição de código em projetos internos, mas permite evolução para produto.

2. **Flexibilidade estratégica**: Permite começar com código aberto e gradualmente desenvolver componentes premium.

3. **Benefícios de marketing**: Estabelece a Oryum Tech como referência em ferramentas de desenvolvimento no Brasil.

4. **Potencial educacional**: Facilita a adoção em cursos e treinamentos.

5. **Monetização progressiva**: Permite testar diferentes estratégias de monetização sem comprometer a adoção inicial.

### Implementação

```
# Versão gratuita
pip install oryum-stack
oryum new meu_projeto

# Recursos premium
pip install oryum-stack-premium  # Requer licença/login
oryum new meu_projeto --template=saas-completo
```

## Exemplos de Código

### Exemplo 1: Definição da CLI Principal

```python
# oryum_stack/cli.py
import typer
from typing import Optional
from oryum_stack import __version__
from oryum_stack.commands import new, make_model, make_route
from oryum_stack.utils.i18n import translate as _

app = typer.Typer(
    name="oryum",
    help=_("Ferramenta para criação de projetos Flask com autenticação e painel admin")
)

# Registrar comandos
app.add_typer(new.app, name="new")
app.command(name="make:model")(make_model.make_model)
app.command(name="make:route")(make_route.make_route)

@app.callback()
def main(version: bool = typer.Option(False, "--version", "-v", help=_("Mostrar versão"))):
    """
    ORYUM STACK CLI: Gerador de projetos Flask com autenticação e painel admin.
    """
    if version:
        typer.echo(f"ORYUM STACK CLI v{__version__}")
        raise typer.Exit()

if __name__ == "__main__":
    app()
```

### Exemplo 2: Comando de Criação de Projeto

```python
# oryum_stack/commands/new.py
import typer
import os
from pathlib import Path
from cookiecutter.main import cookiecutter
from oryum_stack.utils.i18n import translate as _
from oryum_stack.config.defaults import DEFAULT_CONFIG

app = typer.Typer(help=_("Criar um novo projeto Flask"))

@app.callback(invoke_without_command=True)
def new(
    project_name: str,
    db_type: str = typer.Option("sqlite", help=_("Tipo de banco de dados (sqlite/postgresql)")),
    with_oauth: bool = typer.Option(False, help=_("Incluir autenticação OAuth com Google")),
    with_premium: bool = typer.Option(False, help=_("Incluir sistema de assinatura premium")),
    output_dir: Path = typer.Option(
        os.getcwd(), help=_("Diretório onde o projeto será criado")
    ),
):
    """
    Cria um novo projeto Flask com autenticação e painel admin.
    """
    typer.echo(_("Criando projeto: {0}").format(project_name))
    
    # Preparar contexto para o Cookiecutter
    context = {
        "project_name": project_name,
        "db_type": db_type,
        "with_oauth": "y" if with_oauth else "n",
        "with_premium": "y" if with_premium else "n",
    }
    
    # Caminho para o template
    template_path = Path(__file__).parent.parent / "templates" / "project"
    
    # Executar Cookiecutter
    result_path = cookiecutter(
        str(template_path),
        extra_context=context,
        output_dir=str(output_dir),
        no_input=True
    )
    
    # Instalação de dependências
    typer.echo(_("Instalando dependências..."))
    os.chdir(result_path)
    os.system("pip install -r requirements.txt")
    
    # Inicializar banco de dados
    typer.echo(_("Inicializando banco de dados..."))
    os.system("python init_db.py")
    
    typer.echo(_("Projeto criado com sucesso em: {0}").format(result_path))
    typer.echo(_("Para executar o projeto:"))
    typer.echo(f"cd {project_name}")
    typer.echo("flask run")
```

### Exemplo 3: Modelo de Usuário Gerado

```python
# {{cookiecutter.project_name}}/models/user.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base import Base, db

class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200))
    role = Column(String(20), default='user')  # admin, user, etc.
    profile_image = Column(String(200), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    {% if cookiecutter.with_oauth == 'y' %}
    # OAuth fields
    google_id = Column(String(100), nullable=True, unique=True)
    {% endif %}
    
    {% if cookiecutter.with_premium == 'y' %}
    # Premium fields
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)
    {% endif %}
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email}>'
```

## Próximos Passos

1. **Desenvolvimento do MVP**:
   - Implementar estrutura básica da CLI
   - Criar templates Cookiecutter para projeto, models e routes
   - Desenvolver sistema de internacionalização

2. **Testes e Validação**:
   - Testar em projetos internos da Oryum
   - Coletar feedback e refinar

3. **Preparação para Lançamento**:
   - Finalizar documentação bilíngue
   - Configurar CI/CD e publicação no PyPI
   - Preparar repositório GitHub

4. **Estratégia de Longo Prazo**:
   - Definir roadmap de recursos premium
   - Estabelecer métricas de sucesso
   - Planejar estratégia de marketing

---

Este plano técnico fornece uma base sólida para o desenvolvimento da ORYUM STACK CLI, alinhando-se com os objetivos de produtividade, reutilização e padronização da Oryum Tech. A abordagem modular e a estratégia Open Core oferecem flexibilidade para evolução futura, seja como ferramenta interna ou produto comercial.
