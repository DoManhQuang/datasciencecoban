import math
import random
import matplotlib.pyplot as plt


class Point(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.fitness = -999

    def print_point(self):
        return str(self.name) + "[" + str(self.x) + "," + str(self.y) + "]: " + str(self.fitness)


def display_points_oxy(list_points, point_temp):
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
    plt.plot(array_x, array_y, 'go')
    plt.plot(point_temp.x, point_temp.y, 'rx')
    plt.show()
    pass

def display_points_oxy_10_test(list_points, opt_x, opt_y):
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
    plt.plot(array_x, array_y, 'go')
    plt.plot(opt_x, opt_y, 'rx')
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
    
    # khoi tao ngau nhien
    a1 = -0.1
    a2 = 0.3
    n_point = len(list_point)
    n_cat = 5  # so luong meo
    n_copy_cat = 8  # so luong ban sao
    fs_point = []  # mang fitness value cua bay meo

    for i in range(0, n_cat):
        temp = Point('temp', 999, 999)
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
                copy_cat.fitness = fitness_value_cso(total_i, n_point, a1, a2)
                if copy_cat.fitness >= temp.fitness:
                    temp = copy_cat

            # print(temp.print_point())
            if copy_cat.fitness > confidence:
                break

        fs_point.append(temp)
        # print(fs_point)

    fs_max = Point('temp_max', 999, 999)
    for fs_i in fs_point:
        if fs_i.fitness >= fs_max.fitness:
            fs_max = fs_i
    fs_max.name = 'cat_fs_max'

    return fs_max


if __name__ == '__main__':
    points = [Point('A', 1, 2),
              Point('B', 1, 4),
              Point('C', 3, 5),
              Point('D', 3, 2),
              Point('E', 5, 3),
              Point('F', 6, 1),
              Point('G', 7, 5)]

    # tinh diem ky vong
    points_conf = Point('conf', 3, 3)
    sum_d = total_distance_oxy(points_conf, points)
    f_conf = fitness_value_cso(sum_d, len(points), -0.1, 0.3)
    print('confidence: ', f_conf)
    display_points_oxy(points, points_conf)

    # cso
    cat_fitness_max = cat_stupid_swarm_optimization(points, f_conf)
    print(cat_fitness_max.print_point())
    display_points_oxy(points, cat_fitness_max)

    # ket qua chay thu 10 lan
    opt_x = [3.71, 3.592, 3.359, 3.534, 3.533, 3.591, 3.559, 3.586, 3.475, 3.641]
    opt_y = [2.961 ,3.083 ,3.193 ,3.041 ,3.044 ,3.056 ,2.9 ,3.007 ,2.964 ,3.038]
    opt_x.append(cat_fitness_max.x)
    opt_y.append(cat_fitness_max.y)
    display_points_oxy_10_test(points, opt_x, opt_y)

    pass