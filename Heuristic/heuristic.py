import random

def sortAcess(listAcess):
    listAcess.sort(key=lambda acess: acess['totalItens'], reverse=True)
    listAcess.sort(key=lambda acess: acess['orderTotal'], reverse=True)

    # print(listAcess)
    # print(len(listAcess))
    # print(listAcess[0])

    return listAcess

def getListAcess(acess):    
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

def calculate_score(list_order, wave_pedidos, LP=None, UP=None):
    qtd = 0

    for i in range(len(list_order)):
        if list_order.get(i, 0) - wave_pedidos.get(i, 0) <= 0:
            qtd += list_order.get(i, 0)
    
    if UP is not None:
        return qtd < UP
    return qtd

def getWaveGulosa(list_order, list_acess, LP, UP):
    wave = {
        'idAcess': [],
        'pedidosAtendido': {},
        'totalUnidades': 0,
        'score': 0
    }

    for i in range(len(list_acess)):
        temp_pedidos = wave['pedidosAtendido'].copy()
        
        for j in range(0, len(list_acess[i]['data']), 2):
            item_id = list_acess[i]['data'][j]
            quantidade = list_acess[i]['data'][j + 1]
            temp_pedidos[item_id] = temp_pedidos.get(item_id, 0) + quantidade

        if not calculate_score(list_order, temp_pedidos, LP, UP):
            break  
        
        wave['pedidosAtendido'] = temp_pedidos
        wave['idAcess'].append(list_acess[i]['id'])
        wave['totalUnidades'] = calculate_score(list_order, wave['pedidosAtendido'])
        
    wave['score'] = wave['totalUnidades'] / len(wave['idAcess']) if wave['idAcess'] else 0

    print(wave)
    return wave
    
def getWaveRandom(list_order, list_acess, LP, UP):
    wave = {
        'idAcess': [],
        'pedidosAtendido': {},
        'totalUnidades': 0,
        'score': 0
    }

    for i in range(len(list_acess)):
        id = random.randrange(0, len(list_acess), 2)
        temp_pedidos = wave['pedidosAtendido'].copy()
        
        for j in range(0, len(list_acess[id]['data']), 2):
            item_id = list_acess[id]['data'][j]
            quantidade = list_acess[id]['data'][j + 1]
            temp_pedidos[item_id] = temp_pedidos.get(item_id, 0) + quantidade

        if not calculate_score(list_order, temp_pedidos, LP, UP):
            break  
        
        wave['pedidosAtendido'] = temp_pedidos
        wave['idAcess'].append(list_acess[id]['id'])
        wave['totalUnidades'] = calculate_score(list_order, wave['pedidosAtendido'])
        
    wave['score'] = wave['totalUnidades'] / len(wave['idAcess']) if wave['idAcess'] else 0

    print(wave)
    return wave
    

def construction(order, acess, LP, UP):

    list_order = getOrderList(order)
    list_acess = getListAcess(acess)
    getWaveGulosa(list_order, list_acess, LP, UP)

