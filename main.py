import pygame
import random
from sys import exit
from Recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from Recursos.trabalho import colidiu, falar

limpar_tela()
inicializarBancoDeDados()
pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if nome != "":
        break
    else:
        print("Nome Inválido!")

tamanho = (1000, 700)
pygame.display.set_caption("Guardião das Estrelas")
icone = pygame.image.load("bases/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
branco = (255, 255, 255)
preto = (0, 0, 0)
cinza = (170, 170, 180)
amarelo = (255, 235, 120)
vermelho = (255, 90, 70)

fundo = pygame.image.load("bases/fundo.png")
fundoStart = pygame.image.load("bases/fundoInicio.png")
fundoDead = pygame.image.load("bases/fundoFim.png")

nave = pygame.image.load("bases/nave.png")
nave = pygame.transform.scale(nave, (55, 108))
meteoro = pygame.image.load("bases/meteoro.png")
meteoro = pygame.transform.scale(meteoro, (80, 80))
satelite = pygame.image.load("bases/satelite.png")
satelite = pygame.transform.scale(satelite, (120, 28))
pontoSound = pygame.mixer.Sound("bases/ponto.wav")
explosaoSound = pygame.mixer.Sound("bases/explosao.wav")
pygame.mixer.music.load("bases/musica.ogg")


explosaoQuadros = []
for i in range(1, 7):
    quadro = pygame.image.load("bases/explosao" + str(i) + ".png")
    quadro = pygame.transform.scale(quadro, (160, 160))
    explosaoQuadros.append(quadro)

fonteMenu = pygame.font.SysFont("arial", 28)
fontePequena = pygame.font.SysFont("arial", 18)
fonteGrande = pygame.font.SysFont("arial", 60)


def escrever(texto, fonte, cor, x, y):
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def explodir(x, y):
    
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    for quadro in explosaoQuadros:
        for espera in range(8):
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    exit()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    exit()
            tela.blit(fundo, (0, 0))
            tela.blit(quadro, (x - 80, y - 80))
            pygame.display.update()
            relogio.tick(60)


def jogar():
    posicaoXNave = 472
    posicaoYNave = 580
    movimentoXNave = 0
    velocidadeMovNave = 8
    pontos = 0
    pausado = False
    fundoMov = 0

    
    meteoros = []
    for i in range(5):
        meteoros.append([random.randint(0, 920), random.randint(-600, -90), random.randint(4, 6)])

    
    posicaoXSatelite = 300
    posicaoYSatelite = 200
    movimentoXSatelite = 2
    movimentoYSatelite = 1

    
    raioLua = 40.0
    mudancaLua = 0.15

    pygame.mixer.music.play(-1)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXNave = velocidadeMovNave
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXNave = -velocidadeMovNave
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXNave = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXNave = 0

        if pausado == False:
            
            posicaoXNave = posicaoXNave + movimentoXNave
            if posicaoXNave < 0:
                posicaoXNave = 0
            elif posicaoXNave > 945:
                posicaoXNave = 945

            fundoMov += 2
            if fundoMov >= 700:
                fundoMov = 0

            for m in meteoros:
                m[1] += m[2]
                if m[1] > 700:
                    m[0] = random.randint(0, 920)
                    m[1] = -90
                    m[2] += 0.2
                    if m[2] > 12:
                        m[2] = 12
                    pontos += 1
                    pygame.mixer.Sound.play(pontoSound)
                if colidiu(posicaoXNave + 8, posicaoYNave + 8, 39, 92, m[0] + 10, m[1] + 10, 60, 60):
                    escreverDados(nome, pontos)
                    explodir(posicaoXNave + 27, posicaoYNave + 54)
                    dead(pontos)

            
            if random.randint(1, 40) == 1:
                movimentoXSatelite = random.randint(-3, 3)
                movimentoYSatelite = random.randint(-3, 3)
            posicaoXSatelite += movimentoXSatelite
            posicaoYSatelite += movimentoYSatelite
            if posicaoXSatelite < 0:
                posicaoXSatelite = 0
                movimentoXSatelite = 2
            elif posicaoXSatelite > 880:
                posicaoXSatelite = 880
                movimentoXSatelite = -2
            if posicaoYSatelite < 0:
                posicaoYSatelite = 0
                movimentoYSatelite = 2
            elif posicaoYSatelite > 400:
                posicaoYSatelite = 400
                movimentoYSatelite = -2

            
            raioLua += mudancaLua
            if raioLua > 60:
                mudancaLua = -0.15
            elif raioLua < 40:
                mudancaLua = 0.15

        tela.fill(branco)
        tela.blit(fundo, (0, fundoMov))
        tela.blit(fundo, (0, fundoMov - 700))
        pygame.draw.circle(tela, amarelo, (900, 90), int(raioLua))
        tela.blit(satelite, (posicaoXSatelite, posicaoYSatelite))
        for m in meteoros:
            tela.blit(meteoro, (m[0], m[1]))
        tela.blit(nave, (posicaoXNave, posicaoYNave))

        escrever("Pontos: " + str(pontos), fonteMenu, branco, 20, 15)
        escrever("Press Space to Pause Game", fontePequena, cinza, 10, 670)
        if pausado:
            escrever("PAUSE", fonteGrande, branco, 402, 320)

        pygame.display.update()
        relogio.tick(60)


def dead(pontos):
    pygame.mixer.music.stop()
    nomeMaior, maiorPontos, dataMaior, horaMaior = maior_pontuador()
    larguraButtonStart = 200
    alturaButtonStart = 50
    larguraButtonQuit = 200
    alturaButtonQuit = 50
    startButton = pygame.draw.rect(tela, branco, (280, 520, larguraButtonStart, alturaButtonStart), border_radius=15)
    quitButton = pygame.draw.rect(tela, branco, (520, 520, larguraButtonQuit, alturaButtonQuit), border_radius=15)
    primeiraVez = True
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 190
                    alturaButtonStart = 45
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 190
                    alturaButtonQuit = 45
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 200
                    alturaButtonStart = 50
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    exit()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))
        escrever("FIM DE JOGO", fonteGrande, vermelho, 310, 100)
        escrever(f"{nome}, você fez {pontos} pontos", fonteMenu, branco, 250, 236)
        escrever("Maior pontuação:", fonteMenu, cinza, 250, 326)
        escrever(f"{nomeMaior} - {maiorPontos} pontos", fonteMenu, amarelo, 250, 371)
        escrever(f"em {dataMaior} às {horaMaior}", fonteMenu, amarelo, 250, 411)

        startButton = pygame.draw.rect(tela, branco, (280, 520, larguraButtonStart, alturaButtonStart), border_radius=15)
        escrever("Jogar de novo", fonteMenu, preto, 295, 531)
        quitButton = pygame.draw.rect(tela, branco, (520, 520, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        escrever("Sair do Game", fonteMenu, preto, 537, 531)

        pygame.display.update()
        relogio.tick(60)

        if primeiraVez:
            primeiraVez = False
            falar(f"Fim de jogo. {nome}, você fez {pontos} pontos")


def start():
    nomeMaior, maiorPontos, dataMaior, horaMaior = maior_pontuador()
    larguraButtonStart = 200
    alturaButtonStart = 60
    startButton = pygame.draw.rect(tela, branco, (400, 590, larguraButtonStart, alturaButtonStart), border_radius=15)
    primeiraVez = True
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 190
                    alturaButtonStart = 55
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 200
                    alturaButtonStart = 60
                    jogar()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))
        escrever("GUARDIÃO DAS ESTRELAS", fonteGrande, amarelo, 116, 47)
        escrever(f"Bem-vindo(a), {nome}!", fonteMenu, branco, 300, 156)

        escrever("Pilote a nave e desvie dos meteoros que caem do espaço.", fonteMenu, cinza, 151, 226)
        escrever("Use as setas esquerda e direita para mover a nave.", fonteMenu, cinza, 191, 266)
        escrever("Cada meteoro desviado vale 1 ponto, mas eles ficam mais rápidos.", fonteMenu, cinza, 98, 306)
        escrever("Se um meteoro encostar na nave, o jogo termina.", fonteMenu, cinza, 205, 346)

        if nomeMaior == None:
            escrever("Ainda não há recorde. Seja o primeiro!", fonteMenu, amarelo, 269, 446)
        else:
            escrever(f"Maior pontuador: {nomeMaior} - {maiorPontos} pontos", fonteMenu, amarelo, 150, 436)
            escrever(f"em {dataMaior} às {horaMaior}", fonteMenu, amarelo, 150, 476)

        startButton = pygame.draw.rect(tela, (40, 110, 210), (400, 590, larguraButtonStart, alturaButtonStart), border_radius=15)
        escrever("INICIAR", fonteMenu, branco, 450, 606)

        pygame.display.update()
        relogio.tick(60)

        if primeiraVez:
            primeiraVez = False
            falar(f"Bem vindo, {nome}")


start()
