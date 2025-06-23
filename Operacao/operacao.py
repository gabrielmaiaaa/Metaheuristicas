def Operar(instancia):
    cabecalho = instancia[0]
    corpo = instancia[1:-1]
    LB, UB = instancia[-1]
    pedidos = {}
    corredores = {}

    for o in range(cabecalho[0]):
        pedidos[o] = []

        for itens in corpo[o]:
            pedidos[o].append(itens)
    
    for a in range(cabecalho[0], cabecalho[0] + cabecalho[2]):
        indice = a - cabecalho[0]
        corredores[indice] = []

        for corredor in corpo[a]:
            corredores[indice].append(corredor)
            
    # print(f"Pedidos: {pedidos}")
    # print(f"Corredores: {corredores}")
    # print(f"LB: {LB} e UB: {UB}")
    
    return pedidos, corredores, LB, UB
