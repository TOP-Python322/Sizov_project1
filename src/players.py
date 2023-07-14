"""
Основной модуль: взаимодействие с игроками.
"""

# проект
import data
import utils

def get_name() -> str:
    """Запрашивает имя игрока"""
    while True:    
        name = input(data.MESSAGES['ввод имени'])
        if data.name_pattern.fullmatch(name):
            break
        print(data.MESSAGES['некорректное имя'])

    # усли новый игрок то добавляем его
    if name not in data.players_db:
        data.players_db[name] = {
            'wins': 0,
            'fails': 0,
            'ties': 0
        }
    if data.authorized_player is None:
        data.authorized_player = name
    data.active_players += [name]
   
    # сохранение конфигурации
    utils.write_ini()   
        
#    return name