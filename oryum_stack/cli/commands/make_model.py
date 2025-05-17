"""
ORYUM STACK CLI - Comando para criar modelo
"""
import typer
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from oryum_stack.utils.i18n import translate as _
from oryum_stack.utils.console import console, success, info, error
from oryum_stack.utils.project import is_oryum_project, get_project_root
from oryum_stack.utils.parsers import parse_fields, parse_relationships

def make_model(
    name: str = typer.Argument(..., help=_("Nome do modelo")),
    fields: str = typer.Option(
        None,
        "--fields", "-f",
        help=_("Lista de campos no formato 'nome:tipo:modificadores' (ex: 'titulo:string:nullable,preco:float')")
    ),
    timestamps: bool = typer.Option(
        True,
        "--timestamps/--no-timestamps",
        help=_("Incluir campos created_at e updated_at")
    ),
    relationships: str = typer.Option(
        None,
        "--relationships", "-r",
        help=_("Lista de relacionamentos no formato 'nome:Modelo:tipo' (ex: 'categorias:Categoria:many')")
    ),
):
    """
    Cria um novo modelo SQLAlchemy.
    """
    with console.status(_(f"Gerando modelo: {name}")):
        try:
            # Verificar se estamos em um projeto Oryum
            if not is_oryum_project():
                error(_("Este comando deve ser executado dentro de um projeto Oryum."))
                raise typer.Exit(code=1)

            # Obter raiz do projeto como Path
            project_root = Path(get_project_root())

            # Processar nome do modelo
            model_name = name.strip()
            if not model_name[0].isupper():
                model_name = model_name[0].upper() + model_name[1:]

            model_file = model_name.lower() + ".py"
            model_path = project_root / "models" / model_file

            # Verificar se o modelo já existe
            if model_path.exists():
                error(_(f"O modelo {model_name} já existe em {model_path}"))
                raise typer.Exit(code=1)

            # Processar campos e relacionamentos
            parsed_fields = parse_fields(fields) if fields else []
            parsed_relationships = parse_relationships(relationships) if relationships else []

            # Carregar template
            snippets_dir = Path(__file__).parent.parent / "templates" / "snippets"
            env = Environment(loader=FileSystemLoader(snippets_dir))
            template = env.get_template("model.py.jinja2")

            # Renderizar e escrever o arquivo
            model_content = template.render(
                model_name=model_name,
                fields=parsed_fields,
                timestamps=timestamps,
                relationships=parsed_relationships,
            )
            with open(model_path, "w", encoding="utf-8") as f:
                f.write(model_content)

            # Atualizar __init__.py
            init_path = project_root / "models" / "__init__.py"
            with open(init_path, "a", encoding="utf-8") as f:
                f.write(f"\nfrom .{model_name.lower()} import {model_name}")

        except typer.Exit:
            # Preserve intentional exits
            raise
        except Exception as e:
            error(_(f"Erro ao criar modelo: {e}"))
            raise typer.Exit(code=1)

        # Se chegamos aqui, foi bem-sucedido
        success(_(f"Modelo criado com sucesso: {model_path}"))
        raise typer.Exit(code=0)