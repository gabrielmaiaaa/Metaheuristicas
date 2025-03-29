# Arquivo que vou utilizar para fazer algumas operações com os Datasets
import numpy as np

def Operar(instancia):
    cabecalho = instancia[0]
    corpo = instancia[1:]
    LB, UP = instancia[-1]
    for o in range(cabecalho[0]):
        print(f"Pedido {o}")
        for itens in corpo[o]:
            print(itens)
    
    for a in range(cabecalho[0], cabecalho[0] + cabecalho[2]):
        print(f"Corredor {a}")
        for corredores in corpo[a]:
            print(corredores)

    print(f"LB: {LB} e UP: {UP}")