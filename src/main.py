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

# суперцикл (главное меню)
while True:
    # Ожидание ввода команды игрока
    command = input(data.MESSAGES['ввод команды'])
    
    if command in data.COMMANDS['новая партия']:
        game.mode()
        
        while True:
            result = game.game()
            if result != None:
                players.update(result)
            
                # запрашиваем повтор партии
                if not game.repeat():
                    break
            else:
                break
            
        # очищаем данные от значений прошедшей партии
        utils.clear()
    
    elif command in data.COMMANDS['загрузка']:
        game.load()

    elif command in data.COMMANDS['авторизация']:
        # переключаемся на другого игрока
        data.authorized_player = None
        data.active_players = []
        players.get_name() 
    
    elif command in data.COMMANDS['статистика']:
        # выводим таблицу результатов
        utils.print_statistics()   
    
    elif command in data.COMMANDS['размер поля']:
        utils.update_dim()
        
    elif command in data.COMMANDS['помощь']:
        help.show_help()    
    
    elif command in data.COMMANDS['выход']:
        break
        
    else:
        utils.error_command()

# Действия перед завершением работы приложения
utils.game_over()
