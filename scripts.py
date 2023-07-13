from shutil import get_terminal_size 
import configparser

# размер поля
dim = 3
# ИСПОЛЬЗОВАТЬ: этот range объект нам понадобится очень часто — лучше вычислить его единожды при задании/изменении размера поля
dim_range = range(dim)
# ИСПОЛЬЗОВАТЬ: в all_cells лучше записать общее число ячеек (возможных ходов)
all_cells = dim**2

# КОММЕНТАРИЙ: такой список вряд ли понадобится
empty_row = [' ']*dim

# список ходов
turns = []


# ИСПОЛЬЗОВАТЬ: в нашем проекте dim — глобальная переменная, так её сразу и будем использовать
# ИСПОЛЬЗОВАТЬ: а width нужна для задания максимальной ширины столбца без учёта полей — для игрового поля с токенами это всегда 1, а для сетки с координатами эту ширину необходимо заранее вычислить
def generator_board(width: int = 1) -> str:
    """Генерирует шаблон игрового поля для отображения"""
    # КОММЕНТАРИЙ: тот случай, когда создание переменной ради одного использования оправдано — выражения уже достаточно сложные
    # ИСПОЛЬЗОВАТЬ: поля добавляются к ячейке, не к разделителю
    row = '|'.join([' {} ']*dim)
    # ИСПОЛЬЗОВАТЬ: в width записана ширина собственно данных, двойку добавляем для полей, dim-1 — для вертикальных разделителей
    h_line = '-'*(dim*(width+2) + dim-1)
    return f'\n{h_line}\n'.join([row]*dim)


# >>> print(generator_board().format(*range(9)))
#  0 | 1 | 2
# -----------
#  3 | 4 | 5
# -----------
#  6 | 7 | 8
# >>>
# >>> dim = 5
# >>> coords = range(25)
# КОММЕНТАРИЙ: вычисляем максимальную ширину этих данных
# >>> max_width = max(len(str(n)) for n in coords)
# >>>
# КОММЕНТАРИЙ: пересобираем данные так, чтобы элементы были выровненными вправо строками
# >>> coords = [f'{n:>{max_width}}' for n in coords]
# >>>
# >>> print(generator_board(max_width).format(*coords))
#   0 |  1 |  2 |  3 |  4
# ------------------------
#   5 |  6 |  7 |  8 |  9
# ------------------------
#  10 | 11 | 12 | 13 | 14
# ------------------------
#  15 | 16 | 17 | 18 | 19
# ------------------------
#  20 | 21 | 22 | 23 | 24


def generator_wins(dim: int) -> list:
    """Генерирует выигрышные комбинации"""  
    out = []
    # ИСПОЛЬЗОВАТЬ: регистр lower_snake_case для всех имён кроме классов и условных констант
    my_list = [i for i in range(0, dim**2)]
    
    for i in range(dim):
        out.append({element for element in my_list[i*dim:dim*(i+1)]})
        out.append({element for element in my_list[i::dim]})
    out.append({element for element in my_list[::dim+1]})
    out.append({element for element in my_list[dim-1:-1:dim-1]})

    return out
    
    
def show_title():
    """Выводит заголовок игры"""

    width = get_terminal_size().columns - 2

    title = f'\n#{"="*width}##{" "*width}##'
    title += f'{"Игра".center(width)}##'  
    title += f'{"Крестики-Нолики".center(width)}' 
    title += f'##{" "*width}##{"="*width}#\n'
    
    print(title)

    
def show_help():
    """Выводит справку по игре"""  

    width = get_terminal_size().columns
    
    text_help = f'{"СПРАВКА".center(width)}\n'
    text_help += '  Приложение с интерфейсом командной строки, с помощью которого можно играть одному или вдвоём в игру крестики-нолики на квадратном поле.\n'
    
    text_help += '  После запуска приложение входит в главное меню, в котором ожидает ввод команд игрока. С помощью команд можно настраивать игру, запускать новую партию и выполнять другие действия.\n'    

    print(text_help)


def read_ini() -> dict:
    """Читает данные из файла и формирует структуру данных по статистике"""
    
    stat = {}
    config = configparser.ConfigParser()
    
    # усли файл есть то читаем из него
    if len(config.read('statistics.ini')):
        for section_name in config.sections(): 
#        print('Section:', section_name) 
#        print(' Options:', config.options(section_name)) 
#        for key, value in config.items(section_name): 
#            print(' {} = {}'.format(key, value)) 
#        print()
            stat[section_name] = dict(config.items(section_name))

    return stat
 
 
def write_ini() :
    """Записывает структуру данных по статистике в файл"""
    config = configparser.ConfigParser()
    config.read_dict(statistics)
    with open('statistics.ini', 'w') as configfile:
        config.write(configfile) 
    
    
def get_player_name() -> str:
    """Запрашивает имя игрока"""    
    name = input('Введите имя игрока: ')

    # усли новый игрок то добавляем его
    if name not in statistics:
        statistics[name] = {'wins' : 0, 'fails' : 0, 'ties' : 0}
        # сохранение конфигурации
        write_ini()   
        
    return name
    
# ---------  основная программа -----------------    

# выводим приветствие
show_title()

# читаем файл со статистикой игроков
statistics = read_ini()
# !!! временно для проверки
print(statistics)

# Если первый запуск программы то вывод справки
if len(statistics) == 0:
    show_help()

# запрашиваем имя первого игрока     
get_player_name()    
# подумать над тем где сделать проверку имени игрока в самой функции или отдельно

# Главный цикл
command = input('Введите команду: ')
while command != 'quit':
    # если новая игра
    if command == 'new' or command == 'игра':
        print('Новая игра')
        
    elif command == 'load' or command == 'загрузка':
        print('Загрузка сохраненной партии')
        
    elif command == 'dim' or command == 'размер':
        # добавить здесь обработку исключения на некорректный ввод
        temp_dim = int(input('Введите размер игрового поля в диапазоне от 3 до 20: '))
        while temp_dim < 3 or temp_dim > 20:
            print('Недопустимое значение!\n')
            temp_dim = int(input('Введите размер игрового поля в диапазоне от 3 до 20: '))
        dim = temp_dim
        
    else:
        print('Команда не найдена!\n')

    command = input('Введите команду: ')
    
# завершаем работу приложения
print('GAME OVER')    