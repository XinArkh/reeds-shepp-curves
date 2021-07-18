import math
import turtle
import random as rd
import draw
import utils
import reeds_shepp as rs


def gen_path_nodes():
    # assign points to be followed
    pts = [(-6, -7), (-6, 0), (-4, 6), 
           (0, 5), (0, -2), (-2, -6), 
           (3, -5), (3, 6), (6, 4)]

    # generate path nodes (x, y, phi)
    path_nodes = []
    for i in range(len(pts) - 1):
        # 1. let the vectors point at their successor
        # dx = pts[i+1][0] - pts[i][0]
        # dy = pts[i+1][1] - pts[i][1]
        # phi = math.atan2(dy, dx)
        
        # 2. or generate random directions
        phi = rd.random() * math.pi * 2
        
        path_nodes.append((pts[i][0], pts[i][1], phi))
    path_nodes.append((pts[-1][0], pts[-1][1], 0))  # assign the last node

    # 3. or generate a random path
    # path_nodes = []
    # for _ in range(10):
    #     path_nodes.append( (rd.randint(-7,7), rd.randint(-7,7), rd.random() * math.pi * 2) )

    return path_nodes


def init_turtle():
    turtle.screensize(100, 100)
    tesla = turtle.Turtle()
    tesla.speed(0)  # 0: fast; 1: slow; 8.4: cool
    tesla.shape('arrow')
    tesla.resizemode('user')
    tesla.shapesize(1, 3)

    return tesla


def draw_nodes(path_nodes, tesla):
    for node in path_nodes:
        draw.goto(tesla, node)
        draw.draw_vec(tesla)


def draw_all_paths(path_nodes, tesla, s=0):
    tesla.speed(s)
    for i in range(len(path_nodes) - 1):
        paths = rs.get_all_words(path_nodes[i], path_nodes[i+1])
        for path in paths:
            draw.set_random_pencolor(tesla)
            draw.goto(tesla, path_nodes[i])
            draw.draw_path(tesla, path)


def draw_optimal_path(path_nodes, tesla):
    tesla.pencolor(1, 0, 0)
    tesla.pensize(3)
    tesla.speed(10)
    draw.goto(tesla, path_nodes[0])
    path_length = 0
    optimal_path = []
    for i in range(len(path_nodes) - 1):
        path = rs.get_optimal_word(path_nodes[i], path_nodes[i+1])
        optimal_path.append(path)
        path_length += rs.word_length(path)
        draw.draw_path(tesla, path)
    return optimal_path, path_length


def main():
    path_nodes = gen_path_nodes()
    tesla = init_turtle()

    draw_nodes(path_nodes, tesla)  # draw vectors representing the nodes
    draw_all_paths(path_nodes, tesla)  # draw all paths found
    optimal_path, path_length = draw_optimal_path(path_nodes, tesla)  # draw the optimal path

    print( "Optimal path length: {} px.".format(round(path_length)) )
    print('Optimal path:')
    for i, path in enumerate(optimal_path):
        print('{}:\t{}'.format(i, path))
    turtle.done()


if __name__ == '__main__':
    main()
