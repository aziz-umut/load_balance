c_cont = [45,64,20,65,80,138,56,48,100,100,73,90,120,88,16]   # CPU usage of containers

m_cont = [34,130,82,56,60,27,20,103,76,54,45,100,77,45,110]   # memory usage of containers,

n = 3  # number of nodes

k = len(c_cont)  # number of containers

def average_calculator(listOfElements):  # calculates the average of the given list(listOfElements).
    summation = 0
    for i in range(0, len(listOfElements)):
        summation += listOfElements[i]
    average = summation / len(listOfElements)
    return average


c_average = average_calculator(c_cont)  # average CPU usage of a container

m_average = average_calculator(m_cont)  # average memory usage of a container

# print(c_average)
# print(m_average)


def inner_sum(lst_of_elements, lst_of_index, index):
    sum_out = 0
    for i in range(0, len(lst_of_index)):
        if lst_of_index[i] == index:
            sum_out += lst_of_elements[i]
    return sum_out


def maximum_calculator(nested_list, usage):
    temp_max = 0
    for i in range(0, n):
        temp_sum = inner_sum(usage, nested_list[len(nested_list) - 1], i)
        if temp_sum > temp_max:
            temp_max = temp_sum
    return temp_max


def minimum_calculator(nested_list, usage):
    temp_min = 1000
    for i in range(0, n):
        temp_sum = inner_sum(usage, nested_list[len(nested_list) - 1], i)
        if temp_sum < temp_min:
            temp_min = temp_sum
    return temp_min


# recursive_approximate function's aim is to give out a nested list in which the same number of containers are in each
# node. the output should consist of lists of 0, 1, 2 (because whe have 3 nodes) which indicates first, second, or
# third node.


def recursive_approximate(upper_bound, initial_length, lengthOfList, out_list, out_list_nested, occurrence,is_itFirst=True):
    if is_itFirst:  # this line is true only the first time of recursion and creates a list of zeros the same size as
        # given list.
        for i in range(0, initial_length):
            out_list.append(-1)
            is_itFirst = False
    if (lengthOfList == 0):
        temp_lst = []
        is_minus = False
        for i in range(0, len(out_list)):
            if (out_list[i] == -1):
                is_minus = True
                break
            temp_lst.append(out_list[i])
        if (not is_minus):
            out_list_nested.append(temp_lst)
            temp_upper_bound = maximum_calculator(out_list_nested, c_cont)
            temp_upper_bound_2 = maximum_calculator(out_list_nested, m_cont)
            temp_lower_bound = minimum_calculator(out_list_nested, c_cont)
            temp_lower_bound_2 = minimum_calculator(out_list_nested, m_cont)

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
        for j in range(0, n):
            if occurrence[j] < (initial_length / n):
                out_list[lengthOfList - 1] = j
                if (inner_sum(c_cont, out_list, j) < upper_bound[0] or inner_sum(m_cont, out_list, j) < upper_bound[1]):
                    if occurrence[j] + 1 >= initial_length / n:
                        if (inner_sum(c_cont, out_list, j) < upper_bound[2] and inner_sum(m_cont, out_list, j) <
                                upper_bound[3]):
                            out_list[lengthOfList - 1] = -1
                    new_occurrence = []
                    for k in range(0, len(occurrence)):
                        new_occurrence.append(occurrence[k])
                    new_occurrence[len(occurrence) - n + j] = occurrence[len(occurrence) - n + j] + 1
                    recursive_approximate(upper_bound, initial_length, lengthOfList - 1, out_list, out_list_nested,
                                          new_occurrence, False)
                else:
                    out_list[lengthOfList - 1] = -1
                    recursive_approximate(upper_bound, initial_length, 0, out_list, out_list_nested, occurrence, False)

    return out_list_nested


# print(recursive_permutation_calculator(5, [], [], True))
# print(len(recursive_permutation_calculator(5, [], [], True)))

occurrence_nested = []
for i in range(0, n):
    occurrence_nested.append(0)
nested_assignment_lst = recursive_approximate([100000, 100000, 0, 0], len(c_cont), len(c_cont), [], [], occurrence_nested, True)
# print(len(nested_assignment_lst))


def x_calculator(assignment_lst, i, j):
    if assignment_lst[i] == j:
        return 1
    return 0


# summation_calculator function performs the summation we intended to minimize in the first place.
# i.e. sum of the variation of each node's CPU and memory usage.


def summation_calculator(c_cont, m_cont, c_average, m_average, k, n, assignment_lst):
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
