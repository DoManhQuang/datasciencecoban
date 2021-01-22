import numpy as np
import matplotlib.pyplot as plt


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


def hyper_lance(vector_x, vector_w):
    return np.sign(np.dot(vector_w.T, vector_x))


def update_rule_w(vector_w, vector_x, y_ex):
    return vector_w + vector_x * y_ex


# dau vao tat ca du lieu diem
# cac diem chua dc phan loai
def miss_classification(hyper_function, w_vector, x_matrix, y_class):
    y_vector = np.apply_along_axis(hyper_function, 1, x_matrix, w_vector)
    miss_point = x_matrix[y_class != y_vector]
    return miss_point


def pick_one_from_class_miss(miss_point, x_matrix, y_ex):
    np.random.shuffle(miss_point)
    x_vector = miss_point[0]
    index = np.where(np.all(x_matrix == x_vector, axis=1))
    return x_vector, y_ex[index]


def svm_pla(x_matrix, y_vector):
    w_vector = np.random.rand(3)
    point_miss_class = miss_classification(hyper_lance, w_vector,
                                           x_matrix, y_vector)  # thu ngau nhien
    while point_miss_class.any():
        x_vector, y_ex = pick_one_from_class_miss(point_miss_class,
                                                  x_matrix, y_vector)
        w_vector = w_vector + x_vector * y_ex
        point_miss_class = miss_classification(hyper_lance, w_vector,
                                               x_matrix, y_vector)
    return w_vector


def get_data_point(list_point):
    x_matrix = []
    y_class = []
    for point in list_point:
        x_vector = [1, point.x, point.y]
        y_class.append(point.label)
        x_matrix.append(x_vector)
    return x_matrix, y_class


def get_data_hyper_lance(w_hyper):
    w_0 = w_hyper[0]
    w_1 = w_hyper[1]
    w_2 = w_hyper[2]
    a = -w_1/w_2
    c = -w_0/w_2
    x_data = np.linspace(2, 4, 3)
    y_data = a*x_data + c
    return [x_data, y_data]


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

    matrix, vector = get_data_point(points)
    X = np.array(matrix)
    y = np.array(vector)
    # print(X)
    # print(y)
    w_012 = svm_pla(X, y)
    print(w_012)
    hyper_lance_svm = get_data_hyper_lance(w_012)
    display_oxy(points, hyper_lance_svm)




