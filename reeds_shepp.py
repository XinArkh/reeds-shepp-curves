import math
import copy
from enum import Enum
import utils


class Steering(Enum):
    """
    Steering wheel, go left, straight, or right
    """
    LEFT = 1
    STRAIGHT = 0
    RIGHT = -1


class Gear(Enum):
    """
    Gear shift, go forward or backward
    """
    FORWARD = 1
    BACKWARD = -1


class Letter():
    """
    A letter is an element of a word, while a word is a possible path pattern
    """
    def __init__(self, param, steering, gear):
        self.param = param  # t, u, or v, length of the letter curve
        self.steering = steering
        self.gear = gear

    def __repr__(self):
        if self.steering == Steering.LEFT:
            steering_str = 'left'
        elif self.steering == Steering.RIGHT:
            steering_str = 'right'
        else:
            steering_str = 'straight'

        if self.gear == Gear.FORWARD:
            gear_str = 'forward'
        else:
            gear_str = 'backward'

        info_str = '{ Steering: ' + steering_str + '\tGear: ' + gear_str \
                   + '\tLength: ' + str(round(self.param, 2)) + ' }'

        return info_str

    def reverse_steering(self):
        self.steering = Steering(-self.steering.value)
        # if self.steering == Steering.LEFT:
        #     self.steering = Steering.RIGHT
        # elif self.steering == Steering.RIGHT:
        #     self.steering = Steering.LEFT

    def reverse_gear(self):
        self.gear = Gear(-self.gear.value)
        # self.gear = Gear.BACKWARD if self.gear == Gear.FORWARD else Gear.FORWARD


def word_length(word):
    return sum([abs(letter.param) for letter in word])


def timeflip(word):
    """
    Interchange + and - in a word, which results in (x, y, phi) to (-x, y, -phi)
    """
    word_new = copy.deepcopy(word)  # deepcopy method copies object **and its children**
    for letter in word_new:
        letter.reverse_gear()
    return word_new


def reflect(word):
    """
    Interchange left and right in a word, which results in (x, y, phi) to (x, -y, -phi)
    """
    word_new = copy.deepcopy(word)
    for letter in word_new:
        letter.reverse_steering()
    return word_new


def get_all_words(p1, p2):
    # 12 x 4 = 48 kinds of word patterns
    formulas = [word_cluster_1, word_cluster_2, word_cluster_3, 
                word_cluster_4, word_cluster_5, word_cluster_6, 
                word_cluster_7, word_cluster_8, word_cluster_9, 
                word_cluster_10, word_cluster_11, word_cluster_12]
    x, y, phi = utils.normalize_basis(p1, p2)
    words = []
    for f in formulas:
        words.append(f(x, y, phi))
        words.append(timeflip(f(-x, y, -phi)))
        words.append(reflect(f(x, -y, -phi)))
        words.append(reflect(timeflip(f(-x, -y, phi))))

    # remove letters that have parameter 0
    for i in range(len(words)):
        words[i] = list(filter(lambda e: e.param != 0, words[i]))

    # remove empty words
    words = list(filter(None, words))

    return words


def get_optimal_word(p1 ,p2):
    words = get_all_words(p1, p2)

    i_min = -1
    L_min = float('inf')

    for i, word in enumerate(words):
        L = word_length(word)
        if L <= L_min:
            i_min, L_min = i, L

    return words[i_min]


