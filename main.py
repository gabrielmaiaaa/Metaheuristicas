from Metodos_Arquivos.arquivo import *
from Operacao.operacao import *
from Heuristic.heuristic import *

def main():
    names = ['instance_0001', 'instance_0002', 'instance_0003', 'instance_0004', 'instance_0005',
             'instance_0006', 'instance_0007', 'instance_0008', 'instance_0009', 'instance_0010',
             'instance_0011', 'instance_0012', 'instance_0013', 'instance_0014', 'instance_0015',
             'instance_0016', 'instance_0017', 'instance_0018', 'instance_0019', 'instance_0020'
             ]
    for name in names:
        # arquivo = 'instance_0005'
        instancia = LerArquivo(name)
        pedidos, corredores, LB, UP = Operar(instancia)
        SalvarArquivo(pedidos, corredores, LB, UP,name)
        wave, time, timeRSO = construction(pedidos, corredores, LB, UP)
        SalvarResultados(wave, time, timeRSO, name)

if __name__ == '__main__':
    main()