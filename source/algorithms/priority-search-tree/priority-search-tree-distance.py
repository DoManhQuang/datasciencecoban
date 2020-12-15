import turtle
import math
import matplotlib.pyplot as plt


class BinaryTree(object):
    def __init__(self, data):
        self.data = data
        self.index = None
        self.left = None
        self.right = None
    pass


class Points(object):
    def __init__(self, name, index, x, y):
        self.name = name
        self.index = index
        self.x = x
        self.y = y
        self.flag = False
        self.v_key = None

    def point(self):
        return str(self.name) + "[" + str(self.x) + "," + str(self.y) + "]"


def draw_tree(tree):  # ve cay

    def height(r):
        return 1 + max(height(r.left), height(r.right)) if r else -1

    def jump_to(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()

    def draw(node, x, y, dx):
        if node:
            t.goto(x, y)
            jump_to(x, y - 20)
            t.write(node.data, align='center', font=('Arial', 12, 'normal'))
            draw(node.left, x - dx, y - 60, dx / 2)
            jump_to(x, y - 20)
            draw(node.right, x + dx, y - 60, dx / 2)

    t = turtle.Turtle()
    t.speed(0)
    turtle.delay(0)
    h = height(tree)
    jump_to(0, 30 * h)
    draw(tree, 0, 30 * h, 40 * h)
    t.hideturtle()
    turtle.mainloop()


def distance_points(x1, y1, x2, y2):
    return round(math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)), 2)


def map_distance_points(list_points):
    map_distance = []

    for p1 in list_points:
        arr_dist = []
        for p2 in list_points:
            if p1.index != p2.index:
                dist = distance_points(p1.x, p1.y, p2.x, p2.y)
                arr_dist.append(dist)
            else:
                arr_dist.append(0)
        map_distance.append(arr_dist)
    return map_distance


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


def index_root_tree(list_point):  # find y max
    y_max = -9999
    id_x = -9999
    for point in list_point:
        if point.y > y_max:
            y_max = point.y
            id_x = point.index
    return id_x


def median_v_key(x_left, x_right, list_points):
    cnt = 0
    sum_x = 0
    for point in list_points:
        if point.flag is False:
            if point.x >= x_left:
                if point.x <= x_right:
                    sum_x += point.x
                    cnt += 1
    if cnt == 0:
        return -1
    return round((sum_x/cnt), 4)


def dist_min_root_and_point(index_dad, list_index):

    min_dist = 9999
    idx_min = 9999
    for index_point in list_index:
        if map_dist[index_dad][index_point] < min_dist and index_dad != index_point:
            min_dist = map_dist[index_dad][index_point]
            idx_min = index_point
    return idx_min


def construct_priority_search_tree(list_point, node_dad, index_dad, x_left, x_right):
    node_dad.index = index_dad  # update index
    v_key = median_v_key(x_left, x_right, list_point)  # find median
    if v_key == -1:
        return

    list_point[index_dad].v_key = v_key
    points_left = []
    points_right = []

    for point in list_point:
        if point.flag is False:
            if point.x < v_key:
                points_left.append(point.index)
            if point.x >= v_key:
                points_right.append(point.index)

    if len(points_right) == 0 and len(points_left) == 0:
        return

    if len(points_left) >= 1:
        index_left = dist_min_root_and_point(index_dad, points_left)  # return index point
        node_dad.left = BinaryTree(list_point[index_left].name)
        list_point[index_left].flag = True
        construct_priority_search_tree(list_point, node_dad.left, index_left, x_left, v_key)

    if len(points_right) >= 1:
        index_right = dist_min_root_and_point(index_dad, points_right)
        node_dad.right = BinaryTree(list_point[index_right].name)
        list_point[index_right].flag = True
        construct_priority_search_tree(list_point, node_dad.right, index_right, v_key, x_right)


def query_priority_search_tree(node_dad, list_point):
    if node_dad is None:
        return

    if y_priority > list_point[node_dad.index].y:
        return

    if list_point[node_dad.index].x in range(x_range_min, x_range_max+1):  # point in range(min, max)
        point_query.append(list_point[node_dad.index].name)

    if x_range_min < list_point[node_dad.index].v_key:
        query_priority_search_tree(node_dad.left, list_point)

    if x_range_max > list_point[node_dad.index].v_key:
        query_priority_search_tree(node_dad.right, list_point)


if __name__ == '__main__':

    points = [Points('A', 0, 2, 6),
              Points('B', 1, 1, 4),
              Points('C', 2, 4, 5),
              Points('D', 3, 1, 1),
              Points('E', 4, 2, 2),
              Points('F', 5, 5, 3),
              Points('G', 6, 7, 2)]

    display_points_oxy(points)
    map_dist = map_distance_points(points)
    # print(map_dist)
    index_y_max = index_root_tree(points)
    # print(points[index_y_max].name)
    root = BinaryTree(points[index_y_max].name)
    points[index_y_max].flag = True

    # construct tree
    construct_priority_search_tree(points, root, index_y_max, 0, 8)
    draw_tree(root)

    # query tree
    x_range_min = 3
    x_range_max = 5
    y_priority = 4
    point_query = []
    query_priority_search_tree(root, points)
    print("result query tree: ", point_query)


