import random
import time
from Metodos_Arquivos.arquivo import *
from Heuristic.utils import calculate_score, getAcessList, getOrderList
random.seed(6743)

def build_wave(list_order, list_acess, LB, UP, strategy='greedy'):
    wave = {
        'idAcess': [],
        'itensDePedidosAtendidos': {},
        'pedidosAtendidos': [],
        'totalUnidades': 0,
        'score': 0
    }
    
    accesses = list_acess.copy()
    if strategy == 'random':
        random.shuffle(accesses)
    
    temp_items = {}
    
    for acess in accesses:
        data = acess['data']
        for i in range(0, len(data), 2):
            item_id = data[i]
            quantidade = data[i+1]
            temp_items[item_id] = temp_items.get(item_id, 0) + quantidade
        
        if not calculate_score(list_order, temp_items, LB, UP):
            if strategy == 'greedy':
                break
            continue
        
        wave['idAcess'].append(acess['id'])
        wave['itensDePedidosAtendidos'] = temp_items.copy()
    
    if wave['idAcess']:
        wave['totalUnidades'], wave['pedidosAtendidos'] = calculate_score(
            list_order, wave['itensDePedidosAtendidos'])
        wave['score'] = wave['totalUnidades'] / len(wave['idAcess'])
    
    return wave

def gerar_wave_a_partir_de_ids(ids, list_acess, list_order, LP, UP):
    id_set = set(ids)
    accesses = [a for a in list_acess if a['id'] in id_set]
    return build_wave(list_order, accesses, LP, UP, strategy='greedy')

def refine_wave(wave, list_order, list_acess, LP, UP):
    current_ids = set(wave['idAcess'])
    available_ids = [a['id'] for a in list_acess if a['id'] not in current_ids]
    
    for id_out in wave['idAcess']:
        for id_in in available_ids:
            new_ids = [id_in if id == id_out else id for id in wave['idAcess']]
            new_wave = gerar_wave_a_partir_de_ids(new_ids, list_acess, list_order, LP, UP)
            
            if new_wave['score'] > wave['score']:
                return new_wave
    return wave

def gerar_vizinhos(wave, list_acess, list_order, LP, UP, tabuList, interacao):
    vizinhos = []
    current_ids = set(wave['idAcess'])
    all_ids = {a['id'] for a in list_acess}
    available_ids = list(all_ids - current_ids)
    
    operations = {
        'troca': lambda ids: (ids - {random.choice(list(ids))}) | {random.choice(available_ids)} if available_ids else ids,
        'remove': lambda ids: ids - {random.choice(list(ids))} if len(ids) > 1 else ids,
        'add': lambda ids: ids | {random.choice(available_ids)} if available_ids else ids
    }
    
    for _ in range(interacao):
        operation = random.choice(list(operations.keys()))
        new_ids = operations[operation](current_ids)
        
        if new_ids == current_ids or list(new_ids) in tabuList:
            continue
            
        new_wave = gerar_wave_a_partir_de_ids(new_ids, list_acess, list_order, LP, UP)
        vizinhos.append(new_wave)
    
    return vizinhos

def reinicializacao_parcial(solucao, list_acess, list_order, LP, UP, taxa):
    keep_ids = set(random.sample(solucao['idAcess'], max(1, int(len(solucao['idAcess']) * taxa))))
    available_ids = [a['id'] for a in list_acess if a['id'] not in keep_ids]
    add_ids = set(random.sample(available_ids, min(len(available_ids), len(solucao['idAcess']) - len(keep_ids))))
    return gerar_wave_a_partir_de_ids(keep_ids | add_ids, list_acess, list_order, LP, UP)

def rso(wave, list_order, list_acess, LP, UP, max_inter=100):
    best = wave
    tabuList = []
    historico = []
    tabuList = []
    tabuTenure = 1
    historico = []
    estagnado = 0
    interacao = 5
    

    for _ in range(max_inter):
        vizinhos = gerar_vizinhos(best, list_acess, list_order, LP, UP, tabuList, interacao)
        
        if interacao % 5 == 0:
            vizinhos.append(reinicializacao_parcial(best, list_acess, list_order, LP, UP, 0.2))
            interacao = max(interacao - 1, 5)

        if estagnado >= int(max_inter/4):
            vizinhos.append(reinicializacao_parcial(best, list_acess, list_order, LP, UP, 0.5))
            estagnado = 0
            # print(_)
            # break
        
        if not vizinhos:
            estagnado += 1
            interacao = min(interacao + 1, 30)
            continue
            
        melhorVizinho = max(vizinhos, key=lambda w: w['score'])
        tabuList.append(melhorVizinho['idAcess'])
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

def construction(order, acess, LP, UP):
    list_order = getOrderList(order)
    list_acess = getAcessList(acess)
    
    start = time.perf_counter()
    wave = build_wave(list_order, list_acess, LP, UP, 'random')
    build_time = time.perf_counter() - start
    
    start_rso = time.perf_counter()
    best = rso(wave, list_order, list_acess, LP, UP)
    rso_time = time.perf_counter() - start_rso
    
    return best, build_time, rso_time