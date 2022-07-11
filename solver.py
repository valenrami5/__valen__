from api_connection import ApiConnection as apiconn
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import numpy as np
import re
import time

#WORDLE FINALIZADO


class Wordle:
    def __init__(self, raw_words, len_words, len_cons, len_vows):
        self.raw_words = raw_words
        self.len_words = len_words
        self.len_cons = len_cons
        self.len_vows = len_vows
        
    def accepted_words(self):
        accepted_words=[]
        for word in (self.raw_words[0]):
            if len(word)== self.len_words and len(re.findall('[^aeiou]', word))==self.len_cons and len(re.findall('[aeiou]', word))==self.len_vows:
                accepted_words.append(word)
        return accepted_words
        
class Filtro:
    def __init__(self, accepted_words, len_words):
        self.accepted_words = accepted_words
        self.len_words = len_words
    
    def best_word(self):

        #Scoring words, by its letter-position 
        tupla= []
        freq_dict = {i:{} for i in range (self.len_words)}
        for word in self.accepted_words:
            for idx, letter in enumerate(word):
                if letter in freq_dict[idx]:
                    freq_dict[idx][letter]+=1
                else:
                    freq_dict[idx][letter]=1
        x = freq_dict
        for word in self.accepted_words:
            
            # penalize when letters are repeated in words
            probability = len(set(word))/len(word)
            for idx, letter in enumerate(word):
                probability *= x[idx][letter] / len(self.accepted_words)
            tupla.append([probability, word])
        return sorted(tupla, reverse=True)[0][1]

class Solver:
    def __init__(self, word_chose, accepted_words, res, string):
        self.accepted_words = accepted_words
        self.res = res
        self.string = string
        self.word_chose = word_chose

    def wordle_solver(self):
        words_to_remove=[]
        good_letters=[]

        for letter_wrong_position in self.string:
                good_letters.append(letter_wrong_position) 
        for idx, value in enumerate(self.word_chose):
            if self.res[idx] == True:
                good_letters.append(self.word_chose[idx])

        #Removing letter position false and not in list of right_letters_in_wrong_positions
        remove =list(set(self.word_chose) - set(good_letters))
            
        for word in self.accepted_words:
            for position in range(len(self.word_chose)):

                #Removing words that does not have letters in the right position
                if self.res[position] == True and self.word_chose[position] != word[position] and word not in words_to_remove:
                    words_to_remove.append(word)
                    break

                #Removing words that does have letters in the wrong position
                if self.res[position] == False and self.word_chose[position] == word[position] and word not in words_to_remove:
                    words_to_remove.append(word)
                    break

            #Removing words where letters are in position false and not in list of right_letters_in_wrong_positions
            for i in remove:
                if i in word:
                    words_to_remove.append(word)
                    break

            #Removing words that does not have letters from the right_letters_in_wrong_positions list
            for letter_wrong_position in self.string:
                if letter_wrong_position not in word and word not in words_to_remove:
                    #print('yo soy string ' + str(word))
                    words_to_remove.append(word)
                    
                    break
        
        return list(set(self.accepted_words) - set(words_to_remove))


class Interactive():
    def __init__(self):
        pass

    def first_word(self):
        #Requesting game 
        api_connection = apiconn()
        user, pwd, url = api_connection.api_auth()
        response = requests.get(url, auth= (user, pwd))
        info_game = response.json()
        return info_game
    
    def send_word(self, palabra_ideal):
        #Sending results to the API
        self.palabra_ideal = palabra_ideal
        api_connection = apiconn()
        user, pwd, url = api_connection.api_post()
        word = { 
            'result_word': (self.palabra_ideal)
            
            } 
        response = requests.post(url , auth= (user, pwd), json = word)
        send_word_game = response.json()
        return send_word_game

    def game(self):

        #Main code

        raw_words = pd.read_csv("/home/valentina/SOFKA_CODIGO/words_bank.csv", header=None)
        tic = time.perf_counter()
        j = 0
        tries = 0
        
        #Starting the game
        game_info = self.first_word()
        tic_first_word = time.perf_counter()
        cons_len = game_info['consonants']
        vow_len = game_info['vowels']
        game_len = game_info['length_word']
        id = game_info['id']
        score = 0
        score_list = []
        word_send_list = []
        time_array_list = []
        current_attemps_list = []


        #raw data, after filtering by len
        init = Wordle(raw_words,game_len, cons_len,vow_len).accepted_words()
        accepted_word = accepted_word if j>1 else init
        while (score != 1):
            j += 1

            #Getting the ideal word
            palabra_ideal = Filtro(accepted_word, game_len).best_word()

            #Sending the optimal word
            response = self.send_word(palabra_ideal)
            score = response['score']
            print(score)
            right_letters_in_wrong_positions = response['right_letters_in_wrong_positions']
            position_array = response['position_array']
            word_send = response['word_sent']
            time_array = response['try_datetime']
            current_attemps = response['current_attemps']

            #Filtring by api response
            accepted_word = Solver(palabra_ideal, accepted_word, position_array, right_letters_in_wrong_positions).wordle_solver()
            score_list.append(score)
            word_send_list.append(word_send)
            time_array_list.append(time_array)
            current_attemps_list.append(current_attemps)
            

        toc_first_word = time.perf_counter()  
        toc = time.perf_counter() 
        print(f"I found the word in {toc_first_word - tic_first_word:0.4f} seconds, In my {j} try" )
        time_list = [toc - tic] * len(score_list)
        time_list_first_word = [toc_first_word - tic_first_word] * len(score_list)

        #Saving info in a dataframe
        df = pd.DataFrame(zip([id] * len(score_list), score_list, word_send_list, time_list, time_array_list, current_attemps_list, time_list_first_word  ), columns = ['id', 'score', 'word_sent',
                                         'total_time', 'time_array', 'attemps', 'time_find_word'])
        df.to_csv('/home/valentina/SOFKA_CODIGO/csv_words_bank_new/'+str(id)+'.csv', index=False)
        return df, id, score_list, word_send_list, time_list, time_array_list, current_attemps_list, time_list_first_word

