import sqlite3 as sq
import speech_recognition as sr
import pygetwindow as pw
import win10toast as wt
import tkinter as tk
import os

rec = sr.Recognizer()

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

    if "Люмен" in text:

        with mic as audio_file:
            print("слушаю")
            # with sq.connect("yved.db") as con:
            #     cur = con.execute('''UPDATE yvedi SET kod = (?)''', (1,))
            audio = rec.listen(audio_file)

        try:
            text = rec.recognize_google(audio, language='ru-RU')
            print(text)
        except sr.UnknownValueError:
            print("не разобрал")
        except sr.RequestError as e:
            print("ошибка")

        def request():
            global text
            text = ""
            with mic as audio_file:
                print("скажите запрос")
                audio = rec.listen(audio_file)

            try:
                textrec = rec.recognize_google(audio, language='ru-RU')
                print(text)
            except sr.UnknownValueError:
                print("не разобрал")
            except sr.RequestError as e:
                print("ошибка")

            text_zp = textrec
            text_list = text_zp.split(" ")
            request_text = '+'.join(text_list)
            request = "start" + " " + "https://yandex.ru" + "/search/?text=" + request_text
            os.system(request)

        with sq.connect("castom_commands") as con:
            cur = con.cursor()
            cur.execute('''SELECT name_command FROM commands''')
            command = cur.fetchall()

        for commands_rengen in command:
            commands_rengen = str(commands_rengen[0])
            if commands_rengen in text.lower():
                print("да")

                with sq.connect("castom_commands") as con:
                    cur = con.cursor()
                    cur.execute('''SELECT addres FROM commands WHERE name_command = (?)''', (commands_rengen,))
                    patch = cur.fetchall()
                for g in patch:
                    adres = str(g[0])
                with sq.connect("castom_commands") as con:
                    cur = con.cursor()
                    cur.execute('''SELECT tip_commands FROM commands WHERE name_command = (?)''', (commands_rengen,))
                    func = cur.fetchall()
                for f in func:
                    fn = str(f[0])

                print(adres,fn)

                if fn == "запустить":
                    # with sq.connect("yved.db") as con:
                    #     cur = con.execute('''UPDATE yvedi SET kod = (?)''', (2,))
                    os.startfile(adres)

                elif fn == "завершить":
                    # with sq.connect("yved.db") as con:
                    #     cur = con.execute('''UPDATE yvedi SET kod = (?)''', (2,))
                    delen = adres.split('/')
                    os.system(f"taskkill /F /IM {delen[len(delen)]}")

            elif text.lower() == "свернуть":
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

            elif text.lower() == "запрос":
                    request()