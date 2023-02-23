# NOTA: O programa precisa do arquivo palavras-sete-letras.txt.

import random 
import sys

GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

with open('sevenletterwords.txt') as wordListFile:
    WORDS = wordListFile.readlines()
    for i in range(len(WORDS)):
        WORDS[i] = WORDS[i].strip().upper()


def main():
    input('Pressione Enter para iniciar...')

    gameWords = getWords()
    computerMemory = getComputerMemoryString(gameWords)
    secretPassword = random.choice(gameWords)

    print(computerMemory)
    for triesRemaining in range(4, 0, -1):
        playerMove = askForPlayerGuess(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print('A C C E S S O  G A R A N T I D O')
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print('Accesso Negado ({}/7 corretas)'.format(numMatches))
    print('Sem tentativas. A senha era {}.'.format(secretPassword))


def getWords():

    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord) #acha palavras que não tem letras correspondentes a palavra secreta

    for i in range(500):
        if len(words) == 5:
            break  # Found 5 words, so break out of the loop.

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord) #acha uma palavra com 3 letras e adiciona na matriz de palavras

    for i in range(500):
        if len(words) == 12:
            break  # Quando achar 7 palavras quebra o loop

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord) # adiciona palavras que tem pelo menos uma letra igual a palavra secreta

        while len(words) < 12:
            randomWord = getOneWordExcept(words)
            words.append(randomWord) #adiciona palavras para fechar a matriz

    assert len(words) == 12
    return words


def getOneWordExcept(blocklist=None):
    if blocklist == None:
        blocklist = []

    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def numMatchingLetters(word1, word2):
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def getComputerMemoryString(words):

    # Divide em 2 partes que tem 16 caracteres
    linesWithWords = random.sample(range(16 * 2), len(words))
    # A memoria que ele representa
    memoryAddress = 16 * random.randint(0, 4000)

    # Cria a "memoria" do computador
    computerMemory = []  # Contem 16 strings para cada lado
    nextWord = 0  # O indexador
    for lineNum in range(16):
        # Cria metade da linha como caracteres de lixo
        leftHalf = ''
        rightHalf = ''
        for j in range(16):
            leftHalf += random.choice(GARBAGE_CHARS)
            rightHalf += random.choice(GARBAGE_CHARS)

        if lineNum in linesWithWords:
            # Acha um lugar aleatório para colocar as palavras:
            insertionIndex = random.randint(0, 9)
            # Insere a palavra:
            leftHalf = (leftHalf[:insertionIndex] + words[nextWord]
                + leftHalf[insertionIndex + 7:])
            nextWord += 1
        if lineNum + 16 in linesWithWords:
            # Acha um lugar aleatório para colocar as palavras na do 2º lado:
            insertionIndex = random.randint(0, 9)
            # Insere a palavra:
            rightHalf = (rightHalf[:insertionIndex] + words[nextWord]
                + rightHalf[insertionIndex + 7:])
            nextWord += 1

        computerMemory.append('0x' + hex(memoryAddress)[2:].zfill(4)
                    + '  ' + leftHalf + '    '
                    + '0x' + hex(memoryAddress + (16*16))[2:].zfill(4)
                    + '  ' + rightHalf)

        memoryAddress += 16  # Jump from, say, 0xe680 to 0xe690.

    # Cada string na matriz de memoria do computador é juntada em uma só
    return '\n'.join(computerMemory)


def askForPlayerGuess(words, tries):
    while True:
        print('Insira a senha: ({} tentativas restantes)'.format(tries))
        guess = input('> ').upper()
        if guess in words:
            return guess
        print('Essa palavra não consta nas palavras listadas.')
        print('Tente inserir "{}" ou "{}".'.format(words[0], words[1]))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
         sys.exit()  # Quando Ctrl-C é pressionado, o programa se encerra.