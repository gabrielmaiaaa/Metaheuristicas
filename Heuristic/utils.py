def sortcorredor(listaCorredor):
    listaCorredor.sort(key=lambda corredor: corredor['totalItens'], reverse=True)
    listaCorredor.sort(key=lambda corredor: corredor['pedidosTotal'], reverse=True)

    return listaCorredor

def getListaCorredor(corredor):    
    listaCorredor = []

    for key, value in corredor.items():
        dicionarioCorredor = {
            'id': key,
            'pedidosTotal': value[0],
            'data': [],
            'totalItens': 0
        }
        qtd = 0

        for i in range(1, len(value)):
            numeroDeCorredores = value[i]
            dicionarioCorredor['data'].append(numeroDeCorredores)

            if i%2 == 0:
                qtd += numeroDeCorredores
                
        dicionarioCorredor['totalItens'] = qtd
        listaCorredor.append(dicionarioCorredor)
    
    return sortcorredor(listaCorredor)

def getListaPedidos(pedidos):
    listaPedidos = []

    for key, value in pedidos.items():
        dicionarioPedidos = {
            'id': key,
            'dicionarioPedidos': {}
        }

        for i in range(1, len(value), 2):
            numeroDePedidos = value[i]
            repeticoes = value[i+1]
            dicionarioPedidos['dicionarioPedidos'][numeroDePedidos] = repeticoes
        
        listaPedidos.append(dicionarioPedidos)

    # print(listaPedidos)
    return listaPedidos

def calculateScore(listaPedidos, wave_pedidos):
    tamanho = 0
    pedidos_atendidos = set()
    estoque = wave_pedidos.copy()

    for pedidos in listaPedidos:
        pedido = pedidos['dicionarioPedidos']
        pode_atender = all(
            estoque.get(item, 0) >= qtd 
            for item, qtd in pedido.items()
            )
        
        if pode_atender:
            for item, qtd in pedido.items():
                estoque[item] -= qtd
                tamanho += qtd
            pedidos_atendidos.add(pedidos['id'])

    return tamanho, list(pedidos_atendidos)

def verificaTamanhoUB(listaPedidos, wave_pedidos, UB):
    tamanho = 0
    pedidos_atendidos = set()
    estoque = wave_pedidos.copy()

    for pedidos in listaPedidos:
        pedido = pedidos['dicionarioPedidos']
        pode_atender = all(
            estoque.get(item, 0) >= qtd 
            for item, qtd in pedido.items()
            )
        
        if pode_atender:
            for item, qtd in pedido.items():
                estoque[item] -= qtd
                tamanho += qtd
            pedidos_atendidos.add(pedidos['id'])
    # print(UB, tamanho)

    return tamanho > UB

def verificaTamanhoLB(wave, LB):
    return wave['tamanho'] < LB
