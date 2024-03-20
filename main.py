# -*- coding: utf-8 -*-
import os
import re

import tag_walker
from web_walker import WebWalker


def get_audio_files(directory=None, extensions=['.mp3']):
    if not directory:
        directory = input('Podaj ścieżkę do folderu: ')

    audio_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                audio_files.append(os.path.join(root, file))

    return audio_files


def verify_zaiks_structure(zaiks):
    return bool(re.match(r'\d{7}', zaiks))


def find_em_all(path):
    ww = WebWalker()

    audio_files = get_audio_files(path)

    for song in audio_files:
        print(song)
        zaiks = tag_walker.get_zaiks(song)

        if zaiks:
            if verify_zaiks_structure(zaiks):
                print(f'Numer o poprawnej strukturze już znajduje się w metadanych - {zaiks}')
                continue

        band_name = tag_walker.get_band_name(song)
        song_title = tag_walker.get_song_title(song)

        print(f'{band_name} - {song_title}: ', end='')

        if band_name and song_title:
            ww.open_chrome()
            try:
                if len(song) > 60:
                    zaiks = ww.get_id(band_name=band_name, song_title=song_title[:60])
                else:
                    zaiks = ww.get_id(band_name=band_name, song_title=song_title)
                tag_walker.set_zaiks(song, zaiks)
            except Exception as e:
                print(e)
                with open('not found.txt', 'a+', encoding='utf-8') as f:
                    f.write(f'{band_name} - {song_title}: wystąpił problem\n')
        else:
            print(f'No tags for {song}')
            with open('not found.txt', 'a+', encoding='utf-8') as f:
                f.write(f'No tags for {song}\n')
