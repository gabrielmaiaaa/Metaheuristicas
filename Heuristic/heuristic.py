import random
import time
import numpy as np
from types import new_class
from Metodos_Arquivos.arquivo import *
from Heuristic.utils import calculateScore, getListaCorredor, getListaPedidos, verificaTamanhoUB, verificaTamanhoLB
random.seed(6743)
np.random.seed(6743)

def construirWave(listaPedidos, listaCorredor, UB, tipo="gulosa"):
    wave = {
        'idCorredor': [],
        'itensDePedidosAtendidos': {},
        'pedidosAtendidos': [],
        'tamanho': 0,
        'score': 0
    }
    
    corredores = listaCorredor.copy()
    if tipo == "aleatorio":
        random.shuffle(corredores)
    
    itensDePedidosAtendidos = {}
    
    for corredor in corredores:
        data = corredor['data']
        for i in range(0, len(data), 2):
            idItem = data[i]
            quantidade = data[i+1]
            itensDePedidosAtendidos[idItem] = itensDePedidosAtendidos.get(idItem, 0) + quantidade
        
        if verificaTamanhoUB(listaPedidos, itensDePedidosAtendidos, UB):
            break
        
        wave['idCorredor'].append(corredor['id'])
        wave['itensDePedidosAtendidos'] = itensDePedidosAtendidos.copy()
    
    if wave['idCorredor']:
        wave['tamanho'], wave['pedidosAtendidos'] = calculateScore(
            listaPedidos, wave['itensDePedidosAtendidos'])
        wave['score'] = wave['tamanho'] / len(wave['idCorredor'])
    
    return wave

def gerarNovaWave(ids, listaCorredor, listaPedidos, UB):
    id = set(ids)
    corredores = [a for a in listaCorredor if a['id'] in id]
    return construirWave(listaPedidos, corredores, UB, 'gulosa')

def refinarWave(wave, listaPedidos, listaCorredor, LB, UB):
    idsCorredoresAtuais = set(wave['idCorredor'])
    idsCorredoresDisponiveis = [a['id'] for a in listaCorredor if a['id'] not in idsCorredoresAtuais]
    
    for idCorredor in wave['idCorredor']:
        for idDisponivel in idsCorredoresDisponiveis:
            novoId = [idDisponivel if id == idCorredor else id for id in wave['idCorredor']]
            vizinho = gerarNovaWave(novoId, listaCorredor, listaPedidos, UB)
            
            if vizinho['score'] > wave['score']:
                return vizinho
    return wave

def atualizarPontuacaoOperacao(operacao, recompensa, listaPontuacao, taxa_aprendizado=0.1):
    index = {"troca": 0, "remove": 1, "add": 2}[operacao]
    listaPontuacao[index] = max(0, min(1, listaPontuacao[index] + taxa_aprendizado * recompensa))

def escolher_operacao(listaPontuacao, temperatura=0.3):
    scores = np.array(listaPontuacao)
    exp_scores = np.exp(scores / temperatura)
    probabilidades = exp_scores / exp_scores.sum()
    return random.choices(["troca", "remove", "add"], weights=probabilidades)[0]

def gerarVizinhos(wave, listaCorredor, listaPedidos, LB, UB, tabuList, interacao, listaPontuacao):
    vizinhos = []
    idsCorredoresAtuais = set(wave['idCorredor'])

    if not idsCorredoresAtuais:
        return vizinhos
    
    todosIds = {a['id'] for a in listaCorredor}
    idsCorredoresDisponiveis = list(todosIds - idsCorredoresAtuais)
    
    operacoes = {
        'troca': lambda ids: (ids - {random.choice(list(ids))}) | {random.choice(idsCorredoresDisponiveis)} if idsCorredoresDisponiveis else ids,
        'remove': lambda ids: ids - {random.choice(list(ids))} if len(ids) > 1 else ids,
        'add': lambda ids: ids | {random.choice(idsCorredoresDisponiveis)} if idsCorredoresDisponiveis else ids
    }
    
    for _ in range(interacao):
        # operacao = random.choice(list(operacoes.keys()))
        # novoId = operacoes[operacao](idsCorredoresAtuais)
        operacao = escolher_operacao(listaPontuacao)
        novoId = operacoes[operacao](idsCorredoresAtuais)
        
        if novoId == idsCorredoresAtuais or list(novoId) in tabuList:
            atualizarPontuacaoOperacao(operacao, -0.02, listaPontuacao)
            continue
            
        vizinho = gerarNovaWave(novoId, listaCorredor, listaPedidos, UB)

        if verificaTamanhoLB(vizinho, LB):
            atualizarPontuacaoOperacao(operacao, -0.02, listaPontuacao)
            continue

        recompensa = 0.01 + 0.1 * (vizinho['score'] - wave['score']) / max(1, wave['score'])
        atualizarPontuacaoOperacao(operacao, recompensa, listaPontuacao)
        vizinhos.append(vizinho)
    
    return vizinhos

