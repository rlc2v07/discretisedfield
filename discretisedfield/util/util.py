import numpy as np


def plot_line(ax, p1, p2, color="blue", linewidth=2):
    """
    Plot a line between points p1 and p2 on axis ax.

    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    ax.plot([x1, x2], [y1, y2], [z1, z2], color=color, linewidth=linewidth)

    return ax


def plot_box(ax, p1, p2, color="blue", linewidth=2):
    """
    Plots a cube that spans between p1 and p2 on the given axis.

    Args:
      ax (matplolib axis): matplolib axis object
      p1 (tuple, list, np.ndarray): First cube point
        p1 is of length 3 (xmin, ymin, zmax).
      p2 (tuple, list, np.ndarray): Second cube point
        p2 is of length 3 (xmin, ymin, zmax).
      color (str): matplotlib color string
      linewidth (Real): matplotlib linewidth parameter

    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    # Plot individual lines (edges) of a cube.
    plot_line(ax, (x1, y1, z1), (x2, y1, z1),
              color=color, linewidth=linewidth)
    plot_line(ax, (x1, y2, z1), (x2, y2, z1),
              color=color, linewidth=linewidth)
    plot_line(ax, (x1, y1, z2), (x2, y1, z2),
              color=color, linewidth=linewidth)
    plot_line(ax, (x1, y2, z2), (x2, y2, z2),
              color=color, linewidth=linewidth)

    plot_line(ax, (x1, y1, z1), (x1, y2, z1),
              color=color, linewidth=linewidth)
    plot_line(ax, (x2, y1, z1), (x2, y2, z1),
              color=color, linewidth=linewidth)
    plot_line(ax, (x1, y1, z2), (x1, y2, z2),
              color=color, linewidth=linewidth)
    plot_line(ax, (x2, y1, z2), (x2, y2, z2),
              color=color, linewidth=linewidth)

    plot_line(ax, (x1, y1, z1), (x1, y1, z2),
              color=color, linewidth=linewidth)
    plot_line(ax, (x2, y1, z1), (x2, y1, z2),
              color=color, linewidth=linewidth)
    plot_line(ax, (x1, y2, z1), (x1, y2, z2),
              color=color, linewidth=linewidth)
    plot_line(ax, (x2, y2, z1), (x2, y2, z2),
              color=color, linewidth=linewidth)

    return ax


def plane_line_intersection(n, p0, l, l0):
    """
    Computes an intersection point between line and a plane.

    """
    n = np.array(n)
    p0 = np.array(p0)
    l = np.array(l)
    l0 = np.array(l0)

    # Compensate for Special Case 1
    # If both p0 and l0 are zero vectors, l0 is moved along the line vector,
    # so that it is a non-zero vector.
    if np.all(np.abs(p0) + np.abs(l0) == (0, 0, 0)):
        l0 += l

    if np.dot(l, n) == 0:
        # Line and plane are parallel to each other.
        if np.dot(p0-l0, n) == 0:
            # Line is contained in the plane.
            return False
        else:
            # No intersection
            return False
    else:
        d = np.dot(p0-l0, n) / np.dot(l, n)
        return tuple(d*l+l0)


def box_line_intersection(pmin, pmax, l, l0):
    points = [plane_line_intersection((1, 0, 0), pmin, l, l0),
              plane_line_intersection((1, 0, 0), pmax, l, l0),
              plane_line_intersection((0, 1, 0), pmin, l, l0),
              plane_line_intersection((0, 1, 0), pmax, l, l0),
              plane_line_intersection((0, 0, 1), pmin, l, l0),
              plane_line_intersection((0, 0, 1), pmax, l, l0)]

    # Remove False elements from the list.
    points = list(filter(lambda a: a is not False, points))

    # Find unique points.
    points = tuple(set(points))

    if len(points) != 2:
        return False
    else:
        return points
