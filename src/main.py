"""
Главный модуль: точка входа.
"""

# проект
import data
import game
import help
import players
import utils

# выводим заставку
help.show_title()

# Чтение файлов данных
# ЕСЛИ первый запуск:
if not utils.read_ini():
    # вывод раздела помощи 
    help.show_help()
    
# Запрос имени игрока
players.get_name()    