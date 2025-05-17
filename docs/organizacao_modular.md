# Organização Modular e Fluxo de Geração do ORYUM STACK CLI

## Estrutura do Projeto CLI

A ORYUM STACK CLI será organizada de forma modular para facilitar a manutenção, expansão e personalização. Abaixo está a estrutura de diretórios proposta para o projeto da CLI:

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
│   │   │   ├── cookiecutter.json
│   │   │   └── {{cookiecutter.project_name}}/
│   │   │       ├── .env.example
│   │   │       ├── config.py
│   │   │       ├── settings.py
│   │   │       ├── run.py
│   │   │       ├── init_db.py
│   │   │       ├── requirements.txt
│   │   │       ├── models/
│   │   │       ├── routes/
│   │   │       ├── static/
│   │   │       └── templates/
│   │   ├── model/                # Template para geração de models
│   │   │   ├── cookiecutter.json
│   │   │   └── {{cookiecutter.model_name}}.py
│   │   └── route/                # Template para geração de rotas
│   │       ├── cookiecutter.json
│   │       └── {{cookiecutter.route_name}}.py
│   └── utils/                    # Utilitários gerais
│       ├── __init__.py
│       ├── file_operations.py    # Operações de arquivo
│       ├── validators.py         # Validadores de entrada
│       └── i18n.py               # Internacionalização
├── tests/                        # Testes automatizados
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_new_command.py
│   └── test_make_commands.py
└── docs/                         # Documentação detalhada
    ├── en/                       # Documentação em inglês
    └── pt/                       # Documentação em português
```

## Fluxo de Geração de Projetos

O fluxo de geração de projetos será implementado através da integração entre Typer e Cookiecutter, seguindo estas etapas:

1. **Invocação do Comando**: O usuário executa `oryum new meu_projeto [opções]`

2. **Processamento de Argumentos**: O Typer processa os argumentos e opções fornecidos

3. **Validação**: Verificação de nome do projeto, diretório de destino e opções

4. **Preparação do Contexto**: Criação de um contexto para o Cookiecutter com base nos argumentos e opções

5. **Geração da Estrutura**: Invocação do Cookiecutter com o template apropriado

6. **Personalização Pós-Geração**: Aplicação de modificações específicas com base nas opções (ex: OAuth, tipo de banco de dados)

7. **Instalação de Dependências**: Instalação automática dos pacotes necessários via pip

8. **Inicialização do Banco de Dados**: Execução do script init_db.py para configurar o banco de dados inicial

9. **Instruções Finais**: Exibição de mensagens de sucesso e próximos passos para o usuário

### Exemplo de Implementação do Comando Principal

```python
# oryum_stack/cli.py
import typer
from typing import Optional
from pathlib import Path
from oryum_stack.commands import new, make_model, make_route
from oryum_stack.utils.i18n import translate as _

app = typer.Typer(
    name="oryum",
    help=_("Ferramenta de linha de comando para criação de projetos Flask com autenticação e painel admin")
)

# Registrar comandos
app.add_typer(new.app, name="new")
app.command()(make_model.make_model)
app.command()(make_route.make_route)

if __name__ == "__main__":
    app()
```

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

## Estrutura do Projeto Gerado

O projeto Flask gerado pela CLI terá a seguinte estrutura:

```
meu_projeto/
├── .env                      # Variáveis de ambiente (gerado a partir de .env.example)
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
│   ├── auth.py               # Rotas de autenticação (login, registro, etc.)
│   ├── admin.py              # Rotas do painel administrativo
│   └── main.py               # Rotas principais do site
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   ├── bootstrap.min.css # Bootstrap 5
│   │   └── custom.css        # Estilos personalizados
│   ├── js/
│   │   ├── bootstrap.bundle.min.js
│   │   ├── cropper.min.js    # Cropper.js para edição de imagens
│   │   └── custom.js         # JavaScript personalizado
│   └── img/
│       └── default-avatar.png
└── templates/                # Templates HTML
    ├── base.html             # Template base
    ├── auth/
    │   ├── login.html
    │   ├── register.html
    │   └── profile.html
    ├── admin/
    │   ├── dashboard.html
    │   ├── users.html
    │   └── settings.html
    └── main/
        ├── index.html
        └── about.html
```

## Sistema de Configuração YAML

A CLI suportará personalização via arquivo YAML, permitindo que os usuários definam suas próprias configurações padrão. O arquivo será buscado em:

1. Diretório atual: `./oryum.yaml`
2. Diretório home do usuário: `~/.oryum/config.yaml`

Exemplo de arquivo de configuração YAML:

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
      nullable: false
    - name: password
      type: String
      nullable: false
    - name: role
      type: String
      default: "user"
    - name: profile_image
      type: String
      nullable: true
      
templates:
  use_bootstrap: true
  responsive: true
  language: pt-br
  
admin:
  dashboard_widgets:
    - users_count
    - recent_activities
    - system_status
```

## Internacionalização (i18n)

Para suportar documentação e mensagens bilíngues, a CLI utilizará um sistema simples de internacionalização:

```python
# oryum_stack/utils/i18n.py
import os

# Dicionários de tradução
TRANSLATIONS = {
    'pt': {
        'creating_project': 'Criando projeto: {0}',
        'installing_dependencies': 'Instalando dependências...',
        # ... mais traduções
    },
    'en': {
        'creating_project': 'Creating project: {0}',
        'installing_dependencies': 'Installing dependencies...',
        # ... mais traduções
    }
}

# Detectar idioma do sistema ou usar variável de ambiente
def get_language():
    return os.environ.get('ORYUM_LANG', 'pt')

# Função de tradução
def translate(key, lang=None):
    lang = lang or get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
```

## Extensibilidade

A CLI será projetada para ser facilmente extensível:

1. **Plugins**: Sistema de plugins para adicionar novos comandos ou funcionalidades

2. **Templates Personalizados**: Suporte para templates Cookiecutter personalizados

3. **Hooks**: Pontos de extensão em diferentes etapas do processo de geração

4. **Configuração Flexível**: Capacidade de sobrescrever qualquer configuração padrão

Esta arquitetura modular permitirá que a ORYUM STACK CLI evolua com o tempo, adicionando novas funcionalidades e adaptando-se às necessidades dos usuários, mantendo a compatibilidade com versões anteriores.
