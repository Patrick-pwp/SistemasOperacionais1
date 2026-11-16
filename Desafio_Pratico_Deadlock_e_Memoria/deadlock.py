# Simulador de deadlock.
# Cada processo precisa de uma lista de recursos, que ele pede um de cada vez,
# na ordem da lista. Cada recurso tem uma unica instancia.


class Processo:
    def __init__(self, nome, pedidos):
        self.nome = nome
        self.pedidos = pedidos   # recursos que o processo precisa, na ordem do pedido
        self.possui = []         # recursos que ele ja conseguiu

    def terminou(self):
        return len(self.possui) == len(self.pedidos)

    def proximo_pedido(self):
        if self.terminou():
            return None
        return self.pedidos[len(self.possui)]


def simular(processos, recursos, mostrar=True):
    """Roda rodadas ate todos terminarem ou ninguem conseguir andar.
    Devolve o resultado com os processos que ficaram em deadlock."""
    donos = {r: None for r in recursos}   # quem esta com cada recurso
    rodada = 0

    while True:
        pendentes = [p for p in processos if not p.terminou()]
        if not pendentes:
            if mostrar:
                print("\nTodos os processos terminaram. Nao houve deadlock.")
            return {"deadlock": False, "ciclo": [], "bloqueados": []}

        rodada += 1
        if mostrar:
            print(f"\nRodada {rodada}")

        houve_progresso = False
        for p in pendentes:
            r = p.proximo_pedido()
            if donos[r] is None:
                donos[r] = p.nome
                p.possui.append(r)
                houve_progresso = True
                if mostrar:
                    print(f"  {p.nome} pegou {r}")
                if p.terminou():
                    # quando consegue tudo, o processo usa e libera os recursos
                    for x in p.possui:
                        donos[x] = None
                    if mostrar:
                        print(f"  {p.nome} terminou e liberou {', '.join(p.possui)}")
            else:
                if mostrar:
                    print(f"  {p.nome} quer {r}, mas {donos[r]} esta com ele (espera)")

        if not houve_progresso:
            break

    # ninguem avancou e ainda tem processo pendente: procurar o ciclo
    grafo = montar_grafo_espera(pendentes, donos)
    ciclo = achar_ciclo(grafo)
    bloqueados = [p.nome for p in pendentes]

    if mostrar:
        print("\nNenhum processo conseguiu avancar.")
        print("Grafo de espera (quem espera quem):")
        for quem, espera in grafo.items():
            print(f"  {quem} -> {espera}")
        print("DEADLOCK detectado.")
        print("Processos no ciclo:", " -> ".join(ciclo + [ciclo[0]]))
        fora = [n for n in bloqueados if n not in ciclo]
        if fora:
            print("Bloqueados esperando por quem esta no ciclo:", ", ".join(fora))

    return {"deadlock": True, "ciclo": ciclo, "bloqueados": bloqueados}


def montar_grafo_espera(pendentes, donos):
    """Para cada processo parado, guarda quem esta com o recurso que ele quer."""
    grafo = {}
    for p in pendentes:
        r = p.proximo_pedido()
        grafo[p.nome] = donos[r]
    return grafo


def achar_ciclo(grafo):
    """Segue as setas do grafo a partir de cada processo.
    Se voltar para um processo que ja estava no caminho, achou o ciclo."""
    for inicio in grafo:
        caminho = []
        atual = inicio
        while atual is not None and atual not in caminho:
            caminho.append(atual)
            atual = grafo.get(atual)
        if atual is not None and atual in caminho:
            return caminho[caminho.index(atual):]
    return []


# Cenarios prontos. Cada funcao devolve (processos, recursos).

def cenario_deadlock_simples():
    # igual ao DeadlockDemo da aula: cada um pega um recurso e pede o do outro
    return [Processo("P1", ["R1", "R2"]), Processo("P2", ["R2", "R1"])], ["R1", "R2"]


def cenario_ordem_global():
    # igual ao OrderedLocksDemo: todos pedem na mesma ordem (R1 antes de R2)
    return [Processo("P1", ["R1", "R2"]), Processo("P2", ["R1", "R2"])], ["R1", "R2"]


def cenario_tres_processos():
    # ciclo com tres processos: P1 espera P2, P2 espera P3, P3 espera P1
    processos = [
        Processo("P1", ["R1", "R2"]),
        Processo("P2", ["R2", "R3"]),
        Processo("P3", ["R3", "R1"]),
    ]
    return processos, ["R1", "R2", "R3"]


def cenario_com_processo_fora_do_ciclo():
    # P1 e P2 travam um no outro, P3 so quer R1 e fica esperando
    processos = [
        Processo("P1", ["R1", "R2"]),
        Processo("P2", ["R2", "R1"]),
        Processo("P3", ["R3", "R1"]),
    ]
    return processos, ["R1", "R2", "R3"]


CENARIOS = {
    "1": ("Deadlock simples (2 processos)", cenario_deadlock_simples),
    "2": ("Sem deadlock (pedidos na mesma ordem)", cenario_ordem_global),
    "3": ("Deadlock com 3 processos", cenario_tres_processos),
    "4": ("Deadlock com um processo esperando de fora do ciclo", cenario_com_processo_fora_do_ciclo),
}
