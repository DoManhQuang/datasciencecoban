import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm


class Points(object):
    def __init__(self, val, x, y, lbl):
        self.name = val
        self.x = x
        self.y = y
        self.label = lbl

    def print_point(self):
        return str(self.name) + " [" + str(self.x) + ", " + str(self.y) + "]: " + str(self.label)
    pass


def display_oxy(list_point, hy_svm):
    if hy_svm is not None:
        plt.plot(hy_svm[0], hy_svm[1])
        pass

    lst_ox_red = []
    lst_oy_red = []
    lst_ox_blue = []
    lst_oy_blue = []

    for point in list_point:
        if point.label == 1:
            lst_ox_red.append(point.x)
            lst_oy_red.append(point.y)
        elif point.label == -1:
            lst_ox_blue.append(point.x)
            lst_oy_blue.append(point.y)

    plt.xlabel('Ox')
    plt.ylabel('Oy')
    plt.plot(lst_ox_red, lst_oy_red, 'r+')
    plt.plot(lst_ox_blue, lst_oy_blue, 'bo')
    plt.show()
    pass


def get_data(list_point):
    x_matrix = []
    y_class = []
    for point in list_point:
        x_vector = [point.x, point.y]
        y_class.append(point.label)
        x_matrix.append(x_vector)
    return x_matrix, y_class


def get_data_hyper_lance(w_hyper, b_hyper):
    w_0 = b_hyper[0]
    w_1 = w_hyper[0][0]
    w_2 = w_hyper[0][1]
    a = -w_1/w_2
    c = -w_0/w_2
    x_data = np.linspace(2, 5, 2)
    y_data = a*x_data + c
    return x_data, y_data


if __name__ == '__main__':
    points = [
            Points('A', 1, 1, 1),
            Points('B', 1, 2, 1),
            Points('C', 1, 3, 1),
            Points('D', 2, 1, 1),
            Points('E', 2, 2, 1),
            Points('F', 2, 3, 1),
            Points('L', 3, 2, 1),
            Points('N', 3, 4, 1),
            Points('G', 6, 6, -1),
            Points('H', 5, 6, -1),
            Points('I', 5, 7, -1),
            Points('J', 6, 5, -1),
            Points('K', 6, 7, -1),
            Points('P', 4, 6, -1),
            Points('Q', 6, 4, -1),
            Points('S', 5, 5, -1)
    ]

    X, y = get_data(points)
    hyper_svm = svm.SVC(kernel='linear', C=1e5)
    hyper_svm.fit(X, y)

    w = hyper_svm.coef_
    b = hyper_svm.intercept_

    print('w = ', w)
    print('b = ', b)

    x_hyper, y_hyper = get_data_hyper_lance(w, b)
    hyper_oxy = [x_hyper, y_hyper]
    display_oxy(points, hyper_oxy)








