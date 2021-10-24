import requests
import random
from bs4 import BeautifulSoup as bs


def online():
    if requests.get('https://polechudes-otvet.ru/').status_code == 200:
        return True
    else:
        return False


def questionlink():
    url = 'https://polechudes-otvet.ru/'
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    questions = soup.find_all('a')
    for i in range(len(questions)):
        if i < 3 or i > len(questions) - 7:
            questions[i] = None
        else:
            questions[i] = str(questions[i])[9:44]
    for i in range(0, questions.count(None)):
        questions.remove(None)
    qlink = random.choice(questions)
    while not check(qlink):
        qlink = random.choice(questions)
    return qlink


def check(x):
    url = x
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    if str(soup) == '':
        return False
    else:
        return True


def getqna(x):
    url = x
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    qna = [str(soup.find_all('h1'))[25:-6], random.choice(str(soup.find_all('strong'))[16:-10].split('/'))]
    for i in range(len(qna[1])):
        if ord(qna[1][i]) >= 1072:
            qna[1] = qna[1][:i] + chr(ord(qna[1][i]) - 32) + qna[1][i + 1:]
    return qna


def spin():
    baraban = random.randrange(34)
    if baraban <= 30:
        baraban *= 50
    elif baraban == 31:
        baraban = 'Б'
    elif baraban == 32:
        baraban = '+'
    elif baraban == 33:
        baraban = 'x2'
    return baraban


def main():
    while 1:
        if online():
            questionandanswer = getqna(questionlink())
            sw = ''
            points = 0
            for i in range(len(questionandanswer[1])):
                sw += '_'
            print('ПОЛЕ ЧУДЕС\nВопрос : ' + questionandanswer[0])
            while sw != questionandanswer[1]:
                print(sw)
                sector = spin()
                zap = False
                print('Cектор ' + str(sector) + ' на барабане.')
                if sector == 'Б':
                    print('Вы банкрот.')
                    points = 0
                elif sector == '+':
                    while 1:
                        try:
                            ln = int(input('Какую букву открыть? От 1 до ' + str(len(sw)) + ': '))
                            break
                        except ValueError:
                            print("Вы ввели не число. Повторите ввод")
                    while not 0 < int(ln) <= len(sw) or sw[int(ln) - 1] != '_':
                        if not 0 < int(ln) <= len(sw):
                            print('Цифра вне заданного промежутка.')
                            while 1:
                                try:
                                    ln = int(input('Какую букву открыть? От 1 до ' + str(len(sw)) + ': '))
                                    break
                                except ValueError:
                                    print("Вы ввели не число. Повторите ввод")
                        elif sw[int(ln) - 1] != '_':
                            print('Эта буква уже открыта, попробуйте другую')
                            while 1:
                                try:
                                    ln = int(input('Какую букву открыть? От 1 до ' + str(len(sw)) + ': '))
                                    break
                                except ValueError:
                                    print("Вы ввели не число. Повторите ввод")
                    pos = []
                    start = 0
                    while questionandanswer[1].find(questionandanswer[1][int(ln)-1], start) != -1:
                        pos.append(questionandanswer[1].find(questionandanswer[1][int(ln)-1], start))
                        start = questionandanswer[1].find(questionandanswer[1][int(ln)-1], start) + 1
                    for p in pos:
                        sw = sw[:p] + questionandanswer[1][p] + sw[p + 1:]
                    print(sw)
                elif sector == 'x2':
                    print('Ваши очки удвоены.')
                    points *= 2
                print('Количество очков: ' + str(points))
                letter = input('Буква или слово: ')
                for i in range(len(letter)):
                    if ord(letter[i]) >= 1072:
                        letter = letter[:i] + chr(ord(letter[i]) - 32) + letter[i + 1:]
                    if 1103 > ord(letter[i]) < 1040:
                        zap = True
                while zap:
                    print('В ответе присутствуют запрещённые символы.')
                    letter = input('Буква или слово: ')
                    for i in range(len(letter)):
                        if ord(letter[i]) >= 1072:
                            letter = letter[:i] + chr(ord(letter[i]) - 32) + letter[i + 1:]
                        if not 1103 > ord(letter[i]) < 1040:
                            zap = False
                while sw.find(letter) != -1:
                    print('Эта буква уже открыта, попробуйте другую')
                    letter = input('Буква или слово: ')
                    for i in range(len(letter)):
                    if ord(letter[i]) >= 1072:
                        letter = letter[:i] + chr(ord(letter[i]) - 32) + letter[i + 1:]
                    if not 1103 > ord(letter[i]) < 1040:
                            zap = False
                if len(letter) > 1:
                    if letter != questionandanswer[1]:
                        print('Неверно!')
                    else:
                        if sector != 'x2' and sector != '+' and sector != 'Б' and sector != 'x2':
                            points += int(sector)
                        sw = questionandanswer[1]
                else:
                    pos = []
                    start = 0
                    while questionandanswer[1].find(letter, start) != -1:
                        pos.append(questionandanswer[1].find(letter, start))
                        start = questionandanswer[1].find(letter, start) + 1
                    for p in pos:
                        sw = sw[:p] + questionandanswer[1][p] + sw[p + 1:]
                    if len(pos) == 0:
                        print('Неверно!')
                    elif len(pos) == 1:
                        print('Откройте букву ' + letter)
                        if sector != 'x2' and sector != '+' and sector != 'Б' and sector != 'x2':
                            points += int(sector)
                    elif len(pos) > 1:
                        print('Откройте букву ' + letter)
                        if sector != 'x2' and sector != '+' and sector != 'Б' and sector != 'x2':
                            points += int(sector) * len(pos)
                            print('За ' + str(len(pos)) + ' отгаданные буквы полученные вами очки умножаются на '
                                  + str(len(pos)))
            input('Вы победили! Это было слово ' + questionandanswer[1] + '.\n'
                  + 'Вы набрали ' + str(points) + ' очков.\nЧтобы начать заново нажмите Enter')
        else:
            print('Ошибка подключения к интернету.')


main()
