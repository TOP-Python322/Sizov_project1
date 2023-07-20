"""
Основной модуль: настройка игры и игровой процесс.
"""

# стандартная библиотека
from shutil import get_terminal_size 
# проект
import players
import data
import utils
import bot


def mode() -> None:
    """Определяет режим игры"""
    
    while True:
        number = int(input('\nСколько человек будет играть? Введите 1 или 2: '))
        
        # если два игрока
        if number == 2:
            # Запрос имени второго игрока
            players.get_name() 
            break
            
        # если один игрок то запрашиваем уровень бота
        elif number == 1:    
            bot_level = input(data.MESSAGES['уровень бота'])
            while bot_level != 'l' and bot_level != 'h':
                print(data.MESSAGES['недопустимое значение'])
                bot_level = input(data.MESSAGES['уровень бота'])
                
            if bot_level == 'l':
                data.active_players += ["#1"]   
                data.get_bot_turn = bot.easy
            else:
                data.active_players += ["#2"]   
                data.get_bot_turn = bot.hard    
            break    

        else:
            print(data.MESSAGES['недопустимое значение'])
    
    while True: 
        token = input(f'\nВведите токен которым будет играть {data.active_players[0]} (X или O): ').upper()  
        if token in ['X', 'O', 'Х', 'О']:
            if token == data.TOKENS[1]:
                data.active_players[0],data.active_players[1] = data.active_players[1], data.active_players[0]        
            
            break
        else:
            print(data.MESSAGES['недопустимое значение'])  
            
           
def game() -> list[str] | None:
    """Контроллер игрового процесса.
    
    Возвращает список имён в формате ['имя_выигравшего', 'имя_проигравшего'], пустой список для ничьей или None, если партия не завершена.
   """
    # Инициализация перед началом партии
    data.wins = utils.generator_wins()
    data.field_template = utils.generator_field()
    data.board = dict.fromkeys(range(data.all_cells), ' ')
    data.max_width = max(len(str(n)) for n in data.all_cells_range)
    data.coords = [f'{n:>{data.max_width}}' for n in data.all_cells_range]

    #  Цикл до максимального количества ходов
    for step in range(len(data.turns), data.all_cells):
        # индекс-указатель на игрока и токен
        parity = step % 2
        print(f'\nХод игрока {data.active_players[parity]}')
        # если ход бота
        if data.active_players[parity].startswith('#'):
            step = data.get_bot_turn(parity)      #get_bot_turn(parity)
        else:
            step = get_human_turn()
            
        if step is  None:    
            # сохраняем текущую партию и выходим в главное меню
            # читаем файл с сохраненными записями
            read_saves()
            # обновляем данные
            data.saves_db[frozenset({data.active_players[0], data.active_players[1]})] = {
                'X' : data.active_players[0], 
                'turns' : data.turns, 
                'dim' : data.dim 
            }
            # сохраняем
            save()
            print()
            return None
        # обновляем список ходов и игровое поле
        data.turns.append(step)
        data.board[step] = data.TOKENS[parity]
        print_board(parity)    
        # проверка на выигрыш
        for comb in data.wins:
            if comb <= set(data.turns[parity::2]):
                print(f'\nПобеждает {data.active_players[parity]}\n')
                return [data.active_players[parity],data.active_players[1-parity]]
    print(data.MESSAGES['ничья'])    
    return []    
 
 
def get_human_turn() -> int | None:
    """Запрашивает и выполняет ход игрока. 
      Возвращает None при принудительном завершении партии, или номер ячейки"""
    while True: 
        step = input(data.MESSAGES['ввод хода'])
        # если пустой ввод, то завершаем партию с сохранением
        if step == '':
            return(None)
        try:
            step = int(step)
        except ValueError:
            print(data.MESSAGES['ход не число'])
        else:
            if step in data.turns or step not in range(data.all_cells):
                print(data.MESSAGES['ход недопустим'])
            else:
                return(step)            



