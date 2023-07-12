from shutil import get_terminal_size 


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
    # print(out)
    return out
    
    
def show_title():
    """Выводит заголовок игры"""
    # turtles = get_terminal_size()
    width = get_terminal_size().columns - 2

    title = f'\n#{"="*width}##{" "*width}##'
    title += f'{"Игра".center(width)}##'  
    title += f'{"Крестики-Нолики".center(width)}' 
    title += f'##{" "*width}##{"="*width}#\n'
    
    print(title)

