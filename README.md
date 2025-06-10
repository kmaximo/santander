
# Santander

Santander é um CLI contendo os desafios realizados durante o bootcamp Santander 2025 - Back-End com Python.

Toda a aplicação é baseada em um comando chamado `poetry run santander`.

## Como instalar o projeto

Para instalação do cli do projeto recomendamos que use o `git clone` para fazer essa instalação:

```bash
git clone https://github.com/kmaximo/santander.git
poetry install
poetry shell
```

## Requisitos mínimos

```bash
pip install --user pipx
pipx ensurepath
pipx install poetry
pipx inject poetry poetry-plugin-shell
```


### Sistema Bancário simples

Você pode acessar o sistema usando o comando abaixo e navegar entre as opções disponíveis.

```bash
poetry run santander banco
```

## Mais informações sobre o CLI

Para descobrir outras opções, você pode usar a flag `--help`:

```bash
poetry run santander --help
                                                                       
 Usage: santander.cmd [OPTIONS] COMMAND [ARGS]...

 Forma de uso: santander [SUBCOMANDO] [ARGUMENTOS]
 Existe 1 subcomando disponível para essa aplicação
 - banco: Acessa o sistema bancário simples.
 Exemplos de uso: santander banco # Acessar o sistema bancário
 Para mais informações rápidas: santander --help

╭─ Advanced options ──────────────────────────────────────────────────────────────────────────────────────╮
│ --help     -h    Show this message and exit.                                                            │
│ --version        Show the version and exit.                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Main usage ────────────────────────────────────────────────────────────────────────────────────────────╮
│ banco  Sistema Bancário simples com Python. Permite realizar depósitos, saques e consultar extrato e    │
│        status da conta.                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
