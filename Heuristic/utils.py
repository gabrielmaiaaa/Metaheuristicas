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

    print(list_Order)
    return list_Order

def calculate_score(list_order, wave_pedidos, LB=None, UP=None):
    qtd = 0
    list = []
    
    temp_listOrder = deepcopy(list_order)
    # temp_wave = wave_pedidos.copy()
    temp_wave = deepcopy(wave_pedidos)

    for order in temp_listOrder:
        listOrder = order['listOrder']
        
        pedido_atendido = True
        for id_pedido, qtd_pedido in listOrder.items():
            if temp_wave.get(id_pedido, 0) < qtd_pedido:
                pedido_atendido = False
                continue

        if pedido_atendido:
            for id_pedido, qtd_pedido in listOrder.items():
                temp_wave[id_pedido] -= qtd_pedido
                qtd += qtd_pedido
                if order['id'] not in list:
                    list.append(order['id'])
    
    if UP is not None:
        return qtd < UP
    if LB is not None:
        return qtd > LB
    return qtd, list
