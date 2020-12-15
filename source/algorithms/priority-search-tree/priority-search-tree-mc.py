# from _future_ import division
import turtle


class Points(object):
    def __init__(self, name, x, y, flag, v_key):
        self.name = name
        self.x = x
        self.y = y
        self.visited = flag
        self.middleX = v_key

    def show_point(self):
        return str(self.name) + "[" + str(self.x) + "," + str(self.y) + "]"

    def visited_is(self):
        return self.visited
    pass


class BinaryTree(object):
    def __init__(self, name, x, y, visited, v_key, number):
        self.node = Points(name, x, y, visited, v_key)
        self.number_point = number
        self.left = None
        self.right = None
    pass


def draw_tree(tree):  # ve cay

    def height(r):
        return 1 + max(height(r.left), height(r.right)) if r else -1

    def jump_to(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()

    def draw(node_tree, x, y, dx):
        if node_tree:
            view_node = str(node_tree.node.name) \
                        # + ": " + str(node_tree.node.middleX) \
                        # + "\n (" + str(node_tree.number_point) + ")" + "\n"
            t.goto(x, y)
            jump_to(x, y - 20)
            t.write(view_node, align='center', font=('Arial', 12, 'normal'))
            draw(node_tree.left, x - dx, y - 60, dx / 2)
            jump_to(x, y - 20)
            draw(node_tree.right, x + dx, y - 60, dx / 2)

    t = turtle.Turtle()
    t.speed(0)
    turtle.delay(0)
    h = height(tree)
    jump_to(0, 30 * h)
    draw(tree, 0, 30 * h, 40 * h)
    t.hideturtle()
    turtle.mainloop()


def range_max_x(list_point):
    x_max = -9999
    for point in list_point:
        if x_max < point.x:
            x_max = point.x
    return x_max


def range_min_x(list_point):
    x_min = 9999
    for point in list_point:
        if x_min > point.x:
            x_min = point.x
    return x_min


def find_point_y_min(list_point, left, right):
    point_min = Points('X', 999, 999, False, 0)
    for point in list_point:
        if point.visited is False:
            if point.x >= left:
                if point.x <= right:
                    if point.y < point_min.y:
                        point_min = point
    return point_min


def median_v_key(x_left, x_right, list_points):
    cnt = 0
    sum_x = 0
    for point in list_points:
        if point.visited is False:
            if point.x >= x_left:
                if point.x <= x_right:
                    sum_x += point.x
                    cnt += 1
    if cnt == 0:
        return None
    return round((sum_x/cnt), 4)


def construct_priority_search_tree(list_point, node_dad, x_left, x_right, x_middle):

    if x_middle is None:
        return

    left_points = []
    right_points = []

    for point in list_point:
        if point.visited is False:
            if point.x < x_middle:
                if point.x >= x_left:
                    left_points.append(point)
            elif point.x >= x_middle:
                if point.x <= x_right:
                    right_points.append(point)

    length_lp = len(left_points)
    length_rp = len(right_points)

    # FIND LEFT
    if length_lp > 0:
        node_left = find_point_y_min(left_points, x_left, x_middle)
        node_left.visited = True
        left_middle = median_v_key(x_left, x_middle, list_point)
        node_dad.left = BinaryTree(node_left.name, node_left.x, node_left.y,
                                   node_left.visited, left_middle, length_lp - 1)
        construct_priority_search_tree(list_point, node_dad.left,
                                       x_left, x_middle, left_middle)

    # FIND RIGHT
    if length_rp > 0:
        node_right = find_point_y_min(right_points, x_middle, x_right)
        node_right.visited = True
        right_middle = median_v_key(x_middle, x_right, list_point)
        node_dad.right = BinaryTree(node_right.name, node_right.x, node_right.y,
                                    node_right.visited, right_middle, length_rp - 1)
        construct_priority_search_tree(list_point, node_dad.right,
                                       x_middle, x_right, right_middle)
    pass


def query_priority_search_tree(tree, x_min, x_max, y_priority):
    if tree is None:
        return

    if y_priority < tree.node.y:
        return

    if tree.node.x in range(x_min, x_max + 1):
        result_query.append(tree.node.name)

    if x_min < tree.node.middleX:
        query_priority_search_tree(tree.left, x_min, x_max, y_priority)  # find left

    if x_max > tree.node.middleX:
        query_priority_search_tree(tree.right, x_min, x_max, y_priority)  # find right


def insert_node_to_tree(new_point, tree):

    temp_p = Points('temp', 999, 999, False, 0)

    if temp_p.name == new_point.name:
        return

    middle_old = tree.node.middleX
    if middle_old is None:
        middle_old = 0
    number_old = tree.number_point
    tree.number_point = number_old + 1  # cap nhap so luong node

    if new_point.y < tree.node.y:
        temp_p = tree.node
        tree.node = new_point
    else:
        temp_p = new_point

    middle_new = round(((middle_old * number_old + temp_p.x)/(number_old + 1)), 4)
    tree.node.middleX = middle_new
    if temp_p.x < middle_new:
        if tree.left is None:
            temp_p.visited = True
            tree.left = BinaryTree(temp_p.name, temp_p.x, temp_p.y,
                                   temp_p.visited, temp_p.middleX, 0)
            return
        else:
            insert_node_to_tree(temp_p, tree.left)
    else:
        if tree.right is None:
            temp_p.visited = True
            tree.right = BinaryTree(temp_p.name, temp_p.x, temp_p.y,
                                    temp_p.visited, temp_p.middleX, 0)
            return
        else:
            insert_node_to_tree(temp_p, tree.right)


def delete_node_from_tree(old_node, tree):
    if tree is None:
        return

    # cap nhap lai middle
    middle_old = tree.node.middleX
    number_old = tree.number_point
    tree.number_point = number_old - 1

    if tree.left is not None and tree.right is not None:
        if number_old - 1 == 0:
            middle_new = 0
        else:
            middle_new = round((((middle_old * number_old) - old_node.x) / (number_old - 1)), 4)
        tree.node.middleX = middle_new

    # kiem tra node
    if tree.node.name == old_node.name:
        if tree.left is None and tree.right is None:
            tree.node = None
            return
        else:
            if tree.left is not None:
                if tree.right is not None:
                    if tree.left.node.y < tree.right.node.y:
                        tree.node = tree.left.node  # uu tien ben trai
                        delete_node_from_tree(tree.left.node, tree.left)
                        if tree.left.node is None:
                            tree.left = None

                    else:
                        tree.node = tree.right.node  # uu tien ben phai
                        delete_node_from_tree(tree.right.node, tree.right)
                        if tree.right.node is None:
                            tree.right = None

                else:
                    tree.node = tree.left.node  # con chi ben trai
                    delete_node_from_tree(tree.left.node, tree.left)
                    if tree.left.node is None:
                        tree.left = None

            else:
                tree.node = tree.right.node  #con chi ben phai
                delete_node_from_tree(tree.right.node, tree.right)
                if tree.right.node is None:
                    tree.right = None

    # duyet cay
    else:
        if old_node.x < middle_old:
            delete_node_from_tree(old_node, tree.left)

        if old_node.x > middle_old:
            delete_node_from_tree(old_node, tree.right)


def min_y_in_xrange(x_min, x_max, tree):
    global temp
    if tree is None:
        return

    if tree.node.y > temp.y:
        return

    if tree.node.x in range(x_min, x_max + 1):
        if tree.node.y < temp.y:
            temp = tree.node
            return

    if x_min < tree.node.middleX:
        min_y_in_xrange(x_min, x_max, tree.left)  # find left

    if x_max > tree.node.middleX:
        min_y_in_xrange(x_min, x_max, tree.right)  # find right


if __name__ == '__main__':

    # construct tree
    points = [Points('A', 2, 6, False, 0),
              Points('B', 1, 4, False, 0),
              Points('C', 4, 5, False, 0),
              Points('D', 1, 1, False, 0),
              Points('E', 2, 2, False, 0),
              Points('F', 5, 3, False, 0),
              Points('G', 7, 2, False, 0)]

    range_left = range_min_x(points)
    range_right = range_max_x(points)
    node_root = find_point_y_min(points, range_left, range_right)
    node_root.visited = True
    middle_root = median_v_key(range_left, range_right, points)
    root = BinaryTree(node_root.name, node_root.x, node_root.y,
                      node_root.visited, middle_root, len(points) - 1)
    construct_priority_search_tree(points, root, range_left, range_right, middle_root)

    # insert node
    point_new = Points('H', 2, 3, False, 0)
    insert_node_to_tree(point_new, root)

    # # delete node
    # node_del = Points('E', 2, 2, False, 0)
    # delete_node_from_tree(node_del, root)

    # view tree
    draw_tree(root)

    # query tree
    result_query = []
    query_priority_search_tree(root, 1, 8, 2)
    print('range(min, max): [1, 8]')
    print('y priority: 2')
    print('Ket qua tim kiem: ', result_query)

    # min y in x range
    temp = Points('temp', 999, 999, False, 0)
    min_y_in_xrange(2, 4, root)
    print('min y in x range(2, 4): ')
    print('ket qua tim kiem la: ', temp.name)