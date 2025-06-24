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
    tempoDedicado = 0.1
    match arquivo:
        case "instance_0001":
            tempoDedicado = 0.1
        case "instance_0002":
            tempoDedicado = 0.1
        case "instance_0003":
            tempoDedicado = 3
        case "instance_0004":
            tempoDedicado = 3
        case "instance_0005":
            tempoDedicado = 3
        case "instance_0006":
            tempoDedicado = 3
        case "instance_0007":
            tempoDedicado = 3
        case "instance_0008":
            tempoDedicado = 3
        case "instance_0009":
            tempoDedicado = 3
        case "instance_0010":
            tempoDedicado = 3
        case "instance_0011":
            tempoDedicado = 3
        case "instance_0012":
            tempoDedicado = 1
        case "instance_0013":
            tempoDedicado = 3
        case "instance_0014":
            tempoDedicado = 3
        case "instance_0015":
            tempoDedicado = 3
        case "instance_0016":
            tempoDedicado = 0.1
        case "instance_0017":
            tempoDedicado = 0.1
        case "instance_0018":
            tempoDedicado = 1
        case "instance_0019":
            tempoDedicado = 1
        case "instance_0020":
            tempoDedicado = 0.1
    pedidos, corredores, LB, UB = Operar(instancia)
    SalvarArquivo(pedidos, corredores, LB, UB, arquivo)
    wave, time, score, timeRefinamento, scoreRefinamento, timeRSO, interacao, execucao = construction(pedidos, corredores, LB, UB, tempoDedicado)
    # print(wave)
    SalvarResultados(wave, time, score, timeRefinamento, scoreRefinamento, timeRSO, arquivo, interacao, execucao)

if __name__ == '__main__':
    main()
