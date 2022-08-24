from pydub import AudioSegment, silence
import zipfile
import os
from tkinter import *
from tkinter import filedialog as fd
import tkinter as tk
import tkinter.font as tkFont
import time
def cut_silence(path):
    time_now = time.strftime('%H_%M_%S', time.localtime())
    if os.path.exists(f'Output{time_now}'):
        pass
    else:
        os.mkdir(f'Output{time_now}')
    for filename in os.listdir(path):
        SILENCE_THRESHOLD = -35.0
        # Загружаем аудиофайл
        #print(f'Берём файл {filename}')
        audio = AudioSegment.from_wav(f'{path}/{filename}')
        #print(f'Изначальная длина аудио составила {len(audio)} мс')
        # Находим продолжительность тишины в конце аудио (в миллисекундах)
        trailing_silence = silence.detect_leading_silence(audio.reverse(), silence_threshold=SILENCE_THRESHOLD, )
        #print(f'Тишина от конца начинается {trailing_silence}мс (По мнению этого питомца)')
        trailing_silence = trailing_silence
        #print(
            #f'Время тишины от конца в рамках аудиофайла целиком: {round(audio.duration_seconds, 3)} * 1000 - {trailing_silence} = {round(audio.duration_seconds, 3) * 1000 - trailing_silence}')
        # Обрезаем тишину в конце файла
        trimmed_audio_1 = audio[:-trailing_silence]
        #print(f'Обрезали аудио c конца, его длина составила {len(trimmed_audio_1)}')
        trailing_silence_start = silence.detect_leading_silence(audio, silence_threshold=SILENCE_THRESHOLD)
        trailing_silence_start = trailing_silence_start
        #print(f'Срезаем аудио с начала, длина от начала составила {trailing_silence_start}')
        trimmed_audio = trimmed_audio_1[trailing_silence_start:]
        #print(f'Обрезали аудио с начала ({len(trimmed_audio_1)} - {trailing_silence_start}), его длина составила {len(trimmed_audio)}')
        # Записываем обрезанную дорожку в файл
        trimmed_audio.export(f'Output{time_now}/{filename}', format="wav")
    #print(time_now)
    output_zip = zipfile.ZipFile(f'Output{time_now}.zip','w')
    for root, dirs, files in os.walk(f'Output{time_now}'):
        for f in files:
            output_zip.write(os.path.join(root, f))
    output_zip.close()

def insert_file():
    file_name = fd.askdirectory()
    #print(file_name)
    cut_silence(file_name)
    root.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title("Питомец - звукорежиссёр")
    a = root.geometry('140x150')
    root.resizable(False,False)
    fontStyle = tkFont.Font(family="Lucida Grande", size=10)
    b1 = Button(text="Выбрать папку с аудио", height=10, width=10, command=insert_file, bg='#ffc0cb', compound=tk.CENTER)
    b1.grid(row=500, column=100, ipadx=30, ipady=6, padx=0, pady=0)
    root.mainloop()




