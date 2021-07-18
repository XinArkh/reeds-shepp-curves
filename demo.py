import turtle
import reeds_shepp as rs
import utils
import draw
import math
import random as rd



def main():
    # points to be followed
    pts = [(-6,-7), (-6,0), (-4, 6), (0, 5), (0,-2), (-2, -6), (3, -5), (3, 6), (6, 4)]

    # generate PATH so the vectors are pointing at each other
    PATH = []
    for i in range(len(pts) - 1):
        dx = pts[i+1][0] - pts[i][0]
        dy = pts[i+1][1] - pts[i][1]
        phi = math.atan2(dy, dx)
        PATH.append((pts[i][0], pts[i][1], phi))
    PATH.append((pts[-1][0], pts[-1][1], 0))

    # or you can also manually set the angles:
    # PATH = [(-5,5,90),(-5,5,-90),(1,4,180), (5,4,0), (6,-3,90), (4,-4,-40),(-2,0,240), \
    #         (-6, -7, 160), (-7,-1,80)]

    # or just generate a random route:
    # PATH = []
    # for _ in range(10):
    #     PATH.append((rd.randint(-7,7), rd.randint(-7,7), rd.randint(0,359)))

    # init turtle
    tesla = turtle.Turtle()
    tesla.speed(0) # 0: fast; 1: slow, 8.4: cool
    tesla.shape('arrow')
    tesla.resizemode('user')
    tesla.shapesize(1, 1)

    # draw vectors representing points in PATH
    for pt in PATH:
        draw.goto(tesla, pt)
        draw.vec(tesla)

    # draw all routes found
    tesla.speed(0)
    for i in range(len(PATH) - 1):
        paths = rs.get_all_words(PATH[i], PATH[i+1])

        for path in paths:
            draw.set_random_pencolor(tesla)
            draw.goto(tesla, PATH[i])
            draw.draw_path(tesla, path)

    # draw shortest route
    tesla.pencolor(1, 0, 0)
    tesla.pensize(3)
    tesla.speed(10)
    draw.goto(tesla, PATH[0])
    path_length = 0
    for i in range(len(PATH) - 1):
        path = rs.get_optimal_word(PATH[i], PATH[i+1])
        path_length += rs.word_length(path)
        draw.draw_path(tesla, path)

    print("Shortest path length: {} px.".format(int(draw.scale(path_length))))

    turtle.done()


if __name__ == '__main__':
    main()
