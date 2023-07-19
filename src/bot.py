"""
Основной модуль: вычисления для бота.
"""

# стандартная библиотека
from random import randint
# проект
import data

def easy(bot_index: int) -> int:
    """ Генерирует ход для легкого уровня бота"""
    # пока так, расмотреть другие варианты
    while True:
        step_bot = randint(0, data.all_cells-1)
        if step_bot not in data.turns:
            break            
    return step_bot
    
    
def hard(bot_index: int) -> int:    
    """ Генерирует ход для сложного уровня бота"""
    print('\n !!!!!! Режим не реализован !!!!!!\n')
    