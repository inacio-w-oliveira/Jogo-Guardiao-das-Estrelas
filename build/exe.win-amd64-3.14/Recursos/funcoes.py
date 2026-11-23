import os
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")


def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("log.dat", "r")
        banco.close()
    except:
        print("Log inexistente. Criando...")
        banco = open("log.dat", "w")
        banco.close()


def escreverDados(nome, pontos):
    # Le o log, adiciona a partida (nome, pontos, data, hora) e grava de novo
    banco = open("log.dat", "r")
    dados = banco.read()
    banco.close()
    if dados != "":
        registros = json.loads(dados)
    else:
        registros = []

    dataBr = datetime.now().strftime("%d/%m/%Y")
    horaBr = datetime.now().strftime("%H:%M:%S")
    registros.append([nome, pontos, dataBr, horaBr])

    banco = open("log.dat", "w")
    banco.write(json.dumps(registros))
    banco.close()


def maior_pontuador():
    banco = open("log.dat", "r")
    dados = banco.read()
    banco.close()
    if dados != "":
        registros = json.loads(dados)
    else:
        registros = []

    nomeMaior = None
    dataMaior = None
    horaMaior = None
    maiorPontos = -1

    for nome, pontos, data, hora in registros:
        if pontos > maiorPontos:
            maiorPontos = pontos
            nomeMaior = nome
            dataMaior = data
            horaMaior = hora

    return nomeMaior, maiorPontos, dataMaior, horaMaior
