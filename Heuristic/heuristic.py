import random
import time
from Metodos_Arquivos.arquivo import *
from Heuristic.utils import calculate_score, getAccessList, getOrderList
random.seed(6743)

def build_wave(list_order, list_access, LB, UP, tipo):
    wave = {
        'idAccess': [],
        'itensDePedidosAtendidos': {},
        'pedidosAtendidos': [],
        'totalUnidades': 0,
        'score': 0
    }
    
    accesses = list_access.copy()
    if tipo == 'random':
        random.shuffle(accesses)
    
    temp_items = {}
    
    for access in accesses:
        data = access['data']
        for i in range(0, len(data), 2):
            item_id = data[i]
            quantidade = data[i+1]
            temp_items[item_id] = temp_items.get(item_id, 0) + quantidade
        
        if not calculate_score(list_order, temp_items, LB, UP):
            if tipo == 'gulosa':
                break
            continue
        
        wave['idAccess'].append(access['id'])
        wave['itensDePedidosAtendidos'] = temp_items.copy()
    
    if wave['idAccess']:
        wave['totalUnidades'], wave['pedidosAtendidos'] = calculate_score(
            list_order, wave['itensDePedidosAtendidos'])
        wave['score'] = wave['totalUnidades'] / len(wave['idAccess'])
    
    return wave

def gerar_wave_a_partir_de_ids(ids, list_access, list_order, LP, UP):
    id = set(ids)
    accesses = [a for a in list_access if a['id'] in id]
    return build_wave(list_order, accesses, LP, UP, 'gulosa')

def refine_wave(wave, list_order, list_access, LP, UP):
    atualIds = set(wave['idAccess'])
    available_ids = [a['id'] for a in list_access if a['id'] not in atualIds]
    
    for id_out in wave['idAccess']:
        for id_in in available_ids:
            newIds = [id_in if id == id_out else id for id in wave['idAccess']]
            newWave = gerar_wave_a_partir_de_ids(newIds, list_access, list_order, LP, UP)
            
            if newWave['score'] > wave['score']:
                return newWave
    return wave

def gerar_vizinhos(wave, list_access, list_order, LP, UP, tabuList, interacao):
    vizinhos = []
    atualIds = set(wave['idAccess'])
    todosIds = {a['id'] for a in list_access}
    available_ids = list(todosIds - atualIds)
    
    operations = {
        'troca': lambda ids: (ids - {random.choice(list(ids))}) | {random.choice(available_ids)} if available_ids else ids,
        'remove': lambda ids: ids - {random.choice(list(ids))} if len(ids) > 1 else ids,
        'add': lambda ids: ids | {random.choice(available_ids)} if available_ids else ids
    }
    
    for _ in range(interacao):
        operation = random.choice(list(operations.keys()))
        newIds = operations[operation](atualIds)
        
        if newIds == atualIds or list(newIds) in tabuList:
            continue
            
        newWave = gerar_wave_a_partir_de_ids(newIds, list_access, list_order, LP, UP)
        vizinhos.append(newWave)
    
    return vizinhos

def reinicializacao_parcial(solucao, list_access, list_order, LP, UP, taxa):
    ids = set(random.sample(solucao['idAccess'], max(1, int(len(solucao['idAccess']) * taxa))))
    newIds = [a['id'] for a in list_access if a['id'] not in ids]
    bestIds = set(random.sample(newIds, min(len(newIds), len(solucao['idAccess']) - len(ids))))
    return gerar_wave_a_partir_de_ids(ids | bestIds, list_access, list_order, LP, UP)

def rso(wave, list_order, list_access, LP, UP, max_inter=100):
    best = wave
    tabuList = []
    historico = []
    tabuList = []
    tabuTenure = 1
    historico = []
    estagnado = 0
    interacao = 5

    for _ in range(max_inter):
        vizinhos = gerar_vizinhos(best, list_access, list_order, LP, UP, tabuList, interacao)
        
        if interacao % 5 == 0:
            vizinhos.append(reinicializacao_parcial(best, list_access, list_order, LP, UP, 0.2))
            interacao = max(interacao - 1, 5)

        if estagnado >= int(max_inter/4):
            vizinhos.append(reinicializacao_parcial(best, list_access, list_order, LP, UP, 0.5))
            estagnado = 0
            # print(_)
            # break
        
        if not vizinhos:
            estagnado += 1
            interacao = min(interacao + 1, 30)
            continue
            
        melhorVizinho = max(vizinhos, key=lambda w: w['score'])

        tabuList.append(melhorVizinho['idAccess'])
        if len(tabuList) > tabuTenure:
            tabuList.pop(0)
        
        if melhorVizinho['score'] > best['score']:
            best = melhorVizinho
            estagnado = 0
        else:
            estagnado += 1
            interacao = min(interacao + 1, 30)

        if melhorVizinho in historico[-10:]:
            tabuTenure = min(tabuTenure + 1, 30)
        else:
            tabuTenure = max(tabuTenure - 1, 3)     
               
        historico.append(melhorVizinho)
    
    # print(best)
    return best

def construction(order, access, LP, UP):
    list_order = getOrderList(order)
    list_access = getAccessList(access)
    
    start = time.perf_counter()
    wave = build_wave(list_order, list_access, LP, UP, 'random')
    build_time = time.perf_counter() - start
    
    start_rso = time.perf_counter()
    best = rso(wave, list_order, list_access, LP, UP)
    rso_time = time.perf_counter() - start_rso
    
    return best, build_time, rso_time