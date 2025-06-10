import rich_click as click
import os
from santander.banco import Banco


USER = os.getlogin()

click.rich_click.OPTION_GROUPS = {
    "cli": [
        {
            "name": "Basic usage",
            "options": ["--type", "--output"],
        },
        {
            "name": "Advanced options",
            "options": ["--help", "--version"],
            "table_styles": {
                "row_styles": ["bold", "yellow", "cyan"],
            },
        },
    ],
    "cli banco": [
        {
            "name": "Inputs and outputs",
            "options": ["--input", "--output"],
        },
        {
            "name": "Advanced usage",
            "options": ["--overwrite", "--all", "--help"],
        },
    ],
}
click.rich_click.COMMAND_GROUPS = {
    "cli": [
        {
            "name": "Main usage",
            "commands": ["banco", "proximo"],
        }
    ]
}

def mostrar_banco_menu():
    """Exibe o menu de opções"""
    click.clear()
    click.echo("=" * 40)
    click.echo("SISTEMA BANCÁRIO".center(40))
    click.echo("=" * 40)
    click.echo(f"Bem-vindo {USER}!".center(40))
    click.echo("=" * 40)
    click.echo("\nOpções disponíveis:")
    click.echo("1. Depositar")
    click.echo("2. Sacar")
    click.echo("3. Extrato")
    click.echo("4. Status da Conta")
    click.echo("5. Sair\n")
    return click.prompt("Escolha uma opção", type=int)

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option("1.0.0", prog_name="menu")
def cli():
    """
    Forma de uso: santander [SUBCOMANDO] [ARGUMENTOS]

    Existe 1 subcomando disponível para essa aplicação

    - banco: Acessa o sistema bancário simples.

    Exemplos de uso:
    santander banco # Acessar o sistema bancário

    Para mais informações rápidas: santander --help
    """
    pass


@cli.group(invoke_without_command=True)
def banco():
    """
    Sistema Bancário simples com Python.
    Permite realizar depósitos, saques e consultar extrato e status da conta.
    """
    banco = Banco()  # Instancia o banco
    
    while True:
        opcao = mostrar_banco_menu()

        if opcao == 1:
            valor = click.prompt("Valor do depósito", type=float)
            sucesso, mensagem = banco.depositar(valor)
            emoji = "✅" if sucesso else "❌"
            click.echo(f"\n{emoji} {mensagem}")
            click.pause()
            
        elif opcao == 2:
            valor = click.prompt("Valor do saque", type=float)
            sucesso, mensagem = banco.sacar(valor)
            emoji = "✅" if sucesso else "❌"
            click.echo(f"\n{emoji} {mensagem}")
            click.pause()
            
        elif opcao == 3:
            extrato, saldo = banco.gerar_extrato()
            click.echo("\n" + "=" * 40)
            click.echo("EXTRATO BANCÁRIO".center(40))
            click.echo("=" * 40)
            
            if not extrato:
                click.echo("Nenhuma movimentação registrada.")
            else:
                for movimento in extrato:
                    click.echo(movimento)
            
            click.echo("\n" + "-" * 40)
            click.echo(f"Saldo atual: R$ {saldo:.2f}".rjust(40))
            click.echo("=" * 40)
            click.pause()
            
        elif opcao == 4:
            status = banco.obter_status()
            click.echo("\n" + "=" * 40)
            click.echo("STATUS DA CONTA".center(40))
            click.echo("=" * 40)
            click.echo(f"Saldo: R$ {status['saldo']:.2f}")
            click.echo(f"Saques restantes hoje: {status['saques_restantes']}")
            click.echo(f"Limite por saque: R$ {status['limite_saque']:.2f}")
            click.echo("=" * 40)
            click.pause()
            
        elif opcao == 5:
            click.echo("\nObrigado por usar nosso sistema bancário!")
            break
            
        else:
            click.echo("\n❌ Opção inválida! Tente novamente.")
            click.pause()







# @cli.command()
# @click.option("--all", is_flag=True, help="Get everything")
# def download(all):
#     """Pretend to download some files from somewhere."""
#     click.echo(f"Seja bem-vindo, {USER}!")


# @cli.command()
# def auth():
#     """Authenticate the app."""
#     click.echo(f"Seja bem-vindo, {USER}!")


# @cli.command()
# def config():
#     """Set up the configuration."""
#     click.echo(f"Seja bem-vindo, {USER}!")


if __name__ == "__main__":
    cli()