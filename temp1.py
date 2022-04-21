import os
import time

import requests
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import pyperclip
import keyboard

opts = {
    "alias": ('диана', 'данил'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "code-tree": ('дерево', 'вставь дерево', 'мне нужно дерево'),
        "voices": ('голоса', 'какие у тебя есть голоса'),
        "select-voice": ('поставь голос', 'выбери голос'),
        "math": ('посчитай'),
        "weather": ('погода', 'какая погода')
    }
}


def speak(what):
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


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
    tempcoee = """def rr(num):
        ans = 1
        while ans < num:
            ans *= 2
        return ans


    def build(v, l, r):
        if l == r - 1:
            print(v)
            tree[v] = s[l]
        else:
            mid = (l + r) // 2
            build(2 * v + 1, l, mid)
            build(2 * v + 2, mid, r)
            tree[v] = tree[2 * v + 1] + tree[2 * v + 2]


    def ans(v, l, r, lc, rc):
        if rc < l or r < lc:
            return 0
        elif l == r - 1:
            return tree[v]
        else:
            mid = (l + r) // 2
            return ans(2 * v + 1, l, mid, lc, rc) + ans(2 * v + 2, mid, r, lc, rc)
    """
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == "code-tree":
        keyboard.write(tempcoee)
        pyperclip.copy('The text to be copied to the clipboard.')
        pyperclip.paste()
    elif cmd == "weather":
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': 551487, 'units': 'metric', 'lang': 'ru', 'APPID': 'b98eb293513a16e16e85b5830229ec5f'})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            print("temp:", data['main']['temp'])
            print("temp_min:", data['main']['temp_min'])
            print("temp_max:", data['main']['temp_max'])
        except Exception as e:
            print("Exception (weather):", e)
            pass
    elif cmd == "voices":
        for i in range(10):
            try:
                voices = speak_engine.getProperty('voices')
                speak_engine.setProperty('voice', voices[i].id)

                speak("Привет")
                speak("Мой номер " + str(i))
            except IndexError:
                pass
    elif cmd == "select-voice":
        voices = speak_engine.getProperty('voices')
        speak_engine.setProperty('voice', voices[int(cmd[1])].id)
    else:
        print('Команда не распознана, повторите!')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)

stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)
