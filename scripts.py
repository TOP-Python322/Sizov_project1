from shutil import get_terminal_size 

# размер поля
dim = 3

# список ходов 
turns = []

all_cells = [' ']*dim

def generator_board(dim: int) -> str:
    """Генерирует шаблон игрового поля для отображения"""
    
    out = ''
    for _ in range(dim-1):
        out += ' | '.join(['{}']*dim)
        out += f'\n{"-"*(4*dim-1)}\n' 
    out += ' | '.join(['{}']*dim)
     
    return out 
    
def generator_wins(dim: int) -> list:
    """Генерирует выигрышные комбинации"""  

    out = []
    myList = [i for i in range(0, dim**2)]
    
    for i in range(dim):
        out.append({element for element in myList[i*dim:dim*(i+1)]})
        out.append({element for element in myList[i::dim]})
        
    out.append({element for element in myList[::dim+1]})    
    out.append({element for element in myList[dim-1:-1:dim-1]})
#    print(out) 
    return out
    
    
def show_title():
    """Выводит заголовок игры"""
        
    width = get_terminal_size().columns - 2

    title = f'\n#{"="*(width)}##{" "*(width)}##'    
    title += f'{"Игра".center(width)}##'  
    title += f'{"Крестики-Нолики".center(width)}' 
    title += f'##{" "*(width)}##{"="*(width)}#\n'
    
    print(title)
    
def show_help():
    """Выводит справку по игре"""  

    width = get_terminal_size().columns
    
    text_help = f'{"СПРАВКА".center(width)}\n'
    text_help += '  Приложение с интерфейсом командной строки, с помощью которого можно играть одному или вдвоём в игру крестики-нолики на квадратном поле.\n'
    
    text_help += '  После запуска приложение входит в главное меню, в котором ожидает ввод команд игрока. С помощью команд можно настраивать игру, запускать новую партию и выполнять другие действия.\n'
    

    print(text_help)