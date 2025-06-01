# Função para ler dados do dataset
def LerArquivo(nome):
    with open(f"Datasets/{nome}.txt") as f:
        instancia = [list(map(int, linha.split())) for linha in f.readlines()]
    return instancia

# Função para salvar dados que tiramos após operações com o dataset
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

def SalvarResultados(wave, time, timeRSO, nome):
    cont = 0
    with open(f"Salvar Dados/{nome}Resultados.txt", 'w') as f:
        for key, value in wave.items():
            cont += 1
            if cont <= 3:
                f.write(f"{key}: {', '.join(map(str, value))}\n")
            else:
                f.write(f"{key}: {value}\n")
        
        f.write(f"Tempo Gasto Heuristica: {time}\n")
        f.write(f"Tempo Gasto RSO: {timeRSO}\n")