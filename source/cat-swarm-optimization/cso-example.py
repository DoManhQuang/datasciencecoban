import math
import random

class Point(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def print_point(self):
        return str(self.name) + "[" + str(self.x) + "," + str(self.y) + "]"


def display_points_oxy(list_points):
    array_x = []
    array_y = []
    # Ox
    for point in list_points:
        array_x.append(point.x)
    # Oy
    for point in list_points:
        array_y.append(point.y)

    plt.xlabel('Ox')
    plt.ylabel('Oy')
    plt.plot(array_x, array_y, 'ro')
    plt.show()
    pass


def distance_oxy(x1, y1, x2, y2):
    return round((math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))), 4)


def random_point(size):
    list_random = []
    for i in range(0, size):
        x = round(random.uniform(0.0, 10.0), 3)
        y = round(random.uniform(0.0, 10.0), 3)
        list_random.append(Point('p' + str(i), x, y))
    return list_random


def bfs_point_fs_max(x, y, b):  #b la pham vi tim kiem
    list_random = []
    rows = [-1,  0,  1, 1, 1, 0, -1, -1]
    cols = [-1, -1, -1, 0, 1, 1,  1,  0]
    for i in range(0, 8):
        x_bfs = x + rows[i] * b
        y_bfs = y + cols[i] * b
        list_random.append(Point('p' + str(i), x_bfs, y_bfs))
    return list_random


def total_distance_oxy(point_cat, list_p):
    total_dis = 0
    for point in list_p:
        total_dis += distance_oxy(point_cat.x, point_cat.y, point.x, point.y)
    return total_dis


def fitness_value_cso(total, n, a1, a2):
    return round((a1 * total/n + a2 * n), 4)


def cat_stupid_swarm_optimization(list_point, confidence):
    a1 = -0.1
    a2 = 0.3
    n_point = len(list_point)
    n_cat = 5  # so luong meo
    n_copy_cat = 8  # so luong ban sao
    fs_point = []  # mang fitness value cua bay meo
    for i in range(0, n_cat):

        # khoi tao ngau nhien
        fitness_cat_i = 999
        fitness_cat_i_max = -999
        temp = Point('temp', 999, 999)
        result_cat = []  # ket qua cua 1 con meo
        while True:

            visit_random = False
            points_rd = []


            if visit_random is False:
                visit_random = True
                points_rd = random_point(n_copy_cat)
            else:
                b = 0.5
                points_rd = bfs_point_fs_max(temp.x, temp.y, b)

            for copy_cat in points_rd:
                total_i = total_distance_oxy(copy_cat, list_point)
                fitness_i = fitness_value_cso(total_i, n_point, a1, a2)
                if fitness_i >= fitness_cat_i_max:
                    fitness_cat_i_max = fitness_i
                    temp = copy_cat

            print(fitness_cat_i_max)
            print(temp.print_point())
            if fitness_cat_i_max < confidence:
                break

        result_cat.append(temp)
        result_cat.append(fitness_cat_i)
        fs_point.append(result_cat)
        # print(fs_point)

    return fs_point


if __name__ == '__main__':
    points = [Point('A', 1, 2),
              Point('B', 1, 4),
              Point('C', 3, 5),
              Point('D', 3, 2),
              Point('E', 5, 3),
              Point('F', 6, 1),
              Point('G', 7, 5)]

    # display_points_oxy(points)
    points_x = Point('conf', 3, 3)
    sum_d = total_distance_oxy(points_x, points)
    f_conf = fitness_value_cso(sum_d, len(points), -0.1, 0.3)
    # print(f_conf)
    fitness_list = cat_stupid_swarm_optimization(points, f_conf)
    print(fitness_list)
    pass