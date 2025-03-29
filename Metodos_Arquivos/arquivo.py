# Aqui estaram os códigos de ler arquivo e salvar os dados em arquivo
import numpy as np

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