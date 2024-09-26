import locale
from colorama import init, Fore, Style
init()
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
INFO = Fore.CYAN
WARNING = Fore.YELLOW
SUCCESS = Fore.GREEN
DANGER = Fore.RED
RESET = Style.RESET_ALL

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_extrato(transacao: str, valor: float) -> str:
    return f"{transacao}: {locale.currency(valor, grouping=True)}\n"

def regras_negocio(valor: float, saldo: float, limite: float, numero_saques: int):
    return {
        "excedeu_saldo": valor > saldo,
        "excedeu_limite": valor > limite,
        "excedeu_saques": numero_saques >= LIMITE_SAQUES,
        "valor_positivo": valor > 0
    }

def realizar_transacao(opcao: str, valor: float):
    global saldo, extrato, numero_saques, limite

    resultado_regras = regras_negocio(valor, saldo, limite, numero_saques)

    if opcao == "d":
        if resultado_regras["valor_positivo"]:
            saldo += valor
            extrato += formatar_extrato("Depósito", valor)
            print(f"{SUCCESS}Depósito realizada com sucesso! Valor: {locale.currency(valor, grouping=True)}.{RESET}")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        if resultado_regras["excedeu_saldo"]:
            print(f"{DANGER}Operação falhou! Você não tem saldo suficiente.{RESET}")
        elif resultado_regras["excedeu_limite"]:
            print(f"{DANGER}Operação falhou! O valor do saque excede o limite de {locale.currency(limite, grouping=True)}.{RESET}")
        elif resultado_regras["excedeu_saques"]:
            print(f"{DANGER}Operação falhou! Número máximo de saques excedido.{RESET}")
        elif resultado_regras["valor_positivo"]:
            saldo -= valor
            extrato += formatar_extrato("Saque", valor)
            numero_saques += 1
            print(f"{SUCCESS}Saque realizada com sucesso! Valor: {locale.currency(valor, grouping=True)}.{RESET}")
        else:
            print(f"{DANGER}Operação falhou! O valor informado é inválido.{RESET}")
while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input(f"{INFO}Informe o valor do depósito: {RESET}"))
        realizar_transacao("d", valor)

    elif opcao == "s":
        valor = float(input(f"{INFO}Informe o valor do saque: {RESET}"))
        realizar_transacao("s", valor)

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: {locale.currency(saldo, grouping=True)}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print(f"{WARNING}Operação inválida, por favor selecione novamente a operação desejada.{RESET}")
