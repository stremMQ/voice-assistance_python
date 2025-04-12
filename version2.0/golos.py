from pywinauto.keyboard import send_keys
import speech_recognition as sr
from num2words import num2words
import sounddevice as sd
import pygetwindow as pw
import win10toast as wt
import pyautogui as pg
import sqlite3 as sq
import tkinter as tk
import pywinauto
import datetime
import silero
import numpy
import torch
import time
import os

rec = sr.Recognizer()
language = 'ru'
model_id = 'v4_ru'
device = torch.device('cpu')
lang = 'ru-RU'

model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                         model='silero_tts',
                                         language=language,
                                         speaker=model_id)
model.to(device)

class golos_as():
    def __init__(self, text_g, model):
        sample_rate = 48000
        speaker = 'aidar'
        with sq.connect("settings") as con:
            cur = con.execute('''SELECT golos FROM setting''')
            for f in cur.fetchall():
                igs = f[0]
        speaker = igs
        audio = model.apply_tts(text = text_g,
                                speaker = speaker,
                                sample_rate = sample_rate)

        sd.play(audio, sample_rate)
        time.sleep(len(audio) / sample_rate)
        sd.stop()

def speak():
    with sq.connect("settings") as con:
        cur = con.execute('''SELECT golos FROM setting''')
        for f in cur.fetchall():
            igs = f[0]
    speaker = igs
    return igs

