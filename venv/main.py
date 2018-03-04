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


def how_much_i_suck(theta, points):
    totalError = 0
    for point in points:
        totalError += (point[1] - h(theta, point[0])) ** 2
    return totalError / float(len(points))


def h(theta, x):
    sum = 0
    for i in range(len(theta)):
        sum += theta[i] * x ** i
    return sum


def theta_loop(theta, points, alpha):
    for i in range(len(theta)):
        sum = 0
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


def formulize(theta):
    for i in range(len(theta)-1):
        print(theta[i], "* x ^", i, "+", end = " ")
    print(theta[len(theta)-1], "* x ^", len(theta)-1)


def formulize_v2(theta):
    line = ""
    for i in range(len(theta)-1):
        line += str(theta[i]) + " * x ^ " + str(i) + " + "
    line += str(theta[len(theta)-1]) + " * x ^ " + str(len(theta)-1)
    return line


def main():
    files = ["synthetic-1.csv", "synthetic-2.csv", "synthetic-3.csv"]
    orders = [1,2,4,9]

    # points = genfromtxt(s2, delimiter=',')
    # poly_order = 3
    # learning_rate = .01
    # num_iterations = 1000
    # theta = []
    # theta = initializ_theta(theta, poly_order, 0)
    # alpha = []
    # alpha = initializ_alpha(alpha, poly_order, -3)
    # for i in tqdm(range(num_iterations)):
    #     theta = theta_loop_v2(theta, points, alpha)
    # print(theta)
    # print(alpha)
    # print("Error:", how_much_i_suck(theta, points))
    # print(formulize_v2(theta))

    the_scroll_of_truth = []
    for j in range(6):
        for file in files:
            points = genfromtxt(file, delimiter=',')
            for order in orders:
                init_alpha = order * -1
                if order == 9:
                    init_alpha = -12
                num_iterations = 10 ** j
                theta = []
                theta = initializ_theta(theta, order, 0)
                alpha = []
                alpha = initializ_alpha(alpha, order, init_alpha)
                for i in range(num_iterations):
                    theta = theta_loop_v2(theta, points, alpha)
                print("Iterations:", num_iterations, "\tFile:", file, "\tOrder:", order, "\tError:", how_much_i_suck(theta, points), "\tFormula:", formulize_v2(theta))
                temp = []
                temp.append(file)
                temp.append(order)
                temp.append(how_much_i_suck(theta, points))
                temp.append(formulize_v2(theta))
                the_scroll_of_truth.append(temp)
            print()
        print()
        print()



if __name__ == '__main__': main()