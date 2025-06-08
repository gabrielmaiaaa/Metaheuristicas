from Metodos_Arquivos.arquivo import *
from Operacao.operacao import *
from Heuristic.heuristic import *
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <nome_do_arquivo>")
        sys.exit(1)
    
    arquivo = sys.argv[1].replace('.txt', '') 
    # arquivo = 'instance_0019'
    instancia = LerArquivo(arquivo)
    pedidos, corredores, LB, UP = Operar(instancia)
    SalvarArquivo(pedidos, corredores, LB, UP, arquivo)
    wave, time, score, timeRefinamento, scoreRefinamento, timeRSO, = construction(pedidos, corredores, LB, UP)
    SalvarResultados(wave, time, score, timeRefinamento, scoreRefinamento, timeRSO, arquivo)

if __name__ == '__main__':
    main()
