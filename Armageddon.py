import pygame , sys
from pygame.locals import *
from random import randrange
import random

#importando os modulos
pygame.init() #função para iniciar pygame
pygame.font.init() #função para iniciar as fontes
pygame.mixer.pre_init(44100, 32, 2, 4096) #função do audio

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)

#tamanho da tela
screen = pygame.display.set_mode((1200, 560), 0, 32)

#carregando a imagem de background
background_filename = 'menu.png'
background = pygame.image.load(background_filename).convert()

#Posição de inicio do background
screen.blit(background, (0, 0))

#classe para eventos no menu
class Option:

    hovered = False
    
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
            
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (255, 255, 255) #Botão branco quando o mouse está em cima da string START
        else:
            return (255, 0, 0) #Botão vermelho quando o mouse não esta em cima da string START
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
LEFT = 1
menu_font = pygame.font.Font(None,85) #Fonte do botão START e tamanho
opicoes = [Option("START", (520, 280)) ] #String do botão no menu inicial e localização da String
def inciar(): #Começando o jogo
    #tamanho da tela
    screen = pygame.display.set_mode((1200, 560), 0, 32)

    #carregando a imagem de background
    background_filename = 'jogo.png'
    background = pygame.image.load(background_filename).convert()

    #Musica
    music = pygame.mixer.music
    music.load('audio1.mp3')

    #Criação da nave
    ship = {
        'surface': pygame.image.load('ship.png').convert_alpha(), #Carregando imagem da nave
        'position': [(450), (320)], #Posição inicial
        'speed': { 
            'x': 0,
            'y': 0
        }
    }

    #Explosão da nave
    exploded_ship = {
        'surface': pygame.image.load('ship_exploded.png').convert_alpha(), #Carrega imagem de explosão
        'position': [],
        'speed': {
            'x': 0,
            'y': 0
        },
        'rect': Rect(0, 0, 48, 48) #Tamanho da nave
    }

    explosion_sound = pygame.mixer.Sound('boom.wav') #Carregando barulho da explosão
    explosion_played = False

    clock = pygame.time.Clock() #Usado para controlar os fps dos objetos

    #Lista de imagens dos objetos
    meteoros = ['objt1.png', 'objt2.png', 'objt3.png', 'objt4.png', 'objt5.png',
                'objt6.png', 'objt7.png', 'objt8.png', 'objt9.png', 'objt10.png',
                'objt11.png', 'objt12.png']

    #Criando asteroides
    def create_asteroid():
        return {
            'surface': pygame.image.load(random.choice(meteoros)).convert_alpha(), #Carregando asteroides aleatorios de uma lista
            'position': [randrange(892), -64], #Criando asteroides do ponto 0 até o 892 em X, a partir do ponto -64 em Y
            'speed': (random.choice(velocidade_asteroide)) #Velocidade aleatoria de uma lista de valores
        }

    ticks_to_asteroid = 90 #Velocidade de criação dos asteroides
    asteroids = [] #Lista dos asteroides criados e em uso
    score = 0 #Pontuação inicial
    score = float(score) #Conversão para poder comparar com o recorde no arquivo
    arquivo = open('Best Score.txt', 'r') #Abrindo arquivo
    for i in arquivo: #Lendo arquivo com 'for'
        i = float(i) #Convertendo indice do arquivo em flutuante para exibir e comparar com a nova pontuação
        highscore = i #Variavel da maior pontuação
    arquivo.close() #Fechando arquivo

    def move_asteroids(): #Forma que se move o asteroide
        for asteroid in asteroids: #Lendo a lista de asteroides
            asteroid['position'][1] += asteroid['speed'] #Velocidade do asteroide percorrendo em X
            
    def remove_used_asteroids(): #Removendo asteroide apos o uso
        for asteroid in asteroids: #Lendo a lista de asteroides
            if asteroid['position'][1] > 560: #Se o asteroide passar o ponto 560 em x
                asteroids.remove(asteroid) #Removendo asteroide da lista

    def get_rect(obj): #Obetendo o retangulo do objeto para colisão
        return Rect(obj['position'][0],
                    obj['position'][1],
                    obj['surface'].get_width(),
                    obj['surface'].get_height())

    def ship_collided(): #Verificando se o retangulo da nave esta na mesma posição do retangulo do objeto
        ship_rect = get_rect(ship)
        for asteroid in asteroids:
            if ship_rect.colliderect(get_rect(asteroid)):
                return True
        return False

    collided = False
    collision_animation_counter = 0

    def drawScore(ponto):
        font = pygame.font.SysFont(None, 45) #Fonte do score e tamanho da fonte
        scoreSurf = font.render('Score: %.0f' % (ponto), True, (255, 255, 255)) #String do score e cor da string
        screen.blit(scoreSurf, (976,10)) #Posição da string

    def Nivel(nivel):
        font = pygame.font.SysFont(None, 45) #Fonte do nivel e tamanho da fonte
        nivelSurf = font.render('Nivel: %s' % (nivel), True, (255, 255, 255)) #String do nivel e cor da string
        screen.blit(nivelSurf, (976,50)) #Posição da string

    def bestscore(highscore):
        font = pygame.font.SysFont(None, 45) #Fonte da melhor pontuação e tamanho da fonte
        bestscoreSurf = font.render('Record: %.0f' % (highscore), True, (255, 255, 255)) #String do High Score e cor da string
        screen.blit(bestscoreSurf, (976, 90)) #Posição da string

    velocidade_criação_asteroides = 60 #Velocidade de criação dos objetos
    velocidade_asteroide = [4, 5, 6 , 7] #Velocidade dos objetos
    nivel = 1 #Nivel de velocidade
    cont = 0 #Contavel para nao ficar repetindo atualização da velocidade mais de uma vez

    music.play(loops=10) #Quantidade de vezes que a musica vai ser repetida

    tenpofim=0
    
    while True:

        if not ticks_to_asteroid:
            ticks_to_asteroid = velocidade_criação_asteroides
            asteroids.append(create_asteroid())
        else:
            ticks_to_asteroid -= 1

        ship['speed'] = {
            'x': 0,
            'y': 0
        }

        for event in pygame.event.get(): #Fechando a janela na parte do jogo caso aperte 'Fechar'
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP] and int(ship['position'][1]) >= 5: #Botão para cima com limite de tela até o ponto 5 em Y
            ship['speed']['y'] = -10 #Atualização da nave para cima em Y
        elif pressed_keys[K_DOWN] and int(ship['position'][1]) <= 510: #Botão para baixo com limite de tela até o ponto 510 em Y
            ship['speed']['y'] = 10 #Atualização da nave para baixo em Y

        if pressed_keys[K_LEFT] and int(ship['position'][0]) >= 5: #Botão para esquerda com limite de tela até o ponto 5 em X
            ship['speed']['x'] = -10 #Atualização da nave para esquerda em X
        elif pressed_keys[K_RIGHT] and int(ship['position'][0]) <= 905: #Botão para direita com limite de tela até o ponto 905 em X
            ship['speed']['x'] = 10 #Atualização da nave para direita em X

        screen.blit(background, (0, 0)) #Posição de inicio do background

        move_asteroids() #Chamando função de mover asteroides

        for asteroid in asteroids:
            screen.blit(asteroid['surface'], asteroid['position'])
        if not collided:
            collided = ship_collided()
            ship['position'][0] += ship['speed']['x']
            ship['position'][1] += ship['speed']['y']
            score += 0.05 #Atualização da pontuação gradativamente
            arquivo = open('Best Score.txt', 'w') #Comparando e escrevendo novo recorde no arquivo
            score = float(score)
            highscore = float(highscore)
            if score > highscore:
                highscore = score
            highscore = str(highscore)
            arquivo.write(highscore)
            arquivo.close()
            highscore = float(highscore)
            if score > 100:
                nivel = 2 #Atualização do nivel
                while cont < 1: #Atualizando a lista de velocidade dos objetos
                    for i in velocidade_asteroide:
                        i += 3 #Atualizando cada indice da lista em +3
                        cont += 1
                velocidade_criação_asteroides = 48 #Atualização da velocidade de criação dos objetos
                score += 0.1 #Atualização da pontuação gradativamente
                if score > 250:
                    nivel = 3 #Atualização do nivel
                    while cont < 2: #Atualizando a lista de velocidade dos objetos
                        for i in velocidade_asteroide:
                            i += 3 #Atualizando cada indice da lista em +3
                            cont += 1
                    velocidade_criação_asteroides = 35 #Atualização da velocidade de criação dos objetos
                    score += 0.15 #Atualização da pontuação gradativamente
                    if score > 500:
                        nivel = 4 #Atualização do nivel
                        while cont < 3: #Atualizando a lista de velocidade dos objetos
                            for i in velocidade_asteroide:
                                i += 3 #Atualizando cada indice da lista em +3
                                cont += 1
                        velocidade_criação_asteroides = 22 #Atualização da velocidade de criação dos objetos
                        score += 0.25 #Atualização da pontuação gradativamente
                        if score > 1000:
                            nivel = 5 #Atualização do nivel
                            while cont < 4: #Atualizando a lista de velocidade dos objetos
                                for i in velocidade_asteroide:
                                    i += 3 #Atualizando cada indice da lista em +3
                                    cont += 1
                            velocidade_criação_asteroides = 15 #Atualização da velocidade de criação dos objetos
                            score += 0.5 #Atualização da pontuação gradativamente
                            if score > 2000:
                                nivel = 6 #Atualização do nivel
                                while cont < 5: #Atualizando a lista de velocidade dos objetos
                                    for i in velocidade_asteroide:
                                        i += 3 #Atualizando cada indice da lista em +3
                                        cont += 1
                                velocidade_criação_asteroides = 8 #Atualização da velocidade de criação dos objetos
                                score += 1 #Atualização da pontuação gradativamente
                                if score > 4000:
                                    nivel = 7 #Atualização do nivel
                                    while cont < 6: #Atualizando a lista de velocidade dos objetos
                                        for i in velocidade_asteroide:
                                            i += 3 #Atualizando cada indice da lista em +3
                                            cont += 1
                                    velocidade_criação_asteroides = 6 #Atualização da velocidade de criação dos objetos
                                    score += 1.5 #Atualização da pontuação gradativamente


            screen.blit(ship['surface'], ship['position'])
        else:
            if not explosion_played:
                music.stop() #Parando a musica principal
                explosion_played = True
                explosion_sound.play() #Iniciando musica da explosão
                ship['position'][0] += ship['speed']['x'] #Parando a nave em X
                ship['position'][1] += ship['speed']['y'] #Parando a nave em Y

                screen.blit(ship['surface'], ship['position']) #Parando a nave para explosão
            elif collision_animation_counter == 3: #Depois que passar a ultima animação da explosão
                text = game_font.render('GAME OVER', 1, (255, 0, 0)) #Texto para exibir no fim do jogo e cor da fonte
                screen.blit(text, (335, 250)) #Atualizando a tela com o texto nessa posição
                tenpofim+=1 
                if tenpofim==100: #tempo que passa entre o GAME OVER até voltar para o menu inicial
                    return() #retornar ao menu
            else:
                exploded_ship['rect'].x = collision_animation_counter * 48
                exploded_ship['position'] = ship['position'] #A posição que vai explodir é a posição que a nave se encontra
                screen.blit(exploded_ship['surface'], exploded_ship['position'], #Atualização da sequencia de imagens da explosão na posição que a nave estava
                            exploded_ship['rect'])
                collision_animation_counter += 1 #Passando animações da sequencia de imagem da explosão
        drawScore(score) #Chamando função de exibição da pontuação
        Nivel(nivel) #Chamando função de exibição do nivel
        bestscore(highscore) #Chamando função de exibição da maior pontuação

        pygame.display.update()
        time_passed = clock.tick(30) #Controlar o fps do jogo
        remove_used_asteroids() #Chamando função de remover asteroides

pygame.display.set_caption('Armageddon') #Nome da janela
while True:
    pygame.event.pump() #Manipulador de evento interno das telas apresentadas
    screen.blit(background, (0, 0)) #Atualizando a tela com a imagem nessa posição
    event = pygame.event.poll() #Obter o unico evento da fila de eventos
    if event.type == QUIT: #Fechando a janela na parte do menu inicial caso aperte 'Fechar'
        pygame.quit()
        sys.exit()
    for option in opicoes:
        if option.rect.collidepoint(pygame.mouse.get_pos()): #verifica se o mouse ta em cima
            option.hovered = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: #verifica se foi clicado
                inciar()
    
        else:
            option.hovered = False
        option.draw()
    pygame.display.update()

