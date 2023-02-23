# NOTA: O programa precisa do arquivo palavras-sete-letras.txt.

import random 
import sys

GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

with open('palavras-sete-letras.txt') as arquivoListaPalavras:
    PALAVRAS = arquivoListaPalavras.readlines()
    for i in range(len(PALAVRAS)):
        PALAVRAS[i] = PALAVRAS[i].strip().upper()


def main():
    input('Pressione Enter para iniciar...')

    gamePalavras = getPalavras()
    memoriaComputador = getMemoriaComputadorString(gamePalavras)
    senhaSecreta = random.choice(gamePalavras)

    print(memoriaComputador)
    for tentativasRestantes in range(4, 0, -1):
        movimentoJogador = pergunteChuteJogador(gamePalavras, tentativasRestantes)
        if movimentoJogador == senhaSecreta:
            print('A C C E S S O  G A R A N T I D O')
            return
        else:
            numeroLetrasCorretas = numeroLetrasRelacionadas(senhaSecreta, movimentoJogador)
            print('Accesso Negado ({}/7 corretas)'.format(numeroLetrasCorretas))
    print('Sem tentativas. A senha era {}.'.format(senhaSecreta))


def getPalavras():

    senhaSecreta = random.choice(PALAVRAS)
    palavras = [senhaSecreta]

    while len(palavras) < 3:
        palavraAleatoria = getUmaPalavraExceto(palavras)
        if numeroLetrasRelacionadas(senhaSecreta, palavraAleatoria) == 0:
            palavras.append(palavraAleatoria) #acha palavras que não tem letras correspondentes a palavra secreta

    for i in range(500):
        if len(palavras) == 5:
            break  # Found 5 palavras, so break out of the loop.

        palavraAleatoria = getUmaPalavraExceto(palavras)
        if numeroLetrasRelacionadas(senhaSecreta, palavraAleatoria) == 3:
            palavras.append(palavraAleatoria) #acha uma palavra com 3 letras e adiciona na matriz de palavras

    for i in range(500):
        if len(palavras) == 12:
            break  # Quando achar 7 palavras quebra o loop

        palavraAleatoria = getUmaPalavraExceto(palavras)
        if numeroLetrasRelacionadas(senhaSecreta, palavraAleatoria) != 0:
            palavras.append(palavraAleatoria) # adiciona palavras que tem pelo menos uma letra igual a palavra secreta

        while len(palavras) < 12:
            palavraAleatoria = getUmaPalavraExceto(palavras)
            palavras.append(palavraAleatoria) #adiciona palavras para fechar a matriz

    assert len(palavras) == 12
    return palavras


def getUmaPalavraExceto(blocklist=None):
    if blocklist == None:
        blocklist = []

    while True:
        palavraAleatoria = random.choice(PALAVRAS)
        if palavraAleatoria not in blocklist:
            return palavraAleatoria


def numeroLetrasRelacionadas(word1, word2):
    ocorrencias = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            ocorrencias += 1
    return ocorrencias


def getMemoriaComputadorString(palavras):

    # Divide em 2 partes que tem 16 caracteres
    linhasComPalavras = random.sample(range(16 * 2), len(palavras))
    # A memoria que ele representa
    enderecoMemoria = 16 * random.randint(0, 4000)

    # Cria a "memoria" do computador
    memoriaComputador = []  # Contem 16 strings para cada lado
    proximaPalavra = 0  # O indexador
    for numeroLinha in range(16):
        # Cria metade da linha como caracteres de lixo
        parteEsquerda = ''
        parteDireita = ''
        for j in range(16):
            parteEsquerda += random.choice(GARBAGE_CHARS)
            parteDireita += random.choice(GARBAGE_CHARS)

        if numeroLinha in linhasComPalavras:
            # Acha um lugar aleatório para colocar as palavras:
            indexInseracao = random.randint(0, 9)
            # Insere a palavra:
            parteEsquerda = (parteEsquerda[:indexInseracao] + palavras[proximaPalavra]
                + parteEsquerda[indexInseracao + 7:])
            proximaPalavra += 1
        if numeroLinha + 16 in linhasComPalavras:
            # Acha um lugar aleatório para colocar as palavras na do 2º lado:
            indexInseracao = random.randint(0, 9)
            # Insere a palavra:
            parteDireita = (parteDireita[:indexInseracao] + palavras[proximaPalavra]
                + parteDireita[indexInseracao + 7:])
            proximaPalavra += 1

        memoriaComputador.append('0x' + hex(enderecoMemoria)[2:].zfill(4)
                    + '  ' + parteEsquerda + '    '
                    + '0x' + hex(enderecoMemoria + (16*16))[2:].zfill(4)
                    + '  ' + parteDireita)

        enderecoMemoria += 16  # Jump from, say, 0xe680 to 0xe690.

    # Cada string na matriz de memoria do computador é juntada em uma só
    return '\n'.join(memoriaComputador)


def pergunteChuteJogador(palavras, tentativas):
    while True:
        print('Insira a senha: ({} tentativas restantes)'.format(tentativas))
        chute = input('> ').upper()
        if chute in palavras:
            return chute
        print('Essa palavra não consta nas palavras listadas.')
        print('Tente inserir "{}" ou "{}".'.format(palavras[0], palavras[1]))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
         sys.exit()  # Quando Ctrl-C é pressionado, o programa se encerra.