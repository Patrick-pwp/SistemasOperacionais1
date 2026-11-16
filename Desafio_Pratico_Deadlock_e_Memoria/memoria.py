# Algoritmos de substituicao de paginas: FIFO e LRU.
# A lista "memoria" representa os frames.


def fifo(paginas, frames):
    """FIFO: quando a memoria enche, sai a pagina que entrou primeiro.
    Um HIT nao muda a ordem da lista."""
    memoria = []
    passos = []
    faltas = 0
    hits = 0

    for pagina in paginas:
        saiu = None
        if pagina in memoria:
            hits += 1
            resultado = "HIT"
        else:
            faltas += 1
            resultado = "PAGE FAULT"
            if len(memoria) >= frames:
                saiu = memoria.pop(0)      # a mais antiga fica na posicao 0
            memoria.append(pagina)
        passos.append((pagina, resultado, list(memoria), saiu))

    return {"faltas": faltas, "hits": hits, "passos": passos}


def lru(paginas, frames):
    """LRU: quando a memoria enche, sai a pagina usada ha mais tempo.
    Num HIT a pagina vai para o fim da lista (passa a ser a mais recente)."""
    memoria = []
    passos = []
    faltas = 0
    hits = 0

    for pagina in paginas:
        saiu = None
        if pagina in memoria:
            hits += 1
            resultado = "HIT"
            memoria.remove(pagina)
            memoria.append(pagina)
        else:
            faltas += 1
            resultado = "PAGE FAULT"
            if len(memoria) >= frames:
                saiu = memoria.pop(0)      # a menos recente fica na posicao 0
            memoria.append(pagina)
        passos.append((pagina, resultado, list(memoria), saiu))

    return {"faltas": faltas, "hits": hits, "passos": passos}


def mostrar_execucao(nome, resultado):
    print(f"\n{nome}")
    for pagina, status, memoria, saiu in resultado["passos"]:
        linha = f"Pagina {pagina:<3} -> {str(memoria):<22} {status}"
        if saiu is not None:
            linha += f"  (saiu a pagina {saiu})"
        print(linha)

    total = resultado["faltas"] + resultado["hits"]
    print(f"Page faults: {resultado['faltas']}")
    print(f"Hits: {resultado['hits']}")
    print(f"Taxa de page faults: {resultado['faltas'] / total * 100:.2f}%")
    print(f"Taxa de hits: {resultado['hits'] / total * 100:.2f}%")


def comparar(paginas, frames):
    """Roda FIFO e LRU na mesma sequencia e mostra qual teve menos faltas."""
    r_fifo = fifo(paginas, frames)
    r_lru = lru(paginas, frames)
    mostrar_execucao("FIFO", r_fifo)
    mostrar_execucao("LRU", r_lru)

    print("\nComparacao")
    print(f"{'Algoritmo':<10}{'Page faults':>12}{'Hits':>6}")
    print(f"{'FIFO':<10}{r_fifo['faltas']:>12}{r_fifo['hits']:>6}")
    print(f"{'LRU':<10}{r_lru['faltas']:>12}{r_lru['hits']:>6}")

    if r_fifo["faltas"] < r_lru["faltas"]:
        print("Nesta sequencia o FIFO teve menos page faults que o LRU.")
    elif r_lru["faltas"] < r_fifo["faltas"]:
        print("Nesta sequencia o LRU teve menos page faults que o FIFO.")
    else:
        print("Nesta sequencia os dois tiveram o mesmo numero de page faults.")


# Anomalia de Belady

def faltas_por_frames(algoritmo, paginas, max_frames):
    """Devolve {quantidade de frames: page faults} de 1 ate max_frames."""
    return {f: algoritmo(paginas, f)["faltas"] for f in range(1, max_frames + 1)}


def achar_belady(tabela):
    """A anomalia acontece quando, com mais frames, o numero de faltas AUMENTA.
    Devolve os pares (frames menor, frames maior) em que isso aconteceu."""
    casos = []
    for menor in sorted(tabela):
        for maior in sorted(tabela):
            if maior > menor and tabela[maior] > tabela[menor]:
                casos.append((menor, maior))
    return casos


def analisar_belady(paginas, max_frames):
    print(f"\nSequencia: {paginas}")
    for nome, algoritmo in (("FIFO", fifo), ("LRU", lru)):
        tabela = faltas_por_frames(algoritmo, paginas, max_frames)
        print(f"\n{nome}")
        for f, faltas in tabela.items():
            print(f"  {f} frames -> {faltas} page faults")
        casos = achar_belady(tabela)
        if casos:
            print("  Anomalia de Belady encontrada:")
            for menor, maior in casos:
                print(f"    com {menor} frames: {tabela[menor]} faltas; "
                      f"com {maior} frames: {tabela[maior]} faltas")
        else:
            print("  Sem anomalia: mais frames nunca aumentou as faltas.")
