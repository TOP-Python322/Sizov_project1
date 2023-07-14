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
        

def generator_field(width: int = 1) -> str:
    """Генерирует шаблон игрового поля для отображения"""
    row = '|'.join([' {} ']*data.dim)
    h_line = '-'*(data.dim*(width+2) + data.dim-1)
    return f'\n{h_line}\n'.join([row]*data.dim)

    
def generator_wins() -> list:
    """Генерирует выигрышные комбинации"""  
    out = []
    my_list = [i for i in range(0, data.all_cells)]    
    for i in data.dim_range:
        out.append({element for element in my_list[i*data.dim:data.dim*(i+1)]})
        out.append({element for element in my_list[i::data.dim]})
    out.append({element for element in my_list[::data.dim+1]})
    out.append({element for element in my_list[data.dim-1:-1:data.dim-1]})
    return out
