"""
Вспомогательный модуль: вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
# проект
import data


def read_ini() -> dict:
    """Читает данные из файла и формирует структуру данных по статистике"""    
    config = ConfigParser()    
    config.read(data.PLAYERS_DB_PATH)
    for player in config.sections(): 
        data.players_db[player] = {
            k: int(v)
            for k, v in config[player].items()
        }
    return bool(data.players_db)
 
 
def write_ini() -> None:
    """Записывает структуру данных по статистике в файл"""
    config = ConfigParser()
    config.read_dict(data.players_db)
    with open(data.PLAYERS_DB_PATH, 'w', encoding='utf-8') as configfile:
        config.write(configfile) 
        

