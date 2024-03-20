# -*- coding: utf-8 -*-
from mutagen.id3 import ID3, TIT3


def get_band_name(path):
    try:
        audio = ID3(path)
        band_name = audio.get('TPE1')
        if band_name:
            return band_name.text[0]
        else:
            return None
    except Exception as e:
        print(f'Nie udało się pobrać wykonawcy dla {path}')


def get_song_title(path):
    try:
        audio = ID3(path)
        song_title = audio.get('TIT2')
        if song_title:
            return song_title.text[0]
        else:
            return None
    except Exception as e:
        print(f'Nie udało się pobrać tytułu dla {path}')


def get_zaiks(path):
    try:
        audio = ID3(path)
        zaiks = audio.get('TIT3')
        if zaiks:
            return zaiks.text[0]
        else:
            return None
    except Exception as e:
        print(f'Nie udało się pobrać numeru zaiks dla {path}')


def set_zaiks(path, zaiks):
    audio = ID3(path)
    audio.add(TIT3(encodingg=3, text=zaiks))
    audio.save()
