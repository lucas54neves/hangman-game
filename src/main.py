import requests
import random
from unidecode import unidecode

# Funcao que faz um webscript no site do Wiktionary e busca uma lista de palavras
# em portugues, retornando um array com as palavras
def get_words():
    response = requests.get('https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/BrazilianPortuguese_wordlist')

    text = response.text.split('<li><span lang="pt"><a href="/wiki/')[1:]

    return [element.split('>')[1].split('<')[0] for element in text]

# Funcao que gera uma palavra aleatoria de acordo com a dificuldade inserida, retornando
# uma string
def get_random_word(difficulty):
    print('Gerando a palavra ...')

    if difficulty == 1:
        words = [word for word in get_words() if len(word) < 4]

    if difficulty == 2:
        words = [word for word in get_words() if len(word) >= 4 and len(word) <= 6]

    if difficulty == 3:
        words = [word for word in get_words() if len(word) > 6]

    return unidecode(random.choice(words))

# Exibe a imagem do boneco do jogo de acordo com a quantidade de erros do jogador
def print_person(number):
    if (number == 0):
        print()
        print()
        print()
        print()
    elif (number == 1):
        print('       O')
        print()
        print()
        print()
    elif (number == 2):
        print('       O')
        print('      /')
        print()
        print()
    elif (number == 3):
        print('       O')
        print('      / \\')
        print()
        print()
    elif (number == 4):
        print('       O')
        print('      /|\\')
        print('       |')
        print()
    elif (number == 5):
        print('       O')
        print('      /|\\')
        print('       |')
        print('      /')
    elif (number == 6):
        print('       O')
        print('      /|\\')
        print('       |')
        print('      / \\')

# Funcao que recebe o array com as letras e retorna uma string com a forma que
# a palavra deve ser exibida
def return_word(word):
    display_word = ''

    for letter in word:
        display_word += letter

    return display_word

# Funcao que atualiza a palavra de exibicao, recebendo a letra que deseja atualizar, a palavra
# secreta e a palavra de exibicao desatualizada e retorna a palavra atualizada
def update_word(letter, word, display_word):
    for i in range(len(word)):
        if word[i] == letter:
            display_word[i] = letter

    return display_word

# Funcao que verifica se o jogador ganhou retornando um booleano
def you_win(word):
    return not '_' in word

# Funcao principal do jogo. O funcionamento do jogo funciona a partir
# de um loop que para apenas se o jogador ganhar ou errar seis vezes.
# No final do jogo, o usuario e perguntado se deseja jogar novamente.
def game():
    file = open('logs.txt', 'a', encoding='utf-8')

    attempts = []

    wrong_attempts = []

    print('O jogo vai começar!')

    name = input('Qual seu nome? ')
    
    print('Entre com a dificuldade desejada.')

    print('[1 - fácil / 2 - médio / 3 - difícil]')

    difficulty = int(input('Dificuldade: '))

    while difficulty != 1 and difficulty != 2 and difficulty != 3:
        print('Dificuldade não cadastrada. Tente novamente.')

        difficulty = int(input('Dificuldade: '))

    word = get_random_word(difficulty)

    display_word = ['_' for element in range(0, len(word))]

    while len(wrong_attempts) < 6 and not you_win(display_word):
        print('==================')

        print('      Você')

        print_person(len(wrong_attempts))

        print('==================')

        print('Letras já utilizadas {}.'.format(attempts))

        print('Palavra: {}'.format(return_word(display_word)))

        print('Quantidade de letras da palavras: {}'.format(len(word)))

        letter = input('Entre com uma letra: ').lower()

        if len(letter) != 1:
            print('Entrada de dados inválida. Entre com apenas uma letra.')

            continue

        if letter in attempts:
            print('Entrada de dados inválida. Letra já utilizada.')

            continue

        attempts.append(letter)

        if letter in word:
            print('Você acertou a letra {}.'.format(letter.upper()))

            display_word = update_word(letter, word, display_word)
        else:
            print('Você errou. Não tem a letra {} na palavra.'.format(letter.upper()))

            wrong_attempts.append(letter)

        answer = 'não'

        if you_win(display_word):
            print('Parabéns! Você venceu!')

            print('A palavra é {}.'.format(word))

            answer = input('Deseja jogar novamente? [sim / não] ')

            file.write(f'{name}\t{word}\t{len(attempts)}\t{len(wrong_attempts)}\n')

        elif len(wrong_attempts) == 6:
            print('Sinto muito! Você perdeu.')

            print('A palavra é {}.'.format(word))

            answer = input('Deseja jogar novamente? [sim / não] ')

            file.write(f'{name}\t{word}\t{len(attempts)}\t{len(wrong_attempts)}\n')

        if answer == 'sim':
            attempts = []

            wrong_attempts = []

            print('O jogo vai começar! Entre com a dificuldade desejada.')

            print('[1 - fácil / 2 - médio / 3 - difícil]')

            difficulty = int(input('Dificuldade: '))

            while difficulty != 1 and difficulty != 2 and difficulty != 3:
                print('Dificuldade não cadastrada. Tente novamente.')

                difficulty = int(input('Dificuldade: '))

            word = get_random_word(difficulty)

            display_word = ['_' for element in range(0, len(word))]
    
    file.close()

game()