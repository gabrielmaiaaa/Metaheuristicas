# Aqui estaram os códigos de ler arquivo e salvar os dados em arquivo
import numpy as np

# Função para ler dados do dataset
def LerArquivo(nome):
    instancia = np.loadtxt(f"Datasets/{nome}.txt", dtype=int)
    return instancia

# Função para salvar dados que tiramos após operações com o dataset
def SalvarArquivo(dados, nome):
    return np.savetxt(f"Salvar Dados/{nome}.txt", dados, fmt="%d")