"""
Основной модуль: раздел помощи.
"""

# стандартная библиотека
from shutil import get_terminal_size 

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
    
    