"""
Основной модуль: настройка игры и игровой процесс.
"""

# проект
import players
import data

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