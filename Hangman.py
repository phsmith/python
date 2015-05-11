#!/usr/bin/python3 -tt
# -*- encoding: utf-8 -*-
#
# Author: Phillipe Smith <phillipelnx@gmail.com>
# Description: Simple Python Hangman 
# Version: 1.2

import os, sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from random import randint
from time import sleep

class Hangman:
    
    picture = '''
    +-------+       
    |       |  
    |       O
    |      /|\  
    |      / \  
    |           
===================
'''

    doll = [
        82, # Right leg
        80, # Left leg      
        65, # Right Arm
        63, # Left Arm
        64, # Body
        50, # Head
    ]

    def __init__(self):
        self.errors  = 0
        self.hits    = 0
        
        try:
            print('   JOGO DA FORCA\n====================\n')
            print('Aguarde....\nBuscando lista de palavras no endereço:\nhttp://www.ime.usp.br/~pf/algoritmos/dicios/br .....')
            sleep(5)            
            self.wordlist = urlopen('http://www.ime.usp.br/~pf/algoritmos/dicios/br')
        except HTTPError as e:
            sys.exit('\nO servidor não conseguiu atender a solicitação.\nCódigo do Erro: %d' % e.code)          
        except URLError as e:
            sys.exit('\nFalha ao contactar o servidor.\nCausa: %s' % e.reason)          
        else:
            self.wordlist = self.wordlist.read().decode('iso-8859-1').split()
    
    def play(self):
        self.correct = ''
        self.wrong   = ''       
        self.sorted_word = self.wordlist[randint(0, len(self.wordlist))]
        self.word = ['_'] * (len(self.sorted_word))
                
        while len(self.wrong) <= len(self.doll):
            os.system('cls') if sys.platform.find('win') > -1 else os.system('clear') 
            self.draw()
    
    def kick(self, chars):
        kick = input('Chute uma letra [ 0 = sair ]: ')

        if kick == '0': sys.exit('\nObrigado por jogar!\n')
        
        if kick.isalpha() and len(kick) == 1 and kick not in chars:
            if kick in self.sorted_word:                    
                self.correct += kick        
                for i in range(len(self.sorted_word)):                              
                    if kick == self.sorted_word[i]: 
                        self.word[i] = kick             
            else:
                print('Não há a letra "%s" na palavra... Tente outra...' % kick)
                sleep(5)
                self.wrong += kick
                return kick                     

    def win_or_loose(self):
        if ''.join(self.word) == self.sorted_word:
            self.hits += 1
            print('Você acertou! Parabéns!\n')          
            self.play() if self.again() else sys.exit()
        else:
            if self.n_wrong != len(self.doll):
                self.kick(self.kicks)
            else:
                self.errors += 1
                print('Você Perdeu... A palavra era: %s\n' % self.sorted_word)              
                self.play() if self.again() else sys.exit()
        return 

    def draw(self):
        self.n_wrong = len(self.wrong)
        self.kicks   = self.correct + self.wrong
        draw_picture = self.picture
        draw_header  = '===================='
        draw_points  = '[ Acertos: %s - Erros: %s ]' % (self.hits, self.errors)
        
        if self.n_wrong <= len(self.doll):
            for i in range(self.n_wrong):           
                draw_picture = draw_picture[:self.doll[i]] + ' ' + draw_picture[self.doll[i]+1:]            

            print('   JOGO DA FORCA\t%s\n%s\n%s' % (draw_points, draw_header, draw_picture))            
            print('Chutes: %s\nPalavra: %s\n' % (' '.join(self.kicks), ' '.join(self.word)))

            self.win_or_loose()

    def again(self):
        play_again  = input('Deseja jogar novamente [s ou n]: ')
        self.points = '[ Acertos: %s - Erros: %s ]' % (self.hits, self.errors)
        
        if play_again and play_again[0].lower() == 's':
            print('Aguarde enquanto o jogo é carregado...\n')
            return True
        else:
            print('\nObrigado por jogar!\n')
            return False


if __name__ == '__main__':
    game = Hangman()
    game.play()
    
