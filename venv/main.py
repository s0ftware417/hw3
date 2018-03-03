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


def initializ_theta(theta, poly_power, init):
    for i in range(poly_power + 1):
        theta.append(init)
    return theta


def initializ_alpha(theta, poly_power, init):
    for i in range(poly_power + 1):
        inner = []
        inner.append(init)
        inner.append(1)
        theta.append(inner)
    return theta


def compute_error_for_line_given_points(b, m, points):
    totalError = 0
    for i in range(0, len(points)):
        x = points[i][0]
        y = points[i][1]
        totalError += (y - (m * x + b)) ** 2
    return totalError / float(len(points))


def h(theta, x):
    sum = 0
    for i in range(len(theta)):
        sum += theta[i] * x ** i
    return sum


def theta_loop(theta, points, alpha):
    for i in range(len(theta)):
        sum = 0;
        for point in points:
            sum += (h(theta, point[0]) - point[1]) * point[0] ** i
        theta[i] = theta[i] - (1/len(points)*alpha*sum)
    return theta


def theta_loop_v2(theta, points, alpha):
    for i in range(len(theta)):
        sum = 0;
        for point in points:
            sum += (h(theta, point[0]) - point[1]) * point[0] ** i
        # print("theta", i, "sum =", sum, ".  alpha value =", 2**alpha[i][0], ".  previous direction =", alpha[i][1])
        if (sum >= 0) and (alpha[i][1] == -1):
            alpha[i][0] -= 1
            alpha[i][1] = 1
            # print("switching theta", i)
        if (sum <= 0) and (alpha[i][1] == 1):
            alpha[i][0] -= 1
            alpha[i][1] = -1
            # print("switching theta", i)
        theta[i] = theta[i] - ((1/len(points))*(2**alpha[i][0])*sum)
    # print()
    return theta


def main():
    s1 = "synthetic-1.csv"
    s2 = "synthetic-2.csv"
    s3 = "synthetic-3.csv"
    points = genfromtxt(s1, delimiter=',')
    poly_order = 9
    learning_rate = .01
    num_iterations = 5000
    theta = []
    theta = initializ_theta(theta, poly_order, 0)
    alpha = []
    alpha = initializ_alpha(alpha, poly_order, -9)

    pprint(theta)

    for i in tqdm(range(num_iterations)):
        # theta = theta_loop(theta, points, learning_rate)
        theta = theta_loop_v2(theta, points, alpha)
        # print(theta)

    print(theta)


    #print(gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations))
    #pprint(gradient_descent_runner_2(points, theta, learning_rate, num_iterations))


if __name__ == '__main__': main()