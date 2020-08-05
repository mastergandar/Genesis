import datetime
import os
import webbrowser

import psutil
import pyautogui
import pyttsx3
import speech_recognition as sr
import win32gui
from fuzzywuzzy import fuzz

#music_path = 'ВАШ ПУТЬ К МУЗЫКЕ'

opts = {
    "alias": ('генезис', 'бот', 'консерва'),
    "cmds": {
        "foobar start": ('включи музыку', 'музыка включить'),
        "foobar close": ('выключи музыку', 'музыка выключить'),
        "foobar next": ('следующий трек', 'некст трек'),
        "foobar prev": ('предыдущий трек', 'старый трек'),
        "foobar pause": ('поставь на паузу', 'музыка пауза'),
        "foobar play": ('продолжи музыку', 'музыка продолжить'),
        "ctime": ('сколько время', 'котрый час'),
        "browser": ('открой ютуб', 'открой youtube', 'открой ютюб')
    }
}


def talk(words):
    # print(words)
    # os.system("say " + words)
    speak_engine = pyttsx3.init()
    print(words)
    speak_engine.say(words)
    speak_engine.runAndWait()
    speak_engine.stop()


talk("Привет, чем я могу помочь вам?")


def command():
    global voice
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Говорите")

        r.adjust_for_ambient_noise(source, duration=1)

        audio = r.listen(source)

    try:
        voice = r.recognize_google(audio, language="ru-RU").lower()
        print("[+] Результат сканирования голоса: " + voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[-] Сканирование голоса не дало результатов!")
    except sr.RequestError as e:
        print("[=] Сканеру не удалось подключиться к космической энергии!/n "
              "Проверьте соединение!")
        voice = command()

    return voice




def music_name(music_path):
    music = (os.listdir(music_path))
    print(music)
    return music


def play_music(music_name):
    global hwnd
    index = 0
    i = len(music_name)
    print(i)
    while index < i:
        os.startfile(music_path + music_name[index])
        index += 1
    #hwnd = win32gui.GetFocus()
    #print("HWND: " + str(hwnd))

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'browser':
        url = 'https://www.youtube.com/'
        webbrowser.open(url)

    elif cmd == 'foobar start':
        play_music(music_name(music_path))

    elif cmd == 'foobar close':
        procname = "foobar2000.exe"
        for proc in psutil.process_iter():
            if proc.name() == procname:
                proc.kill()

    elif cmd == 'foobar next':
        win32gui.FindWindow(None, '[foobar2000]')
        win32gui.EnableWindow(None, True)
        win32gui.SetFocus(hwnd)
        pyautogui.press('num6')

    elif cmd == 'foobar prev':
        win32gui.FindWindow(None, '[foobar2000]')
        win32gui.EnableWindow(None, True)
        win32gui.SetFocus(hwnd)
        pyautogui.press('num4')

    elif cmd == 'foobar pause':
        win32gui.FindWindow(None, '[foobar2000]')
        win32gui.EnableWindow(None, True)
        win32gui.SetFocus(hwnd)
        pyautogui.press('num2')

    elif cmd == 'foobar play':
        win32gui.FindWindow(None, '[foobar2000]')
        win32gui.EnableWindow(None, True)
        win32gui.SetFocus(hwnd)
        pyautogui.press('num2')


while True:
    execute_cmd(command())
