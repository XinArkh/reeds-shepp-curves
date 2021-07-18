import math
import turtle
import random as rd
import draw
import utils
import reeds_shepp as rs



def main():
    # assign points to be followed
    pts = [(-6, -7), (-6, 0), (-4, 6), 
           (0, 5), (0, -2), (-2, -6), 
           (3, -5), (3, 6), (6, 4)]

    # generate path nodes (x, y, phi)
    path_nodes = []

    for i in range(len(pts) - 1):

        # 1. let the vectors point at their successor
        dx = pts[i+1][0] - pts[i][0]
        dy = pts[i+1][1] - pts[i][1]
        phi = math.atan2(dy, dx)
        
        # 2. or generate random directions
        # phi = rd.random() * math.pi * 2
        
        path_nodes.append((pts[i][0], pts[i][1], phi))

    path_nodes.append((pts[-1][0], pts[-1][1], 0))  # assign the last node

    # 3. or generate a random route
    # for _ in range(10):
    #     path_nodes.append( (rd.randint(-7,7), rd.randint(-7,7), rd.random() * math.pi * 2) )

    # init turtle
    tesla = turtle.Turtle()
    tesla.speed(0)  # 0: fast; 1: slow; 8.4: cool
    tesla.shape('arrow')
    tesla.resizemode('user')
    tesla.shapesize(1, 3)

    # draw vectors representing the nodes
    for node in path_nodes:
        draw.goto(tesla, node)
        draw.draw_vec(tesla)

    # draw all routes found
    tesla.speed(0)
    for i in range(len(path_nodes) - 1):
        paths = rs.get_all_words(path_nodes[i], path_nodes[i+1])

        for path in paths:
            draw.set_random_pencolor(tesla)
            draw.goto(tesla, path_nodes[i])
            draw.draw_path(tesla, path)

    # draw the shortest route
    tesla.pencolor(1, 0, 0)
    tesla.pensize(3)
    tesla.speed(10)
    draw.goto(tesla, path_nodes[0])
    path_length = 0
    for i in range(len(path_nodes) - 1):
        path = rs.get_optimal_word(path_nodes[i], path_nodes[i+1])
        path_length += rs.word_length(path)
        draw.draw_path(tesla, path)

    print("Shortest path length: {} px.".format(int(draw.scale(path_length))))

    turtle.done()


if __name__ == '__main__':
    main()
