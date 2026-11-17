import sqlite3 as sq
import time
import pyaudio
import os
from tkinter import *
import customtkinter as ctk
from customtkinter import filedialog
import speech_recognition as sr
import asyncio
import subprocess as sb
from PIL import ImageTk

win = ctk.CTk()
win.geometry("650x450")
win.title("Lumen")
win.wm_iconbitmap()
foto = ImageTk.PhotoImage(file = "logo_ds.ico")
win.iconphoto(False,foto)
win.configure(bg = "#606060")
win.resizable(False,False)
frame = ctk.CTkFrame(master=win, width=220, height=450, fg_color="#171717")
frame.pack(side = LEFT)
frame.propagate(False)

frame2 = ctk.CTkScrollableFrame(win, width=430, height= 450)
frame2.pack(side= RIGHT)

def dismiss(win_create):
    win_create.grab_release()
    win_create.destroy()

def del_win(win_del):
    win_del.grab_release()
    win_del.destroy()

def filePatch():
    global file_patch
    file_patch = filedialog.askopenfilename()

def delete_command():
    win_del = ctk.CTkToplevel()
    win_del.after(201, lambda: win_del.iconbitmap("logo_ds.ico"))
    win_del.title("Удаление команды")
    win_del.geometry("450x250")
    win_del.resizable(False,False)
    win_del.protocol("WM_DELETE_WINDOW", lambda: del_win(win_del))

    label_eror = ctk.CTkLabel(win_del, text = "Такой команды нет!")

    entry_name = ctk.CTkEntry(win_del, placeholder_text = "Название команды")
    entry_name.pack(anchor = "center", pady = (80,0))

    def del_cd():
        name_cd = entry_name.get()

        with sq.connect("castom_commands") as con:
            cur = con.execute('''SELECT name_command FROM commands WHERE name_command = (?)''', (name_cd,))
            if cur.fetchall() == []:
                label_eror.pack(anchor = "center" , pady = (10,0))
            else:
                cur = con.execute('''DELETE FROM commands WHERE name_command = (?)''', (name_cd,))
                del_win(win_del)
        commands()

    button_delete = ctk.CTkButton(win_del, text = "Удалить", fg_color = "#171717", hover_color = "#303030", width=170, command = del_cd)
    button_delete.pack(anchor = "center", pady = (5,0))

    win_del.grab_set()

def create_command():


    win_create = ctk.CTkToplevel()
    win_create.after(201, lambda: win_create.iconbitmap("logo_ds.ico"))
    win_create.title("Новая команда")
    win_create.geometry("450x250")
    win_create.resizable(False,False)
    win_create.protocol("WM_DELETE_WINDOW", lambda: dismiss(win_create))

    entry_name_command = ctk.CTkEntry(win_create, placeholder_text="название команды")
    entry_name_command.pack(side = LEFT, pady = (0,15))

    button_fail = ctk.CTkButton(win_create, text = "выбрать путь",fg_color = "#565b5e", hover_color = "#303030", command=filePatch, width=170)
    button_fail.pack(side = LEFT, padx = 2, pady = (0,15))

    comboBox_function = ctk.CTkComboBox(win_create,values=["запустить","завершить"])
    comboBox_function.pack(side = LEFT, pady = (0,15))

    def new():
        patch = file_patch
        name = entry_name_command.get()
        function = comboBox_function.get()
        with sq.connect("castom_commands") as con:
            cur = con.execute('''INSERT INTO commands (name_command,addres,tip_commands) VALUES(?,?,?)''', (name,patch,function,))
        dismiss(win_create)
        commands()


    bytton_safe = ctk.CTkButton(win_create, text = "Добавить", fg_color = "#171717", hover_color = "#303030", command = new)
    bytton_safe.place(x = 155, y = 210)

    win_create.grab_set()

def safe_settings():
    number = index_mic()
    with sq.connect("settings") as con:
        cur = con.execute('''UPDATE setting SET mic = (?)''',(number,))
    settings()