def reiniciarWave(solucao, listaCorredor, listaPedidos, UB, taxa):
    ids = set(random.sample(solucao['idCorredor'], max(1, int(len(solucao['idCorredor']) * taxa))))
    novoId = [a['id'] for a in listaCorredor if a['id'] not in ids]
    waveAtualIds = set(random.sample(novoId, min(len(novoId), len(solucao['idCorredor']) - len(ids)+1)))
    return gerarNovaWave(ids | waveAtualIds, listaCorredor, listaPedidos, UB)

def rso(wave, listaPedidos, listaCorredor, LB, UB, maximoInteracao=100, tempoLimite=0.2):
    waveAtual = wave
    historico = [waveAtual]
    vizinhos = []
    tabuList = []
    tabuTenure = 1
    estagnado = 0
    interacao = 5
    maxVizinhos = 30
    interacaoMaxVizinhos = 0
    historicoInteracao = []
    listaPontuacao = [0.33, 0.33, 0.34] 
    
    patience = int(maximoInteracao * 0.2)
    patienceLR = int(patience * 0.25)
    
    execucao = 0
    tempoInicial = time.time()
    finalizarExecucao  = tempoInicial + (tempoLimite * 60)

    while time.time() < finalizarExecucao:
        execucao += 1
        vizinhos = gerarVizinhos(waveAtual, listaCorredor, listaPedidos, LB, UB, tabuList, interacao, listaPontuacao)

        # tenho q fazer isso aqui ser otimizado
        if estagnado >= patienceLR:
            taxa = random.choice([0.1, 0.2, 0.3, 0.4])
            vizinhos.append(reiniciarWave(waveAtual, listaCorredor, listaPedidos, UB, taxa))
            # interacao = max(interacao - 1, 5)
            patienceLR += int(patience * 0.25)
        
        if not vizinhos:
            estagnado += 1
            interacao = min(interacao + 1, maxVizinhos)
            continue
            
        melhorVizinho = max(vizinhos, key=lambda w: w['score'])

        tabuList.append(melhorVizinho['idCorredor'])
        if len(tabuList) > tabuTenure:
            tabuList.pop(0)
        
        if melhorVizinho['score'] > waveAtual['score']:
            waveAtual = melhorVizinho
            historicoInteracao.append([round(time.time() - tempoInicial, 4), round(melhorVizinho['score'], 2), execucao])
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
            interacaoMaxVizinhos += 1
        else:
            interacaoMaxVizinhos -= 1

        if interacaoMaxVizinhos > 5:  
            maxVizinhos += 5
            interacaoMaxVizinhos = 0
        
        if estagnado >= patience:
            taxa = random.choice([0.7, 0.8])
            vizinho = reiniciarWave(waveAtual, listaCorredor, listaPedidos, UB, taxa)

            if vizinho['idCorredor']:
                waveAtual = vizinho

            estagnado = 0
            maximoInteracao += 50
            # listaPontuacao[0] = max(0, listaPontuacao[0] - 0.2) 
            # listaPontuacao[1] = max(0, listaPontuacao[1] - 0.2) 
            # listaPontuacao[2] = max(0, listaPontuacao[2] - 0.2) 

            patience = int(maximoInteracao * 0.2)
            patienceLR = int(patience * 0.25)
    
    waveAtual = max(historico, key=lambda w: w['score'])
    print(historicoInteracao, maximoInteracao, listaPontuacao)
    print(round(time.time() - tempoInicial, 2))
    return waveAtual

def construction(pedidos, corredor, LB, UB):
    listaPedidos = getListaPedidos(pedidos)
    listaCorredor = getListaCorredor(corredor)
    
    start = time.perf_counter()
    wave = construirWave(listaPedidos, listaCorredor, UB, "aleatorio")
    heuristic_time = time.perf_counter() - start
    heuristic_score = wave['score']

    start_refi = time.perf_counter()
    waveRefinmanto =refinarWave(wave, listaPedidos, listaCorredor, LB, UB)
    refinamento_time = time.perf_counter() - start
    refinamento_score = waveRefinmanto['score']
    
    start_rso = time.perf_counter()
    melhorWave = rso(wave, listaPedidos, listaCorredor, LB, UB)
    rso_time = time.perf_counter() - start_rso

    # print(wave)
    # print()
    print(melhorWave['score'])
    print()
    
    return melhorWave, heuristic_time, heuristic_score, refinamento_time, refinamento_score, rso_time