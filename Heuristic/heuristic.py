import random
from Heuristic.utils import calculate_score, getAcessList, getOrderList

def gerar_wave_a_partir_de_ids(ids, list_acess, list_order, LP, UP):
    wave = {
        'idAcess': [],
        'itensDePedidosAtendidos': {},
        'pedidosAtendidos': [],
        'totalUnidades': 0,
        'score': 0
    }

    pedidosAtendidos_temp = {}

    for id_acess in ids:
        acess = next((a for a in list_acess if a['id'] == id_acess), None)
        if not acess:
            continue
        
        for i in range(0, len(acess['data']), 2):
            item_id = acess['data'][i]
            quantidade = acess['data'][i + 1]
            pedidosAtendidos_temp[item_id] = pedidosAtendidos_temp.get(item_id, 0) + quantidade
        
        if not calculate_score(list_order, pedidosAtendidos_temp, LP, UP):
            continue

        wave['idAcess'].append(id_acess)
        wave['itensDePedidosAtendidos'] = pedidosAtendidos_temp.copy()

    wave['totalUnidades'], wave['pedidosAtendidos'] = calculate_score(list_order, wave['itensDePedidosAtendidos'])
    wave['score'] = wave['totalUnidades'] / len(wave['idAcess']) if wave['idAcess'] else 0

    return wave

def refine_wave(wave, list_order, list_acess, LP, UP):
    melhor_score = wave['score']
    melhor_wave = wave.copy()

    corredores_na_wave = set(wave['idAcess'])
    corredores_fora_wave = [a for a in list_acess if a['id'] not in corredores_na_wave]

    for id_out in wave['idAcess']:
        for novo_acesso in corredores_fora_wave:
            id_in = novo_acesso['id']

            nova_ids = wave['idAcess'][:]
            nova_ids.remove(id_out)
            nova_ids.append(id_in)

            nova_wave = gerar_wave_a_partir_de_ids(nova_ids, list_acess, list_order, LP, UP)

            if nova_wave and nova_wave['score'] > melhor_score:
                melhor_wave = nova_wave
                melhor_score = nova_wave['score']

    print("Melhor score após refinamento:", melhor_score)
    return melhor_wave


def getWaveGulosa(list_order, list_acess, LB, UP):
    wave = {
        'idAcess': [],
        'itensDePedidosAtendidos': {},
        'pedidosAtendidos': [],
        'totalUnidades': 0,
        'score': 0
    }

    for i in range(len(list_acess)):
        temp_pedidosAtendidos = wave['itensDePedidosAtendidos'].copy()
        
        for j in range(0, len(list_acess[i]['data']), 2):
            item_id = list_acess[i]['data'][j]
            quantidade = list_acess[i]['data'][j + 1]
            temp_pedidosAtendidos[item_id] = temp_pedidosAtendidos.get(item_id, 0) + quantidade

        if not calculate_score(list_order, temp_pedidosAtendidos, LB, UP):
            break  
        
        wave['itensDePedidosAtendidos'] = temp_pedidosAtendidos
        wave['idAcess'].append(list_acess[i]['id'])
        wave['totalUnidades'], wave['pedidosAtendidos'] = calculate_score(list_order, wave['itensDePedidosAtendidos'])
        
    wave['score'] = wave['totalUnidades'] / len(wave['idAcess']) if wave['idAcess'] else 0

    print(f'\nWave: {wave}\n')
    return wave
    
def getWaveRandom(list_order, list_acess, LB, UP):
    wave = {
        'idAcess': [],
        'itensDePedidosAtendidos': {},
        'pedidosAtendidos': [],
        'totalUnidades': 0,
        'score': 0
    }

    for i in range(len(list_acess)):
        id = random.randrange(0, len(list_acess))
        
        if list_acess[id]['id'] in wave['idAcess']:
            continue

        temp_pedidosAtendidos = wave['itensDePedidosAtendidos'].copy()
        
        for j in range(0, len(list_acess[id]['data']), 2):
            item_id = list_acess[id]['data'][j]
            quantidade = list_acess[id]['data'][j + 1]
            temp_pedidosAtendidos[item_id] = temp_pedidosAtendidos.get(item_id, 0) + quantidade

        if not calculate_score(list_order, temp_pedidosAtendidos, LB, UP):
            break  
        
        wave['itensDePedidosAtendidos'] = temp_pedidosAtendidos
        wave['idAcess'].append(list_acess[id]['id'])
        wave['totalUnidades'], wave['pedidosAtendidos'] = calculate_score(list_order, wave['itensDePedidosAtendidos'])
        
    wave['score'] = wave['totalUnidades'] / len(wave['idAcess']) if wave['idAcess'] else 0

    print(wave)
    return wave
    

def construction(order, acess, LP, UP):
    list_order = getOrderList(order)
    list_acess = getAcessList(acess)
    wave = getWaveRandom(list_order, list_acess, LP, UP)

    refined_wave = refine_wave(wave, list_order, list_acess, LP, UP)

    print(refined_wave)
