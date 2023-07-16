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

wins = utils.generator_wins()

def mode():
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
            bot_level = input('Введите уровень бота (l- легкий, h - сложный): ')
            while bot_level != 'l' and bot_level != 'h':
                print('Некоректный ввод!')
                bot_level = input('Введите уровень бота (l- легкий, h - сложный): ')
                
            if bot_level == 'l':
                data.active_players += ["#1"] 
                
            else:
                data.active_players += ["#2"] 
                
            break    

        else:
            print('Некоректный ввод!')
    
    while True: 
        token = input(f'\nВведите токен которым будет играть {data.active_players[0]} (X или O): ').upper()  
        if token in ['X', 'O', 'Х', 'О']:
            if token == data.TOKENS[1]:
                data.active_players[0],data.active_players[1] = data.active_players[1], data.active_players[0]        
            
            break
        else:
            print('Некоректный ввод!')  
            
           
def game() -> list[str] | None:
    """Контроллер игрового процесса.
    
    Возвращает список имён в формате ['имя_выигравшего', 'имя_проигравшего'], пустой список для ничьей или None, если партия не завершена.
   """
    data.field_template = utils.generator_field()
    #  Цикл до максимального количества ходов
    for t in range(len(data.turns), data.all_cells):
        # индекс-указатель на игрока и токен
        parity = t % 2
        print(f'\nХод игрока {data.active_players[parity]}')
        # если ход бота
        if data.active_players[parity].startswith('#'):
            get_bot_turn(data.TOKENS[parity], 'l' if data.active_players[parity] == '#1' else 'h')
        else:
            if get_human_turn(data.TOKENS[parity]):
                # сохраняем текущую партию и выходим в главное меню
                save()
                return []
        
        print_board(parity)    
        # проверка на выигрыш
        for comb in wins:
            if comb <= set(data.turns[parity::2]):
                print(f'\nПобеждает {data.active_players[parity]}\n')
                return [data.active_players[parity],data.active_players[1-parity]]
    print('\nПартия закончена. Ничья\n')    
    return []    
 
 
def get_human_turn(token: str) -> bool:
    """Запрашивает и выполняет ход игрока"""
    while True: 
        step = input('Введите номер клетки: ')
        # если пустой ввод, то завершаем партию с сохранением
        if step == '':
            return(True)
        if step.isdigit():
            step = int(step)
            if step in data.turns or step not in range(data.all_cells):
                print("Ход не допустим! ")
            else:
                data.turns.append(step)
                data.board[step] = token
                return(False)
#                break
        else:
            print(data.MESSAGES['недопустимое значение'])


def get_bot_turn(token: str, level: str):
    """Генерирует ход бота.
    Передается токен которым играет бот и уровень сложности"""
    if level == 'l':
        step_bot = bot.game_low()
        data.turns.append(step_bot)
        data.board[step_bot] = token  
    else:
        print('\n !!!!!! Режим не реализован !!!!!!\n')


def print_board(step: int):
    """Выводит игровое поле с выводом ходов"""
    max_width = max(len(str(n)) for n in data.all_cells_range)
    coords = [f'{n:>{max_width}}' for n in data.all_cells_range]
    padding = get_terminal_size().columns - (max_width+3)*data.dim*2
    if step :
        print(utils.concatenate_lines(utils.generator_field(max_width).format(*coords), data.field_template.format(*data.board.values()), padding = padding))
    else:
        print(utils.concatenate_lines(data.field_template.format(*data.board.values()), utils.generator_field(max_width).format(*coords), padding = padding))
        
        
def read_saves():    
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


def save():
    """Сохраняет текущую партию"""
    # читаем файл с сохраненными записями и обновляем структуру данных
    read_saves()
    
    # обновляем данные
    data.saves_db[frozenset({data.active_players[0], data.active_players[1]})] = {
        'X' : data.active_players[0], 
        'turns' : data.turns, 
        'dim' : data.dim 
    }

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

#    with open(data.SAVES_DB_PATH, 'a', encoding='utf-8') as fileout:
#        fileout.write(f'{data.active_players[0]},{data.active_players[1]}!{",".join(turns)}!{data.dim}')    