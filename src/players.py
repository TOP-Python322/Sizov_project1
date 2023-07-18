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
        # сохранение конфигурации для нового игрока
        utils.write_ini() 
        
    if data.authorized_player is None:
        data.authorized_player = name
    data.active_players += [name]      
        

def update(gamers: list[str]) -> None:
    """Обновляет статистику и записыает в файл"""
    # если не ничья
    if len(gamers) > 0:
        # победитель
        # если игрок не бот
        if not gamers[0].startswith('#'):
            data.players_db[gamers[0]]['wins'] += 1
        # проигравший
        # если игрок не бот
        if not gamers[1].startswith('#'):
            data.players_db[gamers[1]]['fails'] += 1    

    else:
        for gamer in data.active_players:
            # если игрок не бот
            if not gamer.startswith('#'):
                data.players_db[gamer]['ties'] += 1
                
    # перезаписываем файл
    utils.write_ini() 
