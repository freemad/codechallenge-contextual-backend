import math


def calculate_distance(end, start):
    return math.sqrt(pow(end.x - start.x, 2) + pow(end.y - start.y, 2))


def calculate_velocity(distance, time_sec):
    return distance / time_sec
