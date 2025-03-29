from Metodos_Arquivos.arquivo import *
from Operacao.operacao import *

def main():
    arquivo = 'instance_0020'
    instancia = LerArquivo(arquivo)
    pedidos, corredores, LB, UP = Operar(instancia)
    SalvarArquivo(pedidos, corredores, LB, UP,"teste")

if __name__ == '__main__':
    main()