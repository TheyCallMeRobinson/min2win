from enum import Enum
from random import randint


class GameState(Enum):
    PLAYING = 0
    LOOSE = 1


class GameCell:
    def __init__(self, value: int):
        self.value = value

    @property
    def get_value(self) -> int:
        return self.value


class Game:
    def __init__(self, rows: int, columns: int):
        self._rows = rows
        self._columns = columns
        self._state = GameState.PLAYING
        self.__field = None
        self.__score = 0
        self.__min_group = 3
        self.new_game()

    def new_game(self) -> None:
        self.__generate_field(self._columns, self._rows)
        self.__score = 0
        self._state = GameState.PLAYING

    @property
    def get_field(self) -> list:
        return self.__field

    @property
    def get_score(self) -> int:
        return self.__score

    @property
    def get_min_group_size(self) -> int:
        return self.__min_group

    @property
    def get_state(self) -> GameState:
        return self._state

    @property
    def get_rows(self) -> int:
        return self._rows

    @property
    def get_columns(self) -> int:
        return self._columns

    def __getitem__(self, coordinate: tuple) -> GameCell:
        return self.__field[coordinate[0]][coordinate[1]]

    def mouse_click(self, row: int, col: int) -> None:
        if self._state == GameState.PLAYING:
            island_size = self.__remove_group(row, col) or 0
            self.__transposition()
            self.__min_group = self.__score // 100 if self.__score >= 300 else 3
            if island_size >= self.__min_group:
                self.__fill_gaps()
            self.__score += island_size ** 2
            if self.check_defeat():
                self._state = GameState.LOOSE
        else:
            pass

    def check_defeat(self) -> bool:
        for i in range(len(self.__field)):
            for j in range(len(self.__field[i])):
                if self.__field[i][j].value != 0:
                    if len(self.__find_group(self.__field, i, j, self.__field[i][j].value)) >= 2:
                        return False
        return True

    def __find_group(self, matrix: list, i: int, j: int, value: int, friends=None) -> list:
        friends = friends or []
        if matrix[i][j].get_value == value and value != 0 and not (i, j) in friends:
            friends.append((i, j))
            if j > 0:
                self.__find_group(matrix, i, j - 1, value, friends)
            if j < len(matrix[-1]) - 1:
                self.__find_group(matrix, i, j + 1, value, friends)
            if i > 0:
                self.__find_group(matrix, i - 1, j, value, friends)
            if i < len(matrix) - 1:
                self.__find_group(matrix, i + 1, j, value, friends)
        return friends

    def __generate_field(self, size_x: int, size_y: int) -> None:
        self.__field = [[GameCell(randint(1, 4)) for _ in range(size_x)] for __ in range(size_y)]

    def __fill_gaps(self) -> None:
        for i in range(0, len(self.__field)):
            for j in range(0, len(self.__field[-1])):
                if self.__field[i][j].get_value == 0:
                    self.__field[i][j] = GameCell(randint(1, 4))

    def __remove_group(self, i: int, j: int) -> int:
        island = self.__find_group(self.__field, i, j, self.__field[i][j].get_value)
        if len(island) > 1:
            for (i, j) in island:
                self.__field[i][j] = GameCell(0)
            return len(island)
        pass

    def __transposition(self) -> None:
        for i in range(len(self.__field) - 1, 0, -1):
            for j in range(0, len(self.__field[-1])):
                if i > 0 and self.__field[i][j].get_value == 0:
                    k = i - 1
                    while k > 0 and self.__field[k][j].get_value == 0:
                        k -= 1
                    self.__field[i][j].value = self.__field[k][j].value
                    self.__field[k][j] = GameCell(0)
        for j in range(0, len(self.__field[-1])):
            if self.__field[-1][j].get_value == 0:
                k = j
                while k < len(self.__field[-1]) - 1 and self.__field[-1][k].get_value == 0:
                    k += 1
                for i in range(0, len(self.__field)):
                    self.__field[i][j].value = self.__field[i][k].value
                    self.__field[i][k] = GameCell(0)
