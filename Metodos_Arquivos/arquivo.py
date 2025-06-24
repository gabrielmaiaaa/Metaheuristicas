def LerArquivo(nome):
    with open(f"Datasets/{nome}.txt") as f:
        instancia = [list(map(int, linha.split())) for linha in f.readlines()]
    return instancia

def SalvarArquivo(pedidos, corredores, LB, UP, nome):
    with open(f"Salvar Dados/{nome}.txt", 'w') as f:
        f.write("Pedidos:\n")
        for key, value in pedidos.items():
            f.write(f"{key}: {' '.join(map(str, value))}\n")
        
        f.write("\nCorredores:\n")
        for key, value in corredores.items():
            f.write(f"{key}: {' '.join(map(str, value))}\n")

        f.write("\nLimite Inferior e Limite Superior:\n")
        f.write(f"{LB} {UP}\n")

def SalvarResultados(wave, time, score, timeRefinamento, scoreRefinamento, timeRSO, nome, interacao, execucao):
    cont = 0
    with open(f"output/Teste1/{nome}Resultados.txt", 'w') as f:
        for key, value in wave.items():
            cont += 1
            if cont <= 3:
                f.write(f"{key}: {', '.join(map(str, value))}\n")
            else:
                f.write(f"{key}: {value}\n")
        f.write(f"Quantidade total de execucoes feitas: {execucao}\n")
        f.write(f"Tempo gasto para construir o RSO: {timeRSO}\n")

        if interacao:
            f.write("\n--- Momento que achou o melhor ---\n")
            f.write(f"Tempo gasto: {interacao[0]}\n")
            f.write(f"Score: {interacao[1]}\n")
            f.write(f"Quantidade de Interacoes: {interacao[2]}\n")
        else: 
            f.write("\n--- Momento que achou o melhor ---\n")
            f.write(f"O historico de interacoes veio vazio.\n")

        f.write('\nHeuristica\n')
        f.write(f"Score: {score}\n")
        f.write(f"Tempo: {time}\n")

        f.write('\nHeuristica Refinamento\n')
        f.write(f"Score: {scoreRefinamento}\n")
        f.write(f"Tempo: {timeRefinamento}\n")
        