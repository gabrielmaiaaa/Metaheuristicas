from Metodos_Arquivos.arquivo import *
from Operacao.operacao import *

def main():
    arquivo = 'instance_0020'
    instancia = LerArquivo(arquivo)
    Operar(instancia)

if __name__ == '__main__':
    main()