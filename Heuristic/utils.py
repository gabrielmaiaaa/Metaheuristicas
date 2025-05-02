import random

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
    total_order={}

    for key, value in order.items():
        for i in range(1, len(value), 2):
            num_pedido = value[i]
            repeticoes = value[i+1]
            total_order[num_pedido] = total_order.get(num_pedido, 0) + repeticoes

    print(total_order)
    return total_order

def calculate_score(list_order, wave_pedidos, LB=None, UP=None):
    qtd = 0

    for i in range(len(list_order)):
        if list_order.get(i, 0) - wave_pedidos.get(i, 0) <= 0:
            qtd += list_order.get(i, 0)
    
    if UP is not None:
        return qtd < UP
    return qtd
