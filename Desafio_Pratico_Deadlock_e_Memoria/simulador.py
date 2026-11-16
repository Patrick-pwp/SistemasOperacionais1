# Desafio pratico de Sistemas Operacionais: deadlock e gerenciamento de memoria.
# Para executar: python simulador.py

import deadlock
import memoria


def ler_paginas():
    texto = input("Digite as paginas separadas por espaco: ")
    try:
        paginas = [int(v) for v in texto.split()]
    except ValueError:
        print("Use apenas numeros inteiros.")
        return None
    if not paginas:
        print("Digite pelo menos uma pagina.")
        return None
    return paginas


def ler_inteiro(pergunta, minimo=1):
    try:
        valor = int(input(pergunta))
    except ValueError:
        print("Digite um numero inteiro.")
        return None
    if valor < minimo:
        print(f"O valor minimo e {minimo}.")
        return None
    return valor


def menu_deadlock():
    print("\nCenarios de deadlock")
    for chave, (nome, _) in deadlock.CENARIOS.items():
        print(f"  {chave} - {nome}")
    escolha = input("Escolha: ").strip()
    if escolha not in deadlock.CENARIOS:
        print("Opcao invalida.")
        return
    processos, recursos = deadlock.CENARIOS[escolha][1]()
    print("\nProcessos e o que cada um pede (nessa ordem):")
    for p in processos:
        print(f"  {p.nome}: {' depois '.join(p.pedidos)}")
    deadlock.simular(processos, recursos)


def menu_substituicao():
    paginas = ler_paginas()
    if paginas is None:
        return
    frames = ler_inteiro("Digite a quantidade de frames: ")
    if frames is None:
        return
    print("\nSequencia:", paginas)
    print("Frames:", frames)
    memoria.comparar(paginas, frames)


def menu_belady():
    print("Enter sem digitar nada usa a sequencia classica 1 2 3 4 1 2 5 1 2 3 4 5")
    texto = input("Digite as paginas separadas por espaco: ").strip()
    if texto == "":
        paginas = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    else:
        try:
            paginas = [int(v) for v in texto.split()]
        except ValueError:
            print("Use apenas numeros inteiros.")
            return
    maximo = ler_inteiro("Ate quantos frames comparar? ", minimo=2)
    if maximo is None:
        return
    memoria.analisar_belady(paginas, maximo)


def main():
    while True:
        print("\nSimulador de Sistemas Operacionais")
        print("1 - Deadlock")
        print("2 - FIFO e LRU")
        print("3 - Anomalia de Belady")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            menu_deadlock()
        elif opcao == "2":
            menu_substituicao()
        elif opcao == "3":
            menu_belady()
        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
