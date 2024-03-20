import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SONG_TITLE_LOCATOR = (By.ID, 'input-vaadin-text-field-13')
BAND_NAME_LOCATOR = (By.ID, 'input-vaadin-text-field-14')
SEARCH_BUTTON_LOCATOR = (By.CLASS_NAME, 'crud-find-retriveBtn')
DETAILS_BOX_SELECTOR = (By.XPATH, '//span[@class="musicWork-card-title"]')
SONGS_COUNTER_SELECTOR = (By.XPATH, '//div[@class="rich-html-text crud-grid-header-rows"]')
ARTISTS_SELECTOR = (By.XPATH, '//span[@slot="summary"]')
ZAIKS_NUMBER_SELECTOR = (By.XPATH, '//div[@class="span-field"]')


class WebWalker():
    def __init__(self):
        self._driver = webdriver.Chrome()
        self.not_found = list()
        self.found_many = list()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.close()

    def _clear_elements(self):
        WebDriverWait(self._driver, 30).until(EC.element_to_be_clickable(SONG_TITLE_LOCATOR)).click()
        self._driver.find_element(*SONG_TITLE_LOCATOR).clear()
        self._driver.find_element(*BAND_NAME_LOCATOR).clear()

    def _write_song_title(self, song_title: str) -> None:
        element = self._driver.find_element(*SONG_TITLE_LOCATOR)
        element.send_keys(song_title)

    def _write_band_name(self, band_name: str) -> None:
        element = self._driver.find_element(*BAND_NAME_LOCATOR)
        element.send_keys(band_name)

    def _click_search(self) -> None:
        self._driver.find_element(*SEARCH_BUTTON_LOCATOR).click()

    def open_chrome(self):
        self._driver.get('https://online.zaiks.org.pl/utwory-muzyczne')

    def _search_data(self, band_name: str, song_title: str) -> None:
        self._clear_elements()
        self._write_song_title(song_title)
        self._write_band_name(band_name)
        self._click_search()

    def _open_details(self, band_name: str, song_title: str) -> None:
        WebDriverWait(self._driver, 300).until(EC.presence_of_element_located(SONGS_COUNTER_SELECTOR))
        elements_counter = self._driver.find_element(*SONGS_COUNTER_SELECTOR).text

        if not os.path.exists('screenshots'):
            os.mkdir('screenshots')

        self._driver.save_screenshot(f'screenshots/screenshot - {band_name} - {song_title}.png')

        if '1' in elements_counter:
            self._driver.find_element(*DETAILS_BOX_SELECTOR).click()
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located(ARTISTS_SELECTOR))
            self._driver.find_element(*ARTISTS_SELECTOR).click()
            self._driver.save_screenshot(f'screenshots/screenshot - {band_name} - {song_title} - details.png')
        elif '0' in elements_counter:
            print(f'nie znaleziono')
            with open('not found.txt', 'a+', encoding='utf-8') as f:
                f.write(f'{band_name} - {song_title}: nie znaleiono')
            self.not_found.append(f'{band_name} - {song_title}')
        else:
            print('znaleziono zbyt wiele pasujących elementów')
            with open('not found.txt', 'a+', encoding='utf-8') as f:
                f.write(f'{band_name} - {song_title}: znaleziono zbyt wiele pasujących elementów')
            self.found_many.append(f'{band_name} - {song_title}')

    def _read_zaiks(self) -> str:
        potential_zaiks_numbers = self._driver.find_elements(*ZAIKS_NUMBER_SELECTOR)

        for element in potential_zaiks_numbers:
            if 'Nr ZAiKS' in element.text:
                zaiks_to_return = re.search(r'\d{7}', element.text).group()
                print(zaiks_to_return)
                return zaiks_to_return

        return ''

    def get_id(self, band_name, song_title) -> str:
        self._search_data(band_name, song_title)
        self._open_details(band_name, song_title)
        zaiks_id = self._read_zaiks()

        return zaiks_id
