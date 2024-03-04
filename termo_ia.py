from requests import get
from unidecode import unidecode
from random import choices

import pandas as pd

alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

pt_br_dictionary = get('https://raw.githubusercontent.com/fserb/pt-br/master/dicio').text.split('\n')

universe = set([unidecode(word) for word in pt_br_dictionary if len(word) == 5])

def stochastic_word_choice(universe):

    words_probability = {} # por posição, por letra

    for i in range(5):

        words_probability[i] = {}

        for letter in alphabet:     

                frequency = 0

                for word in universe:
                    if letter == word[i]:
                        frequency += 1
                
                if len(universe) == 0:
                    words_probability[i][letter] = 0
                else:
                    words_probability[i][letter] = frequency/len(universe)

    words_evaluation = {}    

    for word in universe:
        
        word_evaluation = 1

        for i in range(len(word)):
            word_evaluation *= words_probability[i][word[i]]
        
        words_evaluation[word] = word_evaluation
    
    # !!!
    if len(words_evaluation) == 0:
        raise ValueError('No words in the universe')

    else:
        chosen_word = choices(list(words_evaluation.keys()), list(words_evaluation.values()), k=1)[0]

    return chosen_word

def process_words_feedback(inputed_word, feedback_list, universe):
     
     # feedback = 0 -> não tem a letra
     # feedback = 1 -> tem a letra, mas não na posição
     # feedback = 2 -> tem a letra na posição

    new_universe = universe.copy()

    for i in range(len(feedback_list)):
         
        if feedback_list[i] == 0:
            new_universe = set([word for word in new_universe if inputed_word[i] not in word])

        elif feedback_list[i] == 1:
            new_universe = set([word for word in new_universe if inputed_word[i] != word[i]])
            new_universe = set([word for word in new_universe if inputed_word[i] in word])

        elif feedback_list[i] == 2:
            new_universe = set([word for word in new_universe if inputed_word[i] == word[i]])

        if len(new_universe) == 0:  # Verificar se o universo está vazio
            break  # Se o universo estiver vazio, não há necessidade de continuar a filtragem

    return new_universe

def main(universe=universe):

    right_word = False
    i = 0

    while True:
        
        word_exists = 'n'

        while word_exists == 'n':
        
            word = stochastic_word_choice(universe)
            print(word)

            word_exists = input('Does the word exist? (y/n): ')
          
        feedback = [int(input(f'Feedback for position {i+1}: ')) for i in range(5)]

        if sum(feedback) == 10:
            print(f'The word is {word}')
            break
        
        universe = process_words_feedback(word, feedback, universe)
        
        if len(universe) == 1:
            print(f'The word is {universe.pop()}')
            break

main(universe)