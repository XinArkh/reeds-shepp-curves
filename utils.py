import math


def R(x, y):
    """
    Polar transform (r, theta) for (x, y)
    """
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta


def M(theta):
    """
    Map theta to [-pi, pi)
    """
    theta %= 2 * math.pi
    if theta < -math.pi: theta += 2 * math.pi
    elif theta >= math.pi: theta -= 2 * math.pi
    return theta


def normalize_basis(p1, p2):
    """
    Normalize the basis so that p1 equals (0, 0, 0)
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    phi1 = p1[2]
    # Rotation matrix with -phi
    x_new = math.cos(phi1) * dx + math.sin(phi1) * dy
    y_new = -math.sin(phi1) * dx + math.cos(phi1) * dy
    phi_new = p2[2] - p1[2]
    return x_new, y_new, phi_new


def rad2deg(rad):
    return rad / math.pi * 180