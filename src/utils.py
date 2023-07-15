"""
Вспомогательный модуль: вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
from shutil import get_terminal_size 
# проект
import data


def read_ini() -> dict:
    """Читает данные из файла и формирует структуру данных по статистике"""    
    config = ConfigParser()    
    config.read(data.PLAYERS_DB_PATH, encoding='utf-8')
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


def print_statistics():
    """ Выводит таблицу результатов с именами и статистикой игроков"""
    # Добавить сортировку по колличеству побед
    max_width = max(len(n) for n in data.players_db) +2
    width =  max_width + 36   
    result = f'\n#{"="*width}#\n#'
    result += f'{"Таблица результатов".center(width)}'   
    result += f'#\n#{"="*width}#'    
    print(result)
    print(f'|{"Игрок".center(max_width)}|   Победы  | Поражения |   Ничьи   |')
    print(f'|{"-"*width}|')
    for gamer in data.players_db:
        out = f'|{gamer.center(max_width)}|'
        for value in data.players_db[gamer].values():
            out += f'{str(value).center(11)}|'    
        print(out)
        print(f'|{"-"*width}|')

    
def update_dim():
    """ Обновляет размер поля"""    
#    добавить здесь обработку исключения на некорректный ввод
    while True:
        dim = int(input(data.MESSAGES['размер поля']))
    
        if 3<=dim <= 20:
            break
        else:
            print(data.MESSAGES['недопустимое значение'])

    data.dim = dim
    data.dim_range = range(dim)
    data.all_cells = dim**2
    data.field_template = generator_field()
 
 
def game_over():
    """Действия перед завершением работы приложения"""
    print('GAME OVER') 
    
    
def error_command():
    """ Выводит сообщение о не правильной команде"""   
    print('Такой команды нет!')  


def concatenate_lines(
        multiline1: str,
        multiline2: str,
        *multilines: str,
        padding: int = 8
) -> str:
    """Принимает на вход мнострочные объекты str и возвращает один объект str, строчки которого составлены из соответствующих строчек каждого переданного объекта, раздёлнных отступом."""
    multilines = multiline1, multiline2, *multilines
    multilines = [m.split('\n') for m in multilines]
    padding = ' '*padding
    return '\n'.join(
        padding.join(row)
        for row in zip(*multilines)
    ) 


def clear():
    """Очищает результат партии. 
    Возвращение списка активных игроков к состоянию до ввода команды new, сброс структуры данных для ходов"""    
    data.turns = [] # data.turns.clear() или так, узнать как лучше
    data.board = dict.fromkeys(range(data.all_cells), ' ')
    data.active_players = [data.authorized_player]
    field_template = ''