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
    return gerar_wave_a_partir_de_ids(ids, list_access, list_order, LP, UP)

def rso(wave, list_order, list_access, LP, UP, max_inter=100):
    best = wave
    tabuList = []
    historico = [best]
    vizinhos = []
    tabuList = []
    tabuTenure = 1
    historico = []
    estagnado = 0
    interacao = 5
    maxVizinhos = 30
    interacao_maxVizinhos_counter = 0
    
    if max_inter <= 50:
        patience = int(max_inter/2)
    elif 51 <= max_inter <= 100:
        patience = int(max_inter/4)
    else:
        patience = int(max_inter/6)

    for _ in range(max_inter):
        vizinhos = gerar_vizinhos(best, list_access, list_order, LP, UP, tabuList, interacao)

        # tenho q fazer isso aqui ser otimizado
        if interacao % 5 == 0:
            taxa = random.choice([0.1, 0.2, 0.3, 0.4])
            vizinhos.append(reinicializacao_parcial(best, list_access, list_order, LP, UP, taxa))
            # interacao = max(interacao - 1, 5)
        
        if not vizinhos:
            estagnado += 1
            interacao = min(interacao + 1, maxVizinhos)
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
            interacao = min(interacao + 1, maxVizinhos)

        if melhorVizinho in historico[-10:]:
            tabuTenure = min(tabuTenure + 1, 30)
        else:
            tabuTenure = max(tabuTenure - 1, 3)     
               
        historico.append(melhorVizinho)

        if interacao == maxVizinhos:
            interacao_maxVizinhos_counter += 1
        else:
            interacao_maxVizinhos_counter -= 1

        if interacao_maxVizinhos_counter > 5:  
            maxVizinhos += 5
            interacao_maxVizinhos_counter = 0
        
        if estagnado >= patience:
            taxa = random.choice([0.5, 0.6, 0.7, 0.8])
            best = reinicializacao_parcial(best, list_access, list_order, LP, UP, taxa)
            estagnado = 0
            max_inter += 20
            if max_inter <= 50:
                patience = int(max_inter/2)
            elif 51 <= max_inter <= 100:
                patience = int(max_inter/4)
            else:
                patience = int(max_inter/6)
    
    bes = max(historico, key=lambda w: w['score'])
    print(bes)
    print(max_inter)
    return bes

def construction(order, access, LP, UP):
    list_order = getOrderList(order)
    list_access = getAccessList(access)
    
    start = time.perf_counter()
    wave = build_wave(list_order, list_access, LP, UP, 'random')
    heuristic_time = time.perf_counter() - start

    start_refi = time.perf_counter()
    waveRefinmanto =refine_wave(wave, list_order, list_access, LP, UP)
    refinamento_time = time.perf_counter() - start_refi
    
    start_rso = time.perf_counter()
    best = rso(wave, list_order, list_access, LP, UP)
    rso_time = time.perf_counter() - start_rso
    
    return best, heuristic_time, refinamento_time, rso_time