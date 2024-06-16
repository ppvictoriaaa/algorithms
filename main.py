import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

X = np.array([[ 0.61, 0.71, -0.05],
                [ -1.03, -2.05,  0.87],
                [ 2.5, -3.12,  5.03]])
Y = np.array([[1.], [2.], [2.]])

A = np.concatenate((X, Y), axis=1)

def solve_sistem(X,Y):
    A = np.concatenate((X, Y), axis=1)
    # Приведение матрицы к треугольному виду
    for i in range(len(A)):
        amax = A[i][i]
        for j in range(i+1, len(A)):
            if A[j][i]>amax:
                amax = A[j][i]
                l = j

        a = np.array(A[i])
        b = np.array(A[l])
        A[i] = b
        A[l] = a

    for i in range(len(A)):
        A[i] = A[i] / A[i][i]
        for k in range(len(A)):
            if k!=i:
                A[k] = A[k] - A[k][i]*A[i]
    return A[0:3,3]

if __name__ == '__main__':
    X = np.array([[ 0.61, 0.71, -0.05],
                    [ -1.03, -2.05,  0.87],
                    [ 2.5, -3.12,  5.03]])
    Y = np.array([[-0.16], [0.5], [0.95]])
    print(solve_sistem(X,Y))

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.move(300, 150)
        self.setWindowTitle('Lab5')
        self.font = QFont("Arial", 8, QFont.Bold)
        self.font.setPointSize(11)
        self.setStyleSheet("background-color:yellowgreen")
        self.TEXTSIZE = 12


        x = [[ 0.61, 0.71, -0.05],
            [ -1.03, -2.05,  0.87],
            [ 2.5, -3.12,  5.03]]
        y = [-0.16, 0.5, 0.95]

        self.x = [[QLineEdit() for _ in range(3)] for _ in range(3)]
        for i in range(len(self.x)):
            for j in range(len(self.x[0])):
                self.x[i][j].setText(str(x[i][j]))
                self.x[i][j].setMaximumSize(50, 50)
                self.x[i][j].setStyleSheet("background-color:white")
        self.y = [QLineEdit() for _ in range(3)]
        for i in range(len(self.x)):
            self.y[i].setText(str(y[i]))
            self.y[i].setMaximumSize(50, 50)
            self.y[i].setStyleSheet("background-color:white")

        self.x_lable = [[QLabel('X' + str(i + 1) + ' + ') for i in range(3)] for _ in range(3)]

        for i in self.x_lable:
            for j in i:
                j.setFont(QFont("Arial", self.TEXTSIZE, QFont.Bold))
        self.equal = [QLabel(' = ') for i in range(3)]
        for i in self.equal:
            i.setFont(QFont("Arial", self.TEXTSIZE, QFont.Bold))



        self.xlable = QLabel('X = ?')

        button_show_ideal = QPushButton("Вирішити")
        button_show_ideal.clicked.connect(self.solve)
        button_show_ideal.setFont(QFont("Arial", self.TEXTSIZE, QFont.Bold))
        button_show_ideal.setStyleSheet("background-color:olivedrab")


        for i in range(3):
            for j in range(1, 4):
                grid.addWidget(self.x_lable[i][j - 1], i + 2, (j) * 2 - 1)

                grid.addWidget(self.x[i][j - 1], i + 2, (j) * 2)
            print(self.equal[i])

            grid.addWidget(self.equal[i], i + 2, (j) * 2 + 1)
            grid.addWidget(self.y[i], i + 2, (j) * 2 + 2)

        grid.addWidget(button_show_ideal, 7, 0, 1, 10)

        self.rez = QLabel('')
        grid.addWidget(self.rez, 9, 0, 1, 10)


        label2 = QLabel(self)
        label2.setText("Заповніть матрицю СЛАР")
        label2.setFont(QFont("Arial", 14, QFont.Bold))
        grid.addWidget(label2, 1, 0, 1, 10)


        self.show()

    def solve(self):
        X = np.array([i[0] for i in np.linalg.solve(*self.get_matrixes())]).round(4)

        self.rez.setText('Результат:\n'
                         'X1 = {}\n'
                         'X2 = {}\n'
                         'X3 = {}'.format(*X))
        self.rez.setFont(QFont("Arial", self.TEXTSIZE, QFont.Bold))


    def get_matrixes(self):
        A = np.array([[float(j.text()) for j in i] for i in self.x])
        Y = np.array([[float(j.text())] for j in self.y])
        return A, Y


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
