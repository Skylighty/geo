import matplotlib.pyplot as plt
import numpy as np
import re

def get_points():
    """Collect input data from user
    first - user declares how mnay points he wants to input
    secondly - user inserts the points in format <x,y>"""
    lpoints = []
    points = {}
    no_of_points = input('Please declare how many points do you have: ')
    for i in range(int(no_of_points)):
        new_point = input(f'Please input the {i+1} point in format x,y - e.g. 7,0: ')
        if (not re.match("[0-9].*,[0-9].*", new_point)):
            print('Error! Wrong input, try again')
        else:
            new_point = new_point.split(',')
            for x in range(0, len(new_point)):
                new_point[x] = int(new_point[x])
            lpoints.append(new_point)
    points = sorted(points.items(), key=sorter)
    print(points)
    return points

def sorter(item):
    """Key to sort first by x and then by y"""
    byx = item[1][0]
    byy = item[1][1]
    return (byx, byy)

# def sort_points(points):
#     """Function sorts points in proper order
#     the far right point first, then revers-clockwise
#     with higher 'y' priority"""
#     points = sorted(points, key=lambda x:x[0])
        


def main():
    get_points()


if __name__ == "__main__":
    main()