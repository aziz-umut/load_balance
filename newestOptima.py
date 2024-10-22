
import time

initial_time = time.time()

c_cont = [13,24,7,18,20,21,19,24,16,11,17,24,13,16,13,7,17,12,15,21,9,23,18,23,20,21,17,11,11,19,17,4,20,23,24,12]   # CPU usage of containers

m_cont = [23,23,24,7,23,22,24,7,20,25,12,17,21,19,24,16,11,24,9,18,22,20,24,16,18,23,20,21,17,23,13,21,17,11,21,19]   # memory usage of containers,

n = 3  # number of nodes

k = len(c_cont)  # number of containers


def average_calculator(listOfElements):  # calculates the average of the given list(listOfElements).
    """average_calculator calculates the average of the given list."""
    summation = 0
    for i in range(0, len(listOfElements)):
        summation += listOfElements[i]
    average = summation / len(listOfElements)
    return average


c_average = average_calculator(c_cont)  # average CPU usage of a container

m_average = average_calculator(m_cont)  # average memory usage of a container

print(c_average)
print(m_average)

variation = []
for i in range(0, len(c_cont)):
    variation.append(c_cont[i] + m_cont[i])

c_cont_descent = c_cont.copy()
m_cont_descent = m_cont.copy()
for i in range(0, len(variation)):
    for j in range(0, len(variation) - 1):
        if variation[j] < variation[j + 1]:
            temp_var = variation[j]
            temp_cpu = c_cont_descent[j]
            temp_memory = m_cont_descent[j]
            variation[j] = variation[j + 1]
            variation[j + 1] = temp_var
            c_cont_descent[j] = c_cont_descent[j + 1]
            c_cont_descent[j + 1] = temp_cpu
            m_cont_descent[j] = m_cont_descent[j + 1]
            m_cont_descent[j + 1] = temp_memory
