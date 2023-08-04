"""
Вспомогательный модуль: глобальные переменные и условные константы.
"""

# стандартная библиотека
from collections.abc import Callable
from pathlib import Path
from re import compile
from sys import path


DEBUG: bool = False
debug_data: dict = {}


ROOT_DIR = Path(path[0]).parent
PLAYERS_DB_PATH = ROOT_DIR / 'data/statistics.ini'
SAVES_DB_PATH = ROOT_DIR / 'data/saves.txt'

name_pattern = compile(r'[a-zA-Zа-яА-Я][а-яА-Я\w]+')

# база игроков - имена и статистика игроков 
players_db: dict[str, dict[str, int]] = {}

# база сохраненных партий
saves_db: dict[frozenset, dict] = {}

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
    'некорректное имя': '! Имя игрока должно начинаться с буквы и быть не короче двух символов !',
    'размер поля': '\nВведите новый размер игрового поля в диапазоне от 3 до 20: >',
    'некорректный размер': '\n! Размер должен быть введен числом от 3 до 20 !',
    'недопустимое значение': '\n! Недопустимое значение !',
    'ввод хода': '\nВведите номер клетки: > ',
    'ход не число': '! Номер клетки должен быть числом !> ',
    'ход недопустим': '! Клетка должна находиться в пределах игрового поля и нет быть занятой !> ',
    'ничья': '\nПартия закончена. Ничья\n',
    'уровень бота': '\nВведите уровень бота (l - легкий, h - сложный): ',
    'ошибка команды': '\n! Недопустимая команда !\n',
}


authorized_player: str = None
active_players: list[str] = []
get_bot_turn: Callable = None

# размер поля
dim: int = 3

dim_range: range = range(dim)
all_cells: int = dim**2
all_cells_range: range = range(all_cells)

field_template: str = None

TOKENS = ('X', 'O')

WEIGHT_OWN: float = 1.5
WEIGHT_FOE: float = 1.0

START_MATRICES: tuple = None

#turns: dict[int, str] = {}
turns: dict[int] = []
board: dict[int, str] = dict.fromkeys(range(all_cells), ' ')

# список множеств победных комбинаций
wins : dict = {}

max_width: int = 1
coords = []