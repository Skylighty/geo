from vertex import Vertex, VertexList
import matplotlib.pyplot as plt
import numpy as np
import bmesh
import math
import re

#xs_test = [3, 6, 8, 7, 11, 14, 13, 11, 9, 7, 5, 6, 5, 4, 1]
#ys_test = [0, 2, -2, 5, 4, 10, 9, 15, 13, 15, 12, 10, 7, 9, 4]


def add_vertexes(vertex_list, sorted_points):
    for i in sorted_points:
        vertex_list.vappend(Vertex(sorted_points[i]))


def user_input(whicho):
    """Collect input data from user
    first - user declares how mnay points he wants to input
    secondly - user inserts the points in format <x,y>"""
    xs = []
    ys = []
    list_points = []
    no_of_points = input('Please input how many points do you have: ')
    for i in range(int(no_of_points)):
        new_point = input(
            f'Please input the {i+1} point in format x,y - e.g. 7,0: ')
        # if (not re.match("[0-9].*,[0-9].*", new_point)):
        #    print('Error! Wrong input, try again')
        # else:
        new_point = new_point.split(',')
        list_points.append(int(new_point[0]), int(new_point[1]))
        xs.append(int(new_point[0]))
        ys.append(int(new_point[1]))
    xs = np.array(xs)
    ys = np.array(ys)
    if (whicho == True):
        return xs, ys
    else:
        return list_points


def sortsort(pts_list):
    sorted_pts = sorted(pts_list, key=clockwiseangle_and_distance)
    return sorted_pts


def clockwiseangle_and_distance(point, origin):
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod = normalized[0]*refvec[0] + \
        normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - \
        refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector


def listify(xs, ys):
    listed = []
    for i in range(len(xs)):
        listed.append([xs[i], ys[i]])
    return listify

# def sort_xy(x, y, iflist):
#     """Sort points reverse-clockwise
#     basing on angle since the starting point
#     then rolls the array so the order starts from
#     the far-right vertex"""
#     x0 = np.mean(x)
#     y0 = np.mean(y)
#     r = np.sqrt((x-x0)**2 + (y-y0)**2)
#     angles = np.where((y-y0) > 0, np.arccos((x-x0)/r),
#                       2*np.pi-np.arccos((x-x0)/r))
#     mask = np.argsort(angles)
#     x_sorted = x[mask]
#     y_sorted = y[mask]

#     # Find max 'x' and shift the lists
#     max_index = np.argmax(x_sorted)
#     x_sorted = np.roll(x_sorted, 0-max_index)
#     y_sorted = np.roll(y_sorted, 0-max_index)

#     # Present sorted points as list of lists
#     sorted_points = []
#     for i in range(len(x_sorted)):
#         sorted_points.append([x_sorted[i], y_sorted[i]])

#     # Return list of lists (points) or lists of xs and ys
#     if iflist == True:
#         return sorted_points
#     else:
#         return x_sorted, y_sorted


def main():
    xs_test = np.array([3, 6, 8, 7, 11, 14, 13, 11, 9, 7, 5, 6, 5, 4, 1])
    ys_test = np.array([0, 2, -2, 5, 4, 10, 9, 15, 13, 15, 12, 10, 7, 9, 4])
    lpts = listify(xs_test, ys_test)
    center = tuple(map(operator.truediv, reduce(
        lambda x, y: map(operator.add, x, y), lpts), [len(lpts)] * 2))
    print(sorted(lpts, key=lambda coord: (-135 - math.degrees(math.atan2(*
          tuple(map(operator.sub, coord, center))[::-1]))) % 360))
    sorted_points = sortsort(lpts)
    print(sorted_points)
    vl = VertexList()
    for i in sorted_points:
        vl.vappend(Vertex(i))
    vl.calculate_vertex_params()
    for vertex in vl.vlist:
        vertex.vprint()
    for vertex in vl.vlist:
        print(vertex.vtype)
        print(vertex.y)
        print(vertex.next.y)
        print(vertex.prev.y)


if __name__ == "__main__":
    main()
