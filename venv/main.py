from pprint import pprint
from numpy import *
import time
from math import sqrt
from tqdm import tqdm


def read_in(filename):  #reads in filename and puts it into an array of arrays called data
    f = open(filename, 'r')
    data = []
    for line in f:
        entry = line.split(",")
        temp = []
        temp.append(float(entry[0]))
        temp.append(float(entry[1]))
        data.append(temp)
    return data


def compute_error_for_line_given_points(b, m, points):
    totalError = 0
    for i in range(0, len(points)):
        x = points[i][0]
        y = points[i][1]
        totalError += (y - (m * x + b)) ** 2
    return totalError / float(len(points))


def step_gradient(b_current, m_current, points, learningRate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        x = points[i, 0]
        y = points[i, 1]
        b_gradient += -(2/N) * (y - ((m_current * x) + b_current))
        m_gradient += -(2/N) * x * (y - ((m_current * x) + b_current))
    new_b = b_current - (learningRate * b_gradient)
    new_m = m_current - (learningRate * m_gradient)
    return [new_b, new_m]


def gradient_descent_runner(points, starting_b, starting_m, learning_rate, num_iterations):
    b = starting_b
    m = starting_m
    for i in tqdm(range(num_iterations)):
        b, m = step_gradient(b, m, array(points), learning_rate)
    return [b, m]


def main():
    s1 = "synthetic-1.csv"
    s2 = "synthetic-2.csv"
    s3 = "synthetic-3.csv"
    points = genfromtxt(s1, delimiter=',')
    learning_rate = .01
    initial_b = 0
    initial_m = 0
    num_iterations = 100000
    print(gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations))
    #pprint(points)


if __name__ == '__main__': main()