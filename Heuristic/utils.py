import random
from copy import deepcopy

def sortAcess(listAcess):
    listAcess.sort(key=lambda acess: acess['totalItens'], reverse=True)
    listAcess.sort(key=lambda acess: acess['orderTotal'], reverse=True)

    # print(listAcess)
    # print(len(listAcess))
    # print(listAcess[0])

    return listAcess

def getAcessList(acess):    
    listTest = []

    for key, value in acess.items():
        listAcess = {
            'id': key,
            'orderTotal': value[0],
            'data': [],
            'totalItens': 0
        }
        qtd = 0

        for i in range(1, len(value)):
            num_acess = value[i]
            listAcess['data'].append(num_acess)

            if i%2 == 0:
                qtd += num_acess
                
        listAcess['totalItens'] = qtd
        listTest.append(listAcess)
    
    return sortAcess(listTest)

def getOrderList(order):
    list_Order = []

    for key, value in order.items():
        total_order={
            'id': key,
            'listOrder': {}
        }

        for i in range(1, len(value), 2):
            num_pedido = value[i]
            repeticoes = value[i+1]
            total_order['listOrder'][num_pedido] = repeticoes
        
        list_Order.append(total_order)

    # print(list_Order)
    return list_Order

def calculate_score(list_order, wave_pedidos, LB=None, UP=None):
    qtd_total = 0
    pedidos_atendidos = set()
    estoque_wave = wave_pedidos.copy()

    for order in list_order:
        pedido = order['listOrder']
        pode_atender = all(estoque_wave.get(item, 0) >= qtd for item, qtd in pedido.items())
        
        if pode_atender:
            for item, qtd in pedido.items():
                estoque_wave[item] -= qtd
                qtd_total += qtd
            pedidos_atendidos.add(order['id'])

    if UP is not None:
        return qtd_total < UP
    if LB is not None:
        return qtd_total > LB

    return qtd_total, list(pedidos_atendidos)

