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