def print_board(step: int) -> None:
    """Выводит игровое поле с выводом ходов"""
    padding = get_terminal_size().columns - (data.max_width+3)*data.dim*2
    if step == 1:
        print(utils.concatenate_lines(utils.generator_field(data.max_width).format(*data.coords), data.field_template.format(*data.board.values()), padding = padding))
    else:
        print(utils.concatenate_lines(data.field_template.format(*data.board.values()), utils.generator_field(data.max_width).format(*data.coords), padding = padding))
        
        
def read_saves() -> None:    
    """Читает файл и помещает данные в структуру данных сохраненных партий"""
    # читаем файл с сохраненными записями и парсит данные
    with open(data.SAVES_DB_PATH, 'r', encoding='utf-8') as filein:
        for line in filein:
            record = line.split("!")
            users = record[0].split(",")
            turns = list(map(int, record[1].split(",")))
            dim = int(record[2])
            saves = {}
            saves['X'] = users[0]
            saves['turns'] = turns
            saves['dim'] = dim
            data.saves_db[frozenset({users[0], users[1]})] = saves  


def save() -> None:
    """Сохраняет текущую партию"""
    record = ''
    for key, value in data.saves_db.items():
        users = []
        for user in key:
            users += [user]
        
        turns = []
        for n in value['turns']:
            turns += [str(n)]
        record += f'{users[0]},{users[1]}!{",".join(turns)}!{value["dim"]}\n'  
    with open(data.SAVES_DB_PATH, 'w', encoding='utf-8') as fileout:
        fileout.write(record)           


def repeat() -> bool:
    """Запрашивает запуск новой партии с теми же настройками"""    
    repeat = input('Хотите повторить партию? (y - да, n - нет) ')
    while repeat not in ['y', 'n']:
        print(data.MESSAGES['недопустимое значение'])
        repeat = input("Введите 'y' если хотите повторить партию, или 'n' если хотите выйти в главное меню. ")
        
    if repeat == 'y':
        data.turns = [] # data.turns.clear() или так, узнать как лучше
        data.board = dict.fromkeys(range(data.all_cells), ' ')
        data.field_template = ''
        return True
        
    return False  


def load() -> bool:
    """Загрузка сохраненных партий и инициция игры перед ее возобновлением"""    
    read_saves()
    
    save_slots = [
       set(players_set - {data.authorized_player}).pop()
        for players_set in data.saves_db
        if data.authorized_player in players_set
    ]

    # если записей нет то выводим сообщение и выходим
    if len(save_slots) == 0:
        print(f'Для игрока {data.authorized_player} записи не обнаружены.')
        return False
    index_save = 0
    # если для текущего игрока доступно несколько записей
    if len(save_slots) > 1:
        print(f'Для игрока {data.authorized_player} доступны незавершенные партии со следующими игроками: ')
        for index, player in enumerate(save_slots):
            print(f'{player} -  индекс {index}')
        
        while True:   
            index_save = input('Введите индекс игрока с которым хотите возобновить партию: ')
            if index_save.isdigit():
                index_save = int(index_save)
                if index_save < len(save_slots):
                    break
            print(data.MESSAGES['недопустимое значение'])
            
    # востанавливаем список игроков
    players = frozenset({data.authorized_player, save_slots[index_save]})

    # берем нужную запись
    record = data.saves_db[players]

    data.active_players = [record['X'], set(players - {record['X']}).pop()]
    # загружаем сделанные ходы
    data.turns = record['turns'] 
    # востанавливаем настройки игры
    # если сетка не совпадает, то перенастраиваем игровое поле
    if record['dim'] != data.dim:
        data.dim = record['dim']
        utils.update_dim()
    
    # востанавливаем поле со сделанными ходами
    data.field_template = utils.generator_field()
    for index, value in enumerate(data.turns):
        data.board[value] = data.TOKENS[index%2]
   
    # выводим игровое поле с последними ходами если они были сделаны
    if len(data.turns) > 0:
        print_board((len(data.turns) + 1)%2) 
        
    return True    


def delete() -> None:
    """Удаляет запись о не сохраненной партии после ее завершения"""
    # читаем файл с сохраненными записями и обновляем структуру данных
    read_saves()
    # удаляем запись
    data.saves_db.pop(frozenset({data.active_players[0], data.active_players[1]}))
    # обновляем файл
    save()