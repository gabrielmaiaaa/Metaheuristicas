import random
import time
from Metodos_Arquivos.arquivo import *
from Heuristic.utils import calculate_score, getAcessList, getOrderList
random.seed(6743)

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

def gerar_vizinhos(wave, list_acess, list_order, LP, UP, tabuList, interacao):
    vizinhos = []
    ids_wave = wave['idAcess'][:]
    corredores_na_wave = set(ids_wave)
    corredores_fora_wave = [a for a in list_acess if a['id'] not in corredores_na_wave]

    tentativas = 0
    while len(vizinhos) < interacao and tentativas < interacao * 2:
        nova_ids = ids_wave[:]
        tipo = random.choice(['troca', 'remove', 'add', 'dupla_troca'])

        if tipo == 'troca' and corredores_fora_wave:
            id_out = random.choice(nova_ids)
            nova_ids.remove(id_out)
            novo_in = random.choice(corredores_fora_wave)['id']
            nova_ids.append(novo_in)
        
        elif tipo == 'remove' and len(nova_ids) > 1:
            id_out = random.choice(nova_ids)
            nova_ids.remove(id_out)
        
        elif tipo == 'add' and corredores_fora_wave:
            novo_in = random.choice(corredores_fora_wave)['id']
            if novo_in not in nova_ids:
                nova_ids.append(novo_in)
        
        elif tipo == 'dupla_troca' and len(nova_ids) > 1 and len(corredores_fora_wave) > 1:
            ids_out = random.sample(nova_ids, 2)
            for id_out in ids_out:
                nova_ids.remove(id_out)
            novos_in = random.sample([a['id'] for a in corredores_fora_wave], 2)
            nova_ids.extend(novos_in)

        nova_wave = gerar_wave_a_partir_de_ids(nova_ids, list_acess, list_order, LP, UP)

        if nova_wave and nova_wave['idAcess'] not in tabuList and nova_wave['score'] > wave['score']:
            vizinhos.append(nova_wave)

        tentativas += 1

    return vizinhos


def reinicializacao_parcial(solucao, list_acess, list_order, LP, UP, taxa=0.5):
    n_manter = max(1, int(len(solucao['idAcess']) * taxa))
    ids_manter = random.sample(solucao['idAcess'], n_manter)
    corredores_fora = [a['id'] for a in list_acess if a['id'] not in ids_manter]
    n_adicionar = len(solucao['idAcess']) - n_manter
    ids_novos = random.sample(corredores_fora, n_adicionar)
    nova_ids = ids_manter + ids_novos
    nova_wave = gerar_wave_a_partir_de_ids(nova_ids, list_acess, list_order, LP, UP)
    return nova_wave

def rso(wave, list_order, list_acess, LP, UP, max_inter=30):
    solucaoInicial = wave
    bestSolution = solucaoInicial
    tabuList = []
    tabuTenure = 1
    historico = []
    estaguinado = 0
    interacao = 5

    for _ in range(max_inter):
        vizinhos = gerar_vizinhos(bestSolution, list_acess, list_order, LP, UP, tabuList, interacao)
        
        if not vizinhos:
            estaguinado += 1
            interacao = max(interacao - 1, 5)
            if estaguinado >= int(max_inter/4):
                bestSolution = reinicializacao_parcial(bestSolution, list_acess, list_order, LP, UP)
                estaguinado = 0
            continue

        if interacao % 5 == 0:
            vizinhos.append(reinicializacao_parcial(bestSolution, list_acess, list_order, LP, UP))
            interacao = max(interacao - 1, 5)

        melhor_vizinho = max(vizinhos, key=lambda w: w['score'])
        
        if melhor_vizinho['score'] > bestSolution['score']:
            bestSolution = melhor_vizinho
        
        tabuList.append(melhor_vizinho['idAcess'])
        if len(tabuList) > tabuTenure:
            tabuList.pop(0)
        
        if melhor_vizinho in historico[-10:]:
            tabuTenure = min(tabuTenure + 1, 30)
        else:
            tabuTenure = max(tabuTenure - 1, 3)
        historico.append(melhor_vizinho)
        interacao = min(interacao + 1, 30)

    print(bestSolution)
    print(interacao)
    print(estaguinado)
    return bestSolution
        

def construction(order, acess, LP, UP):
    list_order = getOrderList(order)
    list_acess = getAcessList(acess)

    inicio = time.perf_counter()
    wave = getWaveRandom(list_order, list_acess, LP, UP)
    fim = time.perf_counter()

    inicioRSO = time.perf_counter()
    bestSolution = rso(wave, list_order, list_acess, LP, UP)
    fimRSO = time.perf_counter()

    return bestSolution, fim-inicio, fimRSO-inicioRSO
