import turtle
import random as rd
import utils
import reeds_shepp as rs


# drawing n units (eg turtle.forward(n)) will draw n * SCALE pixels
SCALE = 40


def scale(x):
    """
    Scale the input coordinate(s).
    """
    if type(x) is tuple or type(x) is list:
        return [p * SCALE for p in x]
    return x * SCALE

# note: tesla is a turtle instance

def draw_vec(tesla):
    """
    Draw an arrow.
    """
    tesla.down()
    tesla.pensize(3)
    tesla.forward(scale(1.2))
    tesla.right(25)
    tesla.backward(scale(.4))
    tesla.forward(scale(.4))
    tesla.left(50)
    tesla.backward(scale(.4))
    tesla.forward(scale(.4))
    tesla.right(25)
    tesla.pensize(1)
    tesla.up()


def goto(tesla, pos, scale_pos=True):
    """
    Go to a position without drawing.
    """
    tesla.up()
    if scale_pos:
        tesla.setpos(scale(pos[:2]))
    else:
        tesla.setpos(pos[:2])
    tesla.setheading(utils.rad2deg(pos[2]))
    tesla.down()


def draw_path(tesla, path):
    """
    Draw the path (motions in a word).
    """
    for e in path:
        gear = 1 if e.gear == rs.Gear.FORWARD else -1
        if e.steering == rs.Steering.LEFT:
            tesla.circle(scale(1), gear * utils.rad2deg(e.param))
        elif e.steering == rs.Steering.RIGHT:
            tesla.circle(- scale(1), gear * utils.rad2deg(e.param))
        elif e.steering == rs.Steering.STRAIGHT:
            tesla.forward(gear * scale(e.param))


def set_random_pencolor(tesla):
    """
    Draws noodles.
    """
    r, g, b = 1, 1, 1
    while r + g + b > 2.5:
        r, g, b = rd.uniform(0, 1), rd.uniform(0, 1), rd.uniform(0, 1)
    tesla.pencolor(r, g, b)