print(variation)
for i in range(0, len(variation)):
    if i % 2 == 0:
        c_cont[i] = c_cont_descent[i // 2]
        m_cont[i] = m_cont_descent[i // 2]
    else:
        c_cont[i] = c_cont_descent[len(c_cont_descent) - (i + 1) // 2]
        m_cont[i] = m_cont_descent[len(m_cont_descent) - (i + 1) // 2]


print(c_cont)
print(m_cont)


def inner_sum(lst_of_elements, lst_of_index, index):
    """inner_sum calculates the total usage in one given node."""
    sum_out = 0
    for i in range(0, len(lst_of_index)):
        if lst_of_index[i] == index:
            sum_out += lst_of_elements[i]
    return sum_out


def maximum_calculator(nested_list, usage):
    """maximum_calculator calculates the maximum usage in the last assigned possible assignment list. We assign the
    lists in descending order of variation, so it basically calculates the maximum of the least-deviated possible usages
    every time."""
    temp_max = 0
    for i in range(0, n):
        temp_sum = inner_sum(usage, nested_list[len(nested_list) - 1], i)
        if temp_sum > temp_max:
            temp_max = temp_sum
    return temp_max


def minimum_calculator(nested_list, usage):
    """minimum_calculator calculates the minimum usage in the last assigned possible assignment list. We assign the
    lists in descending order of variation, so it basically calculates the minimum of the least-deviated possible usages
    every time."""
    temp_min = 1000
    for i in range(0, n):
        temp_sum = inner_sum(usage, nested_list[len(nested_list) - 1], i)
        if temp_sum < temp_min:
            temp_min = temp_sum
    return temp_min


def recursive_approximate(upper_bound, initial_length, lengthOfList, out_list, out_list_nested, occurrence,is_itFirst=True):
    """recursive_approximate function's aim is to give out a nested list in which the same number of containers are in
    each node. the output should consist of lists of 0, 1, 2 (because whe have 3 nodes) which indicates first, second,
    or third node. Its output is a nested list that contains numbers which shows which container should be assigned to
    which node."""

    if is_itFirst:  # this line is true only the first time of recursion and creates a list of zeros the same size as
        # given list.
        for i in range(0, initial_length):
            out_list.append(-2)
            is_itFirst = False
    if lengthOfList == 0:
        temp_lst = []
        is_minus = False
        for i in range(0, len(out_list)):  # this is to check if the list has any -1 which means it has a node with
            # too much deviation so that it is eliminated.
            if (out_list[i] == -1):
                is_minus = True
                break
            temp_lst.append(out_list[i])
        if not is_minus:
            out_list_nested.append(temp_lst)
            temp_upper_bound = maximum_calculator(out_list_nested, c_cont)  # maximum for CPU usage.
            temp_upper_bound_2 = maximum_calculator(out_list_nested, m_cont)  # maximum for memory usage.
            temp_lower_bound = minimum_calculator(out_list_nested, c_cont)  # minimum for CPU usage.
            temp_lower_bound_2 = minimum_calculator(out_list_nested, m_cont)  # minimum for memory usage.

            # this code dynamically checks and if necessary changes the bound. upper_bound's 0th and 1st elements are
            # cpu and memory upper limit and 2nd and 3rd are cpu and memory lower limit respectively.
            if ((temp_upper_bound - c_average) ** 2 + (temp_upper_bound_2 - m_average) ** 2 < (
                    upper_bound[0] - c_average) ** 2 + (upper_bound[1] - m_average) ** 2):
                upper_bound[0] = temp_upper_bound
                upper_bound[1] = temp_upper_bound_2

            if ((temp_lower_bound - c_average) ** 2 + (temp_lower_bound_2 - m_average) ** 2 > (
                    upper_bound[2] - c_average) ** 2 + (upper_bound[3] - m_average) ** 2):
                upper_bound[2] = temp_lower_bound
                upper_bound[3] = temp_lower_bound_2
            # print(upper_bound[0])
            # print(upper_bound[1])
            # print(upper_bound[2])
            # print(upper_bound[3])
    else:
        # this part of the code basically performs the recursion to find the possible distributions while also checks
        # upper and lower limits.
        for j in range(0, n):
            if occurrence[j] < (initial_length / n):
                out_list[lengthOfList - 1] = j
                if (inner_sum(c_cont, out_list, j) < upper_bound[0] or inner_sum(m_cont, out_list, j) < upper_bound[1]):
                    if occurrence[j] + 1 >= initial_length / n:
                        if (inner_sum(c_cont, out_list, j) < upper_bound[2] and inner_sum(m_cont, out_list, j) <
                                upper_bound[3]):
                            out_list[lengthOfList - 1] = -1
                    new_occurrence = []
                    if out_list[lengthOfList - 1] == -1:
                        return out_list_nested

                    else:
                        for k in range(0, len(occurrence)):
                            new_occurrence.append(occurrence[k])
                        new_occurrence[len(occurrence) - n + j] = occurrence[len(occurrence) - n + j] + 1
                        recursive_approximate(upper_bound, initial_length, lengthOfList - 1, out_list, out_list_nested,
                                              new_occurrence, False)
                else:
                    out_list[lengthOfList - 1] = -1
                    return out_list_nested

    return out_list_nested


# print(recursive_permutation_calculator(5, [], [], True))
# print(len(recursive_permutation_calculator(5, [], [], True)))

occurrence_nested = []
for i in range(0, n):
    occurrence_nested.append(0)
nested_assignment_lst = recursive_approximate([1000, 1000, 0, 0], len(c_cont), len(c_cont), [], [], occurrence_nested, True)
print(len(nested_assignment_lst))
for i in range(0, len(nested_assignment_lst)):
    for j in range(0, len(nested_assignment_lst[i])):
        if(nested_assignment_lst[i][j] == -1):
            print(nested_assignment_lst[i])


def x_calculator(assignment_lst, i, j):
    """x_calculator returns a value that is 1 if list's ith element is equal to j, otherwise it gives out zero. It
     is like some type of Kronecker Delta function. """
    if assignment_lst[i] == j:
        return 1
    return 0


# summation_calculator function performs the summation we intended to minimize in the first place.
# i.e. sum of the variation of each node's CPU and memory usage.


def summation_calculator(c_cont, m_cont, c_average, m_average, k, n, assignment_lst):
    """summation_calculator basically computes the sum of variations, which is what we intended to minimize in the
    first place. its output is a number which is the sum of the variations of nodes."""
    out_sum = 0
    for j in range(0, n):
        temp_sum_cpu = 0
        temp_sum_memory = 0
        for i in range(0, k):
            temp_sum_cpu += c_cont[i] * x_calculator(assignment_lst, i, j)
            temp_sum_memory += m_cont[i] * x_calculator(assignment_lst, i, j)
        temp_sum_cpu -= c_average
        temp_sum_memory -= m_average
        temp_sum_cpu = temp_sum_cpu ** 2
        temp_sum_memory = temp_sum_memory ** 2
        out_sum += temp_sum_memory + temp_sum_cpu
    return out_sum


# minima_calculator is to find the minima of the sums of possible container assignments.


def minima_calculator(nested_assignment_lst, c_cont, m_cont, c_average, m_average, k, n):
    """minima_calculator calculates the sum of variations of every possible situation that has been determined by
    recursive_approximate function. It then, by using summation_calculator, search for the minimum of those sums.
    Once it finds the minimum, it returns a list which contains the information of which container should be which
    node for the minimum deviation. It also appends this list the minimum value of that summation."""
    prev_minimum = summation_calculator(c_cont, m_cont, c_average, m_average, k, n, nested_assignment_lst[0])
    assigned_lst_min = nested_assignment_lst[0]
    for i in range(1, len(nested_assignment_lst)):
        temp_sum = summation_calculator(c_cont, m_cont, c_average, m_average, k, n, nested_assignment_lst[i])
        if (temp_sum < prev_minimum):
            prev_minimum = temp_sum
            assigned_lst_min = nested_assignment_lst[i]
    assigned_lst_min.append(prev_minimum)
    return assigned_lst_min


# final_minimum is a list that indicates which container should go to which node.
final_minimum = minima_calculator(nested_assignment_lst, c_cont, m_cont, c_average, m_average, k, n)

# this part is just printing out the assigned containers and their memory and CPU usages.
for i in range(0, n):
    temp_sum_cpu = 0
    temp_sum_memory = 0
    for j in range(0, len(final_minimum) - 1):
        if final_minimum[j] == i:
            temp_sum_cpu += c_cont[j]
            temp_sum_memory += m_cont[j]
    print("node " + str(i + 1) + "'s CPU usage = " + str(temp_sum_cpu))
    print("node " + str(i + 1) + "'s memory usage = " + str(temp_sum_memory))

for i in range(0, len(final_minimum) - 1):
    print("container " + str(i + 1) + " should be assigned to node: " + str(final_minimum[i] + 1))

now = time.time()

print(now - initial_time)
