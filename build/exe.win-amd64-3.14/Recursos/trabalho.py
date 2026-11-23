# Funcoes novas do trabalho (item 7)
import pyttsx3


def colidiu(x1, y1, l1, a1, x2, y2, l2, a2):
    # Devolve True se o retangulo 1 encostou no retangulo 2
    return x1 < x2 + l2 and x1 + l1 > x2 and y1 < y2 + a2 and y1 + a1 > y2


def falar(texto):
    # Usa a biblioteca pyttsx3 para falar o texto
    try:
        voz = pyttsx3.init()
        voz.setProperty("rate", 170)
        voz.say(texto)
        voz.runAndWait()
    except:
        print("Nao foi possivel falar:", texto)
