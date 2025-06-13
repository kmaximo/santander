import rich_click as click
from santander.banco import Banco
from santander import __version__

click.rich_click.VERSION = __version__

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

def mostrar_banco_menu_principal():
    """Exibe o menu principal"""
    click.clear()
    click.echo("=" * 40)
    click.echo("Banco Santander".center(40))
    click.echo("=" * 40)
    click.echo("\nMenu Principal:")
    click.echo("1. Cadastrar Usuário")
    click.echo("2. Cadastrar Conta Bancária")
    click.echo("3. Acessar Conta")
    click.echo("4. Listar Todas as Contas")  # Novo item no menu
    click.echo("5. Sair\n")
    return click.prompt("Escolha uma opção", type=int)

def mostrar_banco_menu_conta():
    """Exibe o menu da conta"""
    click.clear()
    click.echo("=" * 40)
    click.echo("MENU DA CONTA".center(40))
    click.echo("=" * 40)
    click.echo("\nOpções disponíveis:")
    click.echo("1. Depositar")
    click.echo("2. Sacar")
    click.echo("3. Extrato")
    click.echo("4. Status da Conta")
    click.echo("5. Voltar ao menu principal\n")
    return click.prompt("Escolha uma opção", type=int)

def cadastrar_usuario(banco):
    """Interface para cadastrar novo usuário"""
    click.echo("\n" + "=" * 40)
    click.echo("CADASTRO DE USUÁRIO".center(40))
    click.echo("=" * 40)
    
    nome = click.prompt("Nome completo")
    data_nascimento = click.prompt("Data de nascimento (DD/MM/AAAA)")
    cpf = click.prompt("CPF (somente números)")
    endereco = click.prompt("Endereço (logradouro, nro - bairro - cidade/UF)")
    
    sucesso, mensagem = banco.cadastrar_usuario(nome, data_nascimento, cpf, endereco)
    emoji = "✅" if sucesso else "❌"
    click.echo(f"\n{emoji} {mensagem}")
    click.pause()

def cadastrar_conta(banco):
    """Interface para cadastrar nova conta"""
    click.echo("\n" + "=" * 40)
    click.echo("CADASTRO DE CONTA".center(40))
    click.echo("=" * 40)
    
    cpf = click.prompt("CPF do usuário (somente números)")
    sucesso, mensagem = banco.cadastrar_conta(cpf)
    
    if sucesso:
        conta = mensagem  # No caso de sucesso, mensagem é o objeto conta
        click.echo("\n✅ Conta cadastrada com sucesso!")
        click.echo(f"\nAgência: {conta.agencia}")
        click.echo(f"Número da conta: {conta.numero_conta}")
        click.echo(f"Titular: {conta.usuario.nome}")
    else:
        click.echo(f"\n❌ {mensagem}")
    
    click.pause()

def listar_contas(banco):
    """Exibe todas as contas cadastradas"""
    contas = banco.listar_contas()
    
    click.echo("\n" + "=" * 40)
    click.echo("CONTAS CADASTRADAS".center(40))
    click.echo("=" * 40)
    
    if not contas:
        click.echo("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            click.echo(f"\nAgência: {conta['agencia']}")
            click.echo(f"Número: {conta['numero_conta']}")
            click.echo(f"Titular: {conta['titular']}")
            click.echo(f"CPF: {conta['cpf_titular']}")
            click.echo(f"Saldo: {conta['saldo']}")
            click.echo("-" * 40)
    
    click.pause()

def acessar_conta(banco):
    """Interface para acessar uma conta"""
    numero_conta = click.prompt("\nNúmero da conta", type=int)
    conta = banco.buscar_conta_por_numero(numero_conta)
    
    if not conta:
        click.echo("\n❌ Conta não encontrada!")
        click.pause()
        return
    
    while True:
        opcao = mostrar_banco_menu_conta()

        if opcao == 1:  # Depositar
            valor = click.prompt("Valor do depósito", type=float)
            sucesso, mensagem = banco.depositar(numero_conta, valor)
            emoji = "✅" if sucesso else "❌"
            click.echo(f"\n{emoji} {mensagem}")
            click.pause()
            
        elif opcao == 2:  # Sacar
            valor = click.prompt("Valor do saque", type=float)
            # Chamada atualizada usando argumentos nomeados
            sucesso, mensagem = banco.sacar(numero_conta=numero_conta, valor=valor)
            emoji = "✅" if sucesso else "❌"
            click.echo(f"\n{emoji} {mensagem}")
            click.pause()
            
        elif opcao == 3:  # Extrato
            extrato, saldo, erro = banco.gerar_extrato(numero_conta, detalhado=True)
            if erro:
                click.echo(f"\n❌ {erro}")
            else:
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
            
        elif opcao == 4:  # Status
            status, erro = banco.obter_status(numero_conta)
            if erro:
                click.echo(f"\n❌ {erro}")
            else:
                click.echo("\n" + "=" * 40)
                click.echo("STATUS DA CONTA".center(40))
                click.echo("=" * 40)
                click.echo(f"Agência: {status['agencia']}")
                click.echo(f"Conta: {status['numero_conta']}")
                click.echo(f"Titular: {status['usuario']}")
                click.echo(f"Saldo: R$ {status['saldo']:.2f}")
                click.echo(f"Saques restantes hoje: {status['saques_restantes']}")
                click.echo(f"Limite por saque: R$ {status['limite_saque']:.2f}")
                click.echo("=" * 40)
            click.pause()
            
        elif opcao == 5:  # Voltar
            break
            
        else:
            click.echo("\n❌ Opção inválida! Tente novamente.")
            click.pause()

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option("1.0.1", prog_name="menu")
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
        opcao = mostrar_banco_menu_principal()

        if opcao == 1:  # Cadastrar usuário
            cadastrar_usuario(banco)
            
        elif opcao == 2:  # Cadastrar conta
            cadastrar_conta(banco)
            
        elif opcao == 3:  # Acessar conta
            acessar_conta(banco)
            
        elif opcao == 4:  # Listar contas (nova opção)
            listar_contas(banco)
            
        elif opcao == 5:  # Sair
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