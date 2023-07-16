"""
Вспомогательный модуль: глобальные переменные и условные константы.
"""

# стандартная библиотека
from pathlib import Path
from re import compile
from sys import path

import utils


ROOT_DIR = Path(path[0]).parent
PLAYERS_DB_PATH = ROOT_DIR / 'data/statistics.ini'
SAVES_DB_PATH = ROOT_DIR / 'data/saves.txt'

name_pattern = compile(r'[a-zA-Zа-яА-Я][а-яА-Я\w]+')

# база игроков - имена и статистика игроков 
players_db: dict[str, dict[str, int]] = {}

# база сохраненных партий
saves_db: dict = {}

COMMANDS = {
    'помощь': ('help', 'помощь'),
    'новая партия': ('new', 'игра'),
    'загрузка': ('load', 'загрузка'),
    'авторизация': ('player', 'игрок'),
    'статистика': ('table', 'таблица'),
    'размер поля': ('dim', 'размер'),
    'выход': ('quit', 'выход'),    
}
MESSAGES = {
    'ввод команды': '\nВведите команду: > ',
    'ввод имени': '\nВведите имя: > ',
    'некорректное имя': '! имя игрока должно начинаться с буквы и быть не короче двух символов',
    'размер поля': '\nВведите размер игрового поля в диапазоне от 3 до 20: >',
    'недопустимое значение': '\nНедопустимое значение!',
    # '': '',
}


authorized_player: str = None
active_players: list[str] = []

# размер поля
dim: int = 3

dim_range: range = range(dim)
all_cells: int = dim**2
all_cells_range: range = range(all_cells)

field_template: str = None

TOKENS = ('X', 'O')

#turns: dict[int, str] = {}
turns: dict[int] = []
board: dict[int, str] = dict.fromkeys(range(all_cells), ' ')