text_g = "Здравствуйте!"
golos_as(text_g, model)
while 1:
    text = ''

    with sq.connect("settings") as con:
        cur = con.execute('''SELECT mic FROM setting''')
        for f in cur.fetchall():
            ind = int(f[0])

    window_title = pw.getAllTitles()
    mic = sr.Microphone(device_index = ind)

    with mic as audio_file:
        print("говорите")
        audio = rec.listen(audio_file)

    try:
        text = rec.recognize_google(audio, language='ru-RU')
        print(text)
    except sr.UnknownValueError:
        print("не разобрал")
    except sr.RequestError as e:
        print("ошибка")

    if "Люмен" in text or "Lumen" in text:
        text = ''
        with mic as audio_file:
            text_g = "слушаю"
            golos_as(text_g, model)

            # with sq.connect("yved.db") as con:
            #     cur = con.execute('''UPDATE yvedi SET kod = (?)''', (1,))

            audio = rec.listen(audio_file)

        try:
            text = rec.recognize_google(audio, language='ru-RU')
            print(text)
        except sr.UnknownValueError:
            if speak() == "baya" or speak() == "kseniya" or speak() == "xenia":
                text_g = "не разобрала"
            else:
                text_g = "не разобрал"

            golos_as(text_g, model)

        except sr.RequestError as e:

            text_g = "ошибка"
            golos_as(text_g, model)

        def request():
            global text
            text = ""
            with mic as audio_file:

                text_g = "скажите запрос"
                golos_as(text_g, model)

                audio = rec.listen(audio_file)

            try:
                textrec = rec.recognize_google(audio, language='ru-RU')
                print(text)
            except sr.UnknownValueError:

                if speak() == "baya" or speak() == "kseniya" or speak() == "xenia":
                    text_g = "не разобрала"
                else:
                    text_g = "не разобрал"

                golos_as(text_g, model)

            except sr.RequestError as e:
                text_g = "ошибка"
                golos_as(text_g, model)

            text_zp = textrec
            text_list = text_zp.split(" ")
            request_text = '+'.join(text_list)
            request = "start" + " " + "https://yandex.ru" + "/search/?text=" + request_text
            os.system(request)

        with sq.connect("castom_commands") as con:
            cur = con.cursor()
            cur.execute('''SELECT name_command FROM commands''')
            command = cur.fetchall()

        if text.lower() == "свернуть":
            win = pw.getAllTitles()
            activ_win = pw.getActiveWindow()
            if activ_win != None:
                titel = activ_win.title
                wins = pw.getWindowsWithTitle(titel)[0]
                wins.minimize()

        elif text.lower() == "развернуть":
            win = pw.getAllTitles()
            activ_win = pw.getActiveWindow()
            if activ_win != None:
                titel = activ_win.title
                wins = pw.getWindowsWithTitle(titel)[0]
                wins.restore()

        elif text.lower() == "закрой":
            win = pw.getAllTitles()
            activ_win = pw.getActiveWindow()
            if activ_win != None:
                path = activ_win.split()
                if "://" in path[len(path)-2]:
                    os.startfile(f'tasckill /f /im {path[len(path)-1] + path[len(path)-1]}')
                else:
                    os.startfile(f'tasckill /f /im {path[len(path)-1]}')

        elif text.lower() == "запрос":
                request()

        elif text.lower() == "время":
            timeP = datetime.datetime.now()
            if timeP.minute < 5 and timeP.minute != 0:
                if timeP.hour == 1:
                    text_g = f'сейчас {num2words(timeP.hour, lang = "ru")} час {num2words(timeP.minute, lang = "ru")} минута'
                elif 1 < timeP.hour < 5:
                    text_g = f'сейчас {num2words(timeP.hour, lang="ru")} часa {num2words(timeP.minute, lang="ru")} минута'
                elif timeP.hour >= 5 or timeP.hour == 0:
                    text_g = f'сейчас {num2words(timeP.hour, lang="ru")} часов {num2words(timeP.minute, lang="ru")} минута'
            elif timeP.minute >= 5 or timeP.minute == 0:
                if timeP.hour == 1:
                    text_g = f'сейчас {num2words(timeP.hour, lang = "ru")} час {num2words(timeP.minute, lang = "ru")} минут'
                elif 1 < timeP.hour < 5:
                    text_g = f'сейчас {num2words(timeP.hour, lang="ru")} часa {num2words(timeP.minute, lang="ru")} минут'
                elif timeP.hour >= 5 or timeP.hour == 0:
                    text_g = f'сейчас {num2words(timeP.hour, lang="ru")} часов {num2words(timeP.minute, lang="ru")} минут'
            golos_as(text_g, model)

        elif text.lower() == "девайсы":
            x = 0
            y = 0
            pg.moveTo(x, y)
            pg.FAILSAFE = False
            text_g = "слушаю указания!"
            golos_as(text_g, model)
            while True:
                text = ''
                with mic as audio_file:
                    print("говорите")
                    audio = rec.listen(audio_file)

                try:
                    text = rec.recognize_google(audio, language=lang)
                    print(text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    text_g = "ошибка"
                    golos_as(text_g, model)

                text_l = text.split()
                lenD = len(text_l)

                if (len(text_l) != 0 and text_l[0] == "вправо") or (len(text_l) != 0 and text_l[0] == "вправa"):
                    try:
                        x += int(text_l[lenD - 1])
                    except ValueError:
                        x += 50
                    print(x, y)
                    pg.moveTo(x, y)

                elif (len(text_l) != 0 and text_l[0] == "влево") or (len(text_l) != 0 and text_l[0] == "влева"):
                    try:
                        x -= int(text_l[lenD - 1])
                    except ValueError:
                        x -= 50
                    print(x, y)
                    pg.moveTo(x, y)

                elif len(text_l) != 0 and text_l[0] == "вверх":
                    try:
                        y -= int(text_l[lenD - 1])
                    except ValueError:
                        y -= 50
                    print(x, y)
                    pg.moveTo(x, y)

                elif len(text_l) != 0 and text_l[0] == "вниз":
                    try:
                        y += int(text_l[lenD - 1])
                    except ValueError:
                        y += 50
                    print(x, y)
                    pg.moveTo(x, y)

                elif text.lower() == "клик-клик":
                    pg.doubleClick(x, y)

                elif text.lower() == "кликнуть":
                    pg.click(x, y)

                elif text.lower() == "стоп":
                    break

                elif text.lower() == "написать":
                    with mic as audio_file:
                        text_g = "что напишем?"
                        golos_as(text_g, model)
                        audio = rec.listen(audio_file)

                    try:
                        text_n = rec.recognize_google(audio, language=lang)
                        print(text)
                    except sr.UnknownValueError:
                        if speak() == "baya" or speak() == "kseniya" or speak() == "xenia":
                            text_g = "не разобрала"
                        else:
                            text_g = "не разобрал"

                        golos_as(text_g, model)

                    except sr.RequestError as e:
                        text_g = "ошибка"
                        golos_as(text_g, model)

                    send_keys(text_n, with_spaces=True)

                elif text.lower() == "отправить":
                    pg.press('enter')

                elif text.lower() == "пробел":
                    pg.press('space')

                elif text.lower() == "точка":
                    send_keys(".")

                elif text.lower() == "двоеточие":
                    send_keys(":")

                elif text.lower() == "запятая":
                    send_keys(",")

                elif text.lower() == "стереть":
                    pg.press('backspace')

                elif text.lower() == "стереть всё":
                    for i in range (0,len(text_n)):
                        pg.press('backspace')

        elif text == "сменить язык" or text == "change the lang":
            if lang == 'ru-RU':
                lang = 'es-US'
                text_g = "язык сменен на английский"
                golos_as(text_g, model)
            else:
                text_g = "язык сменен на русский"
                golos_as(text_g, model)
                lang = 'ru-RU'

        else:
            for commands_rengen in command:
                commands_rengen = str(commands_rengen[0])
                if commands_rengen in text.lower():

                    with sq.connect("castom_commands") as con:
                        cur = con.cursor()
                        cur.execute('''SELECT addres FROM commands WHERE name_command = (?)''', (commands_rengen,))
                        patch = cur.fetchall()
                    for g in patch:
                        adres = str(g[0])
                    with sq.connect("castom_commands") as con:
                        cur = con.cursor()
                        cur.execute('''SELECT tip_commands FROM commands WHERE name_command = (?)''',
                                    (commands_rengen,))
                        func = cur.fetchall()
                    for f in func:
                        fn = str(f[0])

                    if fn == "запустить":
                        # with sq.connect("yved.db") as con:
                        #     cur = con.execute('''UPDATE yvedi SET kod = (?)''', (2,))
                        os.startfile(adres)

                    elif fn == "завершить":
                        # with sq.connect("yved.db") as con:
                        #     cur = con.execute('''UPDATE yvedi SET kod = (?)''', (2,))
                        delen = adres.split('/')
                        os.system(f"taskkill /F /IM {delen[len(delen)]}")
