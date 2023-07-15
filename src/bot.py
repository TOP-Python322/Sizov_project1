"""
Основной модуль: вычисления для бота.
"""

# стандартная библиотека
from random import randint
# проект
import data

def game_low() -> int:
    """ Генерирует ход для легкого бота"""
    # пока так, расмотреть другие варианты
    while True:
        step_bot = randint(0, data.all_cells)
        if step_bot not in data.turns:
            break
            
    return step_bot
    