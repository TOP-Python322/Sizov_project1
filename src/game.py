"""
Основной модуль: настройка игры и игровой процесс.
"""

# проект
import players
import data
import utils

def mode():
    """Определяет режим игры"""
    
    while True:
        number = int(input('Сколько человек будет играть? Введите 1 или 2: '))
        
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
        token = input('Введите токен которым будет играть первый игрок (X или O): ')  
        if token in data.TOKENS:
            if token == data.TOKENS[1]:
                data.active_players[0],data.active_players[1] = data.active_players[1], data.active_players[0]        
            
            break
        else:
            print('Некоректный ввод!')  
            
           
def game() -> list[str] | None:
    """Контроллер игрового процесса.
    
    Возвращает список имён в формате ['имя_выигравшего', 'имя_проигравшего'], пустой список для ничьей или None, если партия не завершена.
   """
    data.field = utils.generator_field()
    #  Цикл до максимального количества ходов
    for t in range(len(data.turns), data.all_cells):
        # индекс-указатель на игрока и токен
        parity = t % 2
        print(f'ход игрока {data.active_players[parity]}')
        # если ход бота
        if data.active_players[parity].startswith('#'):
            get_bot_turn()
        else:
            get_human_turn(data.TOKENS[parity])
            
        print(data.turns)    
        # шаги 11–13
    print('\nПартия закончена.\n')    
    return False    
        
def get_human_turn(token: str):
    """Запрашивает и выполняет ход игрока"""
    while True: 
        step = int(input('Введите номер клетки: '))
        if step in data.turns or step not in range(data.all_cells):
            print("Ход не допустим! ")
        else:
            data.turns[step] = token
            break


def get_bot_turn():
    """Генерирует ход бота"""
    pass        