button_delite = ctk.CTkButton(master = frame2, text = "Удалить команду",fg_color = "#171717", hover_color = "#303030", command = delete_command)
label_NO = ctk.CTkLabel(master = frame2,text = "У вас пока что нет команд", corner_radius= 5)
button_create = ctk.CTkButton(master = frame2, text = "Добавить команду",fg_color = "#171717", hover_color = "#303030", command = create_command)
label_spis_commands = ctk.CTkLabel(master = frame2, text = "", width = 250)
label_inf = ctk.CTkLabel(master = frame2, text = "№: название -- путь -- функция", fg_color="#353535", corner_radius = 3, height = 6)

label_index = ctk.CTkLabel(frame2, text = f"Выбран микровон: ", wraplength = 400)
combobox_mic = ctk.CTkComboBox(frame2, values = '', width = 285)
button_safe = ctk.CTkButton(frame2 , text = "Сохранить", command = safe_settings, fg_color = "#171717", hover_color = "#303030")

def text(b):
    global label_spis_commands
    label_spis_commands = ctk.CTkLabel(master=frame2, text = b, wraplength = 400)
    print(b)

def index_mic_select():
    with sq.connect("settings") as con:
        cur = con.execute('''SELECT mic FROM setting''')
        for f in cur.fetchall():
            ind = int(f[0])
        return ind

def commands():
    textcm = ''


    with sq.connect("castom_commands") as con:
        cur = con.cursor()
        cur.execute('''SELECT * FROM commands''')
        command = cur.fetchall()
        spis_commans = {}

    if command == []:
        label_spis_commands.pack_forget()
        button_delite.pack_forget()
        label_inf.pack_forget()
        button_create.pack_forget()

        label_NO.pack(anchor = "center", pady =(10,0))
        button_create.pack(anchor = "center", pady = (10,0))

    else:
        n = 0
        for g in command :
            g0 = g[0]
            g1 = g[1]
            g2 = g[2]
            spis_commans[n + 1] = str(g0) + " -- " + str(g1) + " -- " + str(g2)
            n += 1

        for k, v in spis_commans.items():
            textcm += f"{k}: {v} \n " " \n "

        button_safe.pack_forget()
        label_index.pack_forget()
        combobox_mic.pack_forget()
        button_delite.pack_forget()
        button_create.pack_forget()
        label_spis_commands.pack_forget()
        label_NO.pack_forget()
        label_inf.pack_forget()

        text(textcm)


        label_inf.pack(anchor = "center", pady = (4,10))
        label_spis_commands.pack(anchor = "center", pady =(10,0))
        button_create.pack(anchor = "center", pady = (10,0))
        button_delite.pack(anchor = "center", pady = (10,0))
        textcm = ''

def list_index(a,m,ind):
    global combobox_mic
    global label_index
    combobox_mic = ctk.CTkComboBox(frame2, values = a, width=285)
    print(m,ind)
    label_index = ctk.CTkLabel(frame2, text=f"Выбран микровон: {m[ind]}", wraplength=400)

def settings():
    global mic

    button_create.pack_forget()
    label_NO.pack_forget()
    button_delite.pack_forget()
    label_spis_commands.pack_forget()
    label_inf.pack_forget()
    label_index.pack_forget()
    combobox_mic.pack_forget()
    button_safe.pack_forget()

    mic = sr.Microphone.list_microphone_names()
    mic2 = []

    for i in mic:
        cnt = 0
        for j in mic2:
            if j == i:
                cnt +=1
        if cnt == 0:
            mic2.append(i)

    ind = index_mic_select()


    list_index(mic2,mic,ind)

    label_index.pack(anchor = "center", pady = (20,0))

    combobox_mic.pack(anchor = "center", pady = (50,0))

    button_safe.pack(anchor = "center", pady = (200,0))


def index_mic():
    global mic
    index = combobox_mic.get()
    index = mic.index(index)
    return index

btn_commands = ctk.CTkButton(frame, text = "команды", fg_color="#303030", hover_color= "#606060", command = commands)
btn_commands.pack(anchor = "w", padx = 50, pady = (180, 0))

btn_settings = ctk.CTkButton(frame, text = "настройки", fg_color="#303030", hover_color= "#606060", command = settings)
btn_settings.pack(anchor = "w", pady = 20, padx = 50)

label_hello = ctk.CTkLabel(master=frame2,text = f"Голосовой помощник Vife приветствует вас!", fg_color="#171717", corner_radius= 5)
label_hello.pack(anchor = "center",pady = (20,0))

win.mainloop()