def word_cluster_1(x, y, phi):
    """
    Formula 8.1 for CSC words
    """
    word = []

    u, t = utils.R(x - math.sin(phi), y - 1 + math.cos(phi))
    v = utils.M(phi - t)

    params = [t, u, v]
    steerings = [Steering.LEFT, Steering.STRAIGHT, Steering.LEFT]
    gears = [Gear.FORWARD, Gear.FORWARD, Gear.FORWARD]

    for i in range(len(params)):
        word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_2(x, y, phi):
    """
    Formula 8.2 for CSC words
    """
    word = []

    u1, t1 = utils.R(x + math.sin(phi), y - 1 - math.cos(phi))
    
    if u1**2 >= 4:
        u = math.sqrt(u1**2 - 4)
        _, theta = utils.R(u, 2)
        t = utils.M(t1 + theta)
        v = utils.M(t - phi)

        params = [t, u, v]
        steerings = [Steering.LEFT, Steering.STRAIGHT, Steering.RIGHT]
        gears = [Gear.FORWARD, Gear.FORWARD, Gear.FORWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_3(x, y, phi):
    """
    Formule 8.3 for C|C|C words    *** TYPO IN PAPER ***
    """
    word = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho <= 4:
        A = math.acos(rho / 4)
        t = utils.M(theta + math.pi/2 + A)
        u = utils.M(math.pi - 2*A)
        v = utils.M(phi - t - u)

        params = [t, u, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.LEFT]
        gears = [Gear.FORWARD, Gear.BACKWARD, Gear.FORWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_4(x, y, phi):
    """
    Formule 8.4 for C|CC words    *** TYPO IN PAPER ***
    """
    word = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho <= 4:
        A = math.acos(rho / 4)
        t = utils.M(theta + math.pi/2 + A)
        u = utils.M(math.pi - 2*A)
        v = utils.M(t + u - phi)

        params = [t, u, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.LEFT]
        gears = [Gear.FORWARD, Gear.BACKWARD, Gear.BACKWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_5(x, y, phi):
    """
    Formule 8.4 for CC|C words    *** TYPO IN PAPER ***
    """
    word = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho <= 4:
        u = math.acos(1 - rho**2 / 8)
        A = math.asin(2 * math.sin(u) / rho)
        t = utils.M(theta + math.pi/2 - A)
        v = utils.M(t - u - phi)

        params = [t, u, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.LEFT]
        gears = [Gear.FORWARD, Gear.FORWARD, Gear.BACKWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_6(x, y, phi):
    """
    Formule 8.7 for CCu|CuC words
    """
    word = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho <= 4:
        if rho <= 2:
            A = math.acos((rho + 2) / 4)
            t = utils.M(theta + math.pi/2 + A)
            u = utils.M(A)
            v = utils.M(phi - t + 2*u)
        else:
            A = math.acos((rho - 2) / 4)
            t = utils.M(theta + math.pi/2 - A)
            u = utils.M(math.pi - A)
            v = utils.M(phi - t + 2*u)

        params = [t, u, u, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.LEFT, Steering.RIGHT]
        gears = [Gear.FORWARD, Gear.FORWARD, Gear.BACKWARD, Gear.BACKWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_7(x, y, phi):
    """
    Formule 8.8 for C|CuCu|C words
    """
    word = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = utils.R(xi, eta)
    u1 = (20 - rho*rho) / 16

    if rho <= 6 and 0 <= u1 and u1 <= 1:
        u = math.acos(u1)
        A = math.asin(2 * math.sin(u) / rho)
        t = utils.M(theta + math.pi/2 + A)
        v = utils.M(t - phi)

        params = [t, u, u, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.LEFT, Steering.RIGHT]
        gears = [Gear.FORWARD, Gear.BACKWARD, Gear.BACKWARD, Gear.FORWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_8(x, y, phi):
    """
    Formule 8.9 for C|C[pi/2]SC words
    """
    word = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho >= 2:
        u = math.sqrt(rho*rho - 4) - 2
        A = math.atan2(2, u+2)
        t = utils.M(theta + math.pi/2 + A)
        v = utils.M(t - phi + math.pi/2)

        params = [t, math.pi/2, u, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.STRAIGHT, Steering.LEFT]
        gears = [Gear.FORWARD, Gear.BACKWARD, Gear.BACKWARD, Gear.BACKWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_9(x, y, phi):
    """
    Formule 8.9 for CSC[pi/2]|C words
    """
    word = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho >= 2:
        u = math.sqrt(rho*rho - 4) - 2
        A = math.atan2(u+2, 2)
        t = utils.M(theta + math.pi/2 - A)
        v = utils.M(t - phi - math.pi/2)

        params = [t, u, math.pi/2, v]
        steerings = [Steering.LEFT, Steering.STRAIGHT, Steering.RIGHT, Steering.LEFT]
        gears = [Gear.FORWARD, Gear.FORWARD, Gear.FORWARD, Gear.BACKWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_10(x, y, phi):
    """
    Formule 8.10 for C|C[pi/2]SC words
    """
    word = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho >= 2:
        t = utils.M(theta + math.pi/2)
        u = rho - 2
        v = utils.M(phi - t - math.pi/2)

        params = [t, math.pi/2, u, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.STRAIGHT, Steering.RIGHT]
        gears = [Gear.FORWARD, Gear.BACKWARD, Gear.BACKWARD, Gear.BACKWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_11(x, y, phi):
    """
    Formule 8.10 for CSC[pi/2]|C words
    """
    word = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho >= 2:
        t = utils.M(theta)
        u = rho - 2
        v = utils.M(phi - t - math.pi/2)

        params = [t, u, math.pi/2, v]
        steerings = [Steering.LEFT, Steering.STRAIGHT, Steering.LEFT, Steering.RIGHT]
        gears = [Gear.FORWARD, Gear.FORWARD, Gear.FORWARD, Gear.BACKWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word


def word_cluster_12(x, y, phi):
    """
    Formule 8.11 for C|C[pi/2]SC[pi/2]|C words
    """
    word = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = utils.R(xi, eta)

    if rho >= 4:
        u = math.sqrt(rho*rho - 4) - 4
        A = math.atan2(2, u+4)
        t = utils.M(theta + math.pi/2 + A)
        v = utils.M(t - phi)

        params = [t, math.pi/2, u, math.pi/2, v]
        steerings = [Steering.LEFT, Steering.RIGHT, Steering.STRAIGHT, Steering.LEFT, Steering.RIGHT]
        gears = [Gear.FORWARD, Gear.BACKWARD, Gear.BACKWARD, Gear.BACKWARD, Gear.FORWARD]

        for i in range(len(params)):
            word.append(Letter(params[i], steerings[i], gears[i]))

    return word
