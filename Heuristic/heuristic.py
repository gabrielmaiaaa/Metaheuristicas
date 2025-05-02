import random
from Heuristic.utils import calculate_score, getAcessList, getOrderList

def getWaveGulosa(list_order, list_acess, LB, UP):
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

        if not calculate_score(list_order, temp_pedidos, LB, UP):
            break  
        
        wave['pedidosAtendido'] = temp_pedidos
        wave['idAcess'].append(list_acess[i]['id'])
        wave['totalUnidades'] = calculate_score(list_order, wave['pedidosAtendido'])
        
    wave['score'] = wave['totalUnidades'] / len(wave['idAcess']) if wave['idAcess'] else 0

    print(wave)
    return wave
    
def getWaveRandom(list_order, list_acess, LB, UP):
    wave = {
        'idAcess': [],
        'pedidosAtendido': {},
        'totalUnidades': 0,
        'score': 0
    }

    for i in range(len(list_acess)):
        id = random.randrange(0, len(list_acess), 2)
        
        if list_acess[id]['id'] in wave['idAcess']:
            continue

        temp_pedidos = wave['pedidosAtendido'].copy()
        
        for j in range(0, len(list_acess[id]['data']), 2):
            item_id = list_acess[id]['data'][j]
            quantidade = list_acess[id]['data'][j + 1]
            temp_pedidos[item_id] = temp_pedidos.get(item_id, 0) + quantidade

        if not calculate_score(list_order, temp_pedidos, LB, UP):
            break  
        
        wave['pedidosAtendido'] = temp_pedidos
        wave['idAcess'].append(list_acess[id]['id'])
        wave['totalUnidades'] = calculate_score(list_order, wave['pedidosAtendido'])
        
    wave['score'] = wave['totalUnidades'] / len(wave['idAcess']) if wave['idAcess'] else 0

    print(wave)
    return wave
    

def construction(order, acess, LB, UP):

    list_order = getOrderList(order)
    list_acess = getAcessList(acess)
    getWaveRandom(list_order, list_acess, LB, UP)

