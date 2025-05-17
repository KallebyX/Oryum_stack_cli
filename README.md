# Oryum Stack CLI

[![PyPI Version](https://img.shields.io/pypi/v/oryum-stack-cli?logo=pypi)](https://pypi.org/project/oryum-stack-cli)
[![Build Status](https://github.com/KallebyX/Oryum_stack_cli/actions/workflows/tests.yml/badge.svg)](https://github.com/KallebyX/Oryum_stack_cli/actions)
[![Coverage Status](https://img.shields.io/codecov/c/gh/KallebyX/Oryum_stack_cli?logo=codecov)](https://codecov.io/gh/KallebyX/Oryum_stack_cli)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Ferramenta de linha de comando para geração rápida de projetos Flask com:

* Estrutura profissional de pastas (`app.py`, `models/`, `routes/`, `templates/`)
* Autenticação via Flask-Login e SQLAlchemy
* Comandos para criar modelos, rotas, APIs e formulários

---

## 🚀 Visão Geral

O **Oryum Stack CLI** acelera a criação de aplicações Flask, fornecendo um *scaffold* completo e personalizável. Ideal para iniciantes e equipes que buscam padronização e produtividade.

---

## 📦 Instalação

```bash
pip install oryum-stack-cli
```

Para testar a versão mais recente via TestPyPI:

```bash
pip install -i https://test.pypi.org/simple oryum-stack-cli
```

---

## ⚙️ Uso Básico

```bash
# Ver ajuda geral
o ryum --help

# Criar um novo projeto Flask
o ryum new meu_projeto

# Criar um modelo SQLAlchemy
o ryum make:model Produto --fields "nome:string,preco:float"
```

---

## 📑 Comandos Disponíveis

| Comando                   | Descrição                                              |
| ------------------------- | ------------------------------------------------------ |
| `oryum new <nome>`        | Gera estrutura inicial de projeto Flask                |
| `oryum make:model <Nome>` | Cria modelo SQLAlchemy (campo\:tipo, timestamps, rel.) |
| `oryum make:route <Nome>` | Gera arquivo de rota em `routes/`                      |
| `oryum make:api <Nome>`   | Cria blueprint RESTful em `api/`                       |
| `oryum make:form <Nome>`  | Gera classe WTForms e template em `forms/`             |

---

## 🧩 Templates e Snippets

Todos os templates estão em:

```
oryum_stack/cli/templates/
```

* **project/**: scaffold de projeto
* **snippets/**: geradores de código para modelos, rotas, APIs e formulários

---

## 🧪 Testes e CI

O projeto inclui testes automáticos com `pytest`:

```bash
pytest tests/
```

A integração contínua com GitHub Actions executa os testes a cada push.

---

## 🤝 Contribuição

1. Faça um *fork* do repositório
2. Crie uma *branch* para sua feature (`git checkout -b feature/foo`)
3. Implemente e documente sua feature
4. Abra um *pull request*

---

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
