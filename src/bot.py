"""
Основной модуль: вычисления для бота.
"""

# стандартная библиотека
from random import randint
from collections.abc import Sequence
from numbers import Real
from random import choice
# проект
import data
import utils


# переменные для аннотации
Series = Sequence[Real | str]
Matrix = Sequence[Series]


def easy(bot_index: int) -> int:
    """ Генерирует ход для легкого уровня бота"""
    # пока так, расмотреть другие варианты
    while True:
        step_bot = randint(0, data.all_cells-1)
        if step_bot not in data.turns:
            break            
    return step_bot
    
    
def hard(bot_index: int) -> int:    
    """Вычисляет наиболее выигрышный ход и возвращает номер клетки для этого хода."""
    tw = weights_tokens(bot_index)
    if data.DEBUG:
        data.debug_data |= {'tokens': vectorization(tw)}
    ew = weights_empty(tw)
    if data.DEBUG:
        data.debug_data |= {'empty': vectorization(ew)}
    if len(data.turns) < 2*data.dim:
        ew = matrix_add(ew, data.START_MATRICES[bot_index])
    weights_clear(tw, ew)
    if data.DEBUG:
        data.debug_data |= {'result': vectorization(ew)}
    ew = vectorization(ew)
    if any(ew):
        return index_of_rand_max(ew)
    else:
        return easy(bot_index)


def weights_tokens(token_index: int) -> Matrix:
    """Конструирует и возвращает матрицу весов занятых ячеек игрового поля."""
    board = tuple(data.board.values())
    board = matricization(board)
    tokensweights = [[0]*data.dim for _ in data.dim_range]
    for i in data.dim_range:
        for j in data.dim_range:
            try:
                if board[i][j] == data.TOKENS[token_index]:
                    tokensweights[i][j] = data.WEIGHT_OWN
                elif board[i][j] == data.TOKENS[token_index-1]:
                    tokensweights[i][j] = data.WEIGHT_FOE
            except IndexError:
                pass
    return tokensweights


def weights_empty(tokensweights: Matrix) -> Matrix:
    """Вычисляет и возвращает матрицу весов пустых ячеек игрового поля."""
    emptyweights = [[0]*data.dim for _ in data.dim_range]
    weights = {data.WEIGHT_OWN, data.WEIGHT_FOE}
    for i in data.dim_range:
        for j in data.dim_range:
            if not tokensweights[i][j]:
                series = [
                    get_row(tokensweights, i),
                    get_column(tokensweights, j),
                    get_maindiag(tokensweights, i, j),
                    get_antidiag(tokensweights, i, j)
                ]
                for seq in series:
                    if not (weights <= set(seq)):
                        emptyweights[i][j] += sum(seq)**2
                emptyweights[i][j] = int(emptyweights[i][j])
    return emptyweights


def weights_clear(tokensweights: Matrix,
                  solvingweights: Matrix) -> None:
    """Обрабатывает матрицу принятия решения, приравнивая к нолю элементы, соответствующие занятым на поле клеткам."""
    for i in data.dim_range:
        for j in data.dim_range:
            if tokensweights[i][j]:
                solvingweights[i][j] = 0


def vectorization(matrix: Matrix) -> Series:
    """Возвращает плоскую последовательность, полученную в результате преобразования переданной матрицы."""
    return [cell for row in matrix for cell in row]


def matricization(sequence: Series) -> Matrix:
    """Возвращает квадратную матрицу, полученную в результате преобразования переданной плоской последовательности."""
    return [sequence[i*data.dim:(i+1)*data.dim] for i in data.dim_range]


def get_row(matrix: Matrix,
            row_index: int) -> Series:
    """Возвращает ряд матрицы по переданному индексу."""
    return matrix[row_index]


def get_column(matrix: Matrix,
               column_index: int) -> Series:
    """Возвращает столбец матрицы по переданному индексу."""
    return [row[column_index] for row in matrix]


def get_maindiag(matrix: Matrix,
                 row_index: int,
                 column_index: int) -> Series:
    """Возвращает главную диагональ матрицы, если элемент по переданным индексам ей принадлежит."""
    if row_index == column_index:
        return [matrix[i][i] for i in data.dim_range]
    return []


def get_antidiag(matrix: Matrix,
                 row_index: int,
                 column_index: int) -> Series:
    """Возвращает побочную диагональ матрицы, если элемент по переданным индексам ей принадлежит."""
    if row_index == data.dim - column_index - 1:
        return [matrix[i][-i-1] for i in data.dim_range]
    return []


def matrix_add(matrix1: Matrix,
               matrix2: Matrix,
               *matrices: Matrix) -> Matrix:
    """Возвращает результат математического сложения двух и более матриц."""
    matrices = matrix1, matrix2, *matrices
    result = [[0]*data.dim for _ in data.dim_range]
    for i in data.dim_range:
        for j in data.dim_range:
            result[i][j] = sum(m[i][j] for m in matrices)
    return result


def index_of_rand_max(series: Series) -> int:
    """Возвращает индекс случайного среди равных максимальных значений в последовательности."""
    m = max(series)
    return choice([i for i, v in enumerate(series) if v == m])


def calc_sm_cross() -> Matrix:
    """Вычисляет и возвращает начальную матрицу стратегии крестика."""
    sm_cross = [[0]*data.dim for _ in data.dim_range]
    half, rem = divmod(data.dim, 2)
    diag = list(range(1, half+1)) + list(range(half+rem, 0, -1))
    for i in data.dim_range:
        sm_cross[i][i] = diag[i]
        sm_cross[i][-i-1] = diag[i]
    return sm_cross


def calc_sm_zero() -> Matrix:
    """Вычисляет и возвращает начальную матрицу стратегии нолика."""

    def triangle_desc(n: int, start: int) -> Matrix:
        """Генерирует и возвращает верхне-треугольную по побочной диагонали матрицу, заполняемую параллельно побочной диагонали значениями по убыванию."""
        flat = []
        indexes = range(n)
        for i in indexes:
            flat += [m if m > 0 else 0 for m in range(start-i, -start, -1)][:n]
        matrix = [flat[i*n:(i+1)*n] for i in indexes]
        if n > 2:
            for i in indexes:
                for j in indexes:
                    if i > n-j-1:
                        matrix[i][j] = 0
        return matrix

    def rot90(matrix: Matrix) -> Matrix:
        """Возвращает "повёрнутую" на 90° матрицу."""
        indexes = range(len(matrix))
        matrix = [[matrix[j][i] for j in indexes] for i in indexes]
        for i in indexes:
            matrix[i] = matrix[i][::-1]
        return matrix

    half, rem = divmod(data.dim, 2)
    quarter = triangle_desc(half, half+rem)
    if data.dim > 6:
        for i in range(half):
            for j in range(half):
                if i == half-j-1:
                    if i != j:
                        quarter[i][j] -= 1
                if i > half-j:
                    quarter[i][i] = half - i - (rem+1)%2
    m1 = quarter
    m2 = rot90(m1)
    m3 = rot90(m2)
    m4 = rot90(m3)
    top, bot = [], []
    for i in range(half):
        top += [m1[i] + [0]*rem + m2[i]]
        bot += [m4[i] + [0]*rem + m3[i]]
    return top + [[0]*data.dim]*rem + bot