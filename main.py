"""
from game import *

__field = [
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 0, 1]
]
for i in range(len(__field) - 1, 0, -1):
    for j in range(0, len(__field[-1])):
        if i > 0 and __field[i][j] == 0:
            k = i - 1
            while k > 0 and __field[k][j] == 0:
                k -= 1
            __field[i][j] = __field[k][j]
            __field[k][j] = 0
for j in range(0, len(__field[-1])):
    if __field[-1][j] == 0:
        k = j
        while k < len(__field[-1]) - 1 and __field[-1][k] == 0:
            k += 1
        for i in range(0, len(__field)):
            __field[i][j] = __field[i][k]
            __field[i][k] = 0

for i in range(0, len(__field)):
    print(__field[i])


def find_group(matrix: list, i: int, j: int, value: int, friends=None) -> list:
    friends = friends or []
    if matrix[i][j] == value and value != 0 and not (i, j) in friends:
        friends.append((i, j))
        if j > 0:
            find_group(matrix, i, j - 1, value, friends)
        if j < len(matrix[-1]) - 1:
            find_group(matrix, i, j + 1, value, friends)
        if i > 0:
            find_group(matrix, i - 1, j, value, friends)
        if i < len(matrix) - 1:
            find_group(matrix, i + 1, j, value, friends)
    return friends


lst = find_group(__field, 1, 1, 1)
print(lst)

"""

import sys
import traceback

from MainFrame import MainWindow

from PyQt5.QtWidgets import QApplication, QMessageBox


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()

    def exception_hook(type_, value, tb):
        msg = '\n'.join(traceback.format_exception(type_, value, tb))
        # print(msg)
        QMessageBox.critical(mw, 'Unhandled top level exception', msg)

    sys.excepthook = exception_hook

    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
