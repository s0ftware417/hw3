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


def initializ_theta(theta, poly_power, init): #initalizes theta values based on the order
    for i in range(poly_power + 1):
        theta.append(init)
    return theta


def initializ_alpha(theta, poly_power, init): #initializes alpha values. only used with theta_loop_v2()
    for i in range(poly_power + 1):
        inner = []
        inner.append(init)
        inner.append(1)
        theta.append(inner)
    return theta


def how_much_i_suck(theta, points): #error calculation. done at the end. mean squared
    totalError = 0
    for point in points:
        totalError += (point[1] - h(theta, point[0])) ** 2
    return totalError / float(len(points))


def h(theta, x): #evaluates x for a given set of thetas and returns a predicted y valua that can be checked against the actual y
    sum = 0
    for i in range(len(theta)):
        sum += theta[i] * x ** i
    return sum


def theta_loop(theta, points, alpha): #this is the original version that has a fixed alpha
    for i in range(len(theta)):
        sum = 0
        for point in points:
            sum += (h(theta, point[0]) - point[1]) * point[0] ** i
        theta[i] = theta[i] - ((1/len(points))*alpha*sum)
    return theta


def theta_loop_v2(theta, points, alpha): #this version handles variable alpha values for each theta
    for i in range(len(theta)):
        sum = 0
        for point in points:
            sum += (h(theta, point[0]) - point[1]) * point[0] ** i
        if (sum >= 0) and (alpha[i][1] == -1): #checks to see if the slope changed form negative to positive
            alpha[i][0] -= 1 #decriments my alpha value for the corresponding theta
            alpha[i][1] = 1 #updates slope for corresponding theta
        if (sum <= 0) and (alpha[i][1] == 1): #other case for the same check
            alpha[i][0] -= 1
            alpha[i][1] = -1
        theta[i] = theta[i] - ((1/len(points))*(2**alpha[i][0])*sum)
    return theta


def formulize_v2(theta): #outputs the final function in a way that is easy for the user to read and the graphing utility to interpret
    line = ""
    for i in range(len(theta)-1):
        line += str(theta[i]) + " * x ^ " + str(i) + " + "
    line += str(theta[len(theta)-1]) + " * x ^ " + str(len(theta)-1)
    return line


def main():
    files = ["synthetic-1.csv", "synthetic-2.csv", "synthetic-3.csv"] #makes my life easy
    orders = [1,2,4,9]

    # points = genfromtxt(files[0], delimiter=',') this block is how i tested single files orders and iterations
    # poly_order = 2
    # learning_rate = .01
    # num_iterations = 1000
    # theta = []
    # theta = initializ_theta(theta, poly_order, 0)
    # alpha = []
    # alpha = initializ_alpha(alpha, poly_order, -2)
    # for i in tqdm(range(num_iterations)):
    #     theta = theta_loop(theta, points, learning_rate)
    #     # theta = theta_loop_v2(theta, points, alpha)
    # print(theta)
    # print(alpha)
    # print("Error:", how_much_i_suck(theta, points))
    # print(formulize_v2(theta))

    the_scroll_of_truth = [] #holds all the output information should I need to do anything with it
    for j in range(6): #loops through different numbers of iterations so I can see the effect on error. Used in line 9 of this function
        print()
        for file in files: #all 3 files
            points = genfromtxt(file, delimiter=',') #array of points
            for order in orders: #line 2 of main
                init_alpha = order * -1 #higher orders work best with smaller initial alpha values so i just make it 2^-order
                if order == 9:
                    init_alpha = -12 #except this case where 2^-12 is the biggest alpha I could use initially in order for it not to diverge
                num_iterations = 10 ** j
                theta = []
                theta = initializ_theta(theta, order, 0)
                alpha = []
                alpha = initializ_alpha(alpha, order, init_alpha)
                for i in range(num_iterations): #where the magic happens
                    theta = theta_loop_v2(theta, points, alpha)
                print("Iterations:", num_iterations, "\tFile:", file, "\tOrder:", order, "\tError:", how_much_i_suck(theta, points), "\tFormula:", formulize_v2(theta))
                temp = []
                temp.append(file)
                temp.append(order)
                temp.append(how_much_i_suck(theta, points))
                temp.append(formulize_v2(theta))
                the_scroll_of_truth.append(temp)
            print() #formatting
        print()



if __name__ == '__main__': main()