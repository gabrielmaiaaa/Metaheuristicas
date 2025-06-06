import random
from copy import deepcopy

def sortAccess(listAccess):
    listAccess.sort(key=lambda access: access['totalItens'], reverse=True)
    listAccess.sort(key=lambda access: access['orderTotal'], reverse=True)

    # print(listAccess)
    # print(len(listAccess))
    # print(listAccess[0])

    return listAccess

def getAccessList(access):    
    listTest = []

    for key, value in access.items():
        listAccess = {
            'id': key,
            'orderTotal': value[0],
            'data': [],
            'totalItens': 0
        }
        qtd = 0

        for i in range(1, len(value)):
            num_access = value[i]
            listAccess['data'].append(num_access)

            if i%2 == 0:
                qtd += num_access
                
        listAccess['totalItens'] = qtd
        listTest.append(listAccess)
    
    return sortAccess(listTest)

